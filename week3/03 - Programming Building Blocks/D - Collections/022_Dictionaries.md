# Dictionaries — eComMart B2B Marketplace

A **dictionary** stores information as **key–value pairs**. Each key identifies a value, so you can look up a product's price or stock quantity by using a meaningful name instead of a numeric position.

In this lesson, we will use dictionaries to manage eComMart products, suppliers, and orders. Examples are designed for someone who is **new to programming** and is working in **VS Code**.

### Before you begin

- **Code** is a set of instructions that you write for the computer.
- A **variable** is a name that stores a value. In `product = {}`, the variable is named `product`.
- Text values go inside quotation marks, such as `"Wireless Mouse"`. Numbers such as `850` do not need quotation marks.
- The `=` sign stores the value on the right in the variable or dictionary field on the left. It does not mean “is equal to” in the same way it is used in ordinary writing.
- `print(...)` asks Python to display information in the terminal.
- The **output** shown after each example is what you should see after running that code, assuming you copy it exactly.

**How to try an example in VS Code:** Open a folder, create a file named `dictionary_practice.py`, type or paste one complete example into the file, save it, and run the Python file. If you are new to VS Code, make sure Python is installed and the Python extension is available. Run examples one at a time unless the instructions say to run them together.

## What we will cover

1. Creating dictionaries
2. Understanding keys and values
3. Accessing values by key
4. Adding and updating entries
5. Retrieving values safely with `get()`
6. Checking whether a key exists with `in`
7. Removing entries with `pop()` and `del`
8. Useful dictionary methods
9. Dictionaries containing lists
10. Nesting dictionaries
11. Lists containing dictionaries
12. Exercises: eComMart product catalogue and order lookup

---

## 1. Creating Dictionaries

Use curly braces `{}` to create a dictionary. Put a colon `:` between each key and its value, and separate pairs with commas.

### An empty dictionary

```python
# Start with an empty product catalogue
product = {}
print(product)
```

**Output**
```text
{}
```

### A dictionary with product details

```python
product = {
    "product_id": "SKU101",
    "name": "Wireless Mouse",
    "price": 850,
    "stock": 120
}
print(product)
```

**Output**
```text
{'product_id': 'SKU101', 'name': 'Wireless Mouse', 'price': 850, 'stock': 120}
```

A dictionary can contain strings, integers, decimals, Boolean values, lists, and even other dictionaries. In this example, keys are strings and values include both strings and numbers.

### Visual: one key points to one value

```text
product
┌────────────────┬──────────────────┐
│ Key            │ Value            │
├────────────────┼──────────────────┤
│ "product_id"   │ "SKU101"         │
│ "name"         │ "Wireless Mouse" │
│ "price"        │ 850              │
│ "stock"        │ 120              │
└────────────────┴──────────────────┘
```

**Remember:** Keys should be unique. If the same key is written more than once in a dictionary literal, the last value for that key is the one kept.

---

## 2. Understanding Keys and Values

- A **key** is the label used to look up information, such as `"price"`.
- A **value** is the information stored under that key, such as `850`.
- A dictionary uses keys, not numbered positions, to access its values.

```python
product = {
    "product_id": "SKU101",
    "name": "Wireless Mouse",
    "price": 850,
    "stock": 120
}

print(product.keys())
print(product.values())
```

**Output**
```text
dict_keys(['product_id', 'name', 'price', 'stock'])
dict_values(['SKU101', 'Wireless Mouse', 850, 120])
```

The output shows the keys and values in insertion order—the order in which they were added.

---

## 3. Accessing Values by Key

Use square brackets with a key to retrieve its value: `dictionary["key"]`.

```python
product = {
    "product_id": "SKU101",
    "name": "Wireless Mouse",
    "price": 850,
    "stock": 120
}

print(product["name"])
print(product["price"])
print(product["stock"])
```

**Output**
```text
Wireless Mouse
850
120
```

### Dictionary keys are not list indexes

In a list, `products[0]` means “get the first item.” In a dictionary, `product["name"]` means “get the value stored under the key `name`.”

```python
product = {"name": "Wireless Mouse", "price": 850}
print(product["name"])
```

**Output**
```text
Wireless Mouse
```

If you use a key that does not exist with square brackets, Python raises a `KeyError`. The next section shows a safer way to retrieve a value when a key might be missing.

---

## 4. Adding and Updating Entries

Use assignment to add a new key or change the value of an existing key.

### Add a new field

```python
product = {"product_id": "SKU101", "name": "Wireless Mouse"}
print(product)

product["category"] = "Computer Accessories"
print(product)
```

**Output**
```text
{'product_id': 'SKU101', 'name': 'Wireless Mouse'}
{'product_id': 'SKU101', 'name': 'Wireless Mouse', 'category': 'Computer Accessories'}
```

### Update an existing value

```python
product = {"name": "Wireless Mouse", "stock": 120}
print(product)

product["stock"] = 170
print(product)
```

**Output**
```text
{'name': 'Wireless Mouse', 'stock': 120}
{'name': 'Wireless Mouse', 'stock': 170}
```

### Increase stock using `+=`

```python
product = {"name": "Laptop Stand", "stock": 80}
print(product)

product["stock"] += 50
print(product)
```

**Output**
```text
{'name': 'Laptop Stand', 'stock': 80}
{'name': 'Laptop Stand', 'stock': 130}
```

### Visual: before and after an update

```text
Before: "stock" ──> 80
                  │
          add 50  ▼
After:  "stock" ──> 130
```

`+= 50` means “take the current value, add 50, and save the result back under the same key.”

---

## 5. Retrieving Values Safely with `get()`

`get()` retrieves a value by key. If the key does not exist, it returns `None` by default instead of raising a `KeyError`. You can also provide a default value.

```python
product = {"product_id": "SKU101", "name": "Wireless Mouse", "stock": 120}

print(product.get("name"))
print(product.get("price"))
print(product.get("price", 0))
```

**Output**
```text
Wireless Mouse
None
0
```

The `"price"` key is missing. The second call returns `None`; the third returns the default value `0`.

### Use `get()` with a simple `if-else`

```python
product = {"product_id": "SKU101", "name": "Wireless Mouse", "stock": 120}
price = product.get("price")

if price is None:
    print("Price is not available")
else:
    print("Price: ₹", price)
```

**Output**
```text
Price is not available
```

This example uses `if-else` to respond to missing information. It does not use exception handling.

---

## 6. Checking Whether a Key Exists with `in`

Use `in` to check whether a key is present. The result is `True` or `False`.

```python
product = {"product_id": "SKU101", "name": "Wireless Mouse", "stock": 120}

print("stock" in product)
print("price" in product)
```

**Output**
```text
True
False
```

You can use the check before accessing a value.

```python
product = {"product_id": "SKU101", "name": "Wireless Mouse", "stock": 120}

if "stock" in product:
    print("Available stock:", product["stock"])
else:
    print("Stock information is missing")
```

**Output**
```text
Available stock: 120
```

**Important:** `"stock" in product` checks whether `"stock"` is a key in the dictionary. It does not check whether `120` is one of the values.

---

## 7. Removing Entries

Use `pop(key)` to remove a key and return its value. Use `del` to delete a key when you do not need the returned value.

### Remove an entry with `pop()`

```python
product = {"name": "USB Hub", "price": 1200, "stock": 45}
print(product)

removed_stock = product.pop("stock")
print("Removed stock value:", removed_stock)
print(product)
```

**Output**
```text
{'name': 'USB Hub', 'price': 1200, 'stock': 45}
Removed stock value: 45
{'name': 'USB Hub', 'price': 1200}
```

### Remove an entry with `del`

```python
product = {"name": "USB Hub", "price": 1200, "stock": 45}
del product["price"]
print(product)
```

**Output**
```text
{'name': 'USB Hub', 'stock': 45}
```

Use `pop()` when you also need the removed value. Both `pop()` and `del` require the key to exist in these examples; use a key check or `get()` when working with potentially missing information.

---

## 8. Useful Dictionary Methods

Start with this sample dictionary:

```python
product = {"product_id": "SKU101", "name": "Wireless Mouse", "stock": 120}
print(product)
```

**Output**
```text
{'product_id': 'SKU101', 'name': 'Wireless Mouse', 'stock': 120}
```

### `keys()` — get the keys

```python
print(product.keys())
```

**Output**
```text
dict_keys(['product_id', 'name', 'stock'])
```

### `values()` — get the values

```python
print(product.values())
```

**Output**
```text
dict_values(['SKU101', 'Wireless Mouse', 120])
```

### `items()` — get key–value pairs

```python
print(product.items())
```

**Output**
```text
dict_items([('product_id', 'SKU101'), ('name', 'Wireless Mouse'), ('stock', 120)])
```

Each pair is shown as a tuple, written with parentheses. Tuples will be covered separately.

### `update()` — add or change multiple entries

```python
product = {"name": "Wireless Mouse", "stock": 120}
print(product)

product.update({"stock": 150, "price": 850})
print(product)
```

**Output**
```text
{'name': 'Wireless Mouse', 'stock': 120}
{'name': 'Wireless Mouse', 'stock': 150, 'price': 850}
```

`update()` changes `"stock"` and adds `"price"`.

### `clear()` — remove all entries

```python
product = {"name": "Wireless Mouse", "stock": 120}
print(product)

product.clear()
print(product)
```

**Output**
```text
{'name': 'Wireless Mouse', 'stock': 120}
{}
```

`clear()` empties the dictionary. The variable still refers to an empty dictionary.

### Quick reference

| Method | What it does |
|---|---|
| `get(key)` | Retrieves a value; can return a default if the key is missing |
| `keys()` | Provides the dictionary's keys |
| `values()` | Provides the dictionary's values |
| `items()` | Provides key–value pairs |
| `update(other)` | Adds or updates entries |
| `pop(key)` | Removes a key and returns its value |
| `clear()` | Removes all entries |

---

## 9. Dictionaries Containing Lists

A **list** stores several items in a particular order. A list uses square brackets `[]`, and commas separate its items. For example, `"USB-C Hub"` and `"Laptop Stand"` are two text items in this list:

```python
product_names = ["USB-C Hub", "Laptop Stand"]
print(product_names)
```

**Output**
```text
['USB-C Hub', 'Laptop Stand']
```

A dictionary can store a list as the value for one of its keys. This is useful when one product has several categories, compatible devices, or warehouse locations.

### Example 1 — Store a list of categories for a product

```python
product = {
    "product_id": "SKU301",
    "name": "USB-C Hub",
    "categories": ["Accessories", "Connectivity", "Office Equipment"]
}

print(product)
```

**Output**
```text
{'product_id': 'SKU301', 'name': 'USB-C Hub', 'categories': ['Accessories', 'Connectivity', 'Office Equipment']}
```

In this example, `"product_id"`, `"name"`, and `"categories"` are dictionary keys. The value for `"categories"` is a list containing three text items.

### Example 2 — Get the whole list from the dictionary

Write the dictionary variable name, then the key in square brackets. This retrieves the value stored under `"categories"`.

```python
print(product["categories"])
```

**Output**
```text
['Accessories', 'Connectivity', 'Office Equipment']
```

### Example 3 — Get one item from that list

Lists use positions called **indexes**. Python starts counting list positions at `0`, so index `0` means the first item and index `1` means the second item.

```python
print(product["categories"][0])
print(product["categories"][1])
```

**Output**
```text
Accessories
Connectivity
```

Read `product["categories"][0]` in two steps:

1. `product["categories"]` gets the list stored under the dictionary key `"categories"`.
2. `[0]` gets the first item in that list.

```text
product
  └── "categories" ──> ["Accessories", "Connectivity", "Office Equipment"]
                              │
                              └── index 0: "Accessories"
```

### Example 4 — Add another item to the list

The list method `.append()` adds one item to the end of a list. Here, it adds a new category to the list stored inside the dictionary.

```python
product["categories"].append("Business Supplies")
print(product["categories"])
```

**Output**
```text
['Accessories', 'Connectivity', 'Office Equipment', 'Business Supplies']
```

Notice that we did not replace the whole dictionary. We accessed the list inside it and added one item to that list.

### Example 5 — A product with warehouse locations

A product may be stocked in more than one warehouse. A list can keep the warehouse names together under one dictionary key.

```python
stock_record = {
    "product_id": "SKU101",
    "name": "Wireless Mouse",
    "warehouse_locations": ["Delhi", "Mumbai", "Bengaluru"]
}

print(stock_record["warehouse_locations"])
print(stock_record["warehouse_locations"][2])
```

**Output**
```text
['Delhi', 'Mumbai', 'Bengaluru']
Bengaluru
```

**Key idea:** A dictionary key can hold a single value, a list of values, or even another dictionary. Use the key first to reach the value; if that value is a list, use a list index to select one item.

---

## 10. Nesting Dictionaries

A dictionary can contain another dictionary as a value. This is useful when eComMart needs to keep supplier information alongside product information.

```python
product = {
    "product_id": "SKU201",
    "name": "Laptop Stand",
    "supplier": {
        "supplier_id": "SUP014",
        "name": "Northstar Office Supplies"
    }
}

print(product)
```

**Output**
```text
{'product_id': 'SKU201', 'name': 'Laptop Stand', 'supplier': {'supplier_id': 'SUP014', 'name': 'Northstar Office Supplies'}}
```

### Access nested values one key at a time

```python
print(product["supplier"])
print(product["supplier"]["name"])
print(product["supplier"]["supplier_id"])
```

**Output**
```text
{'supplier_id': 'SUP014', 'name': 'Northstar Office Supplies'}
Northstar Office Supplies
SUP014
```

### Visual: follow the keys

```text
product
  └── "supplier"
        ├── "supplier_id" ──> "SUP014"
        └── "name"        ──> "Northstar Office Supplies"

product["supplier"]["name"]
             └──────────────> "Northstar Office Supplies"
```

Read `product["supplier"]["name"]` from left to right: first access the supplier dictionary, then access its `"name"` value.

---

## 11. Lists Containing Dictionaries

A list can hold several dictionaries. This is a common way to represent multiple orders or products. It connects the list concepts from the previous lessons with dictionary records.

```python
orders = [
    {"order_id": "ORD1001", "vendor": "Tata Electronics", "amount": 45000},
    {"order_id": "ORD1002", "vendor": "Reliance Digital", "amount": 8750},
    {"order_id": "ORD1003", "vendor": "Infosys Supplies", "amount": 62000}
]

print(orders)
```

**Output**
```text
[{'order_id': 'ORD1001', 'vendor': 'Tata Electronics', 'amount': 45000}, {'order_id': 'ORD1002', 'vendor': 'Reliance Digital', 'amount': 8750}, {'order_id': 'ORD1003', 'vendor': 'Infosys Supplies', 'amount': 62000}]
```

Use a list index to select an order, then a dictionary key to select a field.

```python
print(orders[0]["order_id"])
print(orders[1]["vendor"])
print(orders[2]["amount"])
```

**Output**
```text
ORD1001
Reliance Digital
62000
```

### Visual: list index first, dictionary key second

```text
orders
  ├── index 0 ──> {"order_id": "ORD1001", ...}
  ├── index 1 ──> {"order_id": "ORD1002", ...}
  └── index 2 ──> {"order_id": "ORD1003", ...}

orders[1]["vendor"]
       │      └────> "Reliance Digital"
       └───────────> select the second order
```

---

## 12. Exercise 1: eComMart — Product Catalogue Manager

You are managing product inventory for eComMart. Store each product name as a key and its stock quantity as the value.

### Tasks

1. Create a dictionary with at least four products and their stock counts.
2. Display the initial dictionary.
3. Add 50 units to `"Laptop Stand"`.
4. Remove the discontinued `"USB Hub"` entry.
5. Display the updated dictionary.
6. Calculate the total stock remaining across all products.

### Complete solution

```python
# eComMart product catalogue
stock = {
    "Wireless Mouse": 120,
    "USB Hub": 45,
    "Laptop Stand": 80,
    "Earbuds": 200
}

print("Initial Catalogue:", stock)

# Restock Laptop Stand
stock["Laptop Stand"] += 50
print("After Restocking:", stock)

# Remove discontinued product
stock.pop("USB Hub")
print("After Discontinuing USB Hub:", stock)

# Calculate total stock from the remaining values
total_stock = sum(stock.values())
print("Total Stock:", total_stock, "units")
```

**Expected output**
```text
Initial Catalogue: {'Wireless Mouse': 120, 'USB Hub': 45, 'Laptop Stand': 80, 'Earbuds': 200}
After Restocking: {'Wireless Mouse': 120, 'USB Hub': 45, 'Laptop Stand': 130, 'Earbuds': 200}
After Discontinuing USB Hub: {'Wireless Mouse': 120, 'Laptop Stand': 130, 'Earbuds': 200}
Total Stock: 450 units
```

**Check your understanding:** The total is `120 + 130 + 200 = 450`. The discontinued USB Hub is not included because it was removed before the total was calculated.

---

## 13. Exercise 2: eComMart — Order Lookup

You are helping the operations team look up a business customer's order. Use the order ID as the key in a dictionary, and store the order details as the value.

### Tasks

1. Create a dictionary with three orders.
2. Display the details for order `"ORD1002"`.
3. Check whether `"ORD1004"` exists.
4. Use `if-else` to display a useful message when an order is found or missing.

### Complete solution

```python
orders = {
    "ORD1001": {"vendor": "Tata Electronics", "amount": 45000, "status": "pending"},
    "ORD1002": {"vendor": "Reliance Digital", "amount": 8750, "status": "completed"},
    "ORD1003": {"vendor": "Infosys Supplies", "amount": 62000, "status": "pending"}
}

# Look up an existing order
order = orders.get("ORD1002")
print("Order ORD1002:", order)

# Check for an order that may not exist
order_id = "ORD1004"

if order_id in orders:
    print("Order found:", orders[order_id])
else:
    print("Order", order_id, "was not found")
```

**Expected output**
```text
Order ORD1002: {'vendor': 'Reliance Digital', 'amount': 8750, 'status': 'completed'}
Order ORD1004 was not found
```

---

## Working in VS Code

1. Open your Python learning folder in VS Code.
2. Create a file named `012_Dictionaries.py`.
3. Copy **one code example at a time** into the file.
4. Save the file and run it using the Python extension or the terminal command `python3 012_Dictionaries.py`.
5. Compare the terminal output with the expected output shown below that example. If you combine examples in one file, remember that earlier variables may be changed by later examples.

The downloadable lesson is Markdown (`.md`); the `.py` filename above is for running copied Python examples in VS Code.

---

## Key Takeaways

- A dictionary stores information as **key–value pairs**.
- Use `dictionary["key"]` to access a known key and `get()` when a key might be missing.
- Assignment can add a new key or update an existing value.
- Use `in` to check whether a key exists.
- Use `pop()` or `del` to remove an entry.
- Use `keys()`, `values()`, `items()`, `update()`, and `clear()` for common dictionary operations.
- Dictionaries can contain other dictionaries, and lists can contain dictionaries—both patterns are useful for modelling eComMart products and orders.
