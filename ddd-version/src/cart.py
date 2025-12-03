"""
購物車類別 - Document-Driven Development 版本
嚴格遵循 docs/03_api_specification.md 的定義
"""

from typing import List, Optional, Tuple
import sys
import os
import math

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # 目前檔案所在資料夾
PARENT_DIR = os.path.dirname(CURRENT_DIR)                 # 上一層
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)             # 上兩層

sys.path.insert(0, GRANDPARENT_DIR)

from shared.models.product import Product
from shared.models.cart_item import CartItem
from shared.models.discount_code import DiscountCode


class Cart:
    """
    購物車類別
    
    負責管理購物車中的商品和折扣碼。
    完整 API 文件請參考：docs/03_api_specification.md
    """
    
    def __init__(self):
        """初始化空購物車"""
        self.items: List[CartItem] = []
        self.applied_discount: Optional[DiscountCode] = None
    
    # ========== P0 核心方法 ==========
    
    def add_item(self, product: Product, quantity: int) -> bool:
        """
        加入商品到購物車
        
        如果商品已存在，則累加數量。
        
        Args:
            product (Product): 要加入的商品物件
            quantity (int): 購買數量，範圍 1-99
        
        Returns:
            bool: 成功返回 True，失敗返回 False
        
        Business Rules:
            - BR-001: 數量必須在 1-99 之間
            - BR-002: 數量不能超過庫存
            - BR-003: 累加後的數量仍需符合規則
        
        Reference:
            API 文件 §1
        """
        # 步驟 1: 驗證數量範圍（BR-001）
        if quantity < 1 or quantity > 99:
            return False
        
        # 步驟 2: 檢查庫存（BR-002）
        if quantity > product.stock:
            return False
        
        # 步驟 3: 檢查商品是否已存在
        existing_item = self.find_item(product.id)
        
        if existing_item:
            # 步驟 4: 計算累加後的數量
            new_quantity = existing_item.quantity + quantity
            
            # 步驟 5: 驗證累加後的數量（BR-003）
            if new_quantity > 99 or new_quantity > product.stock:
                return False
            
            # 步驟 6: 更新數量
            existing_item.quantity = new_quantity
            return True
        
        # 步驟 7: 建立新的 CartItem
        new_item = CartItem(product, quantity)
        self.items.append(new_item)
        return True
    
    def remove_item(self, product_id: str) -> bool:
        """
        從購物車移除商品
        
        Args:
            product_id (str): 商品 ID
        
        Returns:
            bool: 成功返回 True，商品不存在返回 False
        
        Reference:
            API 文件 §2
        """
        # 尋找商品
        item = self.find_item(product_id)
        
        # 如果找不到，返回 False
        if item is None:
            return False
        
        # 移除商品
        self.items.remove(item)
        return True
    
    def update_quantity(self, product_id: str, quantity: int) -> bool:
        """
        更新購物車中商品的數量
        
        Args:
            product_id (str): 商品 ID
            quantity (int): 新的數量，範圍 1-99
        
        Returns:
            bool: 成功返回 True，失敗返回 False
        
        Business Rules:
            - BR-001: 數量必須在 1-99 之間
            - BR-002: 數量不能超過庫存
        
        Reference:
            API 文件 §3
        """
        # 步驟 1: 驗證數量範圍（BR-001）
        if quantity < 1 or quantity > 99:
            return False
        
        # 步驟 2: 尋找商品
        item = self.find_item(product_id)
        
        # 步驟 3: 檢查商品是否存在
        if item is None:
            return False
        
        # 步驟 4: 檢查庫存（BR-002）
        if quantity > item.product.stock:
            return False
        
        # 步驟 5: 更新數量
        item.quantity = quantity
        return True
    
    def get_total(self) -> int:
        """
        計算購物車原始總金額（未套用折扣）
        
        Returns:
            int: 總金額
        
        計算公式:
            total = sum(item.subtotal for item in items)
        
        Reference:
            API 文件 §4
        """
        total = 0
        for item in self.items:
            total += item.subtotal
        return total
    
    def apply_discount(self, discount_code: DiscountCode) -> Tuple[bool, str]:
        """
        套用折扣碼
        
        Args:
            discount_code (DiscountCode): 折扣碼物件
        
        Returns:
            tuple[bool, str]: (是否成功, 訊息)
                - 成功: (True, "折扣已套用")
                - 失敗: (False, "錯誤原因")
        
        Business Rules:
            - BR-101: 折扣碼必須是啟用狀態
            - BR-102: 購物車總金額必須 >= min_amount
        
        Reference:
            API 文件 §5
        """
        # 步驟 1: 檢查折扣碼是否啟用（BR-101）
        if not discount_code.is_active:
            return (False, "折扣碼已停用")
        
        # 步驟 2: 取得購物車總金額
        total = self.get_total()
        
        # 步驟 3: 檢查是否達到最低消費門檻（BR-102）
        if total < discount_code.min_amount:
            return (False, f"未達最低消費金額 {discount_code.min_amount} 元")
        
        # 步驟 4: 套用折扣（覆蓋舊的）
        self.applied_discount = discount_code
        
        # 步驟 5: 返回成功
        return (True, "折扣已套用")
    
    def get_final_amount(self) -> int:
        """
        計算最終金額（套用折扣後）
        
        Returns:
            int: 最終金額（四捨五入到整數，最低為 0）
        
        計算公式:
            final_amount = max(0, total - discount_amount)
        
        Reference:
            API 文件 §6
        """
        total = self.get_total()
        discount = self.get_discount_amount()
        final = total - discount
        
        # 確保最終金額不為負數
        return max(0, final)
    
    # ========== P1 建議方法 ==========
    
    def clear(self) -> None:
        """
        清空購物車
        
        移除所有商品和折扣碼。
        
        Reference:
            API 文件 §7
        """
        self.items.clear()
        self.applied_discount = None
    
    def get_item_count(self) -> int:
        """
        取得購物車中的商品種類數
        
        Returns:
            int: 商品種類數
        
        Reference:
            API 文件 §8
        """
        return len(self.items)
    
    # ========== P2 輔助方法 ==========
    
    def get_total_quantity(self) -> int:
        """
        取得購物車中所有商品的數量總和
        
        Returns:
            int: 商品總數量
        
        Reference:
            API 文件 §9
        """
        total = 0
        for item in self.items:
            total += item.quantity
        return total
    
    def find_item(self, product_id: str) -> Optional[CartItem]:
        """
        尋找購物車中的商品
        
        Args:
            product_id (str): 商品 ID
        
        Returns:
            CartItem | None: 找到返回 CartItem，否則返回 None
        
        Reference:
            API 文件 §10
        """
        for item in self.items:
            if item.product.id == product_id:
                return item
        return None
    
    def has_item(self, product_id: str) -> bool:
        """
        檢查購物車中是否有指定商品
        
        Args:
            product_id (str): 商品 ID
        
        Returns:
            bool: 有返回 True，沒有返回 False
        
        Reference:
            API 文件 §11
        """
        return self.find_item(product_id) is not None
    
    def get_discount_amount(self) -> int:
        """
        取得折扣金額
        
        Returns:
            int: 折扣金額（未套用折扣時返回 0）
        
        計算方式:
            - 固定折扣: discount_code.value
            - 百分比折扣: total × (discount_code.value / 100)
            - 無折扣: 0
        
        Reference:
            API 文件 §12
        """
        # 如果沒有套用折扣，返回 0
        if self.applied_discount is None:
            return 0
        
        total = self.get_total()
        discount_code = self.applied_discount
        
        # 根據折扣類型計算
        if discount_code.discount_type == "fixed":
            # 固定金額折扣
            return min(discount_code.value, total)
        
        elif discount_code.discount_type == "percentage":
            # 百分比折扣
            discount_amount = total * discount_code.value / 100
            return math.floor(discount_amount)
        
        return 0
    
    def remove_discount(self) -> None:
        """
        移除折扣碼
        
        Reference:
            API 文件 §13
        """
        self.applied_discount = None