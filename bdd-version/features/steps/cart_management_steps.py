from behave import given, when, then, step
from src.cart import ShoppingCart

@given('我的購物車是空的')
def step_impl(context):
    "初始化一個空購物車"
    context.cart = ShoppingCart()

@when('我加入 {quantity:d} 台 "{product_name}" 價格 {price:d} 元')
def step_impl(context, quantity, product_name, price):
    "加入商品到購物車"
    context.cart.add_item(product_name, quantity, price)

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
    item_names = [item.name for item in items]
    assert expected_name in item_names, \
        f"購物車中找不到 {expected_name}，目前有: {item_names}"    

@then('總計應該是 {expected_total:d} 元')
def step_impl(context, expected_total):
    """驗證購物車總金額"""
    actual_total = context.cart.get_total()
    assert actual_total == expected_total, \
        f"預期總計 {expected_total} 元，但實際是 {actual_total} 元" 