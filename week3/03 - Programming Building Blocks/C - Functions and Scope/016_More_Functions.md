# More Functions

In this notebook we go deeper into how functions work — default values, positional and keyword arguments, accepting any number of arguments, and returning multiple values. These are the patterns you will use constantly in real Python code and in agent tool design.

**What we will cover:**

1. Default argument values
2. Positional arguments
3. Wrong argument order — the error and why it happens
4. Keyword arguments
5. Mixing positional and keyword with `None` defaults
6. `*args` — accepting any number of positional arguments
7. `**kwargs` — accepting any number of keyword arguments
8. Returning multiple values
9. Exercise — Agent tool combining all concepts

> **Note:** The `get_discount_rate()` function from `021_Functions` is used here. Make sure it is defined before running these examples.

```python
def get_discount_rate(cart_total):
    if cart_total >= 3000: return 0.25
    elif cart_total >= 2000: return 0.15
    elif cart_total >= 1000: return 0.10
    elif cart_total >= 500:  return 0.05
    else: return 0.0
```

---

## 1. Default Argument Values

You can give a parameter a **default value**. If the caller does not supply that argument, the default is used. This makes parameters optional.

```python
def greet_vendor(name='Valued Vendor'):
    print(f"\nThank you for partnering with eCOMMart, {name}!")
    print("Your products are live on our platform.")
```

```python
greet_vendor('Tata Electronics')   # uses provided name
greet_vendor('Reliance Digital')   # uses provided name
greet_vendor()                     # uses default
```
```
# Output:

Thank you for partnering with eCOMMart, Tata Electronics!
Your products are live on our platform.

Thank you for partnering with eCOMMart, Reliance Digital!
Your products are live on our platform.

Thank you for partnering with eCOMMart, Valued Vendor!
Your products are live on our platform.
```

```
greet_vendor('Tata')  →  name = 'Tata'          (caller supplied)
greet_vendor()        →  name = 'Valued Vendor'  (default used)
```

> **Rule:** Parameters with default values must come **after** parameters without defaults.
> `def f(a, b=10)` ✅ — `def f(a=10, b)` ❌ — SyntaxError

### B2B eCom examples

```python
def greet_category(category="Electronics"):
    print(f"Welcome to eCOMMart's {category} section!")

greet_category()                   # default
greet_category("Wearables")
greet_category("Home & Kitchen")
```
```
# Output:
Welcome to eCOMMart's Electronics section!
Welcome to eCOMMart's Wearables section!
Welcome to eCOMMart's Home & Kitchen section!
```

```python
def recommend_product(product="Wireless Mouse"):
    print(f"Our top pick today is: {product}")

recommend_product()                # default
recommend_product("Smart Watch")
recommend_product("Laptop Stand")
```
```
# Output:
Our top pick today is: Wireless Mouse
Our top pick today is: Smart Watch
Our top pick today is: Laptop Stand
```

---

## 2. Positional Arguments

When a function has multiple parameters, Python matches values to parameters **by position** — the first value goes to the first parameter, the second to the second, and so on:

```python
def describe_product(name, category, price):
    """
    Prints a formatted product card for eCOMMart.

    Agent Tool Use:
        Call when a customer asks 'Tell me about this product.'

    Args:
        name     (str)  : Product name
        category (str)  : Product category
        price    (float): Price in INR
    """
    print(f"Product  : {name.title()}")
    print(f"Category : {category.title()}")
    print(f"Price    : ₹{price:.2f}\n")
```

```python
describe_product('wireless mouse',  'electronics', 499.00)
describe_product('laptop stand',    'accessories', 850.00)
describe_product('smart watch',     'wearables',   2999.00)
```
```
# Output:
Product  : Wireless Mouse
Category : Electronics
Price    : ₹499.00

Product  : Laptop Stand
Category : Accessories
Price    : ₹850.00

Product  : Smart Watch
Category : Wearables
Price    : ₹2999.00
```

```
describe_product('wireless mouse', 'electronics', 499.00)
                       ↓                ↓            ↓
                      name          category       price
```

---

## 3. Wrong Argument Order — The Error and Why It Happens

If you pass arguments in the wrong order, Python assigns them by position — so the wrong value ends up in the wrong parameter. This usually causes an `AttributeError` or `TypeError`:

```python
# WRONG — price goes to name, category to category, name to price
try:
    describe_product(499.00, 'electronics', 'wireless mouse')
except AttributeError as e:
    print(f"AttributeError: {e}")
```
```
# Output:
AttributeError: 'float' object has no attribute 'title'
```

```
describe_product(499.00, 'electronics', 'wireless mouse')
                   ↓           ↓               ↓
                 name       category          price

name = 499.00  → name.title() fails because 499.00 is a float, not a string
```

> **Prevention:** Use keyword arguments (next section) whenever argument order might be unclear.

---

## 4. Keyword Arguments

With **keyword arguments**, you name each argument when calling the function. The order no longer matters:

```python
# Any order works when you name the arguments
describe_product(price=499.00, name='wireless mouse', category='electronics')
```
```
# Output:
Product  : Wireless Mouse
Category : Electronics
Price    : ₹499.00
```

```python
describe_product(category='wearables', price=2999.00, name='smart watch')
```
```
# Output:
Product  : Smart Watch
Category : Wearables
Price    : ₹2999.00
```

```
Positional → order matters:    describe_product('wireless mouse', 'electronics', 499.00)
Keyword    → order irrelevant: describe_product(price=499.00, name='wireless mouse', category='electronics')
```

---

## 5. Mixing Positional and Keyword — Optional Fields with `None`

A very common pattern: required arguments are positional; optional arguments use keyword with `None` as default. Fields that are `None` are simply not printed:

```python
def create_order(vendor, product, quantity=1, discount_pct=None, express=None):
    """
    Creates and displays an eCOMMart order summary.

    Args:
        vendor       (str)         : Vendor name (required)
        product      (str)         : Product name (required)
        quantity     (int)         : Number of units (default 1)
        discount_pct (float|None)  : Discount percentage if applicable
        express      (str|None)    : Express delivery option if applicable
    """
    print(f"Vendor   : {vendor.title()}")
    print(f"Product  : {product.title()}")
    print(f"Quantity : {quantity}")
    if discount_pct:
        print(f"Discount : {discount_pct}%")
    if express:
        print(f"Express  : {express}")
    print()
```

```python
# Only required fields
create_order('tata electronics', 'wireless mouse')
```
```
# Output:
Vendor   : Tata Electronics
Product  : Wireless Mouse
Quantity : 1
```

```python
# With optional fields
create_order('reliance digital', 'laptop stand', quantity=5, discount_pct=10)
```
```
# Output:
Vendor   : Reliance Digital
Product  : Laptop Stand
Quantity : 5
Discount : 10%
```

```python
# With express delivery
create_order('infosys supplies', 'smart watch', quantity=2, express='Same-day delivery')
```
```
# Output:
Vendor   : Infosys Supplies
Product  : Smart Watch
Quantity : 2
Express  : Same-day delivery
```

```
vendor, product  → always required   → positional
quantity         → almost always 1   → keyword with default
discount_pct     → not always        → keyword, default None
express          → not always        → keyword, default None
```

---

## 6. `*args` — Accepting Any Number of Positional Arguments

Prefix a parameter name with `*` and Python collects all extra positional arguments into a **tuple**. This lets you call the function with any number of values:

```python
def sum_orders(*amounts):
    """
    Accepts any number of order amounts and returns the total.

    Args:
        *amounts: One or more order amounts in INR.

    Returns:
        float: Total of all amounts.
    """
    print(f"Orders received: {amounts}")
    total = sum(amounts)
    print(f"Total: ₹{total:.2f}")
    return total
```

```python
sum_orders(499)
```
```
# Output:
Orders received: (499,)
Total: ₹499.00
```

```python
sum_orders(499, 850)
```
```
# Output:
Orders received: (499, 850)
Total: ₹1349.00
```

```python
sum_orders(499, 850, 2999, 350, 1299)
```
```
# Output:
Orders received: (499, 850, 2999, 350, 1299)
Total: ₹5997.00
```

### Mixing a required argument with `*args`

```python
def log_vendor_activity(vendor_name, *actions):
    """
    Logs any number of actions performed by a vendor.

    Args:
        vendor_name (str)  : The vendor's name (required)
        *actions           : One or more action descriptions
    """
    print(f"Vendor: {vendor_name}")
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
    print()
```

```python
log_vendor_activity('Tata Electronics', 'Listed 10 products')
```
```
# Output:
Vendor: Tata Electronics
  1. Listed 10 products
```

```python
log_vendor_activity('Reliance Digital',
                    'Listed 5 products',
                    'Updated pricing',
                    'Responded to 3 queries')
```
```
# Output:
Vendor: Reliance Digital
  1. Listed 5 products
  2. Updated pricing
  3. Responded to 3 queries
```

```
*actions collects all extra arguments into a tuple:
log_vendor_activity('Tata', 'Action1', 'Action2', 'Action3')
    vendor_name = 'Tata'
    actions     = ('Action1', 'Action2', 'Action3')
```

---

## 7. `**kwargs` — Accepting Any Number of Keyword Arguments

Prefix a parameter name with `**` and Python collects all extra keyword arguments into a **dictionary**. This lets callers pass any named fields they need:

```python
def create_product_listing(name, **details):
    """
    Creates a product listing with any number of extra fields.

    Args:
        name      (str)  : Product name (required)
        **details        : Any additional product fields
    """
    print(f"Product: {name.title()}")
    for key, value in details.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    print()
```

```python
create_product_listing('wireless mouse', price=499, category='Electronics', in_stock=True)
```
```
# Output:
Product: Wireless Mouse
  Price: 499
  Category: Electronics
  In Stock: True
```

```python
create_product_listing('laptop stand',
                       price=850,
                       category='Accessories',
                       warranty='1 year',
                       weight='0.8kg')
```
```
# Output:
Product: Laptop Stand
  Price: 850
  Category: Accessories
  Warranty: 1 year
  Weight: 0.8kg
```

### Checking for specific keys in `**kwargs`

```python
def process_order(order_id, **options):
    """
    Processes an order with optional configuration flags.

    Args:
        order_id  (str)  : The order ID (required)
        **options        : Optional flags — express, gift_wrap, note
    """
    print(f"Processing order: {order_id}")
    if 'express' in options:
        print(f"  Express delivery: {options['express']}")
    if 'gift_wrap' in options:
        print(f"  Gift wrap: {options['gift_wrap']}")
    if 'note' in options:
        print(f"  Note: {options['note']}")
    print()
```

```python
process_order('ORD-1001')
```
```
# Output:
Processing order: ORD-1001
```

```python
process_order('ORD-1002', express=True, gift_wrap=True)
```
```
# Output:
Processing order: ORD-1002
  Express delivery: True
  Gift wrap: True
```

```python
process_order('ORD-1003', express=True, note='Leave at reception')
```
```
# Output:
Processing order: ORD-1003
  Express delivery: True
  Note: Leave at reception
```

```
**options captures all keyword arguments as a dict:
process_order('ORD-1002', express=True, gift_wrap=True)
    order_id = 'ORD-1002'
    options  = {'express': True, 'gift_wrap': True}
```

---

## 8. Returning Multiple Values

A Python function can return more than one value by separating them with commas. The caller unpacks them into separate variables:

```python
def calculate_order_summary(cart_total):
    """
    Calculates and returns subtotal, discount, and grand total.

    Args:
        cart_total (float): The cart subtotal in INR.

    Returns:
        tuple: (subtotal, discount_amount, grand_total)
    """
    disc_rate = get_discount_rate(cart_total)
    discount  = round(cart_total * disc_rate, 2)
    grand     = round(cart_total - discount, 2)
    return cart_total, discount, grand   # returns a tuple
```

```python
subtotal, discount, grand = calculate_order_summary(2500)

print(f"Subtotal : ₹{subtotal:.2f}")
print(f"Discount : ₹{discount:.2f}")
print(f"Grand    : ₹{grand:.2f}")
```
```
# Output:
Subtotal : ₹2500.00
Discount : ₹375.00
Grand    : ₹2125.00
```

```python
subtotal, discount, grand = calculate_order_summary(800)

print(f"Subtotal : ₹{subtotal:.2f}")
print(f"Discount : ₹{discount:.2f}")
print(f"Grand    : ₹{grand:.2f}")
```
```
# Output:
Subtotal : ₹800.00
Discount : ₹40.00
Grand    : ₹760.00
```

```
return cart_total, discount, grand
       ↓
returns a tuple: (2500, 375.0, 2125.0)

subtotal, discount, grand = calculate_order_summary(2500)
   ↑          ↑        ↑
  2500      375.0   2125.0    ← unpacked
```

---

## Quick Reference — Argument Types

```
┌─────────────────┬─────────────────────────────────────────────────────┐
│  Syntax         │  What it does                                       │
├─────────────────┼─────────────────────────────────────────────────────┤
│  def f(a, b)    │  Positional — order matters                         │
│  def f(a, b=10) │  Default value — b is optional                      │
│  f(b=5, a=1)    │  Keyword call — order irrelevant                    │
│  def f(*args)   │  Collects extra positional args into a tuple        │
│  def f(**kwargs)│  Collects extra keyword args into a dict            │
│  return a, b    │  Returns multiple values as a tuple                 │
└─────────────────┴─────────────────────────────────────────────────────┘

Correct order when combining:
def f(positional, *args, keyword=default, **kwargs)
```

---

## Exercise: eCOMMart Vendor Report — Agent Tool

Build a function that combines all the argument types covered in this notebook into one agent-ready tool:

```python
def create_vendor_report(vendor_name, *product_names, currency='INR', **metadata):
    """
    eCOMMart Agent Tool: Generates a vendor summary report.

    Agent Tool Use:
        Call when the operations team requests a vendor summary,
        or when an agent needs to compile a vendor profile.

    Args:
        vendor_name    (str)  : The vendor's name (required, positional)
        *product_names        : Any number of product names
        currency       (str)  : Currency code (default 'INR')
        **metadata            : Any additional report fields (region, rating, etc.)

    Returns:
        dict: Structured report summary.
    """
    print(f"Vendor      : {vendor_name}")
    print(f"Products    : {list(product_names)}")
    print(f"Currency    : {currency}")
    for key, val in metadata.items():
        print(f"  {key.replace('_', ' ').title()}: {val}")
    print()

    return {
        'vendor':   vendor_name,
        'products': list(product_names),
        'currency': currency,
        **metadata
    }
```

```python
# Test 1 — INR vendor with multiple products and metadata
report1 = create_vendor_report(
    'Tata Electronics',
    'Wireless Mouse', 'USB Hub', 'Laptop Stand',
    region='South India',
    rating=4.8
)
print(f"Report keys: {list(report1.keys())}")
```
```
# Output:
Vendor      : Tata Electronics
Products    : ['Wireless Mouse', 'USB Hub', 'Laptop Stand']
Currency    : INR
  Region: South India
  Rating: 4.8

Report keys: ['vendor', 'products', 'currency', 'region', 'rating']
```

```python
# Test 2 — Export vendor, different currency and metadata
report2 = create_vendor_report(
    'Reliance Digital',
    'Smart Watch',
    currency='USD',
    export_ready=True,
    contact='vendor@reliance.com'
)
print(f"Report keys: {list(report2.keys())}")
```
```
# Output:
Vendor      : Reliance Digital
Products    : ['Smart Watch']
Currency    : USD
  Export Ready: True
  Contact: vendor@reliance.com

Report keys: ['vendor', 'products', 'currency', 'export_ready', 'contact']
```

```
create_vendor_report(
    'Tata Electronics',          ← vendor_name   (positional)
    'Mouse', 'Hub', 'Stand',     ← *product_names (collected into tuple)
    currency='INR',              ← keyword with default
    region='South', rating=4.8   ← **metadata    (collected into dict)
)
```
