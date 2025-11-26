import pytest

from cart import Cart
from shared.data.products import get_product_by_id


@pytest.fixture
def populated_cart():
    cart = Cart()
    iphone = get_product_by_id("P001")
    macbook = get_product_by_id("P002")
    assert iphone is not None
    assert macbook is not None

    cart.add_item(iphone.id, 2)
    cart.add_item(macbook.id, 1)
    return cart


def test_apply_valid_fixed_discount(populated_cart):
    success, message = populated_cart.apply_discount("SAVE100")

    assert success
    assert message == "折扣碼可用"
    assert populated_cart.applied_discount.code == "SAVE100"
    assert populated_cart.discount_amount == 100
    assert populated_cart.final_amount == populated_cart.subtotal - 100


def test_apply_valid_percentage_discount(populated_cart):
    success, _ = populated_cart.apply_discount("SALE10")

    assert success
    assert populated_cart.applied_discount.code == "SALE10"
    assert populated_cart.discount_amount == round(populated_cart.subtotal * 0.1)
    assert populated_cart.final_amount == populated_cart.subtotal - populated_cart.discount_amount


def test_apply_discount_below_minimum_amount():
    cart = Cart()
    airpods = get_product_by_id("P003")
    assert airpods is not None

    cart.add_item(airpods.id, 1)
    success, message = cart.apply_discount("SALE20")  # requires 10000

    assert success is False
    assert "未達最低消費" in message
    assert cart.applied_discount is None
    assert cart.discount_amount == 0
    assert cart.final_amount == cart.subtotal


def test_apply_unknown_discount_code():
    cart = Cart()
    product = get_product_by_id("P001")
    assert product is not None
    cart.add_item(product.id, 1)

    with pytest.raises(ValueError, match="折扣碼不存在"):
        cart.apply_discount("UNKNOWN")


def test_get_summary_returns_snapshot(populated_cart):
    populated_cart.apply_discount("SAVE500")

    summary = populated_cart.get_summary()

    assert summary["subtotal"] == populated_cart.subtotal
    assert summary["discount_amount"] == populated_cart.discount_amount
    assert summary["final_amount"] == populated_cart.final_amount
    assert summary["discount_code"] == populated_cart.applied_discount.code
    assert len(summary["items"]) == len(populated_cart.items)
    assert summary["items"][0]["product_id"] == populated_cart.items[0].product.id
