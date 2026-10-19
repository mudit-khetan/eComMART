# Exceptions

Exceptions are events that change the normal flow of a program. Python raises them automatically when errors occur — and you can also raise them deliberately in your own code.

Handling exceptions properly is what separates code that crashes in production from code that recovers gracefully and gives users a meaningful message.

**What we will cover:**

1. `try/except` — catching and recovering from errors
2. `try/except/else/finally` — the full pattern
3. `raise` — triggering exceptions deliberately
4. `assert` — conditional triggers for validation
5. Custom exceptions
6. `with/as` — context managers
7. Custom context managers
8. Exercise — eCOMMart order validation pipeline

---

## 1. `try/except` — Catching and Recovering

Wrap code that might fail in a `try` block. If an exception is raised, the matching `except` block runs instead of crashing:

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Caught: {e}")
```
```
# Output:
Caught: division by zero
```

```python
try:
    number = int("not_a_number")
except ValueError as e:
    print(f"Caught: {e}")
```
```
# Output:
Caught: invalid literal for int() with base 10: 'not_a_number'
```

### Catching multiple exception types

```python
try:
    # statements that might raise an error
    pass
except ValueError:
    # runs if ValueError is raised
    pass
except (TypeError, KeyError):
    # runs if either TypeError or KeyError is raised
    pass
except Exception as e:
    # runs for any other exception; e holds the exception object
    pass
```

### B2B eCom — safe price conversion

```python
def safe_convert_price(raw):
    """
    Safely converts raw input to a float price.

    Returns None if the input is invalid rather than crashing.
    """
    try:
        price = float(raw)
        if price < 0:
            raise ValueError(f"Price cannot be negative: {price}")
        return price
    except (ValueError, TypeError) as e:
        print(f"  Invalid input {raw!r}: {e}")
        return None
```

```python
for v in ['499', '1299.99', 'free', None, '-50', '2 000']:
    result = safe_convert_price(v)
    if result is not None:
        print(f"  {str(v)!r:12} → ₹{result:.2f}")
```
```
# Output:
  '499'        → ₹499.00
  '1299.99'    → ₹1299.99
  Invalid input 'free': could not convert string to float: 'free'
  Invalid input None: float() argument must be a string or a real number, not 'NoneType'
  Invalid input '-50': Price cannot be negative: -50.0
  Invalid input '2 000': could not convert string to float: '2 000'
```

---

## 2. `try/except/else/finally` — The Full Pattern

```
try:
    # code that might raise an exception
except SomeError:
    # runs ONLY if that exception was raised
else:
    # runs ONLY if NO exception was raised
finally:
    # ALWAYS runs — exception or not (use for cleanup)
```

```python
list_of_numbers   = list(range(1, 100))
dictionary_of_numbers = {n**2: n for n in list_of_numbers}
```

**Case 1 — no exception raised:**

```python
try:
    index = list_of_numbers.index(2)       # 2 is at position 1
    value = dictionary_of_numbers[index]   # key 1 → value 1
except (ValueError, KeyError) as e:
    print(f"Error: {e}")
else:
    print(f"Found number at position {index}: {value}")
finally:
    print("Cleanup complete")
```
```
# Output:
Found number at position 1: 1
Cleanup complete
```

**Case 2 — ValueError raised (200 not in list):**

```python
try:
    index = list_of_numbers.index(200)     # 200 not in list → ValueError
    value = dictionary_of_numbers[index]
except (ValueError, KeyError) as e:
    print(f"Error: {e}")
else:
    print(f"Found number at position {index}: {value}")
finally:
    print("Cleanup complete")
```
```
# Output:
Error: 200 is not in list
Cleanup complete
```

```
┌──────────────────────────────────────────────────────────────┐
│  try     → always runs first                                 │
│  except  → runs ONLY if an exception was raised in try       │
│  else    → runs ONLY if NO exception was raised              │
│  finally → ALWAYS runs, even if there was an exception       │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. `raise` — Triggering Exceptions Deliberately

Use `raise` to signal that something has gone wrong. This lets you enforce your own rules and give callers a clear error message:

```python
def validate_price(price):
    """
    Validates a product price.

    Raises:
        TypeError  if price is not a number.
        ValueError if price is negative.
    """
    if not isinstance(price, (int, float)):
        raise TypeError(f"Price must be a number, got {type(price).__name__!r}")
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price}")
    return price
```

```python
for p in [499, -100, 'free']:
    try:
        print(f"  Valid: ₹{validate_price(p)}")
    except (TypeError, ValueError) as e:
        print(f"  Error: {e}")
```
```
# Output:
  Valid: ₹499
  Error: Price cannot be negative: -100
  Error: Price must be a number, got 'str'
```

```
validate_price(-100)
    → raise ValueError("Price cannot be negative: -100")
    → caller's except ValueError block catches it
    → program continues cleanly
```

---

## 4. `assert` — Conditional Triggers for Validation

`assert` is shorthand for "this must be true — if not, raise an `AssertionError`". Use it to enforce preconditions:

```python
def process_bulk_order(product, qty):
    """Validates and processes a bulk order."""
    assert isinstance(qty, int), f"Quantity must be an integer, got {type(qty).__name__}"
    assert qty > 0,              f"Quantity must be positive, got {qty}"
    assert qty <= 1000,          f"Bulk order limit is 1000 units, got {qty}"
    return f"Bulk order accepted: {qty} × {product}"
```

```python
for product, qty in [('Wireless Mouse', 50), ('USB Hub', 0), ('Laptop Stand', 1500)]:
    try:
        print(f"  {process_bulk_order(product, qty)}")
    except AssertionError as e:
        print(f"  AssertionError: {e}")
```
```
# Output:
  Bulk order accepted: 50 × Wireless Mouse
  AssertionError: Quantity must be positive, got 0
  AssertionError: Bulk order limit is 1000 units, got 1500
```

```
assert condition, "message"
  ↓ if condition is True  → nothing happens, code continues
  ↓ if condition is False → raises AssertionError("message")
```

> **`raise` vs `assert`:**
> Use `raise` for errors that can happen in normal use (bad user input, network failure).
> Use `assert` for conditions that should **never** be false if your code is correct — programmer errors, not user errors.

---

## 5. Custom Exceptions

Define your own exception classes by inheriting from `Exception`. Custom exceptions make your error messages precise and let callers catch only the errors they care about:

```python
class InsufficientStockError(Exception):
    """Raised when an order quantity exceeds available stock."""

    def __init__(self, product, requested, available):
        self.product   = product
        self.requested = requested
        self.available = available
        super().__init__(self.__str__())

    def __str__(self):
        return (f"Cannot fulfil '{self.product}': "
                f"requested {self.requested}, only {self.available} available.")


class InvalidSKUError(Exception):
    """Raised when a product SKU does not match the required format."""

    def __init__(self, sku):
        self.sku = sku
        super().__init__(f"Invalid SKU format: {sku!r}")
```

```python
def place_order(product, requested_qty, available_qty):
    if requested_qty > available_qty:
        raise InsufficientStockError(product, requested_qty, available_qty)
    return f"Order placed: {requested_qty} × {product}"


def is_valid_sku(sku):
    """SKU must be a string, start with a letter, and be 4–10 characters."""
    if not isinstance(sku, str): return False
    if not sku[0].isalpha():     return False
    if not (4 <= len(sku) <= 10): return False
    return True


def lookup_product(sku):
    if not is_valid_sku(sku):
        raise InvalidSKUError(sku)
    return f"Product found: {sku}"
```

```python
# Test InsufficientStockError
for prod, req, avail in [('Wireless Mouse', 5, 10), ('Laptop Stand', 8, 3)]:
    try:
        print(f"  {place_order(prod, req, avail)}")
    except InsufficientStockError as e:
        print(f"  StockError: {e}")
```
```
# Output:
  Order placed: 5 × Wireless Mouse
  StockError: Cannot fulfil 'Laptop Stand': requested 8, only 3 available.
```

```python
# Test InvalidSKUError
for sku in ['WM4021', 'EB1299', '123', 'AB']:
    try:
        print(f"  {lookup_product(sku)}")
    except InvalidSKUError as e:
        print(f"  SKUError: {e}")
```
```
# Output:
  Product found: WM4021
  Product found: EB1299
  SKUError: Invalid SKU format: '123'
  SKUError: Invalid SKU format: 'AB'
```

```
Exception hierarchy:
    BaseException
        └── Exception          ← inherit from this
                └── InsufficientStockError   (your custom class)
                └── InvalidSKUError          (your custom class)
```

---

## 6. `with/as` — Context Managers

The `with` statement guarantees that cleanup happens — even if an exception is raised. It is most commonly used for file handling:

```python
with open('filename.txt') as f:
    for line in f:
        print(line)
# file is automatically closed here — even if an exception occurred
```

Without `with`, you would need:
```python
f = open('filename.txt')
try:
    for line in f:
        print(line)
finally:
    f.close()   # must close manually — easy to forget
```

### B2B eCom — reading an order file

```python
import io

# Simulating a CSV file of orders
order_data = "ORD-1001,Wireless Mouse,499\nORD-1002,USB Hub,350\nORD-1003,Laptop Stand,850\n"

with io.StringIO(order_data) as f:
    for line in f:
        order_id, product, price = line.strip().split(',')
        print(f"  {order_id}: {product} — ₹{price}")
```
```
# Output:
  ORD-1001: Wireless Mouse — ₹499
  ORD-1002: USB Hub — ₹350
  ORD-1003: Laptop Stand — ₹850
```

### Multiple context managers

```python
# Open two files at once — both are automatically closed
with open('orders.csv') as f1, open('products.csv') as f2:
    for line1, line2 in zip(f1, f2):
        # process both files together
        pass
```

---

## 7. Custom Context Managers

A context manager is any class that implements `__enter__` and `__exit__`. The `with` statement calls `__enter__` on entry and `__exit__` on exit — whether or not an exception was raised:

```python
class TraceBlock:
    def message(self, arg):
        print('running ' + arg)

    def __enter__(self):
        print('starting with block')
        return self             # returned value is bound to 'as' variable

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            print('exited normally\n')
        else:
            print(f'exception raised: {exc_type.__name__}\n')
            return False        # False means: re-raise the exception
```

**No exception — normal exit:**

```python
with TraceBlock() as action:
    action.message('test 1')
    print('reached')
```
```
# Output:
starting with block
running test 1
reached
exited normally
```

**Exception raised — `__exit__` still called:**

```python
try:
    with TraceBlock() as action:
        action.message('test 2')
        raise TypeError('test error')
        print('not reached')       # never runs
except TypeError:
    pass
```
```
# Output:
starting with block
running test 2
exception raised: TypeError
```

```
with TraceBlock() as action:
    ↓
    __enter__() called → returns self → action = self
    ↓
    block runs
    ↓
    __exit__() called — always, exception or not
```

### User-defined exception with a message

```python
class Career(Exception):
    def __init__(self, job, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._job = job

    def __str__(self):
        return f"So I became a {self._job}"

try:
    raise Career('Engineer')
except Career as e:
    print(e)
```
```
# Output:
So I became a Engineer
```

---

## Exercise: eCOMMart — Order Validation Pipeline

Build a multi-step order validation function that uses all five exception tools: `try/except`, `raise`, `assert`, custom exceptions, and `else/finally`.

```python
def get_discount_rate(total):
    if total >= 3000: return 0.25
    elif total >= 2000: return 0.15
    elif total >= 1000: return 0.10
    elif total >= 500:  return 0.05
    else: return 0.0


def process_ecommart_order(product, sku, price_raw, qty_raw, stock):
    """
    Full order validation and processing pipeline.

    Steps:
        1. Validate SKU format
        2. Convert and validate price
        3. Validate quantity
        4. Check stock availability
        5. Calculate and return order summary

    Returns:
        str: 'Approved: ...' or 'Rejected: ...'
    """
    # Step 1 — validate SKU
    try:
        lookup_product(sku)
    except InvalidSKUError as e:
        return f"Rejected: {e}"

    # Step 2 — convert price
    price = safe_convert_price(price_raw)
    if price is None:
        return f"Rejected: invalid price {price_raw!r}"

    # Step 3 — validate quantity
    try:
        qty = int(qty_raw)
        assert qty > 0, "Quantity must be positive"
    except (ValueError, AssertionError) as e:
        return f"Rejected: {e}"

    # Step 4 — check stock
    try:
        place_order(product, qty, stock)
    except InsufficientStockError as e:
        return f"Rejected: {e}"

    # Step 5 — calculate totals
    subtotal  = price * qty
    disc_rate = get_discount_rate(subtotal)
    discount  = round(subtotal * disc_rate, 2)
    grand     = round(subtotal - discount, 2)

    return (f"Approved: {qty} × {product} @ ₹{price:.2f} "
            f"→ subtotal ₹{subtotal:.2f}, "
            f"discount {int(disc_rate*100)}%, grand ₹{grand:.2f}")
```

```python
orders = [
    ('Wireless Mouse', 'WM4021', '499',      3, 10),   # valid
    ('Laptop Stand',   'LS8050', '850',      8,  3),   # insufficient stock
    ('USB Hub',        '123',    '350',      2, 20),   # invalid SKU
    ('Smart Watch',    'SW2999', 'call_us',  1,  5),   # invalid price
    ('Earbuds',        'EB1299', '1299',     0, 15),   # invalid quantity
]

for prod, sku, price, qty, stock in orders:
    result = process_ecommart_order(prod, sku, price, qty, stock)
    print(f"  {result}")
```
```
# Expected Output:
  Approved: 3 × Wireless Mouse @ ₹499.00 → subtotal ₹1497.00, discount 10%, grand ₹1347.30
  Rejected: Cannot fulfil 'Laptop Stand': requested 8, only 3 available.
  Rejected: Invalid SKU format: '123'
  Rejected: invalid price 'call_us'
  Rejected: Quantity must be positive
```

```
┌─────────────────────────────────────────────────────────────┐
│  Exception tools — when to use which                        │
├──────────────┬──────────────────────────────────────────────┤
│  try/except  │  Handle errors that can reasonably occur     │
│  raise       │  Signal that a rule has been violated        │
│  assert      │  Catch programmer errors / invalid state     │
│  Custom exc  │  Give callers specific, catchable error types │
│  finally     │  Guaranteed cleanup (files, connections)     │
│  with/as     │  Automatic cleanup via context manager       │
└──────────────┴──────────────────────────────────────────────┘
```
