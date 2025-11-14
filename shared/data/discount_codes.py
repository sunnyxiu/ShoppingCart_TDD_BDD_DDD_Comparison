"""
預設折扣碼資料（共用）
所有版本使用相同的折扣碼
"""

from shared.models.discount_code import DiscountCode

DISCOUNT_CODES = {
    "SAVE100": DiscountCode("SAVE100", "fixed", 100, 1000, True),
    "SAVE500": DiscountCode("SAVE500", "fixed", 500, 5000, True),
    "SALE10": DiscountCode("SALE10", "percentage", 10, 0, True),
    "SALE20": DiscountCode("SALE20", "percentage", 20, 10000, True),
    "EXPIRED": DiscountCode("EXPIRED", "fixed", 100, 0, False),
}

def get_discount_code(code: str):
    """根據折扣碼字串取得折扣碼物件（不分大小寫）"""
    return DISCOUNT_CODES.get(code.upper())
