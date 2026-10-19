# Python Operators

Operators are special **symbols** that carry out arithmetic or logical computation. The value the operator acts on is called the **operand**.

```python
print(6 + 3)
```
```
# Output:
9
```

Here `+` is the operator, `6` and `3` are the operands, and `9` is the result.

**What we will cover:**

1. Arithmetic Operators
2. Comparison Operators
3. Logical / Boolean Operators
4. Assignment Operators
5. Identity Operators
6. Membership Operators
7. Bitwise Operators
8. Tasks

---

## 1. Arithmetic Operators

Used to perform standard mathematical operations.

```
┌────────┬──────────────────────┬──────────────────────────────────────┐
│ Symbol │ Operation            │ Example                              │
├────────┼──────────────────────┼──────────────────────────────────────┤
│   +    │ Addition             │ 3 + 2  → 5                           │
│   -    │ Subtraction          │ 3 - 2  → 1                           │
│   *    │ Multiplication       │ 3 * 2  → 6                           │
│   /    │ Division (float)     │ 7 / 2  → 3.5  (always a float)       │
│   //   │ Floor division       │ 7 // 2 → 3    (drops the decimal)    │
│   %    │ Modulus (remainder)  │ 7 % 2  → 1                           │
│   **   │ Exponentiation       │ 3 ** 2 → 9    (3 to the power 2)     │
└────────┴──────────────────────┴──────────────────────────────────────┘
```

```python
print('Addition: ', 1 + 2)
print('Subtraction: ', 2 - 1)
print('Multiplication: ', 2 * 3)
print('Division (always float): ', 7 / 2)
print('Floor division: ', 7 // 2)
print('Modulus: ', 7 % 2)
print('Exponent: ', 3 ** 2)
```
```
# Output:
Addition:  3
Subtraction:  1
Multiplication:  6
Division (always float):  3.5
Floor division:  3
Modulus:  1
Exponent:  9
```

> **Key distinction — `/` vs `//`:**
> - `/` always returns a **float**: `7 / 2 → 3.5`
> - `//` floors to the nearest whole number: `7 // 2 → 3`

```python
x = 16
y = 3

print('x + y =', x + y)
print('x - y =', x - y)
print('x * y =', x * y)
print('x / y =', round(x / y, 3))
print('x // y =', x // y)
print('x % y =', x % y)
print('x ** y =', x ** y)
```
```
# Output:
x + y = 19
x - y = 13
x * y = 48
x / y = 5.333
x // y = 5
x % y = 1
x ** y = 4096
```

```python
print(5 // 6)    # 5 does not divide into 6 even once → 0
print(5 // 6.0)  # same result, but float because one operand is float
print(15 % 10)   # 15 divided by 10 leaves remainder 5
print(3 ** 2)    # 3 to the power of 2 = 3 × 3
```
```
# Output:
0
0.0
5
9
```

### B2B eCom — Arithmetic in Practice

**Calculating GST and final price:**

```python
price    = 1299.00
gst_rate = 0.18

gst   = price * gst_rate
final = price + gst

print(f"Price    : ₹{price:.2f}")
print(f"GST (18%): ₹{gst:.2f}")
print(f"Final    : ₹{final:.2f}")
```
```
# Output:
Price    : ₹1299.00
GST (18%): ₹233.82
Final    : ₹1532.82
```

**Calculating revenue and average order value:**

```python
qty        = 50
unit_price = 499

revenue = qty * unit_price
print(f"Revenue: ₹{revenue}")
```
```
# Output:
Revenue: ₹24950
```

```python
total = 1500
items = 4

avg = total / items
print(f"Average order value: ₹{avg:.2f}")
```
```
# Output:
Average order value: ₹375.00
```

**Shipping cost using floor division and modulus:**

```python
weight = 3.5   # kg

shipping = 50 + (weight - 1) * 30
print(f"Shipping for {weight}kg: ₹{shipping:.2f}")
```
```
# Output:
Shipping for 3.5kg: ₹125.00
```

---

## 2. Comparison Operators


Comparison operators compare two values and always return a **Boolean** — either `True` or `False`.

```
┌────────┬───────────────────────────┬─────────────┐
│ Symbol │ Meaning                   │ Example      │
├────────┼───────────────────────────┼─────────────┤
│   >    │ Greater than              │ 6 > 3  → True │
│   <    │ Less than                 │ 6 < 3  → False│
│   ==   │ Equal to                  │ 6 == 6 → True │
│   !=   │ Not equal to              │ 6 != 3 → True │
│   >=   │ Greater than or equal to  │ 6 >= 6 → True │
│   <=   │ Less than or equal to     │ 3 <= 6 → True │
└────────┴───────────────────────────┴─────────────┘
```

> **Important:** `==` tests equality. `=` assigns a value. These are not the same.

```python
print(6 > 3)
print(6 >= 3)
print(6 < 3)
print(6 == 3)
print(6 != 3)
```
```
# Output:
True
True
False
False
True
```

```python
x = 30
y = 22

print('x > y is',  x > y)
print('x < y is',  x < y)
print('x == y is', x == y)
print('x != y is', x != y)
print('x >= y is', x >= y)
print('x <= y is', x <= y)
```
```
# Output:
x > y is True
x < y is False
x == y is False
x != y is True
x >= y is True
x <= y is False
```

**Chained comparisons** — Python lets you chain comparisons naturally:

```python
z = 3

print('z == 3:', z == 3)
print('0.5 < z <= 5:', 0.5 < z <= 5)   # True — z is between 0.5 and 5
print('0.5 < z <= 1:', 0.5 < z <= 1)   # False — z is 3, not ≤ 1
```
```
# Output:
z == 3: True
0.5 < z <= 5: True
0.5 < z <= 1: False
```

### B2B eCom — Comparison in Practice

```python
cart = 1500

print('cart > 1000:', cart > 1000)
print('cart >= 1500:', cart >= 1500)
print('cart == 2000:', cart == 2000)
print('cart != 500:', cart != 500)
```
```
# Output:
cart > 1000: True
cart >= 1500: True
cart == 2000: False
cart != 500: True
```

---

## 3. Logical / Boolean Operators


Logical operators combine multiple conditions. They return `True` or `False`.

```
┌─────────┬────────────────────────────────────────────────────┐
│ Symbol  │ Meaning                                            │
├─────────┼────────────────────────────────────────────────────┤
│   and   │ True only if BOTH conditions are True              │
│   or    │ True if AT LEAST ONE condition is True             │
│   not   │ Flips the result — True becomes False, vice versa  │
└─────────┴────────────────────────────────────────────────────┘
```

```python
print(True and True)    # both True → True
print(True and False)   # one False → False
print(False and False)  # both False → False
print(True or False)    # at least one True → True
print(False or False)   # neither True → False
print(not True)         # flips → False
print(not False)        # flips → True
```
```
# Output:
True
False
False
True
False
False
True
```

**Truth table:**

```
┌───────┬───────┬───────────┬──────────┐
│   A   │   B   │  A and B  │  A or B  │
├───────┼───────┼───────────┼──────────┤
│ True  │ True  │   True    │  True    │
│ True  │ False │   False   │  True    │
│ False │ True  │   False   │  True    │
│ False │ False │   False   │  False   │
└───────┴───────┴───────────┴──────────┘
```

### B2B eCom — Logical operators in Practice

```python
in_stock          = True
payment_confirmed = True
express_zone      = False

print('Can ship:', in_stock and payment_confirmed)
print('Express eligible:', in_stock and payment_confirmed and express_zone)
print('Any issue:', not in_stock or not payment_confirmed)
```
```
# Output:
Can ship: True
Express eligible: False
Any issue: False
```

**Combining all three operators:**

```python
x = True
y = False

print('x and y is', x and y)
print('x or y is',  x or y)
print('not x is',   not x)
```
```
# Output:
x and y is False
x or y is True
not x is False
```

**Evaluating a complex expression step by step:**

```python
result = True and (not(not False)) or (True and (not True))
print(result)
```
```
# Output:
False
```

```
Step 1: not False        → True
Step 2: not True         → False   (the inner not(not False))
Step 3: True and False   → False   (left side of or)
Step 4: not True         → False
Step 5: True and False   → False   (right side of or)
Step 6: False or False   → False   ← final result
```

---

## 4. Assignment Operators

Assignment operators assign a value to a variable. Compound operators combine an operation with assignment in one step.

```
┌────────┬───────────────┬────────────────────┐
│ Symbol │ Example       │ Equivalent to       │
├────────┼───────────────┼────────────────────┤
│   =    │ x = 5         │ x = 5              │
│   +=   │ x += 5        │ x = x + 5          │
│   -=   │ x -= 5        │ x = x - 5          │
│   *=   │ x *= 5        │ x = x * 5          │
│   /=   │ x /= 5        │ x = x / 5          │
│   //=  │ x //= 5       │ x = x // 5         │
│   %=   │ x %= 5        │ x = x % 5          │
│   **=  │ x **= 5       │ x = x ** 5         │
└────────┴───────────────┴────────────────────┘
```

```python
x = 10
print(f"x = {x}")

x += 5
print(f"x += 5  → {x}")

x -= 3
print(f"x -= 3  → {x}")

x *= 2
print(f"x *= 2  → {x}")

x /= 4
print(f"x /= 4  → {x}")
```
```
# Output:
x = 10
x += 5  → 15
x -= 3  → 12
x *= 2  → 24
x /= 4  → 6.0
```

```python
x = 10
x //= 3
print(f"x //= 3 → {x}")

x = 10
x %= 3
print(f"x %= 3  → {x}")

x = 2
x **= 4
print(f"x **= 4 → {x}")
```
```
# Output:
x //= 3 → 3
x %= 3  → 1
x **= 4 → 16
```

### B2B eCom — Building a Cart Total

```python
cart_total = 500
print(f"cart_total = ₹{cart_total}")

cart_total += 299
print(f"add item ₹299  → ₹{cart_total}")

cart_total += 149
print(f"add item ₹149  → ₹{cart_total}")

cart_total -= 50
print(f"remove item ₹50 → ₹{cart_total}")
```
```
# Output:
cart_total = ₹500
add item ₹299  → ₹799
add item ₹149  → ₹948
remove item ₹50 → ₹898
```

---

## 5. Identity Operators

Identity operators check whether two variables point to the **same object in memory** — not just whether they have the same value.

```
┌──────────┬──────────────────────────────────────────────────┐
│ Symbol   │ Meaning                                          │
├──────────┼──────────────────────────────────────────────────┤
│ is       │ True if both variables refer to the same object  │
│ is not   │ True if they refer to different objects          │
└──────────┴──────────────────────────────────────────────────┘
```

> **`==` vs `is`:**
> - `==` checks if the **values** are equal
> - `is` checks if they are the **exact same object** in memory

```python
a = 'Tata Electronics'
b = 'Tata Electronics'
c = 'Reliance Digital'

print('a is b:', a is b)        # True — Python reuses same string object
print('a is c:', a is c)        # False — different strings
print('a is not c:', a is not c) # True
```
```
# Output:
a is b: True
a is c: False
a is not c: True
```

**Lists with the same content are NOT the same object:**

```python
x3 = [1, 2, 3]
y3 = [1, 2, 3]

print('x3 == y3:', x3 == y3)  # True  — same values
print('x3 is y3:', x3 is y3)  # False — different objects in memory
```
```
# Output:
x3 == y3: True
x3 is y3: False
```

```python
# Assigning one variable to another makes them the SAME object
z3 = x3
print('z3 is x3:', z3 is x3)  # True — z3 and x3 are the same object
```
```
# Output:
z3 is x3: True
```

```
x3 = [1,2,3]  ──┐
                 ├──→ same object in memory
z3 = x3       ──┘

y3 = [1,2,3]  ──→ different object (equal values, different location)
```

---

## 6. Membership Operators

Membership operators test whether a value exists **within a sequence** (string, list, tuple, set, or dictionary).

```
┌──────────┬──────────────────────────────────────────┐
│ Symbol   │ Meaning                                  │
├──────────┼──────────────────────────────────────────┤
│ in       │ True if value is found in the sequence   │
│ not in   │ True if value is NOT found               │
└──────────┴──────────────────────────────────────────┘
```

**Checking substrings in a product name:**

```python
product_name = 'Wireless Bluetooth Mouse'

print('Wireless' in product_name)
print('Keyboard' in product_name)
print('keyboard' not in product_name)   # case sensitive
```
```
# Output:
True
False
True
```

**Checking items in a list:**

```python
categories = ['Electronics', 'Clothing', 'Furniture', 'Sports']

print('Electronics' in categories)
print('Books' not in categories)
```
```
# Output:
True
True
```

**Checking keys in a dictionary:**

> In a dictionary, `in` checks for **keys only**, not values.

```python
vendor_dict = {'V001': 'Tata Electronics', 'V002': 'Reliance Digital'}

print('V001' in vendor_dict)   # True  — V001 is a key
print('V003' in vendor_dict)   # False — V003 not a key
```
```
# Output:
True
False
```

---

## 7. Bitwise Operators

Bitwise operators work on numbers at the binary (bit) level. Each bit is either 0 or 1, and the operator is applied position by position.

```
┌────────┬─────────────┬──────────────────────────────────────────┐
│ Symbol │ Operation   │ What it does                             │
├────────┼─────────────┼──────────────────────────────────────────┤
│   &    │ AND         │ 1 only where BOTH bits are 1             │
│   |    │ OR          │ 1 where EITHER bit is 1                  │
│   ^    │ XOR         │ 1 where bits are DIFFERENT               │
│   ~    │ NOT         │ Flips all bits (result = -(n+1))         │
│  <<    │ Left shift  │ Shifts bits left, multiplies by 2        │
│  >>    │ Right shift │ Shifts bits right, divides by 2          │
└────────┴─────────────┴──────────────────────────────────────────┘
```

```python
a = 5   # binary: 101
b = 3   # binary: 011

print(f"a = {a}  ({bin(a)})")
print(f"b = {b}  ({bin(b)})")

print(f"a & b  = {a & b}   ({bin(a & b)})   AND — 1 only where both are 1")
print(f"a | b  = {a | b}   ({bin(a | b)})   OR  — 1 where either is 1")
print(f"a ^ b  = {a ^ b}   ({bin(a ^ b)})   XOR — 1 where bits differ")
print(f"~a     = {~a}          NOT — flips all bits")
print(f"a << 1 = {a << 1}  ({bin(a << 1)})  left shift  — same as × 2")
print(f"a >> 1 = {a >> 1}   ({bin(a >> 1)})    right shift — same as // 2")
```
```
# Output:
a = 5  (0b101)
b = 3  (0b11)
a & b  = 1   (0b1)    AND — 1 only where both are 1
a | b  = 7   (0b111)  OR  — 1 where either is 1
a ^ b  = 6   (0b110)  XOR — 1 where bits differ
~a     = -6           NOT — flips all bits
a << 1 = 10  (0b1010) left shift  — same as × 2
a >> 1 = 2   (0b10)   right shift — same as // 2
```

```
a = 5 → 1 0 1
b = 3 → 0 1 1
        ─────
a & b → 0 0 1 = 1   (AND: 1 only where both are 1)
a | b → 1 1 1 = 7   (OR:  1 where at least one is 1)
a ^ b → 1 1 0 = 6   (XOR: 1 where they differ)

a << 1 → 1 0 1 0 = 10  (shift left = multiply by 2)
a >> 1 →   1 0   =  2  (shift right = divide by 2)
```

> **When are bitwise operators used in practice?** Mainly in systems programming, permission flags, and low-level data processing — not in everyday application code.

---

## Tasks

### Task 1: eCOMMart — GST Calculator

Write a program that asks the user to enter the price of an item and calculates the GST and final price.

- GST rate = 18%
- Final price = price + (price × 0.18)

```python
price = float(input("Enter item price (₹): "))

gst   = price * 0.18
final = price + gst

print(f"GST (18%)   : ₹{gst:.2f}")
print(f"Final Price : ₹{final:.2f}")
```
```
# Expected Output (with input 500):
Enter item price (₹): 500
GST (18%)   : ₹90.00
Final Price : ₹590.00
```

---

### Task 2: eCOMMart — Shipping Cost Calculator

eCOMMart charges shipping based on total weight:
- First 1 kg: ₹50
- Every additional kg: ₹30

```python
weight = float(input("Enter shipment weight (kg): "))

if weight <= 1:
    cost = 50
else:
    cost = 50 + (weight - 1) * 30

print(f"Shipping Cost: ₹{cost:.2f}")
```
```
# Expected Output (with input 3.5):
Enter shipment weight (kg): 3.5
Shipping Cost: ₹125.00
```

---

### Task 3: eCOMMart — Revenue from 5 Products

Ask the user to enter the price and quantity sold for 5 products. Calculate revenue per product and total revenue.

```python
total_revenue = 0

for i in range(1, 6):
    price = float(input(f"Enter price of product {i}: "))
    qty   = int(input(f"Enter quantity sold: "))
    rev   = price * qty
    print(f"  Revenue: ₹{rev:.2f}")
    total_revenue += rev

print(f"\nTotal Revenue: ₹{total_revenue:.2f}")
```
```
# Expected Output (sample inputs):
Enter price of product 1: 499
Enter quantity sold: 10
  Revenue: ₹4990.00
Enter price of product 2: 799
Enter quantity sold: 5
  Revenue: ₹3995.00
...
Total Revenue: ₹XXXXX.XX
```


---

## Python Operators — Quick Reference

Operators are special symbols that perform operations on values and variables.

### Arithmetic Operators
| Operator | Name | Example | Result |
|:---:|---|---|---|
| `+` | Addition | `10 + 3` | `13` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `10 * 3` | `30` |
| `/` | Division | `10 / 3` | `3.333...` |
| `//` | Floor Division | `10 // 3` | `3` |
| `%` | Modulus (Remainder) | `10 % 3` | `1` |
| `**` | Exponentiation | `2 ** 8` | `256` |

### Comparison Operators
| Operator | Meaning | Example | Result |
|:---:|---|---|---|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `3 <= 5` | `True` |

### Assignment Operators
| Operator | Example | Equivalent to |
|:---:|---|---|
| `=` | `x = 10` | Assign 10 to x |
| `+=` | `x += 3` | `x = x + 3` |
| `-=` | `x -= 3` | `x = x - 3` |
| `*=` | `x *= 3` | `x = x * 3` |
| `/=` | `x /= 3` | `x = x / 3` |
| `//=` | `x //= 3` | `x = x // 3` |
| `%=` | `x %= 3` | `x = x % 3` |
| `**=` | `x **= 3` | `x = x ** 3` |

### Logical Operators
| Operator | Meaning | Example | Result |
|:---:|---|---|---|
| `and` | True if both are True | `True and False` | `False` |
| `or` | True if at least one is True | `True or False` | `True` |
| `not` | Reverses the boolean | `not True` | `False` |

### Membership Operators
| Operator | Meaning | Example |
|:---:|---|---|
| `in` | True if value is in sequence | `"a" in "apple"` → `True` |
| `not in` | True if value is NOT in sequence | `5 not in [1,2,3]` → `True` |

### Identity Operators
| Operator | Meaning | Example |
|:---:|---|---|
| `is` | True if both refer to same object | `x is None` |
| `is not` | True if they refer to different objects | `x is not None` |

### Bitwise Operators
| Operator | Name | Example |
|:---:|---|---|
| `&` | AND | `6 & 3` → `2` |
| `\|` | OR | `6 \| 3` → `7` |
| `^` | XOR | `6 ^ 3` → `5` |
| `~` | NOT | `~6` → `-7` |
| `<<` | Left Shift | `6 << 1` → `12` |
| `>>` | Right Shift | `6 >> 1` → `3` |

### Operator Precedence (Grouping)
Python evaluates expressions in this order (highest to lowest):

| Priority | Operator(s) | Description |
|:---:|---|---|
| 1 | `()` | Parentheses — always evaluated first |
| 2 | `**` | Exponentiation |
| 3 | `+x`, `-x`, `~x` | Unary operators |
| 4 | `*`, `/`, `//`, `%` | Multiplication, Division |
| 5 | `+`, `-` | Addition, Subtraction |
| 6 | `<<`, `>>` | Bitwise shifts |
| 7 | `&` | Bitwise AND |
| 8 | `^` | Bitwise XOR |
| 9 | `\|` | Bitwise OR |
| 10 | `==`, `!=`, `>`, `<`, `>=`, `<=`, `is`, `in` | Comparisons |
| 11 | `not` | Logical NOT |
| 12 | `and` | Logical AND |
| 13 | `or` | Logical OR |

> **Tip:** When in doubt, use `()` parentheses to make your intent explicit.
> `2 + 3 * 4` = `14` but `(2 + 3) * 4` = `20`