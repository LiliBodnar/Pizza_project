from AccountManagement import AccountManagement  # Import the class for account management
from OrderProcessing import OrderProcessing  # Import the class for order processing
from DeliveryManagement import DeliveryManagement  # Import the class for delivery management
from Database import connect  # Import the function to connect to the database
from Menu import display_menu
import datetime
import os

def clear_screen():
    # Check the operating system and clear the screen accordingly
    if os.name == 'nt':  # 'nt' is for Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def main():
    print("Welcome to Gusto D'Italia!")
    db = connect()
    cursor = db.cursor()

    # Step 1: Account Management
    account_manager = AccountManagement(cursor)
    print("Do you want to (1) log in or (2) sign up?")
    choice = input("Enter 1 for log in, 2 for sign up: ")

    if choice == '1':
        account = account_manager.login()
    elif choice == '2':
        account = account_manager.signup()
    
    if account:
        clear_screen()
        print(f"Welcome, {account['FirstName']}!")
        print("")

        print("Choose the number of the option for how you would like to proceed")
        choice = input("(1) Menu    (2) Order    (3) Account    (4) Exit ->")

        if choice == '1':
            # Step 2: Display Menu
            clear_screen()
            display_menu(cursor)
        elif choice == '2':
            # Step 3: Place Order
            ##order_processor = OrderProcessing(cursor)
            ##items = [(1, 2), (2, 1)]  # Example items and quantities
            ##order_details = order_processor.place_order(account['CustomerID'], account['DeliveryAddressID'], items)
            print("")
        elif choice == '4':
            print("Thank you for choosing Gusto D'Italia!")
            cursor.close()
            db.close()
            exit()

        # Step 4: Manage Delivery
        ##delivery_manager = DeliveryManagement(cursor)
        ##delivery_status = delivery_manager.track_delivery(order_details)

        ##print(f"Your order status: {delivery_status}")
    
    print("Thank you for choosing Gusto D'Italia!")
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()