from app.nlp.preprocessor import QueryPreprocessor


def test_preprocessor_basic():
	qp = QueryPreprocessor(keep_stopwords=True, remove_punct=True)
	text = "What's the best pizza place in NYC?"
	norm = qp.preprocess_to_text(text)
	assert norm
	assert "pizza" in norm
	assert "nyc" in norm
	assert "?" not in norm


