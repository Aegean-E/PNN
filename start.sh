#!/usr/bin/env bash
# ==============================================================================
# PNN Discovery Pipeline - Turnkey One-Click Launcher (Linux / macOS)
# ==============================================================================
set -e

echo "[PNN] Starting PNN Perineuronal Net Drug Discovery Pipeline..."
if command -v python3 &>/dev/null; then
    python3 run.py --no-browser "$@"
else
    python run.py --no-browser "$@"
fi

echo "[PNN] Turnkey execution succeeded! Dashboard generated at studio.html"
