try:
    num1 = int(input("enter number 1\n> "))
    num2 = int(input("enter number 2\n> "))
    num3 = int(input("enter number 3\n> "))
    nums = [num1, num2, num3]
    nums = nums[:nums.index(13)] if 13 in nums else nums
    sum = 0
    for num in nums:
        sum = sum + num

    print(f'sum is {sum}')
        

except ValueError:
    print("please enter an integer")
