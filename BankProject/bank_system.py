import json
import os
from bank_accounts import BankAccounts

FILE_NAME = "accounts.json"


class BankSystem():
    '''This controls the inner workings of the bank: saving, loading and searching accounts'''

    def __init__(self, file_name=FILE_NAME):
        self.file_name = file_name

    def save_account(self, accounts):
        '''Saves all accounts. Writes to a temporary file first so a crash cannot damage the real file'''
        account_data = [self.account_to_dict(account) for account in accounts]
        temp_name = self.file_name + ".tmp"
        try:
            with open(temp_name, "w") as file:
                json.dump(account_data, file, indent=4)
            os.replace(temp_name, self.file_name)
        except OSError as error:
            print(f"Warning: could not save data ({error})")

    def load_accounts(self):
        '''Loads existing accounts. Returns an empty list on first run or if the file is unreadable'''
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, "r") as file:
                data_list = json.load(file)
            return [self.dict_to_account(data) for data in data_list]
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            backup = self.file_name + ".corrupt"
            print(f"Warning: {self.file_name} could not be read. A copy was kept as {backup}.")
            try:
                os.replace(self.file_name, backup)
            except OSError:
                pass
            return []

    def dict_to_account(self, data):
        account = BankAccounts()
        account.fullname = data["fullname"]
        account.username = data["username"]
        account.account_number = data["account_number"]
        account.balance = data["balance"]
        account.transactions = data.get("transactions", [])

        if "pin_hash" in data:
            account.salt = data["salt"]
            account.pin_hash = data["pin_hash"]
        else:
            # old file format stored the pin as a number: convert it to a hash
            account.set_pin(str(data["pin"]).zfill(4))
        return account

    def account_to_dict(self, account):
        return {
            "fullname": account.fullname,
            "username": account.username,
            "salt": account.salt,
            "pin_hash": account.pin_hash,
            "account_number": account.account_number,
            "balance": account.balance,
            "transactions": account.transactions
        }

    def find_by_username(self, username, accounts):
        for account in accounts:
            if account.username == username.lower():
                return account
        return None

    def find_by_account_number(self, account_number, accounts):
        for account in accounts:
            if account.account_number == account_number:
                return account
        return None
