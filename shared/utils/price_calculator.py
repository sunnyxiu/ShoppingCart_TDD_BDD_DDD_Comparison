"""
Price Calculator - 價格計算器
=============================

共用的價格計算工具函數

這個模組被所有版本共用，確保價格計算邏輯一致。
各版本的 Cart 類別會呼叫這些函數。

作者：Shopping Cart Team
版本：1.0.0
"""


def calculate_subtotal(unit_price: int, quantity: int) -> int:
    """
    計算商品小計
    
    Args:
        unit_price: 單價
        quantity: 數量
    
    Returns:
        int: 小計金額
    
    Example:
        >>> calculate_subtotal(100, 3)
        300
    """
    return unit_price * quantity


def calculate_total(items: list) -> int:
    """
    計算購物車總金額
    
    Args:
        items: CartItem 列表
    
    Returns:
        int: 總金額
    
    Example:
        >>> items = [
        ...     CartItem(Product("P001", "Item1", 100, 10, ""), 2),
        ...     CartItem(Product("P002", "Item2", 200, 5, ""), 1)
        ... ]
        >>> calculate_total(items)
        400
    """
    total = 0
    for item in items:
        total += item.subtotal
    return total


def calculate_fixed_discount(total: int, discount_amount: int) -> int:
    """
    計算固定金額折扣後的價格
    
    Args:
        total: 原始總金額
        discount_amount: 折扣金額
    
    Returns:
        int: 折扣後金額（最低為 0）
    
    Example:
        >>> calculate_fixed_discount(1000, 100)
        900
        >>> calculate_fixed_discount(50, 100)
        0
    """
    result = total - discount_amount
    return max(0, result)


def calculate_percentage_discount(total: int, discount_percentage: int) -> int:
    """
    計算百分比折扣後的價格
    
    Args:
        total: 原始總金額
        discount_percentage: 折扣百分比（例如：10 表示 10% off，即打 9 折）
    
    Returns:
        int: 折扣後金額（四捨五入到整數）
    
    Example:
        >>> calculate_percentage_discount(1000, 10)
        900
        >>> calculate_percentage_discount(1000, 15)
        850
    """
    discount_multiplier = (100 - discount_percentage) / 100
    result = total * discount_multiplier
    return round(result)


def calculate_final_amount(total: int, discount_code) -> int:
    """
    根據折扣碼計算最終金額
    
    Args:
        total: 原始總金額
        discount_code: DiscountCode 物件（可為 None）
    
    Returns:
        int: 最終金額
    
    Example:
        >>> # 固定金額折扣
        >>> code = DiscountCode("SAVE100", "fixed", 100, 0, True)
        >>> calculate_final_amount(1000, code)
        900
        
        >>> # 百分比折扣
        >>> code = DiscountCode("SALE10", "percentage", 10, 0, True)
        >>> calculate_final_amount(1000, code)
        900
        
        >>> # 無折扣
        >>> calculate_final_amount(1000, None)
        1000
    """
    if discount_code is None:
        return total
    
    if discount_code.discount_type == "fixed":
        return calculate_fixed_discount(total, discount_code.value)
    elif discount_code.discount_type == "percentage":
        return calculate_percentage_discount(total, discount_code.value)
    else:
        # 未知類型，不套用折扣
        return total


def calculate_discount_amount(total: int, discount_code) -> int:
    """
    計算實際折扣金額
    
    Args:
        total: 原始總金額
        discount_code: DiscountCode 物件（可為 None）
    
    Returns:
        int: 折扣金額
    
    Example:
        >>> code = DiscountCode("SAVE100", "fixed", 100, 0, True)
        >>> calculate_discount_amount(1000, code)
        100
        
        >>> code = DiscountCode("SALE10", "percentage", 10, 0, True)
        >>> calculate_discount_amount(1000, code)
        100
    """
    if discount_code is None:
        return 0
    
    final_amount = calculate_final_amount(total, discount_code)
    return total - final_amount


# 便捷的導出
__all__ = [
    'calculate_subtotal',
    'calculate_total',
    'calculate_fixed_discount',
    'calculate_percentage_discount',
    'calculate_final_amount',
    'calculate_discount_amount',
    'PriceCalculator',
]