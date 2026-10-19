# List Comprehensions

A list comprehension is a compact, readable way to build a new list from an existing sequence — all in a single line. Once you are comfortable with `for` loops, comprehensions are the natural next step.

**What we will cover:**

1. Basic syntax — the long way vs the short way
2. With a filter condition
3. With value transformation (ternary)
4. Multiple iteration
5. Nested lists and matrices
6. Set comprehensions
7. Dict comprehensions
8. Generator expressions
9. Exercise

---

## 1. Basic Syntax — The Long Way vs The Short Way

**The pattern:**

```
[ expression   for   variable   in   iterable ]
    what to       each item      where items
    produce       one at a time  come from
```

Here is the same task written both ways — building a list of the first 12 square numbers:

```python
# Long way — for loop with append
L = []
for n in range(12):
    L.append(n ** 2)
print(L)
```
```
# Output:
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]
```

```python
# Short way — list comprehension
print([n ** 2 for n in range(12)])
```
```
# Output:
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]
```

Both produce exactly the same result. Read the comprehension in plain English: *"give me n squared, for each n in the range 0 to 12"*.

### B2B eCom — Uppercase all vendor names for display

```python
vendor_names = ['tata electronics', 'reliance digital', 'infosys supplies']

# Long way
upper = []
for name in vendor_names:
    upper.append(name.upper())
print(upper)
```
```
# Output:
['TATA ELECTRONICS', 'RELIANCE DIGITAL', 'INFOSYS SUPPLIES']
```

```python
# Short way — comprehension
upper = [name.upper() for name in vendor_names]
print(upper)
```
```
# Output:
['TATA ELECTRONICS', 'RELIANCE DIGITAL', 'INFOSYS SUPPLIES']
```

---

## 2. With a Filter Condition

Add an `if` clause at the end to include only items that meet a condition:

```
[ expression   for   variable   in   iterable   if   condition ]
```

```python
# Numbers from 0–19 that are NOT multiples of 3
print([val for val in range(20) if val % 3 > 0])
```
```
# Output:
[1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19]
```

The long-way equivalent:

```python
L = []
for val in range(20):
    if val % 3:
        L.append(val)
print(L)
```
```
# Output:
[1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19]
```

### B2B eCom — Extract only bulk orders above ₹40,000

```python
order_amounts = [12500, 45000, 8750, 62000, 31500, 55000]

bulk_orders = [amt for amt in order_amounts if amt > 40000]
print(bulk_orders)
```
```
# Output:
[45000, 62000, 55000]
```

```
order_amounts: [12500, 45000, 8750, 62000, 31500, 55000]
                  ✗      ✓      ✗      ✓       ✗      ✓    ← if amt > 40000
result:               [45000,        62000,        55000]
```

### B2B eCom — Apply 10% trade discount to all prices

```python
prices = [45000, 12000, 8750, 62000, 31500]

discounted = [round(p * 0.90, 2) for p in prices]
print(discounted)
```
```
# Output:
[40500.0, 10800.0, 7875.0, 55800.0, 28350.0]
```

---

## 3. With Value Transformation — Ternary Expression

You can apply a condition **to the value itself** using a ternary expression. This is different from the filter condition — instead of excluding items, you transform them:

```
[ value_if_true  if  condition  else  value_if_false   for  var  in  iterable ]
```

```python
val = -10
print(val if val >= 0 else -val)   # same as abs(val)
```
```
# Output:
10
```

### B2B eCom — Cap order values at ₹50,000

```python
order_amounts = [12500, 45000, 62000, 31500, 55000]

capped = [50000 if amt > 50000 else amt for amt in order_amounts]
print(capped)
```
```
# Output:
[12500, 45000, 50000, 31500, 50000]
```

```
62000 > 50000 → cap to 50000
55000 > 50000 → cap to 50000
others        → keep as-is
```

**Combining filter and value transformation:**

```python
# Exclude multiples of 3; negate multiples of 2; keep everything else
result = [val if val % 2 else -val
          for val in range(20) if val % 3]
print(result)
```
```
# Output:
[1, -2, -4, 5, 7, -8, -10, 11, 13, -14, -16, 17, 19]
```

```
Step 1 — filter: exclude multiples of 3 → [1,2,4,5,7,8,10,11,13,14,16,17,19]
Step 2 — transform: if divisible by 2 → negate it; otherwise keep it
  1  → odd  → keep  →  1
  2  → even → negate → -2
  4  → even → negate → -4
  5  → odd  → keep  →  5
  ...
```

> The line break before `for` is valid Python and helps readability for longer comprehensions.

---

## 4. Multiple Iteration

Add a second `for` clause to produce combinations from two sequences:

```python
print([(i, j) for i in range(2) for j in range(3)])
```
```
# Output:
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
```

The second `for` is the inner loop — it varies fastest. This is equivalent to:

```python
result = []
for i in range(2):
    for j in range(3):
        result.append((i, j))
```

### B2B eCom — All vendor–product type combinations

```python
vendors       = ['Tata', 'Reliance']
product_types = ['Laptop', 'Phone']

pairs = [(v, p) for v in vendors for p in product_types]
print(pairs)
```
```
# Output:
[('Tata', 'Laptop'), ('Tata', 'Phone'), ('Reliance', 'Laptop'), ('Reliance', 'Phone')]
```

---

## 5. Nested Lists and Matrices

List comprehensions work naturally with nested lists (lists inside lists):

```python
M1 = [[1, 2, 3],
      [4, 5, 6],
      [7, 8, 9]]

M2 = [[9, 8, 7],
      [6, 5, 4],
      [3, 2, 1]]
```

```
M1 visualised:
           Col 0  Col 1  Col 2
Row 0  →  [  1,     2,     3  ]
Row 1  →  [  4,     5,     6  ]
Row 2  →  [  7,     8,     9  ]
```

```python
# Access a whole row
print(M1[2])
```
```
# Output:
[7, 8, 9]
```

```python
# Access a single element — row 2, column 2
print(M1[2][2])
```
```
# Output:
9
```

```python
# Extract the third column using comprehension
col3 = [r[2] for r in M1]
print(col3)
```
```
# Output:
[3, 6, 9]
```

```python
# Same result using explicit row indices
col3b = [M1[r][2] for r in (0, 1, 2)]
print(col3b)
```
```
# Output:
[3, 6, 9]
```

```
For each row r in M1:
  r[2] pulls out the third element

Row 0: [1, 2, 3] → r[2] = 3
Row 1: [4, 5, 6] → r[2] = 6
Row 2: [7, 8, 9] → r[2] = 9

Result: [3, 6, 9]
```

### B2B eCom — Extract first SKU from each warehouse shelf

```python
warehouse_shelf = [
    ['SKU001', 'SKU002'],
    ['SKU003', 'SKU004'],
    ['SKU005', 'SKU006']
]

first_skus = [shelf[0] for shelf in warehouse_shelf]
print(first_skus)
```
```
# Output:
['SKU001', 'SKU003', 'SKU005']
```

---

## 6. Set Comprehensions

Replace `[]` with `{}` to build a **set** — same idea, but the result contains only unique values and has no guaranteed order:

```python
print({n**2 for n in range(12)})
```
```
# Output:
{0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121}
```

```python
# Any number mod 3 can only ever be 0, 1, or 2
print({a % 3 for a in range(1000)})
```
```
# Output:
{0, 1, 2}
```

### B2B eCom — Get unique product categories

```python
products = [
    {"name": "Wireless Mouse", "category": "Electronics", "price": 499},
    {"name": "Laptop Stand",   "category": "Accessories", "price": 850},
    {"name": "USB Hub",        "category": "Electronics", "price": 350},
    {"name": "Smart Watch",    "category": "Wearables",   "price": 2999},
]

unique_categories = {p["category"] for p in products}
print(unique_categories)
```
```
# Output:
{'Electronics', 'Accessories', 'Wearables'}
```

> The order may vary — sets are unordered.

---

## 7. Dict Comprehensions

Use `{key: value for ...}` to build a **dictionary**:

```python
print({n: n**2 for n in range(6)})
```
```
# Output:
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### B2B eCom — Build a name → price lookup dictionary

```python
name_price = {p["name"]: p["price"] for p in products}
print(name_price)
```
```
# Output:
{'Wireless Mouse': 499, 'Laptop Stand': 850, 'USB Hub': 350, 'Smart Watch': 2999}
```

```python
# Now you can look up any product price instantly
print(name_price["Wireless Mouse"])
```
```
# Output:
499
```

---

## 8. Generator Expressions

Replace `[]` with `()` to get a **generator expression**. Instead of building the entire list in memory at once, it produces values **one at a time** as they are needed:

```python
gen = (n**2 for n in range(12))
print(type(gen))
```
```
# Output:
<class 'generator'>
```

```python
# Evaluate all values by converting to a list
print(list(gen))
```
```
# Output:
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]
```

### B2B eCom — Sum large orders without building an intermediate list

```python
order_amounts = [12500, 45000, 8750, 62000, 31500]

# sum() with a generator — memory efficient for large datasets
total = sum(amt for amt in order_amounts if amt > 10000)
print(f"Total of orders above ₹10000: ₹{total}")
```
```
# Output:
Total of orders above ₹10000: ₹151000
```

```
┌──────────────────┬─────────────────────────────────────────────┐
│  Syntax          │  Produces                                   │
├──────────────────┼─────────────────────────────────────────────┤
│  [expr for ...]  │  List — all values built immediately        │
│  {expr for ...]  │  Set  — unique values, unordered            │
│  {k:v for ...]   │  Dict — key-value pairs                     │
│  (expr for ...]  │  Generator — values produced one at a time  │
└──────────────────┴─────────────────────────────────────────────┘
```

---

## Exercise: eCOMMart Product Catalogue Analysis

You are a data analyst at eCOMMart. Use list comprehensions to extract insights from a product dataset.

```python
products = [
    {"name": "Wireless Mouse", "category": "Electronics", "price": 499,  "in_stock": True},
    {"name": "Laptop Stand",   "category": "Accessories", "price": 850,  "in_stock": False},
    {"name": "USB Hub",        "category": "Electronics", "price": 350,  "in_stock": True},
    {"name": "Smart Watch",    "category": "Wearables",   "price": 2999, "in_stock": True},
    {"name": "Earbuds",        "category": "Electronics", "price": 1299, "in_stock": True},
]
```

**Tasks — write each as a single list comprehension:**

1. All `"Electronics"` product names
2. Names of products with price > ₹1000
3. Names of all in-stock products
4. Average price across all products
5. Label strings in format: `"Wireless Mouse — ₹499 (Electronics)"`

```python
# Solution

# 1. Filter by category
electronics = [p["name"] for p in products if p["category"] == "Electronics"]
print(f"Electronics products : {electronics}")

# 2. Premium products (price > 1000)
premium = [p["name"] for p in products if p["price"] > 1000]
print(f"Premium products     : {premium}")

# 3. In-stock products
in_stock = [p["name"] for p in products if p["in_stock"]]
print(f"In-stock products    : {in_stock}")

# 4. Average price — extract prices, then calculate
prices = [p["price"] for p in products]
avg    = sum(prices) / len(prices)
print(f"Average price        : ₹{avg:.2f}")

# 5. Product label strings
labels = [f"{p['name']} — ₹{p['price']} ({p['category']})" for p in products]
print("Product labels       :")
for label in labels:
    print(f"  {label}")
```
```
# Expected Output:
Electronics products : ['Wireless Mouse', 'USB Hub', 'Earbuds']
Premium products     : ['Smart Watch', 'Earbuds']
In-stock products    : ['Wireless Mouse', 'USB Hub', 'Smart Watch', 'Earbuds']
Average price        : ₹1199.40
Product labels       :
  Wireless Mouse — ₹499 (Electronics)
  Laptop Stand — ₹850 (Accessories)
  USB Hub — ₹350 (Electronics)
  Smart Watch — ₹2999 (Wearables)
  Earbuds — ₹1299 (Electronics)
```
