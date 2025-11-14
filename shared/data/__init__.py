"""
Data Package
============

共用的測試資料

使用方式：
    # 方法 1：從 data 直接匯入
    from shared.data import PRODUCTS, DISCOUNT_CODES, get_product_by_id
    
    # 方法 2：分別匯入
    from shared.data.products import PRODUCTS, get_product_by_id
    from shared.data.discount_codes import DISCOUNT_CODES, get_discount_code
"""

# 匯入商品資料
from .products import PRODUCTS, get_product_by_id

# 匯入折扣碼資料
from .discount_codes import DISCOUNT_CODES, get_discount_code

# 定義 __all__
__all__ = [
    'PRODUCTS',
    'DISCOUNT_CODES',
    'get_product_by_id',
    'get_discount_code',
]