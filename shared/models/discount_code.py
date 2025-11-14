"""
折扣碼類別定義（共用）
所有版本使用相同的 DiscountCode 類別
"""

class DiscountCode:
    def __init__(self, code: str, discount_type: str, value: int, 
                 min_amount: int, is_active: bool):
        self.code = code.upper()
        self.discount_type = discount_type  # "fixed" or "percentage"
        self.value = value
        self.min_amount = min_amount
        self.is_active = is_active
    
    def __repr__(self):
        return f"DiscountCode({self.code}, {self.discount_type}, {self.value})"
