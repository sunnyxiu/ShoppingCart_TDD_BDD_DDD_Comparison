"""
主視窗類別（共用）
所有版本使用相同的 UI 介面
"""

from pathlib import Path

import pygame
from shared.ui.views.product_list_view import ProductListView
from shared.ui.views.cart_view import CartView
from shared.ui.views.checkout_view import CheckoutView
from shared.ui.views.base_view import BaseView

class MainWindow:
    def __init__(self, cart, width=1200, height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("電商購物車系統")
        
        self.cart = cart
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 初始化各個視圖
        self.product_view = ProductListView(self.screen, self.cart)
        self.cart_view = CartView(self.screen, self.cart)
        self.checkout_view = CheckoutView(self.screen, self.cart)
        
        self.current_view = "product_list"
        self.nav_font = self._load_shared_font(22)
        self.nav_hint_font = self._load_shared_font(18)
        self._nav_items = [
            ("1", "商品清單", "product_list"),
            ("2", "購物車", "cart"),
            ("3", "結帳 / 折扣", "checkout"),
        ]
        self._view_order = [item[2] for item in self._nav_items]
    
    def run(self):
        """主迴圈"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
    
    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.KEYDOWN and self._handle_global_shortcuts(event):
                continue

            # 分派事件到當前視圖
            if self.current_view == "product_list":
                self.product_view.handle_event(event)
            elif self.current_view == "cart":
                self.cart_view.handle_event(event)
            elif self.current_view == "checkout":
                self.checkout_view.handle_event(event)
    
    def update(self):
        """更新邏輯"""
        if self.current_view == "product_list":
            self.product_view.update()
        elif self.current_view == "cart":
            self.cart_view.update()
        elif self.current_view == "checkout":
            self.checkout_view.update()
    
    def draw(self):
        """繪製畫面"""
        self.screen.fill((255, 255, 255))
        
        if self.current_view == "product_list":
            self.product_view.draw()
        elif self.current_view == "cart":
            self.cart_view.draw()
        elif self.current_view == "checkout":
            self.checkout_view.draw()
        
        self._draw_navigation_bar()
        pygame.display.flip()
    
    def switch_view(self, view_name):
        """切換視圖"""
        self.current_view = view_name

    def _draw_navigation_bar(self):
        """Draws the view-switch instructions at the bottom of the window."""
        y = self.screen.get_height() - 70
        x = 30
        for key, label, view in self._nav_items:
            text = f"{key}. {label}"
            active = view == self.current_view
            fg = (255, 255, 255) if active else (60, 60, 60)
            bg = (30, 120, 210) if active else (235, 235, 235)
            border = 0 if active else 1
            surface = self.nav_font.render(text, True, fg)
            rect = surface.get_rect()
            rect.topleft = (x, y)
            padding = rect.inflate(24, 16)
            pygame.draw.rect(self.screen, bg, padding, border_radius=8)
            if border:
                pygame.draw.rect(self.screen, (200, 200, 200), padding, width=border, border_radius=8)
            self.screen.blit(surface, rect)
            x += padding.width + 10

        hint = "1/2/3 指定視圖；Tab 或 ←/→ 切換；Esc 離開"
        hint_surface = self.nav_hint_font.render(hint, True, (90, 90, 90))
        self.screen.blit(hint_surface, (30, y + 44))

    def _switch_relative(self, step: int) -> None:
        idx = self._view_order.index(self.current_view)
        idx = (idx + step) % len(self._view_order)
        self.current_view = self._view_order[idx]

    def _load_shared_font(self, size: int) -> pygame.font.Font:
        for candidate in BaseView.FONT_CANDIDATES:
            if candidate is None:
                break
            path = Path(candidate)
            if path.exists():
                try:
                    return pygame.font.Font(str(path), size)
                except OSError:
                    continue
        return pygame.font.Font(None, size)

    def _handle_global_shortcuts(self, event: pygame.event.Event) -> bool:
        if event.key == pygame.K_ESCAPE:
            self.running = False
            return True
        if event.key == pygame.K_TAB:
            reverse = bool(event.mod & pygame.KMOD_SHIFT)
            self._switch_relative(-1 if reverse else 1)
            return True
        if event.key == pygame.K_LEFT:
            self._switch_relative(-1)
            return True
        if event.key == pygame.K_RIGHT:
            self._switch_relative(1)
            return True

        shortcuts = {
            pygame.K_1: "product_list",
            pygame.K_KP1: "product_list",
            pygame.K_2: "cart",
            pygame.K_KP2: "cart",
            pygame.K_3: "checkout",
            pygame.K_KP3: "checkout",
        }
        target = shortcuts.get(event.key)
        if target:
            self.switch_view(target)
            return True
        return False
