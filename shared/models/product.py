"""
商品類別定義（共用）
所有版本使用相同的 Product 類別
"""

class Product:
    def __init__(self, id: str, name: str, price: int, stock: int, image_path: str):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.image_path = image_path
    
    def __repr__(self):
        return f"Product({self.id}, {self.name}, ${self.price})"
