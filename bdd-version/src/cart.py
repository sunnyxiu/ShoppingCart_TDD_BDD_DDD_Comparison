import sys
import os

# 將專案根目錄加入路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from shared.models.cart_item import CartItem
from shared.data.products import get_product_by_id
from shared.utils.price_calculator import calculate_total


class ShoppingCart:
    """購物車類別"""
    
    def __init__(self):
        self.items = []  # List[CartItem]
        self.discount_code = None
    
    def add_item(self, product_id: str, quantity: int):
        """
        加入商品到購物車
        
        Args:
            product_id: 商品 ID (例如: "P001")
            quantity: 數量
        
        Raises:
            ValueError: 當數量不合法或庫存不足時
        """
        # 驗證數量
        if quantity <= 0:
            raise ValueError("數量必須大於 0")
        
        if quantity > 99:
            raise ValueError("單項商品數量不可超過 99")
        
        # 取得商品
        product = get_product_by_id(product_id)
        if not product:
            raise ValueError(f"商品不存在: {product_id}")
        
        # 驗證庫存
        if quantity > product.stock:
            raise ValueError("庫存不足")
        
        # 檢查購物車中是否已有此商品
        existing_item = None
        for item in self.items:
            if item.product.id == product_id:
                existing_item = item
                break
        
        if existing_item:
            # 如果已存在，增加數量
            new_quantity = existing_item.quantity + quantity
            
            # 驗證新數量
            if new_quantity > 99:
                raise ValueError("單項商品數量不可超過 99")
            
            # 驗證庫存
            if new_quantity > product.stock:
                raise ValueError("庫存不足")
            
            existing_item.quantity = new_quantity
        else:
            # 如果不存在，新增商品
            self.items.append(CartItem(product, quantity))
    
    def get_items(self):
        """取得購物車中所有商品"""
        return self.items
    
    def get_total(self):
        """計算購物車總金額"""
        return calculate_total(self.items)
    
    def get_item_count(self):
        """取得購物車中的商品總數量"""
        return sum(item.quantity for item in self.items)