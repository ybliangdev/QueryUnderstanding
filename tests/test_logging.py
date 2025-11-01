import json

from app.logging import get_json_logger


def test_json_logger_single_handler_and_format(capsys):
	logger = get_json_logger("qu-test")
	# calling twice should not duplicate handlers
	logger2 = get_json_logger("qu-test")
	assert logger is logger2
	assert len(logger.handlers) == 1

	logger.info("hello", extra={"extra": {"foo": "bar"}})
	captured = capsys.readouterr()
	out = captured.out.strip()
	assert out, "expected log output on stdout"
	payload = json.loads(out)
	assert payload["level"] == "INFO"
	assert payload["message"] == "hello"
	assert payload["logger"] == "qu-test"
	assert "time" in payload
	assert payload.get("foo") == "bar"
