# Reviewing Python Functions and Dictionaries
## eCOMMart AI Squad | Week 4

> Before we introduce classes, we need to look honestly at code you already know how to write —
> and identify exactly where it starts to break down. That breaking point is where OOP begins.

---

## What We Will Cover

1. What you already know — a quick recap
2. Modelling a product with variables
3. Modelling a product with a dictionary
4. Modelling behaviour with functions
5. Where the dictionary + function approach breaks down
6. The problem with scale — what happens when you have 50 products
7. What we need instead — a preview
8. Tasks

---

## 1. What You Already Know

By the end of Week 3 you could:

- Store product data in **variables** and **dictionaries**
- Write **functions** that accept data, process it, and return a result
- Build a complete interactive **order terminal** using loops, conditions, and functions

That is genuinely a lot. The Week 3 capstone — the eCOMMart Order Terminal — is a real, working program. So why do we need anything more?

The answer is: **structure**. As programs grow, the gap between *working* and *well-structured* becomes the difference between code you can maintain and code that becomes impossible to change safely.

---

## 2. Modelling a Product with Variables

In Week 3 you stored a product like this:

```python
product_name     = "Wireless Mouse"
product_sku      = "WM-4021"
product_price    = 499.00
product_category = "Electronics"
product_stock    = 120
product_rating   = 4.5
product_in_stock = True
```

This works perfectly for **one product**. But notice what happens the moment you have a second:

```python
# Product 1
product1_name     = "Wireless Mouse"
product1_sku      = "WM-4021"
product1_price    = 499.00
product1_category = "Electronics"
product1_stock    = 120

# Product 2
product2_name     = "Laptop Stand"
product2_sku      = "LS-7800"
product2_price    = 850.00
product2_category = "Accessories"
product2_stock    = 0
```

You now have **10 separate variables** for 2 products. For 10 products, that is 50 variables — with no connection between them. If you rename `product1_price` to `product1_mrp` you must remember to rename every other product's field too. One typo and the program breaks in a way that is very hard to find.

```
Problem:   Variables are disconnected — they share no structure.
           The connection between them exists only in your naming convention.
           Python itself has no idea that product1_name and product1_price
           belong together.
```

---

## 3. Modelling a Product with a Dictionary

Week 3 introduced a better approach — grouping related data into a dictionary:

```python
product = {
    "name"    : "Wireless Mouse",
    "sku"     : "WM-4021",
    "price"   : 499.00,
    "category": "Electronics",
    "stock"   : 120,
    "rating"  : 4.5,
    "in_stock": True
}
```

This is a genuine improvement. The product's data is now **grouped under one name**. You can pass `product` to a function instead of passing 7 separate arguments.

Multiple products become a list of dictionaries:

```python
catalog = [
    {
        "name"    : "Wireless Mouse",
        "sku"     : "WM-4021",
        "price"   : 499.00,
        "category": "Electronics",
        "stock"   : 120,
        "rating"  : 4.5,
        "in_stock": True
    },
    {
        "name"    : "Laptop Stand",
        "sku"     : "LS-7800",
        "price"   : 850.00,
        "category": "Accessories",
        "stock"   : 0,
        "rating"  : 4.2,
        "in_stock": False
    },
    {
        "name"    : "Smart Watch",
        "sku"     : "SW-9001",
        "price"   : 2999.00,
        "category": "Wearables",
        "stock"   : 30,
        "rating"  : 4.7,
        "in_stock": True
    }
]

# Iterate and display
for p in catalog:
    status = "✅ In Stock" if p["in_stock"] else "❌ Out of Stock"
    print(f"  {p['sku']}  {p['name']:<20} ₹{p['price']:<8.2f}  {status}")
```
```
# Output:
  WM-4021  Wireless Mouse       ₹499.00    ✅ In Stock
  LS-7800  Laptop Stand         ₹850.00    ❌ Out of Stock
  SW-9001  Smart Watch          ₹2999.00   ✅ In Stock
```

This is already much better — and it is exactly the pattern the Week 3 capstone used.

---

## 4. Modelling Behaviour with Functions

A dictionary holds data. Functions hold behaviour — the things you can *do* with that data.

Here is the pattern you used in Week 3: pass a product dictionary to a function, get a result back.

```python
def apply_discount(product, discount_pct):
    """
    Applies a percentage discount to a product's price.

    Args:
        product      (dict): A product dictionary with at least a 'price' key.
        discount_pct (float): Discount percentage (e.g. 10 for 10%).

    Returns:
        float: The discounted price.
    """
    discount_amount = product["price"] * (discount_pct / 100)
    return product["price"] - discount_amount


def check_stock(product, qty_requested):
    """
    Checks whether the requested quantity is available.

    Args:
        product       (dict): A product dictionary with a 'stock' key.
        qty_requested (int): How many units the customer wants.

    Returns:
        bool: True if stock is sufficient, False otherwise.
    """
    return product["stock"] >= qty_requested


def print_product_card(product):
    """
    Prints a formatted product card to the terminal.

    Args:
        product (dict): A product dictionary.
    """
    status = "✅ In Stock" if product["in_stock"] else "❌ Out of Stock"
    print("=" * 48)
    print(f"  {product['name']}")
    print(f"  SKU      : {product['sku']}")
    print(f"  Category : {product['category']}")
    print(f"  Price    : ₹{product['price']:.2f}")
    print(f"  Rating   : ⭐ {product['rating']}")
    print(f"  Status   : {status}")
    print("=" * 48)
```

```python
# Use the functions together
mouse = {
    "name"    : "Wireless Mouse",
    "sku"     : "WM-4021",
    "price"   : 499.00,
    "category": "Electronics",
    "stock"   : 120,
    "rating"  : 4.5,
    "in_stock": True
}

print_product_card(mouse)

sale_price = apply_discount(mouse, 15)
print(f"\n  Sale Price (15% off): ₹{sale_price:.2f}")

has_stock = check_stock(mouse, 5)
print(f"  Can order 5 units?  : {'Yes' if has_stock else 'No'}")
```
```
# Output:
================================================
  Wireless Mouse
  SKU      : WM-4021
  Category : Electronics
  Price    : ₹499.00
  Rating   : ⭐ 4.5
  Status   : ✅ In Stock
================================================

  Sale Price (15% off): ₹424.15
  Can order 5 units?  : Yes
```

This is clean, readable code. So what is the problem?

---

## 5. Where the Dictionary + Function Approach Breaks Down

### Problem 1 — Data and behaviour are completely separate

The `mouse` dictionary knows nothing about `apply_discount` or `check_stock`. The functions know nothing about each other. They are held together only by the fact that you are passing the same dictionary into each one — which is a convention that you follow by choice, not a structure that you MUST adhere to.

If a new developer joins the team they have no way to know which functions belong to which data. There is no signpost that says: *"these three functions are meant to work on product dictionaries."*

```python
# Nothing stops someone from accidentally passing the wrong dict
order = {"order_id": "ORD-001", "customer": "Priya", "total": 1200}

# This runs without error but produces nonsense
print(apply_discount(order, 10))   # KeyError: 'price'
```
```
# Output:
KeyError: 'price'
```

### Problem 2 — No guaranteed structure

Any code in your program can add, remove, or rename a key in any dictionary at any time. There is nothing stopping this:

```python
mouse["price"] = "free"          # price is now a string — will crash apply_discount
del mouse["stock"]               # check_stock will now raise KeyError
mouse["prce"] = 199              # typo — now there are two price-like keys
```

With dictionaries, Python has no way to say *"this dictionary must always have these exact keys with these exact types."* There is no contract.

### Problem 3 — Code duplication across similar things

eCOMMart sells products. It also has sellers, customers, and orders. Each of these needs similar patterns — a way to display them, a way to validate them, a way to calculate something about them.

With the dictionary + function approach, you end up with:

```python
def print_product_card(product):   ...
def print_seller_card(seller):     ...
def print_customer_card(customer): ...
def print_order_card(order):       ...
```

Four functions doing almost the same thing. If you change the display format, you change it in four places — and hope you don't miss one.

### Problem 4 — A function cannot carry state between calls

A function runs, returns a result, and forgets everything. It cannot remember how many times it has been called, or what the previous product was, or maintain a running total across multiple calls — unless you use a global variable, which creates its own problems.

```python
# Fragile — a global variable shared across the whole program
total_products_viewed = 0

def view_product(product):
    global total_products_viewed
    total_products_viewed += 1
    print_product_card(product)
```

This works but it is brittle. Any part of the program can accidentally modify `total_products_viewed`, and there is no clean way to have *separate* view counters for different users.

---

## 6. The Problem with Scale — 50 Products, 3 Sellers, 200 Orders

Let us be concrete about what the Week 3 capstone would look like if eCOMMart grew slightly:

```
catalog         → list of 50 product dicts
sellers         → list of 12 seller dicts
orders          → list of 200 order dicts

Functions needed:
  print_product_card()      apply_product_discount()   check_product_stock()
  validate_product()        update_product_price()      archive_product()

  print_seller_card()       get_seller_rating()         update_seller_stock()
  validate_seller()         deactivate_seller()

  print_order_card()        calculate_order_total()     apply_order_discount()
  validate_order()          cancel_order()              ship_order()
```

That is 17+ functions with no clear grouping. Every function signature includes either `product`, `seller`, or `order` as its first parameter — a strong hint that these functions *belong* to those data structures, but the language has no way to express that.

```
┌─────────────────────────────────────────────────────────────────┐
│  The bigger the program, the more disconnected it gets.         │
│  Every new feature adds more standalone functions.              │
│  The data (dicts) and the behaviour (functions) drift apart.    │
│  Bugs become harder to find. Changes become harder to make.     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. What We Need Instead — A Preview

What if you could tell Python: *"bundle this data and these functions together into a single thing, and make sure the data always has the right shape"*?

That is exactly what a **class** does.

```python
# Week 3 approach — data and functions separate
mouse = {"name": "Wireless Mouse", "price": 499.00, "stock": 120}

def apply_discount(product, pct):
    return product["price"] * (1 - pct / 100)

sale_price = apply_discount(mouse, 15)
```

```python
# Week 4 approach — data and functions bundled together (preview only)
class Product:
    def __init__(self, name, price, stock):
        self.name  = name
        self.price = price
        self.stock = stock

    def apply_discount(self, pct):
        return self.price * (1 - pct / 100)

mouse      = Product("Wireless Mouse", 499.00, 120)
sale_price = mouse.apply_discount(15)
```

In the class version:
- The data (`name`, `price`, `stock`) lives **inside** the object
- The function `apply_discount` lives **inside** the same object
- They belong together — and Python enforces that connection
- Every `Product` you create is guaranteed to have `name`, `price`, and `stock`

Do not worry about the syntax yet — the next file covers it in full. The point of this file is to understand **why** you need it.

```
┌─────────────────────────────────────────────────────────────────┐
│  Classes solve the three core problems:                         │
│                                                                 │
│  ✅  Data + behaviour bundled together — no separation          │
│  ✅  Guaranteed structure — every object has the same fields    │
│  ✅  Behaviour reused across similar things via inheritance     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Tasks

### Task 1 — Spot the Problems

Read the code below. It uses the dictionary + function pattern from Week 3. Identify **at least three things** that could go wrong as this program grows.

```python
def calculate_gst(product):
    return product["price"] * 0.18

def is_eligible_for_free_delivery(product):
    return product["price"] >= 500

catalog = [
    {"name": "USB Hub",     "price": 350, "stock": 45},
    {"name": "Smart Watch", "price": 2999},          # missing stock key
    {"name": "Earbuds Pro", "price": "1299"},        # price is a string
]

for product in catalog:
    gst = calculate_gst(product)
    print(f"{product['name']} — GST: ₹{gst:.2f}")
```

**Write your answers as comments in a `.py` file. Then run the code and observe what actually breaks.**

---

### Task 2 — Extend the Pattern (and feel the pain)

Using only dictionaries and functions (no classes), build the following for eCOMMart:

- A `seller` dictionary with keys: `name`, `city`, `rating`, `total_sales`, `is_verified`
- A `customer` dictionary with keys: `name`, `email`, `membership_tier`, `total_spent`
- A function `print_seller_card(seller)` that prints a formatted seller profile
- A function `print_customer_card(customer)` that prints a formatted customer profile
- A function `get_loyalty_discount(customer)` that returns a discount % based on `membership_tier`:
  - `"PLATINUM"` → 20%, `"GOLD"` → 10%, `"SILVER"` → 5%, `"STANDARD"` → 0%

```python
# Build your solution here

seller = {
    "name"       : "TechPro Distributors",
    "city"       : "Mumbai",
    "rating"     : 4.8,
    "total_sales": 15200,
    "is_verified": True
}

customer = {
    "name"          : "Priya Sharma",
    "email"         : "priya@example.com",
    "membership_tier": "GOLD",
    "total_spent"   : 7400.00
}

def print_seller_card(seller):
    verified = "✅ Verified" if seller["is_verified"] else "⚠️  Unverified"
    print("=" * 44)
    print(f"  Seller   : {seller['name']}")
    print(f"  City     : {seller['city']}")
    print(f"  Rating   : ⭐ {seller['rating']}")
    print(f"  Sales    : {seller['total_sales']} units")
    print(f"  Status   : {verified}")
    print("=" * 44)

def print_customer_card(customer):
    print("=" * 44)
    print(f"  Customer : {customer['name']}")
    print(f"  Email    : {customer['email']}")
    print(f"  Tier     : {customer['membership_tier']}")
    print(f"  Spent    : ₹{customer['total_spent']:.2f}")
    print("=" * 44)

def get_loyalty_discount(customer):
    tiers = {
        "PLATINUM": 20,
        "GOLD"    : 10,
        "SILVER"  :  5,
        "STANDARD":  0
    }
    return tiers.get(customer["membership_tier"], 0)

print_seller_card(seller)
print()
print_customer_card(customer)
discount = get_loyalty_discount(customer)
print(f"\n  Loyalty Discount for {customer['name']}: {discount}%")
```
```
# Expected Output:
============================================
  Seller   : TechPro Distributors
  City     : Mumbai
  Rating   : ⭐ 4.8
  Sales    : 15200 units
  Status   : ✅ Verified
============================================

============================================
  Customer : Priya Sharma
  Email    : priya@example.com
  Tier     : GOLD
  Spent    : ₹7400.00
============================================

  Loyalty Discount for Priya Sharma: 10%
```

**Once you have it working, ask yourself:** if eCOMMart now needs a `Vendor` that is similar to both a `Seller` and a `Customer`, how would you build it without duplicating code? Keep that question in mind as you move to the next file.

---

## Summary

| Approach | What it handles well | Where it breaks down |
|---|---|---|
| Plain variables | A single item with a few fields | More than one item — naming becomes unmanageable |
| Dictionary | Grouped data for one item, list of dicts for many | No guaranteed structure, no type safety, data and behaviour are separate |
| Functions | Reusable behaviour on any dict | No ownership — functions float free with no connection to the data they serve |
| **Class** (next) | Data + behaviour bundled, guaranteed structure, reusable patterns | — covered in the next file |

> **You are not leaving dictionaries and functions behind.**
> Classes use both internally. A class is a better way to *organise* them —
> not a replacement for the concepts themselves.

---

*Next: `02_What_is_OOP_and_Why_It_Matters.md`*
