"""Cart overview view for the pygame demo UI."""

from __future__ import annotations

import pygame

from shared.ui.views.base_view import BaseView


class CartView(BaseView):
    def __init__(self, screen: pygame.Surface, cart):
        super().__init__(screen)
        self.cart = cart
        self._selected_index = 0
        self._message = ""

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        items = self.cart.items
        if event.key == pygame.K_DOWN:
            if items:
                self._selected_index = min(len(items) - 1, self._selected_index + 1)
        elif event.key == pygame.K_UP:
            if items:
                self._selected_index = max(0, self._selected_index - 1)
        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
            self._remove_selected()
        elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):  # '+' key increases quantity
            self._change_quantity(1)
        elif event.key == pygame.K_MINUS:
            self._change_quantity(-1)

    def update(self) -> None:
        items = self.cart.items
        if items:
            self._selected_index = min(self._selected_index, len(items) - 1)
        else:
            self._selected_index = 0

    def draw(self) -> None:
        y = self.draw_title("購物車 (上下鍵移動, +/- 調整, Delete 移除)")
        y = self.draw_line(f"小計：${self.cart.subtotal:,}", y, color=self.SUBTEXT_COLOR)
        y = self.draw_line(f"折扣：-${self.cart.discount_amount:,}", y, color=self.SUBTEXT_COLOR)
        y = self.draw_line(f"應付金額：${self.cart.final_amount:,}", y, color=self.TEXT_COLOR)

        items = self.cart.items
        if not items:
            y = self.draw_line("購物車目前為空。請在商品檢視中加入商品。", y + 20, color=self.SUBTEXT_COLOR)
            message_y = y + 10
        else:
            for index, item in enumerate(items):
                prefix = "→" if index == self._selected_index else "  "
                line = (
                    f"{prefix} {item.product.name} x {item.quantity}  |  "
                    f"單價 ${item.product.price:,}  |  小計 ${item.subtotal:,}"
                )
                color = self.TEXT_COLOR if index != self._selected_index else (180, 90, 20)
                y = self.draw_line(line, y + 10 if index == 0 else y, color=color)
            message_y = y + 20

        self.draw_message(self._message, message_y, success=False)

    # Internal helpers -------------------------------------------------

    def _change_quantity(self, delta: int) -> None:
        items = self.cart.items
        if not items:
            return
        item = items[self._selected_index]
        new_quantity = item.quantity + delta
        try:
            if new_quantity <= 0:
                self.cart.remove_item(item.product.id)
            else:
                self.cart.update_quantity(item.product.id, new_quantity)
        except ValueError as exc:
            self._message = str(exc)
        else:
            self._message = ""

    def _remove_selected(self) -> None:
        items = self.cart.items
        if not items:
            return
        product_id = items[self._selected_index].product.id
        self.cart.remove_item(product_id)
        self._message = f"已移除 {product_id}"
