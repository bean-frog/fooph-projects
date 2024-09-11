import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

stored_password = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4" #sha256

def check_password(input_password):
    if hash_password(input_password) == stored_password:
        return True
    else:
        return False

input_password = input("Enter the password to check: ")

if check_password(input_password):
    print("Password is correct!")
else:
    print("Password is incorrect!")