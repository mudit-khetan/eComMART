# Data Types, Type Conversion, Mixed Expressions, None and NaN
## eCOMMart AI Squad | Week 3

---

## 1. Python Data Types — Overview

Every value in Python has a **type**. The type tells Python what kind of data it is and what operations are allowed on it.

| Type | Full Name | Example | eCOMMart Use |
|---|---|---|---|
| `int` | Integer | `499` | Quantity, stock count, order ID |
| `float` | Floating point | `499.99` | Price, GST amount, discount |
| `str` | String | `"Wireless Mouse"` | Product name, SKU, city |
| `bool` | Boolean | `True` / `False` | Is in stock, is verified, is COD |
| `NoneType` | None | `None` | Missing field, unset value |
| `list` | List | `["Mouse", "Hub"]` | Cart items, search results |
| `tuple` | Tuple | `("S", "M", "L")` | Fixed size options |
| `dict` | Dictionary | `{"name": "Mouse"}` | Product record, order |
| `set` | Set | `{"C101", "C204"}` | Unique buyer IDs |


![Python Numbers](../../../img/li0.png)

Check a value's type using `type()`:

```python
product_name = "Wireless Mouse"
price        = 499.99
quantity     = 3
is_in_stock  = True
promo_code   = None

print(type(product_name))
print(type(price))
print(type(quantity))
print(type(is_in_stock))
print(type(promo_code))
```
```
# Output:
<class 'str'>
<class 'float'>
<class 'int'>
<class 'bool'>
<class 'NoneType'>
```

---

## 2. Implicit Type Conversion

Python **automatically** converts one type to another when needed — without you asking. This only happens when it is safe and no data will be lost.

**Rule: Python always promotes to the more precise type.**

```
int  +  float  →  float
int  +  bool   →  int
float + bool   →  float
```

```python
# int + float → float
quantity   = 3          # int
unit_price = 199.99     # float

line_total = quantity * unit_price
print(line_total)
print(type(line_total))
```
```
# Output:
599.97
<class 'float'>
```

```python
# int + bool → int  (True = 1, False = 0)
base_items = 5      # int
bonus_item = True   # bool → treated as 1

total_items = base_items + bonus_item
print(total_items)
print(type(total_items))
```
```
# Output:
6
<class 'int'>
```

```python
# float + bool → float
price   = 999.00
on_sale = True      # → 1.0

result = price + on_sale
print(result)
print(type(result))
```
```
# Output:
1000.0
<class 'float'>
```

> ⚠️ Python will **never** implicitly convert `str` to a number:
> ```python
> price = "499"
> total = price + 100    # ❌ TypeError: can only concatenate str (not "int") to str
> ```
> You must convert manually — see Section 3.

---

## 3. Explicit Type Conversion

You control the conversion by calling a conversion function directly.

### 3.1 `int()` — to Integer

```python
# str → int
raw_qty = "5"
qty     = int(raw_qty)
print(qty, type(qty))
```
```
# Output:
5 <class 'int'>
```

```python
# float → int  (truncates — does NOT round)
price = 299.99
p_int = int(price)
print(p_int)
```
```
# Output:
299
```

```python
# bool → int
print(int(True))
print(int(False))
```
```
# Output:
1
0
```

```python
# ❌ These all raise errors — know them before they surprise you
try:
    int("abc")
except ValueError as e:
    print(f"ValueError: {e}")

try:
    int("299.99")       # must convert to float first
except ValueError as e:
    print(f"ValueError: {e}")

try:
    int(None)
except TypeError as e:
    print(f"TypeError: {e}")
```
```
# Output:
ValueError: invalid literal for int() with base 10: 'abc'
ValueError: invalid literal for int() with base 10: '299.99'
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

---

### 3.2 `float()` — to Float

```python
# str → float
raw_price = "1299.99"
price     = float(raw_price)
print(price, type(price))
```
```
# Output:
1299.99 <class 'float'>
```

```python
# int → float
stock = 100
print(float(stock))

# bool → float
print(float(True))
print(float(False))
```
```
# Output:
100.0
1.0
0.0
```

```python
# ❌ Common failures
try:
    float("₹499")    # currency symbol breaks it
except ValueError as e:
    print(f"ValueError: {e}")

try:
    float("")
except ValueError as e:
    print(f"ValueError: {e}")

try:
    float(None)
except TypeError as e:
    print(f"TypeError: {e}")
```
```
# Output:
ValueError: could not convert string to float: '₹499'
ValueError: could not convert string to float: ''
TypeError: float() argument must be a string or a real number, not 'NoneType'
```

---

### 3.3 `str()` — to String

```python
# int → str — useful for building labels
order_id = 20241
label    = "ORD-" + str(order_id)
print(label)
```
```
# Output:
ORD-20241
```

```python
# float → str
price = 499.99
tag   = "Price: ₹" + str(price)
print(tag)
```
```
# Output:
Price: ₹499.99
```

```python
# bool → str
status = str(True)
print(status, type(status))
```
```
# Output:
True <class 'str'>
```

---

### 3.4 `bool()` — to Boolean

**Falsy values** — these all evaluate to `False`:

| Value | `bool()` |
|---|---|
| `0` | `False` |
| `0.0` | `False` |
| `""` | `False` |
| `None` | `False` |
| `[]` | `False` |
| `{}` | `False` |

Everything else is `True`.

```python
print(bool(0))        # False
print(bool(499))      # True
print(bool(""))       # False
print(bool("Mouse"))  # True
print(bool(None))     # False
print(bool([]))       # False
print(bool([1, 2]))   # True
```
```
# Output:
False
True
False
True
False
False
True
```

```python
# Practical use — no need to write == True or == False
stock_qty = 0
cart      = []

if not stock_qty:
    print("Out of stock")       # runs — 0 is falsy

if not cart:
    print("Cart is empty")      # runs — [] is falsy
```
```
# Output:
Out of stock
Cart is empty
```

---

## 4. Mixed-Type Expressions

A **mixed-type expression** combines values of different types in one statement.

### 4.1 Numeric mixing — safe, Python promotes automatically

```python
# int + float → float
items = 4           # int
price = 149.99      # float
total = items * price
print(total)        # float
```
```
# Output:
599.96
```

```python
# int arithmetic — division always gives float
a = 10
b = 3
print(a + b)    # 13   int
print(a / b)    # 3.333... float — division ALWAYS returns float
print(a // b)   # 3    int — floor division
```
```
# Output:
13
3.3333333333333335
3
```

---

### 4.2 String + number — always an error

```python
product = "Wireless Mouse"
price   = 499

# ❌ This fails
try:
    print(product + price)
except TypeError as e:
    print(f"TypeError: {e}")

# ✅ Fix 1: convert number to str
print(product + " costs ₹" + str(price))

# ✅ Fix 2: use f-string — handles conversion automatically
print(f"{product} costs ₹{price}")
```
```
# Output:
TypeError: can only concatenate str (not "int") to str
Wireless Mouse costs ₹499
Wireless Mouse costs ₹499
```

---

### 4.3 bool in numeric expressions

```python
is_prime_member = True    # → 1
base_discount   = 10      # %

total_discount = base_discount + (5 * is_prime_member)
print(total_discount)     # 10 + 5×1 = 15
```
```
# Output:
15
```

---

### 4.4 Comparison always returns bool

```python
price    = 1500
min_free = 500

result = price > min_free
print(result)
print(type(result))

# Chain comparisons — Python supports this naturally
print(500 <= price <= 3000)
```
```
# Output:
True
<class 'bool'>
True
```

---

### 4.5 Common mixed-type mistakes in eCOMMart context

```python
# Mistake 1: input() always returns str — easy to forget
qty_raw = "3"            # simulating: qty_raw = input("Enter quantity: ")
# total = 499 * qty_raw  # ❌ TypeError
total   = 499 * int(qty_raw)   # ✅ convert first
print(total)

# Mistake 2: comparing str to int
price_from_form = "1500"              # came from web form
if int(price_from_form) > 1000:       # ✅ convert first
    print("Eligible for discount")

# Mistake 3: string * int repeats, not multiplies
sku = "WM"
print(sku * 3)    # WMWMWM  ← string repetition, not math
```
```
# Output:
1497
Eligible for discount
WMWMWM
```

---

## 5. None — The Null Value

`None` is Python's way of representing **the absence of a value**. It is its own type: `NoneType`.

```python
delivery_note = None    # customer gave no special instructions
promo_code    = None    # no coupon applied
rating        = None    # product not yet rated
```

### None is NOT the same as zero or empty string

```python
a = None    # no value at all
b = 0       # the number zero
c = ""      # an empty string
d = False   # boolean false

print(a == b)   # False
print(a == c)   # False
print(a == d)   # False
```
```
# Output:
False
False
False
```

```
None  → field does not exist or was not provided
0     → a quantity of zero — a valid value
""    → a field exists but is blank
False → a deliberate True/False answer
```

### Checking for None — always use `is`, not `==`

```python
promo_code = None

# ✅ Correct
if promo_code is None:
    print("No promo code applied.")

if promo_code is not None:
    print(f"Applying promo: {promo_code}")
```
```
# Output:
No promo code applied.
```

### None in functions — default return value

```python
# A function with no return statement returns None
def log_order(order_id):
    print(f"Order {order_id} logged.")
    # no return statement

result = log_order("ORD-2041")
print(result)
print(type(result))
```
```
# Output:
Order ORD-2041 logged.
None
<class 'NoneType'>
```

### None as a safe default in function parameters

```python
def create_order(product, delivery_note=None):
    print(f"Product: {product}")
    if delivery_note is None:
        print("No special delivery note.")
    else:
        print(f"Note: {delivery_note}")

create_order("Wireless Mouse")
create_order("Laptop Stand", "Leave at door.")
```
```
# Output:
Product: Wireless Mouse
No special delivery note.
Product: Laptop Stand
Note: Leave at door.
```

---

## 6. NaN — Not a Number

`NaN` stands for **Not a Number**. It is a special `float` value representing an undefined or unrepresentable numeric result.

### Where NaN comes from

```python
import math

# Created explicitly
a = float('nan')
print(a)
print(type(a))          # NaN is a float — not a new type

# From math operations
b = float('inf') - float('inf')
print(b)                # undefined result → nan
```
```
# Output:
nan
<class 'float'>
nan
```

### The strangest thing about NaN — it is not equal to itself

```python
x = float('nan')

print(x == x)     # False ← NaN is the only value not equal to itself
print(x != x)     # True
print(x > 0)      # False
print(x < 0)      # False
print(x == 0)     # False
```
```
# Output:
False
True
False
False
False
```

> This is why you **cannot use `== float('nan')`** to check for NaN — it always returns `False`.

### How to correctly detect NaN

```python
import math

x = float('nan')

print(math.isnan(x))         # True  ✅ — correct way
print(x == float('nan'))     # False ❌ — never use this
```
```
# Output:
True
False
```

### NaN vs None — they are different

```python
import math

none_value = None
nan_value  = float('nan')

print(type(none_value))          # NoneType
print(type(nan_value))           # float

print(none_value is None)        # True
print(math.isnan(nan_value))     # True

# None in math → crashes; NaN in math → propagates as NaN
print(nan_value + 1)             # nan  (no error)
```
```
# Output:
<class 'NoneType'>
<class 'float'>
True
True
nan
```

```
┌──────────────────────────────────────────────────────────────┐
│  None  → no value at all — field missing or not provided     │
│  NaN   → a bad numeric result — undefined or corrupted data  │
│  type(None) = NoneType   type(NaN) = float                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 7. The `is_nan()` Pattern — Handles Both in One Function

In real eCOMMart data pipelines, a missing price field can arrive as `None`, `float('nan')`, or `""` depending on the source system. This function handles all three safely:

```python
import math

def is_nan(value):
    """
    Returns True if a value is missing, undefined, or not usable as a number.
    Handles: None, float('nan'), and empty string.

    Agent Tool Note:
        Call this before any numeric comparison to prevent crashes
        when data arrives from forms, APIs, or CSV files.
    """
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False

# Test
test_values = [499.0, None, float('nan'), "", "1299", 0]
for v in test_values:
    print(f"  {repr(v):<15} → is_nan: {is_nan(v)}")
```
```
# Output:
  499.0           → is_nan: False
  None            → is_nan: True
  nan             → is_nan: True
  ''              → is_nan: True
  '1299'          → is_nan: False
  0               → is_nan: False
```

> `0` is **not** NaN — it is a valid number (zero stock, zero discount). Check `> 0` separately if your business logic requires a positive value.

---

## Quick Reference

| Concept | Key Rule | eCOMMart Example |
|---|---|---|
| Implicit conversion | `int + float → float` automatically | `3 * 199.99 = 599.97` |
| Explicit conversion | Call `int()`, `float()`, `str()`, `bool()` | `int(input())` for quantity |
| Mixed str + int | Always a `TypeError` — use f-string or `str()` | `"Price: ₹" + str(499)` |
| `None` check | Use `is None` / `is not None` | `if promo_code is None` |
| NaN check | Use `math.isnan()` — never `== float('nan')` | `if math.isnan(price)` |
| NaN type | NaN is a `float`, not a separate type | `type(float('nan')) → float` |
| None vs NaN | `None` = no value; `NaN` = bad numeric result | Missing field vs corrupted field |

---

## Tasks

### Task 1: eCOMMart Type Conversion Sampler

Convert each eCOMMart value to the types shown and print a formatted table.

```python
# Starting values
price_str     = "1299"     # string price from a form
qty_float     = 2.0        # float quantity from an API
in_stock_int  = 1          # integer flag (1 = in stock)
product_id    = 5001       # integer used to build a SKU
discount_bool = True       # boolean discount flag

print("=" * 60)
print(f"  {'Original':<20} {'Type':<12} {'Converted':<15} {'New Type'}")
print("=" * 60)

# price_str → int
p_int = int(price_str)
print(f"  {repr(price_str):<20} {type(price_str).__name__:<12} {p_int:<15} {type(p_int).__name__}")

# qty_float → int  (truncates)
q_int = int(qty_float)
print(f"  {repr(qty_float):<20} {type(qty_float).__name__:<12} {q_int:<15} {type(q_int).__name__}")

# in_stock_int → bool
is_bool = bool(in_stock_int)
print(f"  {repr(in_stock_int):<20} {type(in_stock_int).__name__:<12} {is_bool:<15} {type(is_bool).__name__}")

# product_id → str (build SKU)
sku = "SKU-" + str(product_id)
print(f"  {repr(product_id):<20} {type(product_id).__name__:<12} {repr(sku):<15} {type(sku).__name__}")

# discount_bool → float
d_float = float(discount_bool)
print(f"  {repr(discount_bool):<20} {type(discount_bool).__name__:<12} {d_float:<15} {type(d_float).__name__}")
print("=" * 60)
```
```
# Expected Output:
============================================================
  Original             Type         Converted       New Type
============================================================
  '1299'               str          1299            int
  2.0                  float        2               int
  1                    int          True            bool
  5001                 int          'SKU-5001'      str
  True                 bool         1.0             float
============================================================
```

**Key points:**
- `int("1299")` works; `int("1299.99")` raises `ValueError` — use `float()` first for decimals
- `int(2.0)` → `2` — truncates, does not round
- `int(True)` → `1`, `int(False)` → `0` — booleans are a subclass of int

---

### Task 2: Safe Cart Input

Build a cart entry loop that safely handles bad price and quantity input from the user.

```python
import math

def safe_eval_price(raw):
    """Safely converts a string to float. Returns None on failure."""
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

print("eCOMMart Cart — Enter items (type 'done' to stop)\n")

cart = []
while True:
    name = input("Item name (or 'done'): ").strip()
    if name.lower() == "done":
        break

    raw_price = input(f"Price of {name} (₹): ").strip()
    price = safe_eval_price(raw_price)
    if price is None or price <= 0:
        print(f"  ⚠️  Invalid price '{raw_price}' — skipping.\n")
        continue

    raw_qty = input(f"Quantity: ").strip()
    try:
        qty = int(raw_qty)
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
    except ValueError as e:
        print(f"  ⚠️  Invalid quantity '{raw_qty}' — {e} — skipping.\n")
        continue

    total = price * qty
    cart.append({"name": name, "price": price, "qty": qty})
    print(f"  ✅ Added: {name} x{qty} = ₹{total:.2f}\n")

print(f"\nCart has {len(cart)} item(s).")
```

**Key points:**
- `safe_eval_price()` handles price — returns `None` on failure, never crashes
- `int()` inside `try/except ValueError` handles quantity cleanly
- Always validate `> 0` after converting — `float("0")` succeeds but a zero price is logically wrong

---

### Task 3: Type Detective

Given a list of raw catalog prices in mixed types, classify each one.

```python
import math

def safe_eval_price(raw):
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

raw_catalog_prices = [499, "850.00", "1,299", None, True, "FREE", 0, "", "2999.99", False]

print(f"  {'Raw Value':<15} {'Original Type':<12} {'As Float':<12} {'Usable?'}")
print("  " + "─" * 55)

for raw in raw_catalog_prices:
    original_type = type(raw).__name__
    converted     = safe_eval_price(raw)
    usable        = converted is not None and converted > 0

    if usable:
        display = f"₹{converted:.2f}"
        status  = "✅ Yes"
    elif converted == 0.0:
        display = "0.0"
        status  = "⚠️  Zero"
    else:
        display = "—"
        status  = "❌ No"

    print(f"  {repr(raw):<15} {original_type:<12} {display:<12} {status}")
```
```
# Expected Output:
  Raw Value       Original Type As Float     Usable?
  ───────────────────────────────────────────────────────
  499             int          ₹499.00      ✅ Yes
  '850.00'        str          ₹850.00      ✅ Yes
  '1,299'         str          —            ❌ No
  None            NoneType     —            ❌ No
  True            bool         ₹1.00        ✅ Yes
  'FREE'          str          —            ❌ No
  0               int          0.0          ⚠️  Zero
  ''              str          —            ❌ No
  '2999.99'       str          ₹2999.99     ✅ Yes
  False           bool         0.0          ⚠️  Zero
```

**Key points:**
- `"1,299"` fails `float()` — commas must be stripped first with `.replace(",", "")`
- `True` converts to `1.0` — booleans are valid numbers; a price of `₹1.00` from `True` is logically wrong
- `0` converts successfully but is not a usable price — always check `> 0` separately
