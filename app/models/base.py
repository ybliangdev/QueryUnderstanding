from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


IntentDict = Dict[str, object]
EntityDict = Dict[str, object]


class QUModel(ABC):
	"""Abstract QU model interface."""

	@abstractmethod
	def predict(self, raw_text: str, normalized_text: str) -> Tuple[IntentDict, List[EntityDict]]:
		"""Return intent and entities extracted from the input text."""
		raise NotImplementedError


