# For Loops, range(), break, continue, and pass

A `for` loop lets you repeat an action for every item in a sequence — a list, a tuple, a string, or a range of numbers. It is one of the most used constructs in Python.

> **Quick recap:** `if/elif/else` statements were covered in `017_If_elif_else`. This notebook builds on those — most loops contain conditions inside them.

**What we will cover:**

1. `for` loops — basic iteration
2. `range()` — generating number sequences
3. Iterating with index using `enumerate()`
4. `break` — stop a loop early
5. `continue` — skip to the next iteration
6. `pass` — do nothing (placeholder)
7. `continue` vs `pass` — the key difference
8. `for/else` — a rare but useful pattern
9. Tasks

---

## 1. `for` Loops — Basic Iteration

A `for` loop goes through every item in a sequence, one at a time:

```python
order_ids = ['ORD-1001', 'ORD-1002', 'ORD-1003']

for order in order_ids:
    print(order)
```
```
# Output:
ORD-1001
ORD-1002
ORD-1003
```

```
for  order  in  order_ids:
      ↑              ↑
  each item      the list
  one at a time
```

Works with any sequence — strings, tuples, sets:

```python
words = ['cat', 'window', 'defenestrate']

for w in words:
    print(w, len(w))
```
```
# Output:
cat 3
window 6
defenestrate 12
```

### Iterating a copy with `words[:]`

Using `words[:]` creates a **copy** of the list to iterate over, so you can safely modify the original inside the loop:

```python
words = ['cat', 'window', 'defenestrate']

for w in words[:]:          # iterate over a copy
    if len(w) > 6:
        words.insert(0, w)  # modify the original

print(words)
```
```
# Output:
['defenestrate', 'cat', 'window', 'defenestrate']
```

> `'defenestrate'` is 12 characters — it was inserted at the front of the original list. The copy being iterated is unaffected so the loop finishes normally. Iterating over `words` directly instead of `words[:]` could cause an infinite loop here.

---

## 2. `range()` — Generating Number Sequences

`range()` generates a sequence of numbers. It is **not a list** — it is a special object that produces numbers on demand (memory efficient). You can always convert it to a list with `list()`.

**Four forms of `range()`:**

```python
# range(stop) — 0 up to but not including stop
for i in range(5):
    print(i, end=' ')
```
```
# Output:
0 1 2 3 4
```

```python
# range(start, stop) — start up to but not including stop
for i in range(5, 10):
    print(i, end=' ')
```
```
# Output:
5 6 7 8 9
```

```python
# range(start, stop, step) — every nth number
for i in range(0, 10, 3):
    print(i, end=' ')
```
```
# Output:
0 3 6 9
```

```python
# range with negative step — counting backwards
for i in range(-10, -100, -30):
    print(i, end=' ')
```
```
# Output:
-10 -40 -70
```

```python
# range() is not a list
print(range(10))
```
```
# Output:
range(0, 10)
```

```python
# Convert to list when you need to see all values at once
print(list(range(5)))
```
```
# Output:
[0, 1, 2, 3, 4]
```

```
┌──────────────────────────────────────────────────────────┐
│  Form                  │  Example          │  Produces   │
├──────────────────────────────────────────────────────────┤
│  range(stop)           │  range(5)         │  0,1,2,3,4  │
│  range(start, stop)    │  range(2, 5)      │  2,3,4      │
│  range(start,stop,step)│  range(0, 10, 3)  │  0,3,6,9    │
│  range(start,stop,step)│  range(10, 0, -2) │  10,8,6,4,2 │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Iterating with Index using `enumerate()`

When you need both the **position** and the **value**, use `enumerate()` instead of `range(len(...))`:

```python
vendor_names = ['Tata Electronics', 'Reliance Digital', 'Infosys Supplies']

# The old way — works but verbose
for i in range(len(vendor_names)):
    print(i, vendor_names[i])
```
```
# Output:
0 Tata Electronics
1 Reliance Digital
2 Infosys Supplies
```

```python
# The better way — enumerate() gives index and value together
for i, vendor in enumerate(vendor_names):
    print(i, vendor)
```
```
# Output:
0 Tata Electronics
1 Reliance Digital
2 Infosys Supplies
```

```
enumerate(['Tata', 'Reliance', 'Infosys'])
    → (0, 'Tata'), (1, 'Reliance'), (2, 'Infosys')
```

---

## 4. `break` — Stop a Loop Early

`break` exits the loop immediately when a condition is met. Code after the `break` inside the loop is skipped:

```python
products = [
    ('Wireless Mouse', True),
    ('USB Hub', True),
    ('Laptop Stand', False),
    ('Smart Watch', True),
]

print("Scanning inventory...")
for name, in_stock in products:
    if not in_stock:
        print(f"First out-of-stock item found: {name}")
        break
    print(f"  {name} — in stock")
```
```
# Output:
Scanning inventory...
  Wireless Mouse — in stock
  USB Hub — in stock
First out-of-stock item found: Laptop Stand
```

```
Wireless Mouse → in_stock=True  → print, continue loop
USB Hub        → in_stock=True  → print, continue loop
Laptop Stand   → in_stock=False → print "First out-of-stock" → BREAK
Smart Watch    → never reached
```

---

## 5. `continue` — Skip to the Next Iteration

`continue` skips the **rest of the current iteration** and jumps straight to the next one. The loop does not stop:

```python
print("Processing available products:")
for name, in_stock in products:
    if not in_stock:
        print(f"  Skipping {name} — out of stock")
        continue
    print(f"  Processing {name}")
```
```
# Output:
Processing available products:
  Processing Wireless Mouse
  Processing USB Hub
  Skipping Laptop Stand — out of stock
  Processing Smart Watch
```

```
Wireless Mouse → in_stock=True  → skip the if → "Processing Wireless Mouse"
USB Hub        → in_stock=True  → skip the if → "Processing USB Hub"
Laptop Stand   → in_stock=False → "Skipping..." → continue → back to top
Smart Watch    → in_stock=True  → skip the if → "Processing Smart Watch"
```

---

## 6. `pass` — Do Nothing (Placeholder)

`pass` is a statement that does **absolutely nothing**. It is used when Python requires a statement syntactically — for example inside an empty function or class — but you have nothing to write yet:

```python
# Functions planned but not yet written
def process_refund(order_id):
    pass   # TODO: implement later

def send_notification(user_id):
    pass   # TODO: implement later

process_refund('ORD-1001')
send_notification('U-001')
print("Called successfully — pass does nothing")
```
```
# Output:
Called successfully — pass does nothing
```

```python
# Empty class as a placeholder
class BulkOrderProcessor:
    pass
```
```
# Output:
(no output — class created without error)
```

> **`pass` is not for skipping loop iterations.** It literally does nothing. If you want to skip to the next iteration, use `continue`.

---

## 7. `continue` vs `pass` — The Key Difference

This is one of the most commonly confused pairs in Python:

```python
flagged_orders = ['ORD-1001', 'ORD-1002', 'ORD-1003']

# continue — skips the rest of the loop body for that iteration
print("Using continue:")
for order in flagged_orders:
    if order == 'ORD-1002':
        continue              # jumps back to the top of the loop
    print(f"  Processing {order}")
```
```
# Output:
Using continue:
  Processing ORD-1001
  Processing ORD-1003
```

```python
# pass — does nothing, the rest of the loop body still runs
print("\nUsing pass:")
for order in flagged_orders:
    if order == 'ORD-1002':
        pass                  # does nothing — execution continues below
    print(f"  Processing {order}")
```
```
# Output:
Using pass:
  Processing ORD-1001
  Processing ORD-1002
  Processing ORD-1003
```

```
┌───────────┬────────────────────────────────────────────────┐
│ Statement │ What happens                                   │
├───────────┼────────────────────────────────────────────────┤
│ continue  │ Skips the rest of the loop body this iteration │
│           │ Jumps back to the top for the next item        │
├───────────┼────────────────────────────────────────────────┤
│ pass      │ Does absolutely nothing                        │
│           │ Code below it in the same block still runs     │
├───────────┼────────────────────────────────────────────────┤
│ break     │ Exits the loop entirely                        │
│           │ No more iterations happen                      │
└───────────┴────────────────────────────────────────────────┘
```

---

## 8. `for/else` — A Rare but Useful Pattern

A `for` loop can have an `else` clause. The `else` block runs **only if the loop completed without hitting a `break`**. If `break` was triggered, the `else` is skipped:

```python
order_amounts = [12500, 45000, 8750, 62000, 31500]
target = 62000

print(f"Searching for order ₹{target}...")
for amount in order_amounts:
    if amount == target:
        print(f"Found: ₹{amount}")
        break
else:
    print("Order not found in records.")
```
```
# Output:
Searching for order ₹62000...
Found: ₹62000
```

```python
target = 99999

print(f"Searching for order ₹{target}...")
for amount in order_amounts:
    if amount == target:
        print(f"Found: ₹{amount}")
        break
else:
    print("Order not found in records.")
```
```
# Output:
Searching for order ₹99999...
Order not found in records.
```

```
for ... in ...:
    if found:
        break       ← break fires → else is SKIPPED
else:
    ...             ← only runs if NO break happened
```

**Classic use — finding prime numbers:**

```python
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop finished without finding a factor → it's prime
        print(n, 'is a prime number')
```
```
# Output:
2 is a prime number
3 is a prime number
4 equals 2 * 2
5 is a prime number
6 equals 2 * 3
7 is a prime number
8 equals 2 * 4
9 equals 3 * 3
```

---

## Tasks

### Task 1: Number Search in a List

Search for a number in a list. Stop as soon as it is found. If not found after checking all items, say so.

**Instructions:**
- Create `numbers = [10, 20, 30, 40, 50]`
- Ask the user to input a number
- Use a `for` loop with `break` to search
- Use `for/else` to handle the not-found case

```python
numbers = [10, 20, 30, 40, 50]
target = int(input("Enter the number to search: "))

print(f"List: {numbers}")

for num in numbers:
    if num == target:
        print(f"{target} is found in the list.")
        break
else:
    print(f"{target} is not in the list.")
```
```
# Expected Output (with input 30):
List: [10, 20, 30, 40, 50]
Enter the number to search: 30
30 is found in the list.

# Expected Output (with input 99):
List: [10, 20, 30, 40, 50]
Enter the number to search: 99
99 is not in the list.
```

---

### Task 2: Iterate Through a List, Skipping a Word

Print every word in a list, but skip the word `"skip"`.

**Instructions:**
- Create `words = ["apple", "banana", "skip", "cherry", "date"]`
- Use a `for` loop with `continue` to skip `"skip"`
- Print all other words

```python
words = ["apple", "banana", "skip", "cherry", "date"]

print("Words in the list:")
for word in words:
    if word == "skip":
        continue
    print(word)
```
```
# Expected Output:
Words in the list:
apple
banana
cherry
date
```

> **Note:** `continue` is the correct statement here — not `pass`. `pass` would do nothing and `"skip"` would still be printed. `continue` skips the `print(word)` line for that iteration.
