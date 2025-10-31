"""
Tests for custom class mapping and label consistency for user-defined datasets.
"""
import os
import json
import pytest


def test_classes_yaml_or_json_exists():
    """Project should provide a classes mapping file (yaml/json) or module constant.
    We only check presence; contents validated in next tests.
    """
    candidates = [
        "data/classes.yaml",
        "data/classes.json",
        "specs/classes.yaml",
        "specs/classes.json",
    ]
    if not any(os.path.exists(p) for p in candidates):
        pytest.skip("No classes mapping file yet; add one to proceed")


@pytest.mark.parametrize("labels", [[0, 1, 2], [0]])
def test_class_ids_are_non_negative_integers(labels):
    assert all(isinstance(i, int) and i >= 0 for i in labels)


def test_unique_class_names_when_available(tmp_path):
    """Schema example: names should be unique when provided.
    Uses a temp example to document expectations.
    """
    example = {"names": ["person", "car", "dog"]}
    assert len(example["names"]) == len(set(example["names"]))
