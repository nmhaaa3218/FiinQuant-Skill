# FiinQuant Skill Installation Guide

## Agent Self-Install (Automatic)

Agent can self-install by running:

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/install_fiinquant.py | python3
```

## Manual Step-by-Step Installation

### Step 1: Install FiinQuantX Library

**Choose installation location:**

1. **Global (system-wide)** - Shared across all projects
```bash
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

2. **Virtual Environment (.venv)** - Installed in `.venv` folder
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

**Check signalrcore:**
```bash
pip show signalrcore
```
If >= 1.0.0, uninstall and reinstall:
```bash
pip uninstall signalrcore
pip install signalrcore==0.9.x
```

---

### Step 2: Configure Credentials

**Do you have a FiinQuant account?**

- **Yes** → Want to save credentials to `.env`?
  ```env
  # Save at ~/.skills/fiinquant/.env
  FIIN_USERNAME=your_username
  FIIN_PASSWORD=your_password
  ```

- **No** → Register at [fiinquant.vn](https://fiinquant.vn)

---

### Step 3: Register Skill with Agent

Add skill to your agent harness config. Skill location: `~/.skills/fiinquant`

**Config examples by agent:**

| Agent | Config Location |
|-------|-----------------|
| OpenCode | `~/.config/opencode/opencode.json` |
| Codex | `~/.codex/config.toml` |
| Cursor | `~/.cursor/settings.json` |
| Claude Code | `~/.claude/settings.json` |
| Antigravity | `~/.config/antigravity/config.json` |

---

## Skill Structure

```
~/.skills/fiinquant/
├── SKILL.md              # Skill definition
├── FIRST_INSTALL.md      # This guide
├── install_fiinquant.py  # Self-install script
├── .env                  # Credentials (if saved)
└── scripts/
    ├── fiinquant_search.py   # Documentation search tool
    └── first_install.py      # Interactive installer
```

---

## Verify Installation

```python
from FiinQuantX import FiinSession

client = FiinSession(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
).login()

print("Login successful!")
```

---

## Using Documentation Search Tool

```bash
python scripts/fiinquant_search.py "WebSocket realtime"
```

```python
from scripts.fiinquant_search import search_documents, get_document_outline

results = search_documents("WebSocket realtime", limit=5)
outline = get_document_outline()
```