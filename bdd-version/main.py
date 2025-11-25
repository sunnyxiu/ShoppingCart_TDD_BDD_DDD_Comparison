# bdd-version/main.py
import sys
sys.path.append('..')

from src.cart import Cart
from shared.ui.main_window import MainWindow

def main():
    print("=== BDD 版本購物車系統 ===")
    cart = Cart()  # 使用 BDD 方式開發的 Cart
    window = MainWindow(cart)
    window.run()

if __name__ == "__main__":
    main()