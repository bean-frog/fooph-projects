number = input("Enter a number or 'quit'\n> ")
sum = 0
while number.lower() != 'quit':
    sum += int(number)
    number = input("Enter another number or 'quit'\n> ")
print(sum)