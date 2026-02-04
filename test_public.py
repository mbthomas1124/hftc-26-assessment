import pytest
from solution import StreamProcessor


def test_price_priority_execution():
    """
    Requirement: Incoming orders must deplete the most competitive
    prices first (lowest ASK for buyers, highest BID for sellers).
    """
    sp = StreamProcessor()
    # Populate two sell levels
    sp.add_message({"seq": 1, "side": "ASK", "price": 10.0, "volume": 10})
    sp.add_message({"seq": 2, "side": "ASK", "price": 11.0, "volume": 10})

    # Buy order that crosses both levels
    sp.add_message({"seq": 3, "side": "BUY", "price": 11.0, "volume": 15})

    depth = sp.get_book_depth()
    # All volume at 10.0 should be gone, 5 units remain at 11.0
    assert depth["ASKS"] == [(11.0, 5)]
    assert depth["BIDS"] == []


def test_mid_price_calculation():
    """Requirement: Mid-price is the average of the best bid and best ask."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 99.0, "volume": 10})
    sp.add_message({"seq": 2, "side": "ASK", "price": 101.0, "volume": 10})

    assert sp.get_mid_price() == 100.0


def test_order_cancellation():
    """Requirement: CANCEL should remove volume associated with a specific seq."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 50.0, "volume": 100})
    sp.add_message({"seq": 2, "side": "BUY", "price": 50.0, "volume": 50})

    # Verify aggregate volume at the level is 150
    assert sp.get_book_depth()["BIDS"] == [(50.0, 150)]

    # Cancel the first order
    sp.add_message({"seq": 1, "action": "CANCEL"})

    # Volume should now be 50
    assert sp.get_book_depth()["BIDS"] == [(50.0, 50)]


def test_incomplete_book_mid_price():
    """Requirement: Return 0.0 if one or both sides are empty."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 10.0, "volume": 5})
    assert sp.get_mid_price() == 0.0


def test_residual_volume():
    """Requirement: Remaining volume after matching must be added to the book."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "ASK", "price": 100.0, "volume": 10})

    # Buy 25 units at 100.0. 10 match, 15 should rest on the BID side.
    sp.add_message({"seq": 2, "side": "BUY", "price": 100.0, "volume": 25})

    depth = sp.get_book_depth()
    assert depth["ASKS"] == []
    assert depth["BIDS"] == [(100.0, 15)]
