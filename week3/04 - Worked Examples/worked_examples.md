# Week 3 — Worked Examples
## eCOMMart AI Squad | Python Fundamentals

> Each example below is a **complete, runnable Python program**.
> Read the explanation first, then trace through the code, then run it yourself.
> Each example builds on the last — by Example 6 you have a mini agent tool.

---

## Table of Contents

| Example | Title | Key Concepts |
|---|---|---|
| 1 | Product Card Printer | Variables, string types, f-strings |
| 2 | Membership Tier Checker | `if/elif/else`, booleans, comparison operators |
| 3 | Shopping Cart | Lists, dicts, `for` loop, arithmetic |
| 4 | Product Validator | Functions, docstrings, `is_nan`, `safe_eval`, `try/except` |
| 5 | Inventory Manager | Sets, `while` loop, menu-driven program |
| 6 | Mini Agent Tool | All Week 3 concepts combined |

---

## Example 1: Product Card Printer
**Concepts:** Variables, all three string quote types, f-strings, `print`

**Scenario:** eCOMMart needs to display a formatted product card for any item in the catalog.

```python
# =========================================================
# Example 1: eCOMMart Product Card Printer
# Concepts: Variables, single/double/triple quotes, f-strings
# =========================================================

# Single-quote string — good for short clean values
sku      = 'WM-4021'
category = 'Electronics'

# Double-quote string — use when the value contains an apostrophe
tagline  = "India's No.1 Tech Store"

# Triple-quote string — spans multiple lines, preserves line breaks
description = """
  Wireless Bluetooth Mouse
  - Ergonomic design, suitable for all-day use
  - 12-month battery life
  - Compatible with Windows, Mac, Linux
  - Colour: Matte Black
"""

# Variables for price calculation
price     = 499.00
discount  = 10       # 10 percent
gst_rate  = 0.18     # 18%

# Calculations
discount_amt         = price * (discount / 100)
price_after_discount = price - discount_amt
gst_amt              = price_after_discount * gst_rate
final_price          = price_after_discount + gst_amt

# f-string output — embeds variables directly into the string
print("=" * 50)
print(f"  SKU      : {sku}")
print(f"  Category : {category}")
print(f"  Tagline  : {tagline}")
print(f"  MRP      : ₹{price:.2f}")
print(f"  Discount : {discount}%  (-₹{discount_amt:.2f})")
print(f"  GST(18%) : +₹{gst_amt:.2f}")
print(f"  You Pay  : ₹{final_price:.2f}")
print(f"\n  About this product:{description}")
print("=" * 50)
```
```
# Output:
==================================================
  SKU      : WM-4021
  Category : Electronics
  Tagline  : India's No.1 Tech Store
  MRP      : ₹499.00
  Discount : 10%  (-₹49.90)
  GST(18%) : +₹80.84
  You Pay  : ₹529.94

  About this product:
  Wireless Bluetooth Mouse
  - Ergonomic design, suitable for all-day use
  - 12-month battery life
  - Compatible with Windows, Mac, Linux
  - Colour: Matte Black

==================================================
```

**What to observe:**
- Single, double, and triple quotes are all valid — choose based on what is inside the string
- `:.2f` inside an f-string formats a float to exactly 2 decimal places
- Triple-quoted strings preserve line breaks exactly as written — useful for product descriptions
- Calculations happen before the `print` block — keep logic and display separate

**Try it yourself:** Change `price` to `999` and `discount` to `15` — does the output update correctly?

---

## Example 2: Customer Membership Tier Checker
**Concepts:** Variables, `if/elif/else`, Boolean, comparison operators

**Scenario:** eCOMMart assigns a membership tier based on how much a customer has spent this year.

```python
# =========================================================
# Example 2: eCOMMart Membership Tier Checker
# Concepts: if / elif / else, comparison operators, booleans
# =========================================================

customer_name  = "Priya Sharma"
total_spent    = 7400.00      # ₹ spent this year
is_registered  = True         # Boolean flag

# Check if customer is registered first
if not is_registered:
    print(f"{customer_name} is not a registered eCOMMart member.")
else:
    # Determine tier using if-elif-else chain
    if total_spent >= 10000:
        tier    = "PLATINUM"
        benefit = "Free express delivery + 20% cashback on all orders"
    elif total_spent >= 5000:
        tier    = "GOLD"
        benefit = "Free standard delivery + 10% cashback"
    elif total_spent >= 2000:
        tier    = "SILVER"
        benefit = "5% cashback on orders above ₹500"
    else:
        tier    = "STANDARD"
        benefit = "No current benefits — shop to unlock rewards!"

    # How much more to reach the next tier
    if total_spent < 2000:
        gap = 2000 - total_spent
        next_tier = "SILVER"
    elif total_spent < 5000:
        gap = 5000 - total_spent
        next_tier = "GOLD"
    elif total_spent < 10000:
        gap = 10000 - total_spent
        next_tier = "PLATINUM"
    else:
        gap = 0
        next_tier = "already at top tier"

    print(f"\n  Customer   : {customer_name}")
    print(f"  Spent      : ₹{total_spent:,.2f}")
    print(f"  Tier       : ⭐ {tier}")
    print(f"  Benefits   : {benefit}")
    if gap > 0:
        print(f"  Tip        : Spend ₹{gap:,.2f} more to reach {next_tier}!")
```
```
# Output:
  Customer   : Priya Sharma
  Spent      : ₹7,400.00
  Tier       : ⭐ GOLD
  Benefits   : Free standard delivery + 10% cashback
  Tip        : Spend ₹2,600.00 more to reach PLATINUM!
```

**What to observe:**
- `not is_registered` negates a Boolean — reads like plain English
- `elif` chains are checked top to bottom — only the first `True` branch runs, the rest are skipped
- `:,` in the f-string format adds thousand separators: `7400.00` → `7,400.00`
- Two separate `if/elif/else` blocks are used — one for tier, one for the gap to next tier

**Try it yourself:** Change `total_spent` to `1500`, `4999`, and `10000` — trace which branch runs each time.

---

## Example 3: Shopping Cart with a List and Dictionary
**Concepts:** Lists, dictionaries, `for` loop, arithmetic

**Scenario:** A customer is building a cart. Items are stored in a list of dicts and the full bill is calculated.

```python
# =========================================================
# Example 3: eCOMMart Shopping Cart
# Concepts: List of dicts, for loop, arithmetic, f-strings
# =========================================================

# A cart is a list — each item is a dictionary
cart = [
    {"name": "Wireless Mouse",  "price": 499.00,  "qty": 2},
    {"name": "USB Hub",         "price": 350.00,  "qty": 1},
    {"name": "Laptop Stand",    "price": 850.00,  "qty": 1},
    {"name": "Earbuds",         "price": 1299.00, "qty": 1},
]

# Constants — uppercase names signal these never change
GST_RATE      = 0.18    # 18% GST
FREE_DELIVERY = 500     # orders above ₹500 qualify for free delivery

print("=" * 55)
print("         eCOMMart — Shopping Cart")
print("=" * 55)

subtotal = 0

# Loop through each item in the cart
for item in cart:
    line_total = item["price"] * item["qty"]
    subtotal  += line_total
    print(f"  {item['name']:<22} ₹{item['price']:>7.2f} x {item['qty']} = ₹{line_total:.2f}")

# Apply discount based on subtotal
if subtotal >= 3000:
    discount_rate = 0.20
elif subtotal >= 2000:
    discount_rate = 0.15
elif subtotal >= 1000:
    discount_rate = 0.10
else:
    discount_rate = 0.05

discount_amt   = subtotal * discount_rate
after_discount = subtotal - discount_amt
gst_amt        = after_discount * GST_RATE
grand_total    = after_discount + gst_amt

# Delivery — free if subtotal meets the threshold
delivery_charge = 0 if subtotal >= FREE_DELIVERY else 60

print("-" * 55)
print(f"  {'Subtotal':<30} ₹{subtotal:>8.2f}")
print(f"  {'Discount (' + str(int(discount_rate * 100)) + '%)':<30} -₹{discount_amt:>7.2f}")
print(f"  {'GST (18%)':<30} +₹{gst_amt:>7.2f}")
print(f"  {'Delivery':<30} {'FREE' if delivery_charge == 0 else '₹' + str(delivery_charge)}")
print("=" * 55)
print(f"  {'GRAND TOTAL':<30} ₹{grand_total + delivery_charge:>8.2f}")
print("=" * 55)
```
```
# Output:
=======================================================
         eCOMMart — Shopping Cart
=======================================================
  Wireless Mouse         ₹ 499.00 x 2 = ₹998.00
  USB Hub                ₹ 350.00 x 1 = ₹350.00
  Laptop Stand           ₹ 850.00 x 1 = ₹850.00
  Earbuds                ₹1299.00 x 1 = ₹1299.00
-------------------------------------------------------
  Subtotal                       ₹ 3497.00
  Discount (20%)                 -₹  699.40
  GST (18%)                      +₹  503.57
  Delivery                       FREE
=======================================================
  GRAND TOTAL                    ₹ 3301.17
=======================================================
```

**What to observe:**
- A **list of dictionaries** is the most common data structure for carts, catalogs, and orders
- `item["price"]` accesses the value by key inside the loop
- `{value:<22}` left-aligns in 22 characters; `{value:>8.2f}` right-aligns with 2 decimal places — columns line up cleanly
- Uppercase variable names like `GST_RATE` are a Python convention for constants
- `0 if subtotal >= FREE_DELIVERY else 60` is a ternary expression — one-line `if/else`

**Try it yourself:** Add a fifth item to the cart (e.g. `{"name": "Webcam", "price": 2499.00, "qty": 1}`) and observe how the discount tier changes.

---

## Example 4: Product Validator using Functions + `is_nan` + `safe_eval`
**Concepts:** Functions, docstrings, `is_nan`, `safe_eval_price`, `try/except`, return values

**Scenario:** eCOMMart's catalog ingestion receives raw product data — often with missing or bad values. We validate it before saving.

```python
# =========================================================
# Example 4: eCOMMart Product Validator
# Concepts: Functions, docstrings, is_nan, safe_eval, try/except
# =========================================================

import math

# ── Helper: is_nan ────────────────────────────────────────
def is_nan(value):
    """
    Returns True if a value is missing, empty, or not a usable number.

    Agent Tool Note:
        Always call this before any numeric comparison.
        Prevents crashes when data arrives from forms, APIs, or CSV files.

    Args:
        value: Any Python value.

    Returns:
        bool: True if invalid/missing, False if usable.
    """
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


# ── Helper: safe_eval_price ───────────────────────────────
def safe_eval_price(raw):
    """
    Safely converts a string input to float.

    Why not use eval() directly?
        eval("__import__('os').system('rm -rf /')") would execute!
        This wrapper only allows numeric conversion — nothing else.

    Args:
        raw (str): Raw price string from form or API.

    Returns:
        float or None: Numeric price, or None if conversion fails.
    """
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


# ── Main: validate_product ───────────────────────────────
def validate_product(product):
    """
    Validates a raw product dictionary from eCOMMart's catalog feed.

    Checks:
        - name is a non-empty string
        - price is a valid positive number
        - category is one of the allowed categories
        - stock_qty is a non-negative integer

    Agent Tool Note:
        This is the pattern for an agent's input-validation tool.
        It receives raw data, checks it, and returns a structured result.

    Args:
        product (dict): Raw product data with keys: name, price, category, stock_qty.

    Returns:
        dict: {"valid": bool, "errors": list, "cleaned": dict or None}
    """
    ALLOWED_CATEGORIES = {"Electronics", "Accessories", "Wearables", "Home & Kitchen"}
    errors  = []
    cleaned = {}

    # Validate name
    name = product.get("name", "")
    if is_nan(name) or not isinstance(name, str) or len(name.strip()) == 0:
        errors.append("Product name is missing or empty.")
    else:
        cleaned["name"] = name.strip().title()

    # Validate price
    raw_price = product.get("price")
    price = safe_eval_price(str(raw_price)) if raw_price is not None else None
    if is_nan(price) or price is None or price <= 0:
        errors.append(f"Price '{raw_price}' is invalid. Must be a positive number.")
    else:
        cleaned["price"] = round(price, 2)

    # Validate category
    category = product.get("category", "")
    if category not in ALLOWED_CATEGORIES:
        errors.append(f"Category '{category}' is not allowed. Choose from: {sorted(ALLOWED_CATEGORIES)}")
    else:
        cleaned["category"] = category

    # Validate stock_qty
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
        "cleaned": cleaned if len(errors) == 0 else None
    }


# ── Test with sample products ─────────────────────────────
test_products = [
    {"name": "wireless mouse",  "price": "499",  "category": "Electronics",    "stock_qty": 120},
    {"name": "",                "price": "850",  "category": "Accessories",    "stock_qty": 30},
    {"name": "Smart Watch",     "price": "abc",  "category": "Wearables",      "stock_qty": 50},
    {"name": "Mystery Item",    "price": "199",  "category": "Food & Grocery", "stock_qty": -5},
    {"name": "Earbuds Pro",     "price": None,   "category": "Electronics",    "stock_qty": 80},
    {"name": "USB Hub",         "price": "350",  "category": "Electronics",    "stock_qty": 0},
]

print("=" * 60)
print("     eCOMMart — Product Catalog Validation Report")
print("=" * 60)

for i, prod in enumerate(test_products, start=1):
    result = validate_product(prod)
    status = "✅ VALID" if result["valid"] else "❌ INVALID"
    print(f"\n  Product {i}: {prod.get('name', '(no name)')} — {status}")
    if result["valid"]:
        print(f"    Cleaned : {result['cleaned']}")
    else:
        for err in result["errors"]:
            print(f"    ⚠  {err}")

print("\n" + "=" * 60)
```
```
# Output:
============================================================
     eCOMMart — Product Catalog Validation Report
============================================================

  Product 1: wireless mouse — ✅ VALID
    Cleaned : {'name': 'Wireless Mouse', 'price': 499.0, 'category': 'Electronics', 'stock_qty': 120}

  Product 2:  — ❌ INVALID
    ⚠  Product name is missing or empty.

  Product 3: Smart Watch — ❌ INVALID
    ⚠  Price 'abc' is invalid. Must be a positive number.

  Product 4: Mystery Item — ❌ INVALID
    ⚠  Category 'Food & Grocery' is not allowed. Choose from: ['Accessories', 'Electronics', 'Home & Kitchen', 'Wearables']
    ⚠  stock_qty must be 0 or greater.

  Product 5: Earbuds Pro — ❌ INVALID
    ⚠  Price 'None' is invalid. Must be a positive number.

  Product 6: USB Hub — ✅ VALID
    Cleaned : {'name': 'Usb Hub', 'price': 350.0, 'category': 'Electronics', 'stock_qty': 0}

============================================================
```

**What to observe:**
- Functions with clear **docstrings** are self-documenting — agents and humans both read them
- `product.get("name", "")` safely retrieves a dict key with a fallback default — no `KeyError`
- The function returns a **dictionary** (`{"valid": ..., "errors": ..., "cleaned": ...}`) — this is the standard pattern for agent tool responses
- `try/except` inside a function keeps errors contained — `stock_qty` validation handles both `ValueError` and `TypeError` cleanly
- **Note on `.title()`:** `"USB Hub".title()` → `"Usb Hub"` — Python's `.title()` capitalises only the letter immediately after a non-letter character. For acronyms, add a custom mapping or use `.upper()` selectively

**Try it yourself:** Add a seventh product with `price: "-50"` — trace which validation check catches it.

---

## Example 5: Inventory Manager using Sets and a Menu Loop
**Concepts:** Sets, `while` loop, `try/except`, functions, menu-driven program

**Scenario:** A warehouse manager uses a terminal program to manage which products are in stock.

```python
# =========================================================
# Example 5: eCOMMart Inventory Manager
# Concepts: Sets, while loop, try/except, functions, user menu
# =========================================================

def display_menu():
    """Prints the inventory manager menu."""
    print("\n" + "─" * 40)
    print("   eCOMMart Inventory Manager")
    print("─" * 40)
    print("  1. View all products in stock")
    print("  2. Add a product")
    print("  3. Remove a product")
    print("  4. Check if a product is in stock")
    print("  5. View products in BOTH stores")
    print("  6. View products in EITHER store (not both)")
    print("  0. Exit")
    print("─" * 40)


def get_choice(prompt, valid_options):
    """
    Safely reads a menu choice from the user.

    Args:
        prompt        (str): Question to show the user.
        valid_options (set): Allowed values.

    Returns:
        str: The validated user choice.
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"  ⚠  Please enter one of: {sorted(valid_options)}")


# Starting inventory — a set ensures no duplicates
store_A = {"Wireless Mouse", "Laptop Stand", "USB Hub", "Earbuds"}
store_B = {"Smart Watch",    "Laptop Stand", "Phone Case", "Earbuds"}

while True:
    display_menu()
    choice = get_choice("  Enter your choice: ", {"0","1","2","3","4","5","6"})

    if choice == "0":
        print("\n  Exiting Inventory Manager. Goodbye!")
        break

    elif choice == "1":
        print(f"\n  Store A stock ({len(store_A)} items): {sorted(store_A)}")
        print(f"  Store B stock ({len(store_B)} items): {sorted(store_B)}")

    elif choice == "2":
        product = input("  Enter product name to add (Store A): ").strip().title()
        if product:
            store_A.add(product)
            print(f"  ✅ '{product}' added to Store A.")
        else:
            print("  ⚠  Product name cannot be empty.")

    elif choice == "3":
        product = input("  Enter product name to remove (Store A): ").strip().title()
        store_A.discard(product)   # discard does NOT raise an error if not found
        print(f"  ✅ '{product}' removed from Store A (if it existed).")

    elif choice == "4":
        product = input("  Enter product name to check: ").strip().title()
        in_A = product in store_A
        in_B = product in store_B
        if in_A and in_B:
            print(f"  ✅ '{product}' is in BOTH stores.")
        elif in_A:
            print(f"  ✅ '{product}' is in Store A only.")
        elif in_B:
            print(f"  ✅ '{product}' is in Store B only.")
        else:
            print(f"  ❌ '{product}' is not in stock at any store.")

    elif choice == "5":
        common = store_A.intersection(store_B)
        print(f"\n  Products in BOTH stores: {sorted(common)}")

    elif choice == "6":
        exclusive = store_A.symmetric_difference(store_B)
        print(f"\n  Products in EITHER store (not both): {sorted(exclusive)}")
```

```
# Sample Session (choices: 1, 5, 6, 0):

────────────────────────────────────────
   eCOMMart Inventory Manager
────────────────────────────────────────
  1. View all products in stock
  ...
  0. Exit
────────────────────────────────────────
  Enter your choice: 1

  Store A stock (4 items): ['Earbuds', 'Laptop Stand', 'USB Hub', 'Wireless Mouse']
  Store B stock (4 items): ['Earbuds', 'Laptop Stand', 'Phone Case', 'Smart Watch']

  Enter your choice: 5

  Products in BOTH stores: ['Earbuds', 'Laptop Stand']

  Enter your choice: 6

  Products in EITHER store (not both): ['Phone Case', 'Smart Watch', 'USB Hub', 'Wireless Mouse']

  Enter your choice: 0

  Exiting Inventory Manager. Goodbye!
```

**What to observe:**
- **Sets** automatically prevent duplicate entries — the ideal structure for inventory tracking
- `.discard()` removes an item without raising an error if absent; `.remove()` would raise a `KeyError`
- `.intersection()` finds items in both sets; `.symmetric_difference()` finds items in exactly one set
- `while True` with `break` is the standard pattern for a menu-driven terminal program
- `get_choice()` encapsulates input validation — clean, reusable, and testable in isolation

**Try it yourself:** Run the program and try option `2` to add a product, then option `4` to find it. Then try option `3` to remove it and option `4` again.

---

## Example 6: The eCOMMart Mini Agent Tool
**Concepts:** All Week 3 topics combined

**Scenario:** A customer sends a request. The agent tool validates it, looks up products, checks stock, applies pricing, and returns a structured result — exactly the pattern an AI agent uses with a tool call.

```python
# =========================================================
# Example 6: eCOMMart Mini Agent Tool
# ALL Week 3 concepts: variables, strings, collections,
# conditions, loops, functions, is_nan, safe_eval, exceptions
# =========================================================

import math

# ──────────────────────────────────────────────────────────
# SECTION 1: Product Catalog (Dictionary + List)
# ──────────────────────────────────────────────────────────

CATALOG = {
    "WM-4021": {"name": "Wireless Mouse",  "category": "Electronics", "price": 499.00,  "stock": 120},
    "LS-7800": {"name": "Laptop Stand",    "category": "Accessories", "price": 850.00,  "stock": 0},
    "UH-1102": {"name": "USB Hub",         "category": "Electronics", "price": 350.00,  "stock": 45},
    "SW-9001": {"name": "Smart Watch",     "category": "Wearables",   "price": 2999.00, "stock": 30},
    "EB-3310": {"name": "Earbuds Pro",     "category": "Electronics", "price": 1299.00, "stock": 80},
    "PC-0055": {"name": "Phone Case",      "category": "Accessories", "price": 199.00,  "stock": 200},
}

DELIVERY_ZONES = {
    "40": ("Mumbai",    "Same-day delivery"),
    "56": ("Bangalore", "Next-day delivery"),
    "11": ("Delhi",     "2-day delivery"),
    "50": ("Pune",      "Next-day delivery"),
}


# ──────────────────────────────────────────────────────────
# SECTION 2: Helper Functions (Agent Tool Foundations)
# ──────────────────────────────────────────────────────────

def is_nan(value):
    """Returns True if value is missing, empty, or NaN."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def safe_eval_price(raw):
    """Safely converts a string to float. Returns None on failure."""
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


# ──────────────────────────────────────────────────────────
# SECTION 3: Business Logic Functions (Reusable Tools)
# ──────────────────────────────────────────────────────────

def get_product(sku):
    """
    Looks up a product by SKU in the eCOMMart catalog.

    Agent Tool Use:
        Call when customer asks 'Tell me about product WM-4021'
        or when checkout needs product details.

    Args:
        sku (str): Product SKU code.

    Returns:
        dict: {"found": bool, "product": dict or None, "message": str}
    """
    sku = sku.strip().upper()
    if sku in CATALOG:
        return {"found": True, "product": CATALOG[sku], "message": "Product found."}
    return {"found": False, "product": None, "message": f"SKU '{sku}' not found in catalog."}


def check_delivery(pin_code):
    """
    Returns delivery zone and estimated time for a PIN code.

    Agent Tool Use:
        Call when customer asks 'When will my order arrive?'

    Args:
        pin_code (str): 6-digit customer PIN code.

    Returns:
        dict: {"zone": str, "eta": str, "free_delivery_threshold": int}
    """
    if is_nan(pin_code) or len(str(pin_code)) < 6:
        return {"zone": "Unknown", "eta": "Cannot determine", "free_delivery_threshold": 500}

    prefix = str(pin_code)[:2]
    if prefix in DELIVERY_ZONES:
        zone, eta = DELIVERY_ZONES[prefix]
    else:
        zone, eta = "Other", "5-7 business days"

    return {"zone": zone, "eta": eta, "free_delivery_threshold": 500}


def get_discount_rate(cart_total):
    """
    Returns the applicable discount rate for a given cart total.

    Args:
        cart_total (float): Total value of the cart in INR.

    Returns:
        float: Discount rate as a decimal (e.g. 0.15 = 15%).
    """
    if cart_total >= 3000:
        return 0.20
    elif cart_total >= 2000:
        return 0.15
    elif cart_total >= 1000:
        return 0.10
    elif cart_total >= 500:
        return 0.05
    return 0.0


def process_order(sku_list, pin_code):
    """
    Processes a customer order end-to-end.

    This is the main agent tool — it combines all helper functions:
    lookup → stock check → discount → delivery → structured output.

    Agent Tool Use:
        Call when customer says 'I want to order WM-4021 x2 and UH-1102 x1'

    Args:
        sku_list (list of tuples): [(sku, qty), ...]
        pin_code (str): Customer's delivery PIN code.

    Returns:
        dict: Full order summary with items, pricing, and delivery info.
    """
    order_items = []
    subtotal    = 0.0
    issues      = []

    # Step 1: Validate and look up each product
    for sku, raw_qty in sku_list:
        qty = safe_eval_price(str(raw_qty))
        if is_nan(qty) or qty is None or qty <= 0:
            issues.append(f"Invalid quantity for SKU {sku}: '{raw_qty}'")
            continue

        qty = int(qty)
        result = get_product(sku)

        if not result["found"]:
            issues.append(result["message"])
            continue

        product = result["product"]

        # Check stock
        if product["stock"] == 0:
            issues.append(f"'{product['name']}' is out of stock.")
            continue
        if product["stock"] < qty:
            issues.append(f"Only {product['stock']} units of '{product['name']}' available.")
            qty = product["stock"]   # adjust to available stock

        line_total = product["price"] * qty
        subtotal  += line_total
        order_items.append({
            "name"      : product["name"],
            "sku"       : sku,
            "price"     : product["price"],
            "qty"       : qty,
            "line_total": line_total,
        })

    if not order_items:
        return {"success": False, "issues": issues, "summary": None}

    # Step 2: Calculate pricing
    discount_rate  = get_discount_rate(subtotal)
    discount_amt   = subtotal * discount_rate
    after_discount = subtotal - discount_amt
    gst_amt        = after_discount * 0.18
    grand_total    = after_discount + gst_amt

    # Step 3: Delivery info
    delivery      = check_delivery(pin_code)
    delivery_free = subtotal >= delivery["free_delivery_threshold"]

    # Step 4: Return structured output
    return {
        "success": True,
        "issues" : issues,
        "summary": {
            "items"        : order_items,
            "subtotal"     : round(subtotal, 2),
            "discount_rate": discount_rate,
            "discount_amt" : round(discount_amt, 2),
            "gst_amt"      : round(gst_amt, 2),
            "grand_total"  : round(grand_total, 2),
            "delivery"     : delivery,
            "delivery_free": delivery_free,
        }
    }


# ──────────────────────────────────────────────────────────
# SECTION 4: Output Formatter (Display Function)
# ──────────────────────────────────────────────────────────

def print_order_summary(order):
    """Prints a formatted order summary from the process_order result."""
    print("\n" + "=" * 60)
    print("         eCOMMart — Order Summary")
    print("=" * 60)

    if not order["success"]:
        print("  ❌ Order could not be processed.")
        for issue in order["issues"]:
            print(f"     ⚠  {issue}")
        return

    s = order["summary"]

    # Items
    for item in s["items"]:
        print(f"  {item['name']:<25} ₹{item['price']:>7.2f} x {item['qty']} = ₹{item['line_total']:.2f}")

    # Warnings / partial issues
    if order["issues"]:
        print("\n  ⚠  Notes:")
        for issue in order["issues"]:
            print(f"     - {issue}")

    # Pricing breakdown
    print("-" * 60)
    print(f"  {'Subtotal':<35} ₹{s['subtotal']:>8.2f}")
    print(f"  {'Discount (' + str(int(s['discount_rate']*100)) + '%)':<35} -₹{s['discount_amt']:>7.2f}")
    print(f"  {'GST (18%)':<35} +₹{s['gst_amt']:>7.2f}")
    print(f"  {'Delivery':<35} {'FREE ✓' if s['delivery_free'] else '₹60.00'}")
    print("=" * 60)
    grand = s['grand_total'] + (0 if s['delivery_free'] else 60)
    print(f"  {'GRAND TOTAL':<35} ₹{grand:>8.2f}")
    print("=" * 60)

    # Delivery info
    d = s["delivery"]
    print(f"\n  📦 Delivering to  : {d['zone']}")
    print(f"     Estimated time : {d['eta']}")
    print("=" * 60)


# ──────────────────────────────────────────────────────────
# SECTION 5: Run the Agent Tool
# ──────────────────────────────────────────────────────────

# Test Order 1 — valid order, Mumbai zone
order1 = process_order(
    sku_list=[("WM-4021", 2), ("UH-1102", 1), ("EB-3310", 1)],
    pin_code="400001"
)
print_order_summary(order1)

# Test Order 2 — out-of-stock item and invalid qty
order2 = process_order(
    sku_list=[("LS-7800", 1), ("SW-9001", "abc"), ("PC-0055", 3)],
    pin_code="560078"
)
print_order_summary(order2)

# Test Order 3 — unknown SKU and unknown PIN zone
order3 = process_order(
    sku_list=[("XX-9999", 1), ("PC-0055", 2)],
    pin_code="302001"
)
print_order_summary(order3)
```

```
# Output — Order 1 (valid, Mumbai):
============================================================
         eCOMMart — Order Summary
============================================================
  Wireless Mouse            ₹ 499.00 x 2 = ₹998.00
  USB Hub                   ₹ 350.00 x 1 = ₹350.00
  Earbuds Pro               ₹1299.00 x 1 = ₹1299.00
------------------------------------------------------------
  Subtotal                            ₹ 2647.00
  Discount (15%)                      -₹  397.05
  GST (18%)                           +₹  404.99
  Delivery                            FREE ✓
============================================================
  GRAND TOTAL                         ₹ 2654.94
============================================================

  📦 Delivering to  : Mumbai
     Estimated time : Same-day delivery
============================================================

# Output — Order 2 (out-of-stock + bad qty):
============================================================
         eCOMMart — Order Summary
============================================================
  Phone Case                ₹ 199.00 x 3 = ₹597.00

  ⚠  Notes:
     - 'Laptop Stand' is out of stock.
     - Invalid quantity for SKU SW-9001: 'abc'
------------------------------------------------------------
  Subtotal                            ₹  597.00
  Discount (5%)                       -₹   29.85
  GST (18%)                           +₹  102.09
  Delivery                            FREE ✓
============================================================
  GRAND TOTAL                         ₹  669.24
============================================================

  📦 Delivering to  : Bangalore
     Estimated time : Next-day delivery
============================================================

# Output — Order 3 (unknown SKU + unknown zone):
============================================================
         eCOMMart — Order Summary
============================================================
  Phone Case                ₹ 199.00 x 2 = ₹398.00

  ⚠  Notes:
     - SKU 'XX-9999' not found in catalog.
------------------------------------------------------------
  Subtotal                            ₹  398.00
  Discount (0%)                       -₹    0.00
  GST (18%)                           +₹   71.64
  Delivery                            ₹60.00
============================================================
  GRAND TOTAL                         ₹  529.64
============================================================

  📦 Delivering to  : Other
     Estimated time : 5-7 business days
============================================================
```

**What to observe — the full Week 3 picture in one program:**

| Section | Concepts shown |
|---|---|
| `CATALOG`, `DELIVERY_ZONES` | Dictionaries as the data layer — real structure for a product database |
| `is_nan`, `safe_eval_price` | Input validation before every numeric operation — agent tool foundations |
| `get_product`, `check_delivery` | Functions with docstrings and structured dict return values — the agent tool contract |
| `process_order` — `for sku, raw_qty in sku_list` | Loop with tuple unpacking; `continue` skips bad items without crashing |
| Stock check block | Nested `if` conditions; in-place qty adjustment when stock is short |
| `get_discount_rate` | Pure function — single responsibility, easy to test |
| `print_order_summary` | Separates display from logic — the function only formats, never calculates |
| Order 2 output | Partial success — some items failed, one succeeded; issues reported without crashing |
| Order 3 output | Unknown zone handled gracefully — falls back to "Other" / standard delivery |

**Try it yourself:**
1. Add `"PC-0055"` to Order 1's `sku_list` with `qty=100` — observe the stock adjustment note
2. Change Order 3's PIN code to `"560001"` (Bangalore) — observe the delivery zone change
3. Add a new SKU to `CATALOG` and order it — the tool picks it up immediately
