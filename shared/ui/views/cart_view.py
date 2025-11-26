"""Cart overview view for the pygame demo UI."""

from __future__ import annotations
from pathlib import Path
import pygame
import math

# 導入基礎視圖類別
from shared.ui.views.base_view import BaseView


class CartView(BaseView):
    """
    購物車視圖：
    顯示購物車內的商品，使用卡片式網格佈局。
    
    [UI 更新] 參考 ProductListView 的卡片風格。
    [功能] 提供「減少數量」與「直接移除」按鈕。
    """
    # --- UI 常數設定 (與 ProductListView 保持一致以維持風格統一) ---
    COLS = 3                # 每行顯示 3 個商品
    CARD_WIDTH = 300        # 卡片寬度
    CARD_HEIGHT = 400       # 卡片高度
    GAP_X = 40              # 水平間距
    GAP_Y = 40              # 垂直間距
    
    IMG_SIZE = (220, 220)   # 圖片大小
    
    def __init__(self, screen: pygame.Surface, cart):
        """初始化購物車視圖。"""
        super().__init__(screen)
        self.cart = cart
        self._selected_index = 0
        self._message = ""
        self._message_success = False

        # 滾動偏移量
        self._scroll_y = 0
        self._target_scroll_y = 0

        # 初始化字體
        if not hasattr(self, 'font'):
            self.font = self._load_custom_font(24)
        if not hasattr(self, 'small_font'):
            self.small_font = self._load_custom_font(18)
            
        self.title_font = self._load_custom_font(28)
        self.qty_font = self._load_custom_font(22)

        # 圖片快取
        self._image_cache = {}
        # 注意：圖片會隨著購物車內容動態載入，這裡先不預載全部，改在 draw 時處理或動態檢查

    def _load_custom_font(self, size: int) -> pygame.font.Font:
        """載入字體 (Helper)。"""
        for candidate in BaseView.FONT_CANDIDATES:
            if candidate is None: break
            path = Path(candidate)
            if path.exists():
                try:
                    return pygame.font.Font(str(path), size)
                except OSError: continue
        return pygame.font.Font(None, size)

    def _get_product_image(self, product):
        """取得商品圖片，若快取無則載入。"""
        if product.id not in self._image_cache:
            assets_dir = Path("shared/assets/products")
            filename_base = product.name.split(' ')[0].lower()
            img_path = assets_dir / f"{filename_base}.jpg"
            
            try:
                if img_path.exists():
                    img = pygame.image.load(str(img_path)).convert_alpha()
                    self._image_cache[product.id] = pygame.transform.scale(img, self.IMG_SIZE)
                else:
                    self._image_cache[product.id] = None
            except Exception:
                self._image_cache[product.id] = None
                
        return self._image_cache[product.id]

    def handle_event(self, event: pygame.event.Event) -> None:
        """處理輸入事件。"""
        # 1. 滑鼠滾輪
        if event.type == pygame.MOUSEWHEEL:
            self._handle_scroll(event.y)
            return

        # 2. 滑鼠點擊
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
            return

        if event.type != pygame.KEYDOWN:
            return
        '''
        # 3. 鍵盤導航
        items = self.cart.items
        if not items: return

        cols = self.COLS
        total = len(items)

        if event.key == pygame.K_RIGHT:
            if self._selected_index + 1 < total: self._selected_index += 1
        elif event.key == pygame.K_LEFT:
            if self._selected_index - 1 >= 0: self._selected_index -= 1
        elif event.key == pygame.K_DOWN:
            if self._selected_index + cols < total: self._selected_index += cols
        elif event.key == pygame.K_UP:
            if self._selected_index - cols >= 0: self._selected_index -= cols
            
        # 鍵盤操作功能
        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
            self._remove_selected()
        elif event.key == pygame.K_MINUS:
            self._change_quantity(-1)
        elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
            self._change_quantity(1)

        if event.type == pygame.KEYDOWN:
            self._update_scroll_target()
        '''

    def _handle_scroll(self, dy: int):
        """處理滾動。"""
        scroll_step = 60
        self._target_scroll_y -= dy * scroll_step
        
        # 計算最大滾動高度
        screen_h = self.screen.get_height()
        items_count = len(self.cart.items)
        rows = math.ceil(items_count / self.COLS) if items_count > 0 else 0
        
        # 內容起始 Y (考慮到上方有文字資訊，起始位置較低)
        start_y = 220 
        total_h = start_y + rows * (self.CARD_HEIGHT + self.GAP_Y) + 100
        
        max_scroll = max(0, total_h - screen_h)
        self._target_scroll_y = max(0, min(self._target_scroll_y, max_scroll))

    def _update_scroll_target(self):
        """鍵盤移動時自動滾動。"""
        header_height = 220
        row = self._selected_index // self.COLS
        card_y = header_height + row * (self.CARD_HEIGHT + self.GAP_Y)
        
        screen_h = self.screen.get_height()
        view_top = self._target_scroll_y + header_height
        view_bot = self._target_scroll_y + screen_h - 100
        
        if card_y + self.CARD_HEIGHT > view_bot:
            self._target_scroll_y = (card_y + self.CARD_HEIGHT) - (screen_h - 100)
        elif card_y < view_top:
            self._target_scroll_y = card_y - header_height
            
        self._target_scroll_y = max(0, self._target_scroll_y)

    def _handle_mouse_click(self, pos):
        """處理滑鼠點擊卡片與按鈕。"""
        items = self.cart.items
        if not items: return

        start_x = 50
        start_y = 220 - self._scroll_y  # 網格起始 Y 座標 (避開上方文字)

        for index, item in enumerate(items):
            row = index // self.COLS
            col = index % self.COLS
            
            x = start_x + col * (self.CARD_WIDTH + self.GAP_X)
            y = start_y + row * (self.CARD_HEIGHT + self.GAP_Y)
            
            card_rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
            
            if card_rect.collidepoint(pos):
                self._selected_index = index
                
                # --- 檢查按鈕點擊 ---
                bottom_y = y + self.CARD_HEIGHT - 60
                
                # 按鈕尺寸
                btn_w = 60
                btn_h = 36
                
                # 1. 刪除按鈕 (最右邊)
                del_btn_x = x + self.CARD_WIDTH - btn_w - 20
                del_btn_rect = pygame.Rect(del_btn_x, bottom_y + 5, btn_w, btn_h)
                
                # 2. 減少按鈕 (刪除按鈕左邊)
                dec_btn_x = del_btn_x - btn_w - 10
                dec_btn_rect = pygame.Rect(dec_btn_x, bottom_y + 5, btn_w, btn_h)
                
                if del_btn_rect.collidepoint(pos):
                    self._remove_selected()
                elif dec_btn_rect.collidepoint(pos):
                    self._change_quantity(-1)
                
                break

    def update(self) -> None:
        """更新邏輯。"""
        items = self.cart.items
        if items:
            self._selected_index = min(self._selected_index, len(items) - 1)
        else:
            self._selected_index = 0
            
        # 滾動動畫
        diff = self._target_scroll_y - self._scroll_y
        if abs(diff) > 1:
            self._scroll_y += diff * 0.1
        else:
            self._scroll_y = self._target_scroll_y

    def draw(self) -> None:
        """繪製畫面。"""
        # 1. 繪製上方統計資訊 (固定位置)
        y = 40
        title = self.title_font.render("購物車清單", True, (0,0,0))
        self.screen.blit(title, (50, y))
        
        # 統計資訊區塊
        info_x = 50
        info_y = y + 50
        
        # 使用 BaseView 的 draw_line 邏輯或手動繪製
        # 這裡手動繪製以控制排版
        total_info = [
            f"小計：${self.cart.subtotal:,}",
            f"折扣：-${self.cart.discount_amount:,}",
            f"應付金額：${self.cart.final_amount:,}"
        ]
        
        for i, text in enumerate(total_info):
            color = (200, 50, 50) if "應付" in text else (80, 80, 80)
            surf = self.font.render(text, True, color)
            self.screen.blit(surf, (info_x, info_y + i * 30))

        # 2. 繪製商品網格
        items = self.cart.items
        if not items:
            empty_msg = self.font.render("購物車目前是空的。", True, (150, 150, 150))
            self.screen.blit(empty_msg, (50, 220))
        else:
            start_x = 50
            start_y = 220 - self._scroll_y
            
            for index, item in enumerate(items):
                row = index // self.COLS
                col = index % self.COLS
                
                x = start_x + col * (self.CARD_WIDTH + self.GAP_X)
                y = start_y + row * (self.CARD_HEIGHT + self.GAP_Y)
                
                # 畫面外不繪製
                if y + self.CARD_HEIGHT < 0 or y > self.screen.get_height():
                    continue
                    
                self._draw_cart_card(x, y, item, index == self._selected_index)

        # 訊息 Toast
        if self._message:
            self.draw_message(self._message, 0, success=self._message_success) # Y=0 會被 BaseView 處理位置

    def _draw_cart_card(self, x, y, item, is_selected):
        """繪製單張購物車卡片。"""
        rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        product = item.product
        
        # 背景
        pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=18)
        
        # 邊框
        if is_selected:
            pygame.draw.rect(self.screen, (0, 113, 227), rect, width=3, border_radius=18)
        else:
            pygame.draw.rect(self.screen, (230, 230, 230), rect, width=1, border_radius=18)

        # 1. 名稱
        name_surf = self.font.render(product.name, True, (0, 0, 0))
        self.screen.blit(name_surf, (x + 24, y + 24))

        # 2. 右上角數量顯示 (數量 x 單價)
        qty_text = f"x {item.quantity}"
        qty_surf = self.qty_font.render(qty_text, True, (0, 0, 0))
        # 畫在右上角
        qty_rect = qty_surf.get_rect(topright=(x + self.CARD_WIDTH - 24, y + 24))
        # 加個小框框
        box_rect = qty_rect.inflate(16, 10)
        pygame.draw.rect(self.screen, (245, 245, 245), box_rect, border_radius=10)
        self.screen.blit(qty_surf, qty_rect)

        # 3. 圖片
        img = self._get_product_image(product)
        if img:
            img_x = x + (self.CARD_WIDTH - self.IMG_SIZE[0]) // 2
            img_y = y + 80
            self.screen.blit(img, (img_x, img_y))

        # 4. 底部資訊與按鈕
        bottom_y = y + self.CARD_HEIGHT - 60
        
        # 小計金額 (左下)
        subtotal_text = f"小計 ${item.subtotal:,}"
        price_surf = self.small_font.render(subtotal_text, True, (50, 50, 50))
        self.screen.blit(price_surf, (x + 24, bottom_y + 12))

        # --- 按鈕區 (右下) ---
        btn_w = 60
        btn_h = 36
        
        # 刪除按鈕 (最右) - 紅色系
        del_btn_x = x + self.CARD_WIDTH - btn_w - 20
        del_rect = pygame.Rect(del_btn_x, bottom_y + 5, btn_w, btn_h)
        
        del_color = (220, 50, 50) if is_selected else (240, 200, 200)
        del_text_color = (255, 255, 255) if is_selected else (150, 50, 50)
        
        pygame.draw.rect(self.screen, del_color, del_rect, border_radius=18)
        del_surf = self.small_font.render("移除", True, del_text_color)
        del_text_rect = del_surf.get_rect(center=del_rect.center)
        self.screen.blit(del_surf, del_text_rect)

        # 減少按鈕 (左邊) - 灰色系
        dec_btn_x = del_btn_x - btn_w - 10
        dec_rect = pygame.Rect(dec_btn_x, bottom_y + 5, btn_w, btn_h)
        
        dec_color = (230, 230, 230) if is_selected else (240, 240, 240)
        dec_text_color = (50, 50, 50)
        
        pygame.draw.rect(self.screen, dec_color, dec_rect, border_radius=18)
        dec_surf = self.small_font.render("減少", True, dec_text_color)
        dec_text_rect = dec_surf.get_rect(center=dec_rect.center)
        self.screen.blit(dec_surf, dec_text_rect)

    # 邏輯操作 Helper
    def _change_quantity(self, delta: int) -> None:
        items = self.cart.items
        if not items: return
        
        item = items[self._selected_index]
        new_quantity = item.quantity + delta
        try:
            if new_quantity <= 0:
                self.cart.remove_item(item.product.id)
                # 移除後調整索引，避免越界
                self._selected_index = min(self._selected_index, len(self.cart.items) - 1)
            else:
                self.cart.update_quantity(item.product.id, new_quantity)
            self._message = ""
        except ValueError as exc:
            self._message = str(exc)

    def _remove_selected(self) -> None:
        items = self.cart.items
        if not items: return
        
        item = items[self._selected_index]
        self.cart.remove_item(item.product.id)
        self._message = f"已移除 {item.product.name}"
        self._message_success = True
        # 移除後調整索引
        self._selected_index = min(self._selected_index, len(self.cart.items) - 1)