#!/usr/bin/env python3
"""Turnkey one-click entrypoint for the PNN perineuronal net drug discovery project."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure local 'pnn' package is importable when executed directly
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pnn.runner import main

if __name__ == "__main__":
    raise SystemExit(main())
