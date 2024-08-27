# i love ANSI codes lol
class colors:
    RED = '\033[1;31m'  # Bold Red
    ORANGE = '\033[1;33m'  # Bold Orange
    YELLOW = '\033[1;33m'  # Bold Yellow
    GREEN = '\033[1;32m'  # Bold Green
    BLUE = '\033[1;34m'  # Bold Blue
    VIOLET = '\033[1;35m'  # Bold Violet
    RESET = '\033[0m'  # Reset to default color

age = int(input("Enter your age: "))

future_year = 2077
future_age = future_year - (2024 - age)

output_text = "In the year 2077, you will be " + str(future_age) + " years old."

color_codes = [colors.RED, colors.ORANGE, colors.YELLOW, colors.GREEN, colors.BLUE, colors.VIOLET]
current_color = 0

for index, letter in enumerate(output_text):
    if letter != " ":
        print(color_codes[current_color] + letter, end='')
        current_color = (current_color + 1) % len(color_codes)
    else:
        print(letter, end='')

print(colors.RESET) 

