colors = ["\033[1;31m", "\033[1;32m"] # red, green

spanish = {
    "one": "uno",
    "two": "dos",
    "three": "tres",
    "four": "quatro",
    "five": "cinco"
}

spanish["six"] = "seis"
spanish["seven"] = "siete"
spanish["eight"] = "ocho"
spanish["nine"] = "nueve"
spanish["ten"] = "diez"

# print(spanish)

fruits = {
    "apples": 1,
    "bananas": 4,
    "pears": 17,
    "oranges": 14
}

for fruit in fruits:
    if fruits[fruit] < 5:
        print(f"{colors[0]}{fruit} stock is low ({fruits[fruit]} left)")
    else:
        print(f"{colors[1]}{fruit} stock is okay ({fruits[fruit]} left)")
