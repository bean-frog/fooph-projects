
# Problem 1
# Alter the code below to print: "270 is 4.0 hours and 30 minutes." given the following:
totalMinutes = 270
print(f'{totalMinutes} is {(totalMinutes - (totalMinutes % 60))/60} hours and {totalMinutes % 60} minutes')


# Problem # 2 (check from class work)
# Write a program that will convert inches to feet from user input. 
inches = int(input('enter an amount in inches\n> '))
print(f'{inches} is  {inches // 12} feet and {inches % 12} inches')


# Problem 3
# Write a program that takes an integer hour from the user (assume correct input)
# and converts it to the 12-hour time (no need for am or pm). 

hour = int(input('enter an hour\n> '))
print(f"{hour % 12}{'AM' if hour < 12 else 'PM'}")
