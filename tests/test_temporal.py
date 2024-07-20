from collections import deque

import pytest

from temporal.main import TemporalBuffer


@pytest.fixture
def temporal_buffer():
    buffer = TemporalBuffer(temporal_depth=3)
    return buffer


@pytest.fixture
def filled_temporal_buffer():
    buffer = TemporalBuffer(temporal_depth=3)
    buffer.add("id1", {"value": 10})
    buffer.add("id2", {"value": 20})
    buffer.add("id3", {"value": 30})
    buffer.add("id4", {"value": 40})
    return buffer


def test_temporal_buffer_indexing(filled_temporal_buffer):
    assert filled_temporal_buffer[0] == {"value": 40}
    assert filled_temporal_buffer[-1] == {"value": 30}
    assert filled_temporal_buffer[-2] == {"value": 20}
    assert filled_temporal_buffer["id2"] == {"value": 20}
    assert id(filled_temporal_buffer[-2]) == id(filled_temporal_buffer.id_index["id2"])
    assert filled_temporal_buffer.buffer == deque(
        [{"value": 20}, {"value": 30}, {"value": 40}], maxlen=3
    )
    assert list(filled_temporal_buffer.id_index.keys()) == ["id2", "id3", "id4"]


def test_temporal_buffer_initialization(temporal_buffer):
    assert len(temporal_buffer) == 0


def test_temporal_buffer_add(temporal_buffer):
    temporal_buffer.add("id1", {"value": 10})
    temporal_buffer.add("id2", {"value": 20})
    temporal_buffer.add("id3", {"value": 30})
    assert len(temporal_buffer) == 3
    assert temporal_buffer.current == {"value": 30}


def test_temporal_buffer_overflow(temporal_buffer):
    temporal_buffer.add("id1", {"value": 10})
    temporal_buffer.add("id2", {"value": 20})
    temporal_buffer.add("id3", {"value": 30})
    temporal_buffer.add("id4", {"value": 40})
    assert len(temporal_buffer) == 3
    assert temporal_buffer.current == {"value": 40}
    assert temporal_buffer["id1"] is None  # state1 should be evicted


def test_temporal_buffer_index_error(temporal_buffer):
    temporal_buffer.add("id1", {"value": 10})
    with pytest.raises(IndexError):
        temporal_buffer[1]  # Out of range index


def test_temporal_buffer_invalid_argument_type(temporal_buffer):
    with pytest.raises(TypeError):
        temporal_buffer[1.5]  # Invalid argument type


def test_temporal_buffer_not_implemented_error_forward(temporal_buffer):
    with pytest.raises(NotImplementedError):
        temporal_buffer.move_forward()


def test_temporal_buffer_not_implemented_error_backward(temporal_buffer):
    with pytest.raises(NotImplementedError):
        temporal_buffer.move_backward()


def test_temporal_buffer_not_implemented_error_slice(temporal_buffer):
    with pytest.raises(NotImplementedError):
        temporal_buffer[0:1]  # Slicing not implemented
