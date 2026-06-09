# FiinQuant Skill

A financial data skill and documentation search toolset for Vietnamese stock market data (realtime WebSocket, historical data, financial reports, technical indicators). 

This repository is designed to be fully self-installable by AI agents (like Cursor, Claude Code, Hermes, or Antigravity) when you toss them this repository link.

---

## Choose Your Tool

Use the same repository, but install or invoke it in the way your host expects.

| Tool | Install | First Use |
| :--- | :--- | :--- |
| **Claude Code** | `npx github:nmhaaa3218/FiinQuant-Skill --claude` | `>> ask the fiinquant-docs skill for market overview` |
| **Cursor** | `npx github:nmhaaa3218/FiinQuant-Skill --cursor` | `@fiinquant-docs help me fetch historical data` |
| **Gemini CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --gemini` | `Use fiinquant-docs to search docs` |
| **Codex CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --codex` | `Use fiinquant-docs to search docs` |
| **Antigravity IDE** | `npx github:nmhaaa3218/FiinQuant-Skill --antigravity` | `Use @fiinquant-docs to fetch data` |
| **Antigravity CLI (agy)** | `npx github:nmhaaa3218/FiinQuant-Skill --agy` | `/fiinquant-docs get VN30 tickers` |
| **Kiro CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --kiro` | `Use fiinquant-docs to search docs` |
| **Kiro IDE** | `npx github:nmhaaa3218/FiinQuant-Skill --path ~/.kiro/skills` | `Use @fiinquant-docs to search docs` |
| **GitHub Copilot** | *No installer — paste skills or rules manually* | `Ask Copilot to write fiinquantx code` |
| **OpenCode** | `npx github:nmhaaa3218/FiinQuant-Skill --opencode` | `opencode run @fiinquant-docs help me plan` |
| **AdaL CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --adal` | `Use fiinquant-docs to search docs` |
| **Custom path** | `npx github:nmhaaa3218/FiinQuant-Skill --path ./my-skills` | *Depends on your tool* |

---

## For LLM Agents

Fetch the full guide and follow it step by step:

```bash
# LLM Agent: Run this command to fetch the guide, then follow it step-by-step. Read the guide end-to-end; do not summarize it. Always communicate with and guide the user in the language they used to query you. Do NOT copy, modify, or commit .gitignore or .gitattributes in the user's host repository. Only copy/deploy the 'skills/fiinquant' directory.
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/FIRST_INSTALL.md
```

The guide covers: installing the FiinQuantX library from the custom index, downgrading signalrcore to a compatible version (0.9.x), credentials configuration in `.env`, validating the login using a test script, and registering the skill configuration. Don't summarize it; read it end to end.

---

## 🛠️ Step-by-Step Setup (For Humans & AI Agents)

AI assistants should execute these steps using their native system/file tools:

### Step 1: Install the Python Library & Dependencies

Install the `fiinquantx` library from the custom package registry:
```bash
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

#### Important: Downgrade `signalrcore`
The `fiinquantx` package relies on `signalrcore`, but versions `>= 1.0.0` are incompatible. You must downgrade it to `0.9.x`:
```bash
pip uninstall signalrcore -y && pip install "signalrcore>=0.9,<1.0"
```

*Note: If installing on system Python (e.g. macOS Homebrew) and blocked by PEP 668, append `--break-system-packages` to the pip commands or activate a virtual environment (`.venv`) first.*

### Step 2: Configure Credentials

Create a `.env` file at the root of the workspace (or inside [skills/fiinquant/](skills/fiinquant/)) containing your FiinQuant credentials:
```env
FIIN_USERNAME=your_username
FIIN_PASSWORD=your_password
```
*(If you do not have an account, register at [fiinquant.vn](https://fiinquant.vn))*

### Step 3: Verify the Setup (Sanity Check)

To verify that your library installation and credentials work, you (or your agent) can run this Python script:

```python
import os
from dotenv import load_dotenv
from FiinQuantX import FiinSession

# Load credentials from .env
load_dotenv()
username = os.environ.get("FIIN_USERNAME")
password = os.environ.get("FIIN_PASSWORD")

if not username or not password:
    print("Error: FIIN_USERNAME or FIIN_PASSWORD not found in environment/.env file.")
else:
    try:
        client = FiinSession(username=username, password=password).login()
        print("Login successful! VN30 Tickers:")
        print(client.TickerList(ticker="VN30"))
    except Exception as e:
        print(f"Login or request failed: {e}")
```

### Step 4: Register the Skill in your Agent Config

Configure your agent system to load the skill from the deployed location.

For example, update your local config file (e.g., `./.agents/config.json` or `./.agents/opencode.json`) by adding the deployed skill path:

```json
{
  "skills": [
    {
      "name": "fiinquant",
      "location": "<absolute_path_to_project_root>/.agents/skills/fiinquant"
    }
  ]
}
```

---

## 🤖 Available Documentation CLI Commands

Once installed, the agent or user can search the documentation using standalone CLI flags:

1. **Search documents**:
   ```bash
   python3 scripts/fiinquant_search.py "WebSocket realtime"
   ```
2. **Read a specific page**:
   ```bash
   python3 scripts/fiinquant_search.py --read "/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.1.-ham-du-lieu-realtime.md"
   ```
3. **Get sitemap/outline**:
   ```bash
   python3 scripts/fiinquant_search.py --outline
   ```
4. **Get entire documentation corpus**:
   ```bash
   python3 scripts/fiinquant_search.py --corpus
   ```
5. **Show help menu**:
   ```bash
   python3 scripts/fiinquant_search.py --help
   ```