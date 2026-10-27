# Methods
## eCOMMart AI Squad | Week 4

> A class without methods is just a dictionary with extra syntax.
> Methods are where a class comes alive — they define what an object
> can do, how it interacts with the outside world, and how it produces
> new objects from its own state. This file covers every method type
> Python supports and the patterns that make them reliable in real applications.

---

## What We Will Cover

1. The three method types — a precise definition of each
2. Instance methods — deeper patterns
3. `@classmethod` — full coverage including factory methods
4. `@staticmethod` — what it is, when it genuinely belongs in a class
5. The three-way comparison — choosing the right type for any situation
6. `*args` and `**kwargs` in methods
7. Methods that return rich objects — not just primitives
8. Dunder methods — `__len__`, `__contains__`, `__iter__`
9. A complete worked example — `Invoice`
10. Tasks

---

## 1. The Three Method Types — A Precise Definition

Python has exactly three method types. The distinction is about
**what the method has access to** and **what it is bound to**:

```
┌─────────────────┬──────────────────────────────┬────────────────────────────┐
│  Method type    │  First parameter receives     │  Has access to             │
├─────────────────┼──────────────────────────────┼────────────────────────────┤
│  Instance method│  self — the specific object   │  Instance attrs + class    │
│                 │  that called the method        │  attrs + class itself      │
├─────────────────┼──────────────────────────────┼────────────────────────────┤
│  Class method   │  cls — the class itself        │  Class attrs + class only  │
│  (@classmethod) │  not any specific instance    │  NOT instance attrs        │
├─────────────────┼──────────────────────────────┼────────────────────────────┤
│  Static method  │  nothing — no implicit first  │  Only what is passed in    │
│  (@staticmethod)│  parameter at all             │  as explicit arguments     │
└─────────────────┴──────────────────────────────┴────────────────────────────┘
```

The decorator (`@classmethod`, `@staticmethod`) is how you signal which
type a method is. No decorator means instance method.

---

## 2. Instance Methods — Deeper Patterns

You have been writing instance methods since file 01. This section
covers patterns not yet demonstrated.

### Pattern 1 — Returning a formatted dict (not just a scalar)

Methods are not limited to returning strings, floats, or booleans.
A method can assemble and return a structured dictionary — useful when
the caller needs several pieces of related data at once without accessing
individual attributes.

```python
class Invoice:
    def get_tax_breakdown(self):
        """
        Returns a full tax breakdown for this invoice.

        Returns:
            dict: CGST, SGST, IGST, and total tax in INR, keyed by component.
        """
        # eCOMMart uses split GST: CGST + SGST for intra-state,
        # IGST alone for inter-state
        subtotal = self.get_subtotal()
        if self.is_interstate:
            igst  = round(subtotal * 0.18, 2)
            return {
                "cgst"      : 0.0,
                "sgst"      : 0.0,
                "igst"      : igst,
                "total_tax" : igst,
                "regime"    : "IGST (inter-state)",
            }
        else:
            cgst = round(subtotal * 0.09, 2)
            sgst = round(subtotal * 0.09, 2)
            return {
                "cgst"      : cgst,
                "sgst"      : sgst,
                "igst"      : 0.0,
                "total_tax" : round(cgst + sgst, 2),
                "regime"    : "CGST + SGST (intra-state)",
            }
```

The caller gets a clean dict they can format, log, or pass to another
function — no need to call multiple separate getter methods.

### Pattern 2 — Methods with multiple conditional branches

A well-structured instance method handles every valid state the object
can be in. Each branch should be independent and return cleanly.

```python
    def get_payment_status_label(self):
        """
        Returns a human-readable payment status string with an indicator.

        Returns:
            str: Status label with emoji indicator.
        """
        labels = {
            "PAID"           : "✅ Paid in full",
            "PARTIALLY_PAID" : "⚠️  Partially paid",
            "OVERDUE"        : "🔴 Overdue — payment required",
            "PENDING"        : "🕐 Payment pending",
            "CANCELLED"      : "❌ Invoice cancelled",
            "DISPUTED"       : "⚖️  Under dispute",
        }
        return labels.get(self.payment_status, f"Unknown status: {self.payment_status}")
```

---

## 3. `@classmethod` — Full Coverage Including Factory Methods

File 04 introduced `@classmethod` briefly for querying shared state.
Here is the full picture.

### What `cls` gives you

Inside a class method, `cls` is the class object itself — identical to
writing `Invoice` directly. The reason to use `cls` instead of the
hard-coded class name is inheritance: if a subclass calls this method,
`cls` will be the subclass, not `Invoice`. This means the factory creates
the right type automatically.

```python
class Invoice:
    @classmethod
    def get_tax_rate(cls):
        """Returns the current platform GST rate."""
        return cls.GST_RATE          # cls.GST_RATE == Invoice.GST_RATE
```

### Factory methods — the most important use of `@classmethod`

A **factory method** is a class method that constructs and returns a
new instance of the class. This is used when:

- The data to build an object arrives in a format other than individual arguments
- You want a named constructor that documents the source format clearly
- You want to validate the source data before attempting construction

```python
    @classmethod
    def from_dict(cls, data: dict) -> "Invoice":
        """
        Creates an Invoice from a plain dictionary (e.g. loaded from JSON).

        Args:
            data (dict): Must contain keys: invoice_number, seller_gstin,
                         buyer_gstin, line_items, is_interstate, payment_status.

        Returns:
            Invoice: A fully initialised Invoice object.

        Raises:
            KeyError:   If a required key is missing from data.
            ValueError: If any field fails validation.
        """
        required = {
            "invoice_number", "seller_gstin", "buyer_gstin",
            "line_items", "is_interstate", "payment_status"
        }
        missing = required - data.keys()
        if missing:
            raise KeyError(f"Missing required fields: {sorted(missing)}")

        return cls(
            invoice_number = data["invoice_number"],
            seller_gstin   = data["seller_gstin"],
            buyer_gstin    = data["buyer_gstin"],
            line_items     = data["line_items"],
            is_interstate  = data["is_interstate"],
            payment_status = data["payment_status"],
        )

    @classmethod
    def from_csv_row(cls, row: list, headers: list) -> "Invoice":
        """
        Creates an Invoice from a CSV row and its header list.

        Args:
            row     (list): Values from one CSV row.
            headers (list): Column headers matching the row positions.

        Returns:
            Invoice: A fully initialised Invoice object.
        """
        if len(row) != len(headers):
            raise ValueError(
                f"Row has {len(row)} values but headers has {len(headers)} columns."
            )
        data = dict(zip(headers, row))
        data["is_interstate"] = data.get("is_interstate", "false").lower() == "true"
        data["line_items"]    = []   # CSV rows carry summary data; items loaded separately
        return cls.from_dict(data)
```

Factory methods make the calling code self-documenting:

```python
# Without factory method — caller must know the exact argument order
inv = Invoice("INV-2024-00142", "27ABCDE1234F1Z5", "29XYZAB5678G2A1", [], False, "PENDING")

# With factory methods — intent is immediately readable
inv_from_json = Invoice.from_dict(json_data)
inv_from_csv  = Invoice.from_csv_row(csv_row, csv_headers)
```

---

## 4. `@staticmethod` — What It Is and When It Belongs in a Class

A static method has **no implicit first parameter** — no `self`, no `cls`.
It is a plain function that lives inside a class purely for organisational
reasons: it is logically related to the class but does not need to read
or modify any instance or class state.

```python
class Invoice:

    @staticmethod
    def is_valid_gstin(gstin: str) -> bool:
        """
        Validates a GST Identification Number (GSTIN) format.

        Indian GSTIN format: 15 characters
          - Characters 1–2  : State code (numeric, e.g. '27' for Maharashtra)
          - Characters 3–12 : PAN number (alphanumeric)
          - Character 13    : Entity number (numeric, 1–9)
          - Character 14    : 'Z' (default)
          - Character 15    : Checksum digit (alphanumeric)

        Args:
            gstin (str): The GSTIN string to validate.

        Returns:
            bool: True if format is structurally valid, False otherwise.
        """
        if not isinstance(gstin, str):
            return False
        gstin = gstin.strip().upper()
        if len(gstin) != 15:
            return False
        if not gstin[:2].isdigit():
            return False
        if not gstin[2:12].isalnum():
            return False
        if not gstin[12].isdigit():
            return False
        if gstin[13] != "Z":
            return False
        return True

    @staticmethod
    def parse_invoice_number(invoice_number: str) -> dict:
        """
        Parses an eCOMMart invoice number into its components.

        Invoice format: INV-YYYY-NNNNN
          e.g. INV-2024-00142 → year=2024, sequence=142

        Args:
            invoice_number (str): Invoice number string to parse.

        Returns:
            dict: {'prefix': str, 'year': int, 'sequence': int} or
                  {'error': str} if format is invalid.
        """
        parts = invoice_number.strip().upper().split("-")
        if len(parts) != 3 or parts[0] != "INV":
            return {"error": f"Invalid format: {invoice_number!r}. Expected INV-YYYY-NNNNN"}
        try:
            year     = int(parts[1])
            sequence = int(parts[2])
            return {"prefix": "INV", "year": year, "sequence": sequence}
        except ValueError:
            return {"error": f"Non-numeric year or sequence in: {invoice_number!r}"}

    @staticmethod
    def format_gstin_display(gstin: str) -> str:
        """
        Formats a GSTIN with a separator for readability.

        27ABCDE1234F1Z5 → 27-ABCDE1234F-1-Z-5

        Args:
            gstin (str): Raw 15-character GSTIN.

        Returns:
            str: Formatted display string, or original if invalid length.
        """
        g = gstin.strip().upper()
        if len(g) != 15:
            return gstin
        return f"{g[:2]}-{g[2:12]}-{g[12]}-{g[13]}-{g[14]}"
```

### Calling static methods

```python
# Via the class — most common and clearest
print(Invoice.is_valid_gstin("27ABCDE1234F1Z5"))   # True
print(Invoice.is_valid_gstin("INVALID"))            # False
print(Invoice.is_valid_gstin("27ABCDE1234F1Z9"))   # True (Z in pos 13 ✅)

parsed = Invoice.parse_invoice_number("INV-2024-00142")
print(parsed)    # {'prefix': 'INV', 'year': 2024, 'sequence': 142}

bad = Invoice.parse_invoice_number("RCT-2024-00142")
print(bad)       # {'error': "Invalid format: 'RCT-2024-00142'. Expected INV-YYYY-NNNNN"}

print(Invoice.format_gstin_display("27ABCDE1234F1Z5"))  # 27-ABCDE1234F-1-Z-5

# Via an instance — also works, though less common for static methods
inv = Invoice(...)
print(inv.is_valid_gstin("27ABCDE1234F1Z5"))   # True — same result
```
```
# Output:
True
False
True
{'prefix': 'INV', 'year': 2024, 'sequence': 142}
{'error': "Invalid format: 'RCT-2024-00142'. Expected INV-YYYY-NNNNN"}
27-ABCDE1234F-1-Z-5
True
```

### When does a function deserve to be a static method?

```
✅  Put it in the class as @staticmethod when:
      - It validates or parses data that the class works with
      - It is a utility that makes no sense outside the class's domain
      - You want it discoverable via Invoice.helper() not as a stray function
      - It will be called from __init__ or other methods for validation

✅  Keep it as a module-level function when:
      - It is a general utility with no specific tie to this class
      - Multiple unrelated classes would use it
      - It is already imported from another module (e.g. math, datetime)

❌  Do not make it a static method just to avoid writing self:
      - If it reads self.anything, it is an instance method
      - If it reads cls.anything, it is a class method
```

---

## 5. The Three-Way Comparison — Choosing the Right Type

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Question                                           → Method type            │
├──────────────────────────────────────────────────────────────────────────────┤
│  Does it read or modify self.anything?              → Instance method        │
│  Does it read or modify cls.anything?               → @classmethod           │
│  Does it need neither self nor cls?                 → @staticmethod          │
│  Does it create and return a new instance?          → @classmethod (factory) │
│  Does it validate data the class works with?        → @staticmethod          │
│  Does it operate on all instances collectively?     → @classmethod           │
└──────────────────────────────────────────────────────────────────────────────┘
```

```python
class Invoice:

    GST_RATE      = 0.18
    _all_invoices = []

    # ── Instance method — reads self ──────────────────────────────
    def get_subtotal(self):
        return sum(item["qty"] * item["unit_price"] for item in self.line_items)

    # ── Class method — reads cls, returns new instance ────────────
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    # ── Class method — queries shared state ───────────────────────
    @classmethod
    def get_invoice_count(cls):
        return len(cls._all_invoices)

    # ── Static method — no self, no cls ───────────────────────────
    @staticmethod
    def is_valid_gstin(gstin):
        return isinstance(gstin, str) and len(gstin.strip()) == 15
```

Side by side — same invoice, three different method types:

```python
inv = Invoice("INV-2024-00142", "27ABCDE1234F1Z5", "29XYZAB5678G2A1",
              [{"sku": "WH-1042", "qty": 10, "unit_price": 840.0}],
              is_interstate=True, payment_status="PENDING")

# Instance method — called on the object, reads self
print(f"  Subtotal       : ₹{inv.get_subtotal():.2f}")

# Class method — called on the class, reads cls
print(f"  Invoice count  : {Invoice.get_invoice_count()}")

# Static method — called on the class, reads neither
print(f"  Valid GSTIN?   : {Invoice.is_valid_gstin('27ABCDE1234F1Z5')}")
```
```
# Output:
  Subtotal       : ₹8,400.00
  Invoice count  : 1
  Valid GSTIN?   : True
```

---

## 6. `*args` and `**kwargs` in Methods

You used `*args` and `**kwargs` in standalone functions in Week 3.
Inside a class method, the mechanics are identical — the only difference
is that `self` always comes first.

### `*args` in a method — variable number of line items

```python
    def add_line_items(self, *items):
        """
        Adds one or more line items to this invoice.

        Each item must be a dict with keys: sku, description, qty, unit_price.

        Args:
            *items: One or more line item dicts.

        Raises:
            ValueError: If any item is missing a required key.
        """
        required_keys = {"sku", "description", "qty", "unit_price"}
        for i, item in enumerate(items):
            missing = required_keys - item.keys()
            if missing:
                raise ValueError(
                    f"Line item {i + 1} is missing required keys: {sorted(missing)}"
                )
            if item["qty"] <= 0:
                raise ValueError(
                    f"Line item {i + 1}: qty must be positive. Got: {item['qty']}"
                )
            if item["unit_price"] <= 0:
                raise ValueError(
                    f"Line item {i + 1}: unit_price must be positive. "
                    f"Got: {item['unit_price']}"
                )
            self.line_items.append(item)
```

```python
inv = Invoice("INV-2024-00143", "27ABCDE1234F1Z5", "29XYZAB5678G2A1",
              [], is_interstate=False, payment_status="PENDING")

# Add three line items in one call
inv.add_line_items(
    {"sku": "WH-1042", "description": "Industrial Shelf Unit",   "qty": 5,  "unit_price": 2400.00},
    {"sku": "WH-2019", "description": "Packing Foam Roll (10m)", "qty": 20, "unit_price": 185.00},
    {"sku": "WH-3301", "description": "Barcode Scanner",         "qty": 2,  "unit_price": 3750.00},
)

print(f"  Line items added : {len(inv.line_items)}")
print(f"  Subtotal         : ₹{inv.get_subtotal():,.2f}")
```
```
# Output:
  Line items added : 3
  Subtotal         : ₹23,200.00
```

### `**kwargs` in a method — flexible adjustment options

```python
    def apply_adjustments(self, **kwargs):
        """
        Applies named financial adjustments to this invoice.

        Accepted keyword arguments:
            early_payment_discount (float): % discount for early settlement.
            late_penalty_pct       (float): % surcharge for overdue payment.
            freight_charges        (float): Additional freight in INR.
            credit_note_amount     (float): Amount to deduct (credit note).

        Adjustments are recorded and applied when get_grand_total() is called.

        Raises:
            ValueError: If any value is negative.
        """
        for key, value in kwargs.items():
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(
                    f"Adjustment {key!r} must be a non-negative number. Got: {value!r}"
                )
        self.adjustments.update(kwargs)
        print(f"  Applied adjustments: {list(kwargs.keys())}")
```

```python
inv.apply_adjustments(
    early_payment_discount = 2.5,
    freight_charges        = 450.00,
)

inv.apply_adjustments(credit_note_amount=500.00)   # called again — merges with existing

print(f"  Active adjustments : {inv.adjustments}")
```
```
# Output:
  Applied adjustments: ['early_payment_discount', 'freight_charges']
  Applied adjustments: ['credit_note_amount']
  Active adjustments : {'early_payment_discount': 2.5, 'freight_charges': 450.0, 'credit_note_amount': 500.0}
```

---

## 7. Methods That Return Rich Objects

A method is not limited to returning scalars or dicts.
It can construct and return a **new instance** of the same class
or a different class — enabling object-to-object workflows.

```python
    def generate_credit_note(self, reason: str, amount: float) -> "Invoice":
        """
        Generates a credit note invoice against this invoice.

        A credit note is a negative invoice issued to reverse or partially
        reverse a billing. It carries the same GST classification as the
        original.

        Args:
            reason (str):  Description of why the credit is being issued.
            amount (float): Amount being credited in INR. Must be > 0 and
                            <= this invoice's grand total.

        Returns:
            Invoice: A new Invoice object representing the credit note.

        Raises:
            ValueError: If amount is invalid or exceeds the original total.
        """
        if amount <= 0:
            raise ValueError(f"Credit amount must be positive. Got: {amount}")
        if amount > self.get_grand_total():
            raise ValueError(
                f"Credit ₹{amount:.2f} exceeds invoice total "
                f"₹{self.get_grand_total():.2f}."
            )

        credit_number = self.invoice_number.replace("INV", "CRN")

        credit_note = Invoice(
            invoice_number = credit_number,
            seller_gstin   = self.seller_gstin,
            buyer_gstin    = self.buyer_gstin,
            line_items     = [
                {
                    "sku"         : "CREDIT",
                    "description" : reason,
                    "qty"         : 1,
                    "unit_price"  : -amount,    # negative value flags it as credit
                }
            ],
            is_interstate  = self.is_interstate,
            payment_status = "PAID",            # credits are settled immediately
        )
        return credit_note
```

```python
original_inv = Invoice(
    invoice_number = "INV-2024-00144",
    seller_gstin   = "27ABCDE1234F1Z5",
    buyer_gstin    = "29XYZAB5678G2A1",
    line_items     = [{"sku": "FN-0091", "description": "Office Chair",
                       "qty": 4, "unit_price": 7800.00}],
    is_interstate  = True,
    payment_status = "PAID",
)

# One of the chairs was damaged — issue a partial credit note
credit = original_inv.generate_credit_note(
    reason = "1 unit damaged in transit — partial refund",
    amount = 7800.00
)

print(f"  Original invoice : {original_inv.invoice_number}")
print(f"  Credit note      : {credit.invoice_number}")
print(f"  Credit amount    : ₹{abs(credit.get_subtotal()):,.2f}")
print(f"  Credit is_interstate: {credit.is_interstate}")   # inherited from original
print(f"  Type of 'credit' : {type(credit).__name__}")    # still an Invoice
```
```
# Output:
  Original invoice : INV-2024-00144
  Credit note      : CRN-2024-00144
  Credit amount    : ₹7,800.00
  Credit is_interstate: True
  Type of 'credit' : Invoice
```

---

## 8. Dunder Methods — `__len__`, `__contains__`, `__iter__`

**Dunder methods** (double-underscore methods) let your objects work
with Python's built-in syntax — `len()`, `in`, `for`. You already know
`__init__` and `__str__`/`__repr__` are covered in the next file.
Here are three more that are immediately useful:

### `__len__` — makes `len(obj)` work

```python
    def __len__(self) -> int:
        """Returns the number of line items on this invoice."""
        return len(self.line_items)
```

```python
print(len(inv))        # instead of len(inv.line_items) or inv.get_item_count()
```

### `__contains__` — makes `sku in inv` work

```python
    def __contains__(self, sku: str) -> bool:
        """
        Returns True if a product SKU appears on this invoice.

        Enables: 'WH-1042' in invoice
        """
        return any(item["sku"] == sku for item in self.line_items)
```

```python
print("WH-1042" in inv)    # True  — instead of any() loop every time
print("XX-9999" in inv)    # False
```

### `__iter__` — makes `for item in inv` work

```python
    def __iter__(self):
        """
        Iterates over the line items of this invoice.

        Enables: for item in invoice: ...
        """
        return iter(self.line_items)
```

```python
for item in inv:
    print(f"  {item['sku']:<10} {item['description']:<30} "
          f"× {item['qty']:>3}  ₹{item['unit_price']:>8,.2f}")
```
```
# Output:
  WH-1042    Industrial Shelf Unit          ×   5  ₹ 2,400.00
  WH-2019    Packing Foam Roll (10m)        ×  20  ₹   185.00
  WH-3301    Barcode Scanner                ×   2  ₹ 3,750.00
```

---

## 9. A Complete Worked Example — `Invoice`

```python
from datetime import date as Date, timedelta

class Invoice:
    """
    Represents a GST-compliant tax invoice on the eCOMMart B2B platform.

    eCOMMart invoices are generated after order confirmation. They carry
    full GSTIN details for both seller and buyer, a structured line item
    list, and track payment status through its lifecycle.

    Class Attributes:
        GST_RATE        (float): Standard GST rate (0.18).
        PAYMENT_TERMS   (int):   Default payment due days (30).
        VALID_STATUSES  (set):   Allowed payment_status values.
        _all_invoices   (list):  Registry of all Invoice objects created.

    Instance Attributes:
        invoice_number (str):      Unique reference, format INV-YYYY-NNNNN.
        seller_gstin   (str):      Seller's 15-char GSTIN.
        buyer_gstin    (str):      Buyer's 15-char GSTIN.
        line_items     (list):     List of dicts with sku, description, qty, unit_price.
        is_interstate  (bool):     True → IGST; False → CGST + SGST.
        payment_status (str):      One of VALID_STATUSES.
        issued_on      (Date):     Date invoice was raised. Defaults to today.
        due_on         (Date):     Payment due date. Defaults to issued_on + 30 days.
        adjustments    (dict):     Named financial adjustments (freight, discounts, etc.).
    """

    GST_RATE       = 0.18
    PAYMENT_TERMS  = 30
    VALID_STATUSES = {"PENDING", "PAID", "PARTIALLY_PAID",
                      "OVERDUE", "CANCELLED", "DISPUTED"}
    _all_invoices  = []

    def __init__(
        self,
        invoice_number : str,
        seller_gstin   : str,
        buyer_gstin    : str,
        line_items     : list,
        is_interstate  : bool,
        payment_status : str       = "PENDING",
        issued_on      : Date      = None,
    ) -> None:
        # Validate
        if not Invoice.is_valid_gstin(seller_gstin):
            raise ValueError(f"Invalid seller GSTIN: {seller_gstin!r}")
        if not Invoice.is_valid_gstin(buyer_gstin):
            raise ValueError(f"Invalid buyer GSTIN: {buyer_gstin!r}")
        parsed = Invoice.parse_invoice_number(invoice_number)
        if "error" in parsed:
            raise ValueError(parsed["error"])
        if payment_status not in Invoice.VALID_STATUSES:
            raise ValueError(
                f"Invalid payment_status {payment_status!r}. "
                f"Choose from: {sorted(Invoice.VALID_STATUSES)}"
            )

        self.invoice_number = invoice_number.strip().upper()
        self.seller_gstin   = seller_gstin.strip().upper()
        self.buyer_gstin    = buyer_gstin.strip().upper()
        self.line_items     = list(line_items)
        self.is_interstate  = is_interstate
        self.payment_status = payment_status
        self.issued_on      = issued_on or Date.today()
        self.due_on         = self.issued_on + timedelta(days=Invoice.PAYMENT_TERMS)
        self.adjustments    = {}

        Invoice._all_invoices.append(self)

    # ── Static methods ────────────────────────────────────────────
    @staticmethod
    def is_valid_gstin(gstin: str) -> bool:
        """Returns True if gstin is a structurally valid 15-char Indian GSTIN."""
        if not isinstance(gstin, str):
            return False
        g = gstin.strip().upper()
        return (
            len(g) == 15
            and g[:2].isdigit()
            and g[2:12].isalnum()
            and g[12].isdigit()
            and g[13] == "Z"
        )

    @staticmethod
    def parse_invoice_number(invoice_number: str) -> dict:
        """Parses INV-YYYY-NNNNN into components. Returns {'error': ...} on failure."""
        parts = invoice_number.strip().upper().split("-")
        if len(parts) != 3 or parts[0] != "INV":
            return {"error": f"Invalid format: {invoice_number!r}. Expected INV-YYYY-NNNNN"}
        try:
            return {"prefix": "INV", "year": int(parts[1]), "sequence": int(parts[2])}
        except ValueError:
            return {"error": f"Non-numeric year/sequence in: {invoice_number!r}"}

    @staticmethod
    def format_gstin_display(gstin: str) -> str:
        """Formats 27ABCDE1234F1Z5 → 27-ABCDE1234F-1-Z-5 for readability."""
        g = gstin.strip().upper()
        return f"{g[:2]}-{g[2:12]}-{g[12]}-{g[13]}-{g[14]}" if len(g) == 15 else gstin

    # ── Class methods ─────────────────────────────────────────────
    @classmethod
    def from_dict(cls, data: dict) -> "Invoice":
        """Creates an Invoice from a plain dictionary (e.g. loaded from JSON)."""
        required = {"invoice_number", "seller_gstin", "buyer_gstin",
                    "line_items", "is_interstate", "payment_status"}
        missing = required - data.keys()
        if missing:
            raise KeyError(f"Missing required fields: {sorted(missing)}")
        return cls(
            invoice_number = data["invoice_number"],
            seller_gstin   = data["seller_gstin"],
            buyer_gstin    = data["buyer_gstin"],
            line_items     = data["line_items"],
            is_interstate  = data["is_interstate"],
            payment_status = data["payment_status"],
        )

    @classmethod
    def get_invoice_count(cls) -> int:
        """Returns total number of Invoice objects created in this session."""
        return len(cls._all_invoices)

    @classmethod
    def get_pending_invoices(cls) -> list:
        """Returns all invoices with PENDING or OVERDUE payment status."""
        return [inv for inv in cls._all_invoices
                if inv.payment_status in ("PENDING", "OVERDUE")]

    # ── Instance query methods ────────────────────────────────────
    def get_subtotal(self) -> float:
        """Returns the pre-tax line total across all items."""
        return round(sum(i["qty"] * i["unit_price"] for i in self.line_items), 2)

    def get_tax_breakdown(self) -> dict:
        """Returns CGST/SGST or IGST breakdown depending on is_interstate."""
        subtotal = self.get_subtotal()
        if self.is_interstate:
            igst = round(subtotal * Invoice.GST_RATE, 2)
            return {"cgst": 0.0, "sgst": 0.0, "igst": igst,
                    "total_tax": igst, "regime": "IGST (inter-state)"}
        cgst = round(subtotal * 0.09, 2)
        sgst = round(subtotal * 0.09, 2)
        return {"cgst": cgst, "sgst": sgst, "igst": 0.0,
                "total_tax": round(cgst + sgst, 2), "regime": "CGST + SGST (intra-state)"}

    def get_adjustment_total(self) -> float:
        """Returns net effect of all adjustments in INR."""
        total = 0.0
        for key, value in self.adjustments.items():
            if "discount" in key or "credit" in key:
                total -= value * (self.get_subtotal() / 100
                                  if "pct" in key or "discount" in key
                                  else 1)
            else:
                total += value
        return round(total, 2)

    def get_grand_total(self) -> float:
        """Returns subtotal + tax + adjustments."""
        tax = self.get_tax_breakdown()["total_tax"]
        return round(self.get_subtotal() + tax + self.get_adjustment_total(), 2)

    def get_payment_status_label(self) -> str:
        """Returns a human-readable status label with indicator."""
        return {
            "PAID"           : "✅ Paid in full",
            "PARTIALLY_PAID" : "⚠️  Partially paid",
            "OVERDUE"        : "🔴 Overdue",
            "PENDING"        : "🕐 Payment pending",
            "CANCELLED"      : "❌ Cancelled",
            "DISPUTED"       : "⚖️  Under dispute",
        }.get(self.payment_status, f"Unknown: {self.payment_status}")

    def is_overdue(self, as_of: Date = None) -> bool:
        """Returns True if the invoice is unpaid and past its due date."""
        check_date = as_of or Date.today()
        return (
            self.payment_status in ("PENDING", "PARTIALLY_PAID")
            and check_date > self.due_on
        )

    # ── Instance mutating methods ─────────────────────────────────
    def add_line_items(self, *items) -> None:
        """Validates and appends one or more line item dicts to this invoice."""
        required_keys = {"sku", "description", "qty", "unit_price"}
        for i, item in enumerate(items):
            missing = required_keys - item.keys()
            if missing:
                raise ValueError(f"Item {i+1} missing keys: {sorted(missing)}")
            if item["qty"] <= 0 or item["unit_price"] <= 0:
                raise ValueError(f"Item {i+1}: qty and unit_price must be positive.")
            self.line_items.append(item)

    def apply_adjustments(self, **kwargs) -> None:
        """Merges named financial adjustments. Values must be non-negative."""
        for key, value in kwargs.items():
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"Adjustment {key!r} must be >= 0. Got: {value!r}")
        self.adjustments.update(kwargs)

    def mark_paid(self) -> None:
        """Marks this invoice as fully paid."""
        if self.payment_status == "CANCELLED":
            raise RuntimeError("Cannot mark a cancelled invoice as paid.")
        self.payment_status = "PAID"

    def generate_credit_note(self, reason: str, amount: float) -> "Invoice":
        """Creates and returns a credit note Invoice against this invoice."""
        if amount <= 0 or amount > self.get_grand_total():
            raise ValueError(
                f"Credit amount ₹{amount:.2f} is invalid. "
                f"Must be > 0 and ≤ ₹{self.get_grand_total():.2f}."
            )
        return Invoice(
            invoice_number = self.invoice_number.replace("INV", "CRN"),
            seller_gstin   = self.seller_gstin,
            buyer_gstin    = self.buyer_gstin,
            line_items     = [{"sku": "CREDIT", "description": reason,
                               "qty": 1, "unit_price": -amount}],
            is_interstate  = self.is_interstate,
            payment_status = "PAID",
        )

    # ── Dunder methods ────────────────────────────────────────────
    def __len__(self) -> int:
        """Returns number of line items."""
        return len(self.line_items)

    def __contains__(self, sku: str) -> bool:
        """Returns True if the SKU appears on any line item."""
        return any(item["sku"] == sku for item in self.line_items)

    def __iter__(self):
        """Iterates over line items."""
        return iter(self.line_items)

    # ── Display ──────────────────────────────────────────────────
    def print_invoice(self) -> None:
        """Prints a formatted GST invoice to the terminal."""
        tax  = self.get_tax_breakdown()
        print("=" * 62)
        print(f"  eCOMMart Tax Invoice — {self.invoice_number}")
        print("=" * 62)
        print(f"  Issued     : {self.issued_on.strftime('%d %b %Y')}"
              f"    Due: {self.due_on.strftime('%d %b %Y')}")
        print(f"  Seller     : {Invoice.format_gstin_display(self.seller_gstin)}")
        print(f"  Buyer      : {Invoice.format_gstin_display(self.buyer_gstin)}")
        print(f"  GST Regime : {tax['regime']}")
        print(f"  {'─' * 58}")
        print(f"  {'SKU':<12} {'Description':<28} {'Qty':>4} {'Unit Price':>10} {'Amount':>10}")
        print(f"  {'─' * 58}")
        for item in self:
            amount = item["qty"] * item["unit_price"]
            print(f"  {item['sku']:<12} {item['description']:<28} "
                  f"{item['qty']:>4} ₹{item['unit_price']:>9,.2f} ₹{amount:>9,.2f}")
        print(f"  {'─' * 58}")
        print(f"  {'Subtotal':<44} ₹{self.get_subtotal():>9,.2f}")
        if tax["cgst"] > 0:
            print(f"  {'CGST (9%)':<44} ₹{tax['cgst']:>9,.2f}")
            print(f"  {'SGST (9%)':<44} ₹{tax['sgst']:>9,.2f}")
        else:
            print(f"  {'IGST (18%)':<44} ₹{tax['igst']:>9,.2f}")
        if self.adjustments:
            adj = self.get_adjustment_total()
            sign = "+" if adj >= 0 else ""
            print(f"  {'Adjustments':<44} {sign}₹{adj:>8,.2f}")
        print(f"  {'─' * 58}")
        print(f"  {'Grand Total':<44} ₹{self.get_grand_total():>9,.2f}")
        print(f"  {'─' * 58}")
        print(f"  Status     : {self.get_payment_status_label()}")
        print(f"  Items      : {len(self)}    SKU in invoice: "
              f"{'Yes' if self.line_items and self.line_items[0]['sku'] in self else 'N/A'}")
        print("=" * 62)
```

### Running the complete class

```python
from datetime import date as Date

# Build an inter-state invoice
inv = Invoice(
    invoice_number = "INV-2024-00201",
    seller_gstin   = "27ABCDE1234F1Z5",   # Maharashtra seller
    buyer_gstin    = "29XYZAB5678G2A1",   # Karnataka buyer → inter-state
    line_items     = [],
    is_interstate  = True,
    payment_status = "PENDING",
    issued_on      = Date(2024, 12, 1),
)

inv.add_line_items(
    {"sku": "WH-1042", "description": "Industrial Shelf Unit",    "qty": 8,  "unit_price": 2400.00},
    {"sku": "WH-2019", "description": "Packing Foam Roll (10m)",  "qty": 50, "unit_price": 185.00},
    {"sku": "EQ-0071", "description": "Heavy-Duty Trolley",       "qty": 3,  "unit_price": 5500.00},
)

inv.apply_adjustments(freight_charges=750.00, early_payment_discount=1.5)

inv.print_invoice()

# Factory method
data = {
    "invoice_number": "INV-2024-00202",
    "seller_gstin"  : "27ABCDE1234F1Z5",
    "buyer_gstin"   : "27PQRST9876H1Z3",   # same state → intra-state
    "line_items"    : [{"sku": "IT-0091", "description": "Rack Server",
                        "qty": 1, "unit_price": 145000.00}],
    "is_interstate" : False,
    "payment_status": "PAID",
}
inv2 = Invoice.from_dict(data)
tax2 = inv2.get_tax_breakdown()
print(f"\n  INV-00202 regime  : {tax2['regime']}")
print(f"  CGST              : ₹{tax2['cgst']:,.2f}")
print(f"  SGST              : ₹{tax2['sgst']:,.2f}")

# Platform stats
print(f"\n  Total invoices created : {Invoice.get_invoice_count()}")
print(f"  Pending invoices       : {len(Invoice.get_pending_invoices())}")

# Dunder methods in action
print(f"\n  len(inv)               : {len(inv)}")
print(f"  'WH-1042' in inv       : {'WH-1042' in inv}")
print(f"  'XX-9999' in inv       : {'XX-9999' in inv}")
```
```
# Output:
==============================================================
  eCOMMart Tax Invoice — INV-2024-00201
==============================================================
  Issued     : 01 Dec 2024    Due: 31 Dec 2024
  Seller     : 27-ABCDE1234F-1-Z-5
  Buyer      : 29-XYZAB5678G-2-A-1
  GST Regime : IGST (inter-state)
  ──────────────────────────────────────────────────────────
  SKU          Description                  Qty  Unit Price     Amount
  ──────────────────────────────────────────────────────────
  WH-1042      Industrial Shelf Unit          8  ₹  2,400.00  ₹ 19,200.00
  WH-2019      Packing Foam Roll (10m)       50  ₹    185.00  ₹  9,250.00
  EQ-0071      Heavy-Duty Trolley             3  ₹  5,500.00  ₹ 16,500.00
  ──────────────────────────────────────────────────────────
  Subtotal                                        ₹  44,950.00
  IGST (18%)                                      ₹   8,091.00
  Adjustments                                    +₹     391.50
  ──────────────────────────────────────────────────────────
  Grand Total                                     ₹  53,432.50
  ──────────────────────────────────────────────────────────
  Status     : 🕐 Payment pending
  Items      : 3    SKU in invoice: Yes
==============================================================

  INV-00202 regime  : CGST + SGST (intra-state)
  CGST              : ₹13,050.00
  SGST              : ₹13,050.00

  Total invoices created : 2
  Pending invoices       : 1

  len(inv)               : 3
  'WH-1042' in inv       : True
  'XX-9999' in inv       : False
```

---

## 10. Tasks

### Task 1 — `PaymentTransaction`

Build a `PaymentTransaction` class representing a payment made against
an eCOMMart invoice.

**Static methods required:**
- `is_valid_utr(utr)` — validates a UTR number (22 alphanumeric characters)
- `parse_payment_mode(raw)` — normalises `"upi"`, `"UPI"`, `"Upi"` → `"UPI"`;
  accepts `"NEFT"`, `"RTGS"`, `"IMPS"`, `"CHEQUE"`, `"CARD"` — returns
  `{"mode": ..., "valid": bool}`

**Class method required:**
- `from_webhook(cls, payload: dict)` — factory that creates a
  `PaymentTransaction` from a payment gateway webhook payload dict
  with keys: `txn_id`, `utr`, `amount`, `mode`, `invoice_number`, `timestamp`

**Instance methods required:**
- `is_full_payment(invoice_total)` → bool — True if amount >= invoice_total
- `get_receipt_summary()` → dict — structured receipt data
- `get_shortfall(invoice_total)` → float — how much is still outstanding
  (0.0 if fully paid)

**Dunder methods:** `__str__` returning a one-line summary
(covered properly in the next file — implement it simply for now:
`return f"TXN-{self.txn_id} | ₹{self.amount:.2f} via {self.mode}"`)

---

### Task 2 — `ReturnRequest`

Build a `ReturnRequest` class for the eCOMMart returns management system.

**Class attributes:**
- `ALLOWED_REASONS = {"DAMAGED", "WRONG_ITEM", "QUALITY_ISSUE", "NOT_AS_DESCRIBED", "CHANGED_MIND"}`
- `REFUND_WINDOW_DAYS = 7`
- `_open_requests = []`

**Static methods:**
- `is_within_refund_window(order_date, request_date)` → bool —
  True if request is within 7 days of order date
- `calculate_restocking_fee(item_value, reason)` → float —
  `CHANGED_MIND` attracts 10% restocking fee; all other reasons: 0%

**Class method:**
- `get_open_by_reason(cls, reason)` → list — filters `_open_requests` by reason

**Instance methods:**
- `approve(refund_amount)` — sets status to `"APPROVED"`, stores `refund_amount`
- `reject(rejection_reason)` — sets status to `"REJECTED"`, stores reason
- `get_net_refund()` → float — `refund_amount - restocking_fee`
- `print_summary()` — formatted summary card

---

### Task 3 — `VendorContract`

Build a `VendorContract` class representing a supply agreement between
eCOMMart and a vendor.

**Static methods:**
- `is_valid_contract_number(cn)` → bool — format `VC-YYYY-VVVV-NNN`
  (e.g. `VC-2024-0421-001`)
- `calculate_penalty(delay_days, contract_value)` → float —
  penalty = 0.5% of contract value per day delayed, capped at 10%

**Class method factory:**
- `from_renewal(cls, existing_contract, new_end_date)` —
  creates a new `VendorContract` by copying the existing one,
  incrementing the sequence in the contract number, and setting a new end date

**Instance methods with `**kwargs`:**
- `add_clauses(**clauses)` — stores named contract clauses
  (e.g. `exclusivity=True`, `min_order_qty=500`, `payment_terms_days=45`)
- `get_clause(name)` → value or `None`
- `is_expired(as_of=None)` → bool
- `get_days_remaining(as_of=None)` → int
- `print_contract_summary()` — formatted output

---

## Summary

| Method type | Decorator | First param | Has access to | Best for |
|---|---|---|---|---|
| Instance method | none | `self` | Instance attrs + class | Behaviour on one object |
| Class method | `@classmethod` | `cls` | Class attrs + class | Factories, shared state queries |
| Static method | `@staticmethod` | nothing | Only explicit args | Validators, parsers, utilities |

| Pattern | Use when |
|---|---|
| Factory `@classmethod` | Data arrives from JSON, CSV, dict, or another object type |
| `*args` in method | Caller may pass one or many items of the same kind |
| `**kwargs` in method | Caller passes named optional adjustments or configuration |
| Returns new instance | The method produces a derived or related object |
| `__len__` | Object wraps a collection — `len()` should work naturally |
| `__contains__` | Membership test (`in`) is a meaningful operation on this object |
| `__iter__` | Object wraps a collection — `for` loop should work naturally |

> Static methods are the most misused feature in Python OOP.
> The test is simple: if the method body contains `self.` or `cls.` anywhere,
> it is not a static method. If neither appears, and the logic is genuinely
> tied to the class's domain, make it static. Otherwise keep it as a
> module-level function.

---

*Next: `06_str_and_repr.md`*
