import sys
import os

# 將專案根目錄加入路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from behave import given, when, then
from src.cart import ShoppingCart
from shared.data.products import PRODUCTS
from shared.data.discount_codes import get_discount_code

# ==================== Given 步驟 ====================

@given('折價券 "{coupon_code}" 需要最低消費 {min_amount:d} 元')
def step_impl(context, coupon_code, min_amount):
    """驗證折價券的最低消費金額"""
    discount_code = get_discount_code(coupon_code)
    
    assert discount_code is not None, f"找不到折價券: {coupon_code}"
    assert discount_code.min_amount == min_amount, \
        f"{coupon_code} 的最低消費應該是 {min_amount}，但實際是 {discount_code.min_amount}"


@given('折價券 "{coupon_code}" 已經過期')
def step_impl(context, coupon_code):
    """驗證折價券已過期（is_active = False）"""
    discount_code = get_discount_code(coupon_code)
    
    assert discount_code is not None, f"找不到折價券: {coupon_code}"
    assert discount_code.is_active == False, \
        f"{coupon_code} 應該已過期，但還是啟用狀態"
    
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

@when('我嘗試使用折價券 "{coupon_code}"')
def step_impl(context, coupon_code):
    """嘗試套用折價券（可能失敗）"""
    try:
        discount_code = get_discount_code(coupon_code)
        
        if discount_code is None:
            raise ValueError("折價券已過期或無效")
        
        context.cart.apply_discount(discount_code)
        context.discount_success = True
        context.error_message = None
    except ValueError as e:
        context.discount_success = False
        # 統一錯誤訊息格式
        error_msg = str(e)
        if "折扣碼已停用" in error_msg:
            context.error_message = "折價券已過期或無效"
        elif "未達最低消費金額" in error_msg:
            context.error_message = "未達最低消費金額"
        else:
            context.error_message = error_msg
    except Exception as e:
        context.discount_success = False
        context.error_message = str(e)

# ==================== Then 步驟 ====================

@then('折價券應該套用成功')
def step_impl(context):
    """驗證折價券套用成功"""
    assert context.cart.discount_code is not None, \
        "折價券應該已套用，但購物車中沒有折價券"

@then('折價券應該套用失敗')
def step_impl(context):
    """驗證折價券套用失敗"""
    assert context.discount_success == False, \
        "預期折價券套用失敗，但實際成功了"
    
# ==================== 輔助函數 ====================

def _get_product_by_name(product_name):
    """根據商品名稱取得 Product 物件"""
    for product in PRODUCTS:
        if product.name == product_name:
            return product
    raise ValueError(f"找不到商品: {product_name}")