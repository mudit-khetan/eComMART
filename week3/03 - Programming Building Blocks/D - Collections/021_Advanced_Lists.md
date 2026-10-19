# List Methods

In this notebook we dive deeper into all the built-in methods available on a Python list. You will use these constantly when building real applications. Each method is shown with a **before and after** so you can clearly see what changed.

**What we will cover:**

1. `append()`
2. `extend()`
3. `insert()`
4. `pop()`
5. `remove()`
6. `clear()`
7. `copy()`
8. `count()`
9. `index()`
10. `reverse()`
11. `sort()`
12. List Comprehensions
13. Exercise

---

```
┌──────────────────────────────────────────────────────────────────────┐
│                   Quick Reference — List Methods                     │
├──────────────┬───────────────────────────────────────────────────────┤
│  Method      │  What it does                                         │
├──────────────┼───────────────────────────────────────────────────────┤
│  append()    │  Add one item to the end                              │
│  extend()    │  Add all items from another list to the end           │
│  insert()    │  Add one item at a specific position                  │
│  pop()       │  Remove and return an item (by index)                 │
│  remove()    │  Remove the first occurrence of a value               │
│  clear()     │  Remove all items from the list                       │
│  copy()      │  Return a new independent copy of the list            │
│  count()     │  Count how many times a value appears                 │
│  index()     │  Find the position of a value                         │
│  reverse()   │  Reverse the order in place                           │
│  sort()      │  Sort the list in place                               │
└──────────────┴───────────────────────────────────────────────────────┘
```

---

## 1. `append()`

`append()` adds **one item** to the **end** of the list. This changes the list permanently.

```python
l = [1, 2, 3]
print(l)
```
```
# Output:
[1, 2, 3]
```

```python
l.append(4)
print(l)
```
```
# Output:
[1, 2, 3, 4]
```

```
Before: [1, 2, 3]
               ↓  append(4)
After:  [1, 2, 3, 4]
                  ^^^
                  new item added at the end
```

---

## 2. `extend()`

`extend()` adds **every item** from another list to the end. This is different from `append()`.

> **Key difference:**
> - `append([4, 5])` adds the list `[4, 5]` as a **single nested item**
> - `extend([4, 5])` adds `4` and `5` as **two separate items**

```python
# append — adds the list itself as one item
x = [1, 2, 3]
print(x)
```
```
# Output:
[1, 2, 3]
```

```python
x.append([4, 5])
print(x)
```
```
# Output:
[1, 2, 3, [4, 5]]
           ^^^^^^
           one nested list item
```

```python
# extend — adds each element individually
x = [1, 2, 3]
print(x)
```
```
# Output:
[1, 2, 3]
```

```python
x.extend([4, 5])
print(x)
```
```
# Output:
[1, 2, 3, 4, 5]
          ^^^^
          two separate items added
```

```
append([4,5]) → [1, 2, 3, [4, 5]]   ← list inside a list
extend([4,5]) → [1, 2, 3,  4,  5]   ← items merged in flat
```

---

## 3. `insert()`

`insert(index, object)` places an item at a **specific position**.
Everything from that position onward shifts one place to the right.

```python
l = [1, 2, 3, 4]
print(l)
```
```
# Output:
[1, 2, 3, 4]
```

```python
# Insert 'inserted' at index 2
l.insert(2, 'inserted')
print(l)
```
```
# Output:
[1, 2, 'inserted', 3, 4]
```

```
Before: [  1,   2,   3,   4  ]
         idx0 idx1 idx2 idx3

insert(2, 'inserted')

After:  [  1,   2,  'inserted',  3,   4  ]
         idx0 idx1    idx2      idx3  idx4
                      ^^^^^^^^
                      new item pushed everything right
```

---

## 4. `pop()`

`pop()` **removes and returns** an item from the list so you can use the removed value.

- `pop()` with no argument removes the **last item**
- `pop(index)` removes the item at that **specific index**

```python
l = [1, 2, 'inserted', 3, 4]
print(l)
```
```
# Output:
[1, 2, 'inserted', 3, 4]
```

```python
# Pop the last item
ele = l.pop()
print(ele)
```
```
# Output:
4
```

```python
# List after popping the last item
print(l)
```
```
# Output:
[1, 2, 'inserted', 3]
```

```python
# Pop the item at index 0
ele2 = l.pop(0)
print(ele2)
```
```
# Output:
1
```

```python
# List after popping index 0
print(l)
```
```
# Output:
[2, 'inserted', 3]
```

```
pop()    → removes from the right end   ←  most common use
pop(0)   → removes from the left end
pop(n)   → removes from position n
```

---

## 5. `remove()`

`remove(value)` removes the **first occurrence** of a value. If the value appears more than once, only the first one is removed.

```python
l = [1, 2, 'inserted', 3]
print(l)
```
```
# Output:
[1, 2, 'inserted', 3]
```

```python
l.remove('inserted')
print(l)
```
```
# Output:
[1, 2, 3]
```

> **Important — only the first occurrence is removed:**

```python
l = [1, 2, 3, 4, 3]
print(l)
```
```
# Output:
[1, 2, 3, 4, 3]
```

```python
l.remove(3)
print(l)
```
```
# Output:
[1, 2, 4, 3]
         ^
         second 3 is still here — only the first one was removed
```

```
Before: [1, 2, 3, 4, 3]
                ^         ← remove(3) targets this one (first match)
After:  [1, 2, 4, 3]
                   ^      ← this 3 was not touched
```

---

## 6. `clear()`

`clear()` removes **all items** from the list, leaving it empty. The list itself still exists — it is just empty.

```python
l = [1, 2, 3, 4]
print(l)
```
```
# Output:
[1, 2, 3, 4]
```

```python
l.clear()
print(l)
```
```
# Output:
[]
```

> **When is this useful?** When you want to reset a list and start fresh — for example, clearing a shopping cart or resetting a list of pending orders at the start of a new session.

---

## 7. `copy()`

`copy()` creates a **new independent copy** of the list. This is different from simply assigning a list to another variable.

> **Why does this matter?** When you do `b = a`, both `a` and `b` point to the **same list** in memory. Changing one changes both. `copy()` creates a truly separate list.

```python
original = [1, 2, 3]
print(original)
```
```
# Output:
[1, 2, 3]
```

```python
# Direct assignment — both point to the SAME list
ref = original

# copy() — creates a NEW separate list
copied = original.copy()

# Now change via ref
ref.append(99)

print(original)
```
```
# Output:
[1, 2, 3, 99]
```

```python
# original changed because ref IS the same object
print(ref)
```
```
# Output:
[1, 2, 3, 99]
```

```python
# copied is unaffected — it is a separate list
print(copied)
```
```
# Output:
[1, 2, 3]
```

```
original ──┐
            ├──→ [1, 2, 3, 99]   ← SAME object in memory
ref      ──┘

copied   ──→ [1, 2, 3]           ← SEPARATE object in memory
```

---

## 8. `count()`

`count(value)` returns how many times a value appears in the list. Returns `0` if the value is not found — it does **not** raise an error.

> **B2B eCom context:** Check how many times a particular order ID has been logged (duplicate detection).

```python
order_ids = [1001, 1002, 1001, 1003, 1001, 1002]
print(order_ids)
```
```
# Output:
[1001, 1002, 1001, 1003, 1001, 1002]
```

```python
# Order 1001 appears 3 times
print(order_ids.count(1001))
```
```
# Output:
3
```

```python
# Order 1002 appears 2 times
print(order_ids.count(1002))
```
```
# Output:
2
```

```python
# Order 9999 does not exist — returns 0, not an error
print(order_ids.count(9999))
```
```
# Output:
0
```

---

## 9. `index()`

`index(value)` returns the **position** of the first occurrence of a value.

> **Important:** If the value is **not** in the list, Python raises a `ValueError`. Always handle this case.

> **B2B eCom context:** Find which position a vendor occupies in a priority list.

```python
vendor_names = ['Tata', 'Reliance', 'Infosys', 'Wipro']
print(vendor_names)
```
```
# Output:
['Tata', 'Reliance', 'Infosys', 'Wipro']
```

```python
# Find the position of 'Infosys'
print(vendor_names.index('Infosys'))
```
```
# Output:
2
```

```python
# Safely handle a value that may not be in the list
try:
    print(vendor_names.index('Amazon'))
except ValueError:
    print("Vendor not found in the list")
```
```
# Output:
Vendor not found in the list
```

```
vendor_names = ['Tata', 'Reliance', 'Infosys', 'Wipro']
                  0         1           2          3
                                        ↑
                        index('Infosys') returns 2
```

---

## 10. `reverse()`

`reverse()` reverses the order of the list **in place** — meaning the original list is permanently changed. No new list is created.

> **B2B eCom context:** Reverse the display order of product names for a descending catalogue view.

```python
product_names = ['Laptop', 'Mouse', 'Keyboard', 'Monitor']
print(product_names)
```
```
# Output:
['Laptop', 'Mouse', 'Keyboard', 'Monitor']
```

```python
product_names.reverse()
print(product_names)
```
```
# Output:
['Monitor', 'Keyboard', 'Mouse', 'Laptop']
```

```
Before: ['Laptop', 'Mouse', 'Keyboard', 'Monitor']
                         reverse()
After:  ['Monitor', 'Keyboard', 'Mouse', 'Laptop']
         ←────────────────────────────────────────
```

> **Note:** `reverse()` returns `None` — it changes the list directly. Do **not** write `product_names = product_names.reverse()` or you will lose your list.

---

## 11. `sort()`

`sort()` sorts the list **in place** — permanently, in ascending order by default.

> **B2B eCom context:** Sort product prices from lowest to highest, or vendor names alphabetically.

### Sorting numbers

```python
product_prices = [45000, 12000, 8750, 62000, 31500]
print(product_prices)
```
```
# Output:
[45000, 12000, 8750, 62000, 31500]
```

```python
# Sort ascending (lowest to highest — default)
product_prices.sort()
print(product_prices)
```
```
# Output:
[8750, 12000, 31500, 45000, 62000]
```

```python
# Sort descending (highest to lowest)
product_prices.sort(reverse=True)
print(product_prices)
```
```
# Output:
[62000, 45000, 31500, 12000, 8750]
```

### Sorting strings (alphabetically)

```python
vendor_names = ['Tata', 'Reliance', 'Infosys', 'Wipro']
print(vendor_names)
```
```
# Output:
['Tata', 'Reliance', 'Infosys', 'Wipro']
```

```python
vendor_names.sort()
print(vendor_names)
```
```
# Output:
['Infosys', 'Reliance', 'Tata', 'Wipro']
```

```
Unsorted:  [45000, 12000,  8750, 62000, 31500]
                        sort()
Ascending: [ 8750, 12000, 31500, 45000, 62000]
                    sort(reverse=True)
Descending:[62000, 45000, 31500, 12000,  8750]
```

> **Note:** Like `reverse()`, `sort()` returns `None`. It changes the list directly.

---

## 12. List Comprehensions

A **list comprehension** builds a new list from an existing one — in a single line. It replaces the pattern of creating an empty list, looping over another list, and appending.

### Basic Pattern

```
[  expression   for   item   in   list  ]
    what to do    each item   source list
```

### 12.1 — Transform every item

> **B2B eCom context:** Uppercase all product names for display in a catalogue header.

```python
product_names = ['laptop', 'mouse', 'keyboard', 'monitor', 'webcam']
print(product_names)
```
```
# Output:
['laptop', 'mouse', 'keyboard', 'monitor', 'webcam']
```

```python
# The long way (without comprehension)
upper_names = []
for name in product_names:
    upper_names.append(name.upper())
print(upper_names)
```
```
# Output:
['LAPTOP', 'MOUSE', 'KEYBOARD', 'MONITOR', 'WEBCAM']
```

```python
# The short way — list comprehension
upper_names = [name.upper() for name in product_names]
print(upper_names)
```
```
# Output:
['LAPTOP', 'MOUSE', 'KEYBOARD', 'MONITOR', 'WEBCAM']
```

### 12.2 — Filter items with a condition

> **B2B eCom context:** Extract only bulk orders (above ₹40,000) for a B2B priority report.

```python
order_amounts = [12500, 45000, 8750, 62000, 31500, 55000]
print(order_amounts)
```
```
# Output:
[12500, 45000, 8750, 62000, 31500, 55000]
```

```python
bulk_orders = [amount for amount in order_amounts if amount > 40000]
print(bulk_orders)
```
```
# Output:
[45000, 62000, 55000]
```

```
Pattern with condition:
[  expression   for   item   in   list   if   condition  ]
```

### 12.3 — Transform with a calculation

> **B2B eCom context:** Apply a 10% trade discount to all product prices.

```python
product_prices = [45000, 12000, 8750, 62000, 31500]
print(product_prices)
```
```
# Output:
[45000, 12000, 8750, 62000, 31500]
```

```python
discount_rate = 0.10
discounted = [round(price * (1 - discount_rate), 2) for price in product_prices]
print(discounted)
```
```
# Output:
[40500.0, 10800.0, 7875.0, 55800.0, 28350.0]
```

### 12.4 — Filter and transform together

> **B2B eCom context:** From all orders, take only high-value ones (above ₹40,000) and add 18% GST.

```python
order_amounts = [12500, 45000, 8750, 62000, 31500, 55000]
print(order_amounts)
```
```
# Output:
[12500, 45000, 8750, 62000, 31500, 55000]
```

```python
gst_rate = 0.18
high_value_with_gst = [
    round(amt * (1 + gst_rate), 2)
    for amt in order_amounts
    if amt > 40000
]
print(high_value_with_gst)
```
```
# Output:
[53100.0, 73160.0, 64900.0]
```

```
order_amounts = [12500, 45000, 8750, 62000, 31500, 55000]
                   ✗      ✓     ✗      ✓      ✗      ✓    ← if amt > 40000
                        ×1.18        ×1.18          ×1.18 ← apply GST
Result:        [       53100.0,     73160.0,       64900.0]
```

### 12.5 — Nested comprehension (working with nested lists)

> **B2B eCom context:** A warehouse has multiple shelves. Each shelf has multiple SKUs. Extract the first SKU from every shelf.

```python
warehouse_shelf = [
    ['SKU001', 'SKU002'],
    ['SKU003', 'SKU004'],
    ['SKU005', 'SKU006']
]
print(warehouse_shelf)
```
```
# Output:
[['SKU001', 'SKU002'], ['SKU003', 'SKU004'], ['SKU005', 'SKU006']]
```

```python
# Get the first SKU from each shelf
first_sku_per_shelf = [shelf[0] for shelf in warehouse_shelf]
print(first_sku_per_shelf)
```
```
# Output:
['SKU001', 'SKU003', 'SKU005']
```

```
warehouse_shelf:
  Shelf 0 → ['SKU001', 'SKU002']   → shelf[0] → 'SKU001'
  Shelf 1 → ['SKU003', 'SKU004']   → shelf[0] → 'SKU003'
  Shelf 2 → ['SKU005', 'SKU006']   → shelf[0] → 'SKU005'

Result: ['SKU001', 'SKU003', 'SKU005']
```

---

## Exercise: eCOMMart — Order Processing Pipeline

You are building a data processing script for **eCOMMart's** order management system.

**You are given:**

```python
orders = [
    {'id': 1001, 'vendor': 'tata electronics', 'amount': 45000, 'status': 'pending'},
    {'id': 1002, 'vendor': 'reliance digital',  'amount': 8750,  'status': 'completed'},
    {'id': 1003, 'vendor': 'infosys supplies',  'amount': 62000, 'status': 'pending'},
    {'id': 1004, 'vendor': 'wipro hardware',    'amount': 31500, 'status': 'completed'},
    {'id': 1005, 'vendor': 'tata electronics',  'amount': 55000, 'status': 'pending'},
]
```

**Tasks — use list methods and comprehensions:**

1. Extract a list of all vendor names and display them in **Title Case** using a comprehension
2. Extract all **pending** order amounts using a comprehension with a condition
3. Find the **highest and lowest** pending order amounts
4. Add a new order `{'id': 1006, 'vendor': 'HCL tech', 'amount': 72000, 'status': 'pending'}` to the list
5. Count how many orders have `status == 'pending'`
6. Sort the pending amounts in **descending order** and display them

```python
# write your code here

orders = [
    {'id': 1001, 'vendor': 'tata electronics', 'amount': 45000, 'status': 'pending'},
    {'id': 1002, 'vendor': 'reliance digital',  'amount': 8750,  'status': 'completed'},
    {'id': 1003, 'vendor': 'infosys supplies',  'amount': 62000, 'status': 'pending'},
    {'id': 1004, 'vendor': 'wipro hardware',    'amount': 31500, 'status': 'completed'},
    {'id': 1005, 'vendor': 'tata electronics',  'amount': 55000, 'status': 'pending'},
]

# Task 1 — Vendor names in Title Case
vendor_names = [order['vendor'].title() for order in orders]
print("Vendors       :", vendor_names)

# Task 2 — Pending order amounts
pending_amounts = [order['amount'] for order in orders if order['status'] == 'pending']
print("Pending Amounts:", pending_amounts)

# Task 3 — Highest and lowest pending amounts
print("Highest Pending: ₹", max(pending_amounts))
print("Lowest Pending : ₹", min(pending_amounts))

# Task 4 — Add a new order
orders.append({'id': 1006, 'vendor': 'HCL tech', 'amount': 72000, 'status': 'pending'})
print("Total Orders   :", len(orders))

# Task 5 — Count pending orders (recompute after adding new order)
pending_count = [order['status'] for order in orders].count('pending')
print("Pending Orders :", pending_count)

# Task 6 — Sort pending amounts descending
pending_amounts = [order['amount'] for order in orders if order['status'] == 'pending']
pending_amounts.sort(reverse=True)
print("Sorted Pending :", pending_amounts)
```

```
# Expected Output:
Vendors       : ['Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware', 'Tata Electronics']
Pending Amounts: [45000, 62000, 55000]
Highest Pending: ₹ 62000
Lowest Pending : ₹ 45000
Total Orders   : 6
Pending Orders : 4
Sorted Pending : [72000, 62000, 55000, 45000]
```

---

**You now have a complete understanding of all built-in list methods and how to use list comprehensions to write clean, efficient Python code.**
