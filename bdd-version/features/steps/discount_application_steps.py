import sys
import os

# 將專案根目錄加入路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from behave import given, when, then
from src.cart import ShoppingCart
from shared.data.products import PRODUCTS
from shared.data.discount_codes import get_discount_code


# ==================== When 步驟 ====================

@when('我使用折價券 "{coupon_code}" 折抵 {value:d} 元')
def step_impl(context, coupon_code, value):
    """套用固定金額折價券（預期成功）"""
    discount_code = get_discount_code(coupon_code)
    
    # 驗證折扣值是否正確
    assert discount_code is not None, f"找不到折價券: {coupon_code}"
    assert discount_code.discount_type == "fixed", \
        f"{coupon_code} 應該是固定金額折扣"
    assert discount_code.value == value, \
        f"{coupon_code} 的折扣金額應該是 {value}，但實際是 {discount_code.value}"
    
    context.cart.apply_discount(discount_code)


@when('我使用折價券 "{coupon_code}" 折抵 {percentage:d}%')
def step_impl(context, coupon_code, percentage):
    """套用百分比折價券（預期成功）"""
    discount_code = get_discount_code(coupon_code)
    
    # 驗證折扣值是否正確
    assert discount_code is not None, f"找不到折價券: {coupon_code}"
    assert discount_code.discount_type == "percentage", \
        f"{coupon_code} 應該是百分比折扣"
    assert discount_code.value == percentage, \
        f"{coupon_code} 的折扣比例應該是 {percentage}%，但實際是 {discount_code.value}%"
    
    context.cart.apply_discount(discount_code)


# ==================== Then 步驟 ====================

@then('折價券應該套用成功')
def step_impl(context):
    """驗證折價券套用成功"""
    assert context.cart.discount_code is not None, \
        "折價券應該已套用，但購物車中沒有折價券"


# ==================== 輔助函數 ====================

def _get_product_by_name(product_name):
    """根據商品名稱取得 Product 物件"""
    for product in PRODUCTS:
        if product.name == product_name:
            return product
    raise ValueError(f"找不到商品: {product_name}")