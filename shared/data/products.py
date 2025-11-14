"""
預設商品資料（共用）
所有版本使用相同的測試資料
"""

from shared.models.product import Product

PRODUCTS = [
    Product("P001", "iPhone 15", 30000, 10, "assets/products/iphone.png"),
    Product("P002", "MacBook Pro", 50000, 5, "assets/products/macbook.png"),
    Product("P003", "AirPods Pro", 7990, 20, "assets/products/airpods.png"),
    Product("P004", "Apple Watch", 12900, 15, "assets/products/watch.png"),
    Product("P005", "iPad Air", 19900, 8, "assets/products/ipad.png"),
]

def get_product_by_id(product_id: str):
    """根據 ID 取得商品"""
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    return None
