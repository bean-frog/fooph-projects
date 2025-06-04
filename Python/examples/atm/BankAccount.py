import hashlib

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

class BankAccount():
    accounts = [ 
        {
            "username": "user1",
            "passhash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # "password"
            "balance": "1"
        },
         {
            "username": "user2",
            "passhash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", # "123456"
            "balance": "2"
        },
        {
            "username": "user3",
            "passhash": "6ddbb91a63b88bad59b108fa7a4b236155f5b1b1dd2dc9580798624dcbc2dcee", # "verysecure"
            "balance": "3"
        },
        
    ]
    auth = None
    withdraw_limit = 9999
    def __init__(self, name, password):
        if self.auth != None:
            self.auth = None
        for account in self.accounts:
            if (account["username"] == name):
                if (account["passhash"] == hash_pw(password)):
                    print(f'Welcome, {name}')
                    self.auth = name
                else:
                    print(f'wrong password for user: {name}')
    def getBalance(self):
        if self.auth == None:
            print(f'Error: no authenticated user.')
        else:
            return next((account["balance"] for account in self.accounts if account["username"] == self.auth), None)
    def withdraw(self, amount):
        if self.auth == None:
            print(f'Error: no authenticated user.')
        elif amount > self.withdraw_limit:
            print(f'Error: {amount} is above the withdraw limit')
        else:
            account = next((account for account in self.accounts if account["username"] == self.auth), None)
            bal = float(account['balance'])
            if (bal - float(amount)) < 0:
                print(f"You don't have that much money you brokie.\n Balance: {account['balance']}\n Attempted withdrawal: {amount}")
            else:
                account["balance"] -= amount
                print(f"New Balance: {account['balance']}")
    def deposit(self, amount):
        if self.auth == None:
            print(f'Error: no authenticated user.')
        else:
            account = next((account for account in self.accounts if account["username"] == self.auth), None)
            account["balance"] = float(account["balance"]) + amount
            print(f"New Balance: {account['balance']}")
        
                
        

