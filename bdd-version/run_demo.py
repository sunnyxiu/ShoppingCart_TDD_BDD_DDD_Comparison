"""Launch the shared pygame UI with the BDD cart implementation."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is importable (for shared modules)
# PROJECT_DIR = bdd-version
PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent

# Add REPO_ROOT to sys.path to allow 'from shared...' imports
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Add PROJECT_DIR to sys.path to allow 'from src...' imports
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from shared.ui.main_window import MainWindow  # noqa: E402
from src.cart import Cart  # noqa: E402


def main() -> None:
    print("=== BDD Version Shopping Cart ===")
    cart = Cart()
    window = MainWindow(cart)
    window.run()


if __name__ == "__main__":
    main()
