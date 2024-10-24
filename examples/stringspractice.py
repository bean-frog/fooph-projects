# made them one-liners excluding string defs
# because i can

# Problem 2 - append string in the middle of another
p2str1 = "Ault"
p2str2 = "Kelly"
print(f"{p2str1[:(len(p2str1)//2)]}{p2str2}{p2str1[(len(p2str1)//2):]}")

# Problem 3 - create a string with the first, middle, and last characters of the input strings
p3str1 = "America"
p3str2 = "Japan"
print(f"{p3str1[0]}{p3str2[0]}{p3str1[(len(p3str1)//2)]}{p3str2[(len(p3str2)//2)]}{p3str1[-1]}{p3str2[-1]}")

# Problem 4 - arrange lowercase first
p4str1 = "PyNaTive"
print(f"{''.join([char for char in p4str1 if char.islower()])}{''.join([char for char in p4str1 if char.isupper()])}")

# Problem 5 - count letters/digits/symbols
p5str1 = "P@#yn26at^&i5ve"
print(f"Chars: {len([char for char in p5str1 if char.isalpha()])}\nDigits: {len([char for char in p5str1 if char.isdigit()])}\nSymbols: {len([char for char in p5str1 if char.isalpha() == False and char.isdigit() == False])}")

# Problem 6 - zip 2 strings, appending leftovers at the end
p6str1 = "Abc"
p6str2 = "Xyz"
print("".join(p6str1[i] + p6str2[::-1][i] if i < len(p6str1) and i < len(p6str2) else (p6str1[i] if i < len(p6str1) else p6str2[::-1][i]) for i in range(max(len(p6str1), len(p6str2)))))
