grades = []
valid_grades = ['f', 'd', 'c', 'b', 'a']
sum_grades = 0

grade = input("Enter a grade letter, or type 'stop'\n> ")
while grade.strip().lower() != 'stop':
    grades.append(grade.strip().lower()) if grade.strip().lower() in valid_grades else print("Invalid option!\n")
    grade = input("Enter a grade letter, or type 'stop'\n> ")

for grade in grades:
    sum_grades += valid_grades.index(grade)
    
print(f'{(sum_grades / len(grades)):.2f}')