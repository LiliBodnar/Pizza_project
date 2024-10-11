from AccountManagement import AccountManagement  # Import the class for account management
from OrderProcessing import OrderProcessing  # Import the class for order processing
from DeliveryManagement import DeliveryManagement  # Import the class for delivery management
from Database import connect  # Import the function to connect to the database
from Menu import display_menu
from RestaurantMonitoring import RestaurantMonitoring # Import the class for restaurant monitoring
from EarningsReport import EarningsReport # Import the class for earnings report
import datetime
import os

def clear_screen():
    # Check the operating system and clear the screen accordingly
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
    earnings_report = EarningsReport(cursor)
    delivery_manager = DeliveryManagement(cursor)

    # Check if it's an employee or a customer account
    if input("admin"):
        employee_workflow(cursor, earnings_report)
    else:
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
        customer_workflow(cursor, account, order_processor, delivery_manager)
    cursor.close()
    db.close()

def customer_workflow(cursor, account, order_processor, delivery_manager):
    """Customer workflow, where customers can view the menu, place orders, access their account or follow their order delivery."""
    while True:
        print("\nWhat would you like to do?")
        print("1. View Menu")
        print("2. Place an Order")
        print("3. Cancel order")
        print("4. Check order details")
        print("5. View Account")
        print("6. Exit")
        option = input("Enter your choice: ")

        if option == '1':
            clear_screen()
            display_menu(cursor)
        elif option == '2':
            clear_screen()
            order_processor.order_items(account)
            delivery_manager.assign_and_group_orders(cursor, account['CustomerID'])
        elif option == '3':
            delivery_manager.cancel_order(cursor)
            clear_screen()
        elif option == '4':
            delivery_manager.get_order_status(cursor, account['CustomerID'])
            break
        elif option == '5':
            AccountManagement.view_account(cursor, account) 
            clear_screen()
        elif option == '46':
            print("Thank you for using Gusto d'Italia!")
            break
        else:
            print("Invalid option. Please choose again.")

def employee_workflow(cursor, earnings_report):
    """Employee workflow, where employees can monitor orders and view the earnings report."""
    while True:
        print("\nWhat would you like to do?")
        print("1. View Pending Pizza Orders")
        print("2. View Monthly Earnings Report")
        print("3. Exit")
        option = input("Enter your choice: ")

        if option == '1':
            clear_screen()
            monitor = RestaurantMonitoring(cursor)
            monitor.display_pending_pizza_orders()
        elif option == '2':
            clear_screen()
            earnings_report.run()
        elif option == '3':
            print("Thank you for your work at Gusto d'Italia!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()