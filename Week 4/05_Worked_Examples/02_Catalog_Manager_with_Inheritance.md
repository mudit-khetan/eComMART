# Catalog Manager with Inheritance

## eCOMMart AI Squad | Week 4

> “Inheritance is useful when different kinds of objects share a common foundation but need their own specific behaviour.”

## What We Will Cover

1. Review the purpose of a class hierarchy.
2. Build a base `Product` class.
3. Extend the base class with a specialised product class.
4. Use overriding and `super()` appropriately.
5. Create a small catalogue manager that works with different product types.

---

## 1. Why Use Inheritance?

In the previous worked example, a `Product` class stored common details such as an identifier, name, price, and quantity. Some products, however, may need additional information.

For example, an eCOMMart catalogue might include ordinary products and discounted products. Both have names and quantities, but a discounted product can calculate a selling price using its discount rate.

**Inheritance** lets a new class reuse and extend an existing class.

```text
              Product
                 |
                 | inherits from
                 v
          DiscountedProduct
```

The base class holds shared data and behaviour. The child class adds or customises behaviour that is specific to it.

## 2. Create the Base `Product` Class

Start with a class that represents a standard catalogue product.

```python
class Product:
    """Represent a standard eCOMMart catalogue product."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the shared product details."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the total value of the available stock."""
        return self.price * self.quantity

    def display(self):
        """Print the product's basic catalogue details."""
        print(f"{self.product_id} | {self.name} | ₹{self.price} | Stock: {self.quantity}")


mouse = Product("P101", "Wireless Mouse", 799, 25)
mouse.display()
print(f"Stock value: ₹{mouse.stock_value()}")
```

Output:

```text
P101 | Wireless Mouse | ₹799 | Stock: 25
Stock value: ₹19975
```

The base class provides the shared structure and methods. The next class will reuse this foundation rather than copy all the same code.

## 3. Create a Child Class

Use parentheses after the class name to indicate its parent class.

```python
class DiscountedProduct(Product):
    """Represent a product with a percentage discount."""

    def __init__(self, product_id, name, price, quantity, discount_percent):
        """Initialize product details and its discount percentage."""
        super().__init__(product_id, name, price, quantity)

        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100.")

        self.discount_percent = discount_percent

    def selling_price(self):
        """Return the price after applying the percentage discount."""
        discount = self.price * self.discount_percent / 100
        return self.price - discount


sale_mouse = DiscountedProduct(
    "P201", "Gaming Mouse", 1999, 10, 15
)

sale_mouse.display()
print(f"Discount: {sale_mouse.discount_percent}%")
print(f"Selling price: ₹{sale_mouse.selling_price():.2f}")
```

Output:

```text
P201 | Gaming Mouse | ₹1999 | Stock: 10
Discount: 15%
Selling price: ₹1699.15
```

Key ideas:

- `DiscountedProduct(Product)` declares that the child class inherits from `Product`.
- `super().__init__(...)` calls the parent initializer to set the shared attributes.
- The child class adds `discount_percent`.
- The new `selling_price()` method uses the inherited `price` attribute.

## 4. Override a Method

A child class can provide its own implementation of a method inherited from its parent. This is called **method overriding**.

For this example, the base class's `display()` method shows the regular price. The child class can override it to include the discount and final selling price.

```python
class DiscountedProduct(Product):
    """Represent a product with a percentage discount."""

    def __init__(self, product_id, name, price, quantity, discount_percent):
        """Initialize product details and its discount percentage."""
        super().__init__(product_id, name, price, quantity)

        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100.")

        self.discount_percent = discount_percent

    def selling_price(self):
        """Return the price after applying the percentage discount."""
        return self.price * (1 - self.discount_percent / 100)

    def display(self):
        """Print the product details, discount, and selling price."""
        print(
            f"{self.product_id} | {self.name} | "
            f"Regular: ₹{self.price} | "
            f"Discount: {self.discount_percent}% | "
            f"Selling: ₹{self.selling_price():.2f}"
        )


sale_mouse = DiscountedProduct(
    "P201", "Gaming Mouse", 1999, 10, 15
)
sale_mouse.display()
```

Output:

```text
P201 | Gaming Mouse | Regular: ₹1999 | Discount: 15% | Selling: ₹1699.15
```

The child version of `display()` replaces the inherited version for `DiscountedProduct` instances. The base `Product` class still has its original `display()` method.

## 5. Build a Simple Catalogue Manager

A catalogue manager can keep different product objects in one list. Each object can be displayed through its own `display()` method.

```python
class Product:
    """Represent a standard eCOMMart catalogue product."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the shared product details."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the total value of the available stock."""
        return self.price * self.quantity

    def display(self):
        """Print the product's basic catalogue details."""
        print(f"{self.product_id} | {self.name} | ₹{self.price} | Stock: {self.quantity}")


class DiscountedProduct(Product):
    """Represent a product with a percentage discount."""

    def __init__(self, product_id, name, price, quantity, discount_percent):
        """Initialize product details and its discount percentage."""
        super().__init__(product_id, name, price, quantity)

        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100.")

        self.discount_percent = discount_percent

    def selling_price(self):
        """Return the price after applying the percentage discount."""
        return self.price * (1 - self.discount_percent / 100)

    def display(self):
        """Print the product details, discount, and selling price."""
        print(
            f"{self.product_id} | {self.name} | "
            f"Regular: ₹{self.price} | "
            f"Discount: {self.discount_percent}% | "
            f"Selling: ₹{self.selling_price():.2f}"
        )


class CatalogManager:
    """Store and display catalogue products."""

    def __init__(self):
        """Create an empty catalogue."""
        self.products = []

    def add_product(self, product):
        """Add a product object to the catalogue."""
        self.products.append(product)

    def display_all(self):
        """Display every product in the catalogue."""
        for product in self.products:
            product.display()


catalog = CatalogManager()
catalog.add_product(Product("P101", "Wireless Mouse", 799, 25))
catalog.add_product(DiscountedProduct("P201", "Gaming Mouse", 1999, 10, 15))
catalog.add_product(Product("P103", "Laptop Stand", 999, 12))

catalog.display_all()
```

Output:

```text
P101 | Wireless Mouse | ₹799 | Stock: 25
P201 | Gaming Mouse | Regular: ₹1999 | Discount: 15% | Selling: ₹1699.15
P103 | Laptop Stand | ₹999 | Stock: 12
```

The `CatalogManager` does not need separate display logic for each product type. It calls `display()` on each object, and Python uses the implementation belonging to that object's class.

This behaviour is an example of **polymorphism**: different object types respond to the same method call in their own way.

## 6. Add a Catalogue Search

A catalogue manager can also provide a small search method.

```python
class CatalogManager:
    """Store and search catalogue products."""

    def __init__(self):
        """Create an empty catalogue."""
        self.products = []

    def add_product(self, product):
        """Add a product object to the catalogue."""
        self.products.append(product)

    def find_by_id(self, product_id):
        """Return the product with the matching ID, or None."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None


catalog = CatalogManager()
catalog.add_product(Product("P101", "Wireless Mouse", 799, 25))
catalog.add_product(DiscountedProduct("P201", "Gaming Mouse", 1999, 10, 15))

found = catalog.find_by_id("P201")

if found is not None:
    found.display()
else:
    print("Product not found.")
```

Output:

```text
P201 | Gaming Mouse | Regular: ₹1999 | Discount: 15% | Selling: ₹1699.15
```

This section shows the search behaviour in isolation. In a complete script, use the same `Product`, `DiscountedProduct`, and `CatalogManager` definitions together; do not redefine the manager midway through a program unless you intentionally want to replace its definition.

## 7. When Should You Use Inheritance?

Inheritance is useful when a child class truly **is a specialised kind of** its parent and can share the parent's interface.

For example:
- A `DiscountedProduct` is a kind of `Product`.
- It can reuse the common product fields.
- It can add a discount field and specialise display behaviour.

Do not use inheritance only to avoid a few repeated lines. If two objects are related but do not represent a parent-child relationship, composition may be a better fit. The next worked example builds on that distinction.

## 8. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Create a Specialised Product

Create a base `Product` class with `name` and `price`. Create a `DiscountedProduct` child class that adds `discount_percent` and implements `selling_price()`.

For a product named `Desk Lamp`, with a price of `1000` and a discount of `10`, print the selling price to two decimal places.

Expected output:

```text
900.00
```

### Task 2 — Override Display

Create a `Product` class with a `display()` method that prints the product name. Create a `DiscountedProduct` child class that overrides `display()` to include the discount percentage.

For a `Notebook` with a `20%` discount, expected output:

```text
Notebook - Discount: 20%
```

### Task 3 — Build a Catalogue

Create a `CatalogManager` that stores product objects in a list and has an `add_product()` method. Add one regular product and one discounted product. Loop through the catalogue and call `display()` on each object.

Expected output format:

```text
Wireless Mouse
Keyboard - Discount: 10%
```

Use your own class definitions to produce the specified behaviour.

## Summary

| Concept | Purpose |
|---|---|
| Base class | Holds common attributes and behaviour |
| Child class | Reuses and extends a base class |
| `super()` | Calls a method from the parent class |
| Method overriding | Gives a child class its own version of an inherited method |
| Polymorphism | Lets different objects respond to the same method call |
| Catalogue manager | Stores and works with product objects |

Inheritance can reduce duplication when classes have a genuine parent-child relationship. In this example, `DiscountedProduct` reuses `Product` and customises the way a discounted item is displayed.

*Next: `03_Reading_and_Writing_Product_Data.md`*
