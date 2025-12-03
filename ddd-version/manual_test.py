"""
手動測試腳本
用於快速驗證 Cart 的基本功能
"""

import sys
sys.path.append('..')

from src.cart import Cart
from shared.data.products import PRODUCTS, get_product_by_id
from shared.data.discount_codes import get_discount_code

def test_basic_operations():
    """測試基本操作"""
    print("=" * 50)
    print("測試 1: 基本操作")
    print("=" * 50)
    
    cart = Cart()
    iphone = PRODUCTS[0]  # iPhone 15, $30000
    
    # 測試加入商品
    success = cart.add_item(iphone, 2)
    print(f"✓ 加入 iPhone x2: {success}")
    print(f"  商品種類數: {cart.get_item_count()}")
    print(f"  總數量: {cart.get_total_quantity()}")
    print(f"  總金額: ${cart.get_total()}")
    
    # 測試更新數量
    success = cart.update_quantity("P001", 5)
    print(f"✓ 更新數量為 5: {success}")
    print(f"  總金額: ${cart.get_total()}")
    
    # 測試移除商品
    success = cart.remove_item("P001")
    print(f"✓ 移除商品: {success}")
    print(f"  商品種類數: {cart.get_item_count()}")
    print()

def test_discount():
    """測試折扣功能"""
    print("=" * 50)
    print("測試 2: 折扣功能")
    print("=" * 50)
    
    cart = Cart()
    iphone = PRODUCTS[0]
    cart.add_item(iphone, 2)  # $60000
    
    # 測試套用折扣
    discount = get_discount_code("SAVE500")
    success, msg = cart.apply_discount(discount)
    print(f"✓ 套用 SAVE500: {success}")
    print(f"  訊息: {msg}")
    print(f"  原始金額: ${cart.get_total()}")
    print(f"  折扣金額: ${cart.get_discount_amount()}")
    print(f"  最終金額: ${cart.get_final_amount()}")
    print()

def test_edge_cases():
    """測試邊界情況"""
    print("=" * 50)
    print("測試 3: 邊界情況")
    print("=" * 50)
    
    cart = Cart()
    iphone = get_product_by_id("P001")
    
    # 測試數量為 0
    success = cart.add_item(iphone, 0)
    print(f"✓ 加入數量 0: {success} (應為 False)")
    
    # 測試數量超過 99
    success = cart.add_item(iphone, 100)
    print(f"✓ 加入數量 100: {success} (應為 False)")
    
    # 測試數量超過庫存
    success = cart.add_item(iphone, 999)
    print(f"✓ 加入數量超過庫存: {success} (應為 False)")
    
    # 測試移除不存在的商品
    success = cart.remove_item("P999")
    print(f"✓ 移除不存在商品: {success} (應為 False)")
    print()

def test_accumulation():
    """測試累加邏輯"""
    print("=" * 50)
    print("測試 4: 累加邏輯")
    print("=" * 50)
    
    cart = Cart()
    iphone = PRODUCTS[0]
    
    # 第一次加入
    cart.add_item(iphone, 2)
    print(f"✓ 第一次加入 2 個")
    print(f"  數量: {cart.items[0].quantity}")
    
    # 第二次加入（累加）
    cart.add_item(iphone, 3)
    print(f"✓ 第二次加入 3 個")
    print(f"  數量: {cart.items[0].quantity} (應為 5)")
    
    # 嘗試累加超過 99
    success = cart.add_item(iphone, 95)
    print(f"✓ 嘗試累加至 100: {success} (應為 False)")
    print()

def test_discount_threshold():
    """測試折扣門檻"""
    print("=" * 50)
    print("測試 5: 折扣門檻")
    print("=" * 50)
    
    cart = Cart()
    airpods = PRODUCTS[2]  # AirPods Pro, $7990
    
    cart.add_item(airpods, 1)  # $7990
    print(f"購物車金額: ${cart.get_total()}")
    
    # SAVE500 需滿 $5000
    discount = get_discount_code("SAVE500")
    success, msg = cart.apply_discount(discount)
    print(f"✓ 套用 SAVE500 (需滿 5000): {success}")
    print(f"  訊息: {msg}")
    print()

if __name__ == "__main__":
    test_basic_operations()
    test_discount()
    test_edge_cases()
    test_accumulation()
    test_discount_threshold()
    
    print("=" * 50)
    print("✅ 手動測試完成")
    print("=" * 50)