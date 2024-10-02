from OrderProcessing import OrderProcessing
from AccountManagement import AccountManagement
from DeliveryManagement import DeliveryManagement
from Database import execute_query, fetch_results
import mysql.connector
import datetime

def display_menu():
    print("Menu:")
    items = fetch_results("SELECT ItemID, ItemName, Price FROM Item")  # Fetch items from the database
    if items:
        for item in items:
            print(f"{item[0]}: {item[1]} - ${item[2]:.2f}")

def main():
    print("Welcome to the Pizza Delivery System!")
    
    # Step 1: Account Management
    account_manager = AccountManagement()
    account = account_manager.login_or_create_account()

    if account:
        print(f"Welcome back, {account['Username']}!")
        
        # Step 2: Display Menu
        display_menu()
        
        # Assuming you have logic to capture delivery address ID and items
        delivery_address_id = 1  # Example ID, replace with actual logic
        items = [(1, 2), (2, 1)]  # Example items: (ItemID, Quantity)

        # Step 3: Place Order
        order_processor = OrderProcessing()
        order_details = order_processor.place_order(account['CustomerID'], delivery_address_id, items)

        # Step 4: Manage Delivery
        delivery_manager = DeliveryManagement()
        estimated_delivery_time = delivery_manager.calculate_delivery_time(datetime.datetime.now(), 30)  # Example: 30 minutes delivery time
        delivery_status = delivery_manager.track_delivery(order_details['OrderID'])

        print(f"Your order status: {delivery_status}")
        print(f"Estimated delivery time: {estimated_delivery_time}")
    
    print("Thank you for using the Pizza Delivery System!")

if __name__ == "__main__":
    main()