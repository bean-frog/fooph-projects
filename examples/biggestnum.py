try:
    num1 = float(input("Enter number 1\n> "))
    num2 = float(input("Enter number 2\n> "))
    if (num1 == num2):
        print("Numbers are the same")
    elif (num1 > num2):
        print("number 1 is bigger")
    else:
        print("number 2 is bigger")
except ValueError:
    print("invalid input. please use a number")

