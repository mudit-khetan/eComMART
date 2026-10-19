# Sets and Booleans

Two more essential Python data types — **Sets** for working with unique collections, and **Booleans** for representing True/False logic that drives decisions in your code.

**What we will cover:**

1. Sets — creating and adding
2. Uniqueness and the unordered nature of sets
3. Casting a list to a set
4. `remove()` vs `discard()`
5. Booleans — True, False, and None
6. Comparison operators
7. Exercises

---

## 1. Sets

A **set** is an unordered collection of **unique** elements. Sets are created using `set()`.

```python
# Create an empty set — note: use set(), not {} (that creates a dict)
x = set()
print(x)
```
```
# Output:
set()
```

```python
# Add elements using .add()
x.add(1)
print(x)
```
```
# Output:
{1}
```

```python
# Add another element
x.add(2)
print(x)
```
```
# Output:
{1, 2}
```

> **Note:** Sets use curly brackets `{}` in their output — but this is **not** a dictionary. A set is like a dictionary that only has keys and no values.

---

## 2. Uniqueness and the Unordered Nature of Sets

Sets **only store each value once**. Adding a duplicate has no effect:

```python
# Try to add 1 again — already in the set
x.add(1)
print(x)
```
```
# Output:
{1, 2}
```

```
x.add(1) → already exists → ignored
x.add(2) → already exists → ignored
x.add(3) → new value     → added

Result: {1, 2, 3}
```

> **Important — sets are unordered.** Unlike lists and tuples, sets have no guaranteed order. The same set may display in a different order each time you run your code. **Never rely on the position of items in a set.**

```
List  → ['C101', 'C204', 'C305']   ← order is guaranteed
Tuple → ('C101', 'C204', 'C305')   ← order is guaranteed
Set   → {'C204', 'C101', 'C305'}   ← order is NOT guaranteed
```

---

## 3. Casting a List to a Set

A very common use case: you have a list with duplicates and want only the unique values. Cast it to a set:

```python
# A list of buyer IDs with repeated entries
l = [1, 1, 2, 2, 3, 4, 5, 6, 1, 1]
print(l)
```
```
# Output:
[1, 1, 2, 2, 3, 4, 5, 6, 1, 1]
```

```python
# Cast to set — duplicates are removed automatically
print(set(l))
```
```
# Output:
{1, 2, 3, 4, 5, 6}
```

```
list: [1, 1, 2, 2, 3, 4, 5, 6, 1, 1]
              ↓  set()
set:  {1, 2, 3, 4, 5, 6}
       duplicates removed, unique values only
```

---

## 4. `remove()` vs `discard()`

Sets have two methods for removing an element. They behave differently when the element is **not found**:

| Method | Element found | Element NOT found |
|---|---|---|
| `remove(value)` | Removes it | Raises `KeyError` |
| `discard(value)` | Removes it | Does nothing — no error |

```python
s = {1, 2, 3, 4}
print(s)
```
```
# Output:
{1, 2, 3, 4}
```

```python
# discard — safe, no error even if element is missing
s.discard(3)
print(s)
```
```
# Output:
{1, 2, 4}
```

```python
# discard a value that isn't there — no error
s.discard(99)
print(s)
```
```
# Output:
{1, 2, 4}
```

```python
s2 = {1, 2, 3, 4}

# remove — works when element exists
s2.remove(3)
print(s2)
```
```
# Output:
{1, 2, 4}
```

```python
# remove a value that isn't there — raises KeyError
try:
    s2.remove(99)
except KeyError as e:
    print(f"KeyError: {e}")
```
```
# Output:
KeyError: 99
```

```
┌──────────────────────────────────────────────────────┐
│  Use discard() when you're not sure the item exists  │
│  Use remove()  when you know it should be there      │
└──────────────────────────────────────────────────────┘
```

> The full set of advanced methods (`difference`, `intersection`, `union`, and more) are covered in the next notebook — **015_Advanced_Sets**.

---

## 5. Booleans

Booleans represent one of two values: **`True`** or **`False`**. They are the foundation of all decision-making in Python.

```python
# Assign a boolean value directly
a = True
print(a)
```
```
# Output:
True
```

```python
# Booleans are actually integers underneath
print(int(True))
print(int(False))
```
```
# Output:
1
0
```

---

## 6. Comparison Operators

Comparison operators evaluate two values and return a Boolean result:

```python
print(1 > 2)
```
```
# Output:
False
```

```python
print(2 > 1)
```
```
# Output:
True
```

```python
print(10 == 10)
```
```
# Output:
True
```

```python
print(10 != 5)
```
```
# Output:
True
```

```
┌────────────────────────────────────────────────┐
│  Operator  │  Meaning              │  Example  │
├────────────┼───────────────────────┼───────────┤
│     >      │  Greater than         │  5 > 3    │
│     <      │  Less than            │  2 < 8    │
│     >=     │  Greater or equal     │  5 >= 5   │
│     <=     │  Less or equal        │  3 <= 4   │
│     ==     │  Equal to             │  10 == 10 │
│     !=     │  Not equal to         │  5 != 3   │
└────────────┴───────────────────────┴───────────┘
```

> We will use these operators extensively in the **if statements** and **loops** notebooks coming up.

---

## 7. `None` — A Placeholder Value

`None` represents the **absence of a value**. Use it when you want a variable to exist but don't have a value for it yet.

```python
# A shipment not yet assigned
pending_shipment = None
print(pending_shipment)
```
```
# Output:
None
```

```python
# Later, assign an actual value
pending_shipment = 'ORD-1005'
print(pending_shipment)
```
```
# Output:
ORD-1005
```

```
pending_shipment = None      ← placeholder, no value yet
pending_shipment = 'ORD-1005'  ← value assigned when ready
```

---

## Exercise 1: eCOMMart — Unique Buyers Tracker

eCOMMart's analytics team wants to count unique customers who purchased during a flash sale. Some customers made multiple purchases and should be counted only once.

**Instructions:**
- Start with the buyer ID list below (contains duplicates)
- Convert to a set to get unique buyers
- Check if `"C305"` and `"C999"` are in the set
- Print the total count of unique buyers

```python
# Solution
buyer_ids = ["C101", "C204", "C101", "C305", "C204", "C408", "C101"]
unique_buyers = set(buyer_ids)

print(f"All Purchase Records : {buyer_ids}")
print(f"Unique Buyers        : {unique_buyers}")

print(f"\nIs C305 a buyer? {'Yes' if 'C305' in unique_buyers else 'No'}")
print(f"Is C999 a buyer? {'Yes' if 'C999' in unique_buyers else 'No'}")

print(f"\nTotal Unique Buyers: {len(unique_buyers)}")
```
```
# Expected Output:
All Purchase Records : ['C101', 'C204', 'C101', 'C305', 'C204', 'C408', 'C101']
Unique Buyers        : {'C101', 'C204', 'C305', 'C408'}

Is C305 a buyer? Yes
Is C999 a buyer? No

Total Unique Buyers: 4
```

> **Note:** The order of items inside the set may vary each time you run this — sets are unordered. The count will always be 4.

---

## Exercise 2: eCOMMart — Order Eligibility Checker

eCOMMart uses boolean flags to decide whether an order can be processed and whether it qualifies for express delivery.

**Rules:**
- An order is **processed** if: `is_payment_confirmed` **and** `is_in_stock` are both `True`
- An order is **express eligible** if: it is processed **and** `is_express_zone` is `True`

**Instructions:**
- Define boolean variables for two sample orders
- Use `and` to combine conditions
- Print a clear summary for each order

```python
# Solution

# --- Order 1: Wireless Mouse ---
is_payment_confirmed_1 = True
is_in_stock_1          = True
is_express_zone_1      = True

order_processed_1  = is_payment_confirmed_1 and is_in_stock_1
express_delivery_1 = order_processed_1 and is_express_zone_1

print("Order 1 (Wireless Mouse):")
print(f"  Payment Confirmed : {is_payment_confirmed_1}")
print(f"  In Stock          : {is_in_stock_1}")
print(f"  Express Zone      : {is_express_zone_1}")
print(f"  Order Processed   : {'Yes' if order_processed_1 else 'No'}")
print(f"  Express Delivery  : {'Yes' if express_delivery_1 else 'No'}")

# --- Order 2: Laptop Stand ---
is_payment_confirmed_2 = True
is_in_stock_2          = False
is_express_zone_2      = True

order_processed_2  = is_payment_confirmed_2 and is_in_stock_2
express_delivery_2 = order_processed_2 and is_express_zone_2

print("\nOrder 2 (Laptop Stand):")
print(f"  Payment Confirmed : {is_payment_confirmed_2}")
print(f"  In Stock          : {is_in_stock_2}")
print(f"  Express Zone      : {is_express_zone_2}")
print(f"  Order Processed   : {'Yes' if order_processed_2 else 'No'}")
print(f"  Express Delivery  : {'Yes' if express_delivery_2 else 'No'}")
```
```
# Expected Output:
Order 1 (Wireless Mouse):
  Payment Confirmed : True
  In Stock          : True
  Express Zone      : True
  Order Processed   : Yes
  Express Delivery  : Yes

Order 2 (Laptop Stand):
  Payment Confirmed : True
  In Stock          : False
  Express Zone      : True
  Order Processed   : No
  Express Delivery  : No
```
