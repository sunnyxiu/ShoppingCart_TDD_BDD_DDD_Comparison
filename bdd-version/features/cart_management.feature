Feature: 購物車功能

  Scenario: 加入商品到空購物車
    Given 我的購物車是空的
    When 我加入 1 台 "iPhone 15" 價格 30000 元
    Then 購物車應該有 1 件商品
    And 商品名稱應該是 "iPhone 15"
    And 總計應該是 30000 元

  Scenario: 加入同樣商品到購物車中
    Given 我的購物車中已有 1 台 "MacBook Pro" 價格 50000 元
    When 我加入 1 台 "MacBook Pro"
    Then 購物車應該有 2 台 "MacBook Pro"
    And 總計應該是 100000 元

  Scenario: 加入商品數量超過庫存
    Given 商品 "iPhone 15" 的庫存有 10 台
    And 我的購物車是空的
    When 我嘗試加入 11 台 "iPhone 15"
    Then 加入應該失敗
    And 應該顯示錯誤訊息 "庫存不足"

  Scenario: 加入商品數量為零
    Given 我的購物車是空的
    When 我嘗試加入 0 台 "iPhone 15"
    Then 加入應該失敗
    And 應該顯示錯誤訊息 "數量必須大於 0"

  Scenario: 加入商品數量為負數
    Given 我的購物車是空的
    When 我嘗試加入 -1 台 "iPhone 15"
    Then 加入應該失敗
    And 應該顯示錯誤訊息 "數量必須大於 0"

  Scenario: 加入商品數量超過99
    Given 我的購物車是空的
    When 我嘗試加入 100 台 "iPhone 15"
    Then 加入應該失敗
    And 應該顯示錯誤訊息 "單項商品數量不可超過 99"

  Scenario: 移除購物車中存在的商品
    Given 我的購物車中已有 1 台 "iPhone 15" 價格 30000 元
    When 我移除 "iPhone 15"
    Then 購物車應該是空的
    And 總計應該是 0 元

  Scenario: 移除購物車中不存在的商品
    Given 我的購物車中只有 1 台 "MacBook Pro"
    When 我嘗試移除 "iPhone 15"
    Then 移除應該失敗
    And 應該顯示錯誤訊息 "商品不存在於購物車"

  Scenario: 更新購物車中商品數量
    Given 我的購物車中已有 1 台 "MacBook Pro" 價格 50000 元
    When 我將 "MacBook Pro" 的數量更新為 3 台
    Then 購物車應該有 3 台 "MacBook Pro"
    And 總計應該是 150000 元

  Scenario: 更新商品數量超過庫存
    Given 商品 "iPhone 15" 的庫存有 10 台
    And 我的購物車中已有 1 台 "iPhone 15"
    When 我嘗試將 "iPhone 15" 的數量更新為 11 台
    Then 更新應該失敗
    And 應該顯示錯誤訊息 "庫存不足"

  Scenario: 清空購物車
    Given 我的購物車中有以下商品:
      | 商品名稱      | 數量 | 價格   |
      | iPhone 15    | 1   | 30000 |
      | MacBook Pro  | 1   | 50000 |
    And 已套用折價券 "SAVE100"
    When 我清空購物車
    Then 購物車應該是空的
    And 折價券應該被移除
    And 總計應該是 0 元