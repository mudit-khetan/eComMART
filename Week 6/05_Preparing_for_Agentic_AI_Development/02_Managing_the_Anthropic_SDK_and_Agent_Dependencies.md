# Managing the Anthropic SDK and Agent Dependencies

## Lesson purpose

In eComMART, your ordinary Python functions can already check stock levels and return a clear message. In a future week, an AI assistant could *choose* when to use one of those functions. Before then, developers need to understand how an AI software library fits into a Python project and how to keep its dependencies under control.

This is a **concept-and-setup lesson**, not an AI integration assignment. You will examine an optional Python SDK (software development kit), see how its version could be recorded, and verify that the eComMART stock rule still works without an AI connection.

**Core for Week 6:** use a virtual environment, understand dependencies, maintain `requirements.txt`, and run local tests. **Optional/stretch only:** install the Anthropic SDK and inspect its installed version. **No account, real API key, subscription, payment, or live API call is required for any graded or required Week 6 work.**

## Learning objectives

By the end of this lesson, you will be able to:

- Explain SDK, LLM provider, dependency, and transitive dependency in plain language.
- Distinguish core eComMART dependencies from optional AI-specific dependencies.
- Install and inspect an optional package using the project's virtual environment.
- Explain why recorded package versions help collaborators reproduce a project.
- Keep stock-alert business logic independent of an AI provider.
- Identify which steps are optional and why no live AI connection is needed.

## 1. Where an SDK fits in the eComMART story

Imagine a store manager asking a future eComMART assistant: “Which products should we reorder?” The assistant might eventually use an LLM (large language model) to understand that question and then run a Python function to check quantities.

**For Week 6, you build and test only the Python part.** You do not need an LLM to decide whether 2 units is below a threshold of 5.

```text
Future possibility (not built this week)

Store manager's question
          |
          v
   LLM interprets request      <-- Future optional AI service
          |
          v
   eComMART stock-check tool    <-- Ordinary Python function
          |
          v
   Stock alert or no alert      <-- Can be tested locally today
```

| Term | Meaning | Why a beginner should care |
|---|---|---|
| Library / package | Reusable code you can install and import | `pytest` is a package used to run tests |
| SDK | A library (and related tools) designed to help your program use a service | The `anthropic` package offers Python methods for Anthropic's API |
| LLM | A model trained to work with language | Later it may interpret a manager's request |
| API | An interface through which programs request work from another service | A future LLM connection would use an API |
| Direct dependency | A package your project chooses to use | `pytest` for your tests |
| Transitive dependency | A package installed because another package needs it | `pip` may install supporting libraries automatically |

**Key distinction:** installing an SDK does **not** mean your program has connected to an LLM. Installing a package, creating a client object, and sending an actual API request are different actions. **Do not send requests in Week 6.**

## 2. Start with a clean, separate practice project

For the optional experiment, make a new folder called `ecommart_sdk_sandbox`. Do **not** edit your Week 5 product catalog or turn the Week 6 low-stock instructor demo into an AI-dependent app.

```text
ecommart_sdk_sandbox/
├── .venv/                    # Generated on your computer
├── stock_rule.py             # Plain Python; no SDK required
├── test_stock_rule.py        # Plain pytest tests
└── requirements.txt          # Record installed packages
```

Open a terminal **inside** `ecommart_sdk_sandbox`, then create the environment:

| System | Create | Activate |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

If PowerShell blocks activation, use Command Prompt and the listed `.bat` command instead of changing machine-wide security settings.

Check that you are using the environment's Python:

```bash
python -c "import sys; print(sys.executable)"
```

**Expected result:** the displayed Python path contains your `ecommart_sdk_sandbox/.venv` folder. Next install the core test dependency:

```bash
python -m pip install pytest
python -m pytest --version
```

**Expected result:** a pytest version appears; no AI service is contacted.

## 3. Keep the stock rule deterministic — core concept

A **deterministic** function returns the same result for the same inputs. It does not need an API key or an internet connection.

Create `stock_rule.py`:

```python
def needs_reorder(quantity, threshold=5):
    """Return True when quantity is below the reorder threshold."""
    if quantity < 0 or threshold < 0:
        raise ValueError("Quantity and threshold cannot be negative")
    return quantity < threshold
```

Create `test_stock_rule.py`:

```python
import pytest

from stock_rule import needs_reorder


def test_below_threshold():
    # Arrange: quantity 2, threshold 5
    # Act and assert:
    assert needs_reorder(2, 5) is True


def test_at_threshold():
    assert needs_reorder(5, 5) is False


def test_negative_quantity():
    with pytest.raises(ValueError):
        needs_reorder(-1, 5)
```

Run:

```bash
python -m pytest -q
```

**Expected result:** `3 passed` (the time and other output may differ). These tests remain valuable even if the project never uses an LLM.

## 4. Optional/stretch — install the Anthropic SDK

**Skip this entire section if you only want to meet Week 6's required outcomes.** The SDK does not appear in `stock_rule.py` or its tests.

The Python package distributed by Anthropic is named `anthropic`. Its verified PyPI release was **`2.4.0` on November 2, 2026**, at the time this lesson was authored. Release versions can change; always verify when updating the course.

Official package page: <https://pypi.org/project/anthropic/>

Only if you choose the optional experiment, run inside `ecommart_sdk_sandbox`:

```bash
python -m pip install anthropic==2.4.0
python -m pip show anthropic
```

**Expected result:** `pip show` includes `Name: anthropic` and `Version: 2.4.0`. This confirms that a Python package is installed. **It does not prove an API connection.**

You may also inspect imports, without creating a client or calling a server:

```bash
python -c "import anthropic; print('Anthropic SDK import succeeded')"
```

If the import succeeds, the message appears. Do **not** use `client.messages.create(...)` or any other network request in Week 6.

**Python-version check:** the SDK documentation specifies Python **3.10 or newer**. If your system has an older Python 3 version, do not force installation for this optional activity; use the core examples and ask your instructor about a supported interpreter.

## 5. Record dependencies without confusing core and stretch

A `requirements.txt` file is a list of installable packages. Its purpose is to help someone else install the dependencies that a project actually needs.

For the **required** stock-rule tests, you need `pytest`. In your core practice project, record the version installed in *your* environment:

```bash
python -m pip freeze > requirements.txt
```

Open the file. It may contain more than one line because dependencies can install additional packages. This is normal.

If you completed the **optional SDK experiment** in this *separate sandbox*, `pip freeze` will also include `anthropic==2.4.0` and its supporting dependencies. That does **not** mean `anthropic` is required for the instructor demo or Week 5 catalog challenge.

For teaching purposes, a direct-dependency list can be easier to read:

```text
# Example OPTIONAL AI sandbox dependencies only
pytest==<version-you-actually-installed>
anthropic==2.4.0
```

The angle-bracket placeholder above is **not** valid to install literally. Replace it with the version reported by `python -m pip show pytest`, or use `pip freeze` to generate a valid file automatically.

| Approach | Purpose | Student takeaway |
|---|---|---|
| `python -m pip install pytest` | Install a package into the active environment | Core |
| `python -m pip freeze > requirements.txt` | Record currently installed package versions | Core |
| `python -m pip install -r requirements.txt` | Recreate dependencies in another environment | Core |
| `python -m pip install anthropic==2.4.0` | Add the optional AI provider SDK | Stretch only |

**Note:** `pip freeze` records the current environment, not necessarily only packages your code imports. Keeping optional experiments in a separate environment avoids adding unnecessary packages to the required project.

## 6. Common mistakes and troubleshooting

| What happens | Likely cause | What to do |
|---|---|---|
| `No module named pytest` | Wrong environment or pytest not installed | Activate `.venv`; run `python -m pip install pytest` |
| `No module named anthropic` | Optional SDK not installed | Skip it for core work, or install only in the optional sandbox |
| Installed package appears in another project | Wrong interpreter or inactive `.venv` | Check `python -c "import sys; print(sys.executable)"` |
| `pip` complains about Python version | Interpreter too old for that release | Use a supported Python version or skip the optional SDK |
| `requirements.txt` contains many extra packages | `pip freeze` captured transitive dependencies | This is expected; use a clean venv for each project |
| Student thinks a placeholder key enables Claude | Confusing configuration with authentication | A fake key never grants service access; no API call is needed |

## 7. Guided practice and knowledge check

**Core practice (local, no API):**

1. Explain in one sentence why eComMART's reorder rule should not depend on an LLM.
2. Run the three tests for `needs_reorder()`.
3. Generate a `requirements.txt` from your environment and locate the pytest entry.
4. Explain how you would recreate the environment with `python -m pip install -r requirements.txt`.

**Optional/stretch:** in a separate sandbox, install `anthropic==2.4.0`, use `pip show` to confirm its version, then explain why installing an SDK is not the same as making an API request. Do not make one.

**Check your understanding:**

- **Q:** Which part of the low-stock tool should be tested first: the Python rule or the LLM connection? **A:** The Python rule, because it can be checked reliably and locally.
- **Q:** Is `anthropic` needed for the Week 6 required test suite? **A:** No.
- **Q:** Does `requirements.txt` store an API key? **A:** No; package dependencies and configuration secrets are different things.

## 8. Recap and what comes next

You now know that an SDK is an optional bridge to a service, while eComMART's business rules are ordinary Python that can be tested without one. Keep every project isolated, record only its actual dependencies, and do not mix experimental AI packages into the required catalog application.

**Next lesson:** `03_API_Key_Configuration_for_Claude.md` shows the *shape* of safe API-key configuration using a fake placeholder. It does **not** authenticate or contact Claude.

### Reference links

- Anthropic Python SDK documentation: <https://github.com/anthropics/anthropic-sdk-python>
- PyPI package/version record (accessed November 4, 2026): <https://pypi.org/project/anthropic/2.4.0/>
