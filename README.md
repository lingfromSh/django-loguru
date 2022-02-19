# django-loguru

Use loguru in Django.

## Installation

```
pip install dj_loguru
```

## Usage

The only thing you need to do is set `LOGGING_CONFIG` to `None` and configure your own logging.

```python
LOGGING_CONFIG = None

LOGGING = {
    "formats": {
        ...
    },
    "sinks": {

    },
    "loggers": {

    }
}
```
