"""
Video processing tests: ensure frame iterator and batching contracts for real-time inference.
"""
import os
import pytest


def test_video_reader_iterable_contract():
    """Expect a video reader util that yields frames (numpy arrays) lazily.
    Skips if util not present yet.
    """
    try:
        from src.video import read_frames  # expected generator: read_frames(path, stride=1)
    except Exception:
        pytest.skip("video.read_frames not implemented yet")

    try:
        it = read_frames("data/sample.mp4")
    except FileNotFoundError:
        pytest.skip("No sample video available yet")
    except NotImplementedError:
        pytest.skip("read_frames stub not ready")

    assert hasattr(it, "__iter__"), "read_frames should return an iterable/generator"


@pytest.mark.parametrize("batch_size", [1, 4])
def test_batching_helper_if_available(batch_size):
    """When batching helper exists, confirm it groups frames to lists of length<=batch_size.
    """
    try:
        from src.video import batch_frames
    except Exception:
        pytest.skip("batch_frames not implemented yet")

    frames = [0, 1, 2, 3, 4]  # stand-in tokens for frames
    batches = list(batch_frames(frames, batch_size))
    assert all(1 <= len(b) <= batch_size for b in batches)
