from AccountManagement import AccountManagement  # Import the class for account management
from OrderProcessing import OrderProcessing  # Import the class for order processing
from Database import connect  # Import the function to connect to the database
from Menu import display_menu
import datetime
import os

def clear_screen():
    if os.name == 'nt': 
        os.system('cls')
    else:  
        os.system('clear')

def main():
    print("Welcome to Gusto d'Italia!")
    db = connect()
    cursor = db.cursor()

    account_manager = AccountManagement(cursor)
    order_processor = OrderProcessing(cursor)

    account = None
    while not account:
        print("Do you want to (1) log in or (2) sign up?")
        choice = input("Enter 1 for log in, 2 for sign up: ")
        if choice == '1':
            account = account_manager.login()
        elif choice == '2':
            account = account_manager.signup()

    clear_screen()
    print(f"Welcome, {account['FirstName']}!")
    customer_workflow(cursor, account, order_processor)
    cursor.close()
    db.close()

def customer_workflow(cursor, account, order_processor):
    """Customer workflow, where customers can view the menu, place orders, access their account or follow their order delivery."""
    while True:
        print("\nWhat would you like to do?")
        print("1. View Menu")
        print("2. Place an Order")
        print("3. View Account")
        print("4. Exit")
        option = input("Enter your choice: ")

        if option == '1':
            clear_screen()
            display_menu(cursor)
        elif option == '2':
            clear_screen()
            order_processor.order_items(account)
        elif option == '3':
            AccountManagement.view_account(cursor, account) 
            clear_screen()
        elif option == '4':
            print("Thank you for using Gusto d'Italia!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()