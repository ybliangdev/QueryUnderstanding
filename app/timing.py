import time


def now_ms() -> int:
	return int(time.perf_counter() * 1000)


def elapsed_ms(start_ms: int) -> int:
	return max(0, now_ms() - start_ms)


