import random
colors = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;34m", "\033[1;35m"]

file = open("nums.txt", "w")
for i in range(100):
    num = random.randint(1, 99999)
    file.write(f"{num}\n")
file.close()
numlist = []
new = open("nums.txt", "r")
for line in new:
    line = line.replace("\n", "")
    numlist.append(int(line))
print(sorted(numlist))
new.close()

