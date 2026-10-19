# While Loops and User Input

A `while` loop keeps running as long as a condition is `True`. Unlike a `for` loop — which iterates over a known sequence — a `while` loop is used when you don't know in advance how many times you need to repeat something. This makes it perfect for programs that run until the user decides to stop.

**What we will cover:**

1. Basic `while` loop — condition-controlled
2. `while True` with `break` — the sentinel pattern
3. Accepting user input with `input()`
4. `while` + `input()` — keeping programs running
5. Using `while` loops to build menus
6. Processing a list with `while` + `pop()`
7. Accidental infinite loops — how to spot and fix them
8. Tasks

---

## 1. Basic `while` Loop — Condition-Controlled

A `while` loop checks a condition **before every iteration**. As soon as the condition becomes `False`, the loop stops:

```python
# Set an initial condition
game_active = True

while game_active:
    # code runs here as long as game_active is True
    # something inside the loop must eventually set game_active = False
    pass
```

```
                 ┌─────────────────────┐
                 │  Check condition    │
                 └────────┬────────────┘
                          │
              ┌───────────┴───────────┐
          True│                       │False
              ▼                       ▼
       ┌─────────────┐        ┌──────────────┐
       │  Run loop   │        │  Exit loop   │
       │  body       │        │  Continue    │
       └──────┬──────┘        │  program     │
              │               └──────────────┘
              └──────────────────────┘
              (go back and check condition again)
```

**B2B eCom example — countdown stock alert:**

```python
stock_count = 5

while stock_count > 0:
    print(f"Items remaining in stock: {stock_count}")
    stock_count -= 1

print("Out of stock!")
```
```
# Output:
Items remaining in stock: 5
Items remaining in stock: 4
Items remaining in stock: 3
Items remaining in stock: 2
Items remaining in stock: 1
Out of stock!
```

> **Three things every `while` loop needs:**
> 1. An **initial value** for the condition variable (set before the loop)
> 2. A **condition** to test
> 3. Something **inside the loop** that eventually makes the condition `False`
>
> Miss number 3 and you get an infinite loop.

---

## 2. `while True` with `break` — The Sentinel Pattern

The cleanest way to run a loop until a user types a quit word is `while True` combined with `break`. The loop runs forever until you explicitly break out of it:

```python
while True:
    # code runs here
    # when the exit condition is met:
    break   # exits the loop immediately
```

**B2B eCom example — order entry session:**

```python
orders_entered = []

while True:
    entry = input("Enter order ID (or 'done' to finish): ")

    if entry == 'done':
        print("Session ended.")
        break

    orders_entered.append(entry)
    print(f"Order {entry} recorded.")

print(f"Orders this session: {orders_entered}")
```
```
# Expected Output (with inputs ORD-1001, ORD-1002, done):
Enter order ID (or 'done' to finish): ORD-1001
Order ORD-1001 recorded.
Enter order ID (or 'done' to finish): ORD-1002
Order ORD-1002 recorded.
Enter order ID (or 'done' to finish): done
Session ended.
Orders this session: ['ORD-1001', 'ORD-1002']
```

```
┌──────────────────────────────────────────────────────┐
│  while True:       ← starts unconditionally          │
│      entry = input(...)                              │
│      if entry == 'done':                             │
│          break     ← the only exit from the loop     │
│      # otherwise keep looping                        │
└──────────────────────────────────────────────────────┘
```

---

## 3. Accepting User Input with `input()`

`input()` displays a message to the user, waits for them to type something, and returns what they typed as a **string**:

```python
variable = input('Please enter a value: ')
```

> **Important:** `input()` always returns a string. If you need a number, convert it with `int()` or `float()`.

```python
# String input — use directly
vendor_name = input("Enter vendor name: ")
print(f"New vendor added: {vendor_name}")
```
```
# Expected Output (with input 'Tata Electronics'):
Enter vendor name: Tata Electronics
New vendor added: Tata Electronics
```

```python
# Numeric input — must convert
price = float(input("Enter product price (₹): "))
gst   = price * 0.18
print(f"GST (18%): ₹{gst:.2f}")
```
```
# Expected Output (with input 499):
Enter product price (₹): 499
GST (18%): ₹89.82
```

---

## 4. `while` + `input()` — Keeping Programs Running

Combine `while` and `input()` to let users enter as much data as they want before stopping.

### Version 1 — Simple sentinel (has a bug)

```python
sales = []
new_item = ''

while new_item != 'done':
    new_item = input("Enter item name (or 'done' to stop): ")
    sales.append(new_item)   # bug: also appends 'done'

print(sales)
```
```
# Expected Output (with inputs 'Wireless Mouse', 'USB Hub', 'done'):
['Wireless Mouse', 'USB Hub', 'done']
```

The word `'done'` ends up in the list. Fix it with an `if` check:

### Version 2 — Fixed with `if` guard

```python
sales = []
new_item = ''

while new_item != 'done':
    new_item = input("Enter item name (or 'done' to stop): ")
    if new_item != 'done':
        sales.append(new_item)

print(sales)
```
```
# Expected Output (with inputs 'Wireless Mouse', 'USB Hub', 'done'):
['Wireless Mouse', 'USB Hub']
```

### Version 3 — Cleanest: `while True` with `break`

```python
sales = []

while True:
    new_item = input("Enter item name (or 'done' to stop): ")
    if new_item == 'done':
        break
    sales.append(new_item)

print(sales)
```
```
# Expected Output (with inputs 'Wireless Mouse', 'USB Hub', 'done'):
['Wireless Mouse', 'USB Hub']
```

```
┌─────────────────────────────────────────────────────┐
│  Version 1  │  Simple but buggy — 'done' in list   │
│  Version 2  │  Works — two checks on same value     │
│  Version 3  │  Cleanest — one check, one exit point │
└─────────────────────────────────────────────────────┘
```

---

## 5. Using `while` Loops to Build Menus

A `while` loop is the standard way to build a menu that runs until the user quits. Define your action functions first, then build the menu loop:

```python
# Define actions first
def check_order_status():
    print("  → Fetching order status from database...")

def view_inventory():
    print("  → Loading current inventory levels...")

def process_return():
    print("  → Opening return request form...")
```

```python
# Menu loop
choice = ''

while choice != 'q':
    print("\n===== eCOMMart Operations Menu =====")
    print("[1] Check order status")
    print("[2] View inventory")
    print("[3] Process a return")
    print("[q] Quit")

    choice = input("\nEnter your choice: ")

    if choice == '1':
        check_order_status()
    elif choice == '2':
        view_inventory()
    elif choice == '3':
        process_return()
    elif choice == 'q':
        print("Goodbye!")
    else:
        print("Invalid choice — please enter 1, 2, 3, or q.")
```
```
# Expected Output (with choices 1, 2, 3, q):

===== eCOMMart Operations Menu =====
[1] Check order status
[2] View inventory
[3] Process a return
[q] Quit
Enter your choice: 1
  → Fetching order status from database...

===== eCOMMart Operations Menu =====
...
Enter your choice: q
Goodbye!
```

> **Pattern:** Define functions before the loop. The loop only decides **which** function to call — the functions contain the actual logic. This keeps the menu clean and the code easy to extend.

---

## 6. Processing a List with `while` + `pop()`

Use a `while` loop to drain a list one item at a time using `pop()`. This is a common pattern for processing a queue of items:

### LIFO — Last In, First Out (`pop()`)

`pop()` with no argument removes from the **end** of the list — the most recently added item is processed first:

```python
pending_orders = ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004']
processed = []

while len(pending_orders) > 0:
    order = pending_orders.pop()   # removes from the end
    print(f"Processing {order}...")
    processed.append(order)

print(f"\nPending  : {pending_orders}")
print(f"Processed: {processed}")
```
```
# Output:
Processing ORD-1004...
Processing ORD-1003...
Processing ORD-1002...
Processing ORD-1001...

Pending  : []
Processed: ['ORD-1004', 'ORD-1003', 'ORD-1002', 'ORD-1001']
```

### FIFO — First In, First Out (`pop(0)`)

`pop(0)` removes from the **front** — the oldest item is processed first. This is the fairer model for customers:

```python
pending_orders = ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004']
processed = []

while len(pending_orders) > 0:
    order = pending_orders.pop(0)   # removes from the front
    print(f"Processing {order}...")
    processed.append(order)

print(f"\nPending  : {pending_orders}")
print(f"Processed: {processed}")
```
```
# Output:
Processing ORD-1001...
Processing ORD-1002...
Processing ORD-1003...
Processing ORD-1004...

Pending  : []
Processed: ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004']
```

```
Original list:  [ORD-1001, ORD-1002, ORD-1003, ORD-1004]
                    ↑                               ↑
               pop(0)                            pop()
               FIFO                              LIFO
             (first in,                       (last in,
             first out)                       first out)
```

---

## 7. Accidental Infinite Loops

An infinite loop runs forever because the condition never becomes `False`. Every beginner creates at least one. Here is how to recognise and fix them:

### Cause 1 — Forgetting to update the variable

```python
# BROKEN — current_number never changes
current_number = 1

while current_number <= 5:
    print(current_number)
    # missing: current_number += 1
```
```
# Output (would run forever — never printed, must Ctrl+C to stop):
1
1
1
1
...
```

```python
# FIXED — increment inside the loop
current_number = 1

while current_number <= 5:
    print(current_number)
    current_number += 1
```
```
# Output:
1
2
3
4
5
```

### Cause 2 — Updating in the wrong direction

```python
# BROKEN — counting down when condition checks for <= 5
current_number = 1

while current_number <= 5:
    print(current_number)
    current_number -= 1    # goes 1, 0, -1, -2 ... always <= 5!
```
```
# Output (would run forever):
1
0
-1
-2
...
```

```
Condition: current_number <= 5
After -= 1: 1 → 0 → -1 → -2 → ... always True → never stops
```

> **How to stop an infinite loop in VS Code:**
> Press `Ctrl + C` in the terminal. This sends a keyboard interrupt and stops the running program.

> **How to spot one before running:**
> Ask yourself — *"Is there any way the condition can ever become False?"* If the loop body doesn't change the variables in the condition, the answer is no.

---

## Tasks

### Task 1: eCOMMart — Vendor Registration Loop

Build a loop that lets a user register vendors one at a time until they type `done`.

**Instructions:**
- Use `while True` with `break`
- After the loop, display all registered vendors with numbering

```python
vendors = []

while True:
    name = input("Enter vendor name (or 'done' to finish): ")
    if name.lower() == 'done':
        break
    vendors.append(name)
    print(f"Vendor '{name}' registered.")

print(f"\nRegistered Vendors ({len(vendors)}):")
for i, vendor in enumerate(vendors, 1):
    print(f"  {i}. {vendor}")
```
```
# Expected Output (with inputs 'Tata Electronics', 'Reliance Digital', 'done'):
Enter vendor name (or 'done' to finish): Tata Electronics
Vendor 'Tata Electronics' registered.
Enter vendor name (or 'done' to finish): Reliance Digital
Vendor 'Reliance Digital' registered.
Enter vendor name (or 'done' to finish): done

Registered Vendors (2):
  1. Tata Electronics
  2. Reliance Digital
```

---

### Task 2: eCOMMart — Order Queue Processor (FIFO)

Process a list of pending orders in the order they were received (first in, first out).

**Instructions:**
- Start with a predefined list of order IDs
- Use `while` + `pop(0)` to process each order
- Move processed orders to a `completed` list
- Print a summary at the end

```python
pending_orders = ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004']
completed = []

print(f"Pending orders: {pending_orders}\n")

while len(pending_orders) > 0:
    order = pending_orders.pop(0)
    print(f"Processing {order}... done.")
    completed.append(order)

print(f"\nAll orders processed.")
print(f"Completed: {completed}")
```
```
# Expected Output:
Pending orders: ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004']

Processing ORD-1001... done.
Processing ORD-1002... done.
Processing ORD-1003... done.
Processing ORD-1004... done.

All orders processed.
Completed: ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004']
```

---

### Task 3: eCOMMart — Stock Level Monitor

Check a stock dictionary using a `while` loop and flag items that need restocking.

**Instructions:**
- Use a dictionary of product names and quantities
- Iterate using a `while` loop and an index counter
- Flag items with quantity `0` as OUT OF STOCK
- Flag items with quantity `<= 2` as LOW
- Collect all flagged items and print a restock summary

```python
stock = {
    'Wireless Mouse': 3,
    'USB Hub':        0,
    'Earbuds':        5,
    'Laptop Stand':   0,
}

items = list(stock.items())
low_stock = []
i = 0

while i < len(items):
    name, qty = items[i]
    if qty == 0:
        print(f"  ALERT: {name} is OUT OF STOCK")
        low_stock.append(name)
    elif qty <= 2:
        print(f"  WARNING: {name} is LOW ({qty} left)")
        low_stock.append(name)
    else:
        print(f"  OK: {name} ({qty} in stock)")
    i += 1

print(f"\nItems needing restock: {low_stock}")
```
```
# Expected Output:
  OK: Wireless Mouse (3 in stock)
  ALERT: USB Hub is OUT OF STOCK
  OK: Earbuds (5 in stock)
  ALERT: Laptop Stand is OUT OF STOCK

Items needing restock: ['USB Hub', 'Laptop Stand']
```

---

### Challenge: eCOMMart — Live Sales Terminal

Build a complete sales entry terminal using a `while` loop.

**Requirements:**
- Keep running until the cashier types `done`
- For each item: ask for name, unit price, and quantity
- After `done`, print a full receipt with:
  - Each item and its line total
  - Subtotal
  - GST at 18%
  - Discount: 10% if subtotal ≥ ₹2000, 5% if ≥ ₹1000, else 0%
  - Grand Total

```python
cart = []

print("=== eCOMMart Sales Terminal ===")

while True:
    name = input("\nEnter item name (or 'done' to print receipt): ")
    if name.lower() == 'done':
        break
    price = float(input("Enter price (₹): "))
    qty   = int(input("Enter quantity: "))
    cart.append({'name': name, 'price': price, 'qty': qty})

# --- Calculate totals ---
subtotal = sum(i['price'] * i['qty'] for i in cart)
gst      = round(subtotal * 0.18, 2)

if subtotal >= 2000:
    disc_rate = 0.10
elif subtotal >= 1000:
    disc_rate = 0.05
else:
    disc_rate = 0.0

discount    = round(subtotal * disc_rate, 2)
grand_total = round(subtotal + gst - discount, 2)

# --- Print receipt ---
print("\n" + "=" * 42)
print("        eCOMMart — Sales Receipt")
print("=" * 42)
for i in cart:
    line = i['price'] * i['qty']
    print(f"  {i['name']:<20} ₹{i['price']:.2f} x {i['qty']} = ₹{line:.2f}")
print("-" * 42)
print(f"  {'Subtotal':<28} ₹{subtotal:.2f}")
print(f"  {'GST (18%)':<28} ₹{gst:.2f}")
print(f"  {'Discount (' + str(int(disc_rate * 100)) + '%)':<28}-₹{discount:.2f}")
print(f"  {'Grand Total':<28} ₹{grand_total:.2f}")
print("=" * 42)
```
```
# Expected Output (with inputs: Wireless Mouse / 499 / 2, Earbuds / 1299 / 1, done):
=== eCOMMart Sales Terminal ===

Enter item name (or 'done' to print receipt): Wireless Mouse
Enter price (₹): 499
Enter quantity: 2

Enter item name (or 'done' to print receipt): Earbuds
Enter price (₹): 1299
Enter quantity: 1

Enter item name (or 'done' to print receipt): done

==========================================
        eCOMMart — Sales Receipt
==========================================
  Wireless Mouse       ₹499.00 x 2 = ₹998.00
  Earbuds              ₹1299.00 x 1 = ₹1299.00
------------------------------------------
  Subtotal                     ₹2297.00
  GST (18%)                    ₹413.46
  Discount (10%)              -₹229.70
  Grand Total                  ₹2480.76
==========================================
```

```
Verification:
  Wireless Mouse: ₹499 × 2 = ₹998
  Earbuds:       ₹1299 × 1 = ₹1299
  Subtotal                 = ₹2297   → qualifies for 10% discount
  GST:     ₹2297 × 0.18   = ₹413.46
  Discount: ₹2297 × 0.10  = ₹229.70
  Grand:   2297 + 413.46 − 229.70 = ₹2480.76
```
