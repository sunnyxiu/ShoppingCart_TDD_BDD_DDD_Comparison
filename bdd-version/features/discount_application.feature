Feature: 折扣功能

  Scenario: 套用固定金額折價券
    Given 我的購物車中已有 1 台 "Apple Watch" 價格 15000 元
    When 我使用折價券 "SAVE100" 折抵 100 元
    Then 折價券應該套用成功
    And 總計應該是 14900 元

  Scenario: 套用百分比折價券
    Given 我的購物車中已有 1 台 "Apple Watch" 價格 10000 元
    When 我使用折價券 "SALE10" 折抵 10%
    Then 折價券應該套用成功
    And 總計應該是 9000 元

  Scenario: 購物車金額未達最低消費
    Given 折價券 "SALE20" 需要最低消費 10000 元
    And 我的購物車中已有 1 台 "AirPods Pro" 價格 7990 元
    When 我嘗試使用折價券 "SALE20"
    Then 折價券應該套用失敗
    And 應該顯示錯誤訊息 "未達最低消費金額"

  Scenario: 使用已過期的折價券
    Given 折價券 "EXPIRED" 已經過期
    And 我的購物車中已有 1 台 "AirPods Pro" 價格 7990 元
    When 我嘗試使用折價券 "EXPIRED"
    Then 折價券應該套用失敗
    And 應該顯示錯誤訊息 "折價券已過期或無效"

  Scenario: 套用新折價券會覆蓋舊折價券
    Given 我的購物車中已有 1 台 "Apple Watch" 價格 15000 元
    And 已使用折價券 "SALE10" 折抵 10%
    When 我使用折價券 "SAVE100" 折抵 100 元
    Then 折價券應該套用成功
    And 總計應該是 14900 元
    And 折價券 "SALE10" 應該被移除

  Scenario: 折價券代碼不區分大小寫
    Given 我的購物車中已有 1 台 "Apple Watch" 價格 15000 元
    When 我使用折價券 "save100" 折抵 100 元
    Then 折價券應該套用成功
    And 總計應該是 14900 元