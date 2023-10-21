# STREAMZERO FX Executor Helper

 This package can be used for logging and accessing service configuration, parameters, secrets and state through it's context.
 
```python
from fx_ef import context
```

### Accessing package configuration

```python
from fx_ef import context

context.config.get('some_configuration_key')
```

### Accessing execution parameters

```python
from fx_ef import context

context.params.get('param_name')
```

### Accessing secrets

With `fx_ef.context.secrets` you can access secrets stored on platform, project or package level.    

```python
from fx_ef import context

context.secrets.get('secret_name')
```

This command will first lookup for secret named `secret_name` within package secrets (defined in `secrets.json` file of the package). If such key doesn't exist it will lookup for it within project secrets, and finally within platform's secrets. If secret with such name doesn't exist `None` will be returned.

### Setting secrets

Using `fx_ef.context.secrets.set(name, value, context)` method you can set secrets on project and platform level.   

```python
from fx_ef import context

context.secrets.set(name="platform_secret", value={"somekey":"someval"}, context="platform")
```

| Parameter | Description                                                                                 |
|-----------|---------------------------------------------------------------------------------------------|
| name | Name of the secret to be set. If secret with the same name already exist it will be updated |
| value | Value of the secret that should be set |
| context | Context of the secret. Possible values are `platform` and `project` |


### Accessing package id and name

```python
from fx_ef import context

context.package.name
context.package.id
```

### Accessing and updating package state

```python
from fx_ef import context

context.state.get()
context.state.put("some_key", "some_value")
```

### Logging

Available levels: DEBUG, INFO (default), ERROR, WARNING, CRITICAL

```python
from fx_ef import context

context.logging.setLevel('INFO')

context.logging.debug("debug msg")
context.logging.info("info msg")
context.logging.error("error msg")
context.logging.warning("warning msg")
context.logging.critical("critical msg")
```

### Sending events
Used for sending events to the system. Those events can be used to trigger another service execution.

```python
from fx_ef import context

print("sending event with some data")

context.events.send(
    event_type="sample_event_type",
    data={"some_key": "some_val"}
)

```

| Parameter    | Description                                                                                       |
|--------------|---------------------------------------------------------------------------------------------------|
| event_type   | Type of the event (string)                                                                        |
| event_source | Source of the event (if not provided it default to service name of current execution.             |
| data         | Event data (dict)                                                                                 |
| topic        | Name of the topic that event should be sent to. If not provider it will be set to system default. |



### Scheduling retry of service execution

Used for scheduling next execution of the service from within that service script.

```python
from fx_ef import context

context.retry(minutes=0, hours=0, days=0, cron_expression=None, parameters={}):
```

| Parameter       | Description                                                                                                                                                                                                        |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| minutes         | Number of minutes until next execution                                                                                                                                                                   |
| hours           | Number of hours until next execution                                                                                                                                                                     |
| days            | Number of days until next execution                                                                                                                                                                      |
| cron_expression | Cron like expression when next execution should occur. It is not allowed to have `/` in the cron expression (e.g. */2 3 * * *) If `cron_expression` is set `minutes`, `hours` and `days` will be skipped |
| parameters      | Parameters that will be passed to next execution                                                                                                                                                                   |


```python
from fx_ef import context

# retry in 3 minutes
jobid = context.scheduler.retry(minutes=3)

# retry in 3 hours
jobid = context.scheduler.retry(hours=3)

# retry in 3 days
jobid = context.scheduler.retry(days=3)

# retry on 56th minute of next hour
jobid = context.scheduler.retry(cron_expression="56 * * * *")
```


## Using `fx_ef` for local development

To use `fx_ef` for local development and testing without need to run scripts through Executor `EF_ENV=local` env variable must be set. When it is set `fx_ef.context` will be read from local file `ef_env.json` that must be created within same directory as the script that is accessing `fx_ef.context`.  
`ef_env.json` must have following structure:

```json
{
  "params": {
    "package_name": "some_package_name",
    "package_id": "some_package_id",
    "optional_param_1": "param_1_value",
    "optional_param_2": "param_2_value"
  },
  "secrets": {
    "secret_param_1": "secret_1_value",
    "secret_param_2": "secret_2_value"
  },
  "config": {
    "config_param_1": "config_1_value",
    "config_param_2": "config_2_value"
  }
}
```

NOTE: `params`, `package_name` and `package_id` are mandatory.

When `EF_ENV=local` is set, package state is also stored and fetched from the local file `ef_package_state.json` within the same directory. If file does not exist it will be created on the fly. 

By default `context.events.send(...)` will be skipped when local env is set. If event should be sent anyway following should be added in `config` section of the `ef_env.json` file:

```json
{
  "params": {...},
  "secrets": {...},
  "config": {
    "KAFKA_BOOTSTRAP_SERVER": "kafka",
    "KAFKA_PORT": "9092",
    "DEFAULT_TOPIC": "your_topic_name"
  }
}
```

| Parameter              | Description                                                                        |
|------------------------|------------------------------------------------------------------------------------|
| KAFKA_BOOTSTRAP_SERVER | address of the kafka server                                                        |
| KAFKA_PORT             | kafka port                                                                         |
| DEFAULT_TOPIC          | name of the default topic which will be used if it is not passed via send() method |

