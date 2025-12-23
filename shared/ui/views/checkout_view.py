"""Checkout view for the pygame demo UI."""

from __future__ import annotations
from pathlib import Path
import pygame
import math

# 導入基礎視圖類別
from shared.ui.views.base_view import BaseView


class CheckoutView(BaseView):
    """
    結帳視圖：
    顯示最終結帳金額、折扣碼輸入與商品明細。
    
    [UI 更新]
    1. 頂部固定顯示資訊與輸入框。
    2. 下方列表區域支援滾動，且右側有滑動條 (Scrollbar)。
    3. 商品以白色長條卡片顯示。
    4. 新增「清空購物車」按鈕。
    """
    # --- UI 常數設定 ---
    # 區域高度
    HEADER_HEIGHT = 300     # 頂部固定區域高度 (標題 + 統計 + 輸入框)
    FOOTER_HEIGHT = 80      # 底部按鈕區域高度
    
    # 列表項目設定
    ITEM_ROW_HEIGHT = 100   # 每個商品行的高度
    ITEM_GAP = 15           # 商品行之間的間距
    LIST_PADDING_X = 50     # 列表左右邊距
    
    # 輸入框設定
    INPUT_BOX_WIDTH = 400
    INPUT_BOX_HEIGHT = 46

    def __init__(self, screen: pygame.Surface, cart):
        """初始化結帳視圖。"""
        super().__init__(screen)
        self.cart = cart
        
        # --- 輸入框狀態 ---
        self.input_text = ""
        self.input_active = False # 是否正在輸入
        self.discount_message = "" # 折扣回饋訊息
        self.discount_success = False

        # --- 滾動狀態 ---
        self._scroll_y = 0
        self._target_scroll_y = 0
        
        # --- UI 元件區域 (用於點擊偵測) ---
        self.input_rect = pygame.Rect(0, 0, 0, 0) 
        self.clear_btn_rect = pygame.Rect(0, 0, 0, 0)

        # 初始化字體
        if not hasattr(self, 'font'):
            self.font = self._load_custom_font(24)
        if not hasattr(self, 'small_font'):
            self.small_font = self._load_custom_font(18)
        
        self.title_font = self._load_custom_font(32)
        self.info_font = self._load_custom_font(22)

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

    def handle_event(self, event: pygame.event.Event) -> None:
        """處理輸入事件。"""
        # 1. 滑鼠滾輪 (滾動列表)
        if event.type == pygame.MOUSEWHEEL:
            self._handle_scroll(event.y)
            return

        # 2. 滑鼠點擊
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
            return

        # 3. 鍵盤輸入 (僅在輸入框激活時處理文字，或全域快捷鍵)
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    self._apply_discount()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    # 限制長度與過濾特殊鍵
                    if len(self.input_text) < 20 and event.unicode.isprintable():
                        self.input_text += event.unicode
            else:
                # 非輸入狀態下的滾動支援 (選用)
                if event.key == pygame.K_UP:
                    self._handle_scroll(1)
                elif event.key == pygame.K_DOWN:
                    self._handle_scroll(-1)

    def _handle_scroll(self, dy: int):
        """處理滾動邏輯。"""
        scroll_step = 50
        self._target_scroll_y -= dy * scroll_step
        
        # 計算內容總高度
        items_count = len(self.cart.items)
        content_height = items_count * (self.ITEM_ROW_HEIGHT + self.ITEM_GAP) + self.ITEM_GAP
        
        # 可視區域高度 (扣掉 Header 和 Footer)
        screen_h = self.screen.get_height()
        view_h = screen_h - self.HEADER_HEIGHT - 60 # 60 是底部留白
        
        max_scroll = max(0, content_height - view_h)
        self._target_scroll_y = max(0, min(self._target_scroll_y, max_scroll))

    def _handle_mouse_click(self, pos):
        """處理點擊事件：輸入框激活、按鈕觸發。"""
        # 1. 檢查輸入框
        if self.input_rect.collidepoint(pos):
            self.input_active = True
        else:
            self.input_active = False # 點擊其他地方取消聚焦
            
        # 2. 檢查清空購物車按鈕
        if self.clear_btn_rect.collidepoint(pos):
            self._clear_cart()

    def _apply_discount(self):
        """套用折扣碼邏輯。"""
        code = self.input_text.strip()
        if not code: return
        
        # 呼叫購物車邏輯 (假設 cart 有 apply_discount 方法，或模擬之)
        # 這裡模擬邏輯，實際應呼叫 self.cart.apply_discount(code)
        try:
            if hasattr(self.cart, 'apply_discount'):
                self.cart.apply_discount(code)
                self.discount_message = f"折扣碼 '{code}' 套用成功！"
                self.discount_success = True
            else:
                # 若購物車物件沒這個方法，手動模擬 (僅供 Demo)
                if code == "SAVE10": # 範例代碼
                    self.discount_message = "折扣碼 SAVE10 套用成功！"
                    self.discount_success = True
                else:
                    raise ValueError("無效的折扣碼")
        except ValueError as e:
            self.discount_message = str(e)
            self.discount_success = False
            
        # 清空輸入框 (可選)
        # self.input_text = ""

    def _clear_cart(self):
        """清空購物車。"""
        if hasattr(self.cart, 'clear'):
            self.cart.clear()
        else:
            # Fallback
            self.cart.items = [] 
        
        self.discount_message = "購物車已清空"
        self.discount_success = True
        # 重置滾動
        self._target_scroll_y = 0

    def update(self) -> None:
        """更新動畫與狀態。"""
        # 平滑滾動
        diff = self._target_scroll_y - self._scroll_y
        if abs(diff) > 1:
            self._scroll_y += diff * 0.2
        else:
            self._scroll_y = self._target_scroll_y

    def draw(self) -> None:
        """繪製結帳畫面。"""
        # 1. 繪製頂部固定區域 (Header)
        self._draw_header()
        
        # 2. 繪製滾動列表 (Items)
        self._draw_item_list()
        
        # 3. 繪製捲軸 (Scrollbar)
        self._draw_scrollbar()
        
        # 4. 繪製底部按鈕 (清空購物車)
        self._draw_footer_buttons()

    def _draw_header(self):
        """繪製標題、統計資訊與輸入框。"""
        start_x = 50
        y = 40
        
        # 標題
        title = self.title_font.render("結帳", True, (0, 0, 0))
        self.screen.blit(title, (start_x, y))
        
        # 統計資訊 (左側)
        y += 50
        info_lines = [
            f"商品數量：{len(self.cart.items)}",
            f"小計：${self.cart.subtotal:,}",
            f"折扣：-${self.cart.discount_amount:,}",
            f"應付金額：${self.cart.final_amount:,}"
        ]
        
        for i, line in enumerate(info_lines):
            color = (20, 20, 20) if i < 3 else (200, 50, 50) # 最後一行金額紅色
            surf = self.info_font.render(line, True, color)
            self.screen.blit(surf, (start_x, y + i * 30))
            
        # --- 折扣碼輸入框區域 ---
        # 提示文字
        input_label_y = y + 130
        label_surf = self.small_font.render("輸入折扣碼 (點擊輸入, Enter 套用)", True, (100, 100, 100))
        self.screen.blit(label_surf, (start_x, input_label_y))
        
        # 輸入框本體
        box_y = input_label_y + 25
        self.input_rect = pygame.Rect(start_x, box_y, self.INPUT_BOX_WIDTH, self.INPUT_BOX_HEIGHT)
        
        # 背景色
        bg_color = (255, 255, 255)
        pygame.draw.rect(self.screen, bg_color, self.input_rect, border_radius=8)
        
        # 邊框 (激活時藍色，否則灰色)
        border_color = (0, 113, 227) if self.input_active else (200, 200, 200)
        border_width = 2 if self.input_active else 1
        pygame.draw.rect(self.screen, border_color, self.input_rect, width=border_width, border_radius=8)
        
        # 輸入文字
        text_surf = self.font.render(self.input_text, True, (0, 0, 0))
        # 垂直置中
        text_rect = text_surf.get_rect(midleft=(start_x + 10, self.input_rect.centery))
        self.screen.blit(text_surf, text_rect)
        
        # 光標 (激活時閃爍)
        if self.input_active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = text_rect.right + 2
            pygame.draw.line(self.screen, (0, 0, 0), (cursor_x, text_rect.top + 5), (cursor_x, text_rect.bottom - 5), 2)

        # 折扣訊息回饋
        if self.discount_message:
            msg_color = (0, 150, 0) if self.discount_success else (200, 50, 50)
            msg_surf = self.small_font.render(self.discount_message, True, msg_color)
            self.screen.blit(msg_surf, (start_x + self.INPUT_BOX_WIDTH + 20, box_y + 12))

    def _draw_item_list(self):
        """繪製可滾動的商品列表區域。"""
        # 定義列表顯示區域 (Clip Area) 防止繪製到 Header 上
        list_start_y = self.HEADER_HEIGHT
        screen_w, screen_h = self.screen.get_size()
        view_h = screen_h - list_start_y - 60 # 底部留一點空間
        
        # 設定裁切區域 (Clipping)
        clip_rect = pygame.Rect(0, list_start_y, screen_w, view_h)
        self.screen.set_clip(clip_rect)
        
        start_x = self.LIST_PADDING_X
        # 根據滾動量計算起始 Y
        current_y = list_start_y + 10 - self._scroll_y 
        
        items = self.cart.items
        if not items:
            empty_text = self.font.render("目前沒有商品", True, (150, 150, 150))
            self.screen.blit(empty_text, (start_x, list_start_y + 50))
        else:
            row_width = screen_w - (self.LIST_PADDING_X * 2) - 30 # 30 是留給捲軸的空間
            
            for item in items:
                # 簡單的可見性檢查 (Culling)
                if current_y + self.ITEM_ROW_HEIGHT < list_start_y:
                    current_y += self.ITEM_ROW_HEIGHT + self.ITEM_GAP
                    continue
                if current_y > screen_h:
                    break
                
                # 繪製商品行 (白色圓角長方形)
                row_rect = pygame.Rect(start_x, current_y, row_width, self.ITEM_ROW_HEIGHT)
                pygame.draw.rect(self.screen, (255, 255, 255), row_rect, border_radius=12)
                
                # 商品資訊文字
                # 1. 名稱 (左)
                name_surf = self.font.render(item.product.name, True, (0, 0, 0))
                self.screen.blit(name_surf, (start_x + 20, current_y + 35))
                
                # 2. 數量與單價 (中)
                detail_text = f"數量: {item.quantity}  x  ${item.product.price:,}"
                detail_surf = self.small_font.render(detail_text, True, (100, 100, 100))
                # 放在名稱右側或是固定位置
                self.screen.blit(detail_surf, (start_x + 300, current_y + 40))
                
                # 3. 小計 (右)
                subtotal_text = f"${item.subtotal:,}"
                sub_surf = self.font.render(subtotal_text, True, (0, 0, 0))
                sub_rect = sub_surf.get_rect(midright=(start_x + row_width - 30, current_y + 50))
                self.screen.blit(sub_surf, sub_rect)
                
                current_y += self.ITEM_ROW_HEIGHT + self.ITEM_GAP

        # 解除裁切
        self.screen.set_clip(None)

    def _draw_scrollbar(self):
        """在右側繪製滑動條。"""
        screen_w, screen_h = self.screen.get_size()
        bar_width = 12
        bar_x = screen_w - bar_width - 10
        
        # 捲軸區域 (Track)
        track_y = self.HEADER_HEIGHT
        track_h = screen_h - self.HEADER_HEIGHT - 60
        
        # 計算內容高度
        items_count = len(self.cart.items)
        content_h = items_count * (self.ITEM_ROW_HEIGHT + self.ITEM_GAP) + self.ITEM_GAP
        
        # 如果內容小於視窗，不需要捲軸
        if content_h <= track_h:
            return
            
        # 繪製軌道 (灰色細線)
        pygame.draw.rect(self.screen, (230, 230, 230), (bar_x, track_y, bar_width, track_h), border_radius=6)
        
        # 計算滑塊 (Thumb) 高度與位置
        view_ratio = track_h / content_h
        thumb_h = max(30, track_h * view_ratio) # 最小高度 30
        
        scroll_ratio = self._scroll_y / (content_h - track_h)
        # 限制 ratio 0~1
        scroll_ratio = max(0, min(1, scroll_ratio))
        
        thumb_y = track_y + (track_h - thumb_h) * scroll_ratio
        
        # 繪製滑塊 (深灰色)
        pygame.draw.rect(self.screen, (160, 160, 160), (bar_x, thumb_y, bar_width, thumb_h), border_radius=6)

    def _draw_footer_buttons(self):
        """繪製底部的操作按鈕 (例如清空購物車)。"""
        screen_w, screen_h = self.screen.get_size()
        
        # 清空購物車按鈕 (右下角)
        btn_w, btn_h = 140, 44
        btn_x = screen_w - btn_w - 80
        btn_y = 250 # 位於導航欄上方
        
        self.clear_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        
        # 按鈕外觀 (紅色警示風格)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.clear_btn_rect.collidepoint(mouse_pos)
        
        bg_color = (200, 50, 50) if not is_hover else (220, 70, 70)
        pygame.draw.rect(self.screen, bg_color, self.clear_btn_rect, border_radius=22)
        
        # 按鈕文字
        text = self.font.render("清空購物車", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.clear_btn_rect.center)
        self.screen.blit(text, text_rect)