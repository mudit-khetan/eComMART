# Week 3 — Solutions
## eCOMMart AI Squad | Python Fundamentals

> ⚠️ **Attempt the exercises yourself first.**
> These solutions are a learning reference — not a shortcut.
> Each solution includes an explanation of the key choices made.

---

## Solution 1 — Product Label with All Three String Types

```python
# Solution 1: eCOMMart Product Label

# Single-quote string — clean, no apostrophes inside
sku      = 'WM-4021'
category = 'Electronics'

# Double-quote string — contains an apostrophe
tagline  = "India's Top Tech Store"

# Triple-quote string — multi-line product description
description = """
    Wireless Ergonomic Mouse
    12-month battery life
    Compatible with Windows & Mac
"""

price    = 499.00
discount = 10               # percent

# Calculate
discount_amt = price * (discount / 100)
final_price  = price - discount_amt

# Print
print("=" * 50)
print(f"  SKU      : {sku}")
print(f"  Category : {category}")
print(f"  Tagline  : {tagline}")
print(f"  MRP      : ₹{price:.2f}")
print(f"  Discount : {discount}%  (-₹{discount_amt:.2f})")
print(f"  You Pay  : ₹{final_price:.2f}")
print(f"\n  Description:{description}")
print("=" * 50)
```
```
# Output:
==================================================
  SKU      : WM-4021
  Category : Electronics
  Tagline  : India's Top Tech Store
  MRP      : ₹499.00
  Discount : 10%  (-₹49.90)
  You Pay  : ₹449.10

  Description:
    Wireless Ergonomic Mouse
    12-month battery life
    Compatible with Windows & Mac

==================================================
```

**Key points:**
- All three quote types are interchangeable for simple strings — the choice depends on what is inside the string
- Triple-quoted strings preserve indentation and newlines exactly as written
- `:.2f` rounds to 2 decimal places and always shows 2 digits after the decimal point

---

## Solution 2 — Price Calculator for 5 Cart Items

```python
# Solution 2: 5-Item Cart Bill

item1_name,  item1_price = "Wireless Mouse", 499.00
item2_name,  item2_price = "USB Hub",        350.00
item3_name,  item3_price = "Phone Case",     199.00
item4_name,  item4_price = "Earbuds Pro",   1299.00
item5_name,  item5_price = "Laptop Stand",   850.00

subtotal = item1_price + item2_price + item3_price + item4_price + item5_price

GST_RATE = 0.18
gst_amt  = subtotal * GST_RATE

discount = 100.00 if subtotal > 1000 else 0.00

grand_total = subtotal + gst_amt - discount

print(f"  {'Item 1 — ' + item1_name:<30} : ₹{item1_price:.2f}")
print(f"  {'Item 2 — ' + item2_name:<30} : ₹{item2_price:.2f}")
print(f"  {'Item 3 — ' + item3_name:<30} : ₹{item3_price:.2f}")
print(f"  {'Item 4 — ' + item4_name:<30} : ₹{item4_price:.2f}")
print(f"  {'Item 5 — ' + item5_name:<30} : ₹{item5_price:.2f}")
print("  " + "─" * 40)
print(f"  {'Subtotal':<30} : ₹{subtotal:.2f}")
print(f"  {'GST (18%)':<30} : ₹{gst_amt:.2f}")
print(f"  {'Discount':<30} : -₹{discount:.2f}")
print(f"  {'Grand Total':<30} : ₹{grand_total:.2f}")
```
```
# Output:
  Item 1 — Wireless Mouse        : ₹499.00
  Item 2 — USB Hub               : ₹350.00
  Item 3 — Phone Case            : ₹199.00
  Item 4 — Earbuds Pro           : ₹1299.00
  Item 5 — Laptop Stand          : ₹850.00
  ────────────────────────────────────────
  Subtotal                       : ₹3197.00
  GST (18%)                      : ₹575.46
  Discount                       : -₹100.00
  Grand Total                    : ₹3672.46
```

**Key points:**
- `if subtotal > 1000 else 0.00` is a **ternary (inline) if expression** — a clean one-liner for simple conditions
- `f"{'text':<30}"` pads the label to 30 characters, left-aligned — makes the output column-aligned
- Verification: 499 + 350 + 199 + 1299 + 850 = ₹3197 → GST = ₹575.46 → Grand = ₹3672.46 ✅

---

## Solution 3 — Customer Membership Tier

```python
# Solution 3: Membership Tier Checker

total_spent = float(input("Enter your total spending this year (₹): "))

if total_spent >= 10000:
    tier    = "PLATINUM"
    benefit = "Free express delivery + 20% cashback on all orders"
    gap     = 0
    next_t  = None
elif total_spent >= 5000:
    tier    = "GOLD"
    benefit = "Free standard delivery + 10% cashback"
    gap     = 10000 - total_spent
    next_t  = "PLATINUM"
elif total_spent >= 2000:
    tier    = "SILVER"
    benefit = "5% cashback on orders above ₹500"
    gap     = 5000 - total_spent
    next_t  = "GOLD"
else:
    tier    = "STANDARD"
    benefit = "No current benefits — shop to unlock rewards!"
    gap     = 2000 - total_spent
    next_t  = "SILVER"

print(f"\n  Your Tier  : ⭐ {tier}")
print(f"  Benefits   : {benefit}")
if next_t:
    print(f"  Tip        : Spend ₹{gap:,.2f} more to reach {next_t}!")
else:
    print("  You are at the top tier. Congratulations!")
```
```
# Output (with input 7400):
  Your Tier  : ⭐ GOLD
  Benefits   : Free standard delivery + 10% cashback
  Tip        : Spend ₹2,600.00 more to reach PLATINUM!
```

**Key points:**
- `float(input(...))` converts the string input to a float in one step
- Setting `gap = 0` and `next_t = None` in the PLATINUM branch avoids an `UnboundLocalError` if those variables were referenced later
- `:,` adds thousand separators — `7400.00` becomes `7,400.00`

---

## Solution 4 — Product Catalog as a Dictionary

```python
# Solution 4: Product Catalog Dictionary

catalog = {
    "WM-4021": {"name": "Wireless Mouse",  "price": 499.00,  "category": "Electronics", "in_stock": True},
    "LS-7800": {"name": "Laptop Stand",    "price": 850.00,  "category": "Accessories", "in_stock": True},
    "UH-1102": {"name": "USB Hub",         "price": 350.00,  "category": "Electronics", "in_stock": True},
    "SW-9001": {"name": "Smart Watch",     "price": 2999.00, "category": "Wearables",   "in_stock": True},
    "PC-0055": {"name": "Phone Case",      "price": 199.00,  "category": "Accessories", "in_stock": True},
}

# Access a specific product
sku = "LS-7800"
product = catalog.get(sku)
if product:
    print(f"SKU {sku}: {product['name']} — ₹{product['price']:.2f}")

# Add a new product
catalog["EB-3310"] = {"name": "Earbuds Pro", "price": 1299.00, "category": "Electronics", "in_stock": True}
print(f"\nAdded: {catalog['EB-3310']['name']}")

# Mark Laptop Stand as out of stock
catalog["LS-7800"]["in_stock"] = False
print(f"\n{catalog['LS-7800']['name']} is now out of stock.")

# Print all in-stock products
print("\n  In-Stock Products:")
for sku, details in catalog.items():
    if details["in_stock"]:
        print(f"  {sku} — {details['name']:<25} ₹{details['price']:.2f}")
```
```
# Output:
SKU LS-7800: Laptop Stand — ₹850.00

Added: Earbuds Pro

Laptop Stand is now out of stock.

  In-Stock Products:
  WM-4021 — Wireless Mouse            ₹499.00
  UH-1102 — USB Hub                   ₹350.00
  SW-9001 — Smart Watch               ₹2999.00
  PC-0055 — Phone Case                ₹199.00
  EB-3310 — Earbuds Pro               ₹1299.00
```

**Key points:**
- `catalog.get(sku)` returns `None` instead of raising a `KeyError` if the SKU doesn't exist — always prefer `.get()` for safe lookups
- `catalog.items()` gives both key and value in each loop iteration
- Updating a nested dict value: `catalog["LS-7800"]["in_stock"] = False` — no need to redefine the whole entry

---

## Solution 5 — Tuple + Set Operations

```python
# Solution 5: Confirmed Order (Tuple) + Buyer Sets

# Part A — Tuple
confirmed_order = ("Wireless Mouse", "USB Hub", "Wireless Mouse", "Laptop Stand", "Earbuds")

print("Confirmed Order:")
for item in confirmed_order:
    print(f"  - {item}")

# Demonstrate immutability
try:
    confirmed_order[0] = "Smart Watch"   # This will fail
except TypeError as e:
    print(f"\nCannot modify tuple: {e}")

count = confirmed_order.count("Wireless Mouse")
print(f"\n'Wireless Mouse' appears {count} time(s) in the order.")

# Part B — Sets
sale_1_buyers = {"C101", "C204", "C305", "C408"}
sale_2_buyers = {"C204", "C408", "C512", "C617"}

both_sales  = sale_1_buyers.intersection(sale_2_buyers)
either_sale = sale_1_buyers.symmetric_difference(sale_2_buyers)
all_buyers  = sale_1_buyers.union(sale_2_buyers)

print(f"\nBuyers in BOTH sales    : {sorted(both_sales)}")
print(f"Buyers in EXACTLY ONE   : {sorted(either_sale)}")
print(f"Total unique buyers     : {len(all_buyers)} → {sorted(all_buyers)}")
```
```
# Output:
Confirmed Order:
  - Wireless Mouse
  - USB Hub
  - Wireless Mouse
  - Laptop Stand
  - Earbuds

Cannot modify tuple: 'tuple' object does not support item assignment

'Wireless Mouse' appears 2 time(s) in the order.

Buyers in BOTH sales    : ['C204', 'C408']
Buyers in EXACTLY ONE   : ['C101', 'C305', 'C512', 'C617']
Total unique buyers     : 6 → ['C101', 'C204', 'C305', 'C408', 'C512', 'C617']
```

**Key points:**
- Wrapping the tuple modification in `try/except TypeError` makes the demonstration clean rather than crashing
- `sorted()` on a set gives a consistent printed order — sets are unordered
- `intersection`, `symmetric_difference`, `union` are the three most useful set operations for real analytics

---

## Solution 6 — Smart Discount Engine

```python
# Solution 6: Discount Engine with is_nan and safe_eval

import math

def is_nan(value):
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False

def safe_eval_price(raw):
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

def get_discount(raw_cart_total):
    price = safe_eval_price(str(raw_cart_total)) if raw_cart_total is not None else None

    if is_nan(price) or price is None:
        return {"valid": False, "message": f"Invalid cart total: '{raw_cart_total}'"}

    if price <= 0:
        return {"valid": False, "message": f"Cart total must be positive. Got: {price}"}

    if price >= 3000:   pct = 20
    elif price >= 2000: pct = 15
    elif price >= 1000: pct = 10
    elif price >= 500:  pct = 5
    else:               pct = 0

    discount_amt = price * (pct / 100)
    final        = price - discount_amt

    return {
        "valid"       : True,
        "original"    : price,
        "discount_pct": pct,
        "discount_amt": round(discount_amt, 2),
        "final"       : round(final, 2),
    }

# Test
test_inputs = ["2500", "999", "", None, "abc", "0", "-500"]
for inp in test_inputs:
    result = get_discount(inp)
    if result["valid"]:
        print(f"  ₹{result['original']:>7.2f} → {result['discount_pct']}% off → Pay ₹{result['final']:.2f}")
    else:
        print(f"  ❌ {result['message']}")
```
```
# Output:
  ₹2500.00 → 15% off → Pay ₹2125.00
  ₹ 999.00 → 5% off → Pay ₹949.05
  ❌ Invalid cart total: ''
  ❌ Invalid cart total: 'None'
  ❌ Invalid cart total: 'abc'
  ❌ Cart total must be positive. Got: 0.0
  ❌ Cart total must be positive. Got: -500.0
```

**Key points:**
- `safe_eval_price(str(raw_cart_total)) if raw_cart_total is not None else None` — guards against calling `str(None)` which would produce the string `"None"` and pass `float()` as `None` (which then fails correctly)
- Returning a dict with a `"valid"` key is the standard agent tool response contract — callers always check `valid` first

---

## Solution 7 — Shopping Cart System

```python
# Solution 7: Cart System with Functions

def add_item(cart, name, price, qty):
    """Adds an item to the cart list."""
    cart.append({"name": name, "price": price, "qty": qty})

def calculate_subtotal(cart):
    """Returns the sum of price × qty for all items."""
    return sum(item["price"] * item["qty"] for item in cart)

def display_receipt(cart):
    """Prints a full formatted receipt with discount and GST."""
    if not cart:
        print("  Cart is empty.")
        return

    print("\n" + "=" * 55)
    print("         eCOMMart — Receipt")
    print("=" * 55)

    subtotal = 0
    for item in cart:
        line = item["price"] * item["qty"]
        subtotal += line
        print(f"  {item['name']:<22} ₹{item['price']:>7.2f} x {item['qty']} = ₹{line:.2f}")

    # Discount
    if subtotal >= 3000:   rate = 0.20
    elif subtotal >= 2000: rate = 0.15
    elif subtotal >= 1000: rate = 0.10
    elif subtotal >= 500:  rate = 0.05
    else:                  rate = 0.0

    disc       = subtotal * rate
    after_disc = subtotal - disc
    gst        = after_disc * 0.18
    total      = after_disc + gst

    print("-" * 55)
    print(f"  {'Subtotal':<35} ₹{subtotal:>8.2f}")
    if rate > 0:
        print(f"  {'Discount (' + str(int(rate*100)) + '%)':<35} -₹{disc:>7.2f}")
    print(f"  {'GST (18%)':<35} +₹{gst:>7.2f}")
    print("=" * 55)
    print(f"  {'GRAND TOTAL':<35} ₹{total:>8.2f}")
    print("=" * 55)

# Main loop
cart = []
print("eCOMMart Cart — type 'done' when finished.\n")
while True:
    name = input("Enter item name (or 'done'): ").strip()
    if name.lower() == "done":
        break
    try:
        price = float(input(f"Enter price of {name} (₹): "))
        qty   = int(input(f"Enter quantity: "))
        if price <= 0 or qty <= 0:
            print("  ⚠  Price and quantity must be positive.\n")
            continue
        add_item(cart, name, price, qty)
        print(f"  ✅ {name} added.\n")
    except ValueError:
        print("  ⚠  Invalid number entered. Try again.\n")

display_receipt(cart)
```

**Key points:**
- `sum(item["price"] * item["qty"] for item in cart)` is a **generator expression** inside `sum()` — efficient and concise
- `try/except ValueError` around `float()` and `int()` prevents a crash if the user types text instead of a number

---

## Solution 8 — Delivery Zone Checker

```python
# Solution 8: Delivery Zone Checker

import math

def is_nan(value):
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False

ZONES = {
    "40": ("Mumbai",    "Same-day delivery"),
    "56": ("Bangalore", "Next-day delivery"),
    "11": ("Delhi",     "2-day delivery"),
    "50": ("Pune",      "Next-day delivery"),
}

def check_delivery(pin_code):
    """
    Returns delivery zone and ETA for an eCOMMart order.

    Agent Tool Use:
        Call when customer asks 'When will my order arrive?'
        or checkout needs to display delivery estimate.

    Args:
        pin_code (str or None): Customer's 6-digit PIN code.

    Returns:
        dict: {"zone": str, "eta": str, "pin_code": str, "valid": bool}
    """
    if is_nan(pin_code) or len(str(pin_code).strip()) < 2:
        return {"valid": False, "zone": "Unknown", "eta": "Cannot determine", "pin_code": str(pin_code)}

    prefix = str(pin_code).strip()[:2]

    if prefix in ZONES:
        zone, eta = ZONES[prefix]
    else:
        zone, eta = "Other", "5-7 business days"

    return {"valid": True, "zone": zone, "eta": eta, "pin_code": str(pin_code)}

# Tests
pins = ["400001", "560078", "110011", "502001", None, "", "9"]
for pin in pins:
    result = check_delivery(pin)
    if result["valid"]:
        print(f"  PIN {result['pin_code']} → {result['zone']} | {result['eta']}")
    else:
        print(f"  PIN '{pin}' → ❌ Invalid PIN code")
```
```
# Output:
  PIN 400001 → Mumbai | Same-day delivery
  PIN 560078 → Bangalore | Next-day delivery
  PIN 110011 → Delhi | 2-day delivery
  PIN 502001 → Pune | Next-day delivery
  PIN 'None' → ❌ Invalid PIN code
  PIN '' → ❌ Invalid PIN code
  PIN '9' → ❌ Invalid PIN code
```

**Key points:**
- `str(pin_code).strip()[:2]` — safely converts to string, strips spaces, then takes the first 2 characters
- Storing the ZONES as a dict with the 2-digit prefix as key makes lookup O(1) — much cleaner than a chain of `elif`

---

## Solution 9 — Product Validator (Full Agent Tool)

```python
# Solution 9: Full Product Validator

import math

def is_nan(value):
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False

def safe_eval_price(raw):
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

def validate_product(product):
    """
    Validates a raw product dict from eCOMMart's catalog feed.

    Agent Tool Use:
        Call before inserting any product into the catalog database
        or when processing bulk uploads from sellers.

    Args:
        product (dict): Raw data with keys: name, price, category, stock_qty.

    Returns:
        dict: {
            "valid"  : bool,
            "errors" : list of str,
            "cleaned": dict or None
        }
    """
    ALLOWED = {"Electronics", "Accessories", "Wearables", "Home & Kitchen"}
    errors  = []
    cleaned = {}

    # Name
    name = product.get("name", "")
    if is_nan(name) or not isinstance(name, str) or len(name.strip()) == 0:
        errors.append("name is missing or empty.")
    else:
        cleaned["name"] = name.strip().title()

    # Price
    raw_price = product.get("price")
    price = safe_eval_price(str(raw_price)) if raw_price is not None else None
    if is_nan(price) or price is None or price <= 0:
        errors.append(f"price '{raw_price}' is invalid — must be a positive number.")
    else:
        cleaned["price"] = round(price, 2)

    # Category
    category = product.get("category", "")
    if category not in ALLOWED:
        errors.append(f"category '{category}' not allowed. Use: {sorted(ALLOWED)}")
    else:
        cleaned["category"] = category

    # Stock
    try:
        qty = int(product.get("stock_qty", -1))
        if qty < 0:
            errors.append("stock_qty must be 0 or greater.")
        else:
            cleaned["stock_qty"] = qty
    except (ValueError, TypeError):
        errors.append("stock_qty must be a whole number.")

    return {
        "valid"  : len(errors) == 0,
        "errors" : errors,
        "cleaned": cleaned if not errors else None,
    }

# Tests
test_products = [
    {"name": "wireless mouse",  "price": "499",   "category": "Electronics",    "stock_qty": 120},
    {"name": "",                "price": "850",   "category": "Accessories",    "stock_qty": 30},
    {"name": "Smart Watch",     "price": "abc",   "category": "Wearables",      "stock_qty": 50},
    {"name": "Mystery Item",    "price": "199",   "category": "Food & Grocery", "stock_qty": -5},
    {"name": "Earbuds Pro",     "price": None,    "category": "Electronics",    "stock_qty": 80},
    {"name": "USB Hub",         "price": "350",   "category": "Electronics",    "stock_qty": 0},
]

for i, prod in enumerate(test_products, 1):
    r = validate_product(prod)
    status = "✅ VALID" if r["valid"] else "❌ INVALID"
    print(f"\nProduct {i}: {prod.get('name','(no name)')} — {status}")
    if r["valid"]:
        print(f"  Cleaned: {r['cleaned']}")
    else:
        for err in r["errors"]:
            print(f"  ⚠  {err}")
```
```
# Output:
Product 1: wireless mouse — ✅ VALID
  Cleaned: {'name': 'Wireless Mouse', 'price': 499.0, 'category': 'Electronics', 'stock_qty': 120}

Product 2:  — ❌ INVALID
  ⚠  name is missing or empty.

Product 3: Smart Watch — ❌ INVALID
  ⚠  price 'abc' is invalid — must be a positive number.

Product 4: Mystery Item — ❌ INVALID
  ⚠  category 'Food & Grocery' not allowed. Use: ['Accessories', 'Electronics', 'Home & Kitchen', 'Wearables']
  ⚠  stock_qty must be 0 or greater.

Product 5: Earbuds Pro — ❌ INVALID
  ⚠  price 'None' is invalid — must be a positive number.

Product 6: USB Hub — ✅ VALID
  Cleaned: {'name': 'Usb Hub', 'price': 350.0, 'category': 'Electronics', 'stock_qty': 0}
```

> **Note on `.title()`:** `"USB Hub".title()` → `"Usb Hub"` — Python's `.title()` lowercases all letters after the first in each word. This is expected behaviour for acronyms. In production you would add a custom acronym map. The test passes because the validation logic is correct.

---

## Solution 10 — List Comprehension Analytics

```python
# Solution 10: List Comprehension Product Analytics

products = [
    {"name": "Wireless Mouse",  "category": "Electronics", "price": 499,  "in_stock": True,  "rating": 4.5},
    {"name": "Laptop Stand",    "category": "Accessories", "price": 850,  "in_stock": False, "rating": 4.2},
    {"name": "USB Hub",         "category": "Electronics", "price": 350,  "in_stock": True,  "rating": 3.9},
    {"name": "Smart Watch",     "category": "Wearables",   "price": 2999, "in_stock": True,  "rating": 4.7},
    {"name": "Earbuds Pro",     "category": "Electronics", "price": 1299, "in_stock": True,  "rating": 4.6},
    {"name": "Phone Case",      "category": "Accessories", "price": 199,  "in_stock": True,  "rating": 3.8},
]

# 1. In-stock product names
in_stock_names = [p["name"] for p in products if p["in_stock"]]
print("In-stock         :", in_stock_names)

# 2. Electronics under ₹1000
budget_electronics = [p["name"] for p in products if p["category"] == "Electronics" and p["price"] < 1000]
print("Budget Electronics:", budget_electronics)

# 3. Prices with GST (in-stock only)
gst_prices = [round(p["price"] * 1.18, 2) for p in products if p["in_stock"]]
print("Prices with GST  :", gst_prices)

# 4. Top-rated labels (rating > 4.4)
top_rated = [f"{p['name']} ⭐{p['rating']}" for p in products if p["rating"] > 4.4]
print("Top rated        :", top_rated)

# 5. Average price
all_prices    = [p["price"] for p in products]
average_price = sum(all_prices) / len(all_prices)
print(f"Average price    : ₹{average_price:.2f}")
```
```
# Output:
In-stock         : ['Wireless Mouse', 'USB Hub', 'Smart Watch', 'Earbuds Pro', 'Phone Case']
Budget Electronics: ['Wireless Mouse', 'USB Hub']
Prices with GST  : [588.82, 413.0, 3538.82, 1532.82, 234.82]
Top rated        : ['Wireless Mouse ⭐4.5', 'Smart Watch ⭐4.7', 'Earbuds Pro ⭐4.6']
Average price    : ₹1032.67
```

**Key points:**
- List comprehensions follow the pattern `[expression for item in iterable if condition]`
- The condition (`if ...`) at the end is optional — omit it to include all items
- Comprehensions replace 3–4 lines of `for` + `if` + `append` with one clean, readable line

---

## Solution 11 — Exception Handling: Safe Order Processor

```python
# Solution 11: Safe Order Processor with try/except/finally

CATALOG = {
    "WM-4021": {"name": "Wireless Mouse", "price": 499.00,  "stock": 120},
    "UH-1102": {"name": "USB Hub",        "price": 350.00,  "stock": 45},
    "SW-9001": {"name": "Smart Watch",    "price": 2999.00, "stock": 30},
}

def process_order(sku, qty_str, pin_code):
    """
    Safely processes an eCOMMart order with full error handling.

    Agent Tool Use:
        Call when processing a customer's order request.

    Args:
        sku      (str): Product SKU.
        qty_str  (str): Quantity as a string (from form input).
        pin_code (str): Delivery PIN code.

    Returns:
        dict: {"success": bool, "total": float or None, "message": str}
    """
    try:
        # Validate and convert quantity
        qty = int(qty_str)
        if qty <= 0:
            raise ValueError(f"Quantity must be a positive integer. Got: {qty}")

        # Look up SKU — will raise KeyError if not found
        product = CATALOG[sku]

        # Check stock
        if product["stock"] < qty:
            raise ValueError(f"Only {product['stock']} units of '{product['name']}' in stock.")

        total = product["price"] * qty
        return {
            "success": True,
            "total"  : round(total, 2),
            "message": f"Order confirmed: {product['name']} x{qty} = ₹{total:.2f} | PIN: {pin_code}"
        }

    except ValueError as e:
        return {"success": False, "total": None, "message": f"Validation error: {e}"}

    except KeyError:
        return {"success": False, "total": None, "message": f"SKU '{sku}' not found in catalog."}

    finally:
        print(f"  [LOG] Order processing attempt complete for SKU={sku}, qty={qty_str}.")

# Tests
test_cases = [
    ("WM-4021", "3",   "400001"),
    ("WM-4021", "0",   "400001"),
    ("WM-4021", "abc", "400001"),
    ("XX-9999", "2",   "560078"),
    ("SW-9001", "1",   "110011"),
]
for sku, qty, pin in test_cases:
    result = process_order(sku, qty, pin)
    icon   = "✅" if result["success"] else "❌"
    print(f"  {icon} {result['message']}\n")
```
```
# Output:
  [LOG] Order processing attempt complete for SKU=WM-4021, qty=3.
  ✅ Order confirmed: Wireless Mouse x3 = ₹1497.00 | PIN: 400001

  [LOG] Order processing attempt complete for SKU=WM-4021, qty=0.
  ❌ Validation error: Quantity must be a positive integer. Got: 0

  [LOG] Order processing attempt complete for SKU=WM-4021, qty=abc.
  ❌ Validation error: invalid literal for int() with base 10: 'abc'

  [LOG] Order processing attempt complete for SKU=XX-9999, qty=2.
  ❌ SKU 'XX-9999' not found in catalog.

  [LOG] Order processing attempt complete for SKU=SW-9001, qty=1.
  ✅ Order confirmed: Smart Watch x1 = ₹2999.00 | PIN: 110011
```

**Key points:**
- `raise ValueError(...)` inside a function lets you signal an error with a custom message — callers catch it
- `CATALOG[sku]` raises `KeyError` automatically if the key doesn't exist — you don't have to check manually
- `finally` runs **no matter what** — even if there is an exception. Perfect for logging and cleanup

---

## Solution 12 — Capstone: eCOMMart Order Terminal

```python
# Solution 12: eCOMMart Order Terminal (Capstone)

import math

# ─── Catalog ────────────────────────────────────────────
CATALOG = {
    "WM-4021": {"name": "Wireless Mouse",  "price": 499.00,  "stock": 120},
    "LS-7800": {"name": "Laptop Stand",    "price": 850.00,  "stock": 0},
    "UH-1102": {"name": "USB Hub",         "price": 350.00,  "stock": 45},
    "SW-9001": {"name": "Smart Watch",     "price": 2999.00, "stock": 30},
    "EB-3310": {"name": "Earbuds Pro",     "price": 1299.00, "stock": 80},
    "PC-0055": {"name": "Phone Case",      "price": 199.00,  "stock": 200},
}

# ─── Helpers ─────────────────────────────────────────────
def is_nan(value):
    """Returns True if value is missing, empty, or NaN."""
    if value is None: return True
    if isinstance(value, float) and math.isnan(value): return True
    if isinstance(value, str) and value.strip() == "": return True
    return False

def safe_eval_price(raw):
    """Safely converts a string to float. Returns None on failure."""
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

# ─── Business Logic ──────────────────────────────────────
def get_discount_rate(subtotal):
    """Returns discount rate as a decimal based on cart total."""
    if subtotal >= 3000: return 0.20
    elif subtotal >= 2000: return 0.15
    elif subtotal >= 1000: return 0.10
    elif subtotal >= 500: return 0.05
    return 0.0

def view_catalog():
    """Prints the full eCOMMart product catalog."""
    print("\n" + "─" * 55)
    print(f"  {'SKU':<10} {'Name':<22} {'Price':>8}  {'Stock':>6}")
    print("─" * 55)
    for sku, p in CATALOG.items():
        stock_label = f"{p['stock']} units" if p["stock"] > 0 else "OUT OF STOCK"
        print(f"  {sku:<10} {p['name']:<22} ₹{p['price']:>7.2f}  {stock_label}")
    print("─" * 55)

def add_to_cart(cart):
    """Prompts user for SKU and quantity and adds to cart."""
    sku = input("  Enter SKU: ").strip().upper()

    if sku not in CATALOG:
        print(f"  ❌ SKU '{sku}' not found.")
        return

    product = CATALOG[sku]

    if product["stock"] == 0:
        print(f"  ❌ '{product['name']}' is out of stock.")
        return

    raw_qty = input(f"  Enter quantity (max {product['stock']}): ").strip()
    qty = safe_eval_price(raw_qty)

    if is_nan(qty) or qty is None or qty <= 0:
        print("  ❌ Invalid quantity.")
        return

    qty = int(qty)
    if qty > product["stock"]:
        print(f"  ⚠  Only {product['stock']} available. Adding {product['stock']} instead.")
        qty = product["stock"]

    # Check if SKU already in cart — update quantity instead of adding duplicate
    for item in cart:
        if item["sku"] == sku:
            item["qty"] += qty
            print(f"  ✅ Updated: {product['name']} — total qty now {item['qty']}")
            return

    cart.append({"sku": sku, "name": product["name"], "price": product["price"], "qty": qty})
    print(f"  ✅ Added: {product['name']} x{qty}")

def view_cart(cart):
    """Displays the current cart contents."""
    if not cart:
        print("  Cart is empty.")
        return
    print("\n  Current Cart:")
    for item in cart:
        print(f"  {item['name']:<25} ₹{item['price']:.2f} x {item['qty']}")

def checkout(cart):
    """Prints the final receipt with all pricing applied."""
    if not cart:
        print("  ❌ Cart is empty — nothing to checkout.")
        return

    pin = input("\n  Enter your delivery PIN code: ").strip()

    subtotal = sum(item["price"] * item["qty"] for item in cart)
    rate     = get_discount_rate(subtotal)
    disc_amt = subtotal * rate
    after    = subtotal - disc_amt
    gst      = after * 0.18
    delivery = 0 if subtotal >= 500 else 60
    total    = after + gst + delivery

    print("\n" + "=" * 58)
    print("          eCOMMart — Final Receipt")
    print("=" * 58)
    for item in cart:
        line = item["price"] * item["qty"]
        print(f"  {item['name']:<25} ₹{item['price']:>7.2f} x {item['qty']} = ₹{line:.2f}")
    print("-" * 58)
    print(f"  {'Subtotal':<38} ₹{subtotal:>8.2f}")
    if rate > 0:
        print(f"  {'Discount (' + str(int(rate*100)) + '%)':<38} -₹{disc_amt:>7.2f}")
    print(f"  {'GST (18%)':<38} +₹{gst:>7.2f}")
    print(f"  {'Delivery':<38} {'FREE ✓' if delivery == 0 else '₹60.00'}")
    print("=" * 58)
    print(f"  {'GRAND TOTAL':<38} ₹{total:>8.2f}")
    print("=" * 58)
    print(f"\n  📦 Delivery PIN: {pin}")
    print("  Thank you for shopping at eCOMMart!\n")

# ─── Main Menu ───────────────────────────────────────────
def show_menu():
    """Displays the main terminal menu."""
    print("\n" + "─" * 40)
    print("   eCOMMart Order Terminal")
    print("─" * 40)
    print("  1. View catalog")
    print("  2. Add item to cart")
    print("  3. View cart")
    print("  4. Checkout")
    print("  0. Exit")
    print("─" * 40)

# ─── Program Entry Point ─────────────────────────────────
cart = []

print("\n  Welcome to eCOMMart Order Terminal!")

while True:
    show_menu()
    choice = input("  Enter choice: ").strip()

    if choice == "0":
        print("\n  Thank you for using eCOMMart. Goodbye!\n")
        break
    elif choice == "1":
        view_catalog()
    elif choice == "2":
        add_to_cart(cart)
    elif choice == "3":
        view_cart(cart)
    elif choice == "4":
        checkout(cart)
    else:
        print("  ⚠  Invalid option. Please choose 0–4.")
```

**Key points — the full Week 3 picture:**
- **Every function has a docstring** — describing what it does and when to call it
- `is_nan` + `safe_eval_price` guard every user input before it is used in logic
- The cart is a **list of dicts** — the standard pattern for any ordered collection with named fields
- `sum(item["price"] * item["qty"] for item in cart)` — generator expression inside `sum()` for a clean subtotal
- `while True` + `break` — the standard Python pattern for a menu-driven terminal
- Functions are small, single-purpose, and reusable — this is the foundation for building agent tools

---

## Solutions — Type Conversion Tasks (008b)

### Task 1: Type Conversion Sampler

```python
# Task 1: eCOMMart Type Conversion Sampler

price_str      = "1299"
qty_float      = 2.0
in_stock_int   = 1
product_id     = 5001
discount_bool  = True

print("=" * 60)
print(f"  {'Original':<20} {'Type':<12} {'Converted':<15} {'New Type'}")
print("=" * 60)

# price_str → int and float
p_int   = int(price_str)
p_float = float(price_str)
print(f"  {repr(price_str):<20} {type(price_str).__name__:<12} {p_int:<15} {type(p_int).__name__}")
print(f"  {repr(price_str):<20} {type(price_str).__name__:<12} {p_float:<15} {type(p_float).__name__}")

# qty_float → int and str
q_int = int(qty_float)
q_str = str(qty_float)
print(f"  {repr(qty_float):<20} {type(qty_float).__name__:<12} {q_int:<15} {type(q_int).__name__}")
print(f"  {repr(qty_float):<20} {type(qty_float).__name__:<12} {repr(q_str):<15} {type(q_str).__name__}")

# in_stock_int → bool
is_bool = bool(in_stock_int)
print(f"  {repr(in_stock_int):<20} {type(in_stock_int).__name__:<12} {is_bool:<15} {type(is_bool).__name__}")

# product_id → str (used in a SKU)
pid_str = str(product_id)
sku     = "SKU-" + pid_str
print(f"  {repr(product_id):<20} {type(product_id).__name__:<12} {repr(sku):<15} {type(sku).__name__}")

# discount_bool → int and float
d_int   = int(discount_bool)
d_float = float(discount_bool)
print(f"  {repr(discount_bool):<20} {type(discount_bool).__name__:<12} {d_int:<15} {type(d_int).__name__}")
print(f"  {repr(discount_bool):<20} {type(discount_bool).__name__:<12} {d_float:<15} {type(d_float).__name__}")
print("=" * 60)
```
```
# Output:
============================================================
  Original             Type         Converted       New Type
============================================================
  '1299'               str          1299            int
  '1299'               str          1299.0          float
  2.0                  float        2               int
  2.0                  float        '2.0'           str
  1                    int          True            bool
  5001                 int          'SKU-5001'      str
  True                 bool         1               int
  True                 bool         1.0             float
============================================================
```

**Key points:**
- `int("1299")` works; `int("1299.99")` raises `ValueError` — convert to float first if the string has decimals
- `int(2.0)` → `2` (truncates, does not round)
- `int(True)` → `1`, `int(False)` → `0` — booleans are a subclass of int in Python

---

### Task 2: Safe Cart Input

```python
# Task 2: Safe Cart Input

def safe_eval_price(raw):
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
- `safe_eval_price()` handles price — returns `None` on failure
- `int()` inside `try/except ValueError` handles quantity — catches both non-numeric strings and the manually raised negative-value error
- Always validate `> 0` after converting — `float("0")` succeeds but a zero price is logically wrong

---

### Task 3: Type Detective

```python
# Task 3: Type Detective

def safe_eval_price(raw):
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

raw_catalog_prices = [499, "850.00", "1,299", None, True, "FREE", 0, "", "2999.99", False]

print(f"  {'Raw Value':<15} {'Original Type':<15} {'As Float':<12} {'Usable?'}")
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

    print(f"  {repr(raw):<15} {original_type:<15} {display:<12} {status}")
```
```
# Output:
  Raw Value       Original Type   As Float     Usable?
  ───────────────────────────────────────────────────────
  499             int             ₹499.00      ✅ Yes
  '850.00'        str             ₹850.00      ✅ Yes
  '1,299'         str             —            ❌ No
  None            NoneType        —            ❌ No
  True            bool            ₹1.00        ✅ Yes
  'FREE'          str             —            ❌ No
  0               int             0.0          ⚠️  Zero
  ''              str             —            ❌ No
  '2999.99'       str             ₹2999.99     ✅ Yes
  False           bool            0.0          ⚠️  Zero
```

**Key points:**
- `"1,299"` fails `float()` — commas must be stripped first with `.replace(",", "")`
- `True` converts to `1.0` and `False` to `0.0` — booleans are valid numbers in Python
- `0` converts successfully but is logically not a usable price — always check `> 0` separately
