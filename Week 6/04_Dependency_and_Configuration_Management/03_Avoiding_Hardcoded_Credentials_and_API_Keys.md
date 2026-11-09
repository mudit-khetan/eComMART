# Avoiding Hardcoded Credentials and API Keys

## Lesson purpose

In the previous lesson, you moved the eComMART stock threshold into `.env`. A threshold is ordinary configuration; sharing its value usually does not create a security risk. Other settings are different. A password or API key can grant access to services, so copying it into a Python file, screenshot, or shared project can expose that access.

This lesson teaches a safe habit **before** you work with any AI SDKs: keep sensitive values separate from source code, share only safe templates, and check configuration without displaying it. You will practice entirely with a **fake placeholder key**. **No Anthropic signup, real API key, payment, or live API call is needed or permitted for required Week 6 work.**

**Core for Week 6:** understand the risk of hardcoding, keep `.env` private, and demonstrate reading a local setting. **Optional/stretch:** explore the placeholder API-key naming convention and validation code. Anthropic SDK calls and advanced test mocking are not required.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain what credentials and API keys are, in beginner-friendly terms.
- Recognize a hardcoded secret and describe why it is risky.
- Use `.env`, `.env.example`, and `.gitignore` appropriately.
- Read a placeholder key without printing its contents.
- Explain why a `.env` file alone is **not** a security system.
- Identify safe steps to take if a real key is accidentally exposed.
- Connect this practice to the optional Claude configuration discussed later in Week 6.

## 1. eComMART needs settings—but not all settings are equal

Imagine eComMART has two configuration values:

- `LOW_STOCK_THRESHOLD=5`: an ordinary setting that controls when an alert appears.
- `ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE`: a **fake** training example for how an AI integration might be configured in a later week.

The first value is not usually secret. The second **name** represents a category of setting that would be sensitive **if it held a real API key**.

| Word | Plain-language meaning | Example |
|---|---|---|
| Credential | Information used to prove you are allowed to access something | Password or access token |
| API | A way for one software program to request a service from another program | A future AI text service |
| API key | A string used by a service to associate requests with an account or project | A *fake* `ANTHROPIC_API_KEY` value in this lesson |
| Secret | Any value that must not be exposed to unauthorized people | A real password or active API key |
| Hardcoded | Written directly into the program's source code | `password = "real-password"` (illustration only) |

**Important:** a placeholder key is **not a working credential**. Having a `.env` file does not connect you to Claude, Anthropic, or any other provider.

## 2. The risky approach: hardcoding

Consider this **do-not-copy pattern**:

```python
# BAD PATTERN — illustrative fake value, not an active key
api_key = "YOUR_PLACEHOLDER_KEY_HERE"
```

Even with a fake value, this demonstrates the habit we want to avoid: when a real key is inserted into code, it can accidentally travel with that code into a shared ZIP, classroom submission, screenshot, Git commit, or public repository.

Other problems with hardcoding include:

1. Changing a key requires editing code instead of changing configuration.
2. Teammates may share the same credential when they should have independent access.
3. A copied key can remain in version-control history even after the visible line is deleted.

**Safer direction:** Keep the program responsible for *reading* a setting, not *containing* the secret itself.

## 3. Step 1 — Reuse the safe practice project

Continue in `ecommart_venv_practice` from the previous lesson. You should already have:

```text
ecommart_venv_practice/
├── .venv/                    # local Python environment
├── .env                      # local settings; do not share
├── .env.example              # shareable safe template
├── .gitignore
├── requirements.txt
└── show_config.py
```

Your `requirements.txt` from the previous lesson should contain:

```text
pytest==9.2.0
python-dotenv==1.2.4
```

These are the course's verified example versions as of **4 November 2026**. Activate `.venv` and install them if needed:

```bash
python -m pip install -r requirements.txt
```

**No SDK installation is needed for this exercise.** The `anthropic` package will be introduced as **optional/stretch** in `05_Preparing_for_Agentic_AI_Development/02_Managing_the_Anthropic_SDK_and_Agent_Dependencies.md`.

## 4. Step 2 — Add a fake key to the local .env file

Open your **local** `.env` file. Keep the stock threshold and add a second line:

```dotenv
LOW_STOCK_THRESHOLD=5
ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE
```

This is intentionally a **nonfunctional placeholder**. Do not replace it with a real key in Week 6.

Now open `.env.example` and show the *names and safe examples* that another learner would need:

```dotenv
LOW_STOCK_THRESHOLD=5
ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE
```

Since both shown values are non-sensitive examples, it is safe to share **this** `.env.example`. If you ever work with real secrets in a future program, do **not** copy their values to `.env.example`.

**Do not submit `.env`.** Submit or share `.env.example` when an exercise asks for configuration documentation.

## 5. Step 3 — Check that a setting exists without printing it

Create a new file named `check_placeholder_key.py` beside `.env`:

```python
import os
from pathlib import Path

from dotenv import load_dotenv

project_folder = Path(__file__).resolve().parent
load_dotenv(project_folder / ".env")

api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key == "YOUR_PLACEHOLDER_KEY_HERE":
    print("Training placeholder is configured; no API call will be made.")
elif not api_key:
    print("ANTHROPIC_API_KEY is not configured.")
else:
    print("A non-placeholder value was found. Do not use it in this exercise.")
```

Run it in the activated practice environment:

```bash
python check_placeholder_key.py
```

**Expected output:**

```text
Training placeholder is configured; no API call will be made.
```

Notice what this script **does not do**:

- It does not print `api_key`.
- It does not create an Anthropic client.
- It does not send requests or connect to the internet.
- It does not use a real credential.

The comparison with `YOUR_PLACEHOLDER_KEY_HERE` is for **training only**. In a real application, a program would not hardcode an expected secret value for comparison. It would check configuration safely and rely on the service to authenticate a request when appropriate.

### What happens if the entry is missing?

Temporarily delete or comment out the `ANTHROPIC_API_KEY` line from `.env` and run the script again in a new process.

**Expected output:**

```text
ANTHROPIC_API_KEY is not configured.
```

Restore the fake placeholder line afterward.

## 6. Step 4 — Confirm what should and should not be shared

Open `.gitignore` and confirm it includes:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
```

Review your project using this table:

| File | Share with another learner? | Why? |
|---|---|---|
| `show_config.py` and `check_placeholder_key.py` | Yes | Code reads settings but does not contain active secrets |
| `requirements.txt` | Yes | Documents which packages to install |
| `.env.example` | Yes | Uses safe, fake example values |
| `.gitignore` | Yes | Documents files to exclude from new Git tracking |
| `.env` | **No** | Local configuration may contain private values in real projects |
| `.venv/` | **No** | Local installed environment is machine-specific |

A `.gitignore` rule is not a magic shield. It does **not** encrypt `.env`, secure a computer, stop manual uploads, or remove files already tracked by Git. Treat access to files and screenshots carefully, too.

## 7. What to do if a real key is exposed

You will **not** create a real key during Week 6, but it is useful to know the response pattern for later work:

1. **Stop using and distributing the exposed credential.** Do not paste its value into a support ticket, class discussion, or chatbot conversation.
2. **Revoke or rotate it** using the service provider's account controls. Simply deleting it from code does not make the old key safe again.
3. **Notify the appropriate instructor or security contact** if the key belonged to an organization.
4. **Remove the exposed value from shared files and investigate where it appeared**, including repository history, logs, screenshots, and backups according to your organization's process.
5. **Replace it only through an approved secrets-management method** if a real integration is needed in a later, authorized project.

For production systems, teams often use a dedicated secrets manager or hosting-platform secret settings rather than relying on a developer's `.env` file alone. Those systems are **outside the required Week 6 scope**.

## 8. How this relates to the Week 6 and Week 5 applications

### Instructor Demo: new low-stock notifier

The instructor demo's **core** functionality checks product stock and formats an alert. It needs no LLM and no API key. The core tests verify deterministic behavior—given the same stock and threshold, the function returns the same result.

The demo includes an `anthropic_client.py` file as an **optional/stretch wrapper only**. Reading about or configuring a fake `ANTHROPIC_API_KEY` does **not** mean students must invoke that wrapper or make a live API call. We will explicitly keep it out of required tests and grading.

### Independent Challenge: your own Week 5 catalog

Your required Week 6 takeaway is to improve **your own** `05_Product_Catalog_App.py` from Week 5: add `.venv`, a reviewed `requirements.txt`, **one** environment variable (for example, your local database path), separate modules, and **2–3 simple pytest tests**. You do **not** need to add an Anthropic key or AI integration to your catalog.

### Agentic AI connection in one sentence

Later, an AI-powered application may need a key to talk to an LLM service; the good configuration habit is the same even though this week's program makes **no** external AI request.

## 9. Guided practice: find and fix the mistake

**Situation:** A teammate preparing an eComMART example writes:

```python
# Illustrative anti-pattern; value is not a real credential.
ANTHROPIC_API_KEY = "YOUR_PLACEHOLDER_KEY_HERE"
```

Without contacting an AI service, explain:

1. Why would this be dangerous if the value were a *real* key?
2. Which file should hold a **local** placeholder value for the exercise?
3. What should a shareable `.env.example` contain?
4. How can Python read the value using `os.getenv()` after loading `.env`?
5. Why is it better to report “configured” instead of printing the key?

**Expected reasoning:** (1) code gets copied or committed; (2) `.env`; (3) names and fake sample values only; (4) `load_dotenv(...)` followed by `os.getenv("ANTHROPIC_API_KEY")`; (5) output or logs can also leak secrets.

**Success checklist**

- [ ] I can identify a hardcoded secret in source code.
- [ ] My `.env` uses only a clearly fake training placeholder.
- [ ] My `.env.example` contains no real credential.
- [ ] My `.gitignore` excludes `.env` and `.venv/`.
- [ ] I ran `check_placeholder_key.py` without printing a key or making an API call.
- [ ] I understand that Anthropic integration is optional/stretch, not required.

## 10. Common mistakes and fixes

| Mistake | Why it matters | Safer approach |
|---|---|---|
| Printing `os.getenv("ANTHROPIC_API_KEY")` | Output may appear in screenshots or logs | Print whether the placeholder is configured, not its value |
| Putting an active key in `.env.example` | The template is intended to be shared | Use a fake placeholder instead |
| Assuming `.gitignore` protects a file already committed | Git history may still contain it | Rotate an exposed real key; seek help cleaning history |
| Treating `.env` as an encrypted vault | It is an ordinary text file | Use appropriate secret management in real deployments |
| Attempting a live Claude call with the placeholder | A placeholder does not authenticate | **Do not make live API calls in Week 6 required work** |
| Installing the Anthropic SDK for the core low-stock task | It adds needless setup and confuses required scope | Focus on local Python logic, config, and tests |

## 11. Knowledge check

1. What is the difference between a harmless threshold and a real API key?
2. If `.env` contains a real key in a future project, is it safe to email the file to a teammate?
3. Why is deleting a publicly exposed real key from one Python file insufficient?
4. Does the required Week 6 work involve paid API usage?
5. Does adding an Anthropic placeholder turn the low-stock notifier into an AI application?

**Answers:** 1. The threshold changes behavior; a real key can authorize account access; 2. No; 3. It may remain copied or valid elsewhere, so it must be revoked or rotated; 4. No; 5. No—it is still ordinary Python until optional AI integration is deliberately added.

## 12. Recap

**Keep code and configuration separate. Keep private configuration out of shared work.** For Week 6, learn the pattern using a fake placeholder and a local stock threshold. You do not need a real Anthropic account, working key, or external API request.

**Next:** `../05_Preparing_for_Agentic_AI_Development/00_What_Is_an_Agent_Tool.md` builds on your existing modules, configuration, and tests by introducing agent tools—an important step before adding tests to the eComMART project.
