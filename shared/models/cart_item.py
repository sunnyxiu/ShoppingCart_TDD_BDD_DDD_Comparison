"""
購物車項目類別定義（共用）
所有版本使用相同的 CartItem 類別
"""

class CartItem:
    def __init__(self, product, quantity: int):
        self.product = product
        self.quantity = quantity
    
    @property
    def subtotal(self) -> int:
        return self.product.price * self.quantity
    
    def __repr__(self):
        return f"CartItem({self.product.name} x{self.quantity})"