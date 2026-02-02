# Challenge: HFT Stream Processor (with Cancellations)

In High-Frequency Trading, your system must maintain a persistent "Source of Truth" as messages arrive one by one. Sometimes, a message indicates that a previously sent piece of data is now invalid and must be removed.

## Technical Specifications

### 1. `__init__(self)`
* **Input:** None.
* **Behavior:** Initializes the processor state.

### 2. `add_message(message)`
* **Input Type:** `dict`
* **Key: `"seq"`**: `int` (The unique sequence identifier).
* **Key: `"val"`**: `Any` (The data value; can be `float`, `int`, `str`, or `None`).
* **Key: `"action"`**: `str` (Optional; if present and equals `"CANCEL"`, the sequence is blacklisted).
* **Output:** **None** (The return value is ignored; this method only updates internal state).

### 3. `get_clean_stream()`
* **Input:** None.
* **Output Type:** `list`
* **Format:** A list of values (`val`) only, sorted by their `seq` (ascending).

---

## Processing Rules
1.  **Filter Nulls:** If a message contains `{"val": None}`, ignore it.
2.  **Global Cancellation:** If `{"action": "CANCEL"}` is received for a `seq`, that ID is permanently blacklisted. All existing and future data for that ID must be excluded.
3.  **De-duplication:** For non-blacklisted IDs, keep only the **first** valid value received.

## Example Cases

### Example 1: Basic Logic
- **Action:** `add_message({"seq": 2, "val": "B"})` -> (Returns `None`)
- **Action:** `add_message({"seq": 1, "val": "A"})` -> (Returns `None`)
- **Action:** `add_message({"seq": 2, "val": "C"})` -> (Returns `None`)
- **Result:** `get_clean_stream()` returns `["A", "B"]`.

### Example 2: Cancellation
- **Action:** `add_message({"seq": 10, "val": 100})`
- **Action:** `add_message({"seq": 10, "action": "CANCEL"})`
- **Result:** `get_clean_stream()` returns `[]`.

---

## Local Testing
```bash
pytest test_public.py