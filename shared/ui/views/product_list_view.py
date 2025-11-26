"""Product list view for the pygame demo UI."""

from __future__ import annotations
from pathlib import Path  # 導入 Path 用於處理檔案路徑
import pygame
import math # 用於計算網格行數

# 導入商品資料：這是 UI 繪製商品清單的數據來源
from shared.data.products import PRODUCTS
# 導入基礎視圖類別：提供基本的繪圖工具和字體載入功能
from shared.ui.views.base_view import BaseView


class ProductListView(BaseView):
    """
    商品清單視圖：
    負責顯示商品列表（包含圖片）、處理鍵盤選擇，並將選中的商品加入購物車。
    
    [UI 更新] 參考現代電商風格，改為卡片式網格佈局。
    [更新] 支援滑鼠點擊選取與購買，右下角按鈕改為圓角長方形。
    [新功能] 卡片右上角顯示「購物車數量 / 總庫存」即時狀態。
    [新功能] 支援滑鼠滾輪滾動列表。
    """
    # --- UI 常數設定 ---
    # 網格設定
    COLS = 3                # 每行顯示 3 個商品
    CARD_WIDTH = 300        # 卡片寬度
    CARD_HEIGHT = 400       # 卡片高度
    GAP_X = 40             # 水平間距
    GAP_Y = 40             # 垂直間距
    
    # 內容設定
    IMG_SIZE = (220, 220)   # 圖片放大顯示
    SCROLL_SPEED = 20       # 滾動平滑度

    def __init__(self, screen: pygame.Surface, cart):
        """初始化商品列表視圖，並預先載入商品圖片。"""
        super().__init__(screen)  # 呼叫 BaseView 的初始化，設定 screen 和字體
        self.cart = cart         # 接收購物車實例 (TDD/BDD/DDD 核心邏輯)
        self._products = PRODUCTS # 載入所有商品數據
        self._selected_index = 0  # 當前選中商品的索引 (預設為第一個)
        self._message = ""        # 顯示給用戶的狀態訊息 (例如：成功加入/庫存不足)
        self._message_success = False # 訊息是否為成功狀態 (用於決定顏色)
        
        # 滾動偏移量 (Y軸)
        self._scroll_y = 0
        self._target_scroll_y = 0

        # 修正：確保 self.font 存在 (如果 BaseView 未定義或名稱不同)
        if not hasattr(self, 'font'):
            self.font = self._load_custom_font(24)
            
        # 修正：確保 self.small_font 存在，用於顯示第二行資訊
        if not hasattr(self, 'small_font'):
            self.small_font = self._load_custom_font(18)
            
        # 標題字體 (稍微大一點)
        self.title_font = self._load_custom_font(28)
        
        # 數量顯示字體 (稍大一點，清楚顯示 5/10)
        self.qty_font = self._load_custom_font(22)

        # --- 圖片載入邏輯 ---
        self._image_cache = {} # 用於儲存已載入的 Pygame Surface 圖片物件
        self._load_product_images()

    def _load_custom_font(self, size: int) -> pygame.font.Font:
        """嘗試從 BaseView 定義的候選路徑中載入字體檔案。"""
        for candidate in BaseView.FONT_CANDIDATES:
            if candidate is None:
                break
            path = Path(candidate)
            if path.exists(): # 檢查檔案是否存在
                try:
                    return pygame.font.Font(str(path), size) # 載入字體檔案
                except OSError:
                    continue
        return pygame.font.Font(None, size) # 最終 fallback

    def _load_product_images(self):
        """輔助方法：從 assets 目錄預先載入並縮放所有商品的圖片。"""
        # 設定圖片資料夾路徑 (相對於專案根目錄)
        assets_dir = Path("shared/assets/products")
        
        for product in self._products:
            # 根據商品名稱推斷檔案名稱。例如 "iPhone 15 Pro" -> "iphone.jpg"
            # 這裡簡單取名稱的第一個單字並轉小寫作為檔名基礎
            filename_base = product.name.split(' ')[0].lower()
            img_path = assets_dir / f"{filename_base}.jpg"

            try:
                if img_path.exists():
                    # 載入圖片並轉換格式以優化效能 (convert_alpha 處理透明度，雖然 jpg 沒有)
                    img_surface = pygame.image.load(str(img_path)).convert_alpha()
                    # 縮放圖片到卡片適合的大小
                    scaled_surface = pygame.transform.scale(img_surface, self.IMG_SIZE)
                    # 將處理好的圖片存入快取字典，鍵值為商品 ID
                    self._image_cache[product.id] = scaled_surface
                else:
                    self._image_cache[product.id] = None
            except pygame.error as e:
                 print(f"Error loading image {img_path}: {e}")
                 self._image_cache[product.id] = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """處理 Pygame 事件，主要負責鍵盤輸入 (支援網格導航)。"""
        # 處理滑鼠滾輪
        if event.type == pygame.MOUSEWHEEL:
            self._handle_scroll(event.y)
            return

        # 新增滑鼠點擊處理
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
            return
        

    def _handle_scroll(self, dy: int):
        """處理滾輪事件更新目標滾動位置。"""
        # 滾動速度
        scroll_step = 60 
        # event.y > 0 為向上滾，代表頁面要往上看，所以 scroll_y 應減少
        self._target_scroll_y -= dy * scroll_step
        
        # 計算最大滾動範圍
        screen_h = self.screen.get_height()
        rows = math.ceil(len(self._products) / self.COLS)
        # 140 is start_y, 100 is bottom margin
        total_content_height = 140 + rows * (self.CARD_HEIGHT + self.GAP_Y) + 100
        max_scroll = max(0, total_content_height - screen_h)
        
        # 限制範圍
        self._target_scroll_y = max(0, min(self._target_scroll_y, max_scroll))

    def _handle_mouse_click(self, pos: tuple[int, int]):
        """處理滑鼠點擊：選取卡片或點擊購買按鈕。"""
        # 重建卡片位置邏輯以檢測點擊
        start_x = 50
        start_y = 140 - self._scroll_y
        
        for index, product in enumerate(self._products):
            row = index // self.COLS
            col = index % self.COLS
            
            x = start_x + col * (self.CARD_WIDTH + self.GAP_X)
            y = start_y + row * (self.CARD_HEIGHT + self.GAP_Y)
            
            # 卡片區域
            card_rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
            
            if card_rect.collidepoint(pos):
                self._selected_index = index
                # 點擊時不強制滾動，讓使用者自由瀏覽
                # self._update_scroll_target() 
                
                # 進一步檢查是否點擊了右下角的購買按鈕 (圓角長方形)
                bottom_y = y + self.CARD_HEIGHT - 60
                
                # 定義按鈕尺寸和位置 (需與 draw 對應)
                btn_width = 70
                btn_height = 36
                btn_x = x + self.CARD_WIDTH - btn_width - 20
                btn_y = bottom_y + 5
                
                btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
                
                if btn_rect.collidepoint(pos):
                    self._add_selected_product()
                
                break # 找到點擊的卡片後停止迴圈

    def _update_scroll_target(self):
        """計算滾動位置，讓選中的卡片保持在可見區域。"""
        # 頂部預留空間 (標題等)
        header_height = 100 
        # 底部預留空間
        bottom_margin = 100
        
        row = self._selected_index // self.COLS
        # 卡片頂部 Y 座標
        card_y = header_height + row * (self.CARD_HEIGHT + self.GAP_Y)
        
        # 簡單的跟隨邏輯：如果卡片太低，就往下滾；太高就往上滾
        screen_height = self.screen.get_height()
        
        # 理想的顯示區域 (Viewport)
        viewport_top = self._target_scroll_y + header_height
        viewport_bottom = self._target_scroll_y + screen_height - bottom_margin
        
        if card_y + self.CARD_HEIGHT > viewport_bottom:
            # 卡片在視窗下方，往下滾
            self._target_scroll_y = (card_y + self.CARD_HEIGHT) - (screen_height - bottom_margin)
        elif card_y < viewport_top:
            # 卡片在視窗上方，往上滾
            self._target_scroll_y = card_y - header_height
            
        # 限制滾動範圍 (不要滾過頭)
        self._target_scroll_y = max(0, self._target_scroll_y)

    def _get_cart_quantity(self, product_id: str) -> int:
        """Helper: 從購物車中取得特定商品的當前數量。"""
        if not hasattr(self.cart, 'items'):
            return 0
        
        # 遍歷購物車項目，尋找符合的 product_id
        for item in self.cart.items:
            # 兼容常見的 CartItem 結構 (item.product.id)
            if hasattr(item, 'product') and hasattr(item.product, 'id') and item.product.id == product_id:
                return item.quantity
            # 兼容簡單結構 (直接 item.id)
            elif hasattr(item, 'id') and item.id == product_id:
                return item.quantity
        return 0

    def update(self) -> None:
        """每幀更新邏輯。"""
        # 防止索引越界
        self._selected_index = min(self._selected_index, len(self._products) - 1)
        
        # 平滑滾動效果
        diff = self._target_scroll_y - self._scroll_y
        if abs(diff) > 1:
            self._scroll_y += diff * 0.1
        else:
            self._scroll_y = self._target_scroll_y

    def draw(self) -> None:
        """繪製商品列表畫面 (網格卡片風格)。"""
        # 1. 繪製標題 (固定在頂部，不隨滾動移動)
        title_y = 40
        title_surf = self.title_font.render("在商店選購", True, (0, 0, 0)) # 黑體標題
        self.screen.blit(title_surf, (50, title_y))
        
        subtitle_surf = self.small_font.render("各種機型。依你所需來打造。", True, (100, 100, 100))
        self.screen.blit(subtitle_surf, (50, title_y + 40))
        
        # 2. 計算網格起始位置
        start_x = 50
        start_y = 140 - self._scroll_y # 套用滾動偏移
        
        # 3. 繪製每個商品卡片
        for index, product in enumerate(self._products):
            row = index // self.COLS
            col = index % self.COLS
            
            x = start_x + col * (self.CARD_WIDTH + self.GAP_X)
            y = start_y + row * (self.CARD_HEIGHT + self.GAP_Y)
            
            # 檢查是否在畫面內 (簡單優化)
            if y + self.CARD_HEIGHT < 0 or y > self.screen.get_height():
                continue
                
            self._draw_card(x, y, product, index == self._selected_index)

        # 4. 繪製操作訊息 (固定在右上角)
        if self._message:
            self.draw_message_toast(self._message, success=self._message_success)

    def _draw_card(self, x, y, product, is_selected):
        """繪製單個商品卡片。"""
        rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        
        # 卡片背景 (白色)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=18)
        
        # 選中狀態的外框
        if is_selected:
            # 藍色外框，稍微厚一點
            pygame.draw.rect(self.screen, (0, 113, 227), rect, width=3, border_radius=18)
        else:
            # 未選中時，畫一個很淡的陰影/邊框效果
            pygame.draw.rect(self.screen, (230, 230, 230), rect, width=1, border_radius=18)

        # 1. 商品標題
        name_surf = self.font.render(product.name, True, (0, 0, 0))
        self.screen.blit(name_surf, (x + 24, y + 24))
        
        # 2. 右上角：購物車數量 / 總庫存
        # 獲取當前購物車內數量
        cart_qty = self._get_cart_quantity(product.id)
        qty_text_str = f"{cart_qty}/{product.stock}"
        
        qty_surf = self.qty_font.render(qty_text_str, True, (0, 0, 0))
        qty_rect = qty_surf.get_rect()
        
        # 繪製方框 (在標題的右側，或固定在卡片右上角)
        # 固定在卡片右上角: x + width - padding - text_width
        box_padding_x = 10
        box_padding_y = 5
        box_width = qty_rect.width + box_padding_x * 2        
        box_x = x + self.CARD_WIDTH - box_width - 24
        box_y = y + 24        
        
        # 畫文字
        self.screen.blit(qty_surf, (box_x + box_padding_x, box_y + box_padding_y))

        # 3. 商品圖片 (置中)
        img_surface = self._image_cache.get(product.id)
        if img_surface:
            img_x = x + (self.CARD_WIDTH - self.IMG_SIZE[0]) // 2
            img_y = y + 80
            self.screen.blit(img_surface, (img_x, img_y))
            
        # 4. 底部資訊區域
        bottom_y = y + self.CARD_HEIGHT - 60
        
        # 價格 (左下)
        price_text = f"NT${product.price:,} 起"
        price_surf = self.small_font.render(price_text, True, (50, 50, 50))
        self.screen.blit(price_surf, (x + 24, bottom_y + 10))
        
        # 5. 購買按鈕 (圓角長方形)
        btn_width = 70
        btn_height = 36
        btn_x = x + self.CARD_WIDTH - btn_width - 20 # 距離右邊 20px
        btn_y = bottom_y + 5 # 距離價格區域頂部 5px (稍微垂直置中)
        
        btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        
        # 按鈕背景 (藍色)
        btn_color = (0, 113, 227) if is_selected else (240, 240, 240)
        pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=btn_rect.height // 2)
        
        # 按鈕文字
        stock_str = "購買"
        btn_text_color = (255, 255, 255) if is_selected else (0, 113, 227)
        btn_surf = self.small_font.render(stock_str, True, btn_text_color)
        text_rect = btn_surf.get_rect(center=btn_rect.center)
        self.screen.blit(btn_surf, text_rect)

    def draw_message_toast(self, message, success=True):
        """繪製右上角的提示訊息 (Toast)。"""
        # 背景色
        bg_color = (250, 250, 250) if success else (250, 250, 250)
        border_color = (200, 200, 200) if success else (200, 200, 200)
        text_color = (20, 20, 20) if success else (100, 20, 20)
        
        font = self.font
        text_surf = font.render(message, True, text_color)
        
        # 計算位置 (右上角)
        padding = 10
        w = text_surf.get_width() + padding * 2
        h = text_surf.get_height() + padding * 2
        x = self.screen.get_width() - w - 20
        y = 20
        
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, rect, width=2, border_radius=8)
        self.screen.blit(text_surf, (x + padding, y + padding))

    # Internal helpers -------------------------------------------------

    def _add_selected_product(self) -> None:
        """將選中的商品加入購物車的核心邏輯。"""
        product = self._products[self._selected_index]
        try:
            # 呼叫購物車核心邏輯 (TDD/BDD/DDD 的主要入口)
            self.cart.add_item(product.id, 1)
        except ValueError as exc:  # 捕獲購物車邏輯拋出的錯誤 (例如：庫存不足)
            self._message = str(exc)
            self._message_success = False
        else: # 如果 try 區塊成功執行 (沒有拋出例外)
            self._message = f"已加入 {product.name}"
            self._message_success = True