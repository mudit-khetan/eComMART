# START HERE — Week 6 eComMART Instructor Demo Examples

**Week 6 · Python Virtual Environments, Packaging, and Testing**

## Welcome: what is in this folder?

This folder is the **reference-code companion** for the Week 6 Instructor Demo. You will learn how a small Python project keeps its dependencies, configuration, business rules, and tests separate.

The example application is **eComMART Low-Stock Notifier**. It checks a few sample products and creates a message when the quantity in stock is **strictly less than** a configured threshold. For example, with threshold `10`, a product with `4` units is low stock, but a product with exactly `10` units is not.

**Do not confuse this with your Week 5 catalog.** This is a small, **new instructor example** without a live database. Your required independent challenge is to restructure **your own existing Week 5 SQLite catalog**, using `07_Practice_and_Review/03_Independent_Challenge_Restructure_Your_Week5_Catalog.md`.

**Core:** local `.venv`, pinned dependencies, one environment variable, simple modules, and 2–3 pytest tests. **Optional/stretch:** inspecting the Anthropic SDK wrapper. There is **no real API key, Anthropic account, signup, payment, or live Claude/API call required anywhere in Week 6 graded or required work**. If a key is shown, use a **nonworking placeholder only**. Never submit a real credential.

## 1. What files will you see?

```text
Examples/
├── 00_START_HERE.md              # this guide
└── ecommart_notify/
    ├── requirements.txt          # required Python dependencies only
    ├── .env.example              # safe template for local configuration
    ├── main.py                   # starts the local notifier
    ├── config.py                 # reads and validates the threshold
    ├── stock_alert.py            # deterministic low-stock rule and messages
    ├── anthropic_client.py       # OPTIONAL/STRETCH ONLY; not run by main.py
    └── tests/
        ├── test_stock_alert.py   # core test examples for stock rules
        └── test_config.py        # core test example for configuration errors
```

**Important:** The Python source files listed above are created in the upcoming `Examples/ecommart_notify/` batches. This guide explains how to use them once the code files are supplied. Do not assume a missing example file already exists: continue with the lesson walkthrough or the next approved code batch.

Your own `.venv/`, `.env`, and Python caches are **generated locally** and are not supplied in the example folder. In a shared Git repository, ignore them using `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.pyc
```

## 2. Before you start

- Python **3.10 or newer**, with `venv` support, is installed.
- You have an editor such as VS Code, and know how to open its terminal.
- You have completed the Week 6 explanations for `venv`, `requirements.txt`, imports, `.env`, and pytest—or follow the instructor as they explain them.
- You can download packages from your permitted Python package index, unless they are cached already. Downloading Python dependencies is **not** an Anthropic/LLM API call.

Check your Python version:

| Operating system | Command |
|---|---|
| Windows | `py --version` |
| macOS/Linux | `python3 --version` |

If the command does not work, check Python installation first. The following commands assume your terminal is open **inside `Examples/ecommart_notify/`**, next to `main.py` and `requirements.txt`.

## 3. Step 1 — Create an isolated virtual environment

| Terminal | Create `.venv` | Activate `.venv` |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS/Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

A virtual environment is a **private Python workspace for one project**, keeping the packages here separate from another project. It is normal for the terminal prompt to show `(.venv)` after activation, but check the actual interpreter:

```bash
python -c "import sys; print(sys.executable)"
```

**Expected:** the printed path is inside `ecommart_notify/.venv`.

If PowerShell refuses to run the activation script, use Command Prompt with its activation command, or call `.venv\Scripts\python.exe` directly (Windows) / `.venv/bin/python` (macOS/Linux) instead of `python`. Do not weaken security settings just to run the lesson.

## 4. Step 2 — Install dependencies

The core example's `requirements.txt` contains these two packages:

```text
python-dotenv==1.2.4
pytest==9.2.0
```

- `python-dotenv` lets the program load settings stored in `.env`.
- `pytest` is used to run automated checks.
- `==` locks a package to the shown version so two developers can reproduce the same basic environment.

With `.venv` selected, run:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
```

**Expected:** installation succeeds and pytest reports version `9.2.0`. Python built-ins like `os` do not belong in `requirements.txt`.

**Optional/stretch:** `anthropic_client.py` is a separate teaching reference. The Anthropic package is **not a core requirement** and does not need to be installed for `main.py`, the exercises, or the tests. Do not add it to the required `requirements.txt` just to complete Week 6.

## 5. Step 3 — Create safe local configuration

Inside `ecommart_notify/`, create `.env` by copying `.env.example`. An example template is:

```dotenv
# Local business setting used by the core notifier
LOW_STOCK_THRESHOLD=10
# OPTIONAL/STRETCH ONLY — fake key, not used for required work
ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE
```

- `.env.example` is a **safe template** you may share.
- `.env` is the **local version** you should not submit or commit.
- `LOW_STOCK_THRESHOLD=10` means an alert is generated when the current quantity is **below** 10.
- The `ANTHROPIC_API_KEY` line is a **nonworking placeholder**, not a valid credential. **Do not replace it with a real key for this week**. No live API call or signup is necessary.

## 6. Step 4 — Run the local notifier

From `Examples/ecommart_notify/`:

```bash
python main.py
```

The instructor demo has a short built-in sample product list. With `LOW_STOCK_THRESHOLD=10`, expect the same **business decisions** shown below:

| Product | Quantity | Result |
|---|---:|---|
| Wireless Barcode Scanner | 4 | Low stock |
| Thermal Label Roll | 120 | OK |
| USB-C Docking Station | 8 | Low stock |
| Shipping Label Printer | 10 | OK — equal is not low |

The precise formatting of messages comes from `stock_alert.py` and is explained in `06_Building_the_eComMART_Mini_Project/03_Refactoring_into_Modules_and_env_Config.md`. The example is **local and deterministic**; it neither contacts Claude nor reads your Week 5 database.

**Try it:** Set `LOW_STOCK_THRESHOLD=5` in `.env`, rerun `python main.py`, and predict which products still trigger alerts. The scanner with 4 units stays low; the docking station with 8 units is now OK. If your edit has no effect, check whether your terminal already sets `LOW_STOCK_THRESHOLD`: shell variables normally take priority over `.env`.

## 7. Step 5 — Run the tests

Open your terminal **inside `Week 6/Examples/ecommart_notify/`** — the directory containing `stock_alert.py`, `config.py`, and `requirements.txt` — not inside `Week 6/`, `Examples/`, or `tests/`. Then run:

```bash
python -m pytest -q
```

**Expected for the complete core example:** **3 passed**. The tests check typical low stock, equality at the threshold, and an invalid configuration setting. `-q` means less verbose output. A passing result indicates that these tested scenarios behave as expected; it does not mean all possible bugs have been ruled out.

Arrange → Act → Assert is the pattern used in the tests:

1. **Arrange:** choose example quantity and threshold.
2. **Act:** call `is_low_stock(...)`.
3. **Assert:** compare the result with what the rule requires.

The three tests run locally and do not make network/API calls or change the Week 5 catalog database.

## 8. Common beginner issues

| Problem | What to check |
|---|---|
| `No module named dotenv` | Is the correct `.venv` active? Did you install `requirements.txt` into it? |
| `No module named pytest` | Run `python -c "import sys; print(sys.executable)"` and check the selected interpreter |
| `can't open file 'main.py'` | Open a terminal inside `Examples/ecommart_notify/`, not the parent `Examples/` folder |
| `No module named stock_alert` | Check that `stock_alert.py` is beside `main.py` and you run from the project root |
| Threshold change seems ignored | A preexisting shell environment variable may override `.env`; try a clean terminal |
| Config error for `banana` | The threshold must be a nonnegative whole number, such as `10` |
| Test fails on equality | Low-stock means `< threshold`, **not** `<= threshold` |
| An Anthropic import fails | It is optional; do not import/run the wrapper for required work |

## 9. Core versus optional/stretch

| Core — complete this week | Optional/stretch — do not require |
|---|---|
| Create and use `.venv` | Install or inspect the Anthropic SDK |
| Install from `requirements.txt` | Examine `anthropic_client.py` as a future integration point |
| Configure `LOW_STOCK_THRESHOLD` in `.env` | Mock external calls or add advanced tests |
| Understand separate `main.py`, `config.py`, and `stock_alert.py` | Connect the stock tool to an LLM in a later week |
| Run 2–3 simple pytest tests | Use a paid model, credentials, or live network calls |

## 10. What to do after the Instructor Demo

**Your required Takeaway Hands-on Exercise:** open `../07_Practice_and_Review/03_Independent_Challenge_Restructure_Your_Week5_Catalog.md` and restructure **your own Week 5 SQLite catalog**. Copy the original first; then add `.venv`, `requirements.txt`, `ECOMMART_DB_PATH` in `.env`, separated modules, and **2–3 pytest tests**. Confirm the original add, view, search, update, delete, and persistence behavior still works. Use `../07_Practice_and_Review/solutions.md` **only after trying the challenge**.

### Completion check

- [ ] I can explain why `.venv` is local and `requirements.txt` is shared.
- [ ] I know how to make `.env` from `.env.example`.
- [ ] I can run `python main.py` locally and predict the low-stock decisions.
- [ ] I can run `python -m pytest -q` and explain a test result.
- [ ] I know the demo is different from my ongoing Week 5 catalog.
- [ ] I understand the Anthropic wrapper is optional and no real key, account, payment, or live call is required.
