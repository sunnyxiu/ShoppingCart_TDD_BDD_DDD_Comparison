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
        self._views = ["product_list", "cart", "checkout"]
    
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self._switch_relative(-1)
                elif event.key == pygame.K_RIGHT:
                    self._switch_relative(1)
            
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
        nav_items = [
            ("←/→", "切換視圖"),
            ("Esc", "離開"),
        ]
        text = "   |   ".join(
            f"[{key}] {label}"
            for key, label in nav_items
        )
        surface = self.nav_font.render(text, True, (60, 60, 60))
        rect = surface.get_rect()
        rect.left = 20
        rect.bottom = self.screen.get_height() - 10
        pygame.draw.rect(self.screen, (235, 235, 235), (
            0,
            rect.top - 6,
            self.screen.get_width(),
            rect.height + 12,
        ))
        self.screen.blit(surface, rect)
        hint = "←/→ 切換視圖；Esc 離開"
        hint_surface = self.nav_hint_font.render(hint, True, (100, 100, 100))
        self.screen.blit(hint_surface, (20, rect.top - 24))

    def _switch_relative(self, step: int) -> None:
        idx = self._views.index(self.current_view)
        idx = (idx + step) % len(self._views)
        self.current_view = self._views[idx]

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
