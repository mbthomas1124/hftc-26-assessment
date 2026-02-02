import pytest
from solution import StreamProcessor


def test_basic_ordering():
    """Requirement: get_clean_stream must return values sorted by seq."""
    sp = StreamProcessor()
    sp.add_message({"seq": 10, "val": "C"})
    sp.add_message({"seq": 1, "val": "A"})
    sp.add_message({"seq": 5, "val": "B"})
    assert sp.get_clean_stream() == ["A", "B", "C"]


def test_de_duplication_first_seen():
    """Requirement: Only the FIRST valid value for a seq ID is kept."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "val": "Keep"})
    sp.add_message({"seq": 1, "val": "Ignore"})
    assert sp.get_clean_stream() == ["Keep"]


def test_null_filtering():
    """Requirement: Messages with val=None must be ignored."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "val": None})
    sp.add_message({"seq": 2, "val": "Valid"})
    assert sp.get_clean_stream() == ["Valid"]


def test_retroactive_cancellation():
    """Requirement: CANCEL action must remove existing data for that seq."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "val": "Value1"})
    sp.add_message({"seq": 2, "val": "Value2"})
    sp.add_message({"seq": 1, "action": "CANCEL"})
    assert sp.get_clean_stream() == ["Value2"]


def test_proactive_cancellation():
    """Requirement: CANCEL action must blacklist future data for that seq."""
    sp = StreamProcessor()
    sp.add_message({"seq": 9, "action": "CANCEL"})
    sp.add_message({"seq": 9, "val": "I am blacklisted"})
    sp.add_message({"seq": 1, "val": "Visible"})
    assert sp.get_clean_stream() == ["Visible"]


def test_mixed_types():
    """Requirement: Values can be of Any type (int, float, str)."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "val": 100})
    sp.add_message({"seq": 2, "val": "string_val"})
    sp.add_message({"seq": 3, "val": 10.5})
    assert sp.get_clean_stream() == [100, "string_val", 10.5]
