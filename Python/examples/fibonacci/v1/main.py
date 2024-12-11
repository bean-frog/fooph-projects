import random
import time
colors = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;34m", "\033[1;35m"]

out = open("nums.txt", "w")
num1 = 1
num2 = 1

out.write(f"{str(num1)}\n{str(num2)}")

for i in range(100):
    tmp = num1
    num1 = num2
    num2 = num1 + tmp
    out.write(f"{str(num2)}\n")
    print(f"{random.choice(colors)}{str(num2)}")
    time.sleep(0.01)

out.close()
