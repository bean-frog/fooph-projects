locations = {
    100: "vapa",
    200: "english",
    300: "language",
    500: "cs",
    700: "testing center",
    800: "history",
    1700: "science"
}
special_cases = {
    500: "library",
    800: "math",
    800: "social studies",
    100: "band",
    100: "choir"
}

name = str(input("Hi there, what's your name?\n> "))
destination = str(input(f'Hi, {name}. Where are you trying to go?\n> ')).lower()

def find_building(dest):
    for building, subject in special_cases.items():
        if subject == dest:
            return building
    for building, subject in locations.items():
        if subject == dest:
            return building    
    return None

building = find_building(destination)

if building:
    print(f"You should go to building {building}.")
else:
    print("You're on your own buddy idk where that is")