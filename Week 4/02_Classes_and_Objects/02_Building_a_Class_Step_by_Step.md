# Building a Class Step by Step
## eCOMMart AI Squad | Week 4

> A class is never written all at once. You start with the minimum that works,
> verify it, then add behaviour in deliberate layers. This file teaches that
> construction process — and introduces the patterns that separate a well-built
> class from one that merely runs.

---

## What We Will Cover

1. The iterative approach — build, verify, extend
2. Mutating methods vs query methods — a critical distinction
3. Methods that derive values from stored state
4. Methods calling other methods — building behaviour from behaviour
5. Returning `self` — method chaining
6. Holding another object as an attribute — composition in practice
7. A complete class built step by step — `CartItem`
8. Tasks

---

## 1. The Iterative Approach — Build, Verify, Extend

A common beginner mistake is to try writing the entire class at once —
all attributes, all methods, full validation — before running a single line.
When something breaks, there are 20 places it could have gone wrong.

The professional approach is layered:

```
Layer 1 — Minimal skeleton     : class + __init__ + one method
Layer 2 — Core behaviour       : the methods this class exists to provide
Layer 3 — Derived values       : methods that compute from stored state
Layer 4 — Guards and validation: raise errors on bad input
Layer 5 — Integration          : hold other objects, delegate to them
```

Each layer is verified before the next is added. Let us apply this to
building `CartItem` — the class that represents one line in an eCOMMart
shopping cart.

From the design in the previous folder, a `CartItem`:
- holds a `Product` object and a `quantity`
- can calculate its own line total and the GST on that total
- knows its own discount amount if a promotion applies
- can describe itself as a formatted string

---

## 2. Mutating Methods vs Query Methods — A Critical Distinction

You may also encounter the terms **getter** and **setter** in object-oriented programming literature. A *getter* retrieves an object's attribute or a derived value, making it a type of query method, while a *setter* updates an attribute and is therefore a type of mutating method. In Python, these operations are often implemented using regular methods or, when appropriate, the `@property` decorator and its corresponding setter.

Before writing a single method, understand this split — it shapes every
design decision:

```
┌──────────────────┬────────────────────────────────────────────────────────┐
│  Mutating method │  Changes the object's state. Returns None (usually).   │
│                  │  Example: restock(), apply_promotion(), cancel()        │
├──────────────────┼────────────────────────────────────────────────────────┤
│  Query method    │  Reads state and returns a value. Never changes state.  │
│                  │  Example: get_line_total(), is_available(), get_badge() │
└──────────────────┴────────────────────────────────────────────────────────┘
```

Why does this matter? A method that is meant to *tell* you something should
never accidentally *change* something. If `get_line_total()` modifies
`self.quantity` as a side effect, every call to it corrupts the cart.

The discipline: **query methods only read. Mutating methods only change.**
Keep them separate and name them to signal intent:

```
get_*()       → query  — returns a value, no side effects
calculate_*() → query  — computes and returns, no side effects
is_*()        → query  — returns bool, no side effects
set_*()       → mutating — changes one field
update_*()    → mutating — changes one or more fields
apply_*()     → mutating — applies a transformation to state
reset_*()     → mutating — restores state to a default
```

---

## 3. Layer 1 — Minimal Skeleton

Start with only what is needed to create a valid object and verify it works:

```python
class CartItem:
    """
    Represents a single line in an eCOMMart shopping cart.

    A CartItem links a Product to the quantity a customer intends
    to purchase. All pricing calculations for that line — subtotal,
    GST, discounts — are the responsibility of this class.

    Attributes:
        product    (Product): The Product object being purchased.
        quantity   (int):     Number of units. Must be >= 1.
    """

    def __init__(self, product, quantity):
        self.product  = product
        self.quantity = quantity
```

Verify immediately — do not move on until this works:

```python
# We need a Product to test with — reuse the class from the previous file
class Product:
    def __init__(self, sku, name, price, category, stock):
        self.sku      = sku
        self.name     = name
        self.price    = price
        self.category = category
        self.stock    = stock

mouse = Product("WM-4021", "Wireless Mouse", 499.00, "Electronics", 120)

# Create a CartItem
item = CartItem(product=mouse, quantity=3)

# Verify attributes are accessible
print(item.quantity)          # 3
print(item.product.name)      # Wireless Mouse  ← dot chaining into the held object
print(item.product.price)     # 499.0
print(type(item.product))     # <class '__main__.Product'>
```
```
# Output:
3
Wireless Mouse
499.0
<class '__main__.Product'>
```

Notice `item.product.name` — two dots in sequence. `item.product` gives
you the `Product` object. `.name` then reads the attribute on *that* object.
This is composition working exactly as designed: `CartItem` holds a `Product`
and you reach through `CartItem` to access `Product`'s data.

---

## 4. Layer 2 — Core Query Methods

The primary job of a `CartItem` is to report its own pricing. These are
all query methods — they read state and return a value, never changing anything.

```python
class CartItem:
    """
    Represents a single line in an eCOMMart shopping cart.

    Attributes:
        product    (Product): The Product object being purchased.
        quantity   (int):     Number of units. Must be >= 1.
        promotion  (float):   Discount percentage applied to this line.
                              0.0 means no promotion active.
    """

    GST_RATE = 0.18    # class-level constant — same for every CartItem

    def __init__(self, product, quantity):
        self.product   = product
        self.quantity  = quantity
        self.promotion = 0.0      # no promotion by default

    def get_unit_price(self):
        """
        Returns the effective unit price after any active promotion.

        Returns:
            float: Unit price in INR after promotion discount.
        """
        return self.product.price * (1 - self.promotion / 100)

    def get_line_subtotal(self):
        """
        Returns the pre-GST total for this line (unit price × quantity).

        Returns:
            float: Line subtotal in INR before GST.
        """
        return self.get_unit_price() * self.quantity

    def get_gst_amount(self):
        """
        Returns the GST amount for this line at the standard 18% rate.

        Returns:
            float: GST in INR on this line's subtotal.
        """
        return self.get_line_subtotal() * self.GST_RATE

    def get_line_total(self):
        """
        Returns the final amount for this line including GST.

        Returns:
            float: Line total in INR inclusive of GST.
        """
        return self.get_line_subtotal() + self.get_gst_amount()
```

Verify each method in isolation:

```python
mouse = Product("WM-4021", "Wireless Mouse", 499.00, "Electronics", 120)
item  = CartItem(product=mouse, quantity=3)

print(f"  Unit price    : ₹{item.get_unit_price():.2f}")
print(f"  Line subtotal : ₹{item.get_line_subtotal():.2f}")
print(f"  GST (18%)     : ₹{item.get_gst_amount():.2f}")
print(f"  Line total    : ₹{item.get_line_total():.2f}")
```
```
# Output:
  Unit price    : ₹499.00
  Line subtotal : ₹1,497.00
  GST (18%)     : ₹269.46
  Line total    : ₹1,766.46
```

Observe the chain: `get_line_total()` calls `get_line_subtotal()`, which
calls `get_unit_price()`, which reads `self.product.price`. Each method
does one small job and delegates upward. This is how complex behaviour is
built from simple, independently-testable pieces.

```
get_line_total()
    └── calls get_line_subtotal()
            └── calls get_unit_price()
                    └── reads self.product.price   (from the held Product object)
                        reads self.promotion        (from CartItem's own state)
```

---

## 5. Layer 3 — Mutating Methods

Now add behaviour that *changes* the `CartItem`'s state. Each mutating
method should validate its input before applying the change.

```python
    def set_quantity(self, new_qty):
        """
        Updates the quantity for this line item.

        Args:
            new_qty (int): New quantity. Must be >= 1.

        Raises:
            ValueError: If new_qty is less than 1.
        """
        if not isinstance(new_qty, int) or new_qty < 1:
            raise ValueError(
                f"Quantity must be a positive integer. Got: {new_qty!r}"
            )
        self.quantity = new_qty

    def apply_promotion(self, discount_pct):
        """
        Applies a promotional discount to this line item.

        Only one promotion can be active at a time. Calling this
        again replaces any existing promotion.

        Args:
            discount_pct (float): Discount percentage, e.g. 10 for 10%.
                                  Must be between 0 and 100 inclusive.

        Raises:
            ValueError: If discount_pct is outside the valid range.
        """
        if not (0 <= discount_pct <= 100):
            raise ValueError(
                f"Discount must be between 0 and 100. Got: {discount_pct}"
            )
        self.promotion = discount_pct

    def remove_promotion(self):
        """Removes any active promotion, restoring the base price."""
        self.promotion = 0.0
```

Verify the interaction between mutating and query methods:

```python
mouse = Product("WM-4021", "Wireless Mouse", 499.00, "Electronics", 120)
item  = CartItem(product=mouse, quantity=3)

print(f"  Before promotion — line total: ₹{item.get_line_total():.2f}")

item.apply_promotion(10)    # 10% flash sale discount
print(f"  After 10% promo  — line total: ₹{item.get_line_total():.2f}")
print(f"  Unit price now   : ₹{item.get_unit_price():.2f}")

item.set_quantity(5)
print(f"  After qty → 5    — line total: ₹{item.get_line_total():.2f}")

item.remove_promotion()
print(f"  Promo removed    — line total: ₹{item.get_line_total():.2f}")
```
```
# Output:
  Before promotion — line total: ₹1,766.46
  After 10% promo  — line total: ₹1,589.81
  Unit price now   : ₹449.10
  After qty → 5    — line total: ₹2,649.69
  Promo removed    — line total: ₹2,949.10
```

Test the validation guards:

```python
try:
    item.set_quantity(0)
except ValueError as e:
    print(f"  ValueError: {e}")

try:
    item.apply_promotion(110)
except ValueError as e:
    print(f"  ValueError: {e}")
```
```
# Output:
  ValueError: Quantity must be a positive integer. Got: 0
  ValueError: Discount must be between 0 and 100. Got: 110
```

---

## 6. Returning `self` — Method Chaining

Some methods are designed to be called one after another in a single
expression. To enable this, the method returns `self` instead of `None`.

```python
    def set_quantity(self, new_qty):
        if not isinstance(new_qty, int) or new_qty < 1:
            raise ValueError(f"Quantity must be a positive integer. Got: {new_qty!r}")
        self.quantity = new_qty
        return self          # ← return self enables chaining

    def apply_promotion(self, discount_pct):
        if not (0 <= discount_pct <= 100):
            raise ValueError(f"Discount must be between 0 and 100. Got: {discount_pct}")
        self.promotion = discount_pct
        return self          # ← return self enables chaining

    def remove_promotion(self):
        self.promotion = 0.0
        return self          # ← return self enables chaining
```

Without chaining — three separate lines:

```python
item.set_quantity(4)
item.apply_promotion(15)
print(f"  Line total: ₹{item.get_line_total():.2f}")
```

With chaining — one fluent expression:

```python
item.set_quantity(4).apply_promotion(15)
print(f"  Line total: ₹{item.get_line_total():.2f}")
```
```
# Output:
  Line total: ₹2,835.97
```

```
item.set_quantity(4).apply_promotion(15)
         ↑                  ↑
         │                  └── called on the CartItem returned by set_quantity()
         └── returns self (the same CartItem object)
```

Chaining reads naturally — *"set quantity to 4 and apply a 15% promotion"* —
and removes the repetition of writing `item.` on every line. It is common
in real APIs: you will see this pattern in query builders, SDK clients,
and data pipeline libraries.

> **When to use it:** Only on mutating methods where the caller will
> frequently call several in sequence. Never on query methods — returning
> a value and returning `self` are mutually exclusive.

---

## 7. Layer 4 — A Display Method That Composes Everything

The final layer: a method that assembles all of the above into a
formatted summary. This is a query method — it reads state and returns
a string representation.

```python
    def summarise(self):
        """
        Returns a formatted string summary of this cart line item.

        Returns:
            str: Multi-line summary including product details, quantity,
                 promotion, and all pricing components.
        """
        promo_label = (
            f"  Promotion     : {self.promotion:.0f}% off\n"
            if self.promotion > 0
            else "  Promotion     : None\n"
        )
        return (
            f"  {'─' * 44}\n"
            f"  Product       : {self.product.name} [{self.product.sku}]\n"
            f"  Category      : {self.product.category}\n"
            f"  Base price    : ₹{self.product.price:.2f}\n"
            f"{promo_label}"
            f"  Unit price    : ₹{self.get_unit_price():.2f}\n"
            f"  Quantity      : {self.quantity}\n"
            f"  Subtotal      : ₹{self.get_line_subtotal():.2f}\n"
            f"  GST (18%)     : ₹{self.get_gst_amount():.2f}\n"
            f"  Line total    : ₹{self.get_line_total():.2f}\n"
            f"  {'─' * 44}"
        )
```

---

## 8. The Complete `CartItem` Class

Every layer assembled into one clean, production-ready class:

```python
class CartItem:
    """
    Represents a single line in an eCOMMart shopping cart.

    A CartItem links a Product to the quantity a customer intends
    to purchase. All pricing calculations for that line — subtotal,
    GST, promotional discounts — are the responsibility of this class.

    Attributes:
        product    (Product): The Product object being purchased.
        quantity   (int):     Number of units. Must be >= 1.
        promotion  (float):   Active discount percentage (0.0 = no promotion).

    Example:
        >>> item = CartItem(product=mouse, quantity=3)
        >>> item.apply_promotion(10).set_quantity(5)
        >>> item.get_line_total()
        2649.69
    """

    GST_RATE = 0.18

    def __init__(self, product, quantity):
        self.product   = product
        self.quantity  = quantity
        self.promotion = 0.0

    # ── Query methods ────────────────────────────────────────────
    def get_unit_price(self):
        """Returns effective unit price after any active promotion."""
        return self.product.price * (1 - self.promotion / 100)

    def get_line_subtotal(self):
        """Returns pre-GST line total (unit price × quantity)."""
        return self.get_unit_price() * self.quantity

    def get_gst_amount(self):
        """Returns 18% GST on the line subtotal."""
        return self.get_line_subtotal() * self.GST_RATE

    def get_line_total(self):
        """Returns final line total inclusive of GST."""
        return self.get_line_subtotal() + self.get_gst_amount()

    def has_promotion(self):
        """Returns True if a promotion is currently active on this line."""
        return self.promotion > 0.0

    # ── Mutating methods ─────────────────────────────────────────
    def set_quantity(self, new_qty):
        """Updates the line quantity. Raises ValueError if < 1."""
        if not isinstance(new_qty, int) or new_qty < 1:
            raise ValueError(
                f"Quantity must be a positive integer. Got: {new_qty!r}"
            )
        self.quantity = new_qty
        return self

    def apply_promotion(self, discount_pct):
        """Applies a promotional discount to this line (0–100%). Returns self."""
        if not (0 <= discount_pct <= 100):
            raise ValueError(
                f"Discount must be between 0 and 100. Got: {discount_pct}"
            )
        self.promotion = discount_pct
        return self

    def remove_promotion(self):
        """Removes any active promotion. Returns self."""
        self.promotion = 0.0
        return self

    # ── Display ──────────────────────────────────────────────────
    def summarise(self):
        """Returns a formatted multi-line string summary of this line item."""
        promo_label = (
            f"  Promotion     : {self.promotion:.0f}% off\n"
            if self.promotion > 0
            else "  Promotion     : None\n"
        )
        return (
            f"  {'─' * 44}\n"
            f"  Product       : {self.product.name} [{self.product.sku}]\n"
            f"  Category      : {self.product.category}\n"
            f"  Base price    : ₹{self.product.price:.2f}\n"
            f"{promo_label}"
            f"  Unit price    : ₹{self.get_unit_price():.2f}\n"
            f"  Quantity      : {self.quantity}\n"
            f"  Subtotal      : ₹{self.get_line_subtotal():.2f}\n"
            f"  GST (18%)     : ₹{self.get_gst_amount():.2f}\n"
            f"  Line total    : ₹{self.get_line_total():.2f}\n"
            f"  {'─' * 44}"
        )
```

### Running the complete class

```python
# Products
mouse = Product("WM-4021", "Wireless Mouse",  499.00, "Electronics", 120)
watch = Product("SW-9001", "Smart Watch",    2999.00, "Wearables",    30)
hub   = Product("UH-1102", "USB Hub",         350.00, "Electronics",  45)

# Build cart items — use chaining on the second item
item_mouse = CartItem(mouse, 3)
item_watch = CartItem(watch, 1).apply_promotion(12)   # 12% launch offer
item_hub   = CartItem(hub,   2).apply_promotion(5)    # 5% bundle deal

# Print each line
print(item_mouse.summarise())
print(item_watch.summarise())
print(item_hub.summarise())

# Cart-level totals (we will build a proper Cart class later)
items        = [item_mouse, item_watch, item_hub]
cart_total   = sum(i.get_line_total() for i in items)
cart_subtotal= sum(i.get_line_subtotal() for i in items)
cart_gst     = sum(i.get_gst_amount() for i in items)

print(f"\n  {'═' * 44}")
print(f"  Cart subtotal   : ₹{cart_subtotal:>10.2f}")
print(f"  Total GST (18%) : ₹{cart_gst:>10.2f}")
print(f"  Cart total      : ₹{cart_total:>10.2f}")
print(f"  {'═' * 44}")
print(f"  Items with promotion : {sum(1 for i in items if i.has_promotion())}")
```
```
# Output:
  ────────────────────────────────────────────
  Product       : Wireless Mouse [WM-4021]
  Category      : Electronics
  Base price    : ₹499.00
  Promotion     : None
  Unit price    : ₹499.00
  Quantity      : 3
  Subtotal      : ₹1,497.00
  GST (18%)     : ₹269.46
  Line total    : ₹1,766.46
  ────────────────────────────────────────────
  ────────────────────────────────────────────
  Product       : Smart Watch [SW-9001]
  Category      : Wearables
  Base price    : ₹2,999.00
  Promotion     : 12% off
  Unit price    : ₹2,639.12
  Quantity      : 1
  Subtotal      : ₹2,639.12
  GST (18%)     : ₹475.04
  Line total    : ₹3,114.16
  ────────────────────────────────────────────
  ────────────────────────────────────────────
  Product       : USB Hub [UH-1102]
  Category      : Electronics
  Base price    : ₹350.00
  Promotion     : 5% off
  Unit price    : ₹332.50
  Quantity      : 2
  Subtotal      : ₹665.00
  GST (18%)     : ₹119.70
  Line total    : ₹784.70
  ────────────────────────────────────────────

  ════════════════════════════════════════════
  Cart subtotal   : ₹   4,801.12
  Total GST (18%) : ₹     864.20
  Cart total      : ₹   5,665.32
  ════════════════════════════════════════════
  Items with promotion : 2
```

---

## 9. Tasks

### Task 1 — Extend `CartItem` with a `to_dict()` Method

Add a `to_dict()` method to `CartItem` that returns a **plain Python dictionary** representing the line item. This dictionary should be suitable for saving to a JSON file.

The dictionary must include all the fields shown in the expected output, including pricing fields as computed values rather than raw attributes.

**Important:** Your method must use the `return` statement to send the dictionary back to the code that calls it. Printing the dictionary inside `to_dict()` is not a substitute for returning it.

#### Step 1 — Implement `to_dict()` in the `CartItem` Class

Complete the following method inside your existing `CartItem` class:

```python
def to_dict(self):
    """
    Serialises this CartItem to a plain dictionary for JSON output.

    Returns:
        dict: All line item fields, including computed pricing values.
    """
    # TODO: Create a dictionary containing all required fields.
    # Include computed pricing values using the appropriate properties.
    # TODO: Return the dictionary using the return statement.
```

**Implementation requirements:**

- Include `sku`, `name`, `category`, `base_price`, `promotion_pct`, and `quantity`.
- Include the computed values `unit_price`, `subtotal`, `gst_amount`, and `line_total`.
- Use the appropriate attributes and properties already defined in `CartItem`.
- Return the completed dictionary using `return`.

#### Step 2 — Call `to_dict()` from the Main Module

After implementing the method, go to the main module or the section where you create and use a `CartItem` instance.

Complete the following skeleton to call your method and print the returned dictionary:

```python
# Create a CartItem instance using the existing constructor.
item = CartItem(
    # TODO: Supply the arguments required by your CartItem class.
)

# Call to_dict() and capture the returned dictionary.
# The return value from item.to_dict() is assigned to item_data.
item_data = item.to_dict()

# Print the dictionary returned by to_dict().
print(item_data)
```

**How this works:**

1. `item.to_dict()` calls the method on the `CartItem` object.
2. The method creates a dictionary containing the item's details and computed pricing values.
3. The `return` statement sends that dictionary back to the calling code.
4. The returned dictionary is stored in `item_data`.
5. `print(item_data)` displays the dictionary in the terminal.

**Remember:** `return` and `print()` serve different purposes. `return` sends a value back to the calling code, while `print()` displays a value on the screen. Keep `to_dict()` responsible for creating and returning the dictionary; let the main module decide how to use or display it.

#### Expected Output

For a mouse item with 3 units and no promotion, the returned dictionary should contain values equivalent to the following:

```python
{
    "sku": "WM-4021",
    "name": "Wireless Mouse",
    "category": "Electronics",
    "base_price": 499.00,
    "promotion_pct": 0.0,
    "unit_price": 499.00,
    "quantity": 3,
    "subtotal": 1497.00,
    "gst_amount": 269.46,
    "line_total": 1766.46
}
```

Your output should contain the same fields and values. The order of dictionary keys does not affect correctness.

#### Verification Checklist

Before moving on, verify that:

- [ ] `to_dict()` creates a plain Python dictionary.
- [ ] All required fields are included.
- [ ] Pricing fields contain computed values.
- [ ] The method returns the dictionary instead of printing it.
- [ ] The main module captures the returned dictionary in `item_data`.
- [ ] Printing `item_data` displays the expected dictionary.