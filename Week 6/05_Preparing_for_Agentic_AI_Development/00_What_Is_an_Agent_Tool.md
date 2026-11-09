# What Is an Agent Tool?

## Lesson purpose

In Weeks 3–5, you learned to write Python functions, organize data, handle errors, and store eComMART products in SQLite. You might have heard the words **LLM**, **agentic AI**, and **agent tool**, but you have not needed to build an AI integration yet. Before we discuss AI packages or API keys, we will make those words understandable.

Imagine an eComMART employee asking, “Which products need to be reordered today?” A normal Python program can check product stock and return a clear answer. Later, an AI assistant could understand the employee's question and decide to ask that Python program for the stock information. The Python program remains responsible for the actual calculation.

**Core for Week 6:** understand the vocabulary and build/test one small, predictable Python function that could *later* be an agent tool. **Optional/stretch:** exploring how an LLM might request that tool. There is **no required LLM connection**, no account signup, no real API key, and no paid API call this week.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain an **LLM** in everyday language without confusing it with a database.
- Explain **agentic AI** as a system that can choose steps and make use of tools toward a goal.
- Describe an **agent tool** as a capability a system can call to perform a specific job.
- Distinguish the role of a language model from the role of normal Python business logic.
- Build and manually check a deterministic eComMART stock-checking function.
- Explain why a tool should be tested before an LLM is allowed to use it.

## 1. Start with the business question

The eComMART warehouse team tracks products and how many units are left. For a simple illustration, imagine this data:

| Product | Units available | Alert threshold | Should there be an alert? |
|---|---:|---:|---|
| Wireless Barcode Scanner | 4 | 10 | Yes |
| Thermal Label Roll | 120 | 10 | No |
| USB-C Docking Station | 8 | 10 | Yes |

The rule is straightforward: if **stock is less than the threshold**, an alert is needed. If the two numbers are equal, there is no alert. You can implement this rule with a Python function. **AI is not needed to compare two numbers.**

Now imagine a person types, “Please check the scanner and tell me whether we need to order more.” Understanding that conversational request is different from calculating whether `4 < 10`. Those two responsibilities can be connected later, but they are not the same task.

## 2. What is an LLM?

**LLM** means **large language model**. It is a type of AI system trained on large amounts of text and other data to produce or work with language. It can help interpret a question, explain information, or draft a reply.

A useful beginner comparison is:

- **LLM:** can interpret an employee's sentence such as “Is the scanner running low?”
- **Python stock function:** can check actual numbers using a rule such as `stock < threshold`.
- **SQLite database:** can store the current product records so the application can retrieve them.

An LLM does **not automatically know** what is in your local Week 5 SQLite database. Nor should you assume its response is a verified inventory fact. To answer accurately, an AI-enabled application would need a safe, explicitly connected way to access the appropriate data.

> **New term — prompt:** the instruction or question a person sends to an LLM. Example: “Explain which products are low on stock.” You do not need to send any prompts to a real model in Week 6.

## 3. What does “agentic AI” mean?

In this program, **agentic AI** refers to an AI-enabled system that can work toward a goal by choosing actions or steps, sometimes by using tools. For example, instead of only generating text about inventory, a future eComMART assistant might:

1. Understand the request, “Check which products need restocking.”
2. Select a stock-checking tool to obtain relevant inventory information.
3. Use the returned result to prepare a clear answer.
4. Ask for a person's approval before taking a sensitive action such as placing an order.

This does **not** mean the AI should be free to do anything. Good systems limit which tools it can access, validate inputs, record important actions, and require human review where appropriate.

An ordinary chatbot that only answers messages is not automatically performing actions. An agentic system may use the model's language abilities to **select** an available action, while code and permissions control what that action actually does.

## 4. What is an agent tool?

An **agent tool** is a specific capability that an AI-enabled system may be allowed to call. A tool might be a Python function that checks inventory, searches approved data, or formats a stock alert. Think of it as a clearly labeled action, not as an AI model itself.

For our beginner example, the tool contract (a description of what goes in and comes out) is:

| Part | eComMART example |
|---|---|
| Tool name | `is_low_stock` |
| Input | `stock` and `threshold`, both whole numbers |
| Rule | Return whether `stock < threshold` |
| Output | `True` or `False` |
| Side effect | None: it does not change the database, order products, or send notifications |

**Input** means the information you give a function. **Output** is the value it returns. A **side effect** is a change outside the returned value, such as updating a database or sending an email. For Week 6, begin with tools that have no side effects.

### Where each part belongs

```text
Employee asks a question
          |
          v
Future LLM-enabled assistant (NOT built or called this week)
          |
          | may choose a permitted tool
          v
Python stock-checking function
          |
          | applies the precise stock rule
          v
True / False result
          |
          v
Future assistant presents a response to the employee
```

In **this week's actual exercise**, you will call the Python function yourself. Everything involving the future assistant is a **conceptual illustration**, not a hidden API requirement.

## 5. Guided example — write a tool-shaped Python function

Create a new practice folder named `agent_tool_practice`. This is a small experiment, not a replacement for your Week 5 product catalog or the instructor's separate low-stock notifier.

Create `stock_tool.py`:

```python
# stock_tool.py

def is_low_stock(stock, threshold):
    """Return True if units available are below the threshold."""
    if not isinstance(stock, int) or isinstance(stock, bool):
        raise ValueError("stock must be a whole number")
    if not isinstance(threshold, int) or isinstance(threshold, bool):
        raise ValueError("threshold must be a whole number")
    if stock < 0 or threshold < 0:
        raise ValueError("stock and threshold cannot be negative")
    return stock < threshold


print(is_low_stock(4, 10))
print(is_low_stock(120, 10))
print(is_low_stock(10, 10))
```

Open a terminal in `agent_tool_practice` and run:

```bash
python stock_tool.py
```

**Expected output:**

```text
True
False
False
```

### Read the code in small steps

1. `def is_low_stock(stock, threshold):` defines a reusable function and names its two inputs.
2. `isinstance(..., int)` checks whether each input is a Python whole number. The extra Boolean check prevents `True`/`False` from being accepted as quantities.
3. `raise ValueError(...)` reports that the caller supplied an unsuitable value.
4. `return stock < threshold` applies the business rule and returns a Boolean (`True` or `False`).
5. The three `print(...)` calls let you see the returned values.

**Why validate inputs?** A future agent might supply an incorrect argument, but ordinary Python programs and people can also make mistakes. Rejecting invalid quantities makes the function safer and easier to test.

**What is deterministic?** A deterministic function returns the same answer for the same valid inputs. `is_low_stock(4, 10)` always returns `True`; there is no randomness or external service involved.

## 6. Check the function before anyone connects an LLM

You recently learned `pytest`. Here is a short preview of how the same function can be tested. To avoid running the three `print` calls when the file is imported, first replace those calls in `stock_tool.py` with this block:

```python
if __name__ == "__main__":
    print(is_low_stock(4, 10))
    print(is_low_stock(120, 10))
    print(is_low_stock(10, 10))
```

`__name__ == "__main__"` means “run these prints only when this file is started directly.” Importing the function for a test will not print sample results.

Create `test_stock_tool.py` in the **same folder**:

```python
import pytest
from stock_tool import is_low_stock


def test_below_threshold():
    # Arrange: sample stock and threshold
    stock, threshold = 4, 10
    # Act
    result = is_low_stock(stock, threshold)
    # Assert
    assert result is True


def test_equal_to_threshold():
    assert is_low_stock(10, 10) is False


def test_negative_stock_rejected():
    with pytest.raises(ValueError):
        is_low_stock(-1, 10)
```

With your Week 6 `.venv` active and `pytest` installed, run from the `agent_tool_practice` folder:

```bash
python -m pytest -q
```

**Expected result:** `3 passed`. If you see `No module named pytest`, activate the environment from earlier lessons and install the required package in that environment.

These three tests are **guided practice**. They do **not** add extra requirements to the independent Week 5 catalog challenge, which still asks for only **2–3 simple pytest tests**.

## 7. What could go wrong without tests?

Suppose someone changes the final line to:

```python
return stock <= threshold
```

Now `is_low_stock(10, 10)` returns `True`, which breaks our agreed eComMART rule. The equal-to-threshold test catches it.

Other problems to watch for:

| Problem | Why it matters | Safe response |
|---|---|---|
| The tool accepts `-5` stock | Negative inventory might be an invalid input for this exercise | Validate inputs and raise a clear error |
| A tool changes records when it should only read | A simple question could unexpectedly change business data | Keep this week's tool read-only and side-effect-free |
| An LLM gives a plausible but invented quantity | A natural-language answer is not proof of current stock | Use verified data from approved tools |
| An API call is required to run tests | Tests become slower, less predictable, and potentially costly | Test local deterministic logic first |

## 8. Guided practice — explain a tool in everyday language

Without writing more code, answer these questions:

1. Which part would understand “Could you check the scanners?” in a future AI assistant?
2. Which part should decide whether `4` is less than `10`?
3. If the stock count is exactly `10` and threshold is `10`, should the alert trigger?
4. Does an LLM automatically have access to `ecommart.db` on your computer?
5. Why is a function without database writes a good first agent tool?

**Self-check:** (1) An LLM-enabled assistant might interpret the request. (2) The Python function. (3) No. (4) No, an application must explicitly connect approved access. (5) It is easier to predict, test, and run safely.

### Optional/stretch — think about a future interface

A future AI application may describe a callable tool using its name, purpose, and expected inputs, then let the model request its use. The application still validates inputs and executes the actual Python function. This is **conceptual only**: no SDK code, live Claude request, or tool-calling framework is needed here.

## 9. Common mistakes and troubleshooting

| Problem | Likely cause | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'stock_tool'` | Test run from another folder or the file is named differently | Run from `agent_tool_practice` and check the filename |
| `No module named pytest` | Wrong environment or pytest not installed | Activate `.venv`; follow the pip lesson |
| Equal-threshold test fails | Used `<=` instead of `<` | Return `stock < threshold` |
| You see three printed lines during pytest | Sample prints run during import | Move prints under `if __name__ == "__main__":` |
| Confusion between LLM and function | The two perform different jobs | LLM interprets language; Python enforces the stock rule |
| Feeling that a Claude account is needed | The conceptual diagram mentions a future assistant | No account, real key, signup, payment, or API call is required |

## 10. Knowledge check

1. What does **LLM** stand for?
2. What makes a system **agentic** in this lesson's simplified explanation?
3. Is an agent tool the same thing as an LLM?
4. What does **deterministic** mean?
5. What should you verify before letting an AI-enabled system call a tool?

**Answers:** (1) Large language model. (2) It can choose steps or permitted tools to pursue a goal. (3) No; a tool is a callable capability, often ordinary code. (4) Same inputs give the same result. (5) Inputs, expected outputs, errors, permissions, and safe behavior through local tests.

## Lesson recap

- An **LLM** works with language; it is not a substitute for verified database facts.
- **Agentic AI** may choose actions using approved tools to work toward a goal.
- An **agent tool** can be an ordinary, well-described Python function.
- A small, deterministic, side-effect-free stock function is an excellent first tool to understand and test.
- **Core:** Python functions, tests, and safe configuration. **Optional/stretch:** an AI SDK or LLM integration later. No real API key, signup, paid service, or live API call is required.

**Next lesson:** `01_Isolated_AI_Project_Environments.md` explains why future AI-enabled Python projects need their own `.venv` and carefully managed packages.
