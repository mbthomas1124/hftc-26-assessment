# Technical Assessment: Limit Order Book Implementation

## Introduction

This assessment requires the implementation of a **Limit Order Book (LOB)**. A limit order book is a fundamental data structure used in financial markets to organize buy and sell interest by price level. Your objective is to develop a system that accurately maintains the state of the market and handles the depletion of liquidity as orders interact.

### Core Objectives
The system must process a continuous stream of messages to perform the following:

* **Inventory Management:** Track active orders by their unique sequence identifiers to manage volume and handle cancellations.
* **Price Discovery:** Identify matches when an incoming order price overlaps with existing prices on the opposite side of the book.
* **Volume Aggregation:** Provide a clear snapshot of total liquidity available at each price level and calculate the prevailing mid-price.



---

## Technical Specifications

### 1. add_message(message: dict) -> None
Processes market data to update the internal state.
* BUY: An order to purchase a security at a specified price.
* ASK: An order to sell a security at a specified price.
* CANCEL: Removes the volume associated with a specific seq identifier from the book.

### 2. get_mid_price() -> float
Returns the current mid-price, defined as the average of the highest available buy price (Best Bid) and the lowest available sell price (Best Ask).
* If the book lacks orders on either side, the method must return 0.0.

### 3. get_book_depth() -> dict
Returns the total aggregate volume available at each price level.
* Format: {"BIDS": [(price, volume), ...], "ASKS": [(price, volume), ...]}
* Ordering: Bids must be ordered by price in descending order. Asks must be ordered by price in ascending order.

---

## Execution and Price Rules

The processor must prioritize the most competitive prices for all order interactions:

1. Price Compatibility: When a new order arrives, the processor checks for price overlap with the opposite side of the book.
    * A BUY order matches if its price is >= the lowest available sell price.
    * An ASK order matches if its price is <= the highest available buy price.
2. Price Priority: Execution always occurs at the most favorable price currently residing in the book.
    * Incoming Buy orders must deplete the lowest Sell prices first.
    * Incoming Sell orders must deplete the highest Buy prices first.
3. Sequential Fulfillment: If an incoming order has sufficient volume to satisfy multiple price levels, it must continue to execute against subsequent levels until its volume is exhausted or the price is no longer compatible.
4. Residual Volume: Any volume remaining after the execution process is complete is added to the book at its specified price level.



---

## Implementation Requirements

Successful implementations will demonstrate efficient state management. The system should accurately track volume across different price levels and ensure that cancellations correctly reduce the book's total liquidity. Candidates should choose data structures that allow for rapid identification of the best available prices and efficient updates to price-level aggregates.

---

## Testing

A small suite of public tests is provided in test_public.py to verify the core logic of your implementation. You can execute these tests using pytest.

Prerequisites:
Ensure you have pytest installed in your environment:

`pip install pytest`

Running Tests:
To run the assessment tests, execute the following command from the root directory of the project:

`pytest test_public.py`

Validation Criteria:
Your implementation must pass all provided test cases to be considered for review. High-scoring solutions will also be evaluated against a hidden suite of edge cases and performance benchmarks.