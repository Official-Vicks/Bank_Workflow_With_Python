import math
from bank_accounts import BankAccounts, SystemException
from bank_system import BankSystem

MAX_LOGIN_ATTEMPTS = 3


class ValidationError(Exception):
    pass


# A class to validate all inputs
class Validation:
    def validate_fullname(self, name):
        if not name or len(name.strip()) == 0:
            raise ValidationError("Full name should not be empty")
        if any(char.isdigit() for char in name):
            raise ValidationError("Full name should not contain numbers")

    def validate_username(self, username):
        if not username or len(username.strip()) == 0:
            raise ValidationError("Username should not be empty")
        if not username.isalpha():
            raise ValidationError("Username must contain only letters")

    def validate_unique_username(self, username, accounts):
        for account in accounts:
            if account.username == username.lower():
                raise ValidationError("Username is already taken")

    def validate_pin(self, pin):
        # the pin is kept as a string so that a pin like 0123 keeps its leading zero
        if not pin.isdigit():
            raise ValidationError("Pin must contain only digits")
        if len(pin) != 4:
            raise ValidationError("Pin must be exactly 4 digits")
        return pin

    def validate_amount(self, text):
        try:
            amount = float(text)
        except ValueError:
            raise ValidationError("Amount must be a number")
        if not math.isfinite(amount):
            raise ValidationError("Amount is not valid")
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero")
        return round(amount, 2)

    def validate_account_number(self, text):
        if not text.isdigit() or len(text) != 10:
            raise ValidationError("Account number must be exactly 10 digits")
        return int(text)


validator = Validation()
bank = BankSystem()


def create_account_flow(accounts):
    print("\n************")
    try:
        name = input("Your fullname: ")
        validator.validate_fullname(name)

        username = input("Your unique username (letters only): ")
        validator.validate_username(username)
        validator.validate_unique_username(username, accounts)

        pin = validator.validate_pin(input("Your desired 4-digit pin: "))

        new_account = BankAccounts()
        new_account.create_account(name, username, pin, accounts)
        accounts.append(new_account)
        bank.save_account(accounts)
        print("Account created successfully")
    except ValidationError as error:
        print(f"Error! {error}")


def login_flow(accounts):
    '''Returns the logged-in account, or None if login fails'''
    print("\n************")
    username = input("Username: ")
    account = bank.find_by_username(username, accounts)

    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        pin = input("Pin: ")
        # the same message is shown for a wrong username or a wrong pin
        if account is not None and pin.isdigit() and account.check_pin(pin):
            print(f"\nWelcome, {account.fullname}")
            return account
        remaining = MAX_LOGIN_ATTEMPTS - attempt
        if remaining > 0:
            print(f"Login failed: invalid username or pin. {remaining} attempt(s) left.")
    print("Too many failed attempts. Returning to the main menu.")
    return None


def transfer_flow(account, accounts):
    try:
        number = validator.validate_account_number(input("Receiver's account number: "))
        receiver = bank.find_by_account_number(number, accounts)
        if receiver is None:
            raise ValidationError("No account found with that account number")
        amount = validator.validate_amount(input("Amount to transfer: ₦"))

        print(f"You are sending ₦{amount:,.2f} to {receiver.fullname}.")
        if input("Type 'y' to confirm: ").lower() != "y":
            print("Transfer cancelled")
            return

        account.transfer(amount, receiver)
        bank.save_account(accounts)
        print("Transfer completed")
        account.get_balance()
    except (ValidationError, SystemException) as error:
        print(f"Transfer interrupted: {error}")


def change_pin_flow(account, accounts):
    try:
        old_pin = input("Current pin: ")
        if not old_pin.isdigit() or not account.check_pin(old_pin):
            raise ValidationError("Current pin is incorrect")
        new_pin = validator.validate_pin(input("New 4-digit pin: "))
        account.set_pin(new_pin)
        bank.save_account(accounts)
        print("Pin changed successfully")
    except ValidationError as error:
        print(f"Pin change failed: {error}")


def account_menu(account, accounts):
    while True:
        print("\n***** ACCOUNT MENU *****")
        print("1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction history")
        print("6. Change pin")
        print("7. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            account.get_balance()
        elif choice == "2":
            try:
                amount = validator.validate_amount(input("Amount to deposit: ₦"))
                account.deposit(amount)
                bank.save_account(accounts)
                print("Deposit completed")
                account.get_balance()
            except (ValidationError, SystemException) as error:
                print(f"Deposit interrupted: {error}")
        elif choice == "3":
            try:
                amount = validator.validate_amount(input("Amount to withdraw: ₦"))
                account.withdraw(amount)
                bank.save_account(accounts)
                print("Withdrawal completed")
                account.get_balance()
            except (ValidationError, SystemException) as error:
                print(f"Withdrawal interrupted: {error}")
        elif choice == "4":
            transfer_flow(account, accounts)
        elif choice == "5":
            account.show_history()
        elif choice == "6":
            change_pin_flow(account, accounts)
        elif choice == "7":
            print("Logged out")
            return
        else:
            print("Invalid option, please choose 1-7")


def main():
    accounts = bank.load_accounts()
    print("***** MINI BANK (learning simulation, no real money) *****")

    while True:
        print("\n1. Create account")
        print("2. Login")
        print("3. Exit")
        query = input("Choose an option: ")

        if query == "1":
            create_account_flow(accounts)
        elif query == "2":
            account = login_flow(accounts)
            if account is not None:
                account_menu(account, accounts)
        elif query == "3":
            print("Bye")
            break
        else:
            print("Invalid option, please choose 1-3")


if __name__ == "__main__":
    main()
