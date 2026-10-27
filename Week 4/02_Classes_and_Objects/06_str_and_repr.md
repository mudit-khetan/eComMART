# `__str__` and `__repr__`: Making Objects Readable
## eCOMMart AI Squad | Week 4

> A business object should be useful to the program and understandable to the
> person reading its output. Python gives classes two special methods for
> describing objects as text: `__str__` for a friendly display and `__repr__`
> for a precise, developer-oriented representation.

---

## What We Will Cover

1. Why Python needs textual representations of objects 
2. What `__str__` does when an object is displayed 
3. What `__repr__` is intended to communicate 
4. How `print()`, `str()`, and `repr()` choose a representation 
5. The difference between a customer-facing display and a debugging view 
6. Formatting dates, amounts, and status values safely 
7. Writing useful representations without changing object state 
8. How lists and dictionaries display objects they contain 
9. A complete `ShipmentBatch` example 
10. Common mistakes and testing strategies 
11. Tasks

---

## 1. Why Objects Need a Textual Representation

In earlier files, you created classes that stored business information and provided methods to calculate or update it. When you print an ordinary string, Python displays the text you expect. When you print a custom object, Python needs a rule for turning that object into text.

Consider a shipment batch in eCOMMart's B2B fulfilment process. It may contain a batch reference, destination, number of packages, carrier, dispatch date, and status. If you print the object without defining a representation, Python normally displays a technical description containing the class name and an identity-like memory address.

```python
class ShipmentBatch:
    """Represents a group of packages prepared for dispatch."""
    def __init__(self, batch_id, destination, package_count, carrier, status):
        """Stores the initial shipment batch details."""
        self.batch_id = batch_id
        self.destination = destination
        self.package_count = package_count
        self.carrier = carrier
        self.status = status
batch = ShipmentBatch("SHP-6208", "Jaipur", 18, "BlueDart", "READY")
print(batch)
```
```text
# Output:
<__main__.ShipmentBatch object at 0x...>
```

The exact address-like text differs between runs. It is not a useful business summary. Python is showing that `batch` refers to a `ShipmentBatch` object, but it is not telling the reader anything about the shipment itself.

We can improve this by defining special methods that tell Python how an object should be represented as text.

```
batch
  │
  ├── str(batch)
  │      └── friendly representation for people
  │
  └── repr(batch)
         └── detailed representation for debugging and inspection
```

The two methods have related purposes, but they are not interchangeable. Knowing which one to implement and what each should contain makes logs, debugging sessions, reports, and command-line output easier to understand.

---

## 2. What `__str__` Does

`__str__` returns a readable string intended for ordinary display. Think of it as the version you would show an operations coordinator who wants to know the current state of a shipment.

A typical implementation includes the most useful identifying information and leaves out details that would clutter the display.

```python
class ShipmentBatch:
    """Represents a group of packages prepared for dispatch."""
    def __init__(self, batch_id, destination, package_count, carrier, status):
        """Stores the initial shipment batch details."""
        self.batch_id = batch_id
        self.destination = destination
        self.package_count = package_count
        self.carrier = carrier
        self.status = status
    def __str__(self):
        """Returns a concise, human-readable shipment description."""
        return (
            f"{self.batch_id} to {self.destination} — "
            f"{self.package_count} packages, {self.status}"
        )
batch = ShipmentBatch("SHP-6208", "Jaipur", 18, "BlueDart", "READY")
print(batch)
print(str(batch))
```
```text
# Output:
SHP-6208 to Jaipur — 18 packages, READY
SHP-6208 to Jaipur — 18 packages, READY
```

Both `print(batch)` and `str(batch)` use the object's string representation. When Python sees `print(batch)`, it converts the object to a string before writing it to the output stream.

### The method's contract

`__str__` must return a string. It should not print the string itself.

```python
def __str__(self):
    """Returns a concise shipment label."""
    return f"{self.batch_id} — {self.status}"
```

The arrow diagram shows the distinction:

```
print(batch)
    │
    └── Python calls str(batch)
              │
              └── batch.__str__()
                        │
                        └── returns a string
                                  │
                                  └── print displays it
```

This is correct:

```python
def __str__(self):
    """Returns the batch identifier and current status."""
    return f"{self.batch_id} — {self.status}"
```

This is incorrect:

```python
def __str__(self):
    """Incorrectly prints instead of returning a string."""
    print(f"{self.batch_id} — {self.status}")
```

The incorrect version prints the text inside `__str__`, but it returns `None` implicitly. Python expects `__str__` to return a string, so calling `str()` on the object raises a `TypeError`.

```python
class BrokenBatch:
    """Illustrates an invalid string representation."""
    def __init__(self, batch_id, status, carrier, destination, package_count):
        """Stores a few fields for the demonstration."""
        self.batch_id = batch_id
        self.status = status
        self.carrier = carrier
        self.destination = destination
        self.package_count = package_count
    def __str__(self):
        """Incorrectly prints the representation instead of returning it."""
        print(f"{self.batch_id} — {self.status}")
broken = BrokenBatch("SHP-6209", "READY", "BlueDart", "Jaipur", 18)
try:
    print(str(broken))
except TypeError as error:
    print(f"TypeError: {error}")
```
```text
# Output:
SHP-6209 — READY
TypeError: __str__ returned non-string (type NoneType)
```

The lesson is simple: return the text. Let the caller decide whether to print it, store it, send it to a log, or place it in a user interface.

---

## 3. What `__repr__` Is For

`__repr__` returns a representation intended primarily for developers. It should communicate enough information to identify the object's important state when inspecting it during development or troubleshooting.

A useful representation might look like a constructor call:

```python
ShipmentBatch(
    batch_id='SHP-6208',
    destination='Jaipur',
    package_count=18,
    carrier='BlueDart',
    status='READY'
)
```

This is not a promise that the displayed text can always recreate the exact object. It is a convention: when practical, a good `repr` resembles valid Python code that communicates the object's important values.

```python
class ShipmentBatch:
    """Represents a group of packages prepared for dispatch."""
    def __init__(self, batch_id, destination, package_count, carrier, status):
        """Stores the initial shipment batch details."""
        self.batch_id = batch_id
        self.destination = destination
        self.package_count = package_count
        self.carrier = carrier
        self.status = status
    def __str__(self):
        """Returns a concise shipment description for routine display."""
        return (
            f"{self.batch_id} to {self.destination} — "
            f"{self.package_count} packages, {self.status}"
        )
    def __repr__(self):
        """Returns a detailed representation for debugging."""
        return (
            f"ShipmentBatch(batch_id={self.batch_id!r}, "
            f"destination={self.destination!r}, "
            f"package_count={self.package_count!r}, "
            f"carrier={self.carrier!r}, "
            f"status={self.status!r})"
        )
batch = ShipmentBatch("SHP-6208", "Jaipur", 18, "BlueDart", "READY")
print(str(batch))
print(repr(batch))
```
```text
# Output:
SHP-6208 to Jaipur — 18 packages, READY
ShipmentBatch(batch_id='SHP-6208', destination='Jaipur', package_count=18, carrier='BlueDart', status='READY')
```

The two representations are different because their audiences are different. The friendly version is short enough for routine operations output. The developer version names the fields and shows their values.

### Why use `!r` inside an f-string?

In an f-string, `!r` asks Python to use `repr()` for the value being inserted. It is particularly helpful for strings because it makes quotes, newline characters, and other special characters easier to spot.

```python
warehouse_note = "Leave at dock 3\nCall before arrival"
print(f"Normal: {warehouse_note}")
print(f"Debug : {warehouse_note!r}")
```
```text
# Output:
Normal: Leave at dock 3
Call before arrival
Debug : 'Leave at dock 3\nCall before arrival'
```

The normal display includes a line break. The representation makes the newline visible as `\n`. This can help when a string contains unexpected whitespace or a hidden character.

---

## 4. `print()`, `str()`, `repr()`, and Interactive Inspection

Python provides several ways to request a textual representation.

| Expression | Purpose |
|---|---|
| `str(value)` | Requests a readable string |
| `repr(value)` | Requests a developer-oriented representation |
| `print(value)` | Converts the value to display text and writes it |
| `f"{value}"` | Uses string formatting, normally the string representation |
| `f"{value!r}"` | Uses the representation form inside an f-string |

When you type an expression into a Python interactive shell and press Enter, the shell usually displays the result using `repr()`. This is why a string entered by itself often appears with quotes, even though `print()` does not show those quotes.

```python
label = "SHP-6210 is ready"
print(label)
print(repr(label))
print(f"{label}")
print(f"{label!r}")
```
```text
# Output:
SHP-6210 is ready
'SHP-6210 is ready'
SHP-6210 is ready
'SHP-6210 is ready'
```

The quotes are part of the representation, not part of the original string.

### A quick comparison

```python
class DispatchNotice:
    """Stores the key details of a dispatch notice."""
    def __init__(self, notice_id, recipient, channel, status, priority):
        """Stores dispatch notice details."""
        self.notice_id = notice_id
        self.recipient = recipient
        self.channel = channel
        self.status = status
        self.priority = priority
    def __str__(self):
        """Returns a short display label."""
        return f"Notice {self.notice_id} for {self.recipient}: {self.status}"
    def __repr__(self):
        """Returns a detailed developer representation."""
        return (
            f"DispatchNotice(notice_id={self.notice_id!r}, "
            f"recipient={self.recipient!r}, channel={self.channel!r}, "
            f"status={self.status!r}, priority={self.priority!r})"
        )
notice = DispatchNotice("NTF-880", "Northstar Retail", "EMAIL", "QUEUED", "HIGH")
print(notice)
print(repr(notice))
```
```text
# Output:
Notice NTF-880 for Northstar Retail: QUEUED
DispatchNotice(notice_id='NTF-880', recipient='Northstar Retail', channel='EMAIL', status='QUEUED', priority='HIGH')
```

A display label helps an operations team scan notices quickly. A detailed representation helps a developer confirm that the intended recipient, channel, status, and priority were stored correctly.

---

## 5. Deciding What Belongs in Each Representation

The goal is not to put every attribute into both methods. Decide what the reader needs in each situation.

For `__str__`, ask:

- What identifies this object at a glance?
- Which two or three values matter most to the intended reader?
- Can the output fit naturally in a list, terminal line, or status message?
- Does the wording remain understandable when several objects are shown?

For `__repr__`, ask:

- Which values are important when diagnosing a bug?
- Are strings represented with `!r` so whitespace is visible?
- Are the fields named so their values are not ambiguous?
- Does the representation avoid leaking credentials or confidential data?

```
┌─────────────────────────────────────────────────────────┐
│ __str__ — routine display                               │
├─────────────────────────────────────────────────────────┤
│ SHP-6208 to Jaipur — 18 packages, READY                 │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ __repr__ — developer inspection                         │
├─────────────────────────────────────────────────────────┤
│ ShipmentBatch(batch_id='SHP-6208', destination='Jaipur',│
│ package_count=18, carrier='BlueDart', status='READY')   │
└─────────────────────────────────────────────────────────┘
```

The exact contents depend on the domain. A short status object may only need an identifier and status in its `str`. A complex configuration object may need more detail in its `repr`. The key is to choose intentionally.

### Do not include secrets

A developer-oriented representation is not a reason to expose passwords, access tokens, private customer data, or payment credentials. Debug output is often copied into tickets, logs, and shared messages. If a class contains a secret, omit it or mask it in both representations.

For example, a payment-related object might show a masked account reference rather than a complete sensitive identifier:

```python
class SettlementProfile:
    """Stores a settlement profile without displaying its secret token."""
    def __init__(self, profile_id, bank_label, account_suffix, secret_token, active):
        """Stores settlement profile details."""
        self.profile_id = profile_id
        self.bank_label = bank_label
        self.account_suffix = account_suffix
        self.secret_token = secret_token
        self.active = active
    def __str__(self):
        """Returns a safe display label."""
        return (
            f"{self.profile_id} — {self.bank_label} "
            f"account ending {self.account_suffix}"
        )
    def __repr__(self):
        """Returns useful debug details while masking the secret token."""
        return (
            f"SettlementProfile(profile_id={self.profile_id!r}, "
            f"bank_label={self.bank_label!r}, "
            f"account_suffix={self.account_suffix!r}, "
            f"secret_token='[REDACTED]', active={self.active!r})"
        )
profile = SettlementProfile(
    "SET-071", "Axis Bank", "4821", "live-secret-value", True
)
print(profile)
print(repr(profile))
```
```text
# Output:
SET-071 — Axis Bank account ending 4821
SettlementProfile(profile_id='SET-071', bank_label='Axis Bank', account_suffix='4821', secret_token='[REDACTED]', active=True)
```

The secret token remains available to the program where needed, but it is not included in the textual representation. Treat representations as potentially shareable output, not as a secure storage area.

---

## 6. Formatting Values Clearly

A good representation uses formatting that matches the meaning of each value. For eCOMMart business objects, this often means:

- Currency values formatted with a rupee symbol and two decimal places
- Dates displayed in a consistent format
- Status values shown in a consistent case
- Long identifiers preserved without accidental truncation
- Optional values represented clearly instead of appearing as unexplained blanks

### Currency formatting

```python
class FreightEstimate:
    """Represents an estimated freight charge for a dispatch."""
    def __init__(self, estimate_id, route, weight_kg, base_charge, fuel_surcharge):
        """Stores freight estimate details."""
        self.estimate_id = estimate_id
        self.route = route
        self.weight_kg = weight_kg
        self.base_charge = base_charge
        self.fuel_surcharge = fuel_surcharge
    def total_charge(self):
        """Returns the base charge plus fuel surcharge."""
        return self.base_charge + self.fuel_surcharge
    def __str__(self):
        """Returns a readable summary with the total charge."""
        return (
            f"{self.estimate_id} | {self.route} | "
            f"{self.weight_kg:.1f} kg | ₹{self.total_charge():,.2f}"
        )
    def __repr__(self):
        """Returns the detailed values used to calculate the estimate."""
        return (
            f"FreightEstimate(estimate_id={self.estimate_id!r}, "
            f"route={self.route!r}, weight_kg={self.weight_kg!r}, "
            f"base_charge={self.base_charge!r}, "
            f"fuel_surcharge={self.fuel_surcharge!r})"
        )
freight = FreightEstimate("FRT-510", "Delhi → Jaipur", 42.5, 1850.00, 222.50)
print(freight)
print(repr(freight))
```
```text
# Output:
FRT-510 | Delhi → Jaipur | 42.5 kg | ₹2,072.50
FreightEstimate(estimate_id='FRT-510', route='Delhi → Jaipur', weight_kg=42.5, base_charge=1850.0, fuel_surcharge=222.5)
```

The comma in `:,.2f` adds thousands separators and keeps two decimal places. That makes monetary values easier to scan. The `repr` uses the stored values so a developer can inspect the inputs to the calculation.

### Date formatting

A class may store dates as ISO strings or as `date` objects. Whatever choice you make, use a consistent display format.

```python
from datetime import date
class PickupWindow:
    """Represents an arranged collection window."""
    def __init__(self, window_id, pickup_date, start_time, end_time, zone):
        """Stores pickup window details."""
        self.window_id = window_id
        self.pickup_date = pickup_date
        self.start_time = start_time
        self.end_time = end_time
        self.zone = zone
    def __str__(self):
        """Returns a compact label for the pickup window."""
        formatted_date = self.pickup_date.strftime("%d %b %Y")
        return (
            f"{self.window_id} | {formatted_date} | "
            f"{self.start_time}-{self.end_time} | {self.zone}"
        )
    def __repr__(self):
        """Returns the stored pickup window fields."""
        return (
            f"PickupWindow(window_id={self.window_id!r}, "
            f"pickup_date={self.pickup_date!r}, "
            f"start_time={self.start_time!r}, "
            f"end_time={self.end_time!r}, zone={self.zone!r})"
        )
window = PickupWindow(
    "PUP-118", date(2026, 10, 24), "10:00", "12:00", "Jaipur-East"
)
print(window)
print(repr(window))
```
```text
# Output:
PUP-118 | 24 Oct 2026 | 10:00-12:00 | Jaipur-East
PickupWindow(window_id='PUP-118', pickup_date=datetime.date(2026, 10, 24), start_time='10:00', end_time='12:00', zone='Jaipur-East')
```

The friendly string uses a human-readable date. The representation preserves the fact that `pickup_date` is a `date` object, not just a string.

---

## 7. Representations Should Not Change State

`__str__` and `__repr__` should describe the current object. They should not quietly update the status, make a network request, write a file, or change financial values.

A representation may call a read-only helper to calculate a display value. It should avoid helpers that change state or perform unrelated actions.

```python
class DispatchCapacity:
    """Tracks capacity for one dispatch run."""
    def __init__(self, run_id, planned_packages, packed_packages, hub, status):
        """Stores dispatch capacity details."""
        self.run_id = run_id
        self.planned_packages = planned_packages
        self.packed_packages = packed_packages
        self.hub = hub
        self.status = status
    def remaining_packages(self):
        """Returns the number of packages not yet packed."""
        return max(0, self.planned_packages - self.packed_packages)
    def is_complete(self):
        """Returns True when all planned packages have been packed."""
        return self.packed_packages >= self.planned_packages
    def __str__(self):
        """Returns a summary without modifying capacity values."""
        return (
            f"{self.run_id} at {self.hub}: "
            f"{self.packed_packages}/{self.planned_packages} packed"
        )
    def __repr__(self):
        """Returns the stored capacity values for debugging."""
        return (
            f"DispatchCapacity(run_id={self.run_id!r}, "
            f"planned_packages={self.planned_packages!r}, "
            f"packed_packages={self.packed_packages!r}, "
            f"hub={self.hub!r}, status={self.status!r})"
        )
capacity = DispatchCapacity("RUN-82", 120, 93, "Jaipur Hub", "PACKING")
before = (capacity.planned_packages, capacity.packed_packages, capacity.status)
print(capacity)
print(repr(capacity))
after = (capacity.planned_packages, capacity.packed_packages, capacity.status)
print(before == after)
```
```text
# Output:
RUN-82 at Jaipur Hub: 93/120 packed
DispatchCapacity(run_id='RUN-82', planned_packages=120, packed_packages=93, hub='Jaipur Hub', status='PACKING')
True
```

The final `True` confirms that displaying the object did not change its stored state. A representation method should be safe to call repeatedly.

### Avoid hidden work in representations

Do not make `__str__` send an email, refresh inventory from an external service, or query a slow database. A developer may inspect an object while debugging, and tools may call `repr()` automatically. If representation triggers significant work, merely inspecting the object could become slow or risky.

```
Good representation
    ├── reads existing attributes
    ├── formats values
    └── returns a string
Risky representation
    ├── calls an external API
    ├── changes object status
    ├── sends notifications
    └── returns a string after hidden work
```

Keep operational actions in explicitly named methods such as `dispatch_packages()` or `send_notice()`. Let representations remain descriptive.

---

## 8. Objects Inside Lists and Dictionaries

One important behaviour is easy to miss: containers generally use `repr()` for the objects they contain. If a list contains custom objects, printing the list does not simply call each object's `__str__` and join the results. It uses their representations.

```python
class RouteCheckpoint:
    """Represents a checkpoint on a delivery route."""
    def __init__(self, checkpoint_id, city, sequence, completed, note):
        """Stores checkpoint details."""
        self.checkpoint_id = checkpoint_id
        self.city = city
        self.sequence = sequence
        self.completed = completed
        self.note = note
    def __str__(self):
        """Returns a compact checkpoint label."""
        state = "done" if self.completed else "pending"
        return f"{self.sequence}. {self.city} ({state})"
    def __repr__(self):
        """Returns all fields needed for debugging."""
        return (
            f"RouteCheckpoint(checkpoint_id={self.checkpoint_id!r}, "
            f"city={self.city!r}, sequence={self.sequence!r}, "
            f"completed={self.completed!r}, note={self.note!r})"
        )
checkpoint_a = RouteCheckpoint("CHK-01", "Delhi", 1, True, "Loaded")
checkpoint_b = RouteCheckpoint("CHK-02", "Gurugram", 2, False, "Awaiting scan")
print(checkpoint_a)
print([checkpoint_a, checkpoint_b])
```
```text
# Output:
1. Delhi (done)
[RouteCheckpoint(checkpoint_id='CHK-01', city='Delhi', sequence=1, completed=True, note='Loaded'), RouteCheckpoint(checkpoint_id='CHK-02', city='Gurugram', sequence=2, completed=False, note='Awaiting scan')]
```

The first line calls `__str__` for one checkpoint. The list uses each checkpoint's `__repr__`, which makes the container's output more informative for developers.

### Why container output matters

You will often inspect lists of records in a debugger, print a list while testing, or view a dictionary returned by an API integration. A useful `__repr__` makes all of these activities easier.

```python
checkpoints = {
    "origin": checkpoint_a,
    "next": checkpoint_b,
}
print(checkpoints)
```
```text
# Output:
{'origin': RouteCheckpoint(checkpoint_id='CHK-01', city='Delhi', sequence=1, completed=True, note='Loaded'), 'next': RouteCheckpoint(checkpoint_id='CHK-02', city='Gurugram', sequence=2, completed=False, note='Awaiting scan')}
```

The dictionary's keys are strings, and its values are custom objects. Python uses the representation of each value when displaying the dictionary.

### Want a friendly list?

If a screen needs a list of short human-readable labels, build those labels explicitly rather than relying on the container's default representation.

```python
labels = [str(checkpoint) for checkpoint in [checkpoint_a, checkpoint_b]]
print(labels)
print(" | ".join(labels))
```
```text
# Output:
['1. Delhi (done)', '2. Gurugram (pending)']
1. Delhi (done) | 2. Gurugram (pending)
```

The list itself still displays its strings with quotes. The joined string displays the labels without list punctuation. Choose the format that suits the reader.

---

## 9. The Main Worked Example — `ShipmentBatch`

Now combine the ideas into one realistic eCOMMart logistics class. This `ShipmentBatch` tracks a group of packages prepared for dispatch. It has business attributes, validation, status changes, calculation methods, and both textual representations.

### Requirements

- The batch identifier must be non-empty.
- Destination and carrier must be non-empty strings.
- Package count must be a positive integer.
- Weight must be a positive number.
- Status must be one of `PLANNED`, `PACKING`, `READY`, `DISPATCHED`, or
`HELD`.
- `__str__` should provide a concise operational summary.
- `__repr__` should expose the stored fields in a useful developer format.
- Calling either representation must not change the batch.

### Class outline

```
ShipmentBatch
  │
  ├── __init__(...)             → validates and stores fields
  ├── total_weight_kg()         → calculates package weight
  ├── can_dispatch()            → checks dispatch readiness
  ├── mark_ready()              → changes status after validation
  ├── mark_dispatched()         → changes status
  ├── build_summary()           → returns a dictionary
  ├── __str__()                 → concise operational display
  └── __repr__()                → detailed developer display
```

### Complete class

```python
class ShipmentBatch:
    """
    Represents a group of B2B packages prepared for dispatch.
    Attributes:
        batch_id (str): Unique shipment batch reference.
        destination (str): Destination city or fulfilment zone.
        package_count (int): Number of packages in the batch.
        carrier (str): Delivery carrier assigned to the batch.
        total_weight (float): Combined shipment weight in kilograms.
        status (str): Current fulfilment status.
        dispatch_date (str | None): Planned or actual dispatch date.
        priority (str): Operational priority level.
    """
    VALID_STATUSES = {"PLANNED", "PACKING", "READY", "DISPATCHED", "HELD"}
    VALID_PRIORITIES = {"LOW", "NORMAL", "HIGH", "URGENT"}
    def __init__(
        self,
        batch_id,
        destination,
        package_count,
        carrier,
        total_weight,
        status="PLANNED",
        dispatch_date=None,
        priority="NORMAL",
    ):
        """Validates and stores the shipment batch details."""
        if not isinstance(batch_id, str) or not batch_id.strip():
            raise ValueError("batch_id must be a non-empty string.")
        if not isinstance(destination, str) or not destination.strip():
            raise ValueError("destination must be a non-empty string.")
        if not isinstance(carrier, str) or not carrier.strip():
            raise ValueError("carrier must be a non-empty string.")
        if not isinstance(package_count, int) or package_count <= 0:
            raise ValueError("package_count must be a positive integer.")
        if not isinstance(total_weight, (int, float)) or total_weight <= 0:
            raise ValueError("total_weight must be a positive number.")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status!r}")
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority!r}")
        if dispatch_date is not None and (
            not isinstance(dispatch_date, str) or not dispatch_date.strip()
        ):
            raise ValueError("dispatch_date must be None or a non-empty string.")
        self.batch_id = batch_id.strip().upper()
        self.destination = destination.strip()
        self.package_count = package_count
        self.carrier = carrier.strip()
        self.total_weight = float(total_weight)
        self.status = status
        self.dispatch_date = dispatch_date
        self.priority = priority
    def total_weight_kg(self):
        """Returns the combined weight in kilograms."""
        return self.total_weight
    def can_dispatch(self):
        """Returns True when the batch is ready and has valid shipment details."""
        return (
            self.status == "READY"
            and self.package_count > 0
            and self.total_weight > 0
            and bool(self.destination)
            and bool(self.carrier)
        )
    def mark_ready(self):
        """Moves a packing batch to READY when its details are valid."""
        if self.status not in {"PLANNED", "PACKING"}:
            raise RuntimeError(
                f"Cannot mark batch {self.batch_id} ready from {self.status}."
            )
        if self.package_count <= 0 or self.total_weight <= 0:
            raise ValueError("A batch needs packages and a positive total weight.")
        self.status = "READY"
    def mark_dispatched(self, dispatch_date):
        """Marks a ready batch as dispatched and records the dispatch date."""
        if not self.can_dispatch():
            raise RuntimeError("Only a ready batch can be dispatched.")
        if not isinstance(dispatch_date, str) or not dispatch_date.strip():
            raise ValueError("dispatch_date must be a non-empty string.")
        self.dispatch_date = dispatch_date
        self.status = "DISPATCHED"
    def build_summary(self):
        """Returns a new dictionary describing the current batch."""
        return {
            "batch_id": self.batch_id,
            "destination": self.destination,
            "package_count": self.package_count,
            "carrier": self.carrier,
            "total_weight_kg": self.total_weight_kg(),
            "status": self.status,
            "dispatch_date": self.dispatch_date,
            "priority": self.priority,
        }
    def __str__(self):
        """Returns a short operational summary for routine display."""
        return (
            f"{self.batch_id} → {self.destination} | "
            f"{self.package_count} packages | {self.status}"
        )
    def __repr__(self):
        """Returns the batch's important stored fields for debugging."""
        return (
            f"ShipmentBatch(batch_id={self.batch_id!r}, "
            f"destination={self.destination!r}, "
            f"package_count={self.package_count!r}, "
            f"carrier={self.carrier!r}, "
            f"total_weight={self.total_weight!r}, "
            f"status={self.status!r}, "
            f"dispatch_date={self.dispatch_date!r}, "
            f"priority={self.priority!r})"
        )
```

### Create a batch and inspect both representations

```python
batch = ShipmentBatch(
    batch_id="shp-6208",
    destination="Jaipur",
    package_count=18,
    carrier="BlueDart",
    total_weight=146.75,
    status="PACKING",
    dispatch_date="2026-10-23",
    priority="HIGH",
)
print(batch)
print(repr(batch))
```
```text
# Output:
SHP-6208 → Jaipur | 18 packages | PACKING
ShipmentBatch(batch_id='SHP-6208', destination='Jaipur', package_count=18, carrier='BlueDart', total_weight=146.75, status='PACKING', dispatch_date='2026-10-23', priority='HIGH')
```

The constructor normalises the batch identifier to uppercase. Both representations show the normalised value that is actually stored, rather than the original lowercase input.

### Move the batch through its workflow

```python
print(f"Can dispatch now? {batch.can_dispatch()}")
batch.mark_ready()
print(batch)
print(f"Can dispatch now? {batch.can_dispatch()}")
batch.mark_dispatched("2026-10-23")
print(batch)
print(repr(batch))
```
```text
# Output:
Can dispatch now? False
SHP-6208 → Jaipur | 18 packages | READY
Can dispatch now? True
SHP-6208 → Jaipur | 18 packages | DISPATCHED
ShipmentBatch(batch_id='SHP-6208', destination='Jaipur', package_count=18, carrier='BlueDart', total_weight=146.75, status='DISPATCHED', dispatch_date='2026-10-23', priority='HIGH')
```

The status-changing methods are explicit commands. The representation methods simply show the state after those commands have run.

### Use the summary for structured output

```python
summary = batch.build_summary()
print(summary)
print(f"Weight: {summary['total_weight_kg']:.2f} kg")
```
```text
# Output:
{'batch_id': 'SHP-6208', 'destination': 'Jaipur', 'package_count': 18, 'carrier': 'BlueDart', 'total_weight_kg': 146.75, 'status': 'DISPATCHED', 'dispatch_date': '2026-10-23', 'priority': 'HIGH'}
Weight: 146.75 kg
```

`build_summary()` is not a replacement for `__str__` or `__repr__`. It serves a different purpose: structured data that another part of the application can read by key. `__str__` and `__repr__` are textual views.

---

## 10. Common Mistakes and Testing Strategies

### Mistake 1 — Returning a non-string value

Both `__str__` and `__repr__` must return strings. Returning a dictionary, integer, or `None` raises a `TypeError` when Python requests the representation.

```python
class IncorrectLabel:
    """Demonstrates an invalid string representation."""
    def __init__(self, label, status, owner, priority, reference):
        """Stores label details."""
        self.label = label
        self.status = status
        self.owner = owner
        self.priority = priority
        self.reference = reference
    def __str__(self):
        """Incorrectly returns a dictionary."""
        return {
            "label": self.label,
            "status": self.status,
            "owner": self.owner,
            "priority": self.priority,
            "reference": self.reference,
        }
bad_label = IncorrectLabel("Dock 4", "OPEN", "Operations", "NORMAL", "LBL-09")
try:
    print(bad_label)
except TypeError as error:
    print(f"TypeError: {error}")
```
```text
# Output:
TypeError: __str__ returned non-string (type dict)
```

Convert the relevant values into a string and return that string.

### Mistake 2 — Forgetting to return

A method that only calls `print()` returns `None` implicitly. Use `return` inside `__str__` and `__repr__`; print the object outside the method.

### Mistake 3 — Writing a `repr` that is too vague

This representation is technically a string but not very informative:

```python
def __repr__(self):
    """Returns an unhelpfully vague representation."""
    return "<ShipmentBatch>"
```

It does not identify which batch is being inspected or what state it is in. A better representation includes important field names and values.

### Mistake 4 — Using `str()` inside `__repr__` without considering clarity

For strings, `!r` is often useful because it reveals whitespace and quoting. For numbers and Boolean values, their representations are already clear. Use formatting intentionally instead of converting every value the same way.

### Mistake 5 — Putting every attribute into `__str__`

A long representation may be hard to read in a dashboard or console. Put the most useful fields in `__str__` and the debugging detail in `__repr__`.

### Mistake 6 — Making representation methods perform actions

Do not dispatch a batch, send a notice, or write a file just because an object is being printed. Keep representations descriptive and state changes explicit.

### Mistake 7 — Exposing confidential values

Representations can appear in error messages and logs. Mask secrets and avoid including private data that is not necessary for debugging.

### Mistake 8 — Assuming a list uses `__str__` for each object

A list uses each element's `repr()` in its own representation. If you need friendly labels, call `str()` for each object explicitly and join the results.

### A small representation test checklist

For every class with custom representations, test these cases:

1. A typical valid object. 2. An object with an optional value set to `None`. 3. Strings that contain spaces or special characters. 4. The object before and after a valid state change. 5. A list containing several instances. 6. A dictionary containing instances as values. 7. Confirmation that printing does not mutate state. 8. Confirmation that secret values are not included.

A representation does not need to be tested with a large framework to be useful. A few focused assertions can catch mistakes early.

```python
batch = ShipmentBatch(
    "SHP-6211", "Indore", 7, "Delhivery", 38.25,
    status="READY", dispatch_date=None, priority="NORMAL"
)
assert isinstance(str(batch), str)
assert isinstance(repr(batch), str)
assert "SHP-6211" in str(batch)
assert "carrier='Delhivery'" in repr(batch)
assert batch.status == "READY"
print("Representation checks passed.")
```
```text
# Output:
Representation checks passed.
```

The assertions check the contract and a few important details. If any assertion fails, Python raises an `AssertionError`, making the issue visible.

---

## 11. Tasks

Use different eCOMMart domain entities for these tasks. Each class must have at least five attributes and at least four methods. Every method must include a docstring. Add test calls and `# Output:` comments showing the expected results.

### Task 1 — `ReviewSummary`: Friendly and Developer Representations

Build a `ReviewSummary` class for the summary of customer feedback on a B2B catalog listing.

Required attributes:

- `summary_id`
- `listing_reference`
- `review_count`
- `average_rating`
- `positive_count`
- `negative_count`

Add at least two more attributes, such as `last_updated` and `moderation_status`.

Implement at least four methods:

1. `positive_percentage()` — returns the percentage of positive reviews. 2. `needs_moderation()` — returns `True` if the summary has a rule-based reason to be reviewed, such as a very low average rating or an invalid count. 3. `build_summary()` — returns a dictionary of the summary values. 4. `__str__()` — returns a concise display such as `REV-SUM-18 | Listing CAT-448 | 4.2/5 from 50 reviews`. 5. `__repr__()` — returns a developer representation with the important stored fields.

Validate that counts are non-negative integers, the positive and negative counts do not exceed the total review count, and the average rating is between 0 and 5. Handle the zero-review case without division by zero. Test both representations and the percentage calculation.

### Task 2 — `FlashSale`: Representation and State Changes

Build a `FlashSale` class representing a time-limited eCOMMart promotion for business buyers.

Required attributes:

- `sale_id`
- `campaign_name`
- `discount_percent`
- `starts_at`
- `ends_at`
- `status`

Add at least two more attributes, such as `eligible_categories`, `minimum_order_value`, or `created_by`.

Implement at least four methods:

1. `is_active_at(timestamp)` — returns whether the supplied timestamp falls within the sale period and the sale status allows it. 2. `activate()` — changes the status to active only if the sale configuration is valid. 3. `build_summary()` — returns a dictionary of sale details. 4. `__str__()` — returns a short campaign label and discount. 5. `__repr__()` — shows enough field values to debug a configuration issue.

Validate that the discount is greater than 0 and no more than 80, that the end time is after the start time, and that the status is valid. Use a different entity from `ReviewSummary`. Test a sale before it starts, during its active window, and after it ends. Ensure the representation methods do not change status.

### Task 3 — `Notification`: Safe Representation and Delivery Status

Build a `Notification` class for a message that eCOMMart may send to a vendor contact about an order or shipment update.

Required attributes:

- `notification_id`
- `recipient_id`
- `channel`
- `subject`
- `message`
- `status`

Add at least two more attributes, such as `created_at`, `sent_at`, or `failure_reason`.

Implement at least four methods:

1. `mark_sent(sent_at)` — updates status and records the send time, unless the notification has already been cancelled. 2. `mark_failed(reason)` — records a failure state and explanation. 3. `build_summary()` — returns structured details without changing the object. 4. `__str__()` — returns a short display that does not expose the full message. 5. `__repr__()` — provides debugging detail while avoiding private message content if it may contain confidential data.

Validate the channel against a small set such as `{"EMAIL", "SMS", "IN_APP"}`. Write tests for a successful delivery transition, a rejected transition, and the safe contents of both representations. Add a comment explaining why message content is not shown in full in the representation.

---

## Summary

| Concept | Key rule |
|---|---|
| `__str__` | Returns a friendly string for routine display |
| `__repr__` | Returns a developer-oriented representation |
| Return value | Both methods must return a string, not print or return `None` |
| `print(obj)` | Uses the string representation |
| `str(obj)` | Requests the readable representation |
| `repr(obj)` | Requests the developer representation |
| `!r` in f-strings | Formats a value using `repr()` |
| Container output | Lists and dictionaries use representations of contained objects |
| Safe debugging | Do not reveal secrets or unnecessary private data |
| Side effects | Representation methods should describe state, not change it |
| `build_summary()` | Returns structured data; it is separate from textual representations |
| Testing | Check types, important fields, containers, state stability, and edge cases |

*Next: `07_Encapsulation_and_Properties.md`*
