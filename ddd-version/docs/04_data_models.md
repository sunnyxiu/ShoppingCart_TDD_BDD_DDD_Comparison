---
title: 04_data_models.md

---

# 資料模型

## Product（商品）
```python
class Product:
    id: str          # 商品編號，如 "P001"
    name: str        # 商品名稱，如 "iPhone 15"
    price: int       # 價格（整數，單位：元）
    stock: int       # 庫存數量
    image_path: str  # 圖片路徑
```

**欄位說明**：
- `id`: 唯一識別碼，不可重複
- `price`: 使用整數避免浮點數誤差
- `stock`: 剩餘庫存，0 表示缺貨

**範例**：
```python
product = Product("P001", "iPhone 15", 30000, 10, "assets/iphone.png")
```

---

## CartItem（購物車項目）
```
class CartItem:
    product: Product   # 購物車中的商品實體
    quantity: int      # 該商品購買數量
```
**欄位說明：**

* `product`：指向一個 Product 實體，包含商品詳細資訊 (ID, 價格, 庫存)
* `quantity`：購買這個商品的數量 (整數)，代表使用者在購物車內的這一筆數量

**範例：**

```
item = CartItem(product, 2)  # 購買 2 個 "iPhone 15"
行為 (methods)（可在 domain 或服務層實作）：

subtotal()：回傳 product.price * quantity

increase_quantity(n)：增加數量（要驗證是否超過上限或庫存）

decrease_quantity(n)：減少數量 (最小值應 ≥ 1)
```

## DiscountCode（折扣碼）
```
class DiscountCode:
    code: str           # 折扣碼字串 (如 "SAVE100", "SALE20")
    discount_type: str  # 折扣類型 "fixed" 或 "percentage"
    value: int          # 折扣值 (若 fixed，為金額；若 percentage，為百分比)
    is_active: bool     # 折扣碼是否啟用
    min_amount: int     # 最低消費門檻 (整數元)，若無門檻可設為 0
```
**欄位說明：**

`code`：折扣碼唯一識別 (不區分大小寫)

`discount_type`：固定金額 ("fixed") 或 百分比 ("percentage")

`value`：如果是 "fixed"，就是扣多少元；如果是 "percentage"，是百分比 (例如 10 表示 10%)

`is_active`：折扣碼是否仍在有效期 / 可用

`min_amount`：要套用折扣碼時購物車總價 (before 折扣) 必須大於或等於這個金額

**範例：**
```
fixed = DiscountCode("SAVE100", "fixed", 100, True, 500)
percent = DiscountCode("SALE20", "percentage", 20, True, 1000)
```
**行為 (methods)**：

* `validate(total_amount: int) -> bool`：驗證購物車總額是否符合作用條件 (is_active, min_amount)
* `calculate_discount(total_amount: int)` -> int：根據 discount_type 計算折扣金額

## Cart（購物車）
```
from typing import List, Optional

class Cart:
    items: List[CartItem]                   # 購物車內所有項目 (每種商品一筆 CartItem)
    applied_discount: Optional[DiscountCode]  # 已套用的折扣碼 (或 None)

```

**欄位說明**：
* `items`：購物車中的所有商品 (CartItem)，每一筆 CartItem 包含 Product + quantity
* `applied_discount`：如果使用者套用了折扣碼，就存折扣碼；否則為 None


**狀態圖**：
```
[Empty Cart] 
   ├─ add_item → [Has Items, No Discount]
   ├─ apply_discount → (invalid, stay same)
   └─ clear → (stay Empty)

[Has Items, No Discount]
   ├─ add_item → (stay, just更多 items)
   ├─ remove_item → (可能變 Empty 或仍有 Items)
   ├─ update_quantity → (just 改數量)
   ├─ apply_discount → [Has Items, Has Discount]
   └─ clear → [Empty Cart]

[Has Items, Has Discount]
   ├─ remove_item → (still with discount? or remove discount if 0 items)
   ├─ update_quantity → (re-validate discount? if total < min_amount → discount失效或移除)
   ├─ apply_discount → (覆蓋舊折扣)
   └─ clear → [Empty Cart]

```