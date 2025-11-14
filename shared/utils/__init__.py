"""
Utils Package
=============

共用的工具函數

這個包提供所有版本都會使用的工具函數，確保計算邏輯一致。

Modules:
    price_calculator: 價格計算相關函數
    discount_validator: 折扣驗證相關函數

Example:
    >>> from shared.utils import price_calculator, discount_validator
    >>> 
    >>> # 計算價格
    >>> total = price_calculator.calculate_total(items)
    >>> 
    >>> # 驗證折扣碼
    >>> is_valid, msg = discount_validator.validate_discount_code(total, code)
"""

# 匯入所有工具模組
from . import price_calculator
from . import discount_validator


# 定義 __all__
__all__ = [
    # 模組
    'price_calculator',
    'discount_validator',
    
    # 常用函數
    'calculate_subtotal',
    'calculate_total',
    'calculate_final_amount',
    'calculate_discount_amount',
    'validate_discount_code',
    'is_active',
    'meets_minimum_amount',
]

__version__ = '1.0.0'