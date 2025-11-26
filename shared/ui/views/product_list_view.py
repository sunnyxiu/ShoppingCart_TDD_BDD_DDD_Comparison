"""Product list view for the pygame demo UI."""

from __future__ import annotations

import pygame

from shared.data.products import PRODUCTS
from shared.ui.views.base_view import BaseView


class ProductListView(BaseView):
    def __init__(self, screen: pygame.Surface, cart):
        super().__init__(screen)
        self.cart = cart
        self._products = PRODUCTS
        self._selected_index = 0
        self._message = ""
        self._message_success = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_DOWN:
            self._selected_index = min(len(self._products) - 1, self._selected_index + 1)
        elif event.key == pygame.K_UP:
            self._selected_index = max(0, self._selected_index - 1)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._add_selected_product()

    def update(self) -> None:
        self._selected_index = min(self._selected_index, len(self._products) - 1)

    def draw(self) -> None:
        y = self.draw_title("商品清單 (上下鍵選擇，Enter 加入購物車)")
        y = self.draw_line("共用資料來源：shared/data/products.py", y, color=self.SUBTEXT_COLOR, font=self.small_font)

        for index, product in enumerate(self._products):
            prefix = "→" if index == self._selected_index else "  "
            line = f"{prefix} {product.name} - ${product.price:,} | 庫存 {product.stock}"
            color = self.TEXT_COLOR if index != self._selected_index else (20, 70, 160)
            y = self.draw_line(line, y, color=color)

        self.draw_message(self._message, y + 10, success=self._message_success)

    # Internal helpers -------------------------------------------------

    def _add_selected_product(self) -> None:
        product = self._products[self._selected_index]
        try:
            self.cart.add_item(product.id, 1)
        except ValueError as exc:  # e.g. stock exceeded
            self._message = str(exc)
            self._message_success = False
        else:
            self._message = f"已加入 {product.name}"
            self._message_success = True
