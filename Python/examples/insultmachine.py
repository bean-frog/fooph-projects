import random
def get_insult(index):
    insults = [
        "your mother was a hamster and your father smelt of elderberries!",
        "i fart in your general direction!",
        "go and boil your bottoms, you sons of silly persons!",
        "go away you silly English knight!",
        "I've got no option but to sell you for scientific experiments!"
    ]
    if index > len(insults):
        return random.choice(list(insults))
    else:
        return(insults[index])
try:
    num = int(input("enter a number\n> "))
    print(get_insult(num))
except ValueError:
    print("must be int")
