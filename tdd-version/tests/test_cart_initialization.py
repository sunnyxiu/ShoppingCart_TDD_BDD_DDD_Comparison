import pytest

from cart import Cart


def test_cart_starts_empty():
    cart = Cart()

    assert cart.items == []
    assert cart.subtotal == 0
    assert cart.discount_amount == 0
    assert cart.final_amount == 0
    assert cart.applied_discount is None
