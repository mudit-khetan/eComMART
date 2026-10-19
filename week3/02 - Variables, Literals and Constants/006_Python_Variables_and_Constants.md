# Python Variables and Constants

In this notebook you will learn about Python variables, constants, and the naming conventions that keep your code readable and professional.

**What we will cover:**

1. What is a variable?
2. Variable naming rules
3. Assigning values to variables
4. Multiple and chained assignment
5. Changing variable values
6. Constants
7. Naming conventions summary
8. Tasks

---

## 1. What is a Variable?

A variable is a **named location in memory** used to store data. Think of it as a label attached to a value — the value can be replaced at any time.

```python
number = 90
print(number)
```
```
# Output:
90
```

```python
# The value of number can be changed later
number = 9.1
print(number)
```
```
# Output:
9.1
```

> **Note:** Python is a **type-inferred** language — you never have to declare a variable's type. Python figures it out automatically. `number = 90` creates an integer; `number = 9.1` reassigns it as a float.

---

## 2. Variable Naming Rules

Python enforces these rules — break them and you get a `SyntaxError`:

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ Must start with a letter (A–Z, a–z) or underscore (_)   │
│  ✅ Can contain letters, digits (0–9), and underscores       │
│  ✅ Case-sensitive: price ≠ Price ≠ PRICE                    │
│  ❌ Cannot start with a digit                                │
│  ❌ Cannot contain spaces or special characters (!, @, #…)  │
│  ❌ Cannot be a Python keyword (if, for, while, True…)      │
└─────────────────────────────────────────────────────────────┘
```

**Valid variable names:**

```python
product_name
seller_city
price_1
_internal_code
year2024
is_in_stock
```

**Invalid variable names:**

```python
first-name      # hyphen not allowed
first@name      # @ not allowed
1product        # cannot start with a digit
product name    # no spaces
```

> **Python convention:** Use `snake_case` for variable names — all lowercase with underscores between words. For example: `product_name`, `seller_city`, `order_total`.

---

## 3. Assigning Values to Variables

Use the **`=`** assignment operator to store a value in a variable. This is not the same as the mathematical equals sign — it means "store this value":

```python
website = "github.com"
print(website)
```
```
# Output:
github.com
```

```python
# Reassign — now website points to a new value
website = "baidu.com"
print(website)
```
```
# Output:
baidu.com
```

### eCOMMart — a complete product variable block

```python
product_name = 'Wireless Mouse'
brand        = 'TechPro'
price        = 499.00
is_in_stock  = True
category     = 'Electronics'
seller_city  = 'Mumbai'

print('Product name:', product_name)
print('Product name length:', len(product_name))
print('Brand:', brand)
print('Price: ₹', price)
print('In Stock:', is_in_stock)
print('Category:', category)
print('Seller City:', seller_city)
```
```
# Output:
Product name: Wireless Mouse
Product name length: 14
Brand: TechPro
Price: ₹ 499.0
In Stock: True
Category: Electronics
Seller City: Mumbai
```

> `print()` accepts multiple arguments separated by commas:

```python
print('Hello', ',', 'World', '!')
```
```
# Output:
Hello , World !
```

---

## 4. Multiple and Chained Assignment

### Multiple values in one line

Assign several variables at once using commas:

```python
a, b, c = 6, 9.3, "Hello"
print(a)
print(b)
print(c)
```
```
# Output:
6
9.3
Hello
```

```python
# Separate statements on one line using semicolons
a = 1; b = 2; c = 3
print(a, b, c)
```
```
# Output:
1 2 3
```

### eCOMMart — unpack product fields in one line

```python
product_name, brand, category, price, is_in_stock = 'Wireless Mouse', 'TechPro', 'Electronics', 499.00, True

print(product_name, brand, category, price, is_in_stock)
print('Product name:', product_name)
print('Brand:', brand)
print('Category:', category)
print('Price: ₹', price)
print('In Stock:', is_in_stock)
```
```
# Output:
Wireless Mouse TechPro Electronics 499.0 True
Product name: Wireless Mouse
Brand: TechPro
Category: Electronics
Price: ₹ 499.0
In Stock: True
```

### Chained assignment — same value to multiple variables

```python
x = y = z = "same"
print(x)
print(y)
print(z)
```
```
# Output:
same
same
same
```

```python
p = q = r = 300
print(p, q, r)
```
```
# Output:
300 300 300
```

---

## 5. Changing Variable Values

A variable can be reassigned as many times as needed — even to a different type:

```python
website = "github.com"
print(website)

website = "baidu.com"   # reassigned to a new string
print(website)
```
```
# Output:
github.com
baidu.com
```

```python
n = 300
print(n)

m = n          # m now points to the same value as n
print(m)

m = 1000       # only m changes — n is unaffected
print(m)
```
```
# Output:
300
300
1000
```

```python
# A variable can even change type entirely
m = "Python is Fun"
m = 10          # now an integer
print(m)
```
```
# Output:
10
```

---

## 6. Constants

A **constant** is a variable whose value is intended never to change. Python does not technically enforce this, but the convention is to write constants in **ALL_CAPS_WITH_UNDERSCORES** — this signals to any developer: *do not change this value*.

### Convention — constants in the same file

```python
PI          = 3.14
GRAVITY     = 9.8
GST_RATE    = 0.18
MAX_CART    = 50
```

### Module pattern — constants in a separate file

For larger projects, constants are stored in their own module file:

**`constants.py`:**
```python
PI       = 3.14
GRAVITY  = 9.8
GST_RATE = 0.18
```

**`main.py`:**
```python
import constants

print(constants.PI)
print(constants.GRAVITY)
print(constants.GST_RATE)
```
```
# Output:
3.14
9.8
0.18
```

> **Note:** Python does not actually prevent you from reassigning a constant — it is a convention, not enforcement. Naming it in capitals is the developer's promise not to change it.

---

## 7. Naming Conventions Summary

```
┌─────────────────────────────────────────────────────────────────┐
│  Style          │  When to use               │  Example         │
├─────────────────────────────────────────────────────────────────┤
│  snake_case     │  Variables and functions    │  product_name    │
│  UPPER_SNAKE    │  Constants                  │  GST_RATE        │
│  CamelCase      │  Classes (covered later)    │  ProductCatalog  │
└─────────────────────────────────────────────────────────────────┘
```

**Case sensitivity — these are eight different variables:**

```python
age   = 1
Age   = 2
aGe   = 3
AGE   = 4
a_g_e = 5
_age  = 6
age_  = 7
AGe   = 8

print(age, Age, aGe, AGE, a_g_e, _age, age_, AGe)
```
```
# Output:
1 2 3 4 5 6 7 8
```

> **Good practice:** Never create variables that differ only by case in the same program — it is confusing to read and easy to get wrong.

---

## Tasks

### Task 1: eCOMMart — Product Variables

1. Write a Python comment: `# eCOMMart Product Catalog Entry`
2. Declare these variables and assign values:
   - `product_name` → `"Wireless Mouse"`
   - `brand` → `"TechPro"`
   - `price` → `499.00`
   - `is_in_stock` → `True`
3. Declare `category` and `seller_city` on the **same line** using comma unpacking
4. Print all variables with labels

```python
# Solution

# eCOMMart Product Catalog Entry
product_name = "Wireless Mouse"
brand        = "TechPro"
price        = 499.00
is_in_stock  = True
category, seller_city = "Electronics", "Mumbai"

print(f"  product_name : {product_name}")
print(f"  brand        : {brand}")
print(f"  price        : ₹{price:.2f}")
print(f"  is_in_stock  : {is_in_stock}")
print(f"  category     : {category}")
print(f"  seller_city  : {seller_city}")
```
```
# Expected Output:
  product_name : Wireless Mouse
  brand        : TechPro
  price        : ₹499.00
  is_in_stock  : True
  category     : Electronics
  seller_city  : Mumbai
```

---

### Task 2: eCOMMart — Price Calculations

Using the product variables from Task 1, perform the following:

1. Check the data type of `product_name`, `price`, and `is_in_stock` using `type()`
2. Find the character count of `product_name` using `len()`
3. Declare:
   - `price_1 = 499` (Wireless Mouse)
   - `price_2 = 350` (USB Hub)

   Calculate:
   - `total` = price_1 + price_2
   - `difference` = price_1 - price_2
   - `avg_price` = total / 2
   - `bulk_cost` = price_1 × 10 units
   - `remainder` = total % 100
   - `tax` = price_1 × 0.18 (18% GST)
   - `per_unit` = total // 2

4. Ask the user for a new product price using `input()`. Calculate and print the price after 20% discount.
5. Use `input()` to collect `product_name`, `category`, `seller_city`, and `price` for a new product, then print a formatted product card.

```python
# Solution

product_name = "Wireless Mouse"
price        = 499.00
is_in_stock  = True

print(f"type(product_name) : {type(product_name)}")
print(f"type(price)        : {type(price)}")
print(f"type(is_in_stock)  : {type(is_in_stock)}")
print(f"len(product_name)  : {len(product_name)}")

price_1 = 499
price_2 = 350
total      = price_1 + price_2
difference = price_1 - price_2
avg_price  = total / 2
bulk_cost  = price_1 * 10
remainder  = total % 100
tax        = price_1 * 0.18
per_unit   = total // 2

print(f"\nprice_1    = ₹{price_1}")
print(f"price_2    = ₹{price_2}")
print(f"total      = ₹{total}")
print(f"difference = ₹{difference}")
print(f"avg_price  = ₹{avg_price:.2f}")
print(f"bulk_cost  = ₹{bulk_cost}")
print(f"remainder  = {remainder}")
print(f"tax (18%)  = ₹{tax:.2f}")
print(f"per_unit   = ₹{per_unit}")

# Part 4 — input with 20% discount
new_price  = float(input("\nEnter a new product price (₹): "))
discounted = new_price * (1 - 0.20)
print(f"After 20% discount : ₹{discounted:.2f}")

# Part 5 — product card from input
product_name = input("\nEnter product name  : ")
category     = input("Enter category      : ")
seller_city  = input("Enter seller city   : ")
price        = float(input("Enter price (₹)     : "))

print("\n" + "=" * 40)
print("    eCOMMart — New Product Card")
print("=" * 40)
print(f"  Product  : {product_name}")
print(f"  Category : {category}")
print(f"  City     : {seller_city}")
print(f"  Price    : ₹{price:.2f}")
print("=" * 40)
```
```
# Expected Output (Parts 1–3, with price_1=499, price_2=350):
type(product_name) : <class 'str'>
type(price)        : <class 'float'>
type(is_in_stock)  : <class 'bool'>
len(product_name)  : 14

price_1    = ₹499
price_2    = ₹350
total      = ₹849
difference = ₹149
avg_price  = ₹424.50
bulk_cost  = ₹4990
remainder  = 49
tax (18%)  = ₹89.82
per_unit   = ₹424

# Expected Output (Part 4, with input 800):
Enter a new product price (₹): 800
After 20% discount : ₹640.00
```
