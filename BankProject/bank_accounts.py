import random
import hashlib
import secrets
from datetime import datetime


# A class to handle exception errors
class SystemException(Exception):
    '''Handles any case of exceptions and possible errors without crash'''


# Create a bank class
class BankAccounts:
    '''Represents one bank account: create, login check, deposit, withdraw, transfer, history'''

    def __init__(self):
        self.fullname = ""
        self.username = ""
        self.salt = ""
        self.pin_hash = ""
        self.account_number = 0
        self.balance = 0.0
        self.transactions = []   # list of dictionaries, one per transaction

    # ---------- PIN SECURITY ----------
    @staticmethod
    def hash_pin(pin, salt):
        '''Turns a pin into a SHA-256 hash. The salt makes equal pins produce different hashes.'''
        return hashlib.sha256((salt + str(pin)).encode()).hexdigest()

    def set_pin(self, pin):
        '''Creates a new random salt and stores only the hash of the pin (never the pin itself)'''
        self.salt = secrets.token_hex(8)
        self.pin_hash = self.hash_pin(pin, self.salt)

    def check_pin(self, pin):
        '''Returns True if the pin entered matches the stored hash'''
        entered_hash = self.hash_pin(pin, self.salt)
        return secrets.compare_digest(entered_hash, self.pin_hash)

    # ---------- ACCOUNT CREATION ----------
    def generate_account_number(self, accounts):
        # a set of existing account numbers
        existing_numbers = {account.account_number for account in accounts}
        while True:
            # generate a 10 digit account number
            account_number = random.randint(1000000000, 9999999999)
            if account_number not in existing_numbers:
                return account_number

    def create_account(self, accountName, username, accountPin, accounts):
        '''When creating an account please provide full name, username and pin'''
        self.fullname = accountName.strip()
        self.username = username.lower()
        self.set_pin(accountPin)
        self.account_number = self.generate_account_number(accounts)
        self.balance = 0.0
        self.transactions = []

        print("\n************")
        print("Account has been created with the following details.")
        print(f"Fullname: {self.fullname}")
        print(f"Username: {self.username}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ₦{self.balance:,.2f}")

    # ---------- BALANCE AND CHECKS ----------
    def get_balance(self):
        print("\n************")
        print(f"Account balance: ₦{self.balance:,.2f}")

    def amount_check(self, amount):
        '''Ensures the amount is a positive value'''
        if amount <= 0:
            raise SystemException("Amount must be greater than zero")

    def viable_transaction(self, amount):
        '''Checks that the current balance is enough for the requested amount'''
        if self.balance < amount:
            raise SystemException(
                f"Insufficient funds. Account {self.username} only has a balance of ₦{self.balance:,.2f}"
            )

    def record_transaction(self, kind, amount, note=""):
        '''Saves a short record of the transaction inside the account'''
        self.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": kind,
            "amount": amount,
            "balance_after": self.balance,
            "note": note
        })

    # ---------- TRANSACTIONS ----------
    def deposit(self, amount):
        '''Enter the amount to be deposited'''
        self.amount_check(amount)
        self.balance = round(self.balance + amount, 2)
        self.record_transaction("Deposit", amount)

    def withdraw(self, amount):
        '''Enter the amount you want to withdraw'''
        self.amount_check(amount)
        self.viable_transaction(amount)
        self.balance = round(self.balance - amount, 2)
        self.record_transaction("Withdrawal", amount)

    def transfer(self, amount, receiver):
        '''Moves money from this account to another BankAccounts object'''
        if receiver is self:
            raise SystemException("You cannot transfer money to your own account")
        self.amount_check(amount)
        self.viable_transaction(amount)
        self.balance = round(self.balance - amount, 2)
        receiver.balance = round(receiver.balance + amount, 2)
        self.record_transaction("Transfer out", amount, f"To {receiver.account_number}")
        receiver.record_transaction("Transfer in", amount, f"From {self.account_number}")

    def show_history(self, count=10):
        '''Prints the most recent transactions'''
        print("\n************")
        if not self.transactions:
            print("No transactions yet.")
            return
        print(f"Last {min(count, len(self.transactions))} transaction(s):")
        for item in self.transactions[-count:]:
            print(
                f"{item['date']} | {item['type']:<12} | "
                f"₦{item['amount']:>12,.2f} | Balance: ₦{item['balance_after']:,.2f} {item['note']}"
            )
