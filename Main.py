from AccountManagement import AccountManagement  # Import the class for account management
from OrderProcessing import OrderProcessing  # Import the class for order processing
from DeliveryManagement import DeliveryManagement  # Import the class for delivery management
from Database import connect  # Import the function to connect to the database
import datetime

def display_menu(cursor):
    # Fetch the menu items from the database
    cursor.execute("SELECT ItemID, ItemName, Price FROM Item")
    items = cursor.fetchall()

    print("Menu:")
    for item in items:
        print(f"{item[0]}: {item[1]} - ${item[2]}")

def main():
    print("Welcome to the Pizza Delivery System!")
    db = connect()
    cursor = db.cursor()

    # Step 1: Account Management
    account_manager = AccountManagement(cursor)
    print("Do you want to (1) log in or (2) sign up?")
    choice = input("Enter 1 for log in, 2 for sign up: ")

    if choice == '1':
        account = account_manager.login_or_create_account()
    elif choice == '2':
        account = account_manager.sign_up()
    
    if account:
        print(f"Welcome, {account['Username']}!")
        
        # Step 2: Display Menu
        display_menu(cursor)
        
        # Step 3: Place Order
        order_processor = OrderProcessing(cursor)
        items = [(1, 2), (2, 1)]  # Example items and quantities
        order_details = order_processor.place_order(account['CustomerID'], account['DeliveryAddressID'], items)

        # Step 4: Manage Delivery
        delivery_manager = DeliveryManagement(cursor)
        delivery_status = delivery_manager.track_delivery(order_details)

        print(f"Your order status: {delivery_status}")
    
    print("Thank you for using the Pizza Delivery System!")
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()