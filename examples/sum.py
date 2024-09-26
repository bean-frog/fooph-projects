def isSum10(num1, num2):
    return (num1 + num2) == 10

    
def sumDouble(num1, num2):
    if num1 == num2:
        return (num1 + num2) * 2
    else:
        return num1 + num2

print(f"isSum10(4,6) ==> {isSum10(4,6)}")
print(f"isSum10(-1,11) ==> {isSum10(-1,11)}")
print(f"isSum10(8,1) ==> {isSum10(8,1)}\n")
print(f"sumDouble(1,2) ==> {sumDouble(1,2)}")
print(f"sumDouble(3,2) ==> {sumDouble(3,2)}")
print(f"sumDouble(2,2) ==> {sumDouble(2,2)}")