# Document-Driven Development 版本

## 📚 開發方法

**Document-Driven Development (DDD)** 是一種「文件先行」的開發方法：

1. **第一步：撰寫詳細的 API 文件**
   - 定義所有方法的簽名、參數、回傳值
   - 列出完整的業務規則和驗證邏輯
   - 提供測試案例和使用範例

2. **第二步：依據文件進行開發**
   - 嚴格遵循文件定義
   - 確保實作與文件 100% 一致
   - 不擅自修改或增減功能

3. **第三步：驗證實作符合文件**
   - 執行 API 符合性測試
   - 檢查文件與程式碼的一致性
   - 記錄文件更新次數

---

## 📁 目錄結構

```
ddd-version/
├── docs/                          # API 文件（DDD 核心）
│   ├── 01_overview.md            # 系統概述
│   ├── 02_architecture.md        # 架構設計
│   ├── 03_api_specification.md   # API 規格 ⭐ 最重要
│   ├── 04_data_models.md         # 資料模型
│   ├── 05_business_rules.md      # 業務規則
│   ├── 06_error_handling.md      # 錯誤處理
│   ├── 07_examples.md            # 使用範例
│   └── api_changelog.md          # API 變更紀錄
│
├── src/                          # 原始碼
│   ├── __init__.py
│   └── cart.py                   # Cart 類別（依文件開發）
│
├── tests/                        # 驗證測試
│   ├── __init__.py
│   ├── test_api_compliance.py    # API 符合性測試
│   └── test_documentation.py     # 文件一致性測試（選做）
│
├── main.py                       # 程式入口
├── manual_test.py                # 手動測試腳本
├── README.md                     # 本檔案
└── requirements.txt              # 套件需求
```

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 執行手動測試

```bash
python manual_test.py
```

### 3. 執行 API 符合性測試

```bash
cd tests
python test_api_compliance.py
# 或使用 pytest
pytest test_api_compliance.py -v
```

### 4. 執行主程式（需要 UI）

```bash
python main.py
```

---

## 📖 核心文件說明

### 1. API 規格文件 (`docs/03_api_specification.md`)

這是 DDD 的核心文件，包含：

- **13 個方法的完整定義**
  - 方法簽名（參數、回傳值、型別）
  - 前置條件和後置條件
  - 業務規則參考
  - 驗證流程
  - 測試案例（10+ 個）
  - 使用範例（3+ 個）

### 2. 業務規則 (`docs/05_business_rules.md`)

定義所有的業務邏輯：

- **BR-001**: 商品數量必須在 1-99 之間
- **BR-002**: 數量不能超過庫存
- **BR-003**: 累加後的數量仍需符合規則
- **BR-101**: 折扣碼必須是啟用狀態
- **BR-102**: 必須達到最低消費門檻
- **BR-201-203**: 價格計算規則

---

## ✅ 實作檢查清單

### 方法實作（13/13）

- [x] `add_item()` - 加入商品
- [x] `remove_item()` - 移除商品
- [x] `update_quantity()` - 更新數量
- [x] `get_total()` - 取得總金額
- [x] `apply_discount()` - 套用折扣
- [x] `get_final_amount()` - 取得最終金額
- [x] `clear()` - 清空購物車
- [x] `get_item_count()` - 取得商品種類數
- [x] `get_total_quantity()` - 取得總數量
- [x] `find_item()` - 尋找商品
- [x] `has_item()` - 檢查商品存在
- [x] `get_discount_amount()` - 取得折扣金額
- [x] `remove_discount()` - 移除折扣

### 文件完整性（8/8）

- [x] 01_overview.md
- [x] 02_architecture.md
- [x] 03_api_specification.md
- [x] 04_data_models.md
- [x] 05_business_rules.md
- [x] 06_error_handling.md
- [x] 07_examples.md
- [x] api_changelog.md

### 測試完整性

- [x] 手動測試通過
- [x] API 符合性測試完成
- [ ] 文件一致性測試（選做）

---

## 📊 開發數據記錄

### 開發時間

| 階段 | 預估時間 | 實際時間 | 備註 |
|-----|---------|---------|------|
| 文件撰寫 | 20-30 小時 | __ 小時 | 8 個文件 |
| 程式實作 | 8-10 小時 | __ 小時 | 13 個方法 |
| 測試驗證 | 2-3 小時 | __ 小時 | API 符合性測試 |
| **總計** | **30-43 小時** | **__ 小時** | |

### 文件更新次數

| 文件 | 更新次數 | 更新原因 |
|-----|---------|---------|
| 03_api_specification.md | __ 次 | |
| 05_business_rules.md | __ 次 | |
| 其他文件 | __ 次 | |

### 遇到的問題

1. **問題描述**：
   - 解決方法：

2. **問題描述**：
   - 解決方法：

---

## 🎯 DDD 方法的優勢

1. **文件即合約**：清楚定義期望行為
2. **減少誤解**：開發者和使用者對 API 有相同理解
3. **易於維護**：文件提供完整的參考
4. **便於協作**：其他人可以依據文件實作

---

## 🎯 DDD 方法的挑戰

1. **前期投入大**：需要花大量時間撰寫文件
2. **文件同步**：需要保持文件與程式碼一致
3. **過度設計**：可能在實作前就定義過多細節

---

## 📝 下一步

1. 完成 UI 整合（`main.py`）
2. 收集完整的開發數據
3. 與 TDD、BDD 版本進行比較
4. 撰寫期末報告

---

## 版本資訊

- 版本：DDD Version 1.0.0
- 最後更新：2024-11-XX