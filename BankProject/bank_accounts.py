import random

# A class to handle exception errors
class SystemException(Exception):
    '''Handles any case of exceptions and possible errors without crash'''

# Create a bank class
class BankAccounts:
    '''A method to create account, deposit, withdraw and make transfers'''
    def __init__(self):
        pass

    def generate_account_number(self, accounts):
        # a set of existing account numbers
        existing_numbers = {account.account_number for account in accounts}
        while True:
            #generate 10 digit account number
            account_number = random.randint(10000000, 99999999)
            print(account_number)
            if account_number not in existing_numbers:
                return account_number
    
    def create_account(self, accountName, username, accountPin, accounts):
        '''When creating an account please provide full name, username and pin'''
        self.fullname = accountName
        self.username = username
        self.pin = accountPin
        self.account_number = self.generate_account_number(accounts)
        self.balance = 0

        print("\n************")
        print(f"Account {self.username} has been created with the following details.\nFullname: {self.fullname}\nUsername: {self.username}\nAccount Number: {self.account_number}\nBalance: ${self.balance:.2f}")
        return {
            "fullname": self.fullname,
            "username": self.username,
            "pin": self.pin,
            "account_number":self.account_number,
            "balance": self.balance
        }

    def login(self, pin):
        '''Input pin to be authorized'''
        if self.pin == pin:
            print("\nLogin successful.")
            return True
        else:
            print("\nIncorrect pin.")
            return False

    def get_balance(self):
        print("\n************")
        print(f"Account balance: ${self.balance:.2f}")

    def amount_check(self, amount):
        '''Ensures the amount is a positive value'''
        if amount <= 0:
            raise SystemException(
                f"Error! Deposit/Withdrawal amount must be greater than zero"
            )

    def deposit(self, amount):
        '''Enter the amount to be deposited'''
        try:
            self.get_balance()
            self.amount_check(amount)
            self.balance += amount
            print("Deposit Completed")
            self.get_balance()
        except SystemException as error:
            print(f"Deposit interrupted: {error}")

    def viable_transaction(self, amount):
        '''This checks if the initiated transaction is possible depending on the current balance and account status.\n
        If all conditions are met then the transaction can proceed'''
        if self.balance >= amount:
            return
        else:
            raise SystemException(
                f"Sorry account {self.username} only has a balance of ${self.balance:.2f}"
            )
    def withdraw(self, amount):
        '''Enter the amount you want to withdraw'''
        try:
            self.amount_check(amount)
            self.viable_transaction(amount)
            self.balance -= amount
            print("Withdraw completed")
            self.get_balance()
        except SystemException as error:
            print(f"Withdraw interrupted: {error}")