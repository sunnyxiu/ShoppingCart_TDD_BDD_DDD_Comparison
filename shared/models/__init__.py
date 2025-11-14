"""
Models Package
==============

共用的資料結構類別

使用方式：
    # 方法 1：從 models 直接匯入
    from shared.models import Product, CartItem, DiscountCode
    
    # 方法 2：分別匯入
    from shared.models.product import Product
    from shared.models.cart_item import CartItem
    from shared.models.discount_code import DiscountCode
"""

# 將類別匯入到 models 層級，方便使用
from .product import Product
from .cart_item import CartItem
from .discount_code import DiscountCode

# 定義 __all__，控制 from models import * 的行為
__all__ = [
    'Product',
    'CartItem',
    'DiscountCode',
]

# 版本資訊
__version__ = '1.0.0'