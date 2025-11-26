# run_gui.py (在專案根目錄)
import sys
# 將專案根目錄加入路徑，確保能找到 tdd_version 和 ui
sys.path.append('.') 

# 從 TDD 隊友的程式碼中匯入 Cart 類別
# 我們假設 TDD 隊友在 tdd_version/src/cart.py 裡定義了 ShoppingCart
from tdd_version.src.cart import ShoppingCart 

# 從你的 UI 模組中匯入 MainWindow 類別
from ui.main_window import MainWindow 

def main():
    # 1. 實例化邏輯核心 (用 TDD 版本測試)
    cart = ShoppingCart()
    
    # 2. 實例化 UI
    app = MainWindow(cart)
    
    # 3. 啟動 Pygame 主迴圈
    app.run()

if __name__ == "__main__":
    main()