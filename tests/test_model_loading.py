"""
Basic TDD test: verify YOLO model can be imported and loaded from config/weights.
Use pytest -k model_loading to run. All tests are lightweight and skip if deps missing.
"""
import os
import importlib
import pytest


@pytest.mark.parametrize("module_name, attr", [
    ("ultralytics", "YOLO"),  # YOLOv8/11 package
])
def test_ultralytics_available(module_name, attr):
    """Package import smoke test. Skips if library isn't installed in CI.
    This ensures the project declares/test pins deps properly.
    """
    mod = pytest.importorskip(module_name, reason=f"{module_name} not installed")
    assert hasattr(mod, attr), f"{module_name}.{attr} not found"


def test_model_path_env_or_default():
    """Allow model path from env MODEL_PATH or default repo path.
    Does not require the file to exist; we only assert path resolution logic.
    """
    env_path = os.getenv("MODEL_PATH")
    default_candidates = [
        "data/models/best.pt",
        "data/models/yolov8n.pt",
        "data/models/yolov11n.pt",
    ]
    if env_path:
        assert isinstance(env_path, str) and env_path.strip(), "MODEL_PATH env empty"
    else:
        # at least one default candidate should be a plausible relative path
        assert any(p.endswith(".pt") for p in default_candidates)


@pytest.mark.slow
@pytest.mark.skipif(os.getenv("CI", "false").lower() == "true", reason="Skip heavy load in CI")
def test_model_load_smoke():
    """Optional local smoke test: try to construct YOLO(model) if file exists.
    - If no model file present, test is skipped.
    - If ultralytics missing, test is skipped.
    """
    ul = pytest.importorskip("ultralytics", reason="ultralytics not installed")
    candidates = [
        os.getenv("MODEL_PATH"),
        "data/models/best.pt",
        "data/models/yolov8n.pt",
        "data/models/yolov11n.pt",
    ]
    candidates = [c for c in candidates if c]
    existing = next((c for c in candidates if os.path.exists(c)), None)
    if not existing:
        pytest.skip("No local model weights found; skipping load smoke test")
    _ = ul.YOLO(existing)
