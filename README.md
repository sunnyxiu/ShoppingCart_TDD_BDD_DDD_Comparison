# ShoppingCart_TDD_BDD_DDD_Comparison
本專案採用完全獨立開發的方式，讓 TDD、BDD、Document-Driven 三位開發者各自獨立實作完整的購物車系統，以便進行公平的比較。

## 版本目錄結構

- `tdd-version/`
	- `src/cart.py`: 嚴格依循 TDD 流程開發的購物車實作。
	- `tests/`: 以 pytest 撰寫的單元測試與整合測試。
- `bdd-version/`
	- `src/`: 以 BDD 為導向的購物車實作。
	- `features/`: Gherkin 規格與對應步驟定義。
- `ddd-version/`
	- `src/`: 以 DDD 概念拆分的核心程式碼。
	- `docs/`: Ubiquitous Language 與領域文件。

所有版本在 `shared/` 資料夾中共用相同的資料模型、折扣與價格邏輯，確保比較過程的公平性。

## 運行方式

- TDD 版本：
	- `python -m pytest tdd-version/tests`
	- `python tdd-version/run_demo.py`
- BDD 版本：
	- `python -m pytest bdd-version/features`
	- `python bdd-version/run_demo.py`
- DDD 版本：
	- `python -m pytest ddd-version/tests`
	- `python ddd-version/run_demo.py`