from bank_accounts import *
from bank_system import *

bank = BankSystem()

accounts_data = bank.load_accounts()
accounts = []

for data in accounts_data:
    accounts.append(bank.dict_to_account(data))

# print(accounts[1].fullname)
class ValidationError(Exception):
    pass

# A class to validate all inputs
class Validation:
    def __init__(self):
        pass
    
    def validate_fullname(self, name):
        if not name or len(name.strip()) == 0:
            raise ValidationError("Name should not be empty")
    
    def validate_username(self, username):
        if not username or len(username.strip()) == 0:
            raise ValidationError("Name should not be empty")
        if not username.isalpha():
            raise ValidationError("username must contain only letters")
    
    def validate_unique_username(self, username, accounts):
        for account in accounts:
            if account.username == username:
                raise ValidationError("username is already taken")
            
    def validate_unique_account_number(self, account_number, accounts):
        # for account in accounts:
        #     if account.account_number ==
        pass

    def validate_pin(self, pin):
        # pin comes in as string from input
        if not pin.isdigit():
            raise ValidationError("Pin must contain only digits")
        if len(pin) != 4:
            raise ValidationError("Pin must be exactly 4 digits")
        return int(pin) # return the int version


print("***** MINI BANK *****")
print("1. Create account")
print("2. Login")
print("3. Exit")

error_check = Validation()
query = input("Choose an option: ")

if query == "1":
    print("************")
    try:
        name = input("Your fullname: ")
        error_check.validate_fullname(name)
        
        username = input("Your unique username: ")
        error_check.validate_username(username)
        # assuming the first validation is passed
        error_check.validate_unique_username(username, accounts)
        
        pin_input = input("Your desired pin: ")
        pin = error_check.validate_pin(pin_input) # returns int
        
        new_account = BankAccounts()
        new_account.create_account(name, username, pin, accounts)
        accounts.append(new_account)
        bank.save_account(accounts)
        print("Account created successfully")
    except ValidationError as error:
        print(f"Error! {error}")
    
elif query == "2":
    try:
        pin_input = input("Your desired pin: ")
        pin = error_check.validate_pin(pin_input) # returns int
    
        # new_accounts.login(pin)
    except ValidationError as error:
        print(f"Login error! {error}")
else:
    print("Bye")