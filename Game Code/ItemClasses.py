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
        self.pokeballs = 3

    def get_pokeballs(self):
        return self.pokeballs
    
    def refresh_pokeballs(self):
        self.pokeballs = 3