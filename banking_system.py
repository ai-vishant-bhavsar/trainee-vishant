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
        df = pd.DataFrame(columns=["Account Number", "Name", "Mobile Number", "Email", "Address", "Account Type", 
                                   "IFSC code", "Branch Name", "Branch Address", "Account PIN", "Balance"])
        df.to_excel(excel_file, index=False)
        print("Excel file created with Headers.")
    else:
        print("Excel file already exists.")

def load_form_excel():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    return pd.DataFrame(columns=["Account Number", "Name", "Mobile Number", "Email", "Address", "Account Type", 
                                 "IFSC code", "Branch Name", "Branch Address", "Account PIN", "Balance"])

def save_to_excel(df):
    df.to_excel(excel_file, index=False)
    print("Data saved to Excel file.")

def get_valid_input(prompt: str, is_numeric=False) -> str:
    while True:
        value = input(prompt).strip()
        if is_numeric:
            try:
                num = int(value)
                if num > 0:
                    return num
            except ValueError:
                pass
        elif value.isalpha():
            return value
        print(f"Invalid input! Please enter a valid {prompt.lower()}.")

def admin_login():
    print("\n Admin login: ")
    while True:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if username == admin_username and password == admin_password:
            print("Admin login successful!")
            return True
        else:
            print("Invalid credentials. Access denied. Try again.")

def apply_interest_to_saving_account():
    df = load_form_excel()
    for index, row in df.iterrows():
        if row["Interest Rate"] > 0:
            interest = row["Balance"] * row["Interest Rate"]
            df.at[index, "Balance"] += interest
            print(f"Interest of {interest} applied to account {row['Account Number']}")
    save_to_excel(df)

def account_number_generator(acc_type):
    while True:
        account_number = [5, 0, 4, 0, 5, 7, 0, 5, 3] + [r.randint(0, 9) for _ in range(3)]
        account_number.append(1 if acc_type == 'saving' else 0)
        account_number_str = ''.join(map(str, account_number))
        if account_number_str not in used_account_numbers:
            used_account_numbers.add(account_number_str)
            return account_number_str

class AccountDetails:
    def __init__(self):
        self.fname = get_valid_input("Enter your first name: ")
        self.mname = get_valid_input("Enter your middle name: ")
        self.lname = get_valid_input("Enter your last name: ")
        self.mo_number = get_valid_input("Enter your mobile number: ", True)
        self.email = input("Enter your email address: ")
        self.address = input("Enter your address: ")
        self.account_type = get_valid_input("Enter type of account (saving(s)/current(c)): ").lower()
        self.account_number = get_valid_input("Enter a 14 digit number: ", True)
        self.account_pin = get_valid_input("Create your 4-digit pin: ", True)
        self.IFSC_code = "HDFC57053"
        self.branch_name = "Ahmedabad"
        self.branch_address = "Sindhubhavan road, Ahmedabad"
        self.balance = 2500.0
        self.interest_rate = 0.03 if self.account_type == "s" else 0.0

    def add_account(self):
        account_type = 'saving' if self.account_type == 's' else 'current'
        account = {
            "Account Number": self.account_number,
            "Name": f"{self.fname} {self.mname} {self.lname}",
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
    type_ = get_valid_input("For which type of interest you want to calculate(Saving account(1)/Fix deposits(2)/Loans(3)): ", True)
    amount = get_valid_input("Enter amount: ", True)
    year = get_valid_input("Enter a years: ", True)
    if type_ == 1:
        interest_rate = 3.5 if amount > 5000000 else 3.0
        interest = (amount * year * interest_rate) / 100
        print(f"Your interest after {year} years is {interest} and your total amount is {amount + interest}.")
    elif type_ == 2:
        age = get_valid_input("Enter you age: ", True)
        interest_rate = 7.40 if age > 60 else 7.90
        interest = (amount * year * interest_rate) / 100
        print(f"Your interest after {year} years is {interest} and your FD amount is {amount + interest}.")
    elif type_ == 3:
        loan_rates = {1: 14.00, 2: 13.30, 3: 24.14}
        type_of_loans = get_valid_input("Enter type of loan (Auto loan(1)/Against Property(2)/Personal loan(3)): ", True)
        interest = (amount * year * loan_rates.get(type_of_loans, 0)) / 100
        print(f"Your loan interest after {year} years is {interest} and the total repayment is {amount + interest}.")
    else:
        print("Invalid input.")

def transaction(transaction_type, account_number, amount):
    df = load_form_excel()
    if account_number not in df["Account Number"].astype(str).values:
        print("Account not found.")
        return
    account_index = df[df["Account Number"] == account_number].index[0]
    account_pin = get_valid_input("Enter your PIN: ", True)
    if account_pin != df.at[account_index, "Account PIN"]:
        print("Invalid PIN.")
        return
    if transaction_type == "deposit":
        df.at[account_index, "Balance"] += amount
        print(f"Deposited {amount}. New Balance: {df.at[account_index, 'Balance']}")
    elif transaction_type == "withdraw":
        balance = df.at[account_index, "Balance"]
        if balance >= amount:
            df.at[account_index, "Balance"] -= amount
            print(f"Withdrew {amount}. New Balance: {df.at[account_index, 'Balance']}")
        else:
            print("Insufficient balance.")
    save_to_excel(df)

def over_draft():
    df = load_form_excel()
    account_number = get_valid_input("Enter your 14 digit account number: ", True)
    if account_number not in df["Account Number"].astype(str).values:
        print("Account not found.")
        return
    account_index = df[df["Account Number"] == account_number].index[0]
    if df.at[account_index, "Account Type"] != "current":
        print("Only current accounts can have overdraft.")
        return
    account_pin = get_valid_input("Enter your PIN: ", True)
    if account_pin != df.at[account_index, "Account PIN"]:
        print("Invalid PIN.")
        return
    amount = get_valid_input("Enter the amount you want to withdraw: ", True)
    balance = df.at[account_index, "Balance"]
    df.at[account_index, "Balance"] -= amount
    print(f"Withdrew {amount} and your overdraft is {abs(amount - balance)}.")
    save_to_excel(df)

def display_all_account():
    df = load_form_excel()
    for _, row in df.iterrows():
        print("\n".join([f"{col}: {'****' if col == 'Account PIN' else row[col]}" for col in df.columns]))

initialized_excel()
while True:
    print('''
    1. Add new account
    2. To see your account details
    3. Deposit money
    4. Withdraw money
    5. Calculate Interest
    6. Overdraft for current account
    7. View all the accounts(Admin only)
    8. Apply interest to all saving accounts (Admin only)
    9. Exit''')
    opt = get_valid_input("Enter a number(1 to 9): ", True)

    if opt == 1:
        AccountDetails().add_account()
    elif opt == 2:
        account_number = get_valid_input("Enter your 14 digit account number: ", True)
        transaction("view", account_number, 0)
    elif opt == 3:
        account_number = get_valid_input("Enter your 14 digit account number: ", True)
        amount = get_valid_input("Enter the amount you want to deposit: ", True)
        transaction("deposit", account_number, amount)
    elif opt == 4:
        account_number = get_valid_input("Enter your 14 digit account number: ", True)
        amount = get_valid_input("Enter the amount you want to withdraw: ", True)
        transaction("withdraw", account_number, amount)
    elif opt == 5:
        calculate_interest()
    elif opt == 6:
        over_draft()
    elif opt == 7:
        if admin_login():
            display_all_account()
    elif opt == 8:
        if admin_login():
            apply_interest_to_saving_account()
    elif opt == 9:
        print("Exiting the program...")
        break
    else:
        print("Invalid input! Please enter again.")
