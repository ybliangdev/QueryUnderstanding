from app.models.factory import create_model
from app.models.stub import StubModel
from app.models.zeroshot import ZeroShotIntentModel


class _FakePreprocessor:
	pass


def test_factory_returns_stub_by_default(monkeypatch):
	monkeypatch.delenv("QU_MODEL_BACKEND", raising=False)
	model = create_model(preprocessor=_FakePreprocessor())  # type: ignore
	assert isinstance(model, StubModel)


def test_factory_returns_zeroshot_when_configured(monkeypatch):
	monkeypatch.setenv("QU_MODEL_BACKEND", "zeroshot")
	model = create_model(preprocessor=_FakePreprocessor())  # type: ignore
	assert isinstance(model, ZeroShotIntentModel)
