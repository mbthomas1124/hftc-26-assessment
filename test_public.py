import pytest
from solution import StreamProcessor
import sys


if sys.version_info.major != 3 or sys.version_info.minor != 11:
    print("-" * 60)
    print("ENVIRONMENT ERROR: Python 3.11 is required for this assessment.")
    print(f"You are currently running: {sys.version.split()[0]}")
    print("Please switch to Python 3.11 to avoid compatibility issues with the grader.")
    print("-" * 60)
    sys.exit(1)


def test_price_priority_execution():
    """
    Requirement 2: Execution always occurs at the most favorable price.
    Incoming BUY must deplete the lowest SELL (Ask) prices first.
    """
    sp = StreamProcessor()
    # Populate two sell levels (Asks)
    sp.add_message({"seq": 1, "side": "SELL", "price": 10.0, "volume": 10})
    sp.add_message({"seq": 2, "side": "SELL", "price": 11.0, "volume": 10})

    # Buy order that crosses both levels.
    # Logic: Should take 10 units at 10.0, then 5 units at 11.0.
    sp.add_message({"seq": 3, "side": "BUY", "price": 11.0, "volume": 15})

    depth = sp.get_book_depth()
    # All volume at 10.0 should be gone, 5 units remain at 11.0
    assert depth["ASKS"] == [(11.0, 5)]
    assert depth["BIDS"] == []


def test_mid_price_calculation():
    """Requirement: Mid-price is the average of the best bid and best ask."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 99.0, "volume": 10})
    sp.add_message({"seq": 2, "side": "SELL", "price": 101.0, "volume": 10})

    # (99.0 + 101.0) / 2 = 100.0
    assert sp.get_mid_price() == 100.0


def test_order_cancellation():
    """Requirement: CANCEL removes volume associated with a specific sequence identifier."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 50.0, "volume": 100})
    sp.add_message({"seq": 2, "side": "BUY", "price": 50.0, "volume": 50})

    # Verify aggregate volume at the level is 150
    assert sp.get_book_depth()["BIDS"] == [(50.0, 150)]

    # Cancel the first order.
    # Note: We include side/price/volume to match the dict schema, even if action is CANCEL.
    sp.add_message(
        {"seq": 1, "side": "BUY", "price": 50.0, "volume": 100, "action": "CANCEL"}
    )

    # Remaining volume should only be from seq 2
    assert sp.get_book_depth()["BIDS"] == [(50.0, 50)]


def test_incomplete_book_mid_price():
    """Requirement: Return 0.0 if the book lacks orders on either side."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 10.0, "volume": 5})
    # ASKS side is empty, so mid-price must be 0.0
    assert sp.get_mid_price() == 0.0


def test_book_depth_sorting():
    """Requirement 3: BIDS ordered descending, ASKS ordered ascending."""
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "BUY", "price": 10.0, "volume": 5})
    sp.add_message({"seq": 2, "side": "BUY", "price": 12.0, "volume": 5})
    sp.add_message({"seq": 3, "side": "SELL", "price": 20.0, "volume": 5})
    sp.add_message({"seq": 4, "side": "SELL", "price": 18.0, "volume": 5})

    depth = sp.get_book_depth()
    assert depth["BIDS"] == [(12.0, 5), (10.0, 5)]  # Correct: High to Low
    assert depth["ASKS"] == [(18.0, 5), (20.0, 5)]  # Correct: Low to High


def test_residual_volume():
    """
    Requirement 4: Any volume remaining after execution is added to the
    book at its specified price level.
    """
    sp = StreamProcessor()
    sp.add_message({"seq": 1, "side": "SELL", "price": 100.0, "volume": 10})

    # Incoming BUY 25 @ 100.0
    # Logic: 10 match against existing SELL, 15 remain as a new BID at 100.0
    sp.add_message({"seq": 2, "side": "BUY", "price": 100.0, "volume": 25})

    depth = sp.get_book_depth()
    assert depth["ASKS"] == []
    assert depth["BIDS"] == [(100.0, 15)]
