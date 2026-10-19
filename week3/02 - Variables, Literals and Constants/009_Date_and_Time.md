# Date and Time in Python
## eCOMMart AI Squad | Week 3

---

## 1. Why Dates Matter in eCOMMart

Every order has a placed date, a delivery deadline, and a return window. Python's `datetime` module lets you work with all of these — create dates, format them for display, calculate gaps, and compare them.

---

## 2. Importing the `datetime` Module

```python
from datetime import date, datetime, timedelta
```

You only import what you need. The three most useful classes:

| Class | What it holds |
|---|---|
| `date` | Year, month, day only |
| `datetime` | Year, month, day, hour, minute, second |
| `timedelta` | A duration — difference between two dates |

---

## 3. `date` — Working with Dates

### Creating a date

```python
from datetime import date

# Specific date
order_date = date(2024, 12, 1)    # year, month, day
print(order_date)
print(type(order_date))
```
```
# Output:
2024-12-01
<class 'datetime.date'>
```

```python
# Today's date — changes every time you run it
today = date.today()
print(today)
```
```
# Output:
(today's date — e.g. 2024-12-01)
```

### Accessing parts of a date

```python
from datetime import date

order_date = date(2024, 12, 1)

print(order_date.year)    # 2024
print(order_date.month)   # 12
print(order_date.day)     # 1
```
```
# Output:
2024
12
1
```

---

## 4. `datetime` — Date + Time Together

```python
from datetime import datetime

# Specific datetime
order_placed = datetime(2024, 12, 1, 14, 30, 0)   # year,month,day,hour,min,sec
print(order_placed)
```
```
# Output:
2024-12-01 14:30:00
```

```python
# Right now — changes every time you run it
now = datetime.now()
print(now)
```
```
# Output:
(current date and time — e.g. 2024-12-01 14:35:22.483910)
```

### Accessing parts

```python
from datetime import datetime

dt = datetime(2024, 12, 1, 14, 30, 0)

print(dt.year)     # 2024
print(dt.month)    # 12
print(dt.day)      # 1
print(dt.hour)     # 14
print(dt.minute)   # 30
print(dt.second)   # 0
```
```
# Output:
2024
12
1
14
30
0
```

---

## 5. Formatting Dates — `strftime()`

`strftime()` converts a date/datetime to a **string** in any format you choose.

| Code | Meaning | Example |
|---|---|---|
| `%d` | Day (01–31) | `01` |
| `%m` | Month (01–12) | `12` |
| `%Y` | Year (4 digits) | `2024` |
| `%B` | Full month name | `December` |
| `%b` | Abbreviated month | `Dec` |
| `%A` | Full weekday name | `Sunday` |
| `%H` | Hour (24h) | `14` |
| `%M` | Minute | `30` |

```python
from datetime import date

order_date = date(2024, 12, 1)

print(order_date.strftime("%d-%m-%Y"))
print(order_date.strftime("%B %d, %Y"))
print(order_date.strftime("%d %b %Y"))
print(f"Order placed on: {order_date.strftime('%d %B %Y')}")
print(f"Day of week: {order_date.strftime('%A')}")
```
```
# Output:
01-12-2024
December 01, 2024
01 Dec 2024
Order placed on: 01 December 2024
Day of week: Sunday
```

> **Weekday logic:** Use `strftime('%A')` or `date.weekday()` (0=Monday, 6=Sunday) to decide whether a delivery falls on a business day.

---

## 6. Parsing Dates — `strptime()`

`strptime()` converts a **string** into a `datetime` object. Use it when dates arrive from forms or APIs as text.

```python
from datetime import datetime

# Date arrives as a string from a form or API
raw_date = "15-10-2024"
parsed   = datetime.strptime(raw_date, "%d-%m-%Y")

print(parsed)
print(type(parsed))
print(parsed.day)
```
```
# Output:
2024-10-15 00:00:00
<class 'datetime.datetime'>
15
```

```
strptime("15-10-2024", "%d-%m-%Y")
             ↑   ↑  ↑         ↑↑↑↑↑↑↑
            day  m  year    must match format exactly
```

---

## 7. `timedelta` — Date Arithmetic

`timedelta` represents a **duration**. Use it to add or subtract days from a date.

```python
from datetime import date, timedelta

order_date    = date(2024, 12, 1)

# Add days — calculate delivery date
delivery_date = order_date + timedelta(days=3)
print(delivery_date)
```
```
# Output:
2024-12-04
```

```python
# Return window — 7 days from delivery
return_deadline = delivery_date + timedelta(days=7)
print(return_deadline)
```
```
# Output:
2024-12-11
```

### Days between two dates

```python
from datetime import date

order_date   = date(2024, 12, 1)
today        = date(2024, 12, 10)

days_elapsed = today - order_date
print(days_elapsed)         # shows as "9 days, 0:00:00"
print(days_elapsed.days)    # use .days to get the integer
```
```
# Output:
9 days, 0:00:00
9
```

```
today - order_date  →  timedelta object
.days               →  integer (the part you usually want)
```

---

## 8. Comparing Dates

Standard comparison operators work directly on `date` and `datetime` objects:

```python
from datetime import date

order_date      = date(2024, 12, 1)
return_deadline = date(2024, 12, 11)
today           = date(2024, 12, 10)

print(today < return_deadline)    # True  — still within return window
print(today > order_date)         # True  — order was placed in the past
print(today == order_date)        # False
```
```
# Output:
True
True
False
```

---

## 9. eCOMMart — Complete Date Example

```python
from datetime import date, timedelta

# Simulate an order
order_id      = "ORD-20241201"
product       = "Wireless Mouse"
order_date    = date(2024, 12, 1)
today         = date(2024, 12, 10)

# Delivery: 3 days after order
delivery_date = order_date + timedelta(days=3)

# Return window: 7 days from delivery
return_by     = delivery_date + timedelta(days=7)

# Days since order
days_since    = (today - order_date).days

# Is return still possible?
can_return    = today <= return_by

print("=" * 45)
print(f"  Order ID    : {order_id}")
print(f"  Product     : {product}")
print(f"  Ordered on  : {order_date.strftime('%d %B %Y')}")
print(f"  Delivered   : {delivery_date.strftime('%d %B %Y')}")
print(f"  Return by   : {return_by.strftime('%d %B %Y')}")
print(f"  Today       : {today.strftime('%d %B %Y')}")
print(f"  Days elapsed: {days_since} days")
print(f"  Can return? : {'Yes ✅' if can_return else 'No ❌ — window closed'}")
print("=" * 45)
```
```
# Output:
=============================================
  Order ID    : ORD-20241201
  Product     : Wireless Mouse
  Ordered on  : 01 December 2024
  Delivered   : 04 December 2024
  Return by   : 11 December 2024
  Today       : 10 December 2024
  Days elapsed: 9 days
  Can return? : Yes ✅
=============================================
```

---

## Quick Reference

| Task | Code |
|---|---|
| Today's date | `date.today()` |
| Current date + time | `datetime.now()` |
| Create a specific date | `date(2024, 12, 1)` |
| Add days | `order_date + timedelta(days=3)` |
| Days between dates | `(date2 - date1).days` |
| Format date as string | `d.strftime("%d %B %Y")` |
| Parse string to date | `datetime.strptime("01-12-2024", "%d-%m-%Y")` |
| Compare dates | `date1 < date2` |
| Day of week name | `d.strftime("%A")` |

---

## Tasks

### Task 1: eCOMMart — Order Timeline Calculator

Given a fixed order date, calculate and display the full order timeline.

```python
from datetime import date, timedelta

order_date    = date(2024, 11, 20)
delivery_date = order_date + timedelta(days=3)
return_by     = delivery_date + timedelta(days=7)
today         = date(2024, 11, 28)

days_since = (today - order_date).days
can_return = today <= return_by

print(f"Order     : {order_date.strftime('%d %B %Y')}")
print(f"Delivery  : {delivery_date.strftime('%d %B %Y')}")
print(f"Return by : {return_by.strftime('%d %B %Y')}")
print(f"Today     : {today.strftime('%d %B %Y')}")
print(f"Days since: {days_since}")
print(f"Can return: {'Yes ✅' if can_return else 'No ❌'}")
```
```
# Expected Output:
Order     : 20 November 2024
Delivery  : 23 November 2024
Return by : 30 November 2024
Today     : 28 November 2024
Days since: 8
Can return: Yes ✅
```

---

### Task 2: eCOMMart — Parse and Format a Date String

A date arrives from the eCOMMart API as the string `"01-12-2024"`. Parse it and display it in three different formats.

```python
from datetime import datetime

raw_date = "01-12-2024"
parsed   = datetime.strptime(raw_date, "%d-%m-%Y")

print(f"Parsed    : {parsed}")
print(f"Month name: {parsed.strftime('%B')}")
print(f"Formatted : {parsed.strftime('%d %B %Y')}")
```
```
# Expected Output:
Parsed    : 2024-12-01 00:00:00
Month name: December
Formatted : 01 December 2024
```

---

### Task 3: eCOMMart — Flash Sale Countdown

A flash sale ends at a specific datetime. Calculate how many days and hours remain.

```python
from datetime import datetime

sale_end    = datetime(2024, 12, 5, 23, 59, 59)
current     = datetime(2024, 12, 3, 10, 0, 0)

time_left   = sale_end - current

hours_left  = time_left.seconds // 3600

print(f"Sale ends   : {sale_end.strftime('%d %B %Y %H:%M')}")
print(f"Current time: {current.strftime('%d %B %Y %H:%M')}")
print(f"Time left   : {time_left.days} days, {hours_left} hours")
```
```
# Expected Output:
Sale ends   : 05 December 2024 23:59
Current time: 03 December 2024 10:00
Time left   : 2 days, 13 hours
```
