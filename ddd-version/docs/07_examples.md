---
title: 07_examples.md

---

# 使用範例

## 範例 1：基本購物流程
```python
from src.cart import Cart
from shared.models.product import Product
from shared.data.products import PRODUCTS
from shared.data.discount_codes import get_discount_code

# 初始化購物車
cart = Cart()

# 取得商品
iphone = PRODUCTS[0]  # iPhone 15, $30000
airpods = PRODUCTS[2]  # AirPods Pro, $7990

# 加入商品
cart.add_item(iphone, 1)   # 加入 1 個 iPhone
cart.add_item(airpods, 2)  # 加入 2 個 AirPods

# 查看購物車
print(f"商品種類數：{cart.get_item_count()}")  # 2
print(f"總數量：{cart.get_total_quantity()}")  # 3
print(f"總金額：${cart.get_total()}")  # $45980

# 套用折扣碼
discount = get_discount_code("SAVE500")  # 滿 5000 折 500
success, msg = cart.apply_discount(discount)
print(msg)  # "折扣已套用"

# 查看最終金額
print(f"折扣金額：${cart.get_discount_amount()}")  # $500
print(f"最終金額：${cart.get_final_amount()}")  # $45480
```

---

## 範例 2：修改購物車
```python
cart = Cart()
iphone = PRODUCTS[0]

# 加入商品
cart.add_item(iphone, 2)

# 更新數量
cart.update_quantity("P001", 5)  # 改為 5 個
print(cart.items[0].quantity)  # 5

# 移除商品
cart.remove_item("P001")
print(len(cart.items))  # 0
```

---

## 範例 3：錯誤處理
```python
cart = Cart()
iphone = Product("P001", "iPhone 15", 30000, 5, "")

# 嘗試加入超過庫存
success = cart.add_item(iphone, 10)
if not success:
    print("錯誤：數量超過庫存")

# 嘗試套用未達門檻的折扣
cart.add_item(iphone, 1)  # $30000
discount = get_discount_code("SAVE500")  # 需滿 $50000
success, msg = cart.apply_discount(discount)
print(msg)  # "未達最低消費金額 50000 元"
```

---

## 範例 4：完整結帳流程

```python
# 初始化購物車
cart = Cart()

# 選擇商品
iphone = PRODUCTS[0]      # iPhone 15, $30000
airpods = PRODUCTS[2]     # AirPods Pro, $7990
watch = PRODUCTS[1]       # Apple Watch, $12900

# 步驟 1：加入商品
cart.add_item(iphone, 1)   # $30000
cart.add_item(airpods, 2)  # $7990 * 2 = $15980
cart.add_item(watch, 1)    # $12900

print("=== Step 1: 加入商品 ===")
print(f"總金額：${cart.get_total()}")           # $58880
print(f"商品總數量：{cart.get_total_quantity()}") # 4

# 步驟 2：修改數量
cart.update_quantity(airpods.product_id, 1)  # 改成 1 個 AirPods

print("\n=== Step 2: 修改數量 ===")
print(f"更新後總金額：${cart.get_total()}")       # $50890

# 步驟 3：套用折扣碼
discount = get_discount_code("SAVE500")  # 滿 5000 折 500
success, msg = cart.apply_discount(discount)

print("\n=== Step 3: 套用折扣碼 ===")
print(msg)                                   # "折扣已套用"
print(f"折扣金額：${cart.get_discount_amount()}")  # $500

# 步驟 4：計算最終金額
print("\n=== Step 4: 結帳金額 ===")
print(f"原始金額：${cart.get_total()}")         # 50890
print(f"折扣後金額：${cart.get_final_amount()}") # 50390

# 步驟 5：移除商品（如果用戶改變主意）
cart.remove_item(iphone.product_id)

print("\n=== Step 5: 移除商品後重新計算 ===")
print(f"新總金額：${cart.get_total()}")             # 20890
print(f"折扣後金額：${cart.get_final_amount()}")     # 20390
```