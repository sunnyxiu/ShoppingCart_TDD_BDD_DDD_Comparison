"""Launch the shared pygame UI with the TDD cart implementation."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root and tdd-version/src are importable
PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent
SRC_DIR = PROJECT_DIR / "src"

for path in (REPO_ROOT, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from shared.ui.main_window import MainWindow  # noqa: E402  (import after sys.path tweak)
from cart import Cart  # noqa: E402


def main() -> None:
    cart = Cart()
    window = MainWindow(cart)
    window.run()


if __name__ == "__main__":
    main()
