
colors = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;34m", "\033[1;35m"]



filename = input("enter a file name\n> ")

try:
    fib = open(filename, "r")
    append = input("append to this file?\n> ")
    if append == "no":
        exit()
    fib = open(filename, "a+")
except:
    
