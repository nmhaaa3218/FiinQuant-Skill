#!/usr/bin/env python3
"""
FiinQuant Quickstart & Sanity Check

Verifies:
1. Python dependencies are correctly installed.
2. Credentials in the .env file are loaded and correct.
3. Connection to FiinQuant server works.

Usage:
  python3 quickstart.py
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not installed (though it should be with fiinquantx), we proceed and read direct env
    pass

try:
    from FiinQuantX import FiinSession
except ImportError:
    print("Error: 'fiinquantx' library is not installed.")
    print("Please follow the setup guide in README.md and run:")
    print("  pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx")
    sys.exit(1)

def main():
    username = os.environ.get("FIIN_USERNAME")
    password = os.environ.get("FIIN_PASSWORD")

    # If the user put credentials in a .env file under skills/fiinquant/ instead of root, load that as well
    if not username or not password:
        local_env = Path(__file__).resolve().parent / "skills" / "fiinquant" / ".env"
        if local_env.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(dotenv_path=local_env)
                username = os.environ.get("FIIN_USERNAME")
                password = os.environ.get("FIIN_PASSWORD")
            except Exception:
                pass

    if not username or not password:
        print("Error: Credentials not found!")
        print("Please configure your credentials by creating a `.env` file containing:")
        print("  FIIN_USERNAME=your_username")
        print("  FIIN_PASSWORD=your_password")
        print("\nYou can place this file in the root directory or inside `skills/fiinquant/`.")
        sys.exit(1)

    print(f"Attempting login to FiinQuant with username: {username}...")
    try:
        # Initialize and login
        client = FiinSession(username=username, password=password).login()
        print("Login successful!")
        
        # Test basic data call
        print("Fetching VN30 Tickers to test connection...")
        tickers = client.TickerList(ticker="VN30")
        print(f"\n[SUCCESS] Retrieved VN30 Tickers list:\n{tickers}")
        
    except Exception as e:
        print(f"\n[FAIL] Authentication or data request failed: {e}")
        print("Please check your credentials in the `.env` file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
