# Advanced Sets

In this notebook we cover every built-in set method in depth. All examples use a consistent B2B eCom context — vendor management across quarters — so you can see how each method applies to real data problems.

**What we will cover:**

1. `add()`
2. `clear()`
3. `copy()`
4. `remove()` vs `discard()` — full comparison
5. `difference()` / `difference_update()`
6. `intersection()` / `intersection_update()`
7. `union()` / `update()`
8. `isdisjoint()` / `issubset()` / `issuperset()`
9. `symmetric_difference()` / `symmetric_difference_update()`
10. Exercise

---

```
┌───────────────────────────────────────────────────────────────────────┐
│                  Quick Reference — Set Methods                        │
├──────────────────────────────┬────────────────────────────────────────┤
│  Method                      │  What it does                          │
├──────────────────────────────┼────────────────────────────────────────┤
│  add(x)                      │  Add element x                         │
│  clear()                     │  Remove all elements                   │
│  copy()                      │  Return a new independent copy         │
│  remove(x)                   │  Remove x — KeyError if not found      │
│  discard(x)                  │  Remove x — no error if not found      │
│  difference(s2)              │  Items in s1 but NOT in s2 (new set)   │
│  difference_update(s2)       │  Same but modifies s1 in place         │
│  intersection(s2)            │  Items in BOTH s1 and s2 (new set)     │
│  intersection_update(s2)     │  Same but modifies s1 in place         │
│  union(s2)                   │  All items from s1 and s2 (new set)    │
│  update(s2)                  │  Same but modifies s1 in place         │
│  isdisjoint(s2)              │  True if s1 and s2 share no elements   │
│  issubset(s2)                │  True if s1 is contained within s2     │
│  issuperset(s2)              │  True if s1 contains all of s2         │
│  symmetric_difference(s2)    │  Items in exactly ONE set (new set)    │
│  symmetric_difference_update │  Same but modifies s1 in place         │
└──────────────────────────────┴────────────────────────────────────────┘
```

> **Pattern to know:** Methods ending in `_update` modify the set **in place** and return `None`. The version without `_update` returns a **new set** and leaves the original unchanged. Never write `s1 = s1.difference_update(s2)` — you will overwrite `s1` with `None`.

---

## 1. `add()`

`add()` inserts one element into the set. If the element already exists, nothing changes.

> **B2B eCom context:** Registering active vendors on the platform.

```python
active_vendors = set()
print(active_vendors)
```
```
# Output:
set()
```

```python
active_vendors.add('Tata Electronics')
print(active_vendors)
```
```
# Output:
{'Tata Electronics'}
```

```python
active_vendors.add('Reliance Digital')
print(active_vendors)
```
```
# Output:
{'Reliance Digital', 'Tata Electronics'}
```

```python
# Adding a duplicate — no change
active_vendors.add('Tata Electronics')
print(active_vendors)
```
```
# Output:
{'Reliance Digital', 'Tata Electronics'}
```

---

## 2. `clear()`

`clear()` removes **all elements** from the set. The set itself still exists — it is just empty.

```python
temp = {'Tata Electronics', 'Reliance Digital'}
print(temp)
```
```
# Output:
{'Reliance Digital', 'Tata Electronics'}
```

```python
temp.clear()
print(temp)
```
```
# Output:
set()
```

> **When is this useful?** Resetting a session's active vendor list, clearing a pending notification set, or starting a new processing batch.

---

## 3. `copy()`

`copy()` creates a **new independent set**. Changes to the original do not affect the copy.

> **Why this matters:** If you write `backup = original`, both names point to the **same object**. `copy()` creates a truly separate one.

```python
vendors_q1 = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
vendors_backup = vendors_q1.copy()

print(vendors_q1)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
```

```python
print(vendors_backup)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
```

```python
# Add to original
vendors_q1.add('Wipro Hardware')
print(vendors_q1)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
```

```python
# Backup is unchanged
print(vendors_backup)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
```

```
vendors_q1     ──→  {'Tata', 'Reliance', 'Infosys', 'Wipro'}  ← changed
vendors_backup ──→  {'Tata', 'Reliance', 'Infosys'}            ← unchanged
```

---

## 4. `remove()` vs `discard()`

Both remove an element. The difference is what happens when the element **is not in the set**:

| Method | Element found | Element NOT found |
|---|---|---|
| `remove(x)` | Removes it | Raises `KeyError` |
| `discard(x)` | Removes it | Does nothing — no error |

```python
s = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
print(s)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
```

```python
# remove() — works when element exists
s.remove('Infosys Supplies')
print(s)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital'}
```

```python
# remove() — raises KeyError when element is missing
try:
    s.remove('Unknown Vendor')
except KeyError as e:
    print(f"KeyError: {e}")
```
```
# Output:
KeyError: 'Unknown Vendor'
```

```python
# discard() — removes when element exists
s.discard('Reliance Digital')
print(s)
```
```
# Output:
{'Tata Electronics'}
```

```python
# discard() — no error when element is missing
s.discard('Unknown Vendor')
print(s)
```
```
# Output:
{'Tata Electronics'}
```

```
┌──────────────────────────────────────────────────────┐
│  Use discard() when you're not sure the item exists  │
│  Use remove()  when you know it must be there        │
└──────────────────────────────────────────────────────┘
```

---

## 5. `difference()` / `difference_update()`

**`difference(s2)`** returns a **new set** with elements that are in `s1` but **not** in `s2`. The original is unchanged.

**`difference_update(s2)`** does the same but **modifies `s1` in place**. Returns `None`.

> **B2B eCom context:** Which vendors were active in Q1 but did NOT return in Q2 (churned vendors)?

```python
vendors_q1 = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
vendors_q2 = {'Reliance Digital', 'Wipro Hardware', 'HCL Tech'}

print(vendors_q1)
print(vendors_q2)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
{'Reliance Digital', 'Wipro Hardware', 'HCL Tech'}
```

```python
# difference() — new set, original unchanged
churned = vendors_q1.difference(vendors_q2)
print(churned)
```
```
# Output:
{'Tata Electronics', 'Infosys Supplies'}
```

```python
# vendors_q1 is unchanged
print(vendors_q1)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
```

```
vendors_q1:  {Tata, Reliance, Infosys, Wipro}
vendors_q2:         {Reliance,          Wipro, HCL}
                     ────────            ─────  ← in both, excluded
difference:  {Tata,          Infosys         }  ← Q1 only (churned)
```

```python
# difference_update() — modifies s1 in place
s1 = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
s2 = {'Reliance Digital', 'HCL Tech'}

print(f"s1 before: {s1}")
s1.difference_update(s2)
print(f"s1 after : {s1}")
```
```
# Output:
s1 before: {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
s1 after : {'Tata Electronics', 'Infosys Supplies'}
```

---

## 6. `intersection()` / `intersection_update()`

**`intersection(s2)`** returns a **new set** with elements that appear in **both** sets.

**`intersection_update(s2)`** keeps only the common elements in `s1` in place. Returns `None`.

> **B2B eCom context:** Which vendors were active in **both** Q1 and Q2 (retained vendors)?

```python
vendors_q1 = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
vendors_q2 = {'Reliance Digital', 'Wipro Hardware', 'HCL Tech'}

# intersection() — new set
retained = vendors_q1.intersection(vendors_q2)
print(retained)
```
```
# Output:
{'Reliance Digital', 'Wipro Hardware'}
```

```python
# vendors_q1 unchanged
print(vendors_q1)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
```

```
vendors_q1:  {Tata, Reliance, Infosys, Wipro}
vendors_q2:         {Reliance,          Wipro, HCL}
                      ───────            ────  ← in both
intersection:         {Reliance,         Wipro}   ← retained
```

```python
# intersection_update() — modifies s1 in place
s1 = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
s2 = {'Reliance Digital', 'Infosys Supplies', 'HCL Tech'}

print(f"s1 before: {s1}")
s1.intersection_update(s2)
print(f"s1 after : {s1}")
```
```
# Output:
s1 before: {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies'}
s1 after : {'Reliance Digital', 'Infosys Supplies'}
```

---

## 7. `union()` / `update()`

**`union(s2)`** returns a **new set** with all elements from both sets. Duplicates appear only once.

**`update(s2)`** adds all elements from `s2` into `s1` in place. Returns `None`.

> **B2B eCom context:** All vendors who were active in either Q1 or Q2 (full vendor pool).

```python
vendors_q1 = {'Tata Electronics', 'Reliance Digital', 'Wipro Hardware'}
vendors_q2 = {'Reliance Digital', 'HCL Tech', 'Infosys Supplies'}

# union() — new set
all_vendors = vendors_q1.union(vendors_q2)
print(all_vendors)
```
```
# Output:
{'Tata Electronics', 'Infosys Supplies', 'Wipro Hardware', 'HCL Tech', 'Reliance Digital'}
```

```python
# vendors_q1 unchanged
print(vendors_q1)
```
```
# Output:
{'Tata Electronics', 'Reliance Digital', 'Wipro Hardware'}
```

```
vendors_q1:   {Tata, Reliance, Wipro}
vendors_q2:          {Reliance, HCL, Infosys}
union:        {Tata, Reliance, Wipro, HCL, Infosys}  ← all, no duplicates
```

```python
# update() — modifies s1 in place
s1 = {'Tata Electronics', 'Reliance Digital'}
s2 = {'Reliance Digital', 'HCL Tech'}

print(f"s1 before: {s1}")
s1.update(s2)
print(f"s1 after : {s1}")
```
```
# Output:
s1 before: {'Reliance Digital', 'Tata Electronics'}
s1 after : {'Reliance Digital', 'HCL Tech', 'Tata Electronics'}
```

---

## 8. `isdisjoint()` / `issubset()` / `issuperset()`

These three methods return a **Boolean** (`True` or `False`) — they check relationships between sets without changing them.

### `isdisjoint(s2)` — Do the sets share any elements?

Returns `True` if the sets have **no elements in common** (null intersection).

```python
online_vendors  = {'Tata Electronics', 'Reliance Digital'}
offline_vendors = {'Wipro Hardware', 'HCL Tech'}
overlap_vendors = {'Tata Electronics', 'Infosys Supplies'}

print(online_vendors.isdisjoint(offline_vendors))
```
```
# Output:
True
```

```python
# online and overlap share 'Tata Electronics'
print(online_vendors.isdisjoint(overlap_vendors))
```
```
# Output:
False
```

```
online:   {Tata, Reliance}
offline:  {Wipro, HCL}         → no overlap → isdisjoint = True
overlap:  {Tata, Infosys}      → shares Tata → isdisjoint = False
```

### `issubset(s2)` — Is s1 entirely contained within s2?

Returns `True` if every element of `s1` is also in `s2`.

```python
premium_vendors = {'Tata Electronics', 'Reliance Digital'}
all_vendors     = {'Tata Electronics', 'Reliance Digital', 'Wipro Hardware', 'HCL Tech'}

print(premium_vendors.issubset(all_vendors))
```
```
# Output:
True
```

### `issuperset(s2)` — Does s1 contain all of s2?

Returns `True` if `s1` contains every element of `s2`.

```python
print(all_vendors.issuperset(premium_vendors))
```
```
# Output:
True
```

```
premium_vendors: {Tata, Reliance}
all_vendors:     {Tata, Reliance, Wipro, HCL}

premium ⊆ all   → issubset    → True  (premium fits inside all)
all ⊇ premium   → issuperset  → True  (all contains premium)
```

---

## 9. `symmetric_difference()` / `symmetric_difference_update()`

**`symmetric_difference(s2)`** returns a **new set** with elements that are in **exactly one** of the two sets — not in both.

**`symmetric_difference_update(s2)`** does the same but modifies `s1` in place. Returns `None`.

> **B2B eCom context:** Which vendors appeared in **only one** quarter — either new arrivals or those who churned?

```python
vendors_q1 = {'Tata Electronics', 'Reliance Digital', 'Wipro Hardware'}
vendors_q2 = {'Reliance Digital', 'HCL Tech', 'Infosys Supplies'}

exclusive = vendors_q1.symmetric_difference(vendors_q2)
print(exclusive)
```
```
# Output:
{'Tata Electronics', 'Wipro Hardware', 'Infosys Supplies', 'HCL Tech'}
```

```
vendors_q1:  {Tata,  Reliance, Wipro}
vendors_q2:          {Reliance, HCL, Infosys}
                       ────────  ← in both, excluded

symmetric:   {Tata,             Wipro, HCL, Infosys}
              ← Q1 only →       ← Q2 only →
```

```python
# symmetric_difference_update() — modifies s1 in place
s1 = {'Tata Electronics', 'Reliance Digital', 'Wipro Hardware'}
s2 = {'Reliance Digital', 'HCL Tech'}

print(f"s1 before: {s1}")
s1.symmetric_difference_update(s2)
print(f"s1 after : {s1}")
```
```
# Output:
s1 before: {'Tata Electronics', 'Reliance Digital', 'Wipro Hardware'}
s1 after : {'Tata Electronics', 'HCL Tech', 'Wipro Hardware'}
```

---

## Exercise: eCOMMart — Quarterly Vendor Analysis

The eCOMMart platform team wants to analyse vendor activity across two quarters using set operations.

**You are given:**

```python
q1_vendors = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
q2_vendors = {'Reliance Digital', 'Wipro Hardware', 'HCL Tech', 'Infosys Supplies'}
```

**Tasks:**

1. Find vendors who were active in **both** quarters (retained)
2. Find vendors who were active in **Q1 only** (churned)
3. Find vendors who joined in **Q2 only** (new)
4. Find **all** vendors across both quarters
5. Find vendors who appeared in **exactly one** quarter
6. Check if `'HCL Tech'` is in Q2
7. Check if Q1 and Q2 share any vendors (are they disjoint?)
8. Check if the retained vendors are a subset of all vendors

```python
# Solution
q1_vendors = {'Tata Electronics', 'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
q2_vendors = {'Reliance Digital', 'Wipro Hardware', 'HCL Tech', 'Infosys Supplies'}

# Task 1 — Retained (in both quarters)
retained = q1_vendors.intersection(q2_vendors)
print(f"Retained (both quarters) : {retained}")

# Task 2 — Churned (Q1 only)
churned = q1_vendors.difference(q2_vendors)
print(f"Churned  (Q1 only)       : {churned}")

# Task 3 — New vendors (Q2 only)
new_vendors = q2_vendors.difference(q1_vendors)
print(f"New      (Q2 only)       : {new_vendors}")

# Task 4 — All vendors
all_vendors = q1_vendors.union(q2_vendors)
print(f"All Vendors              : {all_vendors}")

# Task 5 — Exclusive to one quarter
exclusive = q1_vendors.symmetric_difference(q2_vendors)
print(f"Exclusive to one quarter : {exclusive}")

# Task 6 — Membership check
print(f"\nIs HCL Tech in Q2?        {('HCL Tech' in q2_vendors)}")

# Task 7 — Disjoint check
print(f"Are Q1 & Q2 disjoint?     {q1_vendors.isdisjoint(q2_vendors)}")

# Task 8 — Subset check
print(f"Is retained ⊆ all_vendors? {retained.issubset(all_vendors)}")
```
```
# Expected Output:
Retained (both quarters) : {'Reliance Digital', 'Infosys Supplies', 'Wipro Hardware'}
Churned  (Q1 only)       : {'Tata Electronics'}
New      (Q2 only)       : {'HCL Tech'}
All Vendors              : {'Tata Electronics', 'Wipro Hardware', 'Reliance Digital', 'Infosys Supplies', 'HCL Tech'}
Exclusive to one quarter : {'Tata Electronics', 'HCL Tech'}

Is HCL Tech in Q2?        True
Are Q1 & Q2 disjoint?     False
Is retained ⊆ all_vendors? True
```

---

**You now have a complete understanding of all set methods. Sets are powerful and underused by beginners — keep them in mind whenever you need uniqueness, membership checks, or comparing two groups of data.**
