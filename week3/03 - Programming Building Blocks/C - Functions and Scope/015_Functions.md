# Functions

## Introduction to Functions

A **function** is a named block of code that groups a set of statements so they can be **run more than once**. Functions also accept **parameters** — inputs that change what the function does.

Functions let you avoid repeating the same code. You have already used built-in functions like `len()`, `print()`, and `input()`. Now you will learn to build your own.

> ### Agent Tool Connection
> In AI agent systems, every tool the agent can call **is a function**. When you build
> a function like `get_product_price(sku)`, you are writing a future agent tool.
> The agent reads the function name and its docstring to decide when and how to call it.

**What we will cover:**

1. `def` — defining a function
2. Functions with parameters
3. `return` — getting a value back
4. Docstrings — the agent tool contract
5. Calling one function from another
6. `return` as an early exit
7. Input validation functions
8. Exercise — Shopping Cart System

---

## 1. `def` — Defining a Function

Functions are defined using the `def` keyword:

```python
def function_name(parameter1, parameter2):
    """
    Docstring — describe what this function does.
    The AI agent reads this to decide when to use this tool.
    """
    # code here
    return result
```

```
def  function_name  (parameters):
 ↑         ↑              ↑
keyword  choose a     inputs the
         clear name   function needs
```

**Key rules:**
- Name your function clearly — `calculate_total` not `calc`
- Indent all code inside the function (4 spaces)
- Write a docstring — triple-quoted string just below `def`
- Use `return` to send a value back to the caller

---

## 2. A Simple Function — No Parameters

```python
def welcome_customer():
    print('Welcome to eCOMMart — Shop Smart, Save More!')

welcome_customer()
```
```
# Output:
Welcome to eCOMMart — Shop Smart, Save More!
```

Call the function as many times as you need — the code inside runs each time:

```python
welcome_customer()
welcome_customer()
welcome_customer()
```
```
# Output:
Welcome to eCOMMart — Shop Smart, Save More!
Welcome to eCOMMart — Shop Smart, Save More!
Welcome to eCOMMart — Shop Smart, Save More!
```

---

## 3. Function with a Parameter

A **parameter** is a variable the function receives when called:

```python
def greet_customer(name):
    print(f'Hello {name}! Your eCOMMart account is active.')

greet_customer('Priya')
greet_customer('Rohan')
```
```
# Output:
Hello Priya! Your eCOMMart account is active.
Hello Rohan! Your eCOMMart account is active.
```

```
greet_customer('Priya')
                  ↑
           argument passed in
           → name = 'Priya' inside the function
```

---

## 4. `return` — Getting a Value Back

`return` sends a value back to the caller. Without `return`, a function returns `None`:

```python
def calculate_item_total(price, quantity):
    return price * quantity

item_total = calculate_item_total(299.99, 3)
print(f"Item Total: ₹{item_total:.2f}")
```
```
# Output:
Item Total: ₹899.97
```

The returned value can be stored in a variable, printed, or passed to another function:

```python
# Store it
total = calculate_item_total(499, 2)

# Print it directly
print(calculate_item_total(850, 1))

# Pass it straight into another function
print(f"Total: ₹{calculate_item_total(1299, 3):.2f}")
```
```
# Output:
850
Total: ₹3897.00
```

> **Python doesn't restrict types.** The same function works on any type that supports `*`:

```python
print(calculate_item_total('eCOMMart ', 3))
```
```
# Output:
eCOMMart eCOMMart eCOMMart
```

This is a reminder to validate input types in real tools — see `is_nan()` in `017`.

---

## 5. Docstrings — The Agent Tool Contract

A **docstring** is a triple-quoted string placed immediately after `def`. It describes what the function does, what it accepts, and what it returns. This is not optional — it is how an AI agent understands when to call the function.

```python
def get_discount_rate(cart_total):
    """
    Returns the discount rate for a given cart total.

    eCOMMart Discount Policy:
        ≥ ₹3000 → 25%
        ≥ ₹2000 → 15%
        ≥ ₹1000 → 10%
        ≥ ₹500  →  5%
        < ₹500  →  0%

    Agent Tool Use:
        Call this when a customer asks 'What discount do I get?'
        or when the checkout module needs the discount before billing.

    Args:
        cart_total (float): Total cart value in INR.

    Returns:
        float: Discount rate as a decimal (e.g., 0.15 for 15%).
    """
    if cart_total >= 3000:
        return 0.25
    elif cart_total >= 2000:
        return 0.15
    elif cart_total >= 1000:
        return 0.10
    elif cart_total >= 500:
        return 0.05
    else:
        return 0.0
```

```python
# Test all discount tiers
for cart in [3500, 2500, 1500, 700, 300]:
    rate = get_discount_rate(cart)
    print(f"  ₹{cart} → {int(rate * 100)}% discount")
```
```
# Output:
  ₹3500 → 25% discount
  ₹2500 → 15% discount
  ₹1500 → 10% discount
  ₹700  →  5% discount
  ₹300  →  0% discount
```

---

## 6. Calling One Function from Another

Functions can call other functions. This is how you build complex behaviour from simple, testable pieces:

```python
def print_receipt(items):
    """
    Prints a formatted eCOMMart receipt for a list of items.

    Args:
        items (list of dict): Each dict has 'name', 'price', 'qty'.

    Returns:
        float: Grand total after discount.
    """
    print("=" * 40)
    print("       eCOMMart — Order Receipt")
    print("=" * 40)

    grand_total = 0
    for item in items:
        line_total = item['price'] * item['qty']
        grand_total += line_total
        print(f"  {item['name']:<20} ₹{item['price']:>6.2f} x {item['qty']} = ₹{line_total:.2f}")

    discount_rate = get_discount_rate(grand_total)   # calls another function
    discount_amt  = round(grand_total * discount_rate, 2)
    final_total   = round(grand_total - discount_amt, 2)

    print("-" * 40)
    print(f"  {'Subtotal':<20} ₹{grand_total:>8.2f}")
    print(f"  {'Discount (' + str(int(discount_rate*100)) + '%)':<20} -₹{discount_amt:>7.2f}")
    print(f"  {'Grand Total':<20} ₹{final_total:>8.2f}")
    print("=" * 40)

    return final_total
```

```python
cart_items = [
    {'name': 'Wireless Mouse', 'price': 499.00, 'qty': 1},
    {'name': 'USB Hub',        'price': 350.00, 'qty': 2},
    {'name': 'Laptop Stand',   'price': 850.00, 'qty': 1},
]

total_paid = print_receipt(cart_items)
print(f"\nAmount collected: ₹{total_paid:.2f}")
```
```
# Output:
========================================
       eCOMMart — Order Receipt
========================================
  Wireless Mouse       ₹499.00 x 1 = ₹499.00
  USB Hub              ₹350.00 x 2 = ₹700.00
  Laptop Stand         ₹850.00 x 1 = ₹850.00
----------------------------------------
  Subtotal             ₹ 2049.00
  Discount (15%)       -₹  307.35
  Grand Total          ₹ 1741.65
========================================

Amount collected: ₹1741.65
```

```
print_receipt(cart_items)
    └── calls get_discount_rate(2049)
              └── returns 0.15
    └── calculates discount and final total
    └── returns 1741.65
```

---

## 7. `return` as an Early Exit

`return` stops a function immediately — code after it does not run. Use this to exit as soon as you have your answer:

```python
def find_out_of_stock(inventory):
    """
    Scans inventory and returns the first out-of-stock item name.

    Args:
        inventory (list of dict): Each dict has 'product' and 'stock'.

    Returns:
        str: Name of first out-of-stock product, or 'All items are in stock.'
    """
    for item in inventory:
        if item['stock'] == 0:
            return f"Out of stock: {item['product']}"  # exits immediately
    return 'All items are in stock.'
```

```python
stock_list = [
    {'product': 'Smart Watch', 'stock': 12},
    {'product': 'Earbuds',     'stock': 0},
    {'product': 'Phone Case',  'stock': 8},
]

print(find_out_of_stock(stock_list))
```
```
# Output:
Out of stock: Earbuds
```

```python
all_good = [
    {'product': 'Smart Watch', 'stock': 12},
    {'product': 'Earbuds',     'stock': 5},
]

print(find_out_of_stock(all_good))
```
```
# Output:
All items are in stock.
```

```
Loop reaches Earbuds (stock=0)
    → return "Out of stock: Earbuds"   ← exits here
    → Phone Case is never checked
```

---

## 8. Input Validation Functions

A validation function checks whether an input is safe to use. It always returns a Boolean — `True` if valid, `False` otherwise. This is a foundational pattern for agent tools:

```python
def is_valid_sku(sku):
    """
    Validates an eCOMMart product SKU code.

    Rules:
        - Must be a non-empty string
        - Must start with a letter
        - Must be between 4 and 10 characters long

    Agent Tool Use:
        Call before adding a product to the catalogue
        or looking it up in the database.

    Args:
        sku (str): The product SKU to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(sku, str) or len(sku) == 0:
        return False
    if not sku[0].isalpha():
        return False
    if not (4 <= len(sku) <= 10):
        return False
    return True
```

```python
sku_tests = ['WM4021', '123AB', 'AB', 'LAPTOP-STAND-PREMIUM', 'USB1']

for sku in sku_tests:
    status = '✅ Valid' if is_valid_sku(sku) else '❌ Invalid'
    print(f"  SKU: {sku:<25} → {status}")
```
```
# Output:
  SKU: WM4021                    → ✅ Valid
  SKU: 123AB                     → ❌ Invalid
  SKU: AB                        → ❌ Invalid
  SKU: LAPTOP-STAND-PREMIUM      → ❌ Invalid
  SKU: USB1                      → ✅ Valid
```

```
WM4021              → starts with letter ✓, length 6 ✓  → Valid
123AB               → starts with number ✗              → Invalid
AB                  → length 2 < 4 ✗                   → Invalid
LAPTOP-STAND-PREMIUM→ length 20 > 10 ✗                 → Invalid
USB1                → starts with letter ✓, length 4 ✓  → Valid
```

---

## Exercise: eCOMMart Shopping Cart System

Build the cart module for eCOMMart using three functions that work together.

**Define these three functions:**
- `add_item(cart, item_name, price, quantity)` — appends an item dict to the cart list
- `calculate_total(cart)` — returns the sum of all `price × quantity`
- `display_receipt(cart)` — prints the full bill with subtotal, discount, and grand total

Then collect items from the user in a `while True` loop until they type `done`.

```python
# Solution

def add_item(cart, item_name, price, quantity):
    """Adds one item to the cart list."""
    cart.append({'name': item_name, 'price': price, 'qty': quantity})


def calculate_total(cart):
    """Returns the sum of price × quantity for all items in the cart."""
    return sum(i['price'] * i['qty'] for i in cart)


def display_receipt(cart):
    """Prints a full receipt with discount applied. Returns grand total."""
    subtotal  = calculate_total(cart)
    disc_rate = get_discount_rate(subtotal)
    discount  = round(subtotal * disc_rate, 2)
    grand     = round(subtotal - discount, 2)

    print("=" * 44)
    print("         eCOMMart — Your Receipt")
    print("=" * 44)
    for i in cart:
        line = i['price'] * i['qty']
        print(f"  {i['name']:<20} ₹{i['price']:>7.2f} x {i['qty']} = ₹{line:.2f}")
    print("-" * 44)
    print(f"  {'Subtotal':<30} ₹{subtotal:.2f}")
    print(f"  {'Discount (' + str(int(disc_rate*100)) + '%)':<30}-₹{discount:.2f}")
    print(f"  {'Grand Total':<30} ₹{grand:.2f}")
    print("=" * 44)
    return grand


# Collect items from the user
cart = []

while True:
    name = input("\nEnter item name (or 'done' to finish): ")
    if name.lower() == 'done':
        break
    price = float(input(f"Enter price of {name} (₹): "))
    qty   = int(input("Enter quantity: "))
    add_item(cart, name, price, qty)

display_receipt(cart)
```
```
# Expected Output (with inputs: Smart Watch / 2999 / 1, Phone Case / 199 / 2, done):

Enter item name (or 'done' to finish): Smart Watch
Enter price of Smart Watch (₹): 2999
Enter quantity: 1

Enter item name (or 'done' to finish): Phone Case
Enter price of Phone Case (₹): 199
Enter quantity: 2

Enter item name (or 'done' to finish): done

============================================
         eCOMMart — Your Receipt
============================================
  Smart Watch          ₹2999.00 x 1 = ₹2999.00
  Phone Case           ₹ 199.00 x 2 = ₹ 398.00
--------------------------------------------
  Subtotal                       ₹3397.00
  Discount (25%)                -₹ 849.25
  Grand Total                    ₹2547.75
============================================
```

```
Verification:
  Smart Watch: ₹2999 × 1 = ₹2999
  Phone Case:  ₹199  × 2 = ₹398
  Subtotal              = ₹3397  → qualifies for 25% discount
  Discount: ₹3397 × 0.25 = ₹849.25
  Grand: 3397 − 849.25   = ₹2547.75
```
