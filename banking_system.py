import random as r
import pandas as pd
from openpyxl.workbook import Workbook
import os

excel_file = "Banking System.xlsx"
used_account_numbers = set()

admin_username = "Vishant Bhavsar"
admin_password = "Vish@nt1508"

MINIMUM_BALANCE_CURRENT_ACCOUNT = 5000


def initialized_excel():
    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=["Account Number", "Name", "Mobile Number",
                                   "Email", "Address", "Account Type", "ISFC code",
                                   "Branch Name", "Branch Address", "PIN", "Balance"])
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
                                     "Email", "Address", "Account Type", "ISFC code",
                                     "Branch Name", "Branch Address", "PIN", "Balance"])
        

def save_to_excel(df):
    df.to_excel(excel_file, index=False)
    print("Data saved to Excel file.")


def admin_login():
    print("\n Admin login: ")
    username = str(input("Enter admin username: "))
    password = str(input("Enter admin userpassword: "))
    
    if username == admin_username and password == admin_password:
        print("Admin login successful!")
        return True
    else:
        print("Invalid credentials. Access denied.")
        return False


def apply_interest_to_saving_account():
    df = load_form_excel()
    for index, row in df.iterrow():
        interest_rate = row["Interest Rate"]
        if interest_rate > 0:
            balance = row["Balance"]
            interest = balance * interest_rate
            df.at[index, "Balance"] += interest
            print(f"Interest of {interest} applied to account {row['Account Number']}")
    save_to_excel()


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
        else:
            return account_number_generator(acc_type)


class personal_details:
    def _init_(self):
        self.fname = str(input("Enter your first name: "))
        self.mname = str(input("Enter your middle name: "))
        self.lname = str(input("Enter your last name: "))
        self.mo_number = str(input("Enter your mobile number: "))
        self.email = str(input("Enter your email address: "))
        self.address = str(input("Enter your address: "))


class account_details(personal_details):
    def _init_(self):
        super()._init_()
        self.account_type = str(input("Enter account type(saving/current): "))
        self.account_number = account_number_generator(self.account_type)
        self.account_pin = str(input("Create yout 4 digit pin: "))
        self.ISFC_code = "HDFC57053"
        self.branch_name = "Ahmedabad"
        self.branch_address = "Sindhubhavan road, Ahmedabad"
        self.balance = 2500.0
        if self.account_type == "saving":
            self.intrest_rate = 0.03
        else:
            self.intrest_rate = 0.0

class account_operations(account_details):
    def add_account(self):
        super()._init_()
        acc_holder_name = f"{self.fname} {self.mname} {self.lname}"
        
        account = {
            "Name": acc_holder_name,
            "Mobile Number": self.mo_number,
            "Email": self.email,
            "Address": self.address,
            "Account Type": self.account_type,
            "Account PIN" : self.account_pin,
            "ISFC Code": self.ISFC_code,
            "Branch Name": self.branch_name,
            "Branch Address": self.branch_address,
            "Interest Ratr": self.intrest_rate
        }
        
        df = load_form_excel()
        
        df = df.append(account, ignore_index=True)
        
        save_to_excel(df)
        print(f"{self.fname} {self.lname} your accout is created successfully.")
        
    
    def calculate_interest(self, account_number):
        df = load_form_excel()
        if account_number in df["Account Number"].values:
            account_index = df[df["Account Number"] == account_number].index[0]
            account_type = df.at[account_index, "Account Type"]
            interest_rate = df.at[account_index, "Interest Rate"]
            balance = df.at[account_index, "Balance"]
            
            if account_type == "saving" and interest_rate > 0:
                interest = balance * interest_rate
                df.at[account_index, "Balance"] += interest
                print(f"Interest of {interest} has been added to your saving account.")
                save_to_excel(df)
            else:
                print("No interest applicable for this account type")
        else:
            print("Account number not found.")
    
    
    def transaction(self, transaction_type, account_number, amount):
        df = load_form_excel()
        if account_number in df["Account Number"].values:
            account_index = df[df["Account Number"] == account_number.index[0]]
            pin = str(input("Enter you PIN: "))
            if pin == df.at[account_index, "PIN"]:
                if transaction_type == "deposit":
                    df.at[account_index, "Balance"] += amount
                    print(f"Succesfully deposited {amount} into account {account_number}.")
                    opt = str(input("Do you want to show account balance(Y/N):"))
                    if opt == 'Y':
                        print(f"New Balance: {df.at[account_index, 'Balance']}")
                elif transaction_type == "withdraw":
                    account_type = df.at[account_index, "Account Type"]
                    current_balance = df.at[account_index, "Balance"]
                    if account_type == "current":
                        if current_balance - amount >= MINIMUM_BALANCE_CURRENT_ACCOUNT:
                            df.at[account_index, "Balance"] -= amount
                            print(f"Successfully withdrew {amount} form account {account_number}.")
                            opt = str(input("Do you want to show account balance(Y/N):"))
                            if opt == 'Y':
                                print(f"New Balance: {df.at[account_index, 'Balance']}")
                        else:
                            print(f"Insufficient balance to the withdrawal.")
                else:
                    print("Invalid transaction type.")
                save_to_excel(df)
            else:
                print("Inwalid PIN. Transaction Denied.") 
        else:
            print("Account number not found.")


def validate_account(account_number):
    df = load_form_excel()
    
    if account_number in df["Account Number"].values:
        
        account_pin = str(input("Enter your PIN to access your account: "))
        account_index = df[df["Account Number"] == account_number].index[0]
        
        if account_pin == df.at[account_index,"PIN"]:
            print("Account validated successfully!")
            print("\nYour Account Details: ")
            for col in df.columns:
                print(f"{col}            : {df.at[account_index, col]}")
            return True
        else:
            print("Invalid PIN. Access denide.")
            return True
    else:
        print("Account number not found.")
        return False


def display_all_account():
    df = load_form_excel()
    print("\n All Accounts: ")
    for index, row in df.iterrows():
        print(f"\nAccount number= {row['Account Number']}")
        for col in df.columns:
            if col == "PIN":
                print(f"{col}            : ****")
            else:
                print(f"{col}            : {row[col]}")


initialized_excel()
while True:
    print('''
    1. Add new account
    2. To see your accout details
    3. Deposit money
    4. Withdraw money
    5. View all the accounts(Admin only)
    6. Apply interest to all saving accounts (Admin only)
    7. Exit''')

    opt = int(input("Enter a number(1 to 6): "))
    if opt == 1:
        acc = account_operations()
        acc.add_account()
        continue
    elif opt == 2:
        account_number = str(input("Enter your 14 digit account number: "))
        validate_account(account_number)
        continue
    elif opt == 3:
        account_number = str(input("Enter your 14 digit account number: "))
        amount = float(input("Enter the amount you want to deposit: "))
        acc = account_operations()
        acc.transaction("deposit", account_number, amount)
        continue
    elif opt == 4:
        account_number = str(input("Enter your 14 digit account number: "))
        amount = float(input("Enter the amount you want to deposit: "))
        acc = account_operations()
        acc.transaction("withdraw", account_number, amount)
        continue
    elif opt == 5:
        if admin_login():
            display_all_account()
        continue
    elif opt == 6:
        if admin_login():
            apply_interest_to_saving_account()
        continue
    else:
        break
