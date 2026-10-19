# Lists

Lists are the most general version of a *sequence* in Python. Unlike strings, they are **mutable** — meaning you can change them after they are created.

**What we will cover:**

1. Creating Lists
2. Indexing and Slicing Lists
3. List Operations
4. Built-in Functions on Lists
5. Basic List Methods
6. Nesting Lists
7. Introduction to List Comprehensions
8. Exercise

---

## 1. Creating Lists

Lists are constructed with square brackets `[]` and commas separating every element.

```python
# An empty list — a common starting point before adding items
empty_list = []
print(empty_list)
```
```
# Output:
[]
```

```python
# A list with a single item
single_item = ['laptop']
print(single_item)
```
```
# Output:
['laptop']
```

```python
# A list of integers
my_list = [1, 2, 3]
print(my_list)
```
```
# Output:
[1, 2, 3]
```

Lists can hold **different data types** in the same list — strings, numbers, decimals, all together:

```python
my_list = ['A string', 23, 100.232, 'o']
print(my_list)
```
```
# Output:
['A string', 23, 100.232, 'o']
```

Use `len()` to find out how many items are in a list:

```python
print(len(my_list))
```
```
# Output:
4
```

---

## 2. Indexing and Slicing

Every item in a list has a position number called an **index**. Python starts counting from **0**.

```
           ┌─────────────────────────────────────────────────────────┐
           │   my_list = ['one', 'two', 'three', 4, 5]              │
           ├──────────┬──────────┬──────────┬──────────┬────────────┤
           │  'one'   │  'two'   │ 'three'  │    4     │     5      │
           ├──────────┼──────────┼──────────┼──────────┼────────────┤
Positive → │    0     │    1     │    2     │    3     │     4      │
Negative → │   -5     │   -4     │   -3     │   -2     │    -1      │
           └──────────┴──────────┴──────────┴──────────┴────────────┘
```

```python
my_list = ['one', 'two', 'three', 4, 5]
print(my_list)
```
```
# Output:
['one', 'two', 'three', 4, 5]
```

**Forward indexing** — count from the left, starting at 0:

```python
# Grab element at index 0 (first item)
print(my_list[0])
```
```
# Output:
one
```

**Negative indexing** — count from the right, starting at -1:

```python
# Grab the last item using negative index
print(my_list[-1])
```
```
# Output:
5
```

**Slicing** — grab a range of items using `[start:stop]`. The stop index is *not* included:

```python
# Grab index 1 and everything past it
print(my_list[1:])
```
```
# Output:
['two', 'three', 4, 5]
```

```python
# Grab everything UP TO index 3 (index 3 not included)
print(my_list[:3])
```
```
# Output:
['one', 'two', 'three']
```

**Step slicing** — grab every nth item using `[start:stop:step]`:

```python
# Grab every 2nd item (index 0, 2, 4)
print(my_list[::2])
```
```
# Output:
['one', 'three', 5]
```

---

## 3. List Operations

### Concatenation with `+`

You can join two lists together using `+`. This creates a **new list** — it does not change the original:

```python
print(my_list + ['new item'])
```
```
# Output:
['one', 'two', 'three', 4, 5, 'new item']
```

```python
# The original list is unchanged
print(my_list)
```
```
# Output:
['one', 'two', 'three', 4, 5]
```

To make the change permanent, **reassign** the list:

```python
# Reassign — now the change is saved
my_list = my_list + ['add new item permanently']
print(my_list)
```
```
# Output:
['one', 'two', 'three', 4, 5, 'add new item permanently']
```

### Duplication with `*`

Use `*` to repeat a list. Like `+`, this is **not permanent** unless you reassign:

```python
my_list = ['one', 'two', 'three', 4, 5]
print(my_list * 2)
```
```
# Output:
['one', 'two', 'three', 4, 5, 'one', 'two', 'three', 4, 5]
```

```python
# Original is still unchanged
print(my_list)
```
```
# Output:
['one', 'two', 'three', 4, 5]
```

### Membership check with `in`

Use `in` to check whether an item exists in a list. Returns `True` or `False`:

```python
print('one' in my_list)
```
```
# Output:
True
```

```python
print('ten' in my_list)
```
```
# Output:
False
```

---

## 4. Built-in Functions on Lists

Python has several built-in functions that work directly on lists. These are used constantly in real applications.

> **B2B eCom context:** We have a list of order amounts (in ₹) placed by business buyers on our platform.

```python
order_amounts = [12500, 45000, 8750, 62000, 31500]
print(order_amounts)
```
```
# Output:
[12500, 45000, 8750, 62000, 31500]
```

```python
# len() — how many orders were placed?
print(len(order_amounts))
```
```
# Output:
5
```

```python
# min() — what was the smallest order?
print(min(order_amounts))
```
```
# Output:
8750
```

```python
# max() — what was the largest order?
print(max(order_amounts))
```
```
# Output:
62000
```

```python
# sum() — what is the total revenue from all orders?
print(sum(order_amounts))
```
```
# Output:
159750
```

```
┌────────────────────────────────────────────────────────┐
│  Function  │  What it does               │  Result     │
├────────────┼─────────────────────────────┼─────────────┤
│  len()     │  Count of items             │  5          │
│  min()     │  Smallest value             │  8750       │
│  max()     │  Largest value              │  62000      │
│  sum()     │  Total of all values        │  159750     │
└────────────────────────────────────────────────────────┘
```

---

## 5. Basic List Methods

Lists have built-in **methods** — actions you can call directly on a list using dot notation: `list.method()`.

Lists are flexible for two key reasons:
1. They have **no fixed size** — grow or shrink as needed
2. They have **no fixed type** — mix strings, numbers, anything

```python
# Start with a simple list
l = [1, 2, 3]
print(l)
```
```
# Output:
[1, 2, 3]
```

### `append()` — Add an item to the end

`append()` permanently adds one item to the end of the list:

```python
l.append('append me!')
print(l)
```
```
# Output:
[1, 2, 3, 'append me!']
```

### `pop()` — Remove and return an item

`pop()` removes an item from the list **and returns it** so you can use it.
By default it removes the **last** item, but you can pass an index:

```python
# Pop off the item at index 0
p = l.pop(0)
print(p)
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
[2, 3, 'append me!']
```

```python
# Pop the last item (default behaviour)
popped_item = l.pop()
print(popped_item)
```
```
# Output:
append me!
```

```python
# List after popping the last item
print(l)
```
```
# Output:
[2, 3]
```

> **Important:** Accessing an index that does not exist will raise an error:

```python
# This will cause an IndexError
print(l[100])
```
```
# Output:
IndexError: list index out of range
```

---

## 6. Nesting Lists

Python lists support **nesting** — a list can contain other lists. This lets you represent structures like a grid or a table.

```python
# Three separate lists
lst_1 = [1, 2, 3]
lst_2 = [4, 5, 6]
lst_3 = [7, 8, 9]

# Combine into a matrix (list of lists)
matrix = [lst_1, lst_2, lst_3]
print(matrix)
```
```
# Output:
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

Visualised as a grid:

```
           Column →  0    1    2
                   ┌────┬────┬────┐
          Row 0 →  │  1 │  2 │  3 │   ← matrix[0]
                   ├────┼────┼────┤
          Row 1 →  │  4 │  5 │  6 │   ← matrix[1]
                   ├────┼────┼────┤
          Row 2 →  │  7 │  8 │  9 │   ← matrix[2]
                   └────┴────┴────┘
```

Access items with **two levels of indexing** — first the row, then the column:

```python
# Grab the first row (index 0)
print(matrix[0])
```
```
# Output:
[1, 2, 3]
```

```python
# Grab the first item of the first row — row 0, column 0
print(matrix[0][0])
```
```
# Output:
1
```

```python
# Grab the last item of the last row — row 2, column 2
print(matrix[2][2])
```
```
# Output:
9
```

---

## 7. Introduction to List Comprehensions

List comprehensions are a compact way to build a new list from an existing one — all in a single line.

> Don't worry if this feels unfamiliar — we will return to this topic in much more detail later when we cover loops. For now, just read through the pattern.

**The pattern:**
```
[expression  for  item  in  list]
```

```python
# Without comprehension — the long way
first_col = []
for row in matrix:
    first_col.append(row[0])
print(first_col)
```
```
# Output:
[1, 4, 7]
```

```python
# With comprehension — the short way
first_col = [row[0] for row in matrix]
print(first_col)
```
```
# Output:
[1, 4, 7]
```

Both produce exactly the same result. The comprehension version is shorter and is the preferred Python style.

---

## Exercise: eCOMMart — Daily Sales Tracker

You are a sales analyst at **eCOMMart**, a B2B e-commerce marketplace. Write a program to record and analyse daily sales figures entered by the user.

**Instructions:**
- Start with an **empty list**
- Use `input()` to let the user enter sales amounts (₹) one by one
- Allow the user to type `done` to stop entering figures
- After input, display:
  - All daily sales figures
  - Total sales
  - Average daily sales
  - Best day (highest) and lowest day

**Hint:** Use `float()` to convert the input string to a number, and `len()`, `sum()`, `max()`, `min()` on your list.

```python
# write your code here
sales = []

while True:
    entry = input("Enter sales for the day (₹) or 'done' to finish: ")
    if entry == 'done':
        break
    sales.append(float(entry))

print()
print(f"Daily Sales   : {sales}")
print(f"Total Sales   : ₹{sum(sales):.2f}")
print(f"Average Sales : ₹{sum(sales) / len(sales):.2f}")
print(f"Best Day      : ₹{max(sales):.2f}")
print(f"Lowest Day    : ₹{min(sales):.2f}")
```

```
# Expected Output (with inputs 12500, 9800, 15200):
Enter sales for the day (₹) or 'done' to finish: 12500
Enter sales for the day (₹) or 'done' to finish: 9800
Enter sales for the day (₹) or 'done' to finish: 15200
Enter sales for the day (₹) or 'done' to finish: done

Daily Sales   : [12500.0, 9800.0, 15200.0]
Total Sales   : ₹37500.00
Average Sales : ₹12500.00
Best Day      : ₹15200.00
Lowest Day    : ₹9800.00
```
