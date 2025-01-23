import BankAccount as ba

print("V E R Y S E C U R E B A N K I N G ™")
username = input("username: ")
password = input("password: ")

user = ba.BankAccount(username, password)

while True:
    print('1. Print Balance')
    print('2. Withdraw')
    print('3. Deposit')
    print('4. Exit')

    choice = int(input("Enter a number\n> "))
    if choice == 1:
        print(user.getBalance())
    elif choice == 2:
        user.withdraw(int(input("Enter an amount to withdraw\n> ")))
    elif choice == 3:
        user.deposit(int(input("Enter an amoint to deposit\n> ")))
    elif choice == 4:
        exit()
    else:
        print("invalid choice")
