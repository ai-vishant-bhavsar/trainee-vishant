import random as r
import pandas as pd
import os

excel_file = "Banking System.xlsx"
used_account_numbers = set()

admin_username = "Vishant Bhavsar"
admin_password = "Vish@nt1508"

MINIMUM_BALANCE_SAVING_ACCOUNT = 500


def initialized_excel():
    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=["Account Number", "Name", "Mobile Number",
                                   "Email", "Address", "Account Type", "IFSC code",
                                   "Branch Name", "Branch Address", "Account PIN", "Balance"])
        df.to_excel(excel_file, index=False)
        print("Excel file created with Headers.")
    else:
        print("Excel file already exists.")


def load_form_excel():
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        return df
    else:
        return pd.DataFrame(columns=["Account Number", "Name", "Mobile Number",
                                   "Email", "Address", "Account Type", "IFSC code",
                                   "Branch Name", "Branch Address", "Account PIN", "Balance"])


def save_to_excel(df):
    df.to_excel(excel_file, index=False)
    print("Data saved to Excel file.")


def get_valid_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value.isalpha():
            return value
        print("Invalid input, please enter a valid name.")


def get_valid_number(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt))
            if num > 0:
                return num
            print("Please enter a valid number greater than 0.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def admin_login():
    print("\n Admin login: ")
    while True:
        username = str(input("Enter admin username: "))
        password = str(input("Enter admin password: "))

        if username == admin_username and password == admin_password:
            print("Admin login successful!")
            return True
        else:
            print("Invalid credentials. Access denied. Try again.")
            continue


def apply_interest_to_saving_account():
    df = load_form_excel()
    for index, row in df.iterrows():
        interest_rate = row["Interest Rate"]
        if interest_rate > 0:
            balance = row["Balance"]
            interest = balance * interest_rate
            df.at[index, "Balance"] += interest
            print(f"Interest of {interest} applied to account {row['Account Number']}")
    save_to_excel(df)


def account_number_generator(acc_type):
    while True:
        account_number = [5, 0, 4, 0, 5, 7, 0, 5, 3]
        for i in range(0, 3):
            account_number.append(r.randint(0, 9))
        if acc_type == 'saving':
            account_number.append(1)
        elif acc_type == 'current':
            account_number.append(0)

        account_number_str = ''.join(map(str, account_number))

        if account_number_str not in used_account_numbers:
            used_account_numbers.add(account_number_str)
            return account_number_str


class personal_details:
    def __init__(self):
        self.fname = get_valid_input("Enter your first name: ")
        self.mname = get_valid_input("Enter your middle name: ")
        self.lname = get_valid_input("Enter your last name: ")
        while True:
            self.mo_number = get_valid_number("Enter your mobile number: ")
            if 10 > len(str(self.mo_number)):
                print("Enter a valid number")
                continue
            else:
                break
        self.email = str(input("Enter your email address: "))
        self.address = str(input("Enter your address: "))


class account_details(personal_details):
    def __init__(self):
        super().__init__()
        while True:
            self.account_type = get_valid_input("Enter type of account (saving(s)/current(c)): ").lower()
            if self.account_type == 's':
                break
            elif self.account_type == 'c':
                break
            else:
                print("Invalid Input enter a valid input (saving(s)/current(c)")
                continue
        while True:
            self.account_number = get_valid_number("Enter a 14 digit number: ")
            if len(str(self.account_number)) == 14:
                break
            else:
                print("Invalid number! please enter again")
                if self.account_number in used_account_numbers:
                    print("This account number is already exists enter another number")
                continue

        self.account_pin = get_valid_number("Create your 4-digit pin: ")
        self.IFSC_code = "HDFC57053"
        self.branch_name = "Ahmedabad"
        self.branch_address = "Sindhubhavan road, Ahmedabad"
        self.balance = 2500.0
        if self.account_type == "saving":
            self.interest_rate = 0.03
        else:
            self.interest_rate = 0.0


class account_operations(account_details):
    def add_account(self):
        global account_type
        acc_holder_name = f"{self.fname} {self.mname} {self.lname}"
        if self.account_type == 's':
            account_type = 'saving'
        else:
            account_type = 'current'
        account = {
            "Account Number": self.account_number,
            "Name": acc_holder_name,
            "Mobile Number": self.mo_number,
            "Email": self.email,
            "Address": self.address,
            "Account Type": account_type,
            "Account PIN": self.account_pin,
            "IFSC code": self.IFSC_code,
            "Branch Name": self.branch_name,
            "Branch Address": self.branch_address,
            "Interest Rate": self.interest_rate,
            "Balance": self.balance
        }

        df = load_form_excel()
        df = pd.concat([df, pd.DataFrame([account])], ignore_index=True)
        save_to_excel(df)
        print(f"{self.fname} {self.lname}, your account is created successfully.")


def calculate_interest():
    type = get_valid_input("For which type of interest you want to calculate(Saving account/Fix deposits/Loans)")
    amount = get_valid_number("Enter amount:")
    year = get_valid_number("Enter a years: ")
    if type == "Saving account":
        if amount > 5000000:
            interest = (amount * year * 3.5) / 100
            print(f"Your interest in your {amount} after {year} years is {interest}")
        else:
            interest = (amount * year * 3.0) / 100
            print(f"Your interest in your {amount} after {year} years is {interest}")
    elif type == "Fix deposits":
        age = get_valid_number("Enter you age: ")
        if age > 60:
            interest = (amount * year * 7.40) / 100
            print(f"Your interest in your {amount} after {year} years is {interest}")
        else:
            interest = (amount * year * 7.90) / 100
            print(f"Your interest in your {amount} after {year} years is {interest}")
    elif type == "Loan":
        type_of_loans = get_valid_input("Enter type of loan (Auto loan/Against Property/Personal loan): ")
        if type_of_loans == "Auto loan":
            interest = (amount * year * 14.00) / 100
            print(
                f"if you apply loan for {amount} for {year} yeas then your interest is {interest} and the end you have to pay {amount + interest}")
        elif type_of_loans == "Against Property":
            interest = (amount * year * 13.30) / 100
            print(
                f"if you apply loan for {amount} for {year} yeas then your interest is {interest} and the end you have to pay {amount + interest}")

        elif type_of_loans == "Personal loan":
            interest = (amount * year * 24.14) / 100
            print(
                f"if you apply loan for {amount} for {year} yeas then your interest is {interest} and the end you have to pay {amount + interest}")
        else:
            return False


def transaction(transaction_type, account_number, amount):
    df = load_form_excel()
    if account_number in (df["Account Number"].astype(int)).values:
        account_index = df[df["Account Number"].astype(int) == account_number].index[0]
        account_pin = get_valid_number("Enter your PIN: ")
        if account_pin == (df.at[account_index, "Account PIN"].astype(int)):
            if transaction_type == "deposit":
                df.at[account_index, "Balance"] += amount
                print(f"Successfully deposited {amount} into account {account_number}.")
                opt = str(input("Do you want to show account balance (Y/N):"))
                if opt == 'Y':
                    print(f"New Balance: {df.at[account_index, 'Balance']}")
            elif transaction_type == "withdraw":
                account_type = df.at[account_index, "Account Type"]
                current_balance = df.at[account_index, "Balance"]
                if account_type == "saving":
                    if current_balance - amount >= MINIMUM_BALANCE_SAVING_ACCOUNT:
                        df.at[account_index, "Balance"] -= amount
                        print(f"Successfully withdrew {amount} from account {account_number}.")
                        opt = str(input("Do you want to show account balance (Y/N):"))
                        if opt == 'Y':
                            print(f"New Balance: {df.at[account_index, 'Balance']}")
                    else:
                        print(f"Insufficient balance to withdraw.")
                elif account_type == "current":
                    cr_balance = df.at[account_index, "Balance"]
                    df.at[account_index, "Balance"] -= amount
                    if df.at[account_index, "Balance"] > 0:
                        print(f"Successfully withdrew {amount} from account {account_number}.")
                    else:
                        over_draft(account_number, amount, cr_balance)
                    opt = str(input("Do you want to show account balance (Y/N):"))
                    if opt == 'Y':
                        print(f"New Balance: {df.at[account_index, 'Balance']}")

            else:
                print("Invalid transaction type.")
            save_to_excel(df)
        else:
            print("Invalid PIN. Transaction Denied.")
            return False
    else:
        print("Account number not found.")
        return False


def over_draft(account_number, amount, cr_balance):
    over_draft_opt = get_valid_input("You have no sufficient balance do you want to over draft? (Y/N): ").lower()
    if over_draft_opt == 'y':
        print(f"Successfully withdrew {amount} from your account {account_number} and your overdraft is {abs(amount - cr_balance)}.")
    else:
        print("Transaction successful.")
        return True

def validate_account(account_number):
    df = load_form_excel()

    if account_number in (df["Account Number"].astype(int)).values:

        account_pin = get_valid_number("Enter your PIN to access your account: ")
        account_index = df[df["Account Number"].astype(int) == account_number].index[0]

        if account_pin == (df.at[account_index, "Account PIN"].astype(int)):
            print("Account validated successfully!")
            print("\nYour Account Details: ")
            for col in df.columns:
                print(f"{col}            : {df.at[account_index, col]}")
            return True
        else:
            print("Invalid PIN. Access denied.")
            return False
    else:
        print("Account number not found.")
        return False


def display_all_account():
    df = load_form_excel()
    print("\n All Accounts: ")
    for index, row in df.iterrows():
        for col in df.columns:
            if col == "Account PIN":
                print(f"{col}\t: ****")
            else:
                print(f"{col}\t: {row[col]}")


initialized_excel()
while True:
    print('''
    1. Add new account
    2. To see your account details
    3. Deposit money
    4. Withdraw money
    5. Calculate Interest
    6. View all the accounts(Admin only)
    7. Apply interest to all saving accounts (Admin only)
    8. Exit''')

    opt = int(input("Enter a number(1 to 6): "))
    if opt == 1:
        acc = account_operations()
        acc.add_account()
        continue
    elif opt == 2:
        account_number = get_valid_number("Enter your 14 digit account number: ")
        validate_account(account_number)
        continue
    elif opt == 3:
        account_number = get_valid_number("Enter your 14 digit account number: ")
        amount = float(input("Enter the amount you want to deposit: "))
        transaction("deposit", account_number, amount)
        continue
    elif opt == 4:
        account_number = get_valid_number("Enter your 14 digit account number: ")
        amount = float(input("Enter the amount you want to withdraw: "))
        transaction("withdraw", account_number, amount)
        continue
    elif opt == 5:
        calculate_interest()
        continue
    elif opt == 6:
        if admin_login():
            display_all_account()
        continue
    elif opt == 7:
        if admin_login():
            apply_interest_to_saving_account()
        continue
    else:
        break
