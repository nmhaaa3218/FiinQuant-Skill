#!/usr/bin/env python3
"""
FiinQuant Skill Self-Installer

Usage:
    Agent co the tu dong cai dat skill nay bang cach fetch installation script tu URL:
    https://raw.githubusercontent.com/USER/repo/refs/heads/main/install_fiinquant.py

    Hoac chay truc tiep:
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


def get_default_skill_dir():
    home = Path.home()
    if sys.platform == "win32":
        return home / "AppData" / "Roaming" / "opencode" / "skills"
    else:
        return home / ".config" / "opencode" / "skills"


def get_skill_install_dir():
    default_dir = get_default_skill_dir() / SKILL_NAME

    print(f"\nMặc định, skill sẽ được cài tại:")
    print(f"  {default_dir}")

    use_default = ask_yes_no("Bạn có muốn dùng đường dẫn này không", default=True)

    if use_default:
        return default_dir

    custom = input("\nNhập đường dẫn tùy chỉnh: ").strip()
    return Path(custom) if custom else default_dir


def fetch_installer_content(url):
    """Fetch installer script content from URL."""
    print(f"  Đang tải từ: {url}")
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8")
    except URLError as e:
        print(f"  [!] Không thể tải: {e}")
        return None


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

    print(f"\n  Đang tải skill files...")

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
            print(f"  [!] Không thể tải {dest_path}: {e}")

    return True


def install_library():
    print_header("Cài đặt thư viện FiinQuantX")

    options = ["Global (toàn hệ thống)", "Virtual Environment (.venv)"]
    choice = ask_choice(options, "Cài thư viện ở đâu")

    if choice == 1:
        print("  Đang cài đặt FiinQuantX globally...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install",
            "--extra-index-url", "https://fiinquant.github.io/fiinquantx/simple",
            "fiinquantx"
        ], capture_output=False)

        if result.returncode != 0:
            print("  [!] Cài đặt thất bại")
            return False
        print("  [OK] FiinQuantX đã cài đặt globally")
    else:
        venv_dir = Path(".venv")
        print(f"  Đang tạo virtual environment tại {venv_dir}...")

        if venv_dir.exists():
            shutil.rmtree(venv_dir)

        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

        pip_exe = venv_dir / ("Scripts/pip.exe" if sys.platform == "win32" else "bin/pip")
        print("  Đang cài đặt FiinQuantX trong .venv...")
        subprocess.run([
            str(pip_exe), "install",
            "--extra-index-url", "https://fiinquant.github.io/fiinquantx/simple",
            "fiinquantx"
        ], check=True)
        print(f"  [OK] FiinQuantX đã cài đặt trong .venv")

    check_signalrcore()
    return True


def check_signalrcore():
    print("  Kiểm tra signalrcore...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "signalrcore"],
        capture_output=True, text=True
    )

    if "1.0.0" in result.stdout or ("Version:" in result.stdout and "1." in result.stdout.split("Version:")[-1].split("\n")[0] if "Version:" in result.stdout else False):
        print("  [!] signalrcore >= 1.0.0 được phát hiện. Đang gỡ cài đặt...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "signalrcore", "-y"])
        print("  Đang cài đặt signalrcore 0.9.x...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "signalrcore>=0.9,<1.0"
        ])
        print("  [OK] signalrcore đã được cài đặt phiên bản tương thích")
    else:
        print("  [OK] signalrcore version tương thích")


def setup_credentials(install_dir):
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

        env_file = install_dir / ".env"
        with open(env_file, "w") as f:
            f.write(f"FIIN_USERNAME={username}\n")
            f.write(f"FIIN_PASSWORD={password}\n")

        print(f"  [OK] Đã lưu vào {env_file}")
    else:
        print("  Bạn sẽ cần nhập username/password trong code khi sử dụng.")

    return True


def register_skill(install_dir):
    print_header("Đăng ký Skill với Agent")

    options = [
        "Global Skill - Agent dùng được ở mọi project",
        "Project-based - Skill chỉ dùng trong project hiện tại"
    ]
    choice = ask_choice(options, "Chọn cách đăng ký skill")

    skill_config = {
        "name": SKILL_NAME,
        "location": str(install_dir)
    }

    if choice == 1:
        config_paths = [
            Path.home() / ".config" / "opencode" / "opencode.json",
            Path.home() / ".config" / "opencode" / "opencode.jsonc",
        ]

        for config_path in config_paths:
            if config_path.exists():
                print(f"\n  Tìm thấy cấu hình tại: {config_path}")
                print(f"  Vui lòng thêm skill vào mảng 'skills' trong cấu hình:")
                print(f"\n  {skill_config}")
                break
        else:
            print(f"\n  Global config không tìm thấy.")
            print(f"  Tạo cấu hình mới tại: {config_paths[0].parent}")
            config_paths[0].parent.mkdir(parents=True, exist_ok=True)
            print(f"  Vui lòng thêm vào cấu hình:")
            print(f"\n  {skill_config}")
    else:
        print("\n  [Project-based] Thêm skill vào cấu hình project của bạn.")
        print(f"  Skill path: {install_dir}")
        print(f"\n  {skill_config}")

    return True


def main():
    print_header("FiinQuant Skill Installer")
    print("  Hướng dẫn cài đặt tự động cho FiinQuant skill\n")

    if GITHUB_RAW_URL:
        print(f"  Nguồn: {GITHUB_RAW_URL}\n")

    install_dir = get_skill_install_dir()

    if GITHUB_RAW_URL:
        print(f"\n  Đang tải skill vào {install_dir}...")
        install_dir.mkdir(parents=True, exist_ok=True)
        download_skill_files(install_dir)
    else:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n  Tạo thư mục skill: {install_dir}")

        src_dir = Path(__file__).parent
        for item in src_dir.rglob("*"):
            if item.is_file() and item.name != "install_fiinquant.py":
                rel_path = item.relative_to(src_dir)
                dest_path = install_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                print(f"  [OK] {rel_path}")

    print_step(1, "Cài đặt thư viện FiinQuantX")
    install_library()

    print_step(2, "Cấu hình đăng nhập")
    if not setup_credentials(install_dir):
        print("\n  Bỏ qua bước credentials.")

    print_step(3, "Đăng ký Skill với Agent")
    register_skill(install_dir)

    print_header("Hoàn tất!")
    print(f"""
  Skill đã được cài tại: {install_dir}

  Cấu trúc:
    {install_dir}/
    ├── SKILL.md
    ├── FIRST_INSTALL.md
    ├── .env (credentials)
    └── scripts/
        ├── fiinquant_search.py
        └── first_install.py

  Tiếp theo:
    1. Khởi động lại agent để sử dụng skill
    2. Xem FIRST_INSTALL.md để biết thêm chi tiết
  """)


if __name__ == "__main__":
    main()