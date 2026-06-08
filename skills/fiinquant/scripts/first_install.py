#!/usr/bin/env python3
"""
FiinQuant First-Time Setup Script

Handles:
1. Library installation (global vs venv)
2. Credentials setup (.env)
3. Skill installation (global vs project-based)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
ENV_FILE = SKILL_DIR / ".env"


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(step_num, text):
    print(f"\n[{step_num}] {text}")


def ask_choice(options, prompt="Chọn một tùy chọn"):
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            choice = int(input(f"\n{prompt} (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return choice
        except ValueError:
            pass
        print("Vui lòng nhập số hợp lệ.")


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
        print("Vui lòng nhập 'y' hoặc 'n'.")


def install_library_global():
    print("  Đang cài đặt FiinQuantX globally...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--extra-index-url", "https://fiinquant.github.io/fiinquantx/simple",
        "fiinquantx"
    ], check=True)
    print("  [OK] FiinQuantX đã cài đặt globally")


def install_library_venv():
    venv_dir = SKILL_DIR / ".venv"
    print(f"  Đang tạo virtual environment tại {venv_dir}...")

    if venv_dir.exists():
        shutil.rmtree(venv_dir)

    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    pip_exe = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/pip")
    print("  Đang cài đặt FiinQuantX trong .venv...")
    subprocess.run([
        str(pip_exe), "install",
        "--extra-index-url", "https://fiinquant.github.io/fiinquantx/simple",
        "fiinquantx"
    ], check=True)
    print(f"  [OK] FiinQuantX đã cài đặt trong .venv")
    print(f"\n  Để kích hoạt .venv, chạy:")
    if sys.platform == "win32":
        print(f"    {venv_dir}\\Scripts\\activate")
    else:
        print(f"    source {venv_dir}/bin/activate")


def check_signalrcore():
    print("  Kiểm tra signalrcore...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "signalrcore"],
        capture_output=True, text=True
    )
    if "1.0.0" in result.stdout or "1." in result.stdout:
        print("  [!] signalrcore >= 1.0.0 được phát hiện. Đang gỡ cài đặt...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "signalrcore", "-y"])
        print("  Đang cài đặt signalrcore 0.9.x...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "signalrcore>=0.9,<1.0"
        ])
        print("  [OK] signalrcore đã được cài đặt phiên bản tương thích")
    else:
        print("  [OK] signalrcore version tương thích")


def setup_credentials():
    print_header("Cấu hình thông tin đăng nhập")

    has_account = ask_yes_no("Bạn đã có tài khoản FiinQuant chưa?")

    if not has_account:
        print("\n  Vui lòng đăng ký tại: https://fiinquant.vn")
        print("  Sau khi đăng ký xong, chạy lại script này.")
        return False

    save_env = ask_yes_no("Bạn có muốn lưu username/password vào file .env không?")

    if save_env:
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        with open(ENV_FILE, "w") as f:
            f.write(f"FIIN_USERNAME={username}\n")
            f.write(f"FIIN_PASSWORD={password}\n")

        print(f"  [OK] Đã lưu vào {ENV_FILE}")
    else:
        print("  Bạn sẽ cần nhập username/password trong code khi sử dụng.")

    return True


def install_skill():
    print_header("Cài đặt Skill cho Agent")

    options = [
        "Global Skill - Agent dùng được ở mọi project",
        "Project-based - Skill chỉ dùng trong project hiện tại"
    ]
    choice = ask_choice(options, "Chọn cách cài đặt skill")

    if choice == 1:
        print("\n  [Global Skill] Thêm skill vào cấu hình agent toàn cục...")
        print(f"  Skill path: {SKILL_DIR}")
        print("  Vui lòng thêm vào cấu hình opencode của bạn:")
        print(f"""
  {{
    "skills": [
      {{
        "name": "fiinquant",
        "location": "{SKILL_DIR}"
      }}
    ]
  }}
        """)
    else:
        print("\n  [Project-based] Di chuyển hoặc symlink skill vào project...")
        print(f"  Skill path: {SKILL_DIR}")
        print("  Vui lòng tự thêm vào cấu hình project của bạn.")

    return True


def main():
    print_header("FiinQuant - Cài đặt lần đầu")

    # Step 1: Library installation
    print_step(1, "Cài đặt thư viện FiinQuantX")
    options = ["Global (toàn hệ thống)", "Virtual Environment (.venv)"]
    choice = ask_choice(options, "Cài đặt ở đâu")

    if choice == 1:
        install_library_global()
    else:
        install_library_venv()

    check_signalrcore()

    # Step 2: Credentials
    print_step(2, "Cấu hình đăng nhập")
    if not setup_credentials():
        print("\n  Cài đặt bị hủy. Vui lòng đăng ký tài khoản trước.")
        sys.exit(1)

    # Step 3: Skill installation
    print_step(3, "Cài đặt Skill cho Agent")
    install_skill()

    # Summary
    print_header("Hoàn tất cài đặt!")
    print(f"""
  Cấu trúc skill:
    {SKILL_DIR}/
    ├── SKILL.md
    ├── FIRST_INSTALL.md
    ├── .env (thông tin đăng nhập)
    └── scripts/
        └── fiinquant_search.py

  Tiếp theo:
    1. Xem FIRST_INSTALL.md để biết thêm chi tiết
    2. Chạy 'python scripts/fiinquant_search.py' để test công cụ tìm kiếm
    3. Khởi động lại agent để sử dụng skill
  """)


if __name__ == "__main__":
    main()