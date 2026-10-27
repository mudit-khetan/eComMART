# Encapsulation and Properties
## eCOMMart AI Squad | Week 4

*“A good class protects its rules, not just its data.”*

## What We Will Cover

1. Why uncontrolled attribute changes create bugs in business applications.
2. Public, non-public, and name-mangled attributes in Python.
3. How properties provide a controlled interface to an object's data.
4. How setters validate values before accepting changes.
5. How read-only and computed properties keep business rules in one place.
6. How to design an encapsulated class for eCOMMart's pricing workflow.

---

## 1. Why Encapsulation Matters

Imagine eCOMMart stores a product's selling price. A normal attribute is easy to change:

```python
class PricingTier:
    """Represent a pricing tier used by the eCOMMart catalogue."""

    def __init__(self, name, price):
        """Store the tier name and price."""
        self.name = name
        self.price = price


starter = PricingTier("Starter", 499)
starter.price = -100

print(starter.price)
# Output:
# -100
```

The assignment succeeds, but a negative selling price is not valid for this business example. The problem is not that Python allowed assignment; the problem is that the class did not protect its own rules.

A class should define which values are acceptable and how important data may change. That design principle is called **encapsulation**.

Encapsulation means keeping data and the operations that govern it together behind a clear interface. It helps prevent invalid states and makes a class easier to maintain.

```text
Without a controlled interface

Caller ----------------------> price = -100
                                  |
                                  v
                           Invalid object state


With a controlled interface

Caller ---> price property ---> Validation rule
                                  |
                          +-------+-------+
                          |               |
                       accepted        rejected
                          |               |
                          v               v
                     update value     raise error
```

Encapsulation is not about making every attribute inaccessible. It is about deciding which parts of an object are intended for callers to use and where the class must enforce rules.

## 2. Python's Attribute Conventions

Python does not enforce access modifiers in the same way as languages such as Java. Instead, it uses naming conventions and a name-mangling mechanism.

### 2.1 Public attributes

A name without a leading underscore is conventionally public. Callers may use it directly.

```python
class StoreProfile:
    """Store basic public information about a shop."""

    def __init__(self, store_name):
        """Create a profile with a public store name."""
        self.store_name = store_name


profile = StoreProfile("eCOMMart North")
print(profile.store_name)
# Output:
# eCOMMart North
```

Use public attributes when direct access is part of the intended interface and does not need extra rules.

### 2.2 Non-public attributes: one leading underscore

A single leading underscore communicates: “This is an implementation detail; external code should generally not depend on it.”

```python
class StockCounter:
    """Track a stock count as an implementation detail."""

    def __init__(self, quantity):
        """Store the initial quantity."""
        self._quantity = quantity

    def available_units(self):
        """Return the current quantity through the public interface."""
        return self._quantity


counter = StockCounter(18)
print(counter.available_units())
# Output:
# 18

print(counter._quantity)
# Output:
# 18
```

The underscore does not block access. The last line works, but callers are being warned not to rely on `_quantity` as a stable public interface.

Prefer methods or properties when the class needs to control access. Do not treat the underscore as a security boundary.

### 2.3 Name-mangled attributes: two leading underscores

A name beginning with two underscores, and not ending with two underscores, is transformed by Python's name-mangling mechanism. This helps avoid accidental name clashes in subclasses.

```python
class ApiCredential:
    """Keep a credential field away from accidental name collisions."""

    def __init__(self, label, token):
        """Store the label and an internal token value."""
        self.label = label
        self.__token = token

    def has_token(self):
        """Report whether a token has been configured."""
        return bool(self.__token)


credential = ApiCredential("Inventory API", "demo-token")
print(credential.has_token())
# Output:
# True

print(credential.__dict__)
# Output:
# {'label': 'Inventory API', '_ApiCredential__token': 'demo-token'}
```

Python changes `__token` to `_ApiCredential__token` inside this class. This is called **name mangling**.

It is useful to know what the mechanism does, but do not use it as encryption or secret storage. A determined caller can still access the mangled name. Real credentials should be managed with appropriate secret-management practices.

### 2.4 Do not confuse private conventions with special methods

Names such as `__init__` and `__str__` are special-method names defined by Python's data model. They begin and end with two underscores. They are not the same as a user-defined attribute like `__token`.

```text
__init__     special method: double underscores at both ends
__str__      special method: double underscores at both ends
__token      name-mangled attribute: starts with two underscores
_token       non-public convention: starts with one underscore
token        public attribute: no leading underscore
```

## 3. From a Plain Attribute to a Property

Suppose a pricing tier must always have a non-negative price. We could create a method such as `set_price()`, but Python also provides **properties**. A property allows attribute-style access while running code when the value is read or assigned.

```text
tier.price = 799
      |
      v
@property setter
      |
      v
Validate the proposed price
      |
      +---- valid ----> store the value
      |
      +---- invalid --> raise ValueError
```

The caller still writes `tier.price`, rather than calling a setter method. The class retains control over the update.

### 3.1 The `property` pattern

A property commonly uses three parts:

- A getter decorated with `@property`.
- A setter decorated with `@price.setter`.
- A backing attribute, conventionally named `_price`.

```python
class SimplePrice:
    """Represent a price with a controlled property."""

    def __init__(self, price):
        """Initialize the price through the property setter."""
        self.price = price

    @property
    def price(self):
        """Return the current price."""
        return self._price

    @price.setter
    def price(self, value):
        """Accept a non-negative price and reject invalid values."""
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value


item = SimplePrice(250)
print(item.price)
# Output:
# 250

item.price = 300
print(item.price)
# Output:
# 300
```

Notice that `__init__` assigns to `self.price`, which invokes the setter. The setter stores the actual value in `self._price`. It must not assign to `self.price` inside itself, because that would call the setter again and cause infinite recursion.

```text
self.price = value       self._price = value
        |                         |
        v                         v
calls property setter      stores backing value
```

### 3.2 Why the backing attribute matters

This is incorrect:

```python
@price.setter
def price(self, value):
    """Incorrect example: this recursively calls the setter."""
    self.price = value
```

The assignment to `self.price` re-enters the setter repeatedly. Use a different backing name such as `_price`.

## 4. Validation Belongs Close to the Data

A property setter is a useful place for validation when every assignment must obey the same rule. That way, callers cannot bypass the rule simply by choosing a different code path that assigns the attribute.

For a price, the class might check:

- The value is numeric.
- The value is not a Boolean (because `bool` is a subclass of `int` in Python).
- The value is not negative.
- The value meets the application's chosen precision rules.

The following example uses a simple integer amount to keep the lesson focused. Real financial systems should define currency and precision requirements explicitly.

```python
class PriceLabel:
    """Store a non-negative whole-number price."""

    def __init__(self, amount):
        """Initialize the amount through its validating property."""
        self.amount = amount

    @property
    def amount(self):
        """Return the accepted amount."""
        return self._amount

    @amount.setter
    def amount(self, value):
        """Validate and store a non-negative integer amount."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Amount must be an integer.")
        if value < 0:
            raise ValueError("Amount cannot be negative.")
        self._amount = value


label = PriceLabel(799)
print(label.amount)
# Output:
# 799

label.amount = 999
print(label.amount)
# Output:
# 999
```

The setter is executed both during initialization and later reassignment. That consistency is one of the main advantages of properties.

## 5. Read-Only Properties

Sometimes a value should be visible to callers but should not be directly assignable. A property with a getter and no setter is read-only through the normal attribute interface.

For example, an order summary might expose a formatted label calculated from internal fields. Callers should read the label, not replace it with arbitrary text.

```python
class DeliveryWindow:
    """Describe a delivery window using its start and end hours."""

    def __init__(self, start_hour, end_hour):
        """Store the hours that define the delivery window."""
        if not 0 <= start_hour <= 23:
            raise ValueError("Start hour must be from 0 to 23.")
        if not 0 <= end_hour <= 23:
            raise ValueError("End hour must be from 0 to 23.")
        if end_hour <= start_hour:
            raise ValueError("End hour must be later than start hour.")
        self._start_hour = start_hour
        self._end_hour = end_hour

    @property
    def label(self):
        """Return a readable label for the delivery window."""
        return f"{self._start_hour:02d}:00–{self._end_hour:02d}:00"


window = DeliveryWindow(10, 14)
print(window.label)
# Output:
# 10:00–14:00
```

There is no `@label.setter`. Therefore, `window.label = "any time"` raises `AttributeError` in ordinary use.

Read-only properties are not an absolute security boundary. Their purpose is to define a stable, intentional interface and prevent accidental assignment.

## 6. Computed Properties

A computed property derives its result from other attributes instead of storing a duplicate value. This prevents values from drifting out of sync.

For example, a discount amount can be calculated from the original price and discount percentage. Storing all three independently creates a risk that one changes while the others do not.

```text
original price + discount percentage
                |
                v
       computed discount amount
                |
                v
         final selling price
```

```python
class DiscountOffer:
    """Calculate a discounted price from a base price and percentage."""

    def __init__(self, original_price, discount_percent):
        """Store validated inputs for a discount offer."""
        if original_price < 0:
            raise ValueError("Original price cannot be negative.")
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100.")
        self._original_price = original_price
        self._discount_percent = discount_percent

    @property
    def discount_amount(self):
        """Calculate the discount amount without storing a duplicate."""
        return self._original_price * self._discount_percent / 100

    @property
    def final_price(self):
        """Calculate the price after the discount."""
        return self._original_price - self.discount_amount


offer = DiscountOffer(2000, 15)
print(f"Discount: ₹{offer.discount_amount:.2f}")
# Output:
# Discount: ₹300.00

print(f"Final price: ₹{offer.final_price:.2f}")
# Output:
# Final price: ₹1700.00
```

The values are computed whenever the properties are read. If the inputs were mutable through validated properties, the computed values would automatically reflect the latest accepted inputs.

## 7. A Property Can Have a Setter and a Getter

A property does not have to be read-only. Use a setter when callers are allowed to update the value, but only under defined conditions.

This example adds an active/inactive flag to a catalogue listing. The property normalizes and validates the input so the stored state is always a Boolean.

```python
class CatalogueListing:
    """Represent whether a listing is active in the catalogue."""

    def __init__(self, title, active=True):
        """Create a listing with a title and validated active state."""
        self.title = title
        self.active = active

    @property
    def active(self):
        """Return whether the listing is active."""
        return self._active

    @active.setter
    def active(self, value):
        """Require a Boolean value for the active state."""
        if not isinstance(value, bool):
            raise TypeError("Active must be True or False.")
        self._active = value


listing = CatalogueListing("Cotton T-shirt")
print(listing.active)
# Output:
# True

listing.active = False
print(listing.active)
# Output:
# False
```

Validation should be deliberate. Avoid adding setters and checks just because a property can have them. If an attribute has no meaningful rule and direct access is appropriate, a public attribute may be simpler.

## 8. Property Design Choices

Use the following guide when deciding how to expose a value.

| Requirement | Suitable design | Example |
|---|---|---|
| Caller may freely read and change it | Public attribute | `store_name` |
| Implementation detail, not intended as public API | Leading underscore | `_cache` |
| Reduce accidental clashes in subclass internals | Double-leading-underscore name | `__token` |
| Value can be assigned only after validation | Property with setter | `price` |
| Value should be calculated from other data | Computed property | `final_price` |
| Value should be readable but not assigned through the interface | Getter-only property | `label` |

Do not convert every attribute to a property automatically. Start with a simple interface and introduce a property when validation, computation, compatibility, or a read-only contract provides a real benefit.

## 9. Worked Example: `PricingTier`

eCOMMart needs to represent pricing tiers for catalogue products. Each tier has a name, a base price, and a discount percentage. The base price and discount can be updated, but only when they satisfy the rules. The final price should be computed, not stored as a separate value.

### 9.1 Class design

```text
PricingTier
|
+-- _name                 internal stored name
+-- _base_price           validated through a property
+-- _discount_percent     validated through a property
|
+-- name                  read-only property
+-- base_price            getter + validating setter
+-- discount_percent      getter + validating setter
+-- discount_amount       computed property
+-- final_price           computed property
```

### 9.2 Implementation

```python
class PricingTier:
    """Represent a validated catalogue pricing tier."""

    def __init__(self, name, base_price, discount_percent=0):
        """Initialize the tier using its validated property interface."""
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Tier name cannot be empty.")
        self._name = cleaned_name
        self.base_price = base_price
        self.discount_percent = discount_percent

    @property
    def name(self):
        """Return the tier's display name."""
        return self._name

    @property
    def base_price(self):
        """Return the accepted base price in rupees."""
        return self._base_price

    @base_price.setter
    def base_price(self, value):
        """Accept only non-negative numeric base prices."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Base price must be numeric.")
        if value < 0:
            raise ValueError("Base price cannot be negative.")
        self._base_price = float(value)

    @property
    def discount_percent(self):
        """Return the accepted discount percentage."""
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, value):
        """Accept a discount percentage between 0 and 100."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Discount must be numeric.")
        if not 0 <= value <= 100:
            raise ValueError("Discount must be between 0 and 100.")
        self._discount_percent = float(value)

    @property
    def discount_amount(self):
        """Calculate the discount amount in rupees."""
        return self._base_price * self._discount_percent / 100

    @property
    def final_price(self):
        """Calculate the final price after discount."""
        return self._base_price - self.discount_amount

    def display_summary(self):
        """Return a readable summary of the tier's current pricing."""
        return (
            f"{self.name}: base ₹{self.base_price:.2f}, "
            f"discount {self.discount_percent:.1f}%, "
            f"final ₹{self.final_price:.2f}"
        )


tier = PricingTier("  Standard  ", 2499, 12)
print(tier.display_summary())
# Output:
# Standard: base ₹2499.00, discount 12.0%, final ₹2199.12

tier.discount_percent = 20
print(f"Updated final price: ₹{tier.final_price:.2f}")
# Output:
# Updated final price: ₹1999.20

tier.base_price = 2799
print(f"New final price: ₹{tier.final_price:.2f}")
# Output:
# New final price: ₹2239.20
```

### 9.3 Try invalid assignments

```python
tier.base_price = -50
# Output:
# ValueError: Base price cannot be negative.
```

The exception stops the assignment. The setter does not store the invalid value.

```python
tier.discount_percent = 150
# Output:
# ValueError: Discount must be between 0 and 100.
```

The class centralizes its business rules. Callers do not need to remember every validation rule each time they update a tier.

### 9.4 Read-only values

```python
print(tier.name)
# Output:
# Standard

tier.name = "Premium"
# Output:
# AttributeError: property 'name' of 'PricingTier' object has no setter
```

The name is read-only through the class's public interface. If renaming becomes a supported business operation later, the class can deliberately introduce a validated setter or a dedicated method.

### 9.5 Inspect the stored data

```python
print(tier.__dict__)
# Output:
# {'_name': 'Standard', '_base_price': 2799.0, '_discount_percent': 20.0}
```

The public properties are descriptors on the class; the actual values are held in backing attributes on the instance. This is why `__dict__` shows `_base_price`, rather than a separate stored `base_price` property value.

## 10. Common Mistakes

### Mistake 1: Assigning to the property inside its own setter

```python
@base_price.setter
def base_price(self, value):
    """Incorrect: this recursively invokes the setter."""
    self.base_price = value
```

Use `self._base_price = value` after validation.

### Mistake 2: Assuming `_attribute` is inaccessible

A leading underscore is a convention, not an access-control wall. It signals that callers should generally avoid depending on the name.

### Mistake 3: Treating name mangling as security

Double-leading-underscore names are transformed to reduce accidental clashes. They are not encrypted and do not hide secrets from determined code.

### Mistake 4: Duplicating a value that can be calculated

If `final_price` is always based on `base_price` and `discount_percent`, calculate it as a property rather than maintaining a separate stored field that might become stale.

### Mistake 5: Overengineering every attribute

A property is most useful when it protects a rule, computes a value, or establishes a deliberate interface. Do not add complexity without a reason.

### Mistake 6: Forgetting that initialization can call setters

In `PricingTier.__init__`, assigning `self.base_price = base_price` invokes the setter. This is intentional: initial values receive the same validation as later updates.

## 11. Quick Knowledge Check

1. What does a single leading underscore communicate to other Python developers?
2. Does name mangling make an attribute secret or encrypted?
3. Why should a property's setter store data in `_price` rather than assign to `price` again?
4. When is a getter-only property useful?
5. Why is `final_price` a good candidate for a computed property?
6. What happens if a property setter raises `ValueError`?
7. Why is a property useful when a value must always follow a business rule?

## 12. Practice Tasks

Complete exactly these three tasks. Use the requirements as a checklist and test valid and invalid inputs.

### Task 1 — `EventPass`

**Goal:** Create an event pass with a controlled price.

Requirements:

1. Create an `EventPass` class.
2. Give it a class docstring and a docstring for every method.
3. Store `event_name` as a public attribute.
4. Store the actual price in `_price`.
5. Create a `price` property with a getter and setter.
6. Accept only non-negative numeric prices; reject Booleans and non-numeric values.
7. Raise `ValueError` for a negative price and `TypeError` for an invalid type.
8. Create one valid pass costing ₹1,250 and print its price.
9. Update the price to ₹1,500 and print it.
10. Attempt to set the price to `-1` inside a `try`/`except` block and print the error message.

Expected successful output:

```text
1250
1500
Price cannot be negative.
```

### Task 2 — `CourierParcel`

**Goal:** Expose a calculated shipping label without allowing arbitrary assignment.

Requirements:

1. Create a `CourierParcel` class with a class docstring and docstrings for all methods.
2. Accept `tracking_code`, `weight_kg`, and `priority` in `__init__`.
3. Store the tracking code as `_tracking_code`, and expose it through a getter-only `tracking_code` property.
4. Validate that `tracking_code` is a non-empty string after trimming whitespace.
5. Validate that `weight_kg` is numeric and greater than zero.
6. Validate that `priority` is either `"standard"` or `"express"`.
7. Create a read-only `shipping_label` property returning a string such as `EXPRESS | PKG-204 | 2.5 kg`.
8. Create a parcel with tracking code `" PKG-204 "`, weight `2.5`, and priority `"express"`.
9. Print `parcel.tracking_code` and `parcel.shipping_label`.
10. Try to assign a new tracking code and catch the resulting `AttributeError`.

Expected successful output:

```text
PKG-204
EXPRESS | PKG-204 | 2.5 kg
```

### Task 3 — `SubscriptionPlan`

**Goal:** Build a small encapsulated pricing model with multiple validated and computed properties.

Requirements:

1. Create a `SubscriptionPlan` class with a class docstring and docstrings for every method.
2. Accept `plan_name`, `monthly_fee`, and `discount_percent`.
3. Trim `plan_name` and reject an empty name.
4. Expose `plan_name` as a getter-only property.
5. Use a `monthly_fee` property with a getter and setter. Accept only non-negative numeric values and reject Booleans.
6. Use a `discount_percent` property with a getter and setter. Accept numeric values from `0` to `100`, inclusive, and reject Booleans.
7. Store the values in backing attributes, not by recursively assigning to the properties.
8. Add a computed `monthly_savings` property.
9. Add a computed `discounted_monthly_fee` property.
10. Add a `summary()` method returning the plan name, monthly fee, discount, savings, and discounted fee.
11. Create a plan named `"Business Plus"` with a monthly fee of ₹2,000 and a 15% discount.
12. Print its summary.
13. Update the discount to 25% and print the updated discounted monthly fee.
14. Test at least one invalid assignment for each writable property and handle the exceptions.

Expected key values:

```text
Monthly fee: ₹2000.00
Discount: 15.0%
Monthly savings: ₹300.00
Discounted monthly fee: ₹1700.00
Updated discounted monthly fee: ₹1500.00
```

## Summary

| Concept | What to remember |
|---|---|
| Encapsulation | Keep data and its rules together behind a clear interface. |
| Public attribute | A normal name intended for direct use by callers. |
| Leading underscore | A convention marking an implementation detail. |
| Name mangling | Transforms double-leading-underscore names to reduce accidental clashes. |
| Property getter | Lets a method be accessed using attribute syntax. |
| Property setter | Validates and controls assignments to a property. |
| Backing attribute | Stores the underlying value, often using a leading underscore. |
| Read-only property | Provides a value without a normal assignment interface. |
| Computed property | Calculates a value from other data rather than storing a duplicate. |
| Validation | Reject invalid data before it becomes part of the object's state. |

*Next: 08_Inheritance.md*
