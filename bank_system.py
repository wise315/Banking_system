import random
from validators import validate_password

class BankingSystem:
    def __init__(self):
        # Acts as our in-memory database
        self.accounts = {}
        # Tracks who is currently logged into the system
        self.current_user = None
        
    def create_account(self):
        print("\n--- Create New Account ---")
        name = input("Enter your full name: ").strip()
        if not name:
            print("❌ Name cannot be empty.")
            return
        
        password = input("Create a strong password: ")
        if not validate_password(password):
            print("❌ Account creation failed due to weak password.")
            return
                
        # Generate a unique random 5-digit account number
        while True:
            acct_num = str(random.randint(10000, 99999))
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
        acct_num = input("Enter your account number: ").strip()
        password = input("Enter your password: ")
        
        if acct_num in self.accounts and self.accounts[acct_num]["password"] == password:
            self.current_user = acct_num
            print(f"👋 Welcome back, {self.accounts[acct_num]['name']}!")
        else:
            print("❌ Invalid account number or password.")
            
    def deposit(self):
        print("\n--- Deposit Funds ---")
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("❌ Deposit amount must be greater than zero.")
                return
            
            self.accounts[self.current_user]["balance"] += amount
            self.accounts[self.current_user]["transactions"].append(f"Deposited: ${amount:.2f}")
            print(f"✅ Success! Deposited ${amount:.2f}. New Balance: ${self.accounts[self.current_user]['balance']:.2f}")
        except ValueError:
            print("❌ Error: Invalid input. Please enter a valid number.")

    def withdraw(self):
        print("\n--- Withdraw Funds ---")
        try:
            amount = float(input("Enter amount to withdraw: $"))
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
        except ValueError:
            print("❌ Error: Invalid input. Please enter a valid number.")

    def transfer(self):
        print("\n--- Transfer Funds ---")
        target_acct = input("Enter the recipient's 5-digit account number: ").strip()
        
        if target_acct == self.current_user:
            print("❌ You cannot transfer money to yourself.")
            return
        if target_acct not in self.accounts:
            print("❌ Recipient account number not found.")
            return

        try:
            amount = float(input(f"Enter amount to transfer to {self.accounts[target_acct]['name']}: $"))
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
        except ValueError:
            print("❌ Error: Invalid input. Please enter a valid number.")

    def view_balance(self):
        balance = self.accounts[self.current_user]["balance"]
        print(f"\n💰 Your Current Balance: **${balance:.2f}**")

    def view_summary(self):
        print("\n--- Transaction Summary ---")
        transactions = self.accounts[self.current_user]["transactions"]
        for idx, txt in enumerate(transactions, 1):
            print(f"{idx}. {txt}")
        