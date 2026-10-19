# Setting Up Python with VS Code
## eCOMMart AI Squad | Week 3

> This guide covers everything you need to start writing and running Python in **Visual Studio Code (VS Code)** — the editor we use throughout this course.

---

## What You Will Install

1. **Python** — the programming language interpreter
2. **Visual Studio Code** — the code editor
3. **Python Extension for VS Code** — makes VS Code Python-aware

---

## Step 1: Install Python

### Windows

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click **Download Python 3.x.x** (latest version)
3. Run the installer
4. **Important:** On the first screen, check **"Add Python to PATH"** before clicking Install

   > If you miss this, Python won't work from the terminal.

5. Click **Install Now** and then **Close**

**Verify — open Command Prompt (`Win + R` → type `cmd`) and run:**

```
python --version
```
# Output:

```
# Output:
Python 3.12.0
```
# Output:

### macOS

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the **macOS installer** and run the `.pkg` file

**Verify — open Terminal and run:**

```
python3 --version
```
# Output:

```
# Output:
Python 3.12.0
```
# Output:

> On macOS, always use `python3` instead of `python`.

### Linux (Ubuntu / Debian)

Open Terminal and run:

```
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```
# Output:

---

## Step 2: Install Visual Studio Code

1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Click **Download** for your operating system
3. Run the installer with default settings
4. Launch VS Code once installation completes

---

## Step 3: Install the Python Extension in VS Code

1. Open VS Code
2. Press `Ctrl + Shift + X` (Windows/Linux) or `Cmd + Shift + X` (macOS)
3. Search for **Python**
4. Click **Install** on the extension published by **Microsoft**

Once installed, VS Code detects your Python interpreter automatically.

---

## Step 4: Create Your First Python File

1. Press `Ctrl + Shift + E` to open the Explorer panel
2. Click **Open Folder** — choose or create a folder, e.g. `eCOMMart_Python`
3. Click the **New File** icon in the Explorer panel
4. Name it `hello.py`
5. Type:

```python
print("Hello, eCOMMart!")
```

---

## Step 5: Run Python in VS Code

### Via the Integrated Terminal (Recommended)

1. Press **Ctrl + `** (backtick) to open the terminal inside VS Code
2. Run your file:

**Windows:**
```
# Output:
python hello.py
```

**macOS / Linux:**
```
# Output:
python3 hello.py
```

```
# Output:
Hello, eCOMMart!
```
# Output:

### Via the Play Button

Click the **▶ Run** button at the top-right of the editor. Output appears in the terminal panel at the bottom.

---

## Step 6: VS Code Layout

```
┌──────────────────────────────────────────────────────┐
│  Explorer         │   Editor (hello.py)               │
│                   │                                   │
│  📁 eCOMMart_Python   print("Hello, eCOMMart!")       │
│    └─ hello.py ───┤                                   │
├───────────────────┴───────────────────────────────────┤
│  TERMINAL                                             │
│  > python hello.py                                    │
│  Hello, eCOMMart!                                     │
└───────────────────────────────────────────────────────┘
```
# Output:

| Panel | Shortcut | Purpose |
|---|---|---|
| Explorer | `Ctrl + Shift + E` | Browse files |
| Terminal | `Ctrl + `` ` `` ` | Run Python files |
| Extensions | `Ctrl + Shift + X` | Install add-ons |
| Command Palette | `Ctrl + Shift + P` | Any VS Code command |

---

## Step 7: Select Your Python Interpreter

If VS Code shows an interpreter warning:

1. Press `Ctrl + Shift + P`
2. Type **Python: Select Interpreter**
3. Choose your installed Python version (e.g., `Python 3.12.0`)

The selected interpreter shows in the bottom-left status bar.

---

## How We Work in This Course

Every file has code blocks and output blocks — like this:

```python
# ecommart_demo.py
product = "Wireless Mouse"
price   = 499.00
print(f"Product: {product} | Price: Rs.{price:.2f}")
```

```
# Output:
Product: Wireless Mouse | Price: Rs.499.00
```
# Output:

**Your workflow every session:**
1. Create a `.py` file in your `eCOMMart_Python` folder
2. Type or copy the code into it
3. Open terminal with `Ctrl + ``
4. Run: `python filename.py`
5. Read the output

---

## Common Issues and Fixes

| Problem | Fix |
|---|---|
| `python is not recognized` (Windows) | Re-install Python with **Add to PATH** checked |

| `command not found: python` (Mac/Linux) | Use `python3` |
| No syntax highlighting in VS Code | Install the Microsoft Python Extension |
| Interpreter warning | `Ctrl+Shift+P` → Python: Select Interpreter |
| `No such file or directory` | Terminal is in wrong folder — use `cd eCOMMart_Python` first |

---

## Terminal Quick Reference

| Task | Windows | macOS / Linux |
|---|---|---|
| Check Python version | `python --version` | `python3 --version` |
| Run a file | `python filename.py` | `python3 filename.py` |
| Open interactive shell | `python` | `python3` |
| Exit interactive shell | `exit()` | `exit()` |
| Change folder | `cd foldername` | `cd foldername` |
| List files | `dir` | `ls` |

```
