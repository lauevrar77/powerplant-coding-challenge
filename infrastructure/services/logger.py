import datetime
import json
from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger

from settings import APP_NAME, DEV

_logger = None


class StructuredFormatter(Formatter):
    def __init__(self, app_name):
        self.app_name = app_name

        super(StructuredFormatter, self).__init__()

    def format(self, record):
        now = datetime.datetime.now()

        content = record.msg
        if not isinstance(content, dict):
            content = {"default": record.msg}

        data = {
            "app_name": self.app_name,
            "timestamp": now.timestamp(),
            "date": f"{now}",
            "log_level": record.levelname,
            "content": record.msg,
            "module": record.module,
            "line_number": record.lineno,
        }

        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            data["stack_trace"] = self.formatStack(record.stack_info)

        return json.dumps(data)


def logger():  # noqa: D103
    global _logger
    if not _logger:
        handler = StreamHandler()
        handler.setLevel(DEBUG if DEV else INFO)

        formatter = StructuredFormatter(APP_NAME)
        handler.setFormatter(formatter)

        _logger = getLogger(APP_NAME)
        _logger.setLevel(DEBUG if DEV else INFO)
        _logger.addHandler(handler)
    return _logger
