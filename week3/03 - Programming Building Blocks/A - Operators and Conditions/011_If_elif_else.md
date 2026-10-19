# if, elif, else Statements

`if` statements let your program make decisions and take different actions based on conditions.

Think of it as telling Python:

> "If this is true, do this. Or else if that is true, do that. Otherwise, do something else."

**Syntax:**

```python
if condition1:
    # runs when condition1 is True
elif condition2:
    # runs when condition1 is False and condition2 is True
else:
    # runs when none of the above conditions are True
```

**What we will cover:**

1. Basic `if` and `else`
2. Multiple branches with `elif`
3. B2B eCom examples
4. Indentation rules
5. Handling missing input — `is_nan()`
6. Safe input conversion — `safe_eval_price()`
7. Complete mini agent tool
8. Tasks

---

## 1. Basic `if` and `else`

The simplest form — one condition, two paths:

```python
if True:
    print('It was true!')
```
```
# Output:
It was true!
```

```python
is_in_stock = False

if is_in_stock:
    print('Item is available. Add to cart!')
else:
    print('Sorry, this item is currently out of stock.')
```
```
# Output:
Sorry, this item is currently out of stock.
```

```
if condition:         ← evaluated first
    # this runs       ← only if condition is True
else:
    # this runs       ← only if condition is False
```

---

## 2. Multiple Branches with `elif`

Use `elif` when you have more than two possible outcomes. Python checks each condition from **top to bottom** and stops at the **first True match**:

```python
city = 'Bangalore'

if city == 'Mumbai':
    print('Same-day delivery available!')
elif city == 'Bangalore':
    print('Next-day delivery available.')
elif city == 'Delhi':
    print('2-day delivery available.')
else:
    print('Standard 5-7 day delivery for your location.')
```
```
# Output:
Next-day delivery available.
```

```
city = 'Bangalore'
    ↓
if city == 'Mumbai'?    → No  → skip
elif city == 'Bangalore'? → Yes → print and STOP
(remaining elif/else never checked)
```

---

## 3. B2B eCom Examples

### Example A — Customer Login Check

```python
registered_user = 'priya@ecommart.in'
login_attempt   = 'priya@ecommart.in'

if login_attempt == registered_user:
    print('Welcome back, Priya!')
else:
    print('Email not found. Please register on eCOMMart.')
```
```
# Output:
Welcome back, Priya!
```

### Example B — Membership Tier

```python
total_spent = 8500   # customer's total spending this year (₹)

if total_spent >= 10000:
    print('Congratulations! You are a PLATINUM member.')
elif total_spent >= 5000:
    print('You are a GOLD member.')
elif total_spent >= 2000:
    print('You are a SILVER member.')
else:
    print('You are a standard member. Shop more to unlock rewards!')
```
```
# Output:
You are a GOLD member.
```

```
total_spent = 8500
    ↓
>= 10000? No
>= 5000?  Yes → GOLD ← stops here
```

**Try different values to see how tiers change:**

```
₹12000 → PLATINUM
₹8500  → GOLD
₹3000  → SILVER
₹500   → Standard
```

### Example C — Cart Discount

```python
cart_value = 2500

if cart_value >= 2000:
    discount = 0.20   # 20% off
elif cart_value >= 1000:
    discount = 0.10   # 10% off
elif cart_value >= 500:
    discount = 0.05   # 5% off
else:
    discount = 0.0    # no discount

final_price = cart_value - (cart_value * discount)
print(f"Discount Applied : {int(discount * 100)}%")
print(f"You Pay          : ₹{final_price:.2f}")
```
```
# Output:
Discount Applied : 20%
You Pay          : ₹2000.00
```

**More examples:**

```
₹2500 → 20% off → ₹2000.00
₹1200 → 10% off → ₹1080.00
₹600  →  5% off → ₹570.00
₹300  →  0% off → ₹300.00
```

---

## 4. Indentation

Python uses **indentation** (4 spaces or 1 tab) to define which lines belong inside an `if` block. This is not optional — incorrect indentation causes errors.

```python
cart_value = 600

if cart_value > 500:
    print("Eligible for discount")   # inside the if block
    print("Applying discount...")    # also inside — same indent level

print("Thank you for shopping!")    # outside the if block — always runs
```
```
# Output:
Eligible for discount
Applying discount...
Thank you for shopping!
```

```
if cart_value > 500:
    ← 4 spaces → print("Eligible...")   ← runs only when condition is True
    ← 4 spaces → print("Applying...")   ← same block, same indent

print("Thank you...")   ← no indent = outside the block, always runs
```

---

## 5. Handling Missing Input — `is_nan()`

> ### Agent Tool Foundation
> When an AI agent receives data from a user form, chat, or API feed, values may arrive as `None`, an empty string `""`, or `float('nan')`. Passing these directly into `if price > 500` would crash your program. The `is_nan()` function checks for this first — it is the safety check every agent tool should run before any numeric comparison.

```python
import math

def is_nan(value):
    """
    Checks if a value is missing, empty, or not a usable number.

    Call this before any numeric comparison to prevent crashes
    when user input or API data has missing fields.

    Args:
        value: Any value (string, float, int, None)

    Returns:
        bool: True if the value is missing/invalid, False if usable.
    """
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False
```

```python
# Test with four types of price input
price1 = 499.0          # valid price
price2 = None           # missing from data feed
price3 = float('nan')   # came in as NaN from a pipeline
price4 = ""             # empty string from a web form

for price in [price1, price2, price3, price4]:
    if is_nan(price):
        print(f"  Price is missing or invalid: {price!r} — skipping item.")
    elif price >= 500:
        print(f"  ₹{price} — Free delivery eligible!")
    else:
        print(f"  ₹{price} — Add ₹{500 - price:.2f} more for free delivery.")
```
```
# Output:
  ₹499.0 — Add ₹1.00 more for free delivery.
  Price is missing or invalid: None — skipping item.
  Price is missing or invalid: nan — skipping item.
  Price is missing or invalid: '' — skipping item.
```

```
is_nan() returns True when:
  value is None         → missing entirely
  value is float('nan') → invalid number from pipeline
  value is ""           → empty form field

is_nan() returns False when:
  value is 499.0        → usable number, safe to compare
```

---

## 6. Safe Input Conversion — `safe_eval_price()`

When a customer types a price into a search box or chatbot, it arrives as a **string**. You must convert it to a number before comparing. Python's built-in `eval()` can execute any code, so it is dangerous on user input. Always use a safe wrapper instead:

```python
def safe_eval_price(raw_input):
    """
    Safely converts a string price input to a float.

    Why not use eval() directly?
        eval() executes any Python expression — a security risk.
        This function only converts numeric values.

    Args:
        raw_input (str): The raw string from user or external system.

    Returns:
        float or None: The numeric value, or None if conversion fails.
    """
    try:
        value = float(raw_input)
        return value
    except (ValueError, TypeError):
        return None
```

```python
# Simulate price inputs arriving from a customer search filter
inputs = ["1500", "299.99", "abc", "", "2 000", None]

print("eCOMMart Price Filter Results:")
print("-" * 40)

for raw in inputs:
    price = safe_eval_price(raw)

    if is_nan(price) or price is None:
        print(f"  {raw!r:10} → Invalid — please enter a number.")
    elif price >= 2000:
        print(f"  {raw!r:10} → Premium range  (₹{price:.2f})")
    elif price >= 1000:
        print(f"  {raw!r:10} → Mid range      (₹{price:.2f})")
    elif price >= 500:
        print(f"  {raw!r:10} → Budget range   (₹{price:.2f})")
    else:
        print(f"  {raw!r:10} → Economy range  (₹{price:.2f})")
```
```
# Output:
eCOMMart Price Filter Results:
----------------------------------------
  '1500'     → Mid range      (₹1500.00)
  '299.99'   → Economy range  (₹299.99)
  'abc'      → Invalid — please enter a number.
  ''         → Invalid — please enter a number.
  '2 000'    → Invalid — please enter a number.
  None       → Invalid — please enter a number.
```

```
"1500"  → float("1500")  → 1500.0  ← valid
"abc"   → float("abc")   → ValueError → return None ← caught safely
"2 000" → float("2 000") → ValueError → return None ← space breaks it
None    → float(None)    → TypeError  → return None ← caught safely
```

> **When is `eval()` itself used?**
> `eval()` evaluates a string as a Python expression: `eval("2 + 3 * 10") → 32`. It is powerful but dangerous with user input — a user could type code that harms your system. In agent tools, always use `safe_eval_price()` style guards instead.

---

## 7. Complete Mini Agent Tool — Delivery Eligibility Checker

This brings together `is_nan()`, `safe_eval_price()`, and `if-elif-else` into one agent-ready function. This is the pattern AI agents use as a "tool" — receive raw string input, validate it, apply business logic, return a structured result:

```python
import math

def check_delivery_eligibility(raw_cart_value, pin_code):
    """
    eCOMMart Agent Tool: Checks delivery eligibility and estimated time.

    Args:
        raw_cart_value (str): Cart total as entered by the user.
        pin_code       (str): Customer's delivery PIN code.

    Returns:
        str: A formatted delivery eligibility message.
    """
    # Step 1 — Safely convert input
    cart_value = safe_eval_price(raw_cart_value)

    # Step 2 — Check for invalid value
    if is_nan(cart_value) or cart_value is None:
        return "Invalid cart value. Please enter a valid amount."

    # Step 3 — Determine delivery zone from PIN code
    if pin_code.startswith("40"):
        zone = "Mumbai"
        eta  = "Same-day delivery"
    elif pin_code.startswith("56"):
        zone = "Bangalore"
        eta  = "Next-day delivery"
    elif pin_code.startswith("11"):
        zone = "Delhi"
        eta  = "2-day delivery"
    else:
        zone = "Other"
        eta  = "5-7 day delivery"

    # Step 4 — Check free delivery threshold
    if cart_value >= 500:
        delivery_msg = "FREE delivery!"
    else:
        shortfall    = 500 - cart_value
        delivery_msg = f"Add ₹{shortfall:.2f} more for FREE delivery."

    return (
        f"Zone     : {zone}\n"
        f"ETA      : {eta}\n"
        f"Cart     : ₹{cart_value:.2f}\n"
        f"Delivery : {delivery_msg}"
    )
```

```python
# Test 1 — Valid cart, Mumbai PIN
print(check_delivery_eligibility("1200", "400001"))
```
```
# Output:
Zone     : Mumbai
ETA      : Same-day delivery
Cart     : ₹1200.00
Delivery : FREE delivery!
```

```python
# Test 2 — Below free delivery threshold, Bangalore PIN
print(check_delivery_eligibility("350", "560001"))
```
```
# Output:
Zone     : Bangalore
ETA      : Next-day delivery
Cart     : ₹350.00
Delivery : Add ₹150.00 more for FREE delivery.
```

```python
# Test 3 — Invalid cart value, Delhi PIN
print(check_delivery_eligibility("abc", "110001"))
```
```
# Output:
Invalid cart value. Please enter a valid amount.
```

---

## Tasks

### Task 1: eCOMMart Cart Discount Calculator

Build the checkout module. Apply the right discount based on cart total.

**Rules:**
- Cart ≥ ₹3000 → 25% discount
- Cart ≥ ₹2000 → 15% discount
- Cart ≥ ₹1000 → 10% discount
- Cart ≥ ₹500  →  5% discount
- Below ₹500   → No discount

```python
cart_total = float(input("Enter your eCOMMart cart total (₹): "))

if cart_total >= 3000:
    discount = 0.25
elif cart_total >= 2000:
    discount = 0.15
elif cart_total >= 1000:
    discount = 0.10
elif cart_total >= 500:
    discount = 0.05
else:
    discount = 0.0

final = cart_total - (cart_total * discount)
print(f"Discount Applied : {int(discount * 100)}%")
print(f"Final Amount     : ₹{final:.2f}")
```
```
# Expected Output (with input 3500):
Enter your eCOMMart cart total (₹): 3500
Discount Applied : 25%
Final Amount     : ₹2625.00
```

```
₹3500 → 25% → ₹2625.00
₹2200 → 15% → ₹1870.00
₹1100 → 10% → ₹990.00
₹600  →  5% → ₹570.00
₹200  →  0% → ₹200.00
```

---

### Task 2: Product Return Eligibility Checker

eCOMMart's return policy:
- Within 7 days + not damaged → eligible for **return**
- Within 7 days + damaged → eligible for **replacement**
- 8–30 days → **warranty claim** only
- Over 30 days → **not eligible**

```python
days_since_delivery = int(input("How many days since delivery? "))
is_damaged = input("Is the product damaged? (yes/no): ").lower()

if days_since_delivery <= 7 and is_damaged == 'no':
    print("Eligible for return.")
elif days_since_delivery <= 7 and is_damaged == 'yes':
    print("Eligible for replacement.")
elif days_since_delivery <= 30:
    print("Only warranty claim possible.")
else:
    print("Not eligible for any return.")
```
```
# Expected Outputs:
days=5,  damaged=no  → Eligible for return.
days=5,  damaged=yes → Eligible for replacement.
days=15, damaged=no  → Only warranty claim possible.
days=35, damaged=no  → Not eligible for any return.
```

---

### Task 3: Safe Price Filter (Agent Tool Practice)

Use `is_nan()` and `safe_eval_price()` from above to validate and classify a list of price inputs.

```python
# Price inputs simulating a search filter submitted by users
price_inputs = ["199", "1500", None, "premium", "", "4999"]

for raw in price_inputs:
    price = safe_eval_price(raw)

    if is_nan(price) or price is None:
        print(f"  {raw!r} → Invalid input — please enter a valid number.")
    elif price >= 2000:
        print(f"  {raw!r} → Premium  (₹{price:.2f})")
    elif price >= 500:
        print(f"  {raw!r} → Standard (₹{price:.2f})")
    else:
        print(f"  {raw!r} → Economy  (₹{price:.2f})")
```
```
# Expected Output:
  '199'     → Economy  (₹199.00)
  '1500'    → Standard (₹1500.00)
  None      → Invalid input — please enter a valid number.
  'premium' → Invalid input — please enter a valid number.
  ''        → Invalid input — please enter a valid number.
  '4999'    → Premium  (₹4999.00)
```
