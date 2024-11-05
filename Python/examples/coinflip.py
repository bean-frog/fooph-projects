import random

flip1 = random.randint(0,1)==1
flip2 = random.randint(0,1)==1
flip3 = random.randint(0,1)==1

numflips = 0

while not (flip1 and flip2 and flip3):
    flip1 = flip2
    flip2 = flip3
    flip3 = random.randint(0,1)==1  
    numflips += 1
print(numflips)