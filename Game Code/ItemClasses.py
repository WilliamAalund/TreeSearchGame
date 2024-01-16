class Item:
    def __init__(self):
        pass

class Consumable(Item):
    def __init__(self):
        pass

class KeyItem(Item):
    def __init__(self):
        pass

class Bag():
    def __init__(self):
        self.consumable_pouch = []
        self.key_item_pouch = []