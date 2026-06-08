#!/bin/bash
# FiinQuant Skill Self-Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/install_fiinquant.md | bash

set -e

SKILL_DIR="$HOME/.skills/fiinquant"
BASE_URL="https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/skills/fiinquant"

echo "=========================================="
echo "  FiinQuant Skill Installer"
echo "=========================================="

# Step 1: Install library
echo ""
echo "[1/4] Installing FiinQuantX library..."
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx 2>/dev/null || pip3 install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx

# Fix signalrcore
pip show signalrcore 2>/dev/null | grep -q "1\." && pip uninstall signalrcore -y 2>/dev/null && pip install "signalrcore>=0.9,<1.0" 2>/dev/null && echo "  [OK] signalrcore fixed" || true

# Step 2: Create directory
echo ""
echo "[2/4] Creating skill directory..."
mkdir -p "$SKILL_DIR/scripts"

# Step 3: Download skill files
echo ""
echo "[3/4] Downloading skill files..."
curl -fsSL "$BASE_URL/SKILL.md" -o "$SKILL_DIR/SKILL.md" && echo "  [OK] SKILL.md"
curl -fsSL "$BASE_URL/FIRST_INSTALL.md" -o "$SKILL_DIR/FIRST_INSTALL.md" && echo "  [OK] FIRST_INSTALL.md"
curl -fsSL "$BASE_URL/scripts/fiinquant_search.py" -o "$SKILL_DIR/scripts/fiinquant_search.py" && echo "  [OK] fiinquant_search.py"
curl -fsSL "$BASE_URL/scripts/first_install.py" -o "$SKILL_DIR/scripts/first_install.py" && echo "  [OK] first_install.py"

# Step 4: Quick start questions
echo ""
echo "[4/4] Quick setup..."
read -p "FiinQuant username: " username
read -s -p "FiinQuant password: " password
echo ""

if [ -n "$username" ] && [ -n "$password" ]; then
    cat > "$SKILL_DIR/.env" << EOF
FIIN_USERNAME=$username
FIIN_PASSWORD=$password
EOF
    echo "  [OK] Credentials saved to $SKILL_DIR/.env"
else
    echo "  [SKIP] No credentials provided"
fi

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "Skill installed at: $SKILL_DIR"
echo ""
echo "To register with your agent, add to config:"
echo '  { "name": "fiinquant", "location": "'"$SKILL_DIR"'" }'
echo ""
echo "Then restart your agent and say: 'I want to use fiinquant'"