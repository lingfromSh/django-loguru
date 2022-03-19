# django-loguru

Use loguru in Django.

## Installation

```
pip install dj_loguru
```

## Roadmap

- [x] Replace logging handler with loguru sink
- [x] Configure loguru like logging in Django
- [x] Add support for logging propagate
- [x] Add support for levels
- [ ] Add support for filters
- [ ] Add info about django into extra
- [ ] Add built-in formats  
- [ ] Add built-in middlewares for logging different kinds of info (like request, orm operations, cache)  

## Usage

The only thing you need to do is set `LOGGING_CONFIG` to `None` and configure your own logging like using loguru.

```python
LOGGING_CONFIG = None

LOGGING = {
    "formats": {
        "default": "<green>ts={time:YYYY-MM-DD HH:mm:ss.SSS}</green> |"
        " <level>level={level:<8}</level> |"
        " <cyan>file={file}</cyan> <cyan>module={module}</cyan> <cyan>func={function}</cyan> <cyan>line={line}</cyan>"
        " - <level>{message}</level>",
    },
    "sinks": {
        "console": {
            "output": sys.stderr,
            "format": "default",
            "level": "DEBUG",
        },
        "file": {
            "output": "/tmp/log.log",
            "format": "default",
            "level": "DEBUG",
            "rotation": "1 day",
        },
    },
    "loggers": {
        "dj_loguru": {
            "sinks": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
```
