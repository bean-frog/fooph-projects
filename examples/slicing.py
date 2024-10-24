name = str(input("enter your full name\n> "))
components = name.split(" ")
first = components[0]
last = components[-1]
print(f"hello, {first.capitalize()} {last.capitalize()}")