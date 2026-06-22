import random
import time
# Import both the validator function and the new secure password collector
from validators import validate_password, get_secure_password

class BankingSystem:
    def __init__(self):
        # Acts as our in-memory database
        self.accounts = {}
        # Tracks who is currently logged into the system
        self.current_user = None

    def secure_input(self, prompt, expected_type="string"):
        """
        Custom input handler that enforces data types.
        Allows up to 3 failed attempts before imposing a 10-second penalty delay.
        """
        attempts = 0
        while True:
            user_input = input(prompt).strip()
            
            if expected_type == "string":
                # Ensure it only contains alphabetic characters and spaces (e.g., Names)
                if user_input and user_input.replace(" ", "").isalpha():
                    return user_input
                else:
                    print("❌ Error: Invalid entry. Only text/alphabetic characters are accepted.")
            
            elif expected_type == "numeric_string":
                # For numeric strings that shouldn't be converted to math types (like Account Numbers)
                if user_input and user_input.isdigit():
                    return user_input
                else:
                    print("❌ Error: Invalid entry. Only whole numeric digits are accepted.")

            elif expected_type == "float":
                # For balance inputs, deposits, and withdrawals
                try:
                    value = float(user_input)
                    return value
                except ValueError:
                    print("❌ Error: Invalid entry. Only valid numeric numbers/decimals are accepted.")

            # Increment mistake counter if the input failed validation rules above
            attempts += 1
            if attempts >= 3:
                print("\n⛔ Too many invalid attempts! Please wait 10 seconds before trying again...")
                time.sleep(10)
                attempts = 0 # Reset attempt counter after penalty completes

    def create_account(self):
        print("\n--- Create New Account ---")
        
        # Using secure_input to strictly enforce text/string values
        name = self.secure_input("Enter your full name: ", expected_type="string")
        
        # CHANGED: Replaced standard input() with the secure password handler from validators.py
        password = get_secure_password("Create a strong password (typing will be hidden): ")
                
        # Generate a unique random 5-digit account number
        while True:
            acct_num = str(random.randint(1000000000, 9999999999))
            if acct_num not in self.accounts:
                break
                
        self.accounts[acct_num] = {
            "name": name,
            "password": password,
            "balance": 0.0,
            "transactions": ["Account created."]
        }
        print(f"🥳 Account successfully created! Your Account Number is: **{acct_num}**")
        
    def login(self):
        print("\n--- Login ---")
        acct_num = self.secure_input("Enter your account number: ", expected_type="numeric_string")
        
        # CHANGED: Using get_secure_password here too so the login typing is also hidden
        password = get_secure_password("Enter your password: ")
        
        if acct_num in self.accounts and self.accounts[acct_num]["password"] == password:
            self.current_user = acct_num
            print(f"👋 Welcome back, {self.accounts[acct_num]['name']}!")
        else:
            print("❌ Invalid account number or password.")
            
    def deposit(self):
        print("\n--- Deposit Funds ---")
        amount = self.secure_input("Enter amount to deposit: $", expected_type="float")
        
        if amount <= 0:
            print("❌ Deposit amount must be greater than zero.")
            return
        
        self.accounts[self.current_user]["balance"] += amount
        self.accounts[self.current_user]["transactions"].append(f"Deposited: ${amount:.2f}")
        print(f"✅ Success! Deposited ${amount:.2f}. New Balance: ${self.accounts[self.current_user]['balance']:.2f}")

    def withdraw(self):
        print("\n--- Withdraw Funds ---")
        amount = self.secure_input("Enter amount to withdraw: $", expected_type="float")
        
        if amount <= 0:
            print("❌ Withdrawal amount must be greater than zero.")
            return
        
        current_balance = self.accounts[self.current_user]["balance"]
        if amount > current_balance:
            print(f"❌ Insufficient funds. Your current balance is ${current_balance:.2f}")
            return

        self.accounts[self.current_user]["balance"] -= amount
        self.accounts[self.current_user]["transactions"].append(f"Withdrew: ${amount:.2f}")
        print(f"✅ Success! Withdrew ${amount:.2f}. New Balance: ${self.accounts[self.current_user]['balance']:.2f}")

    def transfer(self):
        print("\n--- Transfer Funds ---")
        target_acct = self.secure_input("Enter the recipient's 5-digit account number: ", expected_type="numeric_string")
        
        if target_acct == self.current_user:
            print("❌ You cannot transfer money to yourself.")
            return
        if target_acct not in self.accounts:
            print("❌ Recipient account number not found.")
            return

        amount = self.secure_input(f"Enter amount to transfer to {self.accounts[target_acct]['name']}: $", expected_type="float")
        
        if amount <= 0:
            print("❌ Transfer amount must be greater than zero.")
            return
        
        sender_balance = self.accounts[self.current_user]["balance"]
        if amount > sender_balance:
            print(f"❌ Insufficient funds. Your current balance is ${sender_balance:.2f}")
            return

        # Perform the transfer
        self.accounts[self.current_user]["balance"] -= amount
        self.accounts[target_acct]["balance"] += amount
        
        # Record history for both parties
        self.accounts[self.current_user]["transactions"].append(f"Transferred ${amount:.2f} to Acct #{target_acct}")
        self.accounts[target_acct]["transactions"].append(f"Received ${amount:.2f} from Acct #{self.current_user}")
        
        print(f"✅ Success! Transferred ${amount:.2f} to {self.accounts[target_acct]['name']}.")

    def view_balance(self):
        balance = self.accounts[self.current_user]["balance"]
        print(f"\n💰 Your Current Balance: **${balance:.2f}**")

    def view_summary(self):
        print("\n--- Transaction Summary ---")
        transactions = self.accounts[self.current_user]["transactions"]
        for idx, txt in enumerate(transactions, 1):
            print(f"{idx}. {txt}")