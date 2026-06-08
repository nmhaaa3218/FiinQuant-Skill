#!/usr/bin/env python3
"""
FiinQuant Skill Self-Installer

Usage:
    Agent can self-install by fetching this script:
    curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/install_fiinquant.py | python3

    Or run directly:
    python install_fiinquant.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

SKILL_NAME = "fiinquant"
GITHUB_RAW_URL = os.environ.get("FIINQUANT_INSTALL_URL", "")


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(step_num, text):
    print(f"\n[{step_num}] {text}")


def ask_choice(options, prompt="Choose an option"):
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            choice = int(input(f"\n{prompt} (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return choice
        except ValueError:
            pass
        print("Please enter a valid number.")


def ask_yes_no(prompt, default=None):
    suffixes = []
    if default is True:
        suffixes = ["Y/n"]
    elif default is False:
        suffixes = ["y/N"]
    else:
        suffixes = ["y/n"]

    suffix = " ".join(suffixes)
    while True:
        response = input(f"{prompt} ({suffix}): ").strip().lower()
        if not response and default is not None:
            return default
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def get_default_skill_dir():
    home = Path.home()
    return home / ".skills" / SKILL_NAME


def get_skill_install_dir():
    default_dir = get_default_skill_dir()

    print(f"\nDefault skill install location:")
    print(f"  {default_dir}")

    use_default = ask_yes_no("Use this location", default=True)

    if use_default:
        return default_dir

    custom = input("\nEnter custom path: ").strip()
    return Path(custom) if custom else default_dir


def download_skill_files(install_dir):
    """Download skill files from GitHub if GITHUB_RAW_URL is set."""
    if not GITHUB_RAW_URL:
        return False

    base_url = GITHUB_RAW_URL.replace("/install_fiinquant.py", "")

    files_to_download = [
        ("SKILL.md", f"{base_url}/SKILL.md"),
        ("FIRST_INSTALL.md", f"{base_url}/FIRST_INSTALL.md"),
        ("scripts/fiinquant_search.py", f"{base_url}/scripts/fiinquant_search.py"),
        ("scripts/first_install.py", f"{base_url}/scripts/first_install.py"),
    ]

    print(f"\n  Downloading skill files...")

    for dest_path, url in files_to_download:
        full_dest = install_dir / dest_path
        full_dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=30) as response:
                content = response.read().decode("utf-8")

            with open(full_dest, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK] {dest_path}")
        except URLError as e:
            print(f"  [!] Failed to download {dest_path}: {e}")

    return True


def install_library():
    print_header("Install FiinQuantX Library")

    options = ["Global (system-wide)", "Virtual Environment (.venv)"]
    choice = ask_choice(options, "Install library where")

    if choice == 1:
        print("  Installing FiinQuantX globally...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install",
            "--extra-index-url", "https://fiinquant.github.io/fiinquantx/simple",
            "fiinquantx"
        ], capture_output=False)

        if result.returncode != 0:
            print("  [!] Installation failed")
            return False
        print("  [OK] FiinQuantX installed globally")
    else:
        venv_dir = Path(".venv")
        print(f"  Creating virtual environment at {venv_dir}...")

        if venv_dir.exists():
            shutil.rmtree(venv_dir)

        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

        pip_exe = venv_dir / ("Scripts/pip.exe" if sys.platform == "win32" else "bin/pip")
        print("  Installing FiinQuantX in .venv...")
        subprocess.run([
            str(pip_exe), "install",
            "--extra-index-url", "https://fiinquant.github.io/fiinquantx/simple",
            "fiinquantx"
        ], check=True)
        print(f"  [OK] FiinQuantX installed in .venv")

    check_signalrcore()
    return True


def check_signalrcore():
    print("  Checking signalrcore...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "signalrcore"],
        capture_output=True, text=True
    )

    if "1.0.0" in result.stdout or ("Version:" in result.stdout and "1." in result.stdout.split("Version:")[-1].split("\n")[0] if "Version:" in result.stdout else False):
        print("  [!] signalrcore >= 1.0.0 detected. Uninstalling...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "signalrcore", "-y"])
        print("  Installing signalrcore 0.9.x...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "signalrcore>=0.9,<1.0"
        ])
        print("  [OK] signalrcore installed compatible version")
    else:
        print("  [OK] signalrcore version compatible")


def setup_credentials(install_dir):
    print_header("Configure Credentials")

    has_account = ask_yes_no("Do you have a FiinQuant account")

    if not has_account:
        print("\n  Please register at: https://fiinquant.vn")
        print("  Run this script again after registration.")
        return False

    save_env = ask_yes_no("Save username/password to .env file")

    if save_env:
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        env_file = install_dir / ".env"
        with open(env_file, "w") as f:
            f.write(f"FIIN_USERNAME={username}\n")
            f.write(f"FIIN_PASSWORD={password}\n")

        print(f"  [OK] Saved to {env_file}")
    else:
        print("  You will need to enter username/password in code when using.")

    return True


def detect_agent_harness():
    """Detect which agent harness is being used based on config files."""
    checks = [
        (Path.home() / ".config" / "opencode" / "opencode.json", "opencode"),
        (Path.home() / ".config" / "opencode" / "opencode.jsonc", "opencode"),
        (Path.home() / ".codex" / "config.toml", "codex"),
        (Path.home() / ".cursor" / "settings.json", "cursor"),
        (Path.home() / ".config" / "claude", "claude"),
        (Path.home() / ".claude" / "settings.json", "claude"),
        (Path.home() / ".config" / "antigravity", "antigravity"),
    ]

    for path, harness in checks:
        if path.exists():
            return harness
    return None


def register_skill(install_dir):
    print_header("Register Skill with Agent")

    harness = detect_agent_harness()

    if harness:
        print(f"\n  Detected agent harness: {harness}")
    else:
        print("\n  Could not auto-detect agent harness.")

    print(f"\n  Skill installed at: {install_dir}")

    skill_config = {
        "name": SKILL_NAME,
        "location": str(install_dir)
    }

    print(f"\n  To register skill, add to your agent config:")
    print(f"\n  {skill_config}")

    print("\n  Config examples by agent:")
    print("  - OpenCode: ~/.config/opencode/opencode.json [skills][]")
    print("  - Codex: ~/.codex/config.toml [plugins][]")
    print("  - Cursor: ~/.cursor/settings.json")
    print("  - Claude Code: ~/.claude/settings.json")
    print("  - Antigravity: ~/.config/antigravity/config.json")

    return True


def main():
    print_header("FiinQuant Skill Installer")
    print("  Automated installation for FiinQuant skill\n")

    if GITHUB_RAW_URL:
        print(f"  Source: {GITHUB_RAW_URL}\n")

    install_dir = get_skill_install_dir()

    if GITHUB_RAW_URL:
        print(f"\n  Downloading skill to {install_dir}...")
        install_dir.mkdir(parents=True, exist_ok=True)
        download_skill_files(install_dir)
    else:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n  Created skill directory: {install_dir}")

        src_dir = Path(__file__).parent
        for item in src_dir.rglob("*"):
            if item.is_file() and item.name != "install_fiinquant.py":
                rel_path = item.relative_to(src_dir)
                dest_path = install_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                print(f"  [OK] {rel_path}")

    print_step(1, "Install FiinQuantX Library")
    install_library()

    print_step(2, "Configure Credentials")
    if not setup_credentials(install_dir):
        print("\n  Skipping credentials step.")

    print_step(3, "Register Skill with Agent")
    register_skill(install_dir)

    print_header("Installation Complete!")
    print(f"""
  Skill installed at: {install_dir}

  Structure:
    {install_dir}/
    ├── SKILL.md
    ├── FIRST_INSTALL.md
    ├── .env (credentials)
    └── scripts/
        ├── fiinquant_search.py
        └── first_install.py

  Next steps:
    1. Restart agent to use skill
    2. See FIRST_INSTALL.md for details
  """)


if __name__ == "__main__":
    main()