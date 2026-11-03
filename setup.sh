#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "Not inside a git repository." >&2; exit 1; }
cd "$ROOT"

[ -f requirements.txt ] || { echo "requirements.txt not found in $ROOT" >&2; exit 1; }

# Python: python3, python, or py (Windows launcher). Skip Windows Store stubs.
PY=""
for cand in python3 python py; do
    if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
        PY="$cand"
        break
    fi
done
if [ -z "$PY" ]; then
    echo "Python 3.8+ not found." >&2
    case "$(uname -s)" in
        Darwin) echo "Install: brew install python" >&2 ;;
        Linux)  echo "Install: sudo apt install python3 python3-venv python3-pip (or your distro's equivalent)" >&2 ;;
        *)      echo "Install from https://www.python.org/downloads/ (tick 'Add to PATH')" >&2 ;;
    esac
    exit 1
fi

# pip
if ! "$PY" -m pip --version >/dev/null 2>&1; then
    echo "pip not found for $PY. Try: $PY -m ensurepip --upgrade (Debian/Ubuntu: sudo apt install python3-pip)" >&2
    exit 1
fi

# ipykernel (system check; installed in the venv below if missing)
HAS_IPYKERNEL=1
"$PY" -c "import ipykernel" >/dev/null 2>&1 || HAS_IPYKERNEL=0

# venv
if [ ! -d .venv ]; then
    "$PY" -m venv .venv || {
        echo "venv creation failed. Debian/Ubuntu: sudo apt install python3-venv" >&2
        exit 1
    }
fi

# Venv python path differs on Windows (Scripts/) vs Unix (bin/)
if [ -x .venv/bin/python ]; then
    VPY=".venv/bin/python"
    ACTIVATE="source .venv/bin/activate"
elif [ -f .venv/Scripts/python.exe ]; then
    VPY=".venv/Scripts/python.exe"
    ACTIVATE="source .venv/Scripts/activate  (PowerShell: .venv\\Scripts\\Activate.ps1)"
else
    echo "Could not find python inside .venv." >&2
    exit 1
fi

"$VPY" -m pip install --upgrade pip
"$VPY" -m pip install -r requirements.txt

"$VPY" -c "import ipykernel" >/dev/null 2>&1 || "$VPY" -m pip install ipykernel
NAME="$(basename "$ROOT")"
"$VPY" -m ipykernel install --user --name "$NAME" --display-name "Python ($NAME)"

[ "$HAS_IPYKERNEL" -eq 0 ] && echo "Note: ipykernel was missing globally; installed in .venv only."
echo "Done. Activate with: $ACTIVATE"