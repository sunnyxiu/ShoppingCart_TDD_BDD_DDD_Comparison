"""
主視窗類別（共用）
所有版本使用相同的 UI 介面
"""

import pygame
from .views.product_list_view import ProductListView
from .views.cart_view import CartView
from .views.checkout_view import CheckoutView

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
        
        pygame.display.flip()
    
    def switch_view(self, view_name):
        """切換視圖"""
        self.current_view = view_name
