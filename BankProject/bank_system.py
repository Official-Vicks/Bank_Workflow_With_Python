import json
from bank_accounts import BankAccounts

class BankSystem():
    '''This controls the inner workings of the bank'''
    def __init__(self):
        pass

    def save_account(self, accounts):
        '''This method saves the created account for later use'''
        account_data = []

        for account in accounts:
            account_data.append(self.account_to_dict(account))

        with open("accounts.json", "w") as file:
            json.dump(account_data, file, indent=4)
            print("\nSaved successfully.")

    def load_accounts(self):
        '''This method loads existing accounts into the system'''
        with open("accounts.json", "r") as file:
            return json.load(file)
        
    def dict_to_account(self, data):
        account = BankAccounts()

        account.fullname = data["fullname"]
        account.username = data["username"]
        account.pin = data["pin"]
        account.account_number = data["account_number"]
        account.balance = data["balance"]

        return account
    
    def account_to_dict(self, account):
        return {
            "fullname": account.fullname,
            "username": account.username,
            "pin": account.pin,
            "account_number":account.account_number,
            "balance": account.balance
        }