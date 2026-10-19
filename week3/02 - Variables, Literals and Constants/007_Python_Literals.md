# Python Literals

A **literal** is a raw, fixed value written directly in your code — as opposed to a variable whose value can change. When you write `price = 499`, the `499` is a literal.

**What we will cover:**

1. Numeric literals — int, float, complex, binary, octal, hex
2. String literals — single, double, and triple quotes
3. Escape characters and raw strings
4. f-Strings — formatted string literals
5. Boolean literals
6. `None` — the special literal
7. Literal collections
8. Tasks

---

## 1. Numeric Literals

Python supports three numeric types, each with several literal forms:

```
┌─────────────────────────────────────────────────────────────────┐
│  Type     │  Example               │  Notes                     │
├─────────────────────────────────────────────────────────────────┤
│  Integer  │  100, 0b1010, 0o310    │  Decimal, binary, octal    │
│  Float    │  299.99, 1.8e-1        │  Decimal, scientific       │
│  Complex  │  3.14j                 │  Imaginary component       │
└─────────────────────────────────────────────────────────────────┘
```

```python
# eCOMMart Numeric Literals Example

product_id    = 0b1010   # Binary literal  → printed as decimal
item_count    = 100      # Decimal literal
category_code = 0o310    # Octal literal   → printed as decimal
hex_sku       = 0x12c    # Hex literal     → printed as decimal

quantity    = 5
reorder_qty = 50

unit_price = 299.99      # Float literal
tax_rate   = 1.8e-1      # Scientific notation: 1.8 × 10⁻¹ = 0.18

signal = 3.14j           # Complex literal (imaginary part only)

print(f"product_id    = 0b1010  → {product_id}")
print(f"item_count    = 100     → {item_count}")
print(f"category_code = 0o310   → {category_code}")
print(f"hex_sku       = 0x12c   → {hex_sku}")
print(f"quantity    = {quantity}")
print(f"reorder_qty = {reorder_qty}")
print(f"unit_price  = {unit_price}")
print(f"tax_rate    = 1.8e-1 → {tax_rate}")
print(f"signal      = {signal}  → imag={signal.imag}, real={signal.real}")
```
```
# Output:
product_id    = 0b1010  → 10
item_count    = 100     → 100
category_code = 0o310   → 200
hex_sku       = 0x12c   → 300
quantity    = 5
reorder_qty = 50
unit_price  = 299.99
tax_rate    = 1.8e-1 → 0.18
signal      = 3.14j  → imag=3.14, real=0.0
```

```
┌─────────────────────────────────────────────────────────┐
│  Binary  0b1010  →  0×2⁴ + 1×2³ + 0×2² + 1×2¹ + 0 = 10│
│  Octal   0o310   →  3×64 + 1×8 + 0 = 200               │
│  Hex     0x12c   →  1×256 + 2×16 + 12 = 300            │
│  All print as decimal — Python converts automatically   │
└─────────────────────────────────────────────────────────┘
```

---

## 2. String Literals — Single, Double, and Triple Quotes

A **string** literal is a sequence of characters surrounded by quotes. Python supports three kinds:

```
┌───────────────┬────────────────────┬──────────────────────────────┐
│  Quote type   │  Syntax            │  Typical use                 │
├───────────────┼────────────────────┼──────────────────────────────┤
│  Single quote │  'text'            │  Short clean values          │
│  Double quote │  "text"            │  Strings with apostrophes    │
│  Triple quote │  """text"""        │  Multi-line, docstrings      │
└───────────────┴────────────────────┴──────────────────────────────┘
```

### 2.1 Single Quote Strings `' '`

```python
product_name = 'Wireless Mouse'
category     = 'Electronics'
seller_city  = 'Mumbai'
order_status = 'Shipped'

print(product_name)
print(category)
print(seller_city)
print(order_status)
```
```
# Output:
Wireless Mouse
Electronics
Mumbai
Shipped
```

> **Watch out:** If the string contains an apostrophe, single quotes will cause a `SyntaxError`:
> ```python
> # WRONG — apostrophe breaks the string
> item = 'Men's Jacket'
>
> # CORRECT — use double quotes instead
> item = "Men's Jacket"
> ```

---

### 2.2 Double Quote Strings `" "`

Use double quotes whenever the string contains an apostrophe:

```python
brand_tagline = "India's Fastest Delivery"
product_note  = "Don't forget to apply your coupon!"
item_label    = "Men's Running Shoes"
error_msg     = "Item not found in catalog."

print(brand_tagline)
print(product_note)
print(item_label)
print(error_msg)
```
```
# Output:
India's Fastest Delivery
Don't forget to apply your coupon!
Men's Running Shoes
Item not found in catalog.
```

**Single and double are interchangeable for simple strings:**

```python
name1 = 'eCOMMart'
name2 = "eCOMMart"
print(name1 == name2)
```
```
# Output:
True
```

---

### 2.3 Triple Quote Strings `""" """` or `''' '''`

Triple quotes let a string span multiple lines. They preserve line breaks and indentation exactly as written. Common uses:

- Product descriptions
- Order confirmation templates
- Email/SMS messages printed to the console
- Function docstrings

```python
product_description = """
Product  : Wireless Bluetooth Headphones
Brand    : SoundMax
Price    : ₹1,499
Offer    : 20% off on orders above ₹999
In Stock : Yes
"""
print(product_description)
```
```
# Output:

Product  : Wireless Bluetooth Headphones
Brand    : SoundMax
Price    : ₹1,499
Offer    : 20% off on orders above ₹999
In Stock : Yes

```

```python
order_confirmation = '''
Thank you for shopping at eCOMMart!

Order ID   : ORD-20241
Item       : Laptop Stand
Quantity   : 1
Amount Paid: ₹850
Status     : Payment Confirmed

Your order will be delivered within 2-3 business days.
'''
print(order_confirmation)
```
```
# Output:

Thank you for shopping at eCOMMart!

Order ID   : ORD-20241
Item       : Laptop Stand
Quantity   : 1
Amount Paid: ₹850
Status     : Payment Confirmed

Your order will be delivered within 2-3 business days.

```

**Triple quotes as function docstrings — the agent tool contract:**

```python
def get_product_info(product_name):
    """
    Retrieves product information from the eCOMMart catalog.

    Args:
        product_name (str): Name of the product to look up.

    Returns:
        str: Product details as a formatted string.

    Agent Tool Note:
        This function is designed to be called by an AI agent
        to answer customer queries like 'Tell me about Wireless Mouse.'
    """
    catalog = {
        'Wireless Mouse': 'Brand: TechPro | Price: ₹499 | In Stock: Yes',
        'Laptop Stand'  : 'Brand: ErgoDesk | Price: ₹850 | In Stock: Yes',
    }
    return catalog.get(product_name, 'Product not found in catalog.')

print(get_product_info('Wireless Mouse'))
print(get_product_info('Unknown Item'))
```
```
# Output:
Brand: TechPro | Price: ₹499 | In Stock: Yes
Product not found in catalog.
```

---

## 3. Escape Characters and Raw Strings

Some characters cannot be typed directly in a string. Use **escape sequences** — a backslash `\` followed by a special character:

```
┌────────┬────────────────────────────────────────┐
│  `\t`  │  Tab (horizontal space)                │
│  `\n`  │  New line                              │
│  `\\`  │  Single backslash                      │
│  `\'`  │  Single quote inside single-quote str  │
│  `\"`  │  Double quote inside double-quote str  │
└────────┴────────────────────────────────────────┘
```

```python
receipt_line = "Item\tPrice\tQty"          # \t = tab
address_line = "123, MG Road\nBangalore"   # \n = new line
path_windows = "C:\\eCOMMart\\data"        # \\ = single backslash

print(receipt_line)
print(address_line)
print(path_windows)
```
```
# Output:
Item	Price	Qty
123, MG Road
Bangalore
C:\eCOMMart\data
```

**Raw strings** — prefix `r` tells Python to treat every backslash literally:

```python
file_path = r"C:\eCOMMart\uploads\images"
print(file_path)
```
```
# Output:
C:\eCOMMart\uploads\images
```

---

## 4. f-Strings — Formatted String Literals

An **f-string** lets you embed variables and expressions directly inside a string by prefixing it with `f` and wrapping the values in `{}`:

```python
product    = "Smart Watch"
price      = 2999
discount   = 10

final_price = price - (price * discount / 100)

print(f"Product : {product}")
print(f"MRP     : ₹{price}")
print(f"Discount: {discount}%")
print(f"You Pay : ₹{final_price:.2f}")
```
```
# Output:
Product : Smart Watch
MRP     : ₹2999
Discount: 10%
You Pay : ₹2699.10
```

```
f"You Pay : ₹{final_price:.2f}"
               ↑           ↑
           variable    format spec
                       .2f = 2 decimal places as float
```

---

## 5. Boolean Literals

A Boolean literal is either `True` or `False` (capital first letter — always):

```python
is_in_stock    = True
is_on_sale     = False
is_cod_allowed = True
```

> **Key fact:** `True == 1` and `False == 0` in Python. Booleans are a subclass of integers, so you can use them in arithmetic:

```python
items_available = is_in_stock + 4   # True(1) + 4 = 5
sale_bonus      = is_on_sale + 100  # False(0) + 100 = 100

print("In Stock:", is_in_stock)
print("On Sale :", is_on_sale)
print(f"Effective stock count : {items_available}")
print(f"Sale bonus applied    : ₹{sale_bonus}")
```
```
# Output:
In Stock: True
On Sale : False
Effective stock count : 5
Sale bonus applied    : ₹100
```

---

## 6. `None` — The Special Literal

`None` represents the **absence of a value**. Use it when a field exists but has not been filled yet:

```python
customer_name = "Rahul Sharma"
delivery_note = None          # no special instructions given
promo_code    = None          # no coupon applied

def show_order_note(note):
    if note is None:
        print("No delivery instructions provided.")
    else:
        print("Delivery note:", note)

show_order_note(delivery_note)
show_order_note("Please leave at the door.")
```
```
# Output:
No delivery instructions provided.
Delivery note: Please leave at the door.
```

```
None is not the same as:
  ""      (empty string — a string that exists but has no characters)
  0       (the number zero — a value)
  False   (a boolean — a value)

None means: this variable exists but has no value yet
```

---

## 7. Literal Collections

Python has four built-in collection types, each with its own literal syntax:

```python
cart_items      = ["Wireless Mouse", "Laptop Stand", "USB Hub"]       # list []
size_options    = ("S", "M", "L", "XL")                               # tuple ()
product_tags    = {"Electronics", "Gadgets", "Best Seller"}            # set {}
product_details = {"name": "Wireless Mouse", "price": 499, "qty": 2}  # dict {}

print(cart_items)
print(size_options)
print(product_tags)
print(product_details)
```
```
# Output:
['Wireless Mouse', 'Laptop Stand', 'USB Hub']
('S', 'M', 'L', 'XL')
{'Electronics', 'Gadgets', 'Best Seller'}
{'name': 'Wireless Mouse', 'price': 499, 'qty': 2}
```

```
┌──────────┬──────────┬───────────┬────────────────────────────────┐
│  Type    │  Syntax  │ Ordered?  │  Key property                  │
├──────────┼──────────┼───────────┼────────────────────────────────┤
│  List    │  [...]   │ Yes       │  Mutable, allows duplicates    │
│  Tuple   │  (...)   │ Yes       │  Immutable, allows duplicates  │
│  Set     │  {...}   │ No        │  Unique values only            │
│  Dict    │  {k:v}   │ Yes(3.7+) │  Key-value pairs               │
└──────────┴──────────┴───────────┴────────────────────────────────┘
```

> **Note:** Sets are unordered — `product_tags` may print in a different order each run. Covered in detail in `014_Sets.md`.

---

## Tasks

### Task 1: eCOMMart Product Label

Write a Python program that stores product details using all **three string quote types** and prints a formatted label.

**Instructions:**
- Use a **single-quote string** for the product SKU
- Use a **double-quote string** for the brand tagline (which contains an apostrophe)
- Use a **triple-quote string** for the full product description (multi-line)
- Print all three with appropriate labels

```python
# Solution

sku         = 'WM-4021'
tagline     = "India's No.1 Tech Store"
description = """
  Wireless Mouse — Ergonomic design, 12-month battery life.
  Compatible with Windows and Mac.
  Price: ₹499
"""

print(f"SKU      : {sku}")
print(f"Tagline  : {tagline}")
print(f"Description:{description}")
```
```
# Expected Output:
SKU      : WM-4021
Tagline  : India's No.1 Tech Store
Description:
  Wireless Mouse — Ergonomic design, 12-month battery life.
  Compatible with Windows and Mac.
  Price: ₹499

```

---

### Task 2: Price Calculator with Numeric Literals

Write a program that uses **integer** and **float** literals to calculate the final price of 5 items in an eCOMMart cart.

**Instructions:**
- Define prices for 5 items using float literals
- Calculate the subtotal
- Apply 18% GST
- Apply a flat ₹50 discount if the subtotal exceeds ₹500
- Print a formatted bill

```python
# Solution

item1 = 299.99
item2 = 199.00
item3 = 849.00
item4 = 499.00
item5 = 150.00

subtotal = item1 + item2 + item3 + item4 + item5
gst      = subtotal * 0.18
discount = 50.00 if subtotal > 500 else 0.00
total    = subtotal + gst - discount

print(f"Subtotal : ₹{subtotal:.2f}")
print(f"GST (18%): ₹{gst:.2f}")
print(f"Discount : ₹{discount:.2f}")
print(f"Total    : ₹{total:.2f}")
```
```
# Expected Output:
Subtotal : ₹1996.99
GST (18%): ₹359.46
Discount : ₹50.00
Total    : ₹2306.45
```

---

### Task 3: Order Confirmation with f-String and Triple Quotes

Write a program that stores a customer name, order ID, and item list, then prints a **multi-line order confirmation message** using an f-string inside triple quotes.

```python
# Solution

customer_name = "Priya Sharma"
order_id      = "ORD-20241"
items         = ["Wireless Mouse", "Laptop Stand"]

confirmation = f"""
===========================================
     eCOMMart — Order Confirmation
===========================================
Customer : {customer_name}
Order ID : {order_id}
Items    : {', '.join(items)}
Status   : Payment Confirmed

Thank you for shopping at eCOMMart!
Your order will be delivered in 2-3 days.
===========================================
"""
print(confirmation)
```
```
# Expected Output:

===========================================
     eCOMMart — Order Confirmation
===========================================
Customer : Priya Sharma
Order ID : ORD-20241
Items    : Wireless Mouse, Laptop Stand
Status   : Payment Confirmed

Thank you for shopping at eCOMMart!
Your order will be delivered in 2-3 days.
===========================================

```
