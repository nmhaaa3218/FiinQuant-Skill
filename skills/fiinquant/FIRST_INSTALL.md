# FiinQuant Skill Setup & Reference Guide

This guide describes how to configure the FiinQuant skill, manage library dependencies, set up credentials, and register the Model Context Protocol (MCP) server.

---

## ⚡ Option 1: 1-Line Automated Installation (Recommended)

You can automatically install the FiinQuant skill directly using our Node.js/NPM command-line installer. This is the easiest and most reliable method for both humans and AI agents.

Select the command corresponding to your agent harness/environment:

| Tool / Environment | 1-Line Installation Command |
| :--- | :--- |
| **Claude Code** | `npx github:nmhaaa3218/FiinQuant-Skill --claude` |
| **Cursor** | `npx github:nmhaaa3218/FiinQuant-Skill --cursor` |
| **Gemini CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --gemini` |
| **Codex CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --codex` |
| **Antigravity IDE** | `npx github:nmhaaa3218/FiinQuant-Skill --antigravity` |
| **Antigravity CLI (agy)** | `npx github:nmhaaa3218/FiinQuant-Skill --agy` |
| **Kiro CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --kiro` |
| **Kiro IDE** | `npx github:nmhaaa3218/FiinQuant-Skill --path .kiro/skills/fiinquant` |
| **OpenCode** | `npx github:nmhaaa3218/FiinQuant-Skill --opencode` |
| **AdaL CLI** | `npx github:nmhaaa3218/FiinQuant-Skill --adal` |

### Passing Credentials During Installation
To make it even simpler, you can pass your FiinQuant username and password as parameters to the command. This will automatically create the `.env` file in the correct deployed location:
```bash
npx github:nmhaaa3218/FiinQuant-Skill --claude --username YOUR_USERNAME --password YOUR_PASSWORD
```
*(Or specify the credentials via environment variables `FIIN_USERNAME` and `FIIN_PASSWORD` before running the command).*

### What the 1-Line Installer Does:
1. **Installs/Patches dependencies**: Automatically installs `fiinquantx` from the custom index and ensures `signalrcore` is downgraded to a compatible version `< 1.0.0` (handling PEP 668 environment blocks automatically).
2. **Deploys skill files locally**: Copies only the `skills/fiinquant` folder structure to the correct project-local directory (e.g. `./.claude/skills/fiinquant` or `./.agents/skills/fiinquant`), keeping your repository root clean.
3. **Creates local credentials file**: Automatically writes your credentials into a local `.env` inside the deployed directory.
4. **Registers the MCP server**: Safely updates your Cursor `settings.json`, Claude `claude_desktop_config.json`, or local `.agents/config.json` with the absolute path to the deployed script.

---

## 🛠️ Option 2: Step-by-Step Manual Setup (Alternative)

If you prefer to perform the setup manually, please follow these steps carefully to ensure the skill is placed in the project-local folders and not directly in the root of your host repository.

> [!WARNING]
> **Safety Warning for AI Agents:**
> 1. Do NOT copy, modify, or overwrite `.gitignore`, `.gitattributes`, or `.git/` files in the user's host project directory.
> 2. Only copy/deploy the files inside the `skills/fiinquant` folder to the local workspace destination (e.g. `./.agents/skills/fiinquant` or `./.claude/skills/fiinquant`).
> 3. Do not stage or commit any installer config metadata (like `.env`) to the host repository.

### Step 1: Install FiinQuantX Library & Dependencies

You can install the library globally or within a virtual environment.

#### Option A: Global Installation
```bash
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

#### Option B: Virtual Environment (.venv)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

#### Patch signalrcore Version
The `fiinquantx` library depends on `signalrcore`, but version `>= 1.0.0` is incompatible. Run this patch to ensure compatibility:
```bash
pip uninstall signalrcore -y && pip install "signalrcore>=0.9,<1.0"
```
*(Append `--break-system-packages` if installing globally on a system Python environment managed by PEP 668).*

---

### Step 2: Deploy Skill Files Locally

Copy the `skills/fiinquant` folder from this repository to your project's local agent directory (depending on which tool you are using):
- For **Claude Code**: Copy to `./.claude/skills/fiinquant`
- For **Cursor**: Copy to `./.cursor/skills/fiinquant`
- For **Antigravity, Gemini, Codex, OpenCode**: Copy to `./.agents/skills/fiinquant`

---

### Step 3: Configure Credentials

Create a `.env` file **inside the deployed skill folder** (e.g., `./.agents/skills/fiinquant/.env` or `./.claude/skills/fiinquant/.env`) containing your FiinQuant credentials:
```env
FIIN_USERNAME=your_username
FIIN_PASSWORD=your_password
```
*(If you do not have an account, register at [fiinquant.vn](https://fiinquant.vn))*

---

### Step 4: Verify the Setup (Sanity Check)

To verify that the installation succeeded and the credentials are valid, run this Python script:

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

---

### Step 5: Register the Skill as a Native MCP Server

Expose the documentation search tool natively to your agent harness by configuring it as a Model Context Protocol (MCP) server.

Add this block to your agent's MCP settings configuration, pointing to the script in the **deployed location**:

```json
"mcpServers": {
  "fiinquant-docs": {
    "command": "python3",
    "args": [
      "<absolute_path_to_project_root>/.agents/skills/fiinquant/scripts/fiinquant_search.py",
      "--mcp"
    ]
  }
}
```
*(Note: Change `.agents` to `.claude` or `.cursor` in the path above depending on where you deployed the skill files).*

---

## 🤖 Available MCP Tools

When loaded, the agent gains access to the following documentation search tools:

1. **`search_documents`**: Search the live documentation.
   - Args: `query` (string), `limit` (integer, optional)
2. **`get_document_outline`**: Fetch sitemap/documentation outline structure.
   - Args: None
3. **`read_document_page`**: Get the full markdown text of a specific page path.
   - Args: `path` (string)
4. **`get_full_corpus`**: Retrieve the entire documentation text block for comprehensive reasoning.
   - Args: None