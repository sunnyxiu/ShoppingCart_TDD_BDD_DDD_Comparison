---
title: 06_error_handling.md

---

# 錯誤處理

## 錯誤處理策略
本系統採用「回傳值」方式處理錯誤，不使用例外（Exception）。

## 回傳值約定

### bool 回傳值
- `True`：操作成功
- `False`：操作失敗

**適用方法**：
- `add_item()`
- `remove_item()`
- `update_quantity()`

### tuple[bool, str] 回傳值
- `(True, "成功訊息")`：操作成功
- `(False, "錯誤訊息")`：操作失敗

**適用方法**：
- `apply_discount()`

## 錯誤訊息規範

### 格式
- 使用繁體中文
- 簡潔明確
- 包含具體資訊（如金額、數量）

### 訊息清單

| 錯誤代碼 | 錯誤訊息 | 觸發條件 |
|---------|---------|---------|
| E-001 | 折扣碼已停用 | `is_active == False` |
| E-002 | 未達最低消費金額 {min_amount} 元 | `total < min_amount` |
| E-003 | 商品不存在於購物車 | 找不到指定商品 |

## 錯誤處理範例
```python
# 範例 1：bool 回傳值
success = cart.add_item(product, 5)
if not success:
    print("加入失敗，請檢查數量或庫存")

# 範例 2：tuple 回傳值
success, message = cart.apply_discount(discount_code)
if not success:
    print(f"折扣套用失敗：{message}")
else:
    print(f"成功：{message}")
```

## 不拋出例外的原因
- 簡化呼叫方的程式碼
- 避免未捕獲例外導致程式崩潰
- 符合 Pygame 事件驅動的設計