from collections import deque

import pytest

from temporal.main import TemporalObject


@pytest.fixture
def temporal_object():
    temporal_object = TemporalObject(temporal_depth=3)
    return temporal_object


@pytest.fixture
def filled_temporal_object():
    temporal_object = TemporalObject(temporal_depth=3)
    temporal_object.add("id1", {"value": 10})
    temporal_object.add("id2", {"value": 20})
    temporal_object.add("id3", {"value": 30})
    temporal_object.add("id4", {"value": 40})
    return temporal_object


def test_temporal_object_indexing(filled_temporal_object):
    assert filled_temporal_object[0] == {"value": 40}
    assert filled_temporal_object[-1] == {"value": 30}
    assert filled_temporal_object[-2] == {"value": 20}
    assert filled_temporal_object["id2"] == {"value": 20}
    assert id(filled_temporal_object[-2]) == id(filled_temporal_object.id_index["id2"])
    assert filled_temporal_object.buffer == deque(
        [{"value": 20}, {"value": 30}, {"value": 40}], maxlen=3
    )
    assert list(filled_temporal_object.id_index.keys()) == ["id2", "id3", "id4"]


def test_temporal_object_initialization(temporal_object):
    assert len(temporal_object) == 0


def test_temporal_object_add(temporal_object):
    temporal_object.add("id1", {"value": 10})
    temporal_object.add("id2", {"value": 20})
    temporal_object.add("id3", {"value": 30})
    assert len(temporal_object) == 3
    assert temporal_object.current == {"value": 30}


def test_temporal_object_overflow(temporal_object):
    temporal_object.add("id1", {"value": 10})
    temporal_object.add("id2", {"value": 20})
    temporal_object.add("id3", {"value": 30})
    temporal_object.add("id4", {"value": 40})
    assert len(temporal_object) == 3
    assert temporal_object.current == {"value": 40}
    assert temporal_object["id1"] is None  # state1 should be evicted


def test_temporal_object_index_error(temporal_object):
    temporal_object.add("id1", {"value": 10})
    with pytest.raises(IndexError):
        temporal_object[1]  # Out of range index


def test_temporal_object_invalid_argument_type(temporal_object):
    with pytest.raises(TypeError):
        temporal_object[1.5]  # Invalid argument type


def test_temporal_object_not_implemented_error_slice(temporal_object):
    with pytest.raises(NotImplementedError):
        temporal_object[0:1]  # Slicing not implemented
