---
title: 03_api_specification.md

---

# Cart API 規格文件

## 版本資訊
- 版本：1.0.0
- 最後更新：2024-11-20

---

## 方法清單

### P0 - 核心方法（必須實作）
1. `add_item()` - 加入商品
2. `remove_item()` - 移除商品
3. `update_quantity()` - 更新數量
4. `get_total()` - 取得總金額
5. `apply_discount()` - 套用折扣
6. `get_final_amount()` - 取得最終金額

### P1 - 建議方法
7. `clear()` - 清空購物車
8. `get_item_count()` - 取得商品種類數

### P2 - 輔助方法
9. `get_total_quantity()` - 取得總數量
10. `find_item()` - 尋找商品
11. `has_item()` - 檢查商品存在
12. `get_discount_amount()` - 取得折扣金額
13. `remove_discount()` - 移除折扣

---

## 詳細規格

### 1. add_item()

#### 基本資訊
- **方法名稱**：`add_item`
- **用途**：將商品加入購物車
- **優先級**：P0（必須實作）

#### 方法簽名
```python
def add_item(self, product: Product, quantity: int) -> bool:
    """
    加入商品到購物車
    
    Args:
        product (Product): 要加入的商品物件
        quantity (int): 購買數量，範圍 1-99
    
    Returns:
        bool: 成功返回 True，失敗返回 False
    
    Raises:
        無（使用回傳值表示成功/失敗）
    """
    pass
```

#### 前置條件（Preconditions）
- `product` 不為 None
- `product` 是有效的 Product 物件
- `quantity` 是整數

#### 後置條件（Postconditions）
**成功時**：
- 商品被加入 `self.items` 清單
- 如果商品已存在，數量累加
- 回傳 `True`

**失敗時**：
- `self.items` 不變
- 回傳 `False`

#### 業務規則
參考 `05_business_rules.md`：
- BR-001: 數量必須在 1-99 之間
- BR-002: 數量不能超過庫存
- BR-003: 累加後的數量仍需符合上述規則

#### 驗證流程
1. 檢查 quantity 是否在 1-99 範圍
├─ 否 → 返回 False
└─ 是 → 繼續
2. 檢查商品是否已在購物車
├─ 是 → 計算累加後的數量，檢查累加後是否 <= 庫存且 <= 99
│         ├─ 否 → 返回 False
│         └─ 是 → 更新數量，返回 True
└─ 否 → 繼續
3. 檢查 quantity 是否 <= 庫存
├─ 否 → 返回 False
└─ 是 → 建立 CartItem，加入清單，返回 True

#### 測試案例

| 案例編號 | 測試情境 | 商品 | 數量 | 庫存 | 購物車狀態 | 預期結果 | 原因 |
|---------|---------|-----|------|-----|----------|---------|------|
| ADD-001 | 正常加入新商品 | iPhone | 2 | 10 | 空 | ✅ True | 合法操作 |
| ADD-002 | 重複加入同商品 | iPhone | 3 | 10 | iPhone x2 | ✅ True | 累加為 5 |
| ADD-003 | 數量為 0 | iPhone | 0 | 10 | 空 | ❌ False | 違反 BR-001 |
| ADD-004 | 數量為負數 | iPhone | -1 | 10 | 空 | ❌ False | 違反 BR-001 |
| ADD-005 | 數量超過 99 | iPhone | 100 | 200 | 空 | ❌ False | 違反 BR-001 |
| ADD-006 | 超過庫存 | iPhone | 15 | 10 | 空 | ❌ False | 違反 BR-002 |
| ADD-007 | 累加後超過庫存 | iPhone | 5 | 10 | iPhone x8 | ❌ False | 違反 BR-002 |
| ADD-008 | 累加後超過 99 | iPhone | 50 | 200 | iPhone x60 | ❌ False | 違反 BR-001 |
| ADD-009 | 邊界值（1） | iPhone | 1 | 10 | 空 | ✅ True | 最小合法值 |
| ADD-010 | 邊界值（99） | iPhone | 99 | 100 | 空 | ✅ True | 最大合法值 |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 加入 2 個 iPhone
success = cart.add_item(product, 2)
print(success)  # True
print(len(cart.items))  # 1
print(cart.items[0].quantity)  # 2
```

**範例 2：重複加入（累加）**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

cart.add_item(product, 2)   # True，數量 2
cart.add_item(product, 3)   # True，累加為 5
print(cart.items[0].quantity)  # 5
```

**範例 3：錯誤處理**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 5, "iphone.png")

# 嘗試加入超過庫存的數量
success = cart.add_item(product, 10)
print(success)  # False
print(len(cart.items))  # 0（購物車未改變）
```

#### 實作提示
```python
def add_item(self, product: Product, quantity: int) -> bool:
    # 步驟 1: 驗證數量範圍
    if quantity < 1 or quantity > 99:
        return False
    
    # 步驟 2: 檢查庫存
    if quantity > product.stock:
        return False
    
    # 步驟 3: 檢查商品是否已存在
    existing_item = self.find_item(product.id)
    
    if existing_item:
        # 步驟 4: 累加數量並驗證
        new_quantity = existing_item.quantity + quantity
        
        # 驗證累加後的數量
        if new_quantity > 99 or new_quantity > product.stock:
            return False
        
        existing_item.quantity = new_quantity
        return True
    
    # 步驟 5: 建立新的 CartItem
    new_item = CartItem(product, quantity)
    self.items.append(new_item)
    return True
```

#### 注意事項
1. **不修改 product 物件**：這個方法不應該改變 product 的庫存
2. **原子性**：如果驗證失敗，購物車狀態不應該改變
3. **冪等性**：相同的操作可以重複執行（累加數量）

---

### 2. remove_item()
#### 基本資訊
- **方法名稱**：`remove_item`
- **用途**：將購物車中的指定商品移除
- **優先級**：P0（必須實作）

#### 方法簽名
```python
def remove_item(self, product_id: str) -> bool:
    """
    從購物車移除指定商品

    Args:
        product_id: 商品 ID

    Returns:
        bool: 成功返回 True，商品不存在返回 False
    """
        pass
```

#### 前置條件（Preconditions）
- `product` 不為 None
- `product` 是有效的 Product 物件
- `quantity` 是整數

#### 後置條件（Postconditions）
**成功時**：
- 商品被移除 `self.items` 清單
- 其他商品保持不變
- 總價與商品數量同步更新
- 回傳 `True`

**失敗時**：
- `self.items` 不變
- 總價與商品數量不變
- 回傳 `False`

#### 驗證流程
1. 檢查商品是否在購物車中
├─ 否 → 返回 False
└─ 是 → 移除，返回 True

#### 測試案例
| 案例編號    | 測試情境      | 商品      | 數量 | 庫存 | 購物車狀態 | 預期結果    | 原因             |
| ------- | --------- | ------- | -- | -- | ----- | ------- | -------------- |
| REM-001 | 成功移除存在的商品 | iPhone  | 2  | 10 | 有iPhone   | ✅ True  | 合法操作  |
| REM-002 | 移除不存在的商品  | AirPods | 1  | 5  | 只有iPhone | ❌ False | 指定商品不在購物車中，無法移除  |
| REM-003 | 從空購物車移除商品 | iPhone  | 1  | 10 | 空     | ❌ False | 購物車為空，無法移除任何商品 |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 加入 2 個 iPhone
cart.add_item(product, 2)

# 移除 iPhone
success = cart.remove_item("P001")
print(success)  # True
print(len(cart.items))  # 0，購物車已空
```

**範例 2：移除不存在的商品**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 購物車有其他商品，但不是 AirPods
cart.add_item(product, 2)

# 嘗試移除 AirPods（不存在）
success = cart.remove_item("P002")
print(success)  # False
print(len(cart.items))  # 1，購物車保持不變

```
**範例 3：從空購物車移除商品**
```python
cart = Cart()

# 嘗試移除 iPhone（購物車為空）
success = cart.remove_item("P001")
print(success)  # False
print(len(cart.items))  # 0，購物車仍然為空

```
#### 實作提示
```python
def remove_item(self, product: Product) -> bool:
    cart_item = self.find_item(product.id)
    # 步驟 1: 驗證購物車是否存在指定商品
    if cart_item:
        self.item.remove(cart_item)
        return True
    else:
        return False    
```
#### 注意事項
1. 不修改 `product` 物件：移除商品只改變購物車 `self.items`，不影響原本 `Product.stock` 或其他屬性。
2. 原子性：如果商品不存在於購物車中，購物車狀態不應改變，方法應直接回傳 False。
3. 冪等性：同一商品多次呼叫 `remove_item`，結果相同：
第一次移除成功 → 返回 True
後續移除 → 返回 False，購物車保持不變
4. 只移除對應商品：僅移除指定 `product.id` 的 CartItem，不影響其他商品。

---

### 3. update_quantity()
#### 基本資訊
- **方法名稱**：`update_quantity`
- **用途**：修改購物車中商品的數量
- **優先級**：P0（必須實作）

#### 方法簽名
```python
def update_quantity(self, product_id: str, quantity: int) -> bool:
    """
    更新購物車中商品的數量

    Args:
        product_id: 商品 ID
        quantity: 新的數量（1-99）

    Returns:
        bool: 成功返回 True，失敗返回 False

    驗證規則：
        - quantity 必須 >= 1 且 <= 99
        - quantity 不能超過庫存
        - 商品必須已存在於購物車
    """
    pass
```

#### 前置條件（Preconditions）
- `product` 不為 None
- `product` 是有效的 Product 物件
- `quantity` 是整數

#### 後置條件（Postconditions）
**成功時**：
- 商品數量更新
- 回傳 `True`

**失敗時**：
- `self.items` 不變
- 回傳 `False`

#### 業務規則
參考 `05_business_rules.md`：
- BR-001: 數量必須在 1-99 之間
- BR-002: 數量不能超過庫存
- BR-003: 更新後的數量仍需符合上述規則
#### 驗證流程
1. 檢查商品是否已在購物車
├─ 否 → 返回 False
└─ 是 → 繼續
2. quantity 必須 >= 1 且 <= 99
├─ 是 → 繼續
└─ 否 → 返回 False
3. 檢查 quantity 是否 <= 庫存
├─ 否 → 返回 False
└─ 是 → 更新清單數量，返回 True

#### 測試案例

| 案例編號    | 測試情境      | 商品      | 數量  | 庫存  | 購物車狀態        | 預期結果    | 原因              |
| ------- | --------- | ------- | --- | --- | ------------ | ------- | --------------- |
| UPD-001 | 成功更新數量    | iPhone  | 5   | 10  | 已有 iPhone x2 | ✅ True  | 合法操作 |
| UPD-002 | 更新不存在的商品  | AirPods | 3   | 5   | 已有 iPhone x2 | ❌ False | 商品不在購物車中，無法更新   |
| UPD-003 | 更新數量為 0   | iPhone  | 0   | 10  | 已有 iPhone x2 | ❌ False | 不合法的數量，低於最小限制 1 |
| UPD-004 | 更新數量為負數   | iPhone  | -3  | 10  | 已有 iPhone x2 | ❌ False | 不合法的數量，低於最小限制 1 |
| UPD-005 | 更新數量超過庫存  | iPhone  | 15  | 10  | 已有 iPhone x2 | ❌ False | 不合法的數量，超過庫存     |
| UPD-006 | 更新數量超過 99 | iPhone  | 100 | 150 | 已有 iPhone x2 | ❌ False | 不合法的數量，超過上限 99  |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 加入 2 個 iPhone
cart.add_item(product, 2)

# 更新數量為 5
success = cart.update_quantity("P001", 5)
print(success)  # True
print(cart.items[0].quantity)  # 5

```
**範例2:更新不存在的商品**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 購物車只有 iPhone
cart.add_item(product, 2)

# 嘗試更新不存在的商品 AirPods
success = cart.update_quantity("P002", 3)
print(success)  # False
```

**範例3: 錯誤處理**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

cart.add_item(product, 2)

# 嘗試更新數量為 0
success = cart.update_quantity("P001", 0)
print(success)  # False
print(cart.items[0].quantity)  # 2，購物車不變
```

#### 實作提示
```python
def update_quantity(self, product_id: str, quantity: int) -> bool:
    # 步驟1: 檢查商品是否已在購物車
    cart_item = self.find_item(product_id)
    if not cart_item:
        return False  # 商品不存在

    # 步驟2: 檢查 quantity >= 1 且 <= 99
    if quantity < 1 or quantity > 99:
        return False  # 不合法數量

    # 步驟3: 檢查 quantity 是否 <= 庫存
    if quantity > cart_item.product.stock:
        return False  # 超過庫存

    # 更新數量
    cart_item.quantity = quantity
    return True
```

#### 注意事項
* 不修改原始 Product 物件
* 原子性：驗證失敗時購物車狀態不改
* 冪等性：相同操作重複執行不影響其他屬性



---
### 4. get_total()
#### 基本資訊
- **方法名稱**：`get_total`
- **用途**：計算購物車原始總金額（未套用折扣）
- **優先級**：P0（必須實作）

#### 方法簽名
```python
def get_total(self) -> int:
    """
    計算購物車原始總金額（未套用折扣）

    Returns:
        int: 總金額

    計算公式：
        sum(item.subtotal for item in items)
    """
    pass
```

#### 前置條件（Preconditions）
* `self.items` 已初始化（通常為空列表或已有購物車項目）
- 每個 `CartItem` 的 `quantity` 與 `product.price` 都是有效數值（整數 ≥ 0）

* 所有 `product` 物件存在且有效

#### 後置條件（Postconditions）
**成功時**：
* 回傳值為購物車中所有商品的總價（整數）
* 不修改購物車內任何商品數量或折扣碼狀態
* 即使購物車為空，回傳 0
* 總價 = `sum(item.product.price * item.quantity for item in self.items)`



#### 業務規則
參考 `05_business_rules.md`：
- BR-201: 小計 = 商品單價 × 數量
- BR-202: 總金額 = Σ(所有項目的小計)


#### 測試案例
| 案例編號   | 測試情境      | 商品               | 數量    | 庫存     | 購物車狀態   | 預期結果        | 原因                    |
| ------ | --------- | ---------------- | ----- | ------ | ------- | ----------- | --------------------- |
| GT-001 | 空購物車（0 元） | 無                | 0     | 0      | 空       | **0 元**     | 無商品時總價應為 0            |
| GT-002 | 單一商品總價計算  | iPhone           | 2     | 10     | 含 1 項商品 | **60000 元** | 30000 × 2 正確計算        |
| GT-003 | 多商品總價計算   | iPhone + AirPods | 2 + 1 | 10 + 5 | 含 2 項商品 | **66000 元** | 30000×2 + 6000×1 合法加總 |

---
### 5. apply_discount()
#### 基本資訊
#### 基本資訊
- **方法名稱**：`apply_discount`
- **用途**：套用折扣碼到購物車
- **優先級**：P0（必須實作）

#### 方法簽名
```python
def apply_discount(self, discount_code: DiscountCode) -> Tuple[bool, str]:
    """
    套用折扣碼

    Args:
        discount_code: 折扣碼物件

    Returns:
        tuple[bool, str]: (是否成功, 訊息)
            成功: (True, "折扣已套用")
            失敗: (False, "錯誤原因")

    驗證規則：
        1. 折扣碼必須是啟用狀態 (is_active == True)
        2. 購物車總金額必須 >= min_amount
        3. 一次只能套用一個折扣碼（新的會覆蓋舊的）

    錯誤訊息：
        - "折扣碼已停用"
        - "未達最低消費金額 {min_amount} 元"
    """
    pass
```

#### 前置條件（Preconditions）
- `discount_code` 必須是 有效的 DiscountCode 物件
- `self.items` 已初始化
- `get_total()` 可被正常呼叫

#### 後置條件（Postconditions）
**成功時**：
- 購物車的折扣碼狀態更新為新的` discount_code`
- 回傳 (True, "折扣已套用")
- 舊的折扣碼（如果有）會被覆蓋

**失敗時**：
- 購物車狀態不變`self.items` 不變
- 回傳 (False, <錯誤訊息>)，例如：
    "折扣碼已停用"
    "未達最低消費金額 {min_amount} 元"
#### 業務規則
參考 `05_business_rules.md`：
- BR-203: 固定金額折扣, 百分比折扣

#### 驗證流程
1. 檢查 discount_code 是否為啟用狀態 (is_active == True)
├─ 否 → 返回 (False, "折扣碼已停用")
└─ 是 → 繼續

2. 檢查 購物車總金額 total 是否 >= discount_code.min_amount
├─ 否 → 返回 (False, f"未達最低消費金額 {discount_code.min_amount} 元")
└─ 是 → 繼續

3. 檢查購物車是否已套用其他折扣碼 (self.applied_discount)
├─ 是 → 覆蓋舊折扣碼
│      └─ 設定 self.applied_discount = discount_code
│         → 返回 (True, "折扣已套用（已覆蓋舊折扣）")
└─ 否 → 設定 self.applied_discount = discount_code
         → 返回 (True, "折扣已套用")


#### 測試案例

| 案例編號 | 測試情境                        | 商品         | 數量 | 庫存 | 購物車狀態            | 預期結果                      | 原因                    |
| ---- | --------------------------- | ---------- | -- | -- | ---------------- | ------------------------- | --------------------- |
| APD-001 | 套用固定金額折扣（type="fixed"）      | A商品（$500）  | 1  | 10 | 金額 $500          | 最終金額 = $500 - $100 = $400 | 固定折扣碼固定扣 $100         |
| APD-002 | 套用百分比折扣（type="percentage"）  | B商品（$800）  | 1  | 5  | 金額 $800          | 最終金額 = $800 × 0.9 = $720  | 百分比折扣 10% off         |
| APD-003 | 未達最低消費門檻                    | C商品（$100）  | 1  | 20 | 金額 $100（門檻 $300） | 拒絕套用折扣碼                   | 金額未達折扣最低門檻            |
| APD-004 | 折扣碼已停用                      | D商品（$400）  | 1  | 3  | 金額 $400          | 拒絕套用折扣碼                   | 折扣碼 status = disabled |
| APD-005 | 覆蓋已存在的折扣碼                   | E商品（$1000） | 1  | 10 | 已套用折扣碼 OLD10     | 新折扣碼成功覆蓋                  | 系統允許更新/覆蓋舊折扣          |
| APD-006 | 折扣碼不分大小寫（SAVE100 = save100） | F商品（$500）  | 1  | 5  | 金額 $500          | 折扣碼可成功套用                  | 系統應做不分大小寫比較           |

# 使用範例
## 範例 1：基本操作流程
```python
cart = Cart()
product = Product("A001", "耳機", 500, 10, "earphone.png")

# 加入 1 個耳機
cart.add_item(product, 1)

# 套用固定折扣 $100
result = cart.apply_coupon("SAVE100")  # type="fixed"

print(result)  # True
print(cart.total_amount())  # 400

```
---
## 範例 2：未達最低消費門檻
```python
cart = Cart()
product = Product("C001", "USB", 100, 20, "usb.png")

cart.add_item(product, 1)

# 嘗試使用需滿 300 才能使用的折扣碼
result = cart.apply_coupon("SAVE50")

print(result)  # False
print(cart.total_amount())  # 100（不變）

```
---
## 範例 3：折扣碼已停用
```python
cart = Cart()
product = Product("D001", "鍵盤", 400, 3, "keyboard.png")

cart.add_item(product, 1)

# 折扣碼目前為 disabled
result = cart.apply_coupon("DISABLED10")

print(result)  # False
print(cart.total_amount())  # 400

```
## 範例4: 覆蓋已存在的折扣碼
```python
cart = Cart()
product = Product("E001", "螢幕", 1000, 10, "monitor.png")

cart.add_item(product, 1)

cart.apply_coupon("OLD10")  # 套用舊折扣
result = cart.apply_coupon("NEW20")  # 新折扣覆蓋舊折扣

print(result)  # True
print(cart.total_amount())  # 應以 NEW20 的折扣為準
```

#### 實作提示
```python
def apply_discount(self, discount_code: DiscountCode) -> Tuple[bool, str]:
    # 步驟 1: 檢查折扣碼是否啟用
    if not discount_code.is_active:
        return False, "折扣碼已停用"
    
    # 步驟 2: 檢查購物車是否有商品（避免總金額為 0）
    if len(self.items) == 0:
        return False, "購物車為空"
    
    # 步驟 3: 檢查是否達到最低消費金額
    total = self.total_amount()
    if total < discount_code.min_amount:
        return False, f"未達最低消費金額 {discount_code.min_amount} 元"
    
    # 步驟 4: 覆蓋現有折扣碼（若有）
    # （不需另外驗證，直接覆蓋即可）
    self.applied_discount = discount_code
    
    # 步驟 5: 套用成功
    return True, "折扣已套用"
```
#### 注意事項
1. 不修改商品或購物車內容物：
    套用折扣碼不應影響 product.stock、商品數量或購物車的項目。
3. 原子性：
如果折扣碼驗證失敗（未達門檻、停用），
5. 不得修改購物車的 applied_discount 狀態。
7. 覆蓋行為需為安全操作：
新折扣碼成功套用時，才允許覆蓋舊折扣碼；
驗證失敗不能覆蓋原有折扣碼。
11. 不得影響未套用折扣的原始金額：
apply_discount() 不應改變購物車的原始總金額，只更新折扣狀態。
14. 大小寫不敏感（若需求有）：
折扣碼比對應在外層統一處理大小寫，以確保 save100 與 SAVE100 視為相同。
18. 不得計算折扣金額（由其他方法負責）：
此方法只負責「驗證並套用折扣碼」，不應計算折扣後價格（例如 get_final_total() 才處理）。
22. 冪等性（Idempotent）：
對同一個折扣碼重複呼叫 apply_discount()，在完全相同條件下應得到相同結果，不會造成重複副作用。
---
### 6. get_final_amount()
#### 基本資訊
- **方法名稱**：`get_final_amount`
- **用途**：計算套用折扣後的最終金額
- **優先級**：P0（必須實作）

#### 方法簽名
```python
    def get_final_amount(self) -> int:
        """
        計算最終金額（套用折扣後）
        
        Returns:
            int: 最終金額（四捨五入到整數，最低為 0）
        
        計算公式：
            - 固定折扣: max(0, total - discount.value)
            - 百分比折扣: max(0, total * (100 - discount.value) / 100)
            - 無折扣: total
        """
    pass
```

#### 前置條件（Preconditions）
- `self.items` 為有效結構
- `self.applied_discount）`若存在，必須是一個有效的 DiscountCode 物件
- `get_total()` 能正確回傳整數金額

#### 後置條件（Postconditions）

- 回傳 整數 金額。
- 若有折扣碼 → 套用折扣後金額必須 ≥ 0（最低為 0）
- 若為百分比折扣 → 結果需為 四捨五入後整數
- `self.items` 不變

#### 業務規則
參考 `05_business_rules.md`：
- BR-203: 折扣計算

#### 測試案例

| 案例編號        | 測試情境           | 商品        | 數量 | 庫存 | 購物車狀態                      | 預期結果        | 原因                           |
| ----------- | -------------- | --------- | -- | -- | -------------------------- | ----------- | ---------------------------- |
| **GFA-001** | 無折扣（總金額正確）     | iPhone 15 | 2  | 10 | 含 2 件 iPhone               | **60000 元** | 無折扣 → 回傳原始金額                 |
| **GFA-002** | 固定金額折扣         | iPhone 15 | 2  | 10 | 含 2 件 iPhone + 折扣碼 1000 元  | **59000 元** | total - 1000，仍 ≥ 0           |
| **GFA-003** | 百分比折扣          | iPhone 15 | 2  | 10 | 含 2 件 iPhone + 10% off     | **54000 元** | 60000 × 0.9 = 54000          |
| **GFA-004** | 折扣超過總金額（結果為 0） | iPhone 15 | 1  | 10 | 含 1 件 iPhone + 折扣碼 50000 元 | **0 元**     | max(0, total - discount)     |
| **GFA-005** | 百分比折扣需四捨五入     | iPhone 15 | 1  | 10 | 含 1 件 iPhone + 33% off     | **20100 元** | 30000 × 0.67 = 20100（正確四捨五入） |
#### 使用範例
**範例 1：套用折扣碼-固定金額**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

cart.add_item(product, 2)  # 總金額：60000

# 套用固定金額折扣 1000 元
discount = DiscountCode("SAVE1000", "fixed", 1000, True, 0)
cart.apply_discount(discount)

final_amount = cart.get_final_amount()
print(final_amount)  # 59000（60000 - 1000）
```
---
**範例 2：套用折扣碼-百分比**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

cart.add_item(product, 2)  # 總金額：60000

# 套用 10% 折扣
discount = DiscountCode("OFF10", "percentage", 10, True, 0)
cart.apply_discount(discount)

final_amount = cart.get_final_amount()
print(final_amount)  # 54000（60000 * 0.9）
```
---
**範例 3：折扣後金額最低為 0**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

cart.add_item(product, 1)  # 總金額：30000

# 套用超過總金額的折扣
discount = DiscountCode("BIGSALE", "fixed", 50000, True, 0)
cart.apply_discount(discount)

final_amount = cart.get_final_amount()
print(final_amount)  # 0（折扣後不可為負數）
```

#### 實作提示
```python
def get_final_amount(self) -> int:
    """
    計算最終金額（套用折扣後）
    """
    
    # 步驟 1: 取得未折扣的總金額
    total = self.get_total()

    # 步驟 2: 若沒有折扣碼 → 直接回傳 total
    if self.discount is None:
        return total

    # 步驟 3: 根據折扣類型計算
    if self.discount.type == "fixed":
        # 固定金額折扣：扣掉 discount.value
        final = total - self.discount.value

    elif self.discount.type == "percentage":
        # 百分比折扣：total * (100 - percent) / 100
        final = total * (100 - self.discount.value) / 100

    else:
        # 未知類型（理論上不會發生）
        return total

    # 步驟 4: 四捨五入並確保不小於 0
    final = round(final)
    final = max(0, final)

    return final
```

#### 注意事項
1. 不修改購物車內容
2. 不修改折扣碼
3. 結果必須為整數
4. 不可拋出例外
不處理驗證錯誤（已在 apply_discount() 保證折扣碼有效）
---
### 7. clear()

#### 基本資訊
- **方法名稱**：`clear`
- **用途**：清空購物車
- **優先級**：P1（建議功能）

#### 方法簽名
```python
def clear(self) -> None:
    """清空購物車（移除所有商品和折扣碼）"""
    pass
```

#### 前置條件（Preconditions）
- 無

#### 後置條件（Postconditions）
**成功時**：
* `self.items` 變為空清單 []
* 所有商品項目被移除
* `self.discount_code`（若存在）會被重置為 None
* 購物車被完全清空
`
#### 測試案例

| 案例編號    | 測試情境      | 商品     | 數量 | 庫存 | 購物車狀態 | 預期結果   | 原因            |
| ------- | --------- | ------ | -- | -- | ----- | ------ | ------------- |
| CLR-001 | 清空有商品的購物車 | iPhone | 2  | 10 | 已加入商品 | ✅ 空購物車 | 所有商品被移除，折扣碼重置 |
| CLR-002 | 清空空購物車    | -      | 0  | 0  | 空     | ✅ 空購物車 | 購物車原本為空，操作仍成功 |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product1 = Product("P001", "iPhone 15", 30000, 10, "iphone.png")
product2 = Product("P002", "AirPods", 8000, 5, "airpods.png")

# 加入商品到購物車
cart.add_item(product1, 2)
cart.add_item(product2, 1)

print(len(cart.items))  # 2（購物車有兩個商品）

# 清空購物車
cart.clear()

print(len(cart.items))  # 0（購物車已清空）
print(cart.applied_discount)  # None（折扣碼已清空）

```

#### 實作提示
```python
def clear(self) -> None:
    # 步驟 1: 移除所有購物車商品
    self.items.clear()
    
    # 步驟 2: 移除已套用的折扣碼
    self.applied_discount = None
    
    # 步驟 3: 購物車已被清空
    # 無回傳值，操作完成即成功
```
#### 注意事項
1. 不修改商品物件：清空購物車不會改變任何 Product 的庫存或屬性，只影響購物車內的列表。
2. 原子性：操作應該是一次完成，要麼清空成功，要麼購物車狀態保持一致（理論上不會失敗）。
3. 冪等性：多次呼叫 clear() 對已清空的購物車不會有副作用，結果仍為空購物車。
---
### 8. get_item_count() 

#### 基本資訊
- **方法名稱**：`get_item_count`
- **用途**：回傳購物車中有幾種不同的商品（不是總數量）
- **優先級**：P1（建議功能）

#### 方法簽名
```python
def get_item_count(self) -> int:
    """
    取得購物車中的商品種類數

    Returns:
        int: 商品種類數
    """
    return len(self.items)
```

#### 前置條件（Preconditions）
- `self.items` 必須是有效

#### 後置條件（Postconditions）
**成功時**：
- 返回值為整數，表示購物車中不同商品的數量。
- 空購物車：返回 0。
- 非空購物車：返回 len(self.items)，不會修改購物車狀態或商品內容。`

#### 測試案例
| 案例編號    | 測試情境     | 商品     | 數量 | 庫存 | 購物車狀態                     | 預期結果 | 原因         |
| ------- | -------- | ------ | -- | -- | ------------------------- | ---- | ---------- |
| GIC-001 | 購物車有多種商品 | iPhone | 2  | 10 | 已加入 iPhone x1, AirPods x1 | 2    | 計算不同商品種類數量 |
| GIC-002 | 購物車有單一商品 | iPhone | 3  | 10 | 已加入 iPhone x3             | 1    | 單一商品，回傳 1  |
| GIC-003 | 購物車為空    | -      | 0  | 0  | 空購物車                      | 0    | 空購物車應回傳 0  |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product1 = Product("P001", "iPhone 15", 30000, 10, "iphone.png")
product2 = Product("P002", "AirPods Pro", 9000, 5, "airpods.png")

# 加入商品
cart.add_item(product1, 2)   # True
cart.add_item(product2, 1)   # True

# 檢查購物車中商品種類數
count = cart.get_item_count()
print(count)  # 2（iPhone 與 AirPods 兩種商品）
```
#### 實作提示
```python
def get_item_count(self) -> int:
    # 步驟 1: 計算購物車中不同商品的數量
    return len(self.items)
```

#### 注意事項
1.不修改購物車內容：此方法只讀取資料，不會改變 self.items 或其他狀態。
2. 安全性：即使購物車為空，也應正確返回 0。
3. 效率：計算應直接回傳清單長度，不需額外迴圈或複雜計算。

---
### 9. get_total_quantity()

#### 基本資訊
- **方法名稱**：`get_total_quantity`
- **用途**：回傳購物車中所有商品的數量總和
- **優先級**：P2（選做功能）

#### 方法簽名
```python
def get_total_quantity(self) -> int:
    """
    取得購物車中所有商品的數量總和

    Returns:
        int: 商品總數量
    """
    pass
```

#### 前置條件（Preconditions）
- `self.items` 必須為有效的列表
- `CartItem.quantity` 必須為非負整數

#### 後置條件（Postconditions）
**成功時**：
- 返回值為購物車中所有商品的數量總和（整數）
- 購物車內容 (self.items) 不會被修改

#### 測試案例

| 案例編號    | 測試情境 | 商品              | 數量   | 庫存    | 購物車狀態                 | 預期結果 | 原因               |
| ------- | ---- | --------------- | ---- | ----- | --------------------- | ---- | ---------------- |
| GTQ-001 | 空購物車 | -               | -    | -     | 空                     | 0    | 購物車沒有任何商品，總數量為 0 |
| GTQ-002 | 單一商品 | iPhone          | 2    | 10    | iPhone x2             | 2    | 只有一種商品，數量即總數量    |
| GTQ-003 | 多種商品 | iPhone, AirPods | 2, 3 | 10, 5 | iPhone x2, AirPods x3 | 5    | 多種商品，總數量為各商品數量加總 |
#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
iphone = Product("P001", "iPhone 15", 30000, 10, "iphone.png")
airpods = Product("P002", "AirPods Pro", 10000, 5, "airpods.png")

# 加入商品到購物車
cart.add_item(iphone, 2)    # iPhone x2
cart.add_item(airpods, 3)  # AirPods x3

# 取得購物車中所有商品的總數量
total_quantity = cart.get_total_quantity()
print(total_quantity)  # 5 (2 + 3)

```
#### 實作提示
```python
def get_total_quantity(self) -> int:
    """
    計算購物車中所有商品的數量總和
    
    Returns:
        int: 商品總數量
    """
    # 步驟 1: 初始化總數量
    total = 0
    
    # 步驟 2: 遍歷購物車中的每個 CartItem
    for item in self.items:
        total += item.quantity  # 累加數量
    
    # 步驟 3: 回傳總數量
    return total
```
#### 注意事項
1. **不修改購物車狀態**：方法僅計算，不會改變 `self.items`
2. **原子性**：方法執行過程中，不應有部分更新。
3. **可重入性**：相同操作可重複呼叫，結果一致
---
### 10. find_item()

#### 基本資訊
- **方法名稱**：`find_item`
- **用途**：根據商品 ID 尋找購物車中的項目
- **優先級**：P2（選做功能）

#### 方法簽名
```python
def find_item(self, product_id: str) -> Optional[CartItem]:
    """
    尋找購物車中的商品

    Args:
        product_id: 商品 ID

    Returns:
        CartItem | None: 找到返回 CartItem，否則返回 None
    """
    pass
```

#### 前置條件（Preconditions）
- `product_id` 不為 None
- `product_id` 是字串（str）
- `self.items` 為有效的購物車清單（list of CartItem）

#### 後置條件（Postconditions）
**成功時**：
- 回傳對應的 `CartItem` 物件
- 購物車內容不會被修改

**失敗時**：
- 回傳 `None`
- 購物車內容不會被修改

#### 測試案例

| 案例編號    | 測試情境      | 商品      | 數量 | 庫存 | 購物車狀態      | 預期結果          | 原因                   |
| ------- | --------- | ------- | -- | -- | ---------- | ------------- | -------------------- |
| FDI-001 | 商品存在於購物車  | iPhone  | 2  | 10 | 已加入 iPhone | ✅ 返回 CartItem | 商品已存在，應回傳對應 CartItem |
| FDI-002 | 商品不存在於購物車 | AirPods | 1  | 5  | 已加入 iPhone | ✅ 返回 None     | 商品不在購物車，應回傳 None     |
| FDI-003 | 空購物車查詢    | iPhone  | 2  | 10 | 空          | ✅ 返回 None     | 購物車為空，應回傳 None       |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 加入 2 個 iPhone
cart.add_item(product, 2)

# 查找商品
item = cart.find_item("P001")
print(item)  # <CartItem object>
print(item.quantity)  # 2
```
**範例 2：查找不存在的商品**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 購物車中沒有 AirPods
item = cart.find_item("P002")
print(item)  # None
```

#### 實作提示
```python
def find_item(self, product_id: str) -> Optional[CartItem]:
    # 步驟 1: 遍歷購物車中的 items 清單
    for item in self.items:
        # 步驟 2: 比對商品 ID
        if item.product.id == product_id:
            return item  # 找到返回 CartItem
    
    # 步驟 3: 若未找到，返回 None
    return None
```

#### 注意事項
1. **不修改購物車**：此方法僅查詢，不應該改變購物車內商品或數量
3. **冪等性**：相同的操作可以重複執行（累加數量）

---
### 11. has_item()

#### 基本資訊
- **方法名稱**：`has_item`
- **用途**：檢查購物車中是否有指定商品
- **優先級**：P2（選做功能）

#### 方法簽名
```python
def has_item(self, product_id: str) -> bool:
    """
    檢查購物車中是否有指定商品

    Args:
        product_id: 商品 ID

    Returns:
        bool: 有返回 True，沒有返回 False
    """
    pass
```

#### 前置條件（Preconditions）
- `product_id` 不為 None
- `product_id` 為有效的商品 ID 字串
- 購物車 `self.items` 已正確初始化

#### 後置條件（Postconditions）
**成功時**：
- 購物車狀態不變
- 回傳 `True`

**失敗時**：
- 購物車狀態不變
- 回傳 `False`


#### 驗證流程
檢查購物車中是否存在 product_id
├─ 是 → 返回 True
└─ 否 → 返回 False


#### 測試案例

| 案例編號    | 測試情境       | 商品      | 數量 | 庫存 | 購物車狀態     | 預期結果    | 原因        |
| ------- | ---------- | ------- | -- | -- | --------- | ------- | --------- |
| HSI-001 | 購物車已有指定商品  | iPhone  | 2  | 10 | iPhone x2 | ✅ True  | 商品存在於購物車  |
| HSI-002 | 購物車中沒有指定商品 | AirPods | 1  | 5  | iPhone x2 | ❌ False | 商品不存在購物車  |
| HSI-003 | 購物車為空      | iPhone  | 1  | 10 | 空         | ❌ False | 購物車沒有任何商品 |

#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 加入 2 個 iPhone
cart.add_item(product, 2)

# 檢查購物車是否有 iPhone
has_iphone = cart.has_item("P001")
print(has_iphone)  # True

# 檢查購物車是否有 AirPods
has_airpods = cart.has_item("P002")
print(has_airpods)  # False
```

#### 實作提示
```python
def has_item(self, product_id: str) -> bool:
    """
    檢查購物車中是否有指定商品
    """
    # 步驟 1: 使用 find_item 查找商品
    item = self.find_item(product_id)
    
    # 步驟 2: 如果找到返回 True，否則返回 False
    return item is not None
```

#### 注意事項
1. 不修改購物車內容：此方法僅檢查存在性，不應更改 items 清單。
2. 冪等性：同樣的查詢可重複執行，結果一致。
3. 健壯性：對不存在的 product_id 返回 False，不拋出例外。
---
### 12. get_discount_amount()

#### 基本資訊
- **方法名稱**：`get_discount_amount`
- **用途**：計算實際折扣了多少錢
- **優先級**：P2（建議功能）

#### 方法簽名
```python
def get_discount_amount(self) -> int:
    """
    取得折扣金額

    Returns:
        int: 折扣金額
    """
    pass
```

#### 前置條件（Preconditions）
- `self` 的購物車已能正確回傳 `get_total_amount`（總金額 ≥ 0）
- `self.discount` 必須是`None`或合法的 Discount 物件（包含折扣類型與折扣值）


#### 後置條件（Postconditions）
**成功時**：
- 回傳正整數的折扣金額
- 折扣金額永遠不會超過總金額
- 不會修改購物車的 items、商品數量、價格
- 若是百分比折扣，折扣金額正確套用四捨五入或無條件捨去（依實作規範）
- 若是固定金額折扣，回傳該固定折扣值，但上限不超過總金額


**失敗時**：
- 回傳 0
- 購物車狀態不變

#### 業務規則
參考 `05_business_rules.md`：
- BR-203: 折扣計算

#### 測試案例

| 案例編號    | 測試情境           | 商品     | 數量 | 庫存 | 購物車狀態                   | 預期結果 | 原因                           |
| ------- | -------------- | ------ | -- | -- | ----------------------- | ---- | ---------------------------- |
| GDA-001 | 無折扣券（無折扣）      | iPhone | 2  | 10 | 總額 2000，無折扣             | 0    | 無折扣情況折扣金額應為 0                |
| GDA-002 | 套用固定金額折扣       | iPhone | 2  | 10 | 總額 2000，折扣 SAVE100      | 100  | 固定折扣 100 元                   |
| GDA-003 | 固定折扣大於總額       | iPhone | 1  | 10 | 總額 500，折扣 SAVE1000      | 500  | 折扣不可超過總額                     |
| GDA-004 | 套用百分比折扣 10%    | iPhone | 2  | 10 | 總額 2000，折扣 SALE10       | 200  | 2000 × 0.1 = 200             |
| GDA-005 | 百分比折扣後有小數      | iPhone | 1  | 10 | 總額 999，折扣 SALE10        | 99   | 999 ×10% = 99.9 → 常見規則為無條件捨去 |
| GDA-006 | 購物車為空          | 無      | 0  | -  | 總額 0，折扣隨意               | 0    | 總額 0 → 折扣金額必然為 0             |
| GDA-007 | 折扣資料異常（折扣類型無效） | iPhone | 1  | 10 | 總額 1000，折扣類型錯誤          | 0    | 無效折扣不應影響金額                   |
| GDA-008 | 商品存在但折扣為 None  | iPhone | 1  | 10 | 總額 1000，discount = None | 0    | 無折扣 → 折扣金額為 0                |
#### 使用範例

**範例 1：固定折扣**
```python
cart = Cart()
product = Product("P001", "iPhone 15", 30000, 10, "iphone.png")

# 加入 1 台 iPhone（總額 30000）
cart.add_item(product, 1)

# 套用固定折扣 SAVE100
cart.discount = Discount(code="SAVE100", discount_type="fixed", amount=100)

print(cart.get_discount_amount())  # 100
```

**範例 2：百分比折扣**
```python
cart = Cart()
product = Product("P002", "AirPods Pro", 8000, 10, "airpods.png")

# 加入 2 組 AirPods（總額 16000）
cart.add_item(product, 2)

# 套用百分比折扣 SALE10（10% off）
cart.discount = Discount(code="SALE10", discount_type="percent", amount=10)

print(cart.get_discount_amount())  # 1600
```
#### 實作提示
```python
def get_discount_amount(self) -> int:
    # 步驟 1: 若無折扣，直接回傳 0
    if not self.discount:
        return 0

    # 步驟 2: 取得購物車總金額
    total_amount = self.get_total_amount()

    # 步驟 3: 根據折扣類型計算折扣金額
    if self.discount.discount_type == "fixed":
        # 固定折扣（例如 SAVE100）
        discount = self.discount.amount

    elif self.discount.discount_type == "percent":
        # 百分比折扣（例如 SALE10 -> 10%）
        discount = total_amount * self.discount.amount / 100

    else:
        # 未知折扣類型 → 不給折扣
        return 0

    # 步驟 4: 折扣不能超過總金額
    discount = min(discount, total_amount)

    # 步驟 5: 只回傳整數（捨去小數）
    return int(discount)

```

#### 注意事項
1. 不可修改購物車金額
get_discount_amount() 只計算折扣，不能改變商品金額或總額。
1. 折扣不能超過總金額
例如：總金額 $80，折扣 $100 → 最多只能折 $80。
1. 百分比折扣需正確處理小數點
計算後再轉成整數（通常為捨去小數）。
1. 允許無折扣
沒有折扣（self.discount is None）應回傳 0。
1. 純查詢方法（Pure Function）
不能改動 self.items、product、discount 等任何狀態）
---
### 13. remove_discount()

#### 基本資訊
- **方法名稱**：`remove_discount`
- **用途**：移除已套用的折扣碼
- **優先級**：P2（選做功能）

#### 方法簽名
```python
def remove_discount(self) -> None:
    """移除折扣碼"""
    pass
```

#### 前置條件（Preconditions）
- `self.discount` 可以是 `None` 或有效的折扣物件

#### 後置條件（Postconditions）
**成功時**：
- self.discount 會被設為 None（折扣被移除）
- 購物車中的商品、數量、金額均不會被修改

#### 測試案例

| 案例編號    | 測試情境                   | 商品     | 數量 | 庫存 | 購物車狀態                    | 預期結果                | 原因                     |
| ------- | ---------------------- | ------ | -- | -- | ------------------------ | ------------------- | ---------------------- |
| RMD-001 | 移除已套用的折扣碼              | iPhone | 2  | 10 | 已加入 iPhone 並套用折扣碼        | 無回傳值（折扣被成功移除）       | 折扣碼存在，應能被清除            |
| RMD-002 | 購物車內有商品但沒有折扣碼          | iPhone | 2  | 10 | 已加入 iPhone，discount=None | 無回傳值（狀態不變）          | 沒有折扣碼，呼叫後應維持 None      |
| RMD-003 | 購物車為空時移除折扣碼            | —      | —  | —  | 空，discount 可能有或沒有        | 無回傳值（折扣被清除或維持 None） | 與商品內容無關，應保持一致行為        |
#### 使用範例

**範例 1：基本使用**
```python
cart = Cart()

# 套用折扣碼
cart.applied_discount = Discount("SAVE100")

# 移除折扣碼
cart.remove_discount()

print(cart.applied_discount)  # None

```

**範例 2：重複移除折扣碼 **
```python
cart = Cart()

# 套用折扣碼
cart.applied_discount = Discount("SALE10")

cart.remove_discount()
cart.remove_discount()  # 再呼叫一次也不應出錯

print(cart.applied_discount)  # None
```


#### 實作提示
```python
def remove_discount(self) -> None:
    # 步驟 1: 檢查是否有折扣碼
    if self.applied_discount is None:
        # 沒有折扣碼時不用做任何事
        return
    
    # 步驟 2: 直接移除折扣碼
    self.applied_discount = None
```

#### 注意事項
1. **安全性**：即使沒有折扣碼，呼叫此方法也不能產生錯誤。
2. **不影響其他狀態**：移除折扣碼不會影響購物車商品、數量或總金額的基礎計算。
3. **冪等性**：多次呼叫 `remove_discount()` 結果相同，且不會修改任何額外資料。
4. **原子性**：方法執行中不會發生部分修改；要嘛移除折扣碼，要嘛不更動。
