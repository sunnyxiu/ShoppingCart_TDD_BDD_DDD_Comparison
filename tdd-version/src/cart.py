from shared.data.products import get_product_by_id
from shared.data.discount_codes import get_discount_code
from shared.models.cart_item import CartItem
from shared.utils.discount_validator import (
    validate_discount_code,
    validate_discount_type,
    validate_discount_value,
)
from shared.utils.price_calculator import (
    calculate_discount_amount,
    calculate_final_amount,
    calculate_total,
)


class Cart:
    """Shopping cart implementation driven by TDD."""

    def __init__(self):
        self._items: list[CartItem] = []
        self._applied_discount = None
        self._discount_amount = 0
        self._final_amount = 0
        self._subtotal = 0

    @property
    def items(self) -> list:
        """Expose cart items; returns a shallow copy to prevent external mutation."""
        return list(self._items)

    @property
    def subtotal(self) -> int:
        return self._subtotal

    @property
    def applied_discount(self):
        return self._applied_discount

    @property
    def discount_amount(self) -> int:
        return self._discount_amount

    @property
    def final_amount(self) -> int:
        return self._final_amount

    def add_item(self, product_id: str, quantity: int = 1) -> None:
        """Add a product to the cart while respecting stock limits."""
        if quantity <= 0:
            raise ValueError("數量必須為正整數")

        product = get_product_by_id(product_id)
        if product is None:
            raise ValueError("未知商品")

        existing_item = self._find_item(product_id)
        new_quantity = quantity if existing_item is None else existing_item.quantity + quantity
        if new_quantity > product.stock:
            raise ValueError("超過庫存")

        if existing_item is None:
            self._items.append(CartItem(product, quantity))
        else:
            existing_item.quantity = new_quantity

        self._recalculate_totals()

    def apply_discount(self, code: str) -> tuple[bool, str]:
        """Apply discount code if valid. Returns (success, message)."""
        discount = get_discount_code(code)
        if discount is None:
            raise ValueError("折扣碼不存在")

        if not validate_discount_type(discount):
            self._clear_discount()
            return False, f"無效的折扣類型: {discount.discount_type}"

        value_valid, value_message = validate_discount_value(discount)
        if not value_valid:
            self._clear_discount()
            return False, value_message

        code_valid, code_message = validate_discount_code(self._subtotal, discount)
        if not code_valid:
            self._clear_discount()
            return False, code_message

        self._applied_discount = discount
        self._recalculate_totals()
        return True, code_message

    def update_quantity(self, product_id: str, quantity: int) -> None:
        """Update quantity for an existing cart item; 0 removes it."""
        if quantity < 0:
            raise ValueError("數量必須為零或正整數")

        item = self._find_item(product_id)
        if item is None:
            raise ValueError("購物車中沒有此商品")

        if quantity == 0:
            self._items = [i for i in self._items if i.product.id != product_id]
        else:
            if quantity > item.product.stock:
                raise ValueError("超過庫存")
            item.quantity = quantity

        self._recalculate_totals()

    def remove_item(self, product_id: str) -> None:
        """Remove a cart item if it exists."""
        before_count = len(self._items)
        self._items = [i for i in self._items if i.product.id != product_id]
        if len(self._items) != before_count:
            self._recalculate_totals()

    def get_summary(self) -> dict:
        """Return a snapshot of the current cart state."""
        items_snapshot = [
            {
                "product_id": item.product.id,
                "name": item.product.name,
                "unit_price": item.product.price,
                "quantity": item.quantity,
                "subtotal": item.subtotal,
            }
            for item in self._items
        ]

        return {
            "items": items_snapshot,
            "subtotal": self._subtotal,
            "discount_amount": self._discount_amount,
            "final_amount": self._final_amount,
            "discount_code": self._applied_discount.code if self._applied_discount else None,
        }

    def clear(self) -> None:
        """Remove all items and reset discounts."""
        self._items = []
        self._applied_discount = None
        self._recalculate_totals()

    # Internal helpers -------------------------------------------------

    def _find_item(self, product_id: str) -> CartItem | None:
        for item in self._items:
            if item.product.id == product_id:
                return item
        return None

    def _recalculate_totals(self) -> None:
        self._subtotal = calculate_total(self._items)
        self._update_discount_amounts()

    def _update_discount_amounts(self) -> None:
        if self._applied_discount is None:
            self._discount_amount = 0
            self._final_amount = self._subtotal
            return

        valid, message = validate_discount_code(self._subtotal, self._applied_discount)
        if not valid:
            self._clear_discount()
            return

        self._discount_amount = calculate_discount_amount(self._subtotal, self._applied_discount)
        self._final_amount = calculate_final_amount(self._subtotal, self._applied_discount)

    def _clear_discount(self) -> None:
        self._applied_discount = None
        self._discount_amount = 0
        self._final_amount = self._subtotal
