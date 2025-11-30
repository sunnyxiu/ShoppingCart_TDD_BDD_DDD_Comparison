import sys
import os

# 將專案根目錄加入路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from shared.models.cart_item import CartItem
from shared.data.products import get_product_by_id
from shared.utils.price_calculator import calculate_total
from typing import List, Tuple


class Cart:
    """購物車類別"""
    
    def __init__(self):
        """初始化購物車"""
        self.items: List[CartItem] = []
        self.applied_discount: None  # 重要！必須初始化這個屬性
    
    def add_item(self, product_id: str, quantity: int) -> bool:
        """加入商品到購物車"""
        # 驗證數量 - 分開檢查
        if quantity <= 0:
            raise ValueError("數量必須大於 0")
        
        if quantity > 99:
            raise ValueError("單項商品數量不可超過 99")
        
        # 取得商品
        product = get_product_by_id(product_id)
        if not product:
            raise ValueError(f"商品不存在: {product_id}")
        
        # 檢查購物車中是否已有此商品
        existing_item = None
        for item in self.items:
            if item.product.id == product_id:
                existing_item = item
                break
        
        if existing_item:
            # 如果已存在，累加數量
            new_quantity = existing_item.quantity + quantity
            
            # 驗證新數量
            if new_quantity > 99:
                raise ValueError("單項商品數量不可超過 99")
            
            # 驗證庫存
            if new_quantity > product.stock:
                raise ValueError("庫存不足")
            
            existing_item.quantity = new_quantity
        else:
            # 驗證庫存
            if quantity > product.stock:
                raise ValueError("庫存不足")
            
            # 新增商品
            self.items.append(CartItem(product, quantity))
        
        return True
    
    def remove_item(self, product_id: str) -> bool:
        """從購物車移除商品"""
        item_exists = any(item.product.id == product_id for item in self.items)
        
        if not item_exists:
            raise ValueError("商品不存在於購物車")
        
        self.items = [item for item in self.items if item.product.id != product_id]
        return True
    
    def update_quantity(self, product_id: str, quantity: int) -> bool:
        """更新購物車中商品的數量"""
        # 驗證數量 - 分開檢查
        if quantity <= 0:
            raise ValueError("數量必須大於 0")
        
        if quantity > 99:
            raise ValueError("單項商品數量不可超過 99")
        
        # 找到購物車中的商品
        target_item = None
        for item in self.items:
            if item.product.id == product_id:
                target_item = item
                break
        
        if not target_item:
            raise ValueError("商品不存在於購物車")
        
        # 取得商品資訊驗證庫存
        product = get_product_by_id(product_id)
        if quantity > product.stock:
            raise ValueError("庫存不足")
        
        # 更新數量
        target_item.quantity = quantity
        return True
    
    def clear(self):
        """清空購物車"""
        self.items = []
        self.applied_discount = None
    
    def get_total(self) -> int:
        """計算購物車原始總金額（未套用折扣）"""
        return calculate_total(self.items)
    
    def get_final_amount(self) -> int:
        """計算最終金額（套用折扣後）"""
        from shared.utils.price_calculator import calculate_final_amount
        
        # 計算原始總金額
        original_total = calculate_total(self.items)
        
        # 如果有折價券，計算折扣後金額
        if self.applied_discount:
            return calculate_final_amount(original_total, self.applied_discount)
        
        return original_total
    
    def apply_discount(self, discount_code) -> Tuple[bool, str]:
        """套用折扣碼"""
        from shared.utils.discount_validator import validate_discount_code
        
        # 計算原始總金額
        original_total = self.get_total()
        
        # 驗證折價券
        is_valid, message = validate_discount_code(original_total, discount_code)
        
        if not is_valid:
            raise ValueError(message)
        
        # 套用折價券（新的會覆蓋舊的）
        self.applied_discount = discount_code
        return True, "折扣已套用"
    
    def get_items(self) -> List[CartItem]:
        """取得購物車中所有商品"""
        return self.items
    
    def get_item_count(self) -> int:
        """取得購物車中的商品總數量"""
        return sum(item.quantity for item in self.items)