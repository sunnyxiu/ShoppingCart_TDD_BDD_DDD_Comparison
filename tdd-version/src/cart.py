class Cart:
    """Shopping cart implementation driven by TDD."""

    def __init__(self):
        self._items: list = []
        self._applied_discount = None
        self._discount_amount = 0
        self._final_amount = 0

    @property
    def items(self) -> list:
        """Expose cart items; returns a shallow copy to prevent accidental mutation."""
        return list(self._items)

    @property
    def subtotal(self) -> int:
        """Current subtotal (no items yet, so zero)."""
        return 0

    @property
    def applied_discount(self):
        return self._applied_discount

    @property
    def discount_amount(self) -> int:
        return self._discount_amount

    @property
    def final_amount(self) -> int:
        return self._final_amount
