"""
Discount Validator - 折扣驗證器
===============================

共用的折扣碼驗證工具函數

這個模組被所有版本共用，確保折扣驗證邏輯一致。
各版本的 Cart 類別會呼叫這些函數。

作者：Shopping Cart Team
版本：1.0.0
"""


def is_active(discount_code) -> bool:
    """
    檢查折扣碼是否啟用
    
    Args:
        discount_code: DiscountCode 物件
    
    Returns:
        bool: 啟用返回 True，否則返回 False
    
    Example:
        >>> code = DiscountCode("SAVE100", "fixed", 100, 0, True)
        >>> is_active(code)
        True
        
        >>> code = DiscountCode("EXPIRED", "fixed", 100, 0, False)
        >>> is_active(code)
        False
    """
    return discount_code.is_active


def meets_minimum_amount(total: int, discount_code) -> bool:
    """
    檢查是否達到最低消費金額
    
    Args:
        total: 購物車總金額
        discount_code: DiscountCode 物件
    
    Returns:
        bool: 達到返回 True，否則返回 False
    
    Example:
        >>> code = DiscountCode("SAVE100", "fixed", 100, 1000, True)
        >>> meets_minimum_amount(1200, code)
        True
        >>> meets_minimum_amount(500, code)
        False
    """
    return total >= discount_code.min_amount


def validate_discount_code(total: int, discount_code) -> tuple[bool, str]:
    """
    驗證折扣碼是否可用
    
    檢查：
    1. 折扣碼是否啟用
    2. 是否達到最低消費金額
    
    Args:
        total: 購物車總金額
        discount_code: DiscountCode 物件
    
    Returns:
        tuple[bool, str]: (是否可用, 訊息)
            - (True, "折扣碼可用")
            - (False, "錯誤訊息")
    
    Example:
        >>> code = DiscountCode("SAVE100", "fixed", 100, 1000, True)
        >>> validate_discount_code(1200, code)
        (True, '折扣碼可用')
        
        >>> validate_discount_code(500, code)
        (False, '未達最低消費金額 1000 元')
        
        >>> code = DiscountCode("EXPIRED", "fixed", 100, 0, False)
        >>> validate_discount_code(1000, code)
        (False, '折扣碼已停用')
    """
    # 檢查是否啟用
    if not is_active(discount_code):
        return False, "折扣碼已停用"
    
    # 檢查是否達到最低消費
    if not meets_minimum_amount(total, discount_code):
        return False, f"未達最低消費金額 {discount_code.min_amount} 元"
    
    # 通過所有驗證
    return True, "折扣碼可用"


def validate_discount_type(discount_code) -> bool:
    """
    驗證折扣類型是否有效
    
    Args:
        discount_code: DiscountCode 物件
    
    Returns:
        bool: 有效返回 True，否則返回 False
    
    Example:
        >>> code = DiscountCode("SAVE100", "fixed", 100, 0, True)
        >>> validate_discount_type(code)
        True
        
        >>> code = DiscountCode("SAVE100", "unknown", 100, 0, True)
        >>> validate_discount_type(code)
        False
    """
    valid_types = ["fixed", "percentage"]
    return discount_code.discount_type in valid_types


def validate_discount_value(discount_code) -> tuple[bool, str]:
    """
    驗證折扣值是否合理
    
    規則：
    - 折扣值必須 > 0
    - 百分比折扣必須 <= 100
    
    Args:
        discount_code: DiscountCode 物件
    
    Returns:
        tuple[bool, str]: (是否有效, 訊息)
    
    Example:
        >>> code = DiscountCode("SAVE100", "fixed", 100, 0, True)
        >>> validate_discount_value(code)
        (True, '折扣值有效')
        
        >>> code = DiscountCode("SALE150", "percentage", 150, 0, True)
        >>> validate_discount_value(code)
        (False, '百分比折扣不能超過 100%')
    """
    # 檢查折扣值是否大於 0
    if discount_code.value <= 0:
        return False, "折扣值必須大於 0"
    
    # 如果是百分比折扣，檢查是否超過 100%
    if discount_code.discount_type == "percentage":
        if discount_code.value > 100:
            return False, "百分比折扣不能超過 100%"
    
    return True, "折扣值有效"


def get_validation_errors(total: int, discount_code) -> list[str]:
    """
    取得所有驗證錯誤訊息
    
    Args:
        total: 購物車總金額
        discount_code: DiscountCode 物件
    
    Returns:
        list[str]: 錯誤訊息列表（空列表表示沒有錯誤）
    
    Example:
        >>> code = DiscountCode("EXPIRED", "percentage", 150, 1000, False)
        >>> errors = get_validation_errors(500, code)
        >>> len(errors)
        3
        >>> "折扣碼已停用" in errors
        True
    """
    errors = []
    
    # 檢查是否啟用
    if not is_active(discount_code):
        errors.append("折扣碼已停用")
    
    # 檢查最低消費
    if not meets_minimum_amount(total, discount_code):
        errors.append(f"未達最低消費金額 {discount_code.min_amount} 元")
    
    # 檢查折扣類型
    if not validate_discount_type(discount_code):
        errors.append(f"無效的折扣類型: {discount_code.discount_type}")
    
    # 檢查折扣值
    is_valid, message = validate_discount_value(discount_code)
    if not is_valid:
        errors.append(message)
    
    return errors


# 便捷的導出
__all__ = [
    'is_active',
    'meets_minimum_amount',
    'validate_discount_code',
    'validate_discount_type',
    'validate_discount_value',
    'get_validation_errors',
    'DiscountValidator',
]