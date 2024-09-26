day = input("what day is it\n> ")

i_suck_at_variable_names = {
    "sunday": 10,
    "monday": 8,
    "tuesday": 8,
    "wednesday": 8,
    "thursday": 8,
    "friday": 8,
    "saturday": 10
}

day_formatted = day.lower()

if day_formatted in i_suck_at_variable_names:
    print(f"{i_suck_at_variable_names[day]} AM alarm")
