# Product Class from Scratch

## eCOMMart AI Squad | Week 4

> “A class turns a repeated data shape into a reusable model that can carry both data and behaviour.”

## What We Will Cover

1. Review the product data represented with dictionaries.
2. Define a `Product` class and create instances.
3. Add methods to calculate and display product information.
4. Validate product values in a simple, readable way.
5. Practise extending the class with new product behaviours.

---

## 1. From Dictionaries to Objects

A dictionary can represent a product:

```python
product = {
    "product_id": "P101",
    "name": "Wireless Mouse",
    "price": 799,
    "quantity": 25
}

print(product["name"])
print(product["price"])
```

Output:

```text
Wireless Mouse
799
```

This works, but if many products use the same structure, the program repeats the same keys and may scatter related operations across separate functions.

A **class** defines a reusable structure and behaviour. An **object** is an instance created from that class.

For eCOMMart, a `Product` object can keep a product's identifier, name, price, and quantity together, along with methods that operate on those values.

## 2. Define a `Product` Class

Start with a class that stores a few attributes.

```python
class Product:
    """Represent a product sold by eCOMMart."""

    def __init__(self, product_id, name, price, quantity):
        """Store the details of a product."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


mouse = Product("P101", "Wireless Mouse", 799, 25)

print(mouse.name)
print(mouse.price)
print(mouse.quantity)
```

Output:

```text
Wireless Mouse
799
25
```

Important parts:

- `class Product:` defines the class.
- `__init__()` runs when a new instance is created.
- `self` refers to the current instance.
- `self.name`, `self.price`, and the other assignments store instance attributes.
- `mouse` refers to the created `Product` object.

The first parameter of an instance method is conventionally named `self`. Python supplies the instance automatically when you call a method through that instance.

## 3. Create Multiple Product Objects

A class is useful because you can create many objects with the same structure but different values.

```python
class Product:
    """Represent a product sold by eCOMMart."""

    def __init__(self, product_id, name, price, quantity):
        """Store the details of a product."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


mouse = Product("P101", "Wireless Mouse", 799, 25)
keyboard = Product("P102", "Keyboard", 1299, 18)
stand = Product("P103", "Laptop Stand", 999, 12)

print(mouse.name)
print(keyboard.name)
print(stand.name)
```

Output:

```text
Wireless Mouse
Keyboard
Laptop Stand
```

Each object stores its own values. Changing one object's quantity does not automatically change another object's quantity.

```python
mouse.quantity = 20

print(mouse.quantity)
print(keyboard.quantity)
```

Output:

```text
20
18
```

## 4. Add Behaviour with Methods

Attributes describe the product. Methods define actions or calculations related to it.

```python
class Product:
    """Represent a product sold by eCOMMart."""

    def __init__(self, product_id, name, price, quantity):
        """Store the details of a product."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the total value of the product's current stock."""
        return self.price * self.quantity

    def display(self):
        """Print a concise product summary."""
        print(f"{self.name}: ₹{self.price}, stock {self.quantity}")


mouse = Product("P101", "Wireless Mouse", 799, 25)
mouse.display()
print(f"Stock value: ₹{mouse.stock_value()}")
```

Output:

```text
Wireless Mouse: ₹799, stock 25
Stock value: ₹19975
```

`stock_value()` returns a value, so the caller can print it, store it, or use it in another calculation. `display()` prints a formatted summary.

## 5. Add a Simple Validation Rule

A product should not normally have a negative price or quantity. You can check values when the object is created.

```python
class Product:
    """Represent a product sold by eCOMMart."""

    def __init__(self, product_id, name, price, quantity):
        """Validate and store product details."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the total value of the product's current stock."""
        return self.price * self.quantity


mouse = Product("P101", "Wireless Mouse", 799, 25)
print(mouse.stock_value())
```

Output:

```text
19975
```

The `raise ValueError(...)` statements stop the object from being created with values that violate these rules.

This is a simple example. It checks negative values, but it does not yet validate every possible issue, such as an empty product name or a price supplied as text.

## 6. Work with a List of Objects

Objects can be stored in lists and processed with loops.

```python
class Product:
    """Represent a product sold by eCOMMart."""

    def __init__(self, product_id, name, price, quantity):
        """Store the details of a product."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the total value of the product's current stock."""
        return self.price * self.quantity


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 18),
    Product("P103", "Laptop Stand", 999, 12)
]

total_stock_value = 0

for product in products:
    value = product.stock_value()
    total_stock_value += value
    print(f"{product.name}: ₹{value}")

print(f"Total stock value: ₹{total_stock_value}")
```

Output:

```text
Wireless Mouse: ₹19975
Keyboard: ₹23382
Laptop Stand: ₹11988
Total stock value: ₹55345
```

The loop does not need to know how each product calculates its stock value. It calls the same method on each object.

## 7. A Simple Object Model

```text
                 Product class
        ┌────────────────────────────┐
        │ Attributes                 │
        │ product_id, name           │
        │ price, quantity             │
        │                            │
        │ Methods                    │
        │ stock_value()              │
        │ display()                  │
        └──────────────┬─────────────┘
                       │ creates
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       mouse        keyboard       stand
       P101           P102         P103
```

The class defines the common structure and behaviour. Each instance contains its own product data.

## 8. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Create a Product

Define a `Product` class with an `__init__()` method that stores `product_id`, `name`, and `price`. Create an object for a `Phone Stand` priced at `399` and print its name and price.

Expected output:

```text
Phone Stand
399
```

### Task 2 — Add a Stock Value Method

Extend `Product` to also store `quantity`. Add a `stock_value()` method that returns `price * quantity`.

Create a product with price `500` and quantity `6`, then print the result of `stock_value()`.

Expected output:

```text
3000
```

### Task 3 — Summarize Multiple Products

Create a `Product` class with `name`, `price`, and `quantity`, plus a `stock_value()` method. Create two objects:

- Desk Lamp: price `899`, quantity `4`
- Notebook: price `149`, quantity `10`

Loop over the objects, print each stock value, and calculate the total.

Expected output:

```text
Desk Lamp: ₹3596
Notebook: ₹1490
Total stock value: ₹5086
```

## Summary

| Concept | Purpose |
|---|---|
| Class | Defines a reusable structure and behaviour |
| Object / instance | A specific value created from a class |
| `__init__()` | Initializes a new instance |
| `self` | Refers to the current instance |
| Instance attributes | Store data for each object |
| Instance methods | Define behaviour using instance data |
| `raise ValueError` | Reject values that violate a rule |
| List of objects | Lets a program process many instances consistently |

A `Product` class keeps related product data and behaviour together. In the next worked example, the same OOP foundations will be expanded into a catalogue manager with inheritance.

*Next: `02_Catalog_Manager_with_Inheritance.md`*
