"""Checkout/summary view for the pygame demo UI."""

from __future__ import annotations

import pygame

from shared.ui.views.base_view import BaseView


class CheckoutView(BaseView):
    def __init__(self, screen: pygame.Surface, cart):
        super().__init__(screen)
        self.cart = cart
        self._discount_input = ""
        self._message = ""
        self._message_success = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_BACKSPACE:
            self._discount_input = self._discount_input[:-1]
        elif event.key == pygame.K_RETURN:
            self._apply_discount_input()
        elif event.key == pygame.K_ESCAPE:
            self._discount_input = ""
        elif event.key == pygame.K_c:
            self.cart.clear()
            self._message = "購物車已清空"
            self._message_success = True
        else:
            char = event.unicode.upper()
            if char.isalnum() and len(self._discount_input) < 12:
                self._discount_input += char

    def update(self) -> None:  # noqa: D401 - no-op but keeps interface consistent
        """No periodic updates required for checkout view."""

    def draw(self) -> None:
        y = self.draw_title("結帳 / 折扣碼")
        y = self.draw_line(f"商品數量：{self._total_items()}", y)
        y = self.draw_line(f"小計：${self.cart.subtotal:,}", y)
        y = self.draw_line(f"折扣：-${self.cart.discount_amount:,}", y)
        y = self.draw_line(f"應付金額：${self.cart.final_amount:,}", y)

        y += 20
        y = self.draw_line("輸入折扣碼（Enter 套用, Backspace 刪除, C 清空購物車）", y, color=self.SUBTEXT_COLOR)
        input_box = f"> {self._discount_input or '----'}"
        y = self.draw_line(input_box, y, color=(30, 120, 180))

        self.draw_message(self._message, y + 10, success=self._message_success)

    # Internal helpers -------------------------------------------------

    def _apply_discount_input(self) -> None:
        code = self._discount_input.strip()
        if not code:
            self._message = "請輸入折扣碼"
            self._message_success = False
            return

        try:
            success, message = self.cart.apply_discount(code)
        except ValueError as exc:
            self._message = str(exc)
            self._message_success = False
        else:
            self._message = message
            self._message_success = success
            if success:
                self._discount_input = ""

    def _total_items(self) -> int:
        return sum(item.quantity for item in self.cart.items)
