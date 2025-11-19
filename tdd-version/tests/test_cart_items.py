import pytest

from cart import Cart
from shared.data.products import get_product_by_id


def test_add_item_creates_cart_item():
    cart = Cart()
    product = get_product_by_id("P001")
    assert product is not None

    cart.add_item(product.id, 2)

    assert len(cart.items) == 1
    item = cart.items[0]
    assert item.product.id == product.id
    assert item.quantity == 2
    assert cart.subtotal == product.price * 2
    assert cart.final_amount == cart.subtotal


def test_add_item_merges_same_product_quantities():
    cart = Cart()
    product = get_product_by_id("P002")
    assert product is not None

    cart.add_item(product.id, 1)
    cart.add_item(product.id, 2)

    item = cart.items[0]
    assert item.quantity == 3
    assert cart.subtotal == product.price * 3


def test_add_item_cannot_exceed_stock():
    cart = Cart()
    product = get_product_by_id("P003")
    assert product is not None

    cart.add_item(product.id, product.stock)

    with pytest.raises(ValueError, match="超過庫存"):
        cart.add_item(product.id, 1)


def test_update_quantity_changes_existing_item():
    cart = Cart()
    product = get_product_by_id("P004")
    assert product is not None

    cart.add_item(product.id, 1)
    cart.update_quantity(product.id, 3)

    item = cart.items[0]
    assert item.quantity == 3
    assert cart.subtotal == product.price * 3


def test_update_quantity_to_zero_removes_item():
    cart = Cart()
    product = get_product_by_id("P005")
    assert product is not None

    cart.add_item(product.id, 2)
    cart.update_quantity(product.id, 0)

    assert cart.items == []
    assert cart.subtotal == 0


def test_update_quantity_cannot_exceed_stock():
    cart = Cart()
    product = get_product_by_id("P002")
    assert product is not None

    cart.add_item(product.id, 1)

    with pytest.raises(ValueError, match="超過庫存"):
        cart.update_quantity(product.id, product.stock + 1)


def test_remove_item_deletes_entry():
    cart = Cart()
    product = get_product_by_id("P001")
    assert product is not None

    cart.add_item(product.id, 1)
    cart.remove_item(product.id)

    assert cart.items == []
    assert cart.subtotal == 0
