class CartItem:
    """購物車中的商品項目"""
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
    
    def get_subtotal(self):
        """計算此項目的小計"""
        return self.quantity * self.price


class ShoppingCart:
    """購物車"""
    def __init__(self):
        self.items = []
        self.coupon = None
    
    def add_item(self, name, quantity, price):
        """加入商品"""
        # TODO: 先實作最簡單的版本
        self.items.append(CartItem(name, quantity, price))
    
    def get_item_count(self):
        """取得購物車中的商品總數量"""
        return sum(item.quantity for item in self.items)
    
    def get_items(self):
        """取得購物車中所有商品"""
        return self.items
    
    def get_total(self):
        """計算購物車總金額"""
        return sum(item.get_subtotal() for item in self.items)