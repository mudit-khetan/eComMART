# `*args` and `**kwargs`

In `022_More_Functions` we introduced `*args` and `**kwargs` briefly. This notebook goes deeper — covering the mechanics, every combination pattern, and a new topic: **unpacking** with `*` and `**` when calling a function.

**What we will cover:**

1. The problem — fixed argument count breaks with too many values
2. `*args` — collecting positional arguments into a tuple
3. `*args` with a required argument before it
4. `**kwargs` — collecting keyword arguments into a dictionary
5. `**kwargs` — checking for specific keys
6. Combining `*args` and `**kwargs` in one function
7. Correct parameter order when mixing all types
8. Unpacking with `*` and `**` when calling a function
9. Exercise

---

## 1. The Problem — Fixed Argument Count

A function with a fixed number of parameters breaks the moment you pass more (or fewer) values than it expects:

```python
def adder(x, y, z):
    print(f"Sum: {x + y + z}")

adder(12, 15, 19)
```
```
# Output:
Sum: 46
```

```python
# Pass 5 values to a 3-parameter function — TypeError
try:
    adder(5, 10, 15, 20, 25)
except TypeError as e:
    print(f"TypeError: {e}")
```
```
# Output:
TypeError: adder() takes 3 positional arguments but 5 were given
```

`*args` and `**kwargs` solve this by letting a function accept **any number of arguments**.

---

## 2. `*args` — Collecting Positional Arguments into a Tuple

Place a `*` before a parameter name and Python collects all extra positional arguments into a **tuple** inside the function:

```python
def adder(*nums):
    total = 0
    for n in nums:
        total = total + n
    print(f"Sum: {total}")

adder(3, 6)
adder(3, 5, 6, 7)
adder(1, 2, 3, 6, 9)
```
```
# Output:
Sum: 9
Sum: 21
Sum: 21
```

> **`*nums` is a tuple inside the function** — not a list:

```python
def show_args(*nums):
    print(f"type : {type(nums)}")
    print(f"value: {nums}")

show_args(10, 20, 30)
```
```
# Output:
type : <class 'tuple'>
value: (10, 20, 30)
```

```
adder(3, 5, 6, 7)
       ↓  ↓  ↓  ↓
     nums = (3, 5, 6, 7)   ← tuple inside the function
```

> **The name `args` is a convention, not a rule.** You can use any name: `*nums`, `*amounts`, `*items`. What matters is the `*`.

### B2B eCom — Sum any number of order amounts

```python
def sum_orders(*amounts):
    """Accepts any number of order amounts and returns the total."""
    print(f"Orders  : {amounts}")
    total = sum(amounts)
    print(f"Total   : ₹{total:.2f}")
    return total
```

```python
sum_orders(12500)
```
```
# Output:
Orders  : (12500,)
Total   : ₹12500.00
```

```python
sum_orders(12500, 45000, 8750)
```
```
# Output:
Orders  : (12500, 45000, 8750)
Total   : ₹66250.00
```

```python
sum_orders(12500, 45000, 8750, 62000, 31500)
```
```
# Output:
Orders  : (12500, 45000, 8750, 62000, 31500)
Total   : ₹159750.00
```

---

## 3. `*args` with a Required Argument Before It

You can mix a required positional argument with `*args`. The required argument must come **first**:

```python
def log_vendor_events(vendor, *events):
    """
    Logs any number of events for a vendor.

    Args:
        vendor  (str): Vendor name — required, always the first argument.
        *events      : Any number of event descriptions.
    """
    print(f"Vendor: {vendor}")
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")
```

```python
log_vendor_events('Tata Electronics', 'Listed 5 products')
```
```
# Output:
Vendor: Tata Electronics
  1. Listed 5 products
```

```python
log_vendor_events('Reliance Digital',
                  'Updated prices',
                  'Added 3 items',
                  'Replied to 7 queries')
```
```
# Output:
Vendor: Reliance Digital
  1. Updated prices
  2. Added 3 items
  3. Replied to 7 queries
```

```
log_vendor_events('Reliance', 'Action1', 'Action2', 'Action3')
                      ↓           ↓           ↓          ↓
                   vendor      events = ('Action1', 'Action2', 'Action3')
```

---

## 4. `**kwargs` — Collecting Keyword Arguments into a Dictionary

Place `**` before a parameter name and Python collects all extra **keyword** arguments into a **dictionary** inside the function:

```python
def intro(**data):
    print(f"Data type: {type(data)}")
    for key, value in data.items():
        print(f"  {key}: {value}")
```

```python
intro(Firstname="Sam", Lastname="Altman", Age=24, Phone=1234567890)
```
```
# Output:
Data type: <class 'dict'>
  Firstname: Sam
  Lastname: Altman
  Age: 24
  Phone: 1234567890
```

```python
intro(Firstname="Jane", Lastname="Foster",
      Email="jane@example.com", Country="USA", Age=27)
```
```
# Output:
Data type: <class 'dict'>
  Firstname: Jane
  Lastname: Foster
  Email: jane@example.com
  Country: USA
  Age: 27
```

> **`**data` is a dict inside the function:**

```python
def show_kwargs(**data):
    print(f"type : {type(data)}")
    print(f"value: {data}")

show_kwargs(name="Wireless Mouse", price=499, category="Electronics")
```
```
# Output:
type : <class 'dict'>
value: {'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics'}
```

```
intro(Firstname="Sam", Age=24)
         ↓                ↓
    data = {'Firstname': 'Sam', 'Age': 24}   ← dict inside the function
```

> **The name `kwargs` is a convention.** You can use any name: `**data`, `**specs`, `**options`. What matters is the `**`.

### B2B eCom — Product listing with any number of fields

```python
def create_product_listing(**specs):
    """Creates a product entry from any number of specification fields."""
    print("Product Listing:")
    for key, value in specs.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
```

```python
create_product_listing(name='Wireless Mouse', price=499,
                       category='Electronics', in_stock=True)
```
```
# Output:
Product Listing:
  Name: Wireless Mouse
  Price: 499
  Category: Electronics
  In Stock: True
```

```python
create_product_listing(name='Laptop Stand', price=850,
                       warranty='1 year', weight='0.8kg', colour='Silver')
```
```
# Output:
Product Listing:
  Name: Laptop Stand
  Price: 850
  Warranty: 1 year
  Weight: 0.8kg
  Colour: Silver
```

---

## 5. `**kwargs` — Checking for Specific Keys

Use `in` to check whether a caller passed a particular keyword argument:

```python
def process_order(order_id, **options):
    """
    Processes an order with optional delivery and packaging flags.

    Args:
        order_id  (str): The order ID — required.
        **options      : Optional flags — express, gift_wrap, note.
    """
    print(f"Order: {order_id}")
    if 'express' in options:
        print(f"  Express delivery: {options['express']}")
    if 'gift_wrap' in options:
        print(f"  Gift wrap: {options['gift_wrap']}")
    if 'note' in options:
        print(f"  Note: {options['note']}")
```

```python
process_order('ORD-1001')                                          # no options
```
```
# Output:
Order: ORD-1001
```

```python
process_order('ORD-1002', express=True, gift_wrap=True)
```
```
# Output:
Order: ORD-1002
  Express delivery: True
  Gift wrap: True
```

```python
process_order('ORD-1003', express=True, note='Leave at reception desk')
```
```
# Output:
Order: ORD-1003
  Express delivery: True
  Note: Leave at reception desk
```

---

## 6. Combining `*args` and `**kwargs` in One Function

You can use both together. A required positional argument comes first, then `*args`, then keyword-only arguments (with defaults), then `**kwargs`:

```python
def generate_invoice(vendor, *items, currency='INR', **meta):
    """
    Generates an invoice combining all argument types.

    Args:
        vendor    (str)  : Vendor name — required, positional.
        *items           : Any number of product names.
        currency  (str)  : Currency code — keyword-only, default 'INR'.
        **meta           : Any extra invoice fields (region, gst_no, etc.).
    """
    print(f"Vendor  : {vendor}")
    print(f"Items   : {list(items)}")
    print(f"Currency: {currency}")
    for k, v in meta.items():
        print(f"  {k.replace('_', ' ').title()}: {v}")
```

```python
generate_invoice('Tata Electronics',
                 'Wireless Mouse', 'Keyboard',
                 region='Mumbai',
                 gst_no='27AABC')
```
```
# Output:
Vendor  : Tata Electronics
Items   : ['Wireless Mouse', 'Keyboard']
Currency: INR
  Region: Mumbai
  Gst No: 27AABC
```

```python
generate_invoice('Reliance Digital',
                 'Smart Watch',
                 currency='USD',
                 export=True)
```
```
# Output:
Vendor  : Reliance Digital
Items   : ['Smart Watch']
Currency: USD
  Export: True
```

---

## 7. Correct Parameter Order When Mixing All Types

When a function uses multiple kinds of parameters, they must appear in this order:

```python
def full_example(pos1, pos2, *args, kw_only='default', **kwargs):
    print(f"pos1    : {pos1}")
    print(f"pos2    : {pos2}")
    print(f"args    : {args}")
    print(f"kw_only : {kw_only}")
    print(f"kwargs  : {kwargs}")

full_example(1, 2, 3, 4, 5, kw_only='custom', extra='value', more=True)
```
```
# Output:
pos1    : 1
pos2    : 2
args    : (3, 4, 5)
kw_only : custom
kwargs  : {'extra': 'value', 'more': True}
```

```
┌──────────────────────────────────────────────────────────────────┐
│  Correct order:                                                  │
│                                                                  │
│  def f(positional, *args, keyword_only=default, **kwargs)        │
│           ↑           ↑          ↑                  ↑           │
│       required    extra       optional            extra          │
│       first      positional   keyword             keyword        │
│                  as tuple     after *             as dict        │
└──────────────────────────────────────────────────────────────────┘
```

```
┌────────────────┬───────────────────────────────────────────────┐
│  Type          │  Captures                                     │
├────────────────┼───────────────────────────────────────────────┤
│  param         │  One required positional value                │
│  param=default │  One optional value with a default            │
│  *args         │  All extra positional values → tuple          │
│  kw=default    │  Keyword-only (after *args) → single value    │
│  **kwargs      │  All extra keyword values → dict              │
└────────────────┴───────────────────────────────────────────────┘
```

---

## 8. Unpacking with `*` and `**` When Calling a Function

`*` and `**` work in the other direction too — you can **unpack** a list or dict into function arguments when calling:

### Unpacking a list with `*`

```python
def add_three(a, b, c):
    print(f"{a} + {b} + {c} = {a + b + c}")

numbers = [10, 20, 30]
add_three(*numbers)           # unpacks list into three positional args
```
```
# Output:
10 + 20 + 30 = 60
```

```
add_three(*[10, 20, 30])
  → add_three(10, 20, 30)
```

### Unpacking a dict with `**`

```python
def show_product(name, price, category):
    print(f"{name} — ₹{price} ({category})")

product = {'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics'}
show_product(**product)       # unpacks dict into keyword args
```
```
# Output:
Wireless Mouse — ₹499 (Electronics)
```

```
show_product(**{'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics'})
  → show_product(name='Wireless Mouse', price=499, category='Electronics')
```

### Combining both when calling

```python
def order_line(vendor, product, quantity=1):
    print(f"{vendor}: {product} x{quantity}")

vendors = ['Tata Electronics']
details = {'product': 'Mouse', 'quantity': 3}

order_line(*vendors, **details)
```
```
# Output:
Tata Electronics: Mouse x3
```

```
┌───────────────────────────────────────────────────────────────┐
│  In function DEFINITION:                                      │
│    *args   → collects positional args into a tuple            │
│    **kwargs→ collects keyword args into a dict                │
│                                                               │
│  In function CALL:                                            │
│    *list   → unpacks a list into positional args              │
│    **dict  → unpacks a dict into keyword args                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Exercise: eCOMMart Order Pipeline

Build two functions that use all the argument types covered in this notebook.

### Part 1 — `calculate_cart(*item_totals, apply_discount=True)`

```python
def get_discount_rate(cart_total):
    if cart_total >= 3000: return 0.25
    elif cart_total >= 2000: return 0.15
    elif cart_total >= 1000: return 0.10
    elif cart_total >= 500:  return 0.05
    else: return 0.0


def calculate_cart(*item_totals, apply_discount=True):
    """
    Calculates cart summary from any number of item totals.

    Args:
        *item_totals        : Any number of individual item totals (INR).
        apply_discount (bool): Whether to apply the eCOMMart discount (default True).

    Returns:
        float: Grand total.
    """
    subtotal = sum(item_totals)

    if apply_discount:
        rate  = get_discount_rate(subtotal)
        disc  = round(subtotal * rate, 2)
        grand = round(subtotal - disc, 2)
    else:
        rate, disc, grand = 0.0, 0.0, subtotal

    print(f"Items    : {item_totals}")
    print(f"Subtotal : ₹{subtotal:.2f}")
    if apply_discount and disc > 0:
        print(f"Discount : {int(rate * 100)}% → -₹{disc:.2f}")
    print(f"Grand    : ₹{grand:.2f}")
    return grand
```

```python
calculate_cart(499, 700, 850)
```
```
# Output:
Items    : (499, 700, 850)
Subtotal : ₹2049.00
Discount : 15% → -₹307.35
Grand    : ₹1741.65
```

```python
calculate_cart(2999, 398)
```
```
# Output:
Items    : (2999, 398)
Subtotal : ₹3397.00
Discount : 25% → -₹849.25
Grand    : ₹2547.75
```

```python
calculate_cart(150, 200, apply_discount=False)
```
```
# Output:
Items    : (150, 200)
Subtotal : ₹350.00
Grand    : ₹350.00
```

### Part 2 — `build_order_record(order_id, *products, **details)`

```python
def build_order_record(order_id, *products, **details):
    """
    Builds a complete order record as a dictionary.

    Args:
        order_id   (str): The order ID — required.
        *products       : Any number of product names.
        **details       : Any extra fields (vendor, express, amount, etc.).

    Returns:
        dict: Complete order record.
    """
    return {
        'order_id': order_id,
        'products': list(products),
        **details
    }
```

```python
record = build_order_record('ORD-2001',
                            'Wireless Mouse', 'USB Hub',
                            vendor='Tata Electronics',
                            express=True,
                            amount=1049)

for key, value in record.items():
    print(f"  {key}: {value}")
```
```
# Expected Output:
  order_id: ORD-2001
  products: ['Wireless Mouse', 'USB Hub']
  vendor: Tata Electronics
  express: True
  amount: 1049
```

---

## Summary

```
┌──────────────┬─────────────────────────────────────────────────┐
│  `*args`     │  Collects extra positional args → tuple         │
│  `**kwargs`  │  Collects extra keyword args → dict             │
│  `*list`     │  Unpacks a list into positional args (in call)  │
│  `**dict`    │  Unpacks a dict into keyword args (in call)     │
├──────────────┼─────────────────────────────────────────────────┤
│  These make functions flexible:                                │
│    • Accept any number of inputs                               │
│    • Work with data structures directly                        │
│    • Form the backbone of agent tool interfaces                │
└──────────────┴─────────────────────────────────────────────────┘
```
