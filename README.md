# FiinQuant Skill

A financial data skill and documentation search toolset for Vietnamese stock market data (realtime WebSocket, historical data, financial reports, technical indicators). 

This repository is designed to be fully self-installable by AI agents (like Cursor, Claude Code, Hermes, or Antigravity) when you toss them this repository link.

---

## For LLM Agents

Fetch the full guide and follow it step by step:

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/skills/fiinquant/FIRST_INSTALL.md
```

The guide covers: installing the FiinQuantX library from the custom index, downgrading signalrcore to a compatible version (0.9.x), credentials configuration in `.env`, validating the login using `quickstart.py`, and registering the Model Context Protocol (MCP) server. Don't summarize it; read it end to end.

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

Create a `.env` file at the root of the workspace (or inside [skills/fiinquant/](file:///Users/manhhanguyen/Downloads/test/skills/fiinquant/)) containing your FiinQuant credentials:
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

### Step 4: Register the Skill as a Native MCP Server

Expose the documentation search tool as a native capability to your coding assistant by configuring it as a Model Context Protocol (MCP) server. 

Add the following to your agent harness configuration (e.g., Cursor MCP Settings, `claude_desktop_config.json`, or the system settings):

```json
"mcpServers": {
  "fiinquant-docs": {
    "command": "python3",
    "args": [
      "<absolute_path_to_this_repository>/skills/fiinquant/scripts/fiinquant_search.py",
      "--mcp"
    ]
  }
}
```

---

## 🤖 Available MCP Tools

Once loaded as a skill or MCP server, the following tools will be available to the agent:

1. **`search_documents`**: Search the live FiinQuant documentation for functions, APIs, or real-time setup guides.
   - Arguments: `query` (string), `limit` (integer, optional)
2. **`get_document_outline`**: Fetch the complete documentation outline / sitemap.
   - Arguments: None
3. **`read_document_page`**: Extract the full markdown content of a specific documentation page.
   - Arguments: `path` (string)
4. **`get_full_corpus`**: Retrieve the entire documentation corpus in one text file (useful for offline reasoning).
   - Arguments: None