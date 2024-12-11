inventory = {
   {
    "name": "apples",
    "price": 1,
    "stock": 69
   },
   {
    "name": "bananas",
    "price": 2,
    "stock": 69
   },
   {
    "name": "kiwis",
    "price": "$45",
    "stock": 69
   },
}

def banner():
    print("███████ ████████  ██████  ██████  ███████ ")
    print("██         ██    ██    ██ ██   ██ ██      ")
    print("███████    ██    ██    ██ ██████  █████   ")
    print("     ██    ██    ██    ██ ██   ██ ██      ")
    print("███████    ██     ██████  ██   ██ ███████ ")



class StoreActions:
    def buy(sku, quantity):
        inventory[sku]["stock"] += quantity
        print(f"Added {quantity} of {inventory[sku][name]} to the inventory")
        
    def sell(sku, quantity):
        inventory[sku]["stock"] -= quantity
        print(f"Removed {quantity} of {inventory[sku][name]} from the inventory")

    def sellall():
        for item in inventory:
            print(item[""])
            #item["stock"] = 0
            print(f"sold all of {item}")
    #def get_price(sku, quantity=1):
   # def showall():
        
StoreActions.sellall()
