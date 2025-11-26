"""
主視窗類別（共用）
所有版本使用相同的 UI 介面

這個類別是 Pygame 的主控制器，負責主迴圈、事件分派、
畫面繪製，以及視圖 (View) 之間的切換邏輯。
"""

from pathlib import Path
import pygame

# 導入各個獨立畫面 (View) 類別
from shared.ui.views.product_list_view import ProductListView
from shared.ui.views.cart_view import CartView
from shared.ui.views.checkout_view import CheckoutView
# 導入基礎視圖類別，用於存取字體候選列表及配色常數
from shared.ui.views.base_view import BaseView


class MainWindow:
    """主應用程式窗口，負責初始化 Pygame 和管理 View 狀態切換。"""
    
    def __init__(self, cart, width=1200, height=800):
        """初始化 Pygame 視窗及應用程式資源。"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height)) # 設定視窗大小
        pygame.display.set_caption("電商購物車系統")         # 設定視窗標題
        
        self.cart = cart        # 購物車邏輯實例 (TDD/BDD/DDD 核心)
        self.clock = pygame.time.Clock() # 用於控制幀率
        self.running = True     # 主迴圈控制旗標
        
        # 初始化各個視圖，並傳入畫面及購物車實例
        self.product_view = ProductListView(self.screen, self.cart)
        self.cart_view = CartView(self.screen, self.cart)
        self.checkout_view = CheckoutView(self.screen, self.cart)
        
        self.current_view = "product_list" # 追蹤當前顯示的視圖名稱 (State)
        self.nav_font = self._load_shared_font(20) # 載入導航按鈕的字體 (微調大小)
        self.nav_hint_font = self._load_shared_font(16) # 載入底部提示的字體
        
        # 導航欄的結構定義： (快捷鍵, 顯示文字, 視圖代碼)
        self._nav_items = [
            ("1", "商品清單", "product_list"),
            ("2", "購物車", "cart"),
            ("3", "結帳", "checkout"),
        ]
        # 視圖切換的順序列表，用於相對切換 (Tab/箭頭)
        self._view_order = [item[2] for item in self._nav_items]
    
    def run(self):
        """主迴圈：應用程式的核心執行點。"""
        while self.running:
            self.handle_events() # 處理所有輸入事件 (滑鼠、鍵盤)
            self.update()        # 更新應用程式的邏輯狀態
            self.draw()          # 繪製畫面
            self.clock.tick(60)  # 限制幀率為 60 FPS
        
        pygame.quit() # 結束 Pygame
    
    def handle_events(self):
        """處理所有 Pygame 事件，並將事件分派給當前視圖。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # 點擊視窗關閉按鈕時結束迴圈
                continue

            # 處理全域快捷鍵 (Esc, Tab, 數字鍵 1/2/3 等)
            if event.type == pygame.KEYDOWN and self._handle_global_shortcuts(event):
                continue # 如果是全域快捷鍵，就不再傳給當前視圖處理

            # 處理導航欄的滑鼠點擊
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左鍵點擊
                if self._handle_nav_click(event.pos):
                    continue  # 如果點擊了導航按鈕，就不再傳遞給視圖

            # 根據 current_view 的狀態，將事件分派給對應的 View 實例
            if self.current_view == "product_list":
                self.product_view.handle_event(event)
            elif self.current_view == "cart":
                self.cart_view.handle_event(event)
            elif self.current_view == "checkout":
                self.checkout_view.handle_event(event)
    
    def update(self):
        """更新當前視圖的內部邏輯（例如動畫或數據更新）。"""
        if self.current_view == "product_list":
            self.product_view.update()
        elif self.current_view == "cart":
            self.cart_view.update()
        elif self.current_view == "checkout":
            self.checkout_view.update()
    
    def draw(self):
        """繪製當前視圖及導航欄。"""
        self.screen.fill(BaseView.BG_COLOR) # 使用 BaseView 定義的背景色
        
        # 根據 current_view 的狀態，呼叫對應 View 的 draw 函式
        if self.current_view == "product_list":
            self.product_view.draw()
        elif self.current_view == "cart":
            self.cart_view.draw()
        elif self.current_view == "checkout":
            self.checkout_view.draw()
        
        self._draw_navigation_bar() # 繪製底部導航欄
        pygame.display.flip()       # 更新整個螢幕顯示
    
    def switch_view(self, view_name):
        """外部方法：強制切換當前視圖到指定的 view_name。"""
        self.current_view = view_name

    def _draw_navigation_bar(self):
        """
        繪製視窗底部的導航按鈕群組。
        使用 BaseView 的配色方案進行渲染。
        
        [更新] 按鈕群組現在會水平置中顯示。
        """
        screen_w, screen_h = self.screen.get_size()
        bar_height = 80
        y_start = screen_h - bar_height
        
        # 每次繪製前清空按鈕區域列表，重新計算
        self._nav_buttons = []

        # 1. 繪製導航欄上方的分隔線 (使用副文字顏色作為線條色)
        #pygame.draw.line(self.screen, (200, 200, 200), (0, y_start), (screen_w, y_start), 1)
        
        # --- 計算按鈕總寬度以進行置中 ---
        padding_x = 20
        padding_y = 12
        gap = 15
        total_width = 0
        button_specs = [] # 用來暫存 (text_string, view_name, width) 以便稍後繪製

        # 第一次迴圈：測量所有按鈕寬度
        for key, label, view in self._nav_items:
            text = f"{key}. {label}"
            # 這裡只為了測量大小，顏色暫不重要
            text_surf = self.nav_font.render(text, True, (0,0,0))
            w = text_surf.get_width() + padding_x * 2
            button_specs.append((text, view, w))
            total_width += w
            
        # 加上間距總和
        if len(button_specs) > 1:
            total_width += gap * (len(button_specs) - 1)
            
        # 計算起始 X 座標 (置中)
        x = (screen_w - total_width) // 2
        y_btn = y_start + 15
        
        # 2. 第二次迴圈：實際繪製按鈕
        for text_str, view, rect_w in button_specs:
            is_active = (view == self.current_view)
            
            # --- 配色邏輯 (對應 BaseView) ---
            if is_active:
                # 選中狀態：高亮背景 + 白色文字
                bg_color = BaseView.HIGHLIGHT_COLOR
                text_color = BaseView.ACTIVE_TEXT_COLOR
                border_color = BaseView.HIGHLIGHT_COLOR
            else:
                # 未選中狀態：淺灰背景 + 深灰文字
                bg_color = BaseView.INACTIVE_BUTTON_BG
                text_color = BaseView.TEXT_COLOR
                border_color = (200, 200, 200) # 淡淡的邊框
            
            # 渲染文字
            text_surf = self.nav_font.render(text_str, True, text_color)
            
            # 按鈕高度
            rect_h = text_surf.get_height() + padding_y * 2
            
            btn_rect = pygame.Rect(x, y_btn, rect_w, rect_h)
            
            # 存儲按鈕區域以便點擊偵測
            self._nav_buttons.append((btn_rect, view))

            # 繪製按鈕背景 (圓角矩形)
            pygame.draw.rect(self.screen, bg_color, btn_rect, border_radius=btn_rect.height // 2)
            
            # 如果未選中，繪製一個細邊框增加層次感
            if not is_active:
                pygame.draw.rect(self.screen, border_color, btn_rect, width=1, border_radius=btn_rect.height // 2)
            
            # 繪製置中文字
            text_rect = text_surf.get_rect(center=btn_rect.center)
            self.screen.blit(text_surf, text_rect)
            
            # 移動 X 座標到下一個按鈕位置
            x += rect_w + gap
        '''
        # 3. 繪製底部的操作提示 (移至右下角，避免與置中的按鈕衝突)
        hint = "操作提示：按 1/2/3 切換頁面，Tab 或 ←/→ 快速切換，Esc 離開程式"
        hint_surf = self.nav_hint_font.render(hint, True, BaseView.HINT_TEXT_COLOR)
        
        # 讓提示文字顯示在視窗右下角
        hint_rect = hint_surf.get_rect(bottomright=(screen_w - 20, screen_h - 15))
        self.screen.blit(hint_surf, hint_rect)
        '''

    def _switch_relative(self, step: int) -> None:
        """根據步長 (step) 進行視圖的相對切換 (例如：上一頁或下一頁)。"""
        try:
            idx = self._view_order.index(self.current_view) # 取得當前視圖的索引
            # 計算新的循環索引 (使用 % len(self._view_order) 確保索引不會超出範圍)
            idx = (idx + step) % len(self._view_order) 
            self.current_view = self._view_order[idx]
        except ValueError:
            # 防呆：如果 current_view 不在列表中，重置為第一個
            self.current_view = self._view_order[0]

    def _handle_nav_click(self, pos) -> bool:
        """檢查滑鼠點擊位置是否在導航按鈕上。"""
        for rect, view_name in self._nav_buttons:
            if rect.collidepoint(pos):
                self.switch_view(view_name)
                return True
        return False

    def _load_shared_font(self, size: int) -> pygame.font.Font:
        """嘗試從 BaseView 定義的候選路徑中載入字體檔案，找不到則使用預設字體。"""
        for candidate in BaseView.FONT_CANDIDATES:
            if candidate is None:
                break
            path = Path(candidate)
            if path.exists(): # 檢查檔案是否存在
                try:
                    return pygame.font.Font(str(path), size) # 載入字體檔案
                except OSError:
                    continue
        return pygame.font.Font(None, size) # 最終 fallback：使用 Pygame 預設字體

    def _handle_global_shortcuts(self, event: pygame.event.Event) -> bool:
        """處理應用程式層級的鍵盤快捷鍵。"""
        if event.key == pygame.K_ESCAPE:
            self.running = False # Esc 鍵：結束應用程式
            return True
        '''
        # Tab, 左/右箭頭鍵：相對切換視圖
        if event.key == pygame.K_TAB:
            # 檢查是否按下了 Shift 鍵 (Shift+Tab = 倒退切換)
            reverse = bool(event.mod & pygame.KMOD_SHIFT) 
            self._switch_relative(-1 if reverse else 1)
            return True
        if event.key == pygame.K_LEFT:
            self._switch_relative(-1)
            return True
        if event.key == pygame.K_RIGHT:
            self._switch_relative(1)
            return True
        
        # 數字鍵 1, 2, 3：絕對切換視圖
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
        '''
        return False # 如果沒有處理任何快捷鍵，返回 False