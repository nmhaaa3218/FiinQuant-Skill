# FiinQuant Skill Setup & Reference Guide

This guide describes how to configure the FiinQuant skill, manage library dependencies, set up credentials, and register the documentation search Model Context Protocol (MCP) server.

---

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

#### Check and Fix signalrcore Version
The `fiinquantx` library depends on `signalrcore`, but version `>= 1.0.0` is incompatible. Run this patch to ensure compatibility:
```bash
pip uninstall signalrcore -y && pip install "signalrcore>=0.9,<1.0"
```
*(Append `--break-system-packages` if installing globally on a system Python environment managed by PEP 668).*

---

### Step 2: Configure Credentials

Create a `.env` file at the root of the workspace (or inside [skills/fiinquant/](file:///Users/manhhanguyen/Downloads/test/skills/fiinquant/)) containing your FiinQuant credentials:
```env
FIIN_USERNAME=your_username
FIIN_PASSWORD=your_password
```
*(If you do not have an account, register at [fiinquant.vn](https://fiinquant.vn))*

---

### Step 3: Verify the Setup (Sanity Check)

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

### Step 4: Register the Skill as a Native MCP Server

Expose the documentation search tool natively to your agent harness (like Cursor, Claude Desktop, Claude Code, or Antigravity) by configuring it as a Model Context Protocol (MCP) server.

Add this block to your agent's MCP settings configuration:

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

When loaded, the agent gains access to the following documentation search tools:

1. **`search_documents`**: Search the live documentation.
   - Args: `query` (string), `limit` (integer, optional)
2. **`get_document_outline`**: Fetch sitemap/documentation outline structure.
   - Args: None
3. **`read_document_page`**: Get the full markdown text of a specific page path.
   - Args: `path` (string)
4. **`get_full_corpus`**: Retrieve the entire documentation text block for comprehensive reasoning.
   - Args: None