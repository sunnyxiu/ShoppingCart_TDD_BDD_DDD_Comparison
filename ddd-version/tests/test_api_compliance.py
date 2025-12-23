"""
API 符合性測試
驗證實作是否完全符合 docs/03_api_specification.md 的定義
"""

import sys
import os
sys.path.append('..')

import pytest
from src.cart import Cart
from shared.models.product import Product
from shared.models.discount_code import DiscountCode
from shared.data.products import PRODUCTS, get_product_by_id
from shared.data.discount_codes import get_discount_code


class TestAPICompliance:
    """測試實作是否符合 API 文件定義"""
    
    def setup_method(self):
        """每個測試前初始化"""
        self.cart = Cart()
        self.iphone = get_product_by_id("P001")
        self.macbook = get_product_by_id("P002")
        self.airpods = get_product_by_id("P003")
    
    # ========== add_item() 測試 ==========
    
    def test_add_item_method_signature(self):
        """測試 add_item 方法簽名"""
        # 驗證方法存在
        assert hasattr(self.cart, 'add_item')
        
        # 驗證回傳值型別是 bool
        result = self.cart.add_item(self.iphone, 1)
        assert isinstance(result, bool)
    
    def test_add_item_new_product(self):
        """ADD-001: 正常加入新商品"""
        result = self.cart.add_item(self.iphone, 2)
        assert result == True
        assert self.cart.get_item_count() == 1
        assert self.cart.items[0].quantity == 2
    
    def test_add_item_accumulation(self):
        """ADD-002: 重複加入同商品（累加）"""
        self.cart.add_item(self.iphone, 2)
        result = self.cart.add_item(self.iphone, 3)
        assert result == True
        assert self.cart.items[0].quantity == 5
    
    def test_add_item_quantity_zero(self):
        """ADD-003: 數量為 0 → False"""
        result = self.cart.add_item(self.iphone, 0)
        assert result == False
        assert self.cart.get_item_count() == 0
    
    def test_add_item_quantity_negative(self):
        """ADD-004: 數量為負數 → False"""
        result = self.cart.add_item(self.iphone, -1)
        assert result == False
        assert self.cart.get_item_count() == 0
    
    def test_add_item_quantity_over_99(self):
        """ADD-005: 數量超過 99 → False"""
        result = self.cart.add_item(self.iphone, 100)
        assert result == False
        assert self.cart.get_item_count() == 0
    
    def test_add_item_exceed_stock(self):
        """ADD-006: 超過庫存 → False"""
        result = self.cart.add_item(self.iphone, self.iphone.stock + 1)
        assert result == False
        assert self.cart.get_item_count() == 0
    
    def test_add_item_accumulation_exceed_stock(self):
        """ADD-007: 累加後超過庫存 → False"""
        self.cart.add_item(self.iphone, self.iphone.stock - 2)
        result = self.cart.add_item(self.iphone, 5)
        assert result == False
        # 購物車狀態不應改變
        assert self.cart.items[0].quantity == self.iphone.stock - 2
    
    def test_add_item_accumulation_over_99(self):
        """ADD-008: 累加後超過 99 → False"""
        self.iphone.stock = 200
        self.cart.add_item(self.iphone, 60)
        result = self.cart.add_item(self.iphone, 50)
        assert result == False
        assert self.cart.items[0].quantity == 60
        self.iphone.stock = 10
    
    def test_add_item_boundary_value_1(self):
        """ADD-009: 邊界值 1 → True"""
        result = self.cart.add_item(self.iphone, 1)
        assert result == True
    
    def test_add_item_boundary_value_99(self):
        """ADD-010: 邊界值 99 → True"""
        # 假設庫存 >= 99
        if self.iphone.stock >= 99:
            result = self.cart.add_item(self.iphone, 99)
            assert result == True
    
    # ========== remove_item() 測試 ==========
    
    def test_remove_item_method_signature(self):
        """測試 remove_item 方法簽名"""
        assert hasattr(self.cart, 'remove_item')
        result = self.cart.remove_item("P001")
        assert isinstance(result, bool)
    
    def test_remove_item_existing(self):
        """REM-001: 成功移除存在的商品"""
        self.cart.add_item(self.iphone, 1)
        result = self.cart.remove_item("P001")
        assert result == True
        assert self.cart.get_item_count() == 0
    
    def test_remove_item_non_existing(self):
        """REM-002: 移除不存在的商品 → False"""
        result = self.cart.remove_item("P999")
        assert result == False
    
    def test_remove_item_empty_cart(self):
        """REM-003: 從空購物車移除 → False"""
        result = self.cart.remove_item("P001")
        assert result == False
    
    # ========== update_quantity() 測試 ==========
    
    def test_update_quantity_method_signature(self):
        """測試 update_quantity 方法簽名"""
        assert hasattr(self.cart, 'update_quantity')
        result = self.cart.update_quantity("P001", 1)
        assert isinstance(result, bool)
    
    def test_update_quantity_success(self):
        """UPD-001: 成功更新數量"""
        self.cart.add_item(self.iphone, 2)
        result = self.cart.update_quantity("P001", 5)
        assert result == True
        assert self.cart.items[0].quantity == 5
    
    def test_update_quantity_non_existing(self):
        """UPD-002: 更新不存在的商品 → False"""
        result = self.cart.update_quantity("P999", 5)
        assert result == False
    
    def test_update_quantity_zero(self):
        """UPD-003: 數量為 0 → False"""
        self.cart.add_item(self.iphone, 2)
        result = self.cart.update_quantity("P001", 0)
        assert result == False
        assert self.cart.items[0].quantity == 2  # 不應改變
    
    def test_update_quantity_negative(self):
        """UPD-004: 數量為負數 → False"""
        self.cart.add_item(self.iphone, 2)
        result = self.cart.update_quantity("P001", -1)
        assert result == False
        assert self.cart.items[0].quantity == 2

    def test_update_quantity_exceed_stock(self):
        """UPD-005: 數量超過庫存 → False"""
        self.cart.add_item(self.iphone, 2)
        result = self.cart.update_quantity("P001", self.iphone.stock + 1)
        assert result == False
        assert self.cart.items[0].quantity == 2
       
    def test_update_quantity_over_99(self):
        """UPD-006: 數量超過 99 → False"""
        self.cart.add_item(self.iphone, 2)
        result = self.cart.update_quantity("P001", 100)
        assert result == False
        assert self.cart.items[0].quantity == 2
    

    # ========== get_total() 測試 ==========
    
    def test_get_total_method_signature(self):
        """測試 get_total 方法簽名"""
        assert hasattr(self.cart, 'get_total')
        result = self.cart.get_total()
        assert isinstance(result, int)
    
    def test_get_total_empty_cart(self):
        """GT-001: 空購物車 → 0"""
        assert self.cart.get_total() == 0
    
    def test_get_total_single_item(self):
        """GT-002: 單一商品"""
        self.cart.add_item(self.iphone, 2)
        expected = self.iphone.price * 2
        assert self.cart.get_total() == expected
    
    def test_get_total_multiple_items(self):
        """GT-003: 多個商品"""
        self.cart.add_item(self.iphone, 2)
        self.cart.add_item(self.airpods, 1)
        expected = self.iphone.price * 2 + self.airpods.price * 1
        assert self.cart.get_total() == expected
    
    # ========== apply_discount() 測試 ==========
    
    def test_apply_discount_method_signature(self):
        """測試 apply_discount 方法簽名"""
        assert hasattr(self.cart, 'apply_discount')
        discount = get_discount_code("SAVE100")
        result = self.cart.apply_discount(discount)
        # 必須回傳 tuple
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)
    
    def test_apply_discount_fixed_success(self):
        """APD-001: 成功套用固定折扣"""
        self.cart.add_item(self.iphone, 2)  # $60000
        discount = get_discount_code("SAVE500")
        success, msg = self.cart.apply_discount(discount)
        assert success == True
        assert msg == "折扣已套用"
        assert self.cart.applied_discount == discount
    
    def test_apply_discount_percentage_success(self):
        """APD-002: 成功套用百分比折扣"""
        self.cart.add_item(self.iphone, 2)
        discount = get_discount_code("SALE10")
        success, msg = self.cart.apply_discount(discount)
        assert success == True
        assert msg == "折扣已套用"
    
    def test_apply_discount_below_threshold(self):
        """APD-003: 未達門檻 → False"""
        self.cart.add_item(self.airpods, 1)  # $7990
        discount = get_discount_code("SALE20")  # 需滿 $10000
        success, msg = self.cart.apply_discount(discount)
        assert success == False
        assert "未達最低消費金額" in msg
        assert "10000" in msg
    
    def test_apply_discount_inactive(self):
        """APD-004: 折扣碼停用 → False"""
        self.cart.add_item(self.iphone, 1)
        discount = get_discount_code("EXPIRED")
        success, msg = self.cart.apply_discount(discount)
        assert success == False
        assert msg == "折扣碼已停用"
    
    def test_apply_discount_override(self):
        """APD-005: 覆蓋舊折扣"""
        self.cart.add_item(self.iphone, 2)
        discount1 = get_discount_code("SAVE100")
        discount2 = get_discount_code("SAVE500")
        
        self.cart.apply_discount(discount1)
        success, msg = self.cart.apply_discount(discount2)
        
        assert success == True
        assert self.cart.applied_discount == discount2

    def test_apply_discount_case_insensitive(self):
        """APD-006: 折扣碼不分大小寫"""
        self.cart.add_item(self.iphone, 1)

        # 文件說 SAVE100 = save100
        discount_upper = get_discount_code("SAVE100")
        discount_lower = get_discount_code("save100")

        # 應該兩個都能找到同一個折扣碼
        assert discount_upper is not None, "折扣碼 SAVE100 不應為 None"
        assert discount_lower is not None, "折扣碼 save100 不應為 None"
        assert discount_upper.code.lower() == discount_lower.code.lower(), \
            "折扣碼應不分大小寫"

        # 套用小寫折扣碼
        success, msg = self.cart.apply_discount(discount_lower)

        assert success == True, "小寫折扣碼應可成功套用"
        assert self.cart.applied_discount.code.lower() == "save100", \
            "系統應以不分大小寫方式識別折扣碼"

    
    # ========== get_final_amount() 測試 ==========
    
    def test_get_final_amount_no_discount(self):
        """GFA-001: 無折扣時"""
        self.cart.add_item(self.iphone, 1)
        assert self.cart.get_final_amount() == self.cart.get_total()
    
    def test_get_final_amount_with_fixed_discount(self):
        """"GFA-002: 固定金額折扣"""
        self.cart.add_item(self.iphone, 1)  # $30000
        discount = get_discount_code("SAVE500")
        self.cart.apply_discount(discount)
        assert self.cart.get_final_amount() == 30000 - 500
    
    def test_get_final_amount_with_percentage_discount(self):
        """"GFA-003: 百分比折扣"""
        self.cart.add_item(self.iphone, 1)  # $30000
        discount = get_discount_code("SALE10")  # 10% off
        self.cart.apply_discount(discount)
        expected = 30000 - (30000 * 10 // 100)
        assert self.cart.get_final_amount() == expected
    
    def test_get_final_amount_discount_exceeds_total(self):
        """"GFA-004: 折扣超過總金額 → 0"""
        # 創建一個總金額很小的購物車，但套用大額折扣
        small_product = Product("TEST", "Test", 100, 10, "")
        self.cart.add_item(small_product, 1)
        
        # 假設折扣超過總金額
        large_discount = DiscountCode("LARGE", "fixed", 1000, 0, True)
        self.cart.apply_discount(large_discount)
        
        assert self.cart.get_final_amount() == 0
    
    def test_percentage_discount_rounding(self):
        """GFA-005: 百分比折扣需四捨五入"""

        self.cart.add_item(self.iphone, 1)

        # 手動建立 33% 折扣
        discount = DiscountCode("save33", "percentage", 33, 0, True)

        success, msg = self.cart.apply_discount(discount)

        assert success is True

        # 30000 * 0.67 = 20100
        assert self.cart.get_final_amount() == 20100

    
    # ========== clear() 測試 ==========
    
    def test_clear_with_items(self):
        """CLR-001: 清空有商品的購物車"""
        self.cart.add_item(self.iphone, 2)
        discount = get_discount_code("SAVE100")
        self.cart.apply_discount(discount)
        
        self.cart.clear()
        
        assert self.cart.get_item_count() == 0
        assert self.cart.applied_discount is None
    
    def test_clear_empty_cart(self):
        """CLR-002: 清空空購物車"""
        self.cart.clear()
        assert self.cart.get_item_count() == 0
    
    # ========== 輔助方法測試 ==========
    
    def test_get_item_count(self):
        """測試 get_item_count"""
        assert self.cart.get_item_count() == 0
        self.cart.add_item(self.iphone, 1)
        assert self.cart.get_item_count() == 1
        self.cart.add_item(self.airpods, 1)
        assert self.cart.get_item_count() == 2
        self.cart.add_item(self.airpods, 1)
        assert self.cart.get_item_count() == 2
    
    def test_get_total_quantity(self):
        """測試 get_total_quantity"""
        self.cart.add_item(self.iphone, 2)
        assert self.cart.get_total_quantity() == 2
        self.cart.add_item(self.airpods, 3)
        assert self.cart.get_total_quantity() == 5
    
    def test_find_item(self):
        """測試 find_item"""
        item = self.cart.find_item("P002")
        assert item is None
        self.cart.add_item(self.iphone, 1)
        item = self.cart.find_item("P001")
        assert item is not None
        assert item.product.id == "P001"
        
        item = self.cart.find_item("P999")
        assert item is None
    
    def test_has_item(self):
        """測試 has_item"""
        assert self.cart.has_item("P001") == False
        self.cart.add_item(self.iphone, 1)
        assert self.cart.has_item("P001") == True
        assert self.cart.has_item("P002") == False
    
    def test_get_discount_amount(self):
        """測試 get_discount_amount"""
        self.cart.add_item(self.iphone, 1)  # $30000
        
        # 無折扣
        assert self.cart.get_discount_amount() == 0
        
        # 固定折扣
        discount = get_discount_code("SAVE500")
        self.cart.apply_discount(discount)
        assert self.cart.get_discount_amount() == 500
    
    def test_gda_001_no_discount(self):
        """GDA-001: 無折扣券（無折扣）"""
        self.cart.add_item(self.iphone, 2)  # 2 * 1000 = 2000
        discount_amount = self.cart.get_discount_amount()
        assert discount_amount == 0


    def test_gda_002_fixed_discount(self):
        """GDA-002: 套用固定金額折扣"""
        self.cart.add_item(self.iphone, 2)  # 2000
        discount = get_discount_code("SAVE100")
        self.cart.apply_discount(discount)
        discount_amount = self.cart.get_discount_amount()
        assert discount_amount == 100


    def test_gda_003_fixed_discount_exceeds_total(self):
        """GDA-003: 固定折扣大於總額"""
        # 將 iPhone 價格暫時改為 500
        self.iphone.price = 500
        self.cart.add_item(self.iphone, 1)  # 總額 500
        discount = DiscountCode("SAVE1000", "fixed", 1000, 0, True)
        self.cart.apply_discount(discount)
        discount_amount = self.cart.get_discount_amount()
        # 折扣不應超過總額
        assert discount_amount == 500
        # 折扣後總額不能小於 0
        assert self.cart.get_final_amount() == 0
        self.iphone.price = 30000



    def test_gda_004_percentage_10(self):
        """GDA-004: 套用百分比折扣 10%"""
        self.cart.add_item(self.iphone, 2)  # 60000
        discount = get_discount_code("SALE10")
        self.cart.apply_discount(discount)
        discount_amount = self.cart.get_discount_amount()
        assert self.cart.get_total() == 60000
        assert discount_amount == 6000  # 60000 * 0.1
        


    def test_gda_005_percentage_truncate_decimal(self):
        """GDA-005: 百分比折扣後有小數 → 無條件捨去"""
        # 假設 iPhone 價格為 999（
        self.iphone.price = 999
        self.cart.add_item(self.iphone, 1)

        discount = get_discount_code("SALE10")
        self.cart.apply_discount(discount)
        discount_amount = self.cart.get_discount_amount()

        # 999 * 0.1 = 99.9 → 無條件捨去 = 99
        assert discount_amount == 99
        self.iphone.price = 30000


    def test_gda_006_empty_cart(self):
        """GDA-006: 購物車為空"""
        discount = get_discount_code("SALE10")
        self.cart.apply_discount(discount)
        discount_amount = self.cart.get_discount_amount()
        assert discount_amount == 0


    def test_gda_007_invalid_discount_type(self):
        """GDA-007: 折扣類型錯誤"""
        self.cart.add_item(self.iphone, 1)
        discount = DiscountCode("BADTYPE", "unknown", 123, 0, True)
        self.cart.apply_discount(discount)
        discount_amount = self.cart.get_discount_amount()

        # invalid discount type → discount should be 0
        assert discount_amount == 0


    def test_gda_008_discount_is_none(self):
        """GDA-008: 商品存在但折扣為 None"""
        self.cart.add_item(self.iphone, 1)

        discount_amount = self.cart.get_discount_amount()

        assert discount_amount == 0

    
    def test_remove_discount(self):
        """RMD-001: remove_discount"""
        self.cart.add_item(self.iphone, 1)
        discount = get_discount_code("SAVE100")
        self.cart.apply_discount(discount)
        
        self.cart.remove_discount()
        assert self.cart.applied_discount is None
    
    def test_rmd_002_remove_when_none(self):
        """RMD-002: 購物車有商品但沒有折扣碼"""
        self.cart.add_item(self.iphone, 2)
        # 初始應為 None
        assert self.cart.applied_discount is None
        # 執行移除
        result = self.cart.remove_discount()
        # 無回傳值或 None 都可
        assert result is None
        # 狀態不變
        assert self.cart.applied_discount is None

    def test_rmd_003_remove_when_cart_empty_no_discount(self):
        """RMD-003: 購物車為空且無折扣碼"""
        
        assert self.cart.applied_discount is None

        result = self.cart.remove_discount()
        assert result is None

        assert self.cart.applied_discount is None




if __name__ == "__main__":
    pytest.main([__file__, "-v"])