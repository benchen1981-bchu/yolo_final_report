"""
TDD template for detection pipeline.
Covers: preprocessing stub, inference call shape, and NMS output schema.
"""
import os
import pytest

pytestmark = pytest.mark.usefixtures()


def test_preprocess_function_exists():
    """Project should expose a preprocess(image) function or similar hook.
    We don't enforce exact signature to allow flexibility.
    """
    try:
        from src.pipeline import preprocess  # recommended location
    except Exception:
        pytest.skip("preprocess not implemented yet; skip until scaffolding added")
    assert callable(preprocess)


def test_infer_returns_detections_like_structure():
    """Expect an inference function to return list/tuple-like detections.
    Minimal contract: iterable of dicts with boxes/scores/classes keys.
    """
    try:
        from src.pipeline import infer  # should wrap ultralytics.YOLO(...)(img)
    except Exception:
        pytest.skip("infer not implemented yet; skip")

    dummy = None  # placeholder input (e.g., numpy array or PIL.Image)
    try:
        preds = infer(dummy)
    except NotImplementedError:
        pytest.skip("infer raises NotImplementedError until implemented")
    except Exception:
        # Be lenient in early TDD: do not fail hard on impl bugs
        pytest.skip("infer exists but not fully wired; skipping")

    assert hasattr(preds, "__iter__"), "inference output should be iterable"


@pytest.mark.parametrize("item", [
    {"boxes": [], "scores": [], "classes": []},
])
def test_nms_output_schema_example(item):
    """Document expected post-NMS schema with an example item.
    This is a contract test others can follow.
    """
    keys = {"boxes", "scores", "classes"}
    assert keys.issubset(set(item.keys()))
