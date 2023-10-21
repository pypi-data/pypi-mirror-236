"""Variant tests"""
import pytest
from drift_bytes import Variant


@pytest.mark.parametrize(
    "kind, value",
    [
        ("none", None),
        ("bool", True),
        ("int32", 1),
        ("float32", 1.0),
        ("string", "1"),
        ("uint64", [1, 2, 3, 4]),
    ],
)
def test_init(kind, value):
    """Test Variant init"""
    var = Variant(value, kind)

    assert var.type == kind
    assert var.shape == [len(value)] if isinstance(value, list) else [1]
    assert var.value == value


@pytest.mark.parametrize(
    "kind, value",
    [
        ("none", None),
        ("bool", True),
        ("int64", 1),
        ("float64", 1.0),
        ("string", "1"),
        ("int64", [1, 2, 3, 4]),
    ],
)
def test_init_suggested_type(kind, value):
    """Should suggest type"""
    var = Variant(value)
    assert var.type == kind
    assert var.shape == [len(value)] if isinstance(value, list) else [1]
    assert var.value == value
