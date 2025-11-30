import sys
import os

# 將專案根目錄加入路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from behave import given, when, then
from src.cart import ShoppingCart
from shared.data.products import PRODUCTS


# ==================== Given 步驟 ====================

@given('我的購物車是空的')
def step_impl(context):
    """初始化一個空購物車"""
    context.cart = ShoppingCart()


@given('我的購物車中已有 {quantity:d} 台 "{product_name}" 價格 {price:d} 元')
def step_impl(context, quantity, product_name, price):
    """購物車預先加入商品"""
    context.cart = ShoppingCart()
    
    product = _get_product_by_name(product_name)
    
    # 驗證價格是否正確
    assert product.price == price, \
        f"{product_name} 的價格應該是 {price}，但實際是 {product.price}"
    
    context.cart.add_item(product.id, quantity)

@given('商品 "{product_name}" 的庫存有 {stock:d} 台')
def step_impl(context, product_name, stock):
    """設定商品庫存（模擬庫存變更）"""
    product = _get_product_by_name(product_name)
    # 暫時修改商品庫存（僅用於測試）
    product.stock = stock

@given('我的購物車中只有 {quantity:d} 台 "{product_name}"')
def step_impl(context, quantity, product_name):
    """購物車中只有指定商品（不驗證價格）"""
    context.cart = ShoppingCart()
    product = _get_product_by_name(product_name)
    context.cart.add_item(product.id, quantity)

@given('我的購物車中已有 {quantity:d} 台 "{product_name}"')
def step_impl(context, quantity, product_name):
    """購物車中已有商品（不指定價格，用於更新數量場景）"""
    context.cart = ShoppingCart()
    product = _get_product_by_name(product_name)
    context.cart.add_item(product.id, quantity)


# ==================== When 步驟 ====================

@when('我加入 {quantity:d} 台 "{product_name}" 價格 {price:d} 元')
def step_impl(context, quantity, product_name, price):
    """加入商品到購物車（指定價格，用於驗證）"""
    product = _get_product_by_name(product_name)
    
    # 驗證價格是否正確
    assert product.price == price, \
        f"{product_name} 的價格應該是 {price}，但實際是 {product.price}"
    
    context.cart.add_item(product.id, quantity)


@when('我加入 {quantity:d} 台 "{product_name}"')
def step_impl(context, quantity, product_name):
    """加入商品（不指定價格，使用產品預設價格）"""
    product = _get_product_by_name(product_name)
    context.cart.add_item(product.id, quantity)

@when('我嘗試加入 {quantity:d} 台 "{product_name}"')
def step_impl(context, quantity, product_name):
    """嘗試加入商品（可能失敗）"""
    try:
        product = _get_product_by_name(product_name)
        context.cart.add_item(product.id, quantity)
        context.add_success = True
        context.error_message = None
    except ValueError as e:
        context.add_success = False
        context.error_message = str(e)
    except Exception as e:
        context.add_success = False
        context.error_message = str(e)

@when('我移除 "{product_name}"')
def step_impl(context, product_name):
    """移除商品（預期成功）"""
    product = _get_product_by_name(product_name)
    context.cart.remove_item(product.id)


@when('我嘗試移除 "{product_name}"')
def step_impl(context, product_name):
    """嘗試移除商品（可能失敗）"""
    try:
        product = _get_product_by_name(product_name)
        context.cart.remove_item(product.id)
        context.remove_success = True
        context.error_message = None
    except ValueError as e:
        context.remove_success = False
        context.error_message = str(e)
    except Exception as e:
        context.remove_success = False
        context.error_message = str(e)

@when('我將 "{product_name}" 的數量更新為 {new_quantity:d} 台')
def step_impl(context, product_name, new_quantity):
    """更新商品數量（預期成功）"""
    product = _get_product_by_name(product_name)
    context.cart.update_item_quantity(product.id, new_quantity)


@when('我嘗試將 "{product_name}" 的數量更新為 {new_quantity:d} 台')
def step_impl(context, product_name, new_quantity):
    """嘗試更新商品數量（可能失敗）"""
    try:
        product = _get_product_by_name(product_name)
        context.cart.update_item_quantity(product.id, new_quantity)
        context.update_success = True
        context.error_message = None
    except ValueError as e:
        context.update_success = False
        context.error_message = str(e)
    except Exception as e:
        context.update_success = False
        context.error_message = str(e)

# ==================== Then 步驟 ====================

@then('購物車應該有 {expected_count:d} 件商品')
def step_impl(context, expected_count):
    """驗證購物車商品總數量"""
    actual_count = context.cart.get_item_count()
    assert actual_count == expected_count, \
        f"預期 {expected_count} 件商品，但實際有 {actual_count} 件"


@then('商品名稱應該是 "{expected_name}"')
def step_impl(context, expected_name):
    """驗證購物車中有指定名稱的商品"""
    items = context.cart.get_items()
    
    assert len(items) > 0, "購物車是空的"
    
    # 檢查是否有此商品
    has_product = any(item.product.name == expected_name for item in items)
    assert has_product, \
        f"購物車中找不到 {expected_name}，目前有: {[item.product.name for item in items]}"


@then('總計應該是 {expected_total:d} 元')
def step_impl(context, expected_total):
    """驗證購物車總金額"""
    actual_total = context.cart.get_total()
    assert actual_total == expected_total, \
        f"預期總計 {expected_total} 元，但實際是 {actual_total} 元"


@then('購物車應該有 {expected_quantity:d} 台 "{product_name}"')
def step_impl(context, expected_quantity, product_name):
    """驗證購物車中特定商品的數量"""
    total_quantity = 0
    
    # 計算該商品的總數量
    for item in context.cart.get_items():
        if item.product.name == product_name:
            total_quantity += item.quantity
    
    assert total_quantity == expected_quantity, \
        f"預期 {product_name} 有 {expected_quantity} 台，但實際有 {total_quantity} 台"

@then('加入應該失敗')
def step_impl(context):
    """驗證操作失敗"""
    assert context.add_success == False, \
        "預期操作失敗，但實際成功了"


@then('應該顯示錯誤訊息 "{expected_message}"')
def step_impl(context, expected_message):
    """驗證錯誤訊息"""
    assert context.error_message == expected_message, \
        f"預期錯誤訊息: '{expected_message}'，實際: '{context.error_message}'"

@then('購物車應該是空的')
def step_impl(context):
    """驗證購物車為空"""
    item_count = context.cart.get_item_count()
    assert item_count == 0, \
        f"購物車應該是空的，但還有 {item_count} 件商品"


@then('移除應該失敗')
def step_impl(context):
    """驗證移除操作失敗"""
    assert context.remove_success == False, \
        "預期移除失敗，但實際成功了"

@then('更新應該失敗')
def step_impl(context):
    """驗證更新操作失敗"""
    assert context.update_success == False, \
        "預期更新失敗，但實際成功了"

# ==================== 輔助函數 ====================

def _get_product_by_name(product_name):
    """根據商品名稱取得 Product 物件"""
    for product in PRODUCTS:
        if product.name == product_name:
            return product
    raise ValueError(f"找不到商品: {product_name}")
