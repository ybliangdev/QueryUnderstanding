from app.timing import now_ms, elapsed_ms


def test_now_ms_and_elapsed_ms_non_negative():
	start = now_ms()
	end = now_ms()
	assert isinstance(start, int)
	assert isinstance(end, int)
	assert end - start >= 0
	assert elapsed_ms(start) >= 0
