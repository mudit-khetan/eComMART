# Basic Project Structure

## Lesson purpose

In the previous lesson, you separated an eComMART stock-alert function from the file that runs it. You learned how one `.py` file can import another. Now we will answer a practical question: **where should all the other project files go?**

In Week 5, your eComMART product catalog ran from `05_Product_Catalog_App.py`, used SQLite, and kept its database path directly in the code. That was appropriate for learning database operations, but a growing application needs a predictable place for code, settings, and tests.

We will design a **small, understandable layout** for the instructor's separate low-stock notifier. You will return to reorganize your **own Week 5 catalog** in the later independent challenge; do not rewrite it in this lesson.

**Core for Week 6:** recognize a basic project layout and know where the entry point, reusable functions, dependencies, local configuration, and tests belong. **Optional/stretch:** explore folders for a larger database-backed application or a future LLM wrapper. No live AI API is used.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain the purpose of common project files and folders.
- Identify the entry point, application logic, configuration, and tests.
- Distinguish files you should share from local files you should not share.
- Sketch a manageable eComMART project without adding unnecessary complexity.
- Run a tiny project using an import and a separate `main.py`.
- Prepare for the following lesson on separating logic, configuration, database, and tests.

## 1. Why organize a working program?

Imagine two new teammates join the eComMART team. One needs to fix a low-stock message; the other needs to change the stock threshold. If all the code and settings are mixed together, both must inspect the same long file. A consistent layout gives them a map:

- **Where does the program start?** In the entry-point file.
- **Where are business rules?** In reusable Python modules.
- **Where are local settings?** In `.env`, read through configuration code when needed.
- **Where are dependencies recorded?** In `requirements.txt`.
- **Where are checks written?** In the `tests/` folder.

This organization is called a **project structure**. It does not make Python faster automatically; it helps humans understand, change, and verify the program.

## 2. The small eComMART notifier layout

The final instructor-demo example planned for Week 6 uses this layout:

```text
ecommart_notify/
├── requirements.txt
├── .env.example
├── main.py
├── config.py
├── stock_alert.py
├── anthropic_client.py       # OPTIONAL/STRETCH only
└── tests/
    ├── test_stock_alert.py
    └── test_config.py
```

Your **local working copy** will also have `.venv/` and `.env` after setup. They are not included in the distributed example because each learner creates their own.

| File or folder | Plain-language role | Required or optional? |
|---|---|---|
| `main.py` | Entry point: runs the program and displays results | Core demo |
| `stock_alert.py` | Reusable functions: decide whether stock is low and format an alert | Core demo |
| `config.py` | Reads and interprets settings such as a threshold | Core demo |
| `requirements.txt` | Lists third-party packages needed to reproduce the environment | Core |
| `.env.example` | Shareable template with safe demonstration values | Core demo support |
| `.env` | Private local settings created by each learner | Core exercise: configure **one** variable |
| `.venv/` | Local isolated Python interpreter and installed packages | Core |
| `tests/` | Holds automated checks for expected behavior and errors | Core: **2–3 simple tests** in takeaway |
| `anthropic_client.py` | Thin wrapper for a possible future Claude integration | **Optional/stretch only**; never required to run |

**Do not confuse:** `.env` and `.venv` have similar names, but they do different jobs. `.env` stores text settings; `.venv` contains the isolated Python environment.

**Important:** The optional wrapper file may exist in the teaching example, but the **core** program and its tests must run without installing the Anthropic SDK, entering a real API key, making a network request, or paying for anything.

## 3. Learn the layout with a very small runnable example

Keep `module_practice/` from Lesson 01 intact. Make another folder named `structure_practice` beside it, inside `week6_practice/`:

```text
week6_practice/
├── module_practice/           # from Lesson 01; keep it
└── structure_practice/
    ├── main.py
    ├── stock_alert.py
    ├── requirements.txt
    ├── .env.example
    └── tests/                  # empty for now
```

Create the `tests` **folder** even though you will write tests later. No package installation is required to run this example. `requirements.txt` and `.env.example` are introduced as project files here; their setup is taught fully in Section 04.

### Step 1 — Add reusable logic in `stock_alert.py`

```python
# stock_alert.py

def is_low_stock(stock, threshold):
    """True when the available units are below the threshold."""
    return stock < threshold


def make_alert(product_name, stock, threshold):
    """Return an easy-to-read stock message."""
    if is_low_stock(stock, threshold):
        return f"LOW STOCK: {product_name} has {stock} units left."
    return f"Stock OK: {product_name} has {stock} units."
```

The functions **return** results. They do not ask users for input, open a database, or call an AI API. That is deliberate: one function should have one clear responsibility.

### Step 2 — Put the startup code in `main.py`

```python
# main.py
from stock_alert import make_alert


def main():
    product_name = "Wireless Mouse"
    stock = 3
    threshold = 5
    message = make_alert(product_name, stock, threshold)
    print(message)


if __name__ == "__main__":
    main()
```

`main()` is an ordinary function chosen as the starting point. The `if __name__ == "__main__":` line makes `main()` run when this file is executed directly, not just because another file imports it.

Open a terminal **inside `structure_practice/`**, then run:

```bash
python main.py
```

**Expected output:**

```text
LOW STOCK: Wireless Mouse has 3 units left.
```

If you get a missing-module error, verify that `main.py` and `stock_alert.py` are in the same `structure_practice` folder.

### Step 3 — Add the dependency file

Create `requirements.txt`. For this simple two-file program, no third-party package is needed, so the file can contain a note:

```text
# The tiny stock-alert program uses only Python's standard library.
# pytest and python-dotenv are introduced in other Week 6 lessons.
```

Comments begin with `#`; `pip` ignores them. In the full Week 6 instructor demo, `requirements.txt` will list the actual pinned third-party dependencies needed for testing and `.env` loading. Do **not** add `os`, `pathlib`, or `sqlite3` to the file: they are built into standard Python.

### Step 4 — Add a safe configuration template

Create `.env.example` with one non-secret setting:

```dotenv
LOW_STOCK_THRESHOLD=5
```

**For now, this file is just a template.** The tiny example still sets `threshold = 5` inside `main.py`; editing `.env.example` will **not** change its output. In the following lesson, `config.py` will explain how to actually read a local `.env` and pass that value to the logic.

That distinction matters: a file being present does not mean Python reads it automatically.

### Step 5 — Set aside `tests/`

Create an empty `tests/` folder. Later, `pytest` will discover files with names such as `test_stock_alert.py`. You will check both a successful low-stock case and an edge case. **You do not need to write tests in this lesson**; those come in Section 04 and in the instructor demo.

## 4. Files you share, files you keep local

When someone else needs to run your project, you normally share **source files** (`.py`), `requirements.txt`, a safe `.env.example`, and the `tests/` source files. Each person creates a new `.venv` and their own `.env`.

Create a `.gitignore` in your local working project when you start tracking it with Git:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
```

| Share in a project repository | Keep out of a project repository |
|---|---|
| `main.py`, `stock_alert.py`, `config.py` | `.venv/` (computer-specific installation files) |
| `requirements.txt` | `.env` (local settings; may eventually contain secrets) |
| `.env.example` containing placeholders, not secrets | Python cache files in `__pycache__/` |
| `tests/test_stock_alert.py` | `.pytest_cache/` generated during tests |

`.gitignore` tells Git not to add **untracked** matching files by default. It is not encryption, and it does not erase credentials that were already uploaded. For Week 6, use fake placeholder API keys only; never paste a real key into a lesson, submission, or repository.

## 5. What changes when the application has a database?

Your Week 5 catalog uses SQLite. In a larger project, database operations would belong in their own module so alert-message logic does not need to know SQL details. For example, a **future design sketch** might be:

```text
ecommart_catalog/               # FUTURE challenge design; not files to create now
├── main.py
├── catalog_logic.py
├── database.py
├── config.py
├── requirements.txt
├── .env.example
└── tests/
    ├── test_catalog_logic.py
    └── test_database.py
```

- `catalog_logic.py` could validate product values and decide what an operation means.
- `database.py` could handle SQLite connections and SQL queries.
- `config.py` could read a database path from an environment variable.
- `tests/` could check results without relying on someone manually clicking through operations.

**This is an illustration, not a required folder layout for your independent challenge.** The exact restructuring steps are in `07_Practice_and_Review/03_Independent_Challenge_Restructure_Your_Week5_Catalog.md`. You will preserve the behavior of your own Week 5 catalog rather than replace it with the instructor's notifier.

## 6. How a request moves through the files

The following is the **planned instructor-demo flow**. No database or AI model is required for the deterministic stock check.

```text
User runs: python main.py
          |
          v
main.py  (starts the app and prints the result)
          |
          +----> config.py  (reads LOW_STOCK_THRESHOLD)
          |
          v
stock_alert.py  (checks stock and returns alert text)
          |
          v
main.py  (displays the returned message)

Optional/stretch ONLY:
A future AI integration could call the same stock-alert function.
The core flow does not invoke anthropic_client.py.
```

Why separate these responsibilities? If the alert wording changes, edit the alert logic. If the setting changes, edit your local configuration. If you want a test, call the relevant function directly instead of running the full application.

## 7. Guided practice — find the right file

Use your new `structure_practice` folder. For each task, decide **which file or folder** should change before opening your editor.

1. Change `"Wireless Mouse"` to `"USB-C Cable"` in the demonstration entry point, run it, and check the message.
2. In the reusable logic, change the low-stock message prefix from `LOW STOCK:` to `REORDER:`. Run again. Which file did you edit?
3. Change `stock = 3` to `stock = 8`. Predict what prints with the threshold still equal to 5.
4. Locate `requirements.txt`, `.env.example`, and `tests/`. Explain what each is for.
5. **Optional/stretch:** draw a box around the files that would be needed to add a real SQLite database to a catalog app. No code required.

**Expected result after Step 3** (with the original `make_alert()` stock-OK wording):

```text
Stock OK: USB-C Cable has 8 units.
```

If you completed Step 2, that `REORDER:` change affects only the *low-stock* branch. The stock-OK branch still prints `Stock OK:`. This is a useful reminder to test multiple outcomes.

## 8. Common mistakes and troubleshooting

| Mistake or symptom | Why it happens | What to do |
|---|---|---|
| `ModuleNotFoundError` when running `main.py` | Files are in different locations or named incorrectly | Confirm both `.py` files are in `structure_practice` |
| `.env.example` changes have no effect | Template values are not loaded automatically | This lesson does not read `.env` yet; the next lesson introduces `config.py` |
| Trying to run `requirements.txt` | It is a dependency list, not a Python program | Run `python main.py`; later use `python -m pip install -r requirements.txt` |
| Adding `sqlite3` to requirements | Confusing built-in modules with third-party packages | Only list packages actually installed from outside standard Python |
| Copying `.venv/` to a teammate | An environment contains local paths and installed binaries | Share requirements and let each person create their own `.venv` |
| Treating `anthropic_client.py` as required | Confusing the optional AI preview with the core assignment | Ignore the wrapper until the optional/stretch material; no live call is needed |

## 9. Knowledge check

1. Which file is the **entry point**, and which contains the **reusable stock logic**?
2. Why is `.env.example` safe to share only when its values are examples or placeholders?
3. Do you install `sqlite3` with `pip` for standard Python?
4. Why does adding a `.env.example` file alone not change `main.py`?
5. Where will the 2–3 required automated tests eventually live?

**Self-check answers:** (1) `main.py`; `stock_alert.py`. (2) It should not expose real private values. (3) No; it is part of the standard library. (4) Code must explicitly read configuration and use it. (5) In `tests/`.

## Lesson recap

- A clear project structure is a map for both learners and teammates.
- Separate the **entry point**, **logic**, **configuration**, **dependencies**, and **tests** by responsibility.
- Share source files and safe templates, not your `.venv` or local `.env`.
- The instructor demo remains a separate low-stock notifier; your Week 5 product catalog is preserved for the independent challenge.
- Anthropic integration is **optional/stretch**, never required for Week 6 completion.

**Next lesson:** `03_Separating_Logic_Config_Database_and_Tests.md` explains the boundaries between these responsibilities and how they help make tests dependable.
