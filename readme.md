## This is a starter for sanic framework

Features:

- use `Database` for async db connection, https://github.com/encode/databases
- auto inject request id to the logger context for correlating events for each request
- common set up for the app entrypoint, app config and logging config
- alembic migration with grabbing `DATABASE_URL` from the config that sanic uses

Example log:
```
2020-06-12 12:47:38,803 89653 INFO c0c72951-6d38-4510-aae3-59c66b44a964 | this is args {'key': ['value']}
2020-06-12 12:47:38,803 89653 INFO c0c72951-6d38-4510-aae3-59c66b44a964 | {"ip": null, "api_client": null, "method": "GET", "path": "/api/v1/demo", "query_string": "key=value", "status_code": 200, "performance_ms": 0.8, "response_body": "{\"key\":[\"value\"]}"}
```


## install conda

## create conda env

```buildoutcfg
conda env create -f env.yaml
```

## Update the db url in `sanic_config.py`

## run server

#### Required envs

```bash
conda activate sanic-start
python main.py
```


## API headers

```buildoutcfg
X-Request-ID
X-Remote-Host
X-Api-Client
```


## Run alembic migration

You need to set the `PYTHONPATH` to the current dir, since in the
`alembic/env.py#L21`, it tries to get the `DATABASE_URL` from the
`sanic_config` so that we only need to store the `DATABASE_URL` in one place


 ## pytest command

See [link](https://docs.pytest.org/en/latest/usage.html#cmdline) for more info.

### Run it in parallel

```
pytest -n <num>
```

### Disable capturing the stdout and stderr in the tests

`pytest -s`

### Stopping after the first (or N) failures

```
pytest -x           # stop after first failure
pytest --maxfail=2  # stop after two failures
```

### To run a specific test within a module

```
pytest test_mod.py::test_func
# or
pytest test_mod.py::TestClass::test_method
```

### Run tests by marker expressions
```
pytest -m slow
```
Will run all tests which are decorated with the `@pytest.mark.slow` decorator.

### Detailed summary report

```
pytest -ra
```

