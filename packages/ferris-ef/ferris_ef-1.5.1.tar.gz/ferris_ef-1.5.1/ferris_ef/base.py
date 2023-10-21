import json
import os
import sys
import requests
import logging
import uuid
from datetime import datetime, timedelta
from cron_validator import CronValidator

from ferris_cli.v2 import ApplicationConfigurator, FerrisEvents
from ferris_cli.v2.services.config import Consul


# from ferris_cli.v2.services.logging import FerrisLoggingHandler


def get_param(paramname):
    fa = json.loads(sys.argv[1])
    try:
        return fa[paramname]
    except Exception as e:
        print(f"Parameter {paramname} not found!")


def get_secret(secretname):
    fa = json.loads(sys.argv[1])
    try:
        return fa['secrets'][secretname]
    except Exception as e:
        print(f"Secret {secretname} not found!")


class PackageState:

    def __init__(self, package, config):
        self._package = package
        self._package_state_key = f"{self._package.name}.state"
        self.consul = Consul(
            consul_host=config.get('CONSUL_HOST'),
            constul_port=config.get('CONSUL_PORT')
        )

    def get(self):
        index, data = self.consul.client.kv.get(self._package_state_key, index=None)
        return json.loads(data['Value']) if data and 'Value' in data else {}

    def put(self, key, value):
        try:
            state = self.get()
        except Exception as e:
            state = {}

        state[key] = value
        self.consul.put_item(self._package_state_key, json.dumps(state))


class PackageStateLocal:

    def __init__(self, package, config):
        self._package = package
        self._package_state_key = "ef_package_state.json"

        if not os.path.isfile(self._package_state_key):
            with open(self._package_state_key, 'w') as sf:
                json.dump({}, sf)

    def get(self):
        sf = open(self._package_state_key)
        data = json.load(sf)

        return data

    def put(self, key, value):
        state = self.get()
        state[key] = value

        with open(self._package_state_key, 'w') as sf:
            json.dump(state, sf)


class Secrets:

    def __init__(self, secrets, config, package=None):
        self.secrets = secrets
        self.package = package
        self.config = config

    def get(self, name):
        return self.secrets.get(name) or self._get_from_api(name)

    def set(self, name, value, context):
        r = requests.post(
            url=f"{os.environ.get('SECRETS_API_URL')}",
            json=dict(
                name=name,
                value=value,
                context=context,
                package_id=self.package.id or None
            )
        )

        return r.status_code, r.text

    def _get_from_api(self, name):
        r = requests.get(
            url=f"{os.environ.get('SECRETS_API_URL')}by-name",
            params=dict(
                name=name,
                package_id=self.package.id
            )
        ).json()

        return r.get('value') or None


class SecretsLocal:

    def __init__(self, secrets, package=None):
        self.secrets = secrets
        self.package = package

    def get(self, name):
        return self.secrets.get(name, {})


class Package:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class Scheduler:

    def __init__(self, package, config, _is_local_env=False):
        self.package = package
        self.config = config
        self._is_local_env = _is_local_env

    def schedule(self, minutes=0, hours=0, days=0, cron_expression=None, parameters={}):
        if not (minutes or hours or days or cron_expression):
            return "At least on of minutes/hours/days/cron_expression must be set"

        if not cron_expression:
            time_now = datetime.now()

            scheduled_time = time_now + timedelta(minutes=minutes) + timedelta(hours=hours) + timedelta(days=days)

            cron_expression = f"{scheduled_time.minute} {scheduled_time.hour} {scheduled_time.day} {scheduled_time.month} *"

        try:
            CronValidator.parse(cron_expression)
        except Exception as e:
            return str(e)

        if self._is_local_env:
            return "OK"

        r = requests.post(
            url=f"{os.environ.get('SERVICES_API_URL')}{self.package.id}/schedule",
            json=dict(
                name=self.package.name,
                source=self.config.get('APP_NAME'),
                schedule=cron_expression,
                parameters=parameters
            )
        )

        return json.loads(r.text).get("scheduled_job_id")

    def retry(self, minutes=0, hours=0, days=0, cron_expression=None, parameters={}):
        return self.schedule(minutes, hours, days, cron_expression, parameters)

    # def delete(self, job_id):
    #     r = requests.delete(
    #         url=f"{os.environ.get('SERVICES_API_URL')}/schedule",
    #     )


class FXEvents:

    def __init__(self, params={}, logger=None, config={}):
        self.params = params
        self.logger = logger
        self.config = config

    def send(self, event_type, event_source=None, data={}, topic=None, reference_id=None):
        data['_fxcid'] = self.params.get('_fxcid', str(uuid.uuid4()))
        data['_fxparentexec'] = self.params.get('_fxexec', str(uuid.uuid4()))

        if not event_source:
            event_source = self.params.get('package_name', "ferris.apps.executor")

        if self.config.get('LOG_EVENTS', True) and self.logger:
            self.logger.info("SENDING EVENT: ")
            self.logger.info(
                dict(
                    event_type=event_type,
                    event_source=event_source,
                    data=data,
                    topic=topic,
                    reference_id=reference_id
                )
            )

        if not self.config['_is_local_env']:
            FerrisEvents().send(
                event_type=event_type,
                event_source=event_source,
                data=data,
                topic=topic,
                reference_id=reference_id
            )
