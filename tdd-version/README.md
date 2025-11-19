# TDD Version Plan

TDD 實作只依賴 `shared/` 目錄提供的模型、資料與工具，所有功能都以 pytest 測試推動。

## 測試與實作邏輯

| 模組 | 來源 | 關聯 |
| --- | --- | --- |
| `shared.models.Product` | 共用 | CartItem 需要固定欄位 |
| `shared.models.CartItem` | 共用 | 購物車項目封裝 |
| `shared.models.DiscountCode` | 共用 | 折扣碼狀態管理 |
| `shared.utils.price_calculator` | 共用 | 負責小計、總額與折扣計算 |
| `shared.utils.discount_validator` | 共用 | 驗證折扣碼可用性 |
| `shared.data.products` / `discount_codes` | 共用 | 測試固定種子資料 |

## 主要測試案例（Red → Green → Refactor）

1. **購物車初始化**
   - 新建 `Cart` 時應為空且總金額為 0。
2. **加入商品**
   - `add_item(product_id, quantity)` 建立 `CartItem` 並累計數量。
   - 連續加入同商品時合併數量、不可超過庫存；違規回報錯誤。
3. **更新與移除**
   - `update_quantity` 調整數量（含設為 0 時移除）。
   - `remove_item` 從購物車刪除指定商品。
4. **合計計算**
   - `cart.subtotal` 與 `cart.total_items` 應使用 `price_calculator.calculate_total`。
5. **折扣碼流程**
   - `apply_discount(code)`：
     - 以 `discount_codes.get_discount_code` 載入折扣碼。
     - 使用 `discount_validator.validate_discount_code` 和 `validate_discount_type/value`。
     - 通過時保存折扣碼並計算 `discount_amount`、`final_amount`。
     - 失敗時提供錯誤訊息並維持原折扣狀態。
6. **最終金額**
   - `get_summary()` 回傳 items、subtotal、discount、final_amount 等欄位。
   - 固定金額與百分比折扣都需呼叫 `price_calculator.calculate_final_amount`。
7. **清空購物車**
   - `clear()` 清除項目與折扣。

## 測試目錄結構

```
tdd-version/
  src/cart.py        # 待實作的 Cart 類別
  tests/
    test_cart_items.py
    test_cart_discounts.py
    test_cart_summary.py
```

每個測試檔以 pytest fixture 提供 `Cart` 實例與共用商品資料，確保測試彼此獨立。
