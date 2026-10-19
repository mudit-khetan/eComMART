# Tuples

In Python, tuples are very similar to lists — but with one critical difference: they are **immutable**, meaning once created, they cannot be changed. Use tuples when data should stay fixed, such as product catalogue entries, GPS coordinates, or confirmed order records.

## List vs Tuple — Key Differences

| Feature | List | Tuple |
|---|---|---|
| **Mutability** | Mutable — can be modified | Immutable — cannot be modified |
| **Syntax** | Square brackets `[]` | Parentheses `()` |
| **Performance** | Slightly slower | Slightly faster |
| **Use Cases** | Dynamic data: shopping cart, task queue | Fixed data: coordinates, confirmed orders, config |
| **Methods** | `append()`, `remove()`, `pop()`, `extend()`, … | `count()` and `index()` only |
| **Memory** | More — dynamic size | Less — fixed size |
| **Safety** | Prone to accidental changes | Values cannot be altered |
| **As dict key** | ✗ Cannot (unhashable) | ✓ Can (hashable if elements are immutable) |

**What we will cover:**

1. Constructing Tuples
2. Indexing and Slicing
3. Basic Tuple Methods
4. Tuple Unpacking
5. Immutability
6. When to Use Tuples
7. Exercises

---

## 1. Constructing Tuples

Tuples use **parentheses** `()` with elements separated by commas.

```python
# A tuple of integers
t = (1, 2, 3)
print(t)
```
```
# Output:
(1, 2, 3)
```

```python
# len() works just like with lists
print(len(t))
```
```
# Output:
3
```

```python
# Tuples can hold mixed types
t = ('one', 2)
print(t)
```
```
# Output:
('one', 2)
```

> **Common beginner mistake — single-element tuples need a trailing comma:**

```python
# WITHOUT the comma — this is just a string in brackets, NOT a tuple
not_a_tuple = ('laptop')
print(not_a_tuple)
print(type(not_a_tuple))
```
```
# Output:
laptop
<class 'str'>
```

```python
# WITH the comma — this IS a tuple
single = ('laptop',)
print(single)
print(type(single))
```
```
# Output:
('laptop',)
<class 'tuple'>
```

```
          ┌──────────────────────────────────┐
          │  ('laptop')   → str  ← No comma  │
          │  ('laptop',)  → tuple ← Comma!   │
          └──────────────────────────────────┘
```

---

## 2. Indexing and Slicing

Indexing and slicing works exactly the same as with lists.

```python
t = ('one', 2)
```

```python
# Forward index — first item
print(t[0])
```
```
# Output:
one
```

```python
# Negative index — last item
print(t[-1])
```
```
# Output:
2
```

```
           ┌────────────────────────┐
           │  t = ('one', 2)        │
           ├───────────┬────────────┤
           │  'one'    │     2      │
           ├───────────┼────────────┤
Positive → │     0     │     1      │
Negative → │    -2     │    -1      │
           └───────────┴────────────┘
```

---

## 3. Basic Tuple Methods

Tuples only have two built-in methods — `count()` and `index()`.

```python
t = ('one', 2, 'one', 3)
print(t)
```
```
# Output:
('one', 2, 'one', 3)
```

```python
# index() — find the position of a value (returns first occurrence)
print(t.index('one'))
```
```
# Output:
0
```

```python
# count() — count how many times a value appears
print(t.count('one'))
```
```
# Output:
2
```

---

## 4. Tuple Unpacking

Tuple unpacking lets you assign each element of a tuple to its own variable in one line. This is used constantly in real Python code — especially when working with records, database rows, or paired data.

```python
# A confirmed order record — (order_id, vendor, amount)
order = ('ORD-1001', 'Tata Electronics', 45000)
print(order)
```
```
# Output:
('ORD-1001', 'Tata Electronics', 45000)
```

```python
# Unpack all three values at once
order_id, vendor, amount = order

print(order_id)
print(vendor)
print(amount)
```
```
# Output:
ORD-1001
Tata Electronics
45000
```

```
order = ('ORD-1001', 'Tata Electronics', 45000)
           ↓                ↓               ↓
        order_id          vendor          amount
```

Unpacking is also the natural way to loop through a tuple of pairs:

```python
price_tiers = (("XS", 399), ("S", 449), ("M", 499), ("L", 549), ("XL", 599), ("XXL", 649))

for size, price in price_tiers:
    print(f"  {size:<3} → ₹{price}")
```
```
# Output:
  XS  → ₹399
  S   → ₹449
  M   → ₹499
  L   → ₹549
  XL  → ₹599
  XXL → ₹649
```

---

## 5. Immutability

Tuples **cannot be changed** after they are created. You cannot add, remove, or modify any element.

```python
t = ('one', 2)

# Attempting to change an element raises a TypeError
try:
    t[0] = 'change'
except TypeError as e:
    print(f"TypeError: {e}")
```
```
# Output:
TypeError: 'tuple' object does not support item assignment
```

```python
# Attempting to append raises an AttributeError
try:
    t.append('new item')
except AttributeError as e:
    print(f"AttributeError: {e}")
```
```
# Output:
AttributeError: 'tuple' object has no attribute 'append'
```

```
List  → [1, 2, 3]  → can change  → [1, 2, 99]   ✓
Tuple → (1, 2, 3)  → immutable   → (1, 2, 99)   ✗ TypeError
```

---

## 6. When to Use Tuples

Use a tuple whenever the data **should not change** after it is created. Here are two real B2B eCom examples:

**Warehouse GPS coordinates — must never change:**

```python
# Latitude and longitude should be fixed
warehouse_location = (28.6139, 77.2090)
print(warehouse_location)
```
```
# Output:
(28.6139, 77.209)
```

```python
print(f"Latitude : {warehouse_location[0]}")
print(f"Longitude: {warehouse_location[1]}")
```
```
# Output:
Latitude : 28.6139
Longitude: 77.209
```

**Product master record — fixed after catalogue creation:**

```python
# (SKU, name, category, price)
product_record = ('SKU-001', 'Wireless Mouse', 'Electronics', 1299.00)
print(product_record)
```
```
# Output:
('SKU-001', 'Wireless Mouse', 'Electronics', 1299.0)
```

```
┌────────────────────────────────────────────────────────┐
│  Use a LIST when data changes over time                │
│    e.g. cart items, pending orders, active sessions    │
│                                                        │
│  Use a TUPLE when data is fixed and must not change    │
│    e.g. GPS coords, SKU records, size/price catalogue  │
└────────────────────────────────────────────────────────┘
```

---

## Exercise 1: Immutable Shopping Cart

You are designing a checkout system for **eCOMMart**. Once a customer confirms payment, the order contents must never be modified. Use a tuple to store and analyse a confirmed order.

**Instructions:**
- Create a tuple `confirmed_order` with 5 product names
- Display all items using a loop
- Attempt to use `.append()` and handle the error
- Count how many times `"Wireless Mouse"` appears

```python
# Solution
confirmed_order = ("Wireless Mouse", "USB Hub", "Wireless Mouse", "Laptop Stand", "Earbuds")

print("Confirmed Order Items:")
for item in confirmed_order:
    print(f"  - {item}")

print("\nAttempting to add a new item:")
try:
    confirmed_order.append("Keyboard")
except AttributeError as e:
    print(f"Error: {e}")

count = confirmed_order.count("Wireless Mouse")
print(f"\nWireless Mouse was ordered {count} time(s).")
```
```
# Expected Output:
Confirmed Order Items:
  - Wireless Mouse
  - USB Hub
  - Wireless Mouse
  - Laptop Stand
  - Earbuds

Attempting to add a new item:
Error: 'tuple' object has no attribute 'append'

Wireless Mouse was ordered 2 time(s).
```

---

## Exercise 2: Product Size and Price Catalogue

eCOMMart sells clothing. Sizes and prices are fixed at the time of catalogue creation — they must not be changed accidentally at runtime.

**Instructions:**
- Create `size_options` tuple with sizes `XS` through `XXL`
- Create `price_tiers` as a tuple of `(size, price)` pairs
- Display all sizes and prices using tuple unpacking in a loop
- Attempt to modify a size and handle the error
- Find and display the price for size `"L"`

```python
# Solution
size_options = ("XS", "S", "M", "L", "XL", "XXL")
price_tiers  = (("XS", 399), ("S", 449), ("M", 499), ("L", 549), ("XL", 599), ("XXL", 649))

print(f"Available Sizes: {size_options}")

print("\nSize Catalogue:")
for size, price in price_tiers:
    print(f"  {size:<3} → ₹{price}")

print("\nAttempting to change 'XS':")
try:
    size_options[0] = "XXXS"
except TypeError as e:
    print(f"Error: {e}")

for size, price in price_tiers:
    if size == "L":
        print(f"\nPrice for size L: ₹{price}")
        break
```
```
# Expected Output:
Available Sizes: ('XS', 'S', 'M', 'L', 'XL', 'XXL')

Size Catalogue:
  XS  → ₹399
  S   → ₹449
  M   → ₹499
  L   → ₹549
  XL  → ₹599
  XXL → ₹649

Attempting to change 'XS':
Error: 'tuple' object does not support item assignment

Price for size L: ₹549
```
