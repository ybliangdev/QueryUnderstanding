import re
from typing import List, Optional

import spacy
from spacy.language import Language

from app.config import get_settings


_CONTRACTIONS = {
	"what's": "what is",
	"who's": "who is",
	"where's": "where is",
	"when's": "when is",
	"how's": "how is",
	"it's": "it is",
	"i'm": "i am",
	"you're": "you are",
	"we're": "we are",
	"they're": "they are",
	"can't": "can not",
	"won't": "will not",
	"don't": "do not",
	"doesn't": "does not",
	"didn't": "did not",
	"isn't": "is not",
	"aren't": "are not",
	"wasn't": "was not",
	"weren't": "were not",
	"couldn't": "could not",
	"shouldn't": "should not",
	"wouldn't": "would not",
}


class QueryPreprocessor:
	"""Cleans and normalizes raw text for downstream models."""

	def __init__(self, keep_stopwords: bool = True, remove_punct: bool = True, spacy_model: Optional[str] = None) -> None:
		self.settings = get_settings()
		self.keep_stopwords = keep_stopwords
		self.remove_punct = remove_punct
		model_name = spacy_model or self.settings.spacy_model
		self.nlp: Language = spacy.load(model_name, disable=["parser", "textcat"])  # keep tagger+lemmatizer+ner

	def expand_contractions(self, text: str) -> str:
		def _repl(match: re.Match[str]) -> str:
			c = match.group(0)
			return _CONTRACTIONS.get(c.lower(), c)

		pattern = re.compile(r"\b(" + "|".join(map(re.escape, _CONTRACTIONS.keys())) + r")\b", re.IGNORECASE)
		return pattern.sub(_repl, text)

	def preprocess_to_tokens(self, text: str) -> List[str]:
		if not text:
			return []
		lowered = text.lower()
		expanded = self.expand_contractions(lowered)
		doc = self.nlp(expanded)
		tokens: List[str] = []
		for token in doc:
			if self.remove_punct and token.is_punct:
				continue
			if not self.keep_stopwords and token.is_stop:
				continue
			lemma = token.lemma_.strip()
			if lemma:
				tokens.append(lemma)
		return tokens

	def preprocess_to_text(self, text: str) -> str:
		return " ".join(self.preprocess_to_tokens(text))


