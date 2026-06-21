from bank_system import BankingSystem

def main():
    bank = BankingSystem()
    print("====== Welcome to the Wise Command-Line Bank ======")
    
    while True:
        try:
            if not bank.current_user:
                # Main Menu (Logged Out)
                print("\n1. Create Account\n2. Login\n3. Exit")
                choice = input("Select an option (1-3): ").strip()
                
                if choice == "1":
                    bank.create_account()
                elif choice == "2":
                    bank.login()
                elif choice == "3":
                    print("\nThank you for banking with us. Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please pick 1, 2, or 3.")
            else:
                # User Menu (Logged In)
                print(f"\n--- User Menu (Logged in as #{bank.current_user}) ---")
                print("1. View Balance\n2. Deposit Money\n3. Withdraw Money\n4. Transfer Funds\n5. Transaction Summary\n6. Logout")
                choice = input("Select an option (1-6): ").strip()

                if choice == "1":
                    bank.view_balance()
                elif choice == "2":
                    bank.deposit()
                elif choice == "3":
                    bank.withdraw()
                elif choice == "4":
                    bank.transfer()
                elif choice == "5":
                    bank.view_summary()
                elif choice == "6":
                    print("🔒 Logged out successfully.")
                    bank.current_user = None
                else:
                    print("❌ Invalid choice. Please pick a number from 1 to 6.")
        
        except Exception as e:
            # Global fall-back safety catch
            print(f"\n⚠️ An unexpected system error occurred: {e}")
            print("Don't worry, your session is secure. Let's pick up right where we left off.")

if __name__ == "__main__":
    main()