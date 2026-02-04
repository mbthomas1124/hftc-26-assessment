from typing import List, Dict, Tuple, Optional


class StreamProcessor:
    def __init__(self):
        """
        Initialize the internal state of the limit order book.

        The processor must maintain the current volume available at
        each price level and track orders by their sequence ID
        to handle potential cancellations.
        """
        # TODO: Initialize data structures for order tracking and price levels
        pass

    def add_message(self, message: dict) -> None:
        """
        Updates the order book based on the incoming message.

        New orders should be checked against existing price levels on the
        opposite side of the book. Volume should be depleted from the best
        available prices first. Any remaining volume should be stored
        at its specified price level.

        Args:
            message (dict): {
                "seq": int,           # Unique sequence identifier
                "side": str,          # "BUY" or "ASK"
                "price": float,       # Limit price
                "volume": int,        # Quantity
                "action": str         # Optional: "CANCEL"
            }
        """
        # TODO: Implement price-based matching and volume update logic
        pass

    def get_mid_price(self) -> float:
        """
        Calculates the arithmetic mean of the highest buy price and
        the lowest sell price currently in the book.

        Returns:
            float: The mid-price, or 0.0 if the book is one-sided or empty.
        """
        # TODO: Implement mid-price calculation
        pass

    def get_book_depth(self) -> Dict[str, List[Tuple[float, int]]]:
        """
        Provides the current aggregate volume at each price level.

        Returns:
            dict: {
                "BIDS": [(price, total_volume), ...],
                "ASKS": [(price, total_volume), ...]
            }
            BIDS must be sorted by price descending.
            ASKS must be sorted by price ascending.
        """
        # TODO: Implement volume aggregation and sorting
        pass
