# Week 3 — Exercises
## eCOMMart AI Squad | Python Fundamentals

> **Instructions:**
> - Work through the exercises in order — each one builds on the previous.
> - Open VS Code, create a new `.py` file for each exercise, and run it from the terminal.
> - Do not look at the Solutions file until you have genuinely attempted the exercise.
> - All exercises use the **eCOMMart** context — think like an eCOMMart developer.

---

## 🟢 Beginner

---

### Exercise 1 — Product Label with All Three String Types
**Topics:** Variables, single quotes, double quotes, triple quotes, f-strings
**Estimated time:** 10 min

eCOMMart needs a formatted product label printed to the terminal.

**Requirements:**
- Store the product SKU using a **single-quote** string (e.g. `'WM-4021'`)
- Store the brand tagline using a **double-quote** string — it must contain an apostrophe (e.g. `"India's Top Tech Store"`)
- Store the full product description using a **triple-quote** string spanning at least 3 lines
- Store the price as a `float` and the discount as an `int`
- Calculate the final price after discount
- Print a formatted label that shows: SKU, tagline, description, MRP, discount %, final price

**Expected output (example):**
```
==================================================
  SKU      : WM-4021
  Tagline  : India's Top Tech Store
  MRP      : ₹499.00
  Discount : 10%
  You Pay  : ₹449.10

  Description:
    Wireless Ergonomic Mouse
    12-month battery life
    Compatible with Windows & Mac
==================================================
```

---

### Exercise 2 — Price Calculator for 5 Cart Items
**Topics:** Variables, float arithmetic, operators, f-strings
**Estimated time:** 10 min

A customer has 5 items in their eCOMMart cart. Calculate and display the complete bill.

**Requirements:**
- Hardcode prices for exactly 5 items (you choose the products and prices)
- Calculate: subtotal, 18% GST, and apply a flat ₹100 discount if subtotal > ₹1000
- Print each item's price, then the subtotal, GST, discount (if applicable), and grand total
- Use `:.2f` formatting throughout

**Expected output (example):**
```
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

---

### Exercise 3 — Customer Membership Tier
**Topics:** `if / elif / else`, comparison operators, variables
**Estimated time:** 10 min

Ask the user to enter their total spending on eCOMMart this year. Print their membership tier and what they need to reach the next tier.

**Tier rules:**
- ≥ ₹10,000 → PLATINUM — "Free express delivery + 20% cashback"
- ≥ ₹5,000  → GOLD — "Free standard delivery + 10% cashback"
- ≥ ₹2,000  → SILVER — "5% cashback on orders above ₹500"
- < ₹2,000  → STANDARD — "No current benefits"

**Requirements:**
- Ask the user: `"Enter your total spending this year (₹): "`
- Print the tier name and its benefit
- If not at the top tier, print how much more they need to spend to reach the next tier

**Expected output (example, with input ₹7400):**
```
  Your Tier  : ⭐ GOLD
  Benefits   : Free standard delivery + 10% cashback
  Tip        : Spend ₹2,600.00 more to reach PLATINUM!
```

---

### Exercise 4 — Product Catalog as a Dictionary
**Topics:** Dictionaries, accessing values, `.get()`, adding and removing keys
**Estimated time:** 15 min

Build a small eCOMMart product catalog as a dictionary where:
- The **key** is the SKU (e.g. `"WM-4021"`)
- The **value** is a nested dictionary with `name`, `price`, `category`, `in_stock`

**Requirements:**
- Populate the catalog with at least 5 products
- Print the name and price of a specific product using its SKU
- Add a new product to the catalog
- Mark one product as out of stock (set `in_stock` to `False`)
- Print all in-stock products using a `for` loop

**Expected output (example):**
```
SKU LS-7800: Laptop Stand — ₹850.00

Added: Earbuds Pro

Laptop Stand is now out of stock.

  In-Stock Products:
  WM-4021 — Wireless Mouse          ₹499.00
  UH-1102 — USB Hub                 ₹350.00
  SW-9001 — Smart Watch             ₹2999.00
  PC-0055 — Phone Case              ₹199.00
  EB-3310 — Earbuds Pro             ₹1299.00
```

---

## 🟡 Intermediate

---

### Exercise 5 — Confirmed Order as a Tuple + Set of Buyers
**Topics:** Tuples, sets, immutability, set operations
**Estimated time:** 15 min

**Part A — Tuple:**
Store a confirmed eCOMMart order as a tuple of product names. Demonstrate that you cannot modify it. Count how many times a specific product appears.

**Part B — Set:**
You have two lists of buyer IDs from two sale events — some buyers participated in both. Use sets to find:
- Buyers who came to both sales (intersection)
- Buyers who came to exactly one sale (symmetric difference)
- Total unique buyers across both sales (union)

**Expected output (example):**
```
Confirmed Order:
  - Wireless Mouse
  - USB Hub
  - Wireless Mouse
  - Laptop Stand
  - Earbuds

Cannot modify tuple: 'tuple' object does not support item assignment

'Wireless Mouse' appears 2 time(s).

Buyers in BOTH sales    : ['C204', 'C408']
Buyers in EXACTLY ONE   : ['C101', 'C305', 'C512', 'C617']
Total unique buyers     : 6 → ['C101', 'C204', 'C305', 'C408', 'C512', 'C617']
```

---

### Exercise 6 — Smart Discount Engine with `safe_eval` and `is_nan`
**Topics:** Functions, `is_nan`, `safe_eval_price`, `if/elif/else`, return values
**Estimated time:** 20 min

Build a discount engine for eCOMMart's checkout. Input comes in as raw strings (from a web form) so you must validate before using.

**Requirements:**
1. Write an `is_nan(value)` function — handles `None`, `float('nan')`, and empty string
2. Write a `safe_eval_price(raw)` function — converts string to float safely using `try/except`
3. Write a `get_discount(raw_cart_total)` function that:
   - Calls `safe_eval_price` and `is_nan` first
   - If invalid: returns `{"valid": False, "message": "Invalid cart total"}`
   - If valid: applies the discount tier logic and returns:
     `{"valid": True, "original": ..., "discount_pct": ..., "discount_amt": ..., "final": ...}`

**Test with these inputs:**
```python
test_inputs = ["2500", "999", "", None, "abc", "0", "-500"]
```

**Expected output:**
```
  ₹2500.00 → 15% off → Pay ₹2125.00
  ₹ 999.00 → 5% off → Pay ₹949.05
  ❌ Invalid cart total: ''
  ❌ Invalid cart total: 'None'
  ❌ Invalid cart total: 'abc'
  ❌ Cart total must be positive. Got: 0.0
  ❌ Cart total must be positive. Got: -500.0
```

---

### Exercise 7 — Shopping Cart System using Functions
**Topics:** Functions, lists of dicts, loops, `input()`, `while` loop
**Estimated time:** 25 min

Build eCOMMart's cart module using functions.

**Requirements — define these functions:**
- `add_item(cart, name, price, qty)` — appends a dict to the cart list
- `calculate_subtotal(cart)` — returns sum of `price × qty` for all items
- `display_receipt(cart)` — prints a full bill with discount and GST

**Then write a loop** that:
- Keeps asking the user for item name, price, and quantity
- Stops when user types `done`
- Calls `display_receipt()` at the end

---

### Exercise 8 — Delivery Zone Checker
**Topics:** Functions, dictionary lookup, `if/elif/else`, string slicing
**Estimated time:** 15 min

Build `check_delivery(pin_code)` — an eCOMMart agent tool.

**Zone rules (based on first 2 digits of PIN):**
- `40` → Mumbai — Same-day delivery
- `56` → Bangalore — Next-day delivery
- `11` → Delhi — 2-day delivery
- `50` → Pune — Next-day delivery
- Anything else → Other — 5-7 days

**Requirements:**
- The function must handle `None`, empty string, and strings shorter than 2 characters gracefully (use `is_nan`)
- Return a dict: `{"zone": ..., "eta": ..., "pin_code": ..., "valid": bool}`
- Test with at least 5 PIN codes including one invalid input

**Expected output (example):**
```
  PIN 400001 → Mumbai | Same-day delivery
  PIN 560078 → Bangalore | Next-day delivery
  PIN 110011 → Delhi | 2-day delivery
  PIN 502001 → Pune | Next-day delivery
  PIN 'None' → ❌ Invalid PIN code
  PIN '' → ❌ Invalid PIN code
  PIN '9' → ❌ Invalid PIN code
```

---

## 🔴 Advanced

---

### Exercise 9 — Product Validator (Full Agent Tool)
**Topics:** Functions, dicts, `try/except`, `is_nan`, `safe_eval`, all data types
**Estimated time:** 30 min

Build `validate_product(product_dict)` — a complete input validation agent tool.

**A valid product must have:**
- `name`: non-empty string
- `price`: positive float (convert from string if needed using `safe_eval_price`)
- `category`: one of `{"Electronics", "Accessories", "Wearables", "Home & Kitchen"}`
- `stock_qty`: non-negative integer

**Return format:**
```python
{
  "valid"  : True or False,
  "errors" : [],             # list of error strings
  "cleaned": {cleaned dict} or None
}
```

**Test with at least 6 products** — mix of valid and invalid.

**Expected output (example):**
```
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

> **Note:** `'USB Hub'.title()` → `'Usb Hub'` — Python's `.title()` lowercases all letters after the first in each word. This is expected behaviour. If you want to preserve acronyms, you would need a custom mapping.

---

### Exercise 10 — List Comprehension: Product Analytics
**Topics:** List comprehensions, filtering, transforming, average
**Estimated time:** 15 min

Given this product dataset, use **list comprehensions only** (no regular for loops) for all operations.

```python
products = [
    {"name": "Wireless Mouse",  "category": "Electronics", "price": 499,  "in_stock": True,  "rating": 4.5},
    {"name": "Laptop Stand",    "category": "Accessories", "price": 850,  "in_stock": False, "rating": 4.2},
    {"name": "USB Hub",         "category": "Electronics", "price": 350,  "in_stock": True,  "rating": 3.9},
    {"name": "Smart Watch",     "category": "Wearables",   "price": 2999, "in_stock": True,  "rating": 4.7},
    {"name": "Earbuds Pro",     "category": "Electronics", "price": 1299, "in_stock": True,  "rating": 4.6},
    {"name": "Phone Case",      "category": "Accessories", "price": 199,  "in_stock": True,  "rating": 3.8},
]
```

**Write list comprehensions for:**
1. Names of all **in-stock** products
2. Names of all **Electronics** products priced below ₹1000
3. Prices with **GST added** (multiply each price by 1.18), for in-stock items only
4. Products with a **rating above 4.4** — return as `"Wireless Mouse ⭐4.5"`
5. Average price of all products (use comprehension to extract prices)

**Expected output:**
```
In-stock         : ['Wireless Mouse', 'USB Hub', 'Smart Watch', 'Earbuds Pro', 'Phone Case']
Budget Electronics: ['Wireless Mouse', 'USB Hub']
Prices with GST  : [588.82, 413.0, 3538.82, 1532.82, 234.82]
Top rated        : ['Wireless Mouse ⭐4.5', 'Smart Watch ⭐4.7', 'Earbuds Pro ⭐4.6']
Average price    : ₹1032.67
```

---

### Exercise 11 — Exception Handling: Safe Order Processor
**Topics:** `try/except/finally`, custom error messages, functions
**Estimated time:** 20 min

eCOMMart's order processor must never crash — even with bad input.

**Write `process_order(sku, qty_str, pin_code)` that:**
- Looks up the SKU in a small catalog dict (you define 4–5 products)
- Converts `qty_str` from string to int inside a `try/except` block
- Raises a `ValueError` with a helpful message if qty ≤ 0
- Raises a `KeyError` (caught) if the SKU doesn't exist
- Prints a `finally` block message: `"Order processing attempt complete."`
- Returns a dict with the order total or an error message

**Test with at least 5 combinations** — valid, zero qty, bad SKU, string qty.

**Expected output (example):**
```
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

---

### Exercise 12 — Capstone: eCOMMart Order Terminal
**Topics:** All Week 3 — variables, strings, collections, conditions, loops, functions, exceptions
**Estimated time:** 40 min

Build a complete interactive eCOMMart order terminal.

**The program must:**

1. Show a menu with options:
   - `1` View catalog
   - `2` Add item to cart (ask for SKU and quantity)
   - `3` View cart
   - `4` Checkout (print full bill with GST + discount + delivery)
   - `0` Exit

2. Use this catalog (dictionary):
```python
CATALOG = {
    "WM-4021": {"name": "Wireless Mouse",  "price": 499.00,  "stock": 120},
    "LS-7800": {"name": "Laptop Stand",    "price": 850.00,  "stock": 0},
    "UH-1102": {"name": "USB Hub",         "price": 350.00,  "stock": 45},
    "SW-9001": {"name": "Smart Watch",     "price": 2999.00, "stock": 30},
    "EB-3310": {"name": "Earbuds Pro",     "price": 1299.00, "stock": 80},
    "PC-0055": {"name": "Phone Case",      "price": 199.00,  "stock": 200},
}
```

3. Validate all inputs using `is_nan()` and `safe_eval_price()`
4. Check if item is in stock before adding to cart
5. Apply: 20% discount if cart ≥ ₹3000, 15% if ≥ ₹2000, 10% if ≥ ₹1000, 5% if ≥ ₹500
6. Add 18% GST on the discounted total
7. Free delivery if cart ≥ ₹500, else ₹60
8. Use `try/except` around any risky operations
9. Every function must have a docstring

---

## 📋 Summary of Exercises

| # | Exercise | Topics | Level |
|---|---|---|---|
| 1 | Product Label | Variables, 3 string types, f-strings | 🟢 |
| 2 | Price Calculator for 5 items | Arithmetic, operators, floats | 🟢 |
| 3 | Membership Tier Checker | if/elif/else, input() | 🟢 |
| 4 | Product Catalog Dictionary | Dicts, loops, .get() | 🟢 |
| 5 | Tuple + Set operations | Tuples, sets, immutability | 🟡 |
| 6 | Smart Discount Engine | Functions, is_nan, safe_eval | 🟡 |
| 7 | Shopping Cart System | Functions, lists, while loop | 🟡 |
| 8 | Delivery Zone Checker | Function, dict lookup, string slice | 🟡 |
| 9 | Product Validator | Full agent tool pattern | 🔴 |
| 10 | List Comprehension Analytics | List comprehensions, filter, map | 🔴 |
| 11 | Exception Handling | try/except/finally, raise | 🔴 |
| 12 | Capstone Order Terminal | All Week 3 topics combined | 🔴 |
