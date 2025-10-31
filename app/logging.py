import json
import logging
import sys
from typing import Any, Dict


class JsonFormatter(logging.Formatter):

	def format(self, record: logging.LogRecord) -> str:
		payload: Dict[str, Any] = {
			"level": record.levelname,
			"message": record.getMessage(),
			"logger": record.name,
			"time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
		}
		if hasattr(record, "extra") and isinstance(record.extra, dict):
			payload.update(record.extra)
		return json.dumps(payload, ensure_ascii=False)


def get_json_logger(name: str = "qu") -> logging.Logger:
	logger = logging.getLogger(name)
	if logger.handlers:
		return logger
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(JsonFormatter())
	logger.addHandler(handler)
	logger.propagate = False
	return logger


