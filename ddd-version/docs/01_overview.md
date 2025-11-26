---
title: 01_overview.md

---

# 電商購物車系統 - 系統概述

## 專案目標
簡述這個購物車系統要解決什麼問題

## 核心功能
- 商品管理（加入、移除、更新數量）
- 折扣碼系統
- 價格計算

## 使用者故事
1. 加入商品到購物車

    **User Story**
    As a customer, I want to add an item to my shopping cart, so that I can purchase it later.

   **Why / User Motivation**
    讓顧客可以先建立購買清單，不必立即結帳。

   **Acceptance Criteria**
    Given 我正在瀏覽商品頁面
    When 我點擊「加入購物車」
    Then 商品應被加入購物車
    And 顯示新增成功的提示
    And 若商品已在購物車中則應更新數量（或提示使用者）
    
2. 從購物車移除商品

    **User Story**
    As a customer, I want to remove items from my shopping cart, so that unwanted items do not affect my total price.

    **Acceptance Criteria**
    Given 我有商品在購物車內
    When 我點擊「移除」
    Then 商品應從購物車中消失
    And 總價應同步更新

3. 更新購物車中的商品數量

    **User Story**
    As a customer, I want to adjust the quantity of items in the cart, so that the purchased amount matches my needs.

    **Acceptance Criteria**
    Given 購物車內已有某商品
    When 我修改數量（增加或減少）
    Then 新數量應立即更新
    And 總價應正確重計
    And 若數量變成 0，應提示是否移除該項商品
4. 套用折扣碼

    **User Story**
    As a customer, I want to apply a discount code, so that I can reduce my total payment.

    **Acceptance Criteria**
    Given 我在結帳前有輸入折扣碼
    When 我按下「套用折扣碼」
    Then 系統應驗證折扣碼是否有效
    And 若有效，應顯示折扣後價格
    And 若無效，應顯示適當錯誤提示（如已過期或不適用）
5. 顯示折扣後的最終價格

    **User Story**
    As a customer, I want to see the updated total price after discounts, so that I know the final amount I need to pay.

    **Acceptance Criteria**
    Given 購物車商品與折扣碼資訊已存在
    When 系統計算總價
    Then 應清楚顯示「原價」、「折扣額」、「最終價格」
    And 應保證計算邏輯一致且正確
    
6. 查看購物車內容

    **User Story**
    As a customer, I want to view the items in my cart, so that I can confirm my order before checkout.

    **Acceptance Criteria**
    Given 我打開購物車頁面
    When 資料成功載入
    Then 我應看到每個商品的名稱、單價、數量、小計
    And 應顯示總價與折扣後價格（若適用）
    
7. 清空購物車（clear）
**User Story**
As a customer, I want to remove everything in my cart, so that I can redo my order.

    **Acceptance Criteria**
    Given 購物車有商品
    When 我選擇清空購物車
    Then 所有商品與折扣碼應被移除
    
8. 查看商品種類數量（get_item_count）
**User Story**
As a customer, I want to know how many kinds of products are in my cart, so that I can know what's in my cart.

    **Acceptance Criteria**
    系統應回傳購物車中「不同商品」的數量
    數量與實際項目一致
    
9. 查看商品總數量（get_total_quantity）
**User Story**
As a customer, I want to see the total amount in my cart, so that I know how many items I am buying.

    **Acceptance Criteria**
    系統返回所有商品 quantity 的加總
10. 查詢購物車中的商品（find_item）
**User Story**
As a system, I need to find the item in the cart through product id, so that can support the add, update and remove.

    **Acceptance Criteria**

    找到 → 回傳 CartItem
    找不到 → 回傳 None
    
11. 檢查商品是否存在於購物車（has_item）
User Story（系統行為）

作為系統，
我需要確認某商品是否存在購物車，
以避免重複邏輯錯誤。

Acceptance Criteria

存在 → True

不存在 → False

12. 顯示折扣金額（get_discount_amount）
**User Story**
As a customer, I want to know the discount amount, so that I knoe how much I saved.


    **Acceptance Criteria**
    Given 總金額與折扣碼
    When 系統計算折扣
    Then 應顯示扣掉多少金額（整數）

13. 移除折扣碼（remove_discount）
User Story
As a customer, I want to remove discount, so that I can apply another discount, or undo the discount.

    **Acceptance Criteria**

    系統清除 applied_discount
    移除後總額應回到原價


## 技術棧
- pytest==7.4.3
- pydantic==2.5.0
- Python 3.x
- Pygame（UI）
- 純 OOP 設計

## 專案範圍
### 包含的功能
- ✅ 基本購物車操作
- ✅ 折扣碼系統

### 不包含的功能
- ❌ 會員系統
- ❌ 資料庫持久化
- ❌ 付款流程