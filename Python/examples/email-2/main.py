try:
    mail = open("mail.txt", "r")
except:
    print("file not found")
    exit()

days = {}

for line in mail:
    words = line.split()
    if (len(words) > 0 and words[0] == "From"):
        if days[line.split()[2]] == None:
            days[line.split()[2]] = 1
        else:
            days[line.split()[2]] += 1

print(days)
