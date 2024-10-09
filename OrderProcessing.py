from datetime import datetime, timedelta
import os
import time
import threading
from Menu import display_menu
from AccountManagement import AccountManagement
from DeliveryManagement import DeliveryManagement
from decimal import Decimal

def clear_screen():
    # Check the operating system and clear the screen accordingly
    if os.name == 'nt':  # 'nt' is for Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

class OrderProcessing:
    def __init__(self, cursor):
        self.cursor = cursor  # Save the cursor for database operations

    
    def check_birthday(self, account):
        customer_id = account['CustomerID']

        self.cursor.execute("""
            SELECT Birthdate FROM Customer WHERE CustomerID = %s
        """, (customer_id,))
        birthdate = self.cursor.fetchone()[0]

        today = datetime.now().date()
        if birthdate and birthdate.month == today.month and birthdate.day == today.day:
            print("Happy Birthday! You get a free pizza and a drink.")
            return True
        return False
    
    def check_coupon(self, cursor, coupon_code):

        cursor.execute("""
            SELECT CouponCode, DiscountPercentage, ExpirationDate, Used 
            FROM Coupons 
            WHERE CouponCode = %s AND ExpirationDate >= CURDATE() AND Used = 0
        """, (coupon_code,))
        coupon = cursor.fetchone()

        if coupon:
            return {"CouponCode": coupon[0], "DiscountPercentage": coupon[1]}
        else:
            print("Invalid or expired coupon.")
            return None

    def calculate_order_details(order_items, cursor, is_birthday, account, coupon_value):
        if not order_items:
            return None, None, None, None  # Return None when no items in order

        # Initialize total price
        total_price = Decimal('0.0')

        item_details = []  # Store details for each item to be printed later

        # Loop through each item in the order
        for item_id, quantity in order_items:
            if item_id[0] == 9:  # Personalized pizza
                ingredient_ids = [ingr_id for ingr_id, _ in item_id[1]]

                # Generate query to fetch ingredients
                placeholders = ', '.join(['%s'] * len(ingredient_ids))
                query = f""" 
                    SELECT i.IngredientName, i.Price 
                    FROM Ingredient i 
                    WHERE i.IngredientID IN ({placeholders})
                """
                cursor.execute(query, ingredient_ids)
                ingredients = cursor.fetchall()

                ingredient_names = [ingredient[0] for ingredient in ingredients]
                ingredient_total_price = sum(ingredient[1] for ingredient in ingredients)

                # Apply 40% profit margin to ingredient total
                price_with_profit = Decimal(ingredient_total_price) * Decimal('1.40')
                item_total = price_with_profit * Decimal(quantity)

                total_price += item_total
                item_details.append({
                    'name': "Personalized Pizza",
                    'quantity': quantity,
                    'price': price_with_profit,
                    'item_total': item_total,
                    'ingredients': ingredient_names
                })
            else:  # Regular pizza
                cursor.execute("SELECT ItemName FROM Item WHERE ItemID = %s", (item_id[0],))
                item_name = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT SUM(i.Price) 
                    FROM IngredientList il 
                    JOIN Ingredient i ON il.IngredientID = i.IngredientID
                    WHERE il.ItemID = %s
                """, (item_id[0],))
                base_price = cursor.fetchone()[0] or Decimal('0.0')

                price_with_profit = base_price * Decimal('1.40')
                item_total = price_with_profit * Decimal(quantity)

                total_price += item_total
                item_details.append({
                    'name': item_name,
                    'quantity': quantity,
                    'price': price_with_profit,
                    'item_total': item_total
                })

        # Birthday bonus
        if is_birthday:
            item_details.append({'name': 'Margherita', 'quantity': 1, 'price': Decimal('0.00'), 'item_total': Decimal('0.00')})
            item_details.append({'name': 'Cola', 'quantity': 1, 'price': Decimal('0.00'), 'item_total': Decimal('0.00')})

        # Check for milestone discount
        milestone = AccountManagement.check_pizza_milestone(cursor, account)
        milestone_discount = total_price * Decimal('0.10') if milestone else Decimal('0.0')

        # Calculate coupon discount
        coupon_discount = (Decimal(coupon_value) / Decimal('100.0')) * total_price if coupon_value != 0.0 else Decimal('0.0')

        # Total discounts
        total_discounts = milestone_discount + coupon_discount
        discounted_total = total_price - total_discounts

        # Apply 9% VAT
        vat = discounted_total * Decimal('0.09')

        # Final total price
        final_price = discounted_total + vat

        return item_details, total_discounts, vat, final_price


    def print_order_summary(order_items, cursor, is_birthday, account, coupon_value):
        item_details, total_discounts, vat, final_price = OrderProcessing.calculate_order_details(order_items, cursor, is_birthday, account, coupon_value)

        if not item_details:
            print("No items in your order.")
            return

        print("\n------------------ Order Summary ------------------")
        print(f"{'Item Name':<20} {'Quantity':<10} {'Price':<10} {'Total':<10}")
        print("-" * 60)

        # Print details of each item
        for item in item_details:
            print(f"{item['name']:<20} {item['quantity']:<10} €{item['price']:.2f}  €{item['item_total']:.2f}")
            if 'ingredients' in item:
                ingredients_line = ", ".join(item['ingredients'])
                print(f"{'Ingredients:':<20} {ingredients_line}")

        print("-" * 60)
        print(f"{'Discounts:':<40} €{total_discounts:.2f}")
        print(f"{'VAT:':<40} €{vat:.2f}")
        print(f"{'Total Price:':<40} €{final_price:.2f}")
        print("---------------------------------------------------\n")


    def order_items(self, account):
        print("Place your order:")
        display_menu(self.cursor) 

        items_ordered = []

        while True:
            item_choice = int(input("Enter item number (or 0 to finish): "))
            if item_choice == 0:
                break

            if item_choice == 9:  # Personalized pizza
                print("\nYou chose a personalized pizza!")

                # Display base options (ingredients 1 and 2)
                print("\nChoose a base:")
                self.cursor.execute("SELECT IngredientID, IngredientName FROM Ingredient WHERE IngredientID IN (1, 2)")
                base_options = self.cursor.fetchall()

                for base in base_options:
                    print(f"{base[0]}. {base[1]}")

                base_choice = int(input("Enter base number: "))
                while base_choice not in [1, 2]:
                    print("Invalid base choice, please select a valid option.")
                    base_choice = int(input("Enter base number: "))

                # Add base to the ingredients list
                personalized_pizza_ingredients = [(base_choice, 1)]

                # Display topping options (ingredients 3 to 19)
                print("\nNow choose up to 5 toppings:")
                self.cursor.execute("SELECT IngredientID, IngredientName FROM Ingredient WHERE IngredientID BETWEEN 3 AND 19")
                topping_options = self.cursor.fetchall()

                toppings_chosen = []
                while len(toppings_chosen) < 5:
                    for topping in topping_options:
                        print(f"{topping[0]}. {topping[1]}")

                    topping_choice = int(input(f"Choose a topping (or 0 to finish): "))
                    if topping_choice == 0:
                        break
                    if topping_choice not in [t[0] for t in topping_options]:
                        print("Invalid topping choice, please select a valid option.")
                    elif topping_choice in toppings_chosen:
                        print("You've already selected this topping.")
                    else:
                        toppings_chosen.append(topping_choice)
                        personalized_pizza_ingredients.append((topping_choice, 1))

                # Ask for quantity of personalized pizza
                quantity = int(input("Enter the quantity of your personalized pizza: "))

                # Add personalized pizza to items_ordered (with quantity applied to all chosen ingredients)
                items_ordered.append(((9, personalized_pizza_ingredients), quantity))

                clear_screen()
                display_menu(self.cursor) 

            else:
                # For non-personalized items
                quantity = int(input("Enter quantity: "))
                items_ordered.append(((item_choice, 0), quantity))

        clear_screen()

        if items_ordered:
            # Show itemized list and total
            is_birthday = self.check_birthday(account)
            coupon_discount = Decimal('0.0')
            OrderProcessing.print_order_summary(items_ordered, self.cursor, is_birthday, account, coupon_discount)

            # Ask for a coupon code before proceeding with the final confirmation
            coupon_code = input("Enter a coupon code if you have one, or press Enter to skip: ").strip()
            coupon = None  # Initialize coupon as None

            if coupon_code:
                coupon = self.check_coupon(self.cursor, coupon_code)  # Validate coupon
                if coupon:
                    coupon_discount = coupon['DiscountPercentage']
                    print(f"Coupon applied! {coupon_discount}% discount.")
                    self.cursor.execute("UPDATE Coupons SET Used = 1 WHERE CouponCode = %s", (coupon_code,))
                else:
                    print("Proceeding without coupon.")
            

            print("\nOptions:")
            print("1. Proceed with order")
            print("2. Go back to menu and cancel order")
            print("3. Exit")
            choice = input("Enter your choice: ")

            clear_screen()

            if choice == '1':
                OrderProcessing.process_order(self.cursor, account, items_ordered, is_birthday, coupon_discount)
            elif choice == '2':
                print("Order cancelled. Returning to the main menu.")
            elif choice == '3':
                print("Thank you for using Gusto d'Italia!")
                exit()

    def process_order(cursor, account, items_ordered, is_birthday, coupon_discount):
        # Check for address and confirm delivery
        account_manager = AccountManagement(cursor)
        delivery_address = account_manager.check_address(account)

        clear_screen()

        print("Confirm total and delivery address:")
        OrderProcessing.print_order_summary(items_ordered, cursor, is_birthday, account, coupon_discount)
        print(f"Delivering to: {delivery_address['StreetName']} {delivery_address['HouseNumber']} {delivery_address['PostalCode']}")

        print("\n1. Proceed with order")
        print("2. Go back")
        print("3. Exit")
        choice = input("Enter your choice: ")

        clear_screen()

        if choice == '1':
            OrderProcessing.place_order(cursor, account, items_ordered, is_birthday, coupon_discount)
            print("Placing order")
        elif choice == '2':
            print("Going back to menu...")
        elif choice == '3':
            print("Thank you for using Gusto d'Italia!")
            exit()

    def place_order(cursor, account, items_ordered, is_birthday, coupon_discount):
        customer_id = account['CustomerID']

        cursor.execute("""
            SELECT cd.DeliveryAddressID
            FROM CustomerDeliveryAddress cd
            INNER JOIN Customer c ON c.CustomerID = cd.CustomerID
            WHERE c.CustomerID = %s
        """, (customer_id,))

        delivery_address = cursor.fetchone()  # Fetch one record

        order_details =OrderProcessing.calculate_order_details(items_ordered, cursor, is_birthday, account, coupon_discount)
        total_price = Decimal(order_details[3])
        print(total_price)
    
        # Step 1: Insert the order into the Order table
        cursor.execute("""
            INSERT INTO `Order` (CustomerID, DeliveryAddressID, OrderPlacementTime, TotalPrice)
            VALUES (%s, %s,NOW(), %s)
        """, (customer_id, delivery_address, total_price))

        cursor.connection.commit()
    
        # Retrieve the newly created OrderID
        order_id = cursor.lastrowid
    
        # Step 2: Insert order items into the OrderItem table
        for item in items_ordered:
            item_id = item[0][0]  # Either the item number or '9' for personalized pizza
            quantity = item[1]    # Quantity ordered
        
            # Insert the order item into OrderItem
            cursor.execute("""
                INSERT INTO OrderItem (OrderID, ItemID, Quantity)
                VALUES (%s, %s, %s)
            """, (order_id, item_id, quantity))
        
            # Retrieve the newly created OrderItemID
            order_item_id = cursor.lastrowid
        
            if item_id == 9:  # Personalized pizza
                for ingredient_id, ingr_quantity in item[0][1]:  # Unpack ingredient details
                    # Insert each ingredient of the personalized pizza
                    cursor.execute("""
                        INSERT INTO CustomPizzaIngredients (OrderItemID, IngredientID, Quantity)
                        VALUES (%s, %s, %s)
                    """, (order_item_id, ingredient_id, ingr_quantity))

        cursor.connection.commit()

        # Step 3: Insert the number of pizzas into Customer

        cursor.execute("""
            SELECT SUM(oi.Quantity)
            FROM `Order` o
            JOIN OrderItem oi ON o.OrderID = oi.OrderID
            WHERE o.OrderID = %s AND oi.ItemID IN (SELECT ItemID FROM Item WHERE ItemType = 'Pizza')
        """, (order_id,))

        number_of_pizzas = cursor.fetchone()
        print(number_of_pizzas[0])

        cursor.execute("""
                UPDATE Customer
                SET NumberOfPizzas = NumberOfPizzas + %s
                WHERE CustomerID = %s
            """, (number_of_pizzas[0], customer_id))
        
        cursor.connection.commit()

        delivery_manager = DeliveryManagement(cursor)

        print("Thank you for your order! You have 5 minutes to cancel your order.")
        

        # 4. Retrieve the order status and estimated delivery time
        #order_status_info = delivery_manager.get_order_status(order_id)

        # 5. Show order status, estimated delivery time, and cancellation window
        #if order_status_info:
            #print(f"Order Status: {order_status_info['OrderStatus']}")
            #print(f"Estimated Delivery Time: {order_status_info['EstimatedDeliveryTime']}")
            #print(f"Remaining Time to Cancel: {order_status_info['RemainingTime']}")

        # 6. Assign and group the order to a delivery person
        #assignment_message = delivery_manager.assign_and_group_orders(order_id)
        #print(assignment_message)
        #order_processor = OrderProcessing(cursor)

        # 7. Start a timer for cancellation, handling user input in a separate thread if needed
        #cancel_timer_thread = threading.Thread(target=order_processor.start_cancel_timer, args=(order_id,))
        #cancel_timer_thread.start()

        print(f"Your order {order_id} has been placed successfully!")
        return
    
    def start_cancel_timer(self, order_id):
        """
        Start a timer to handle order cancellation based on user input.

        :param order_id: The ID of the order to monitor for cancellation.
        """
        time.sleep(60)  # Wait for 5 minutes

        delivery_manager = DeliveryManagement(self.cursor)

        # After waiting, check if the order can still be canceled
        remaining_info = delivery_manager.get_order_status(order_id)
        if remaining_info and remaining_info['RemainingTime'] == "Thank you for ordering, the window for cancellation is now closed.":
            print("You can no longer cancel your order.")
        else:
            # Check if user wants to cancel the order
            user_input = input("Do you want to cancel your order? (yes/no): ")
            if user_input.lower() == 'yes':
                cancel_message = delivery_manager.cancel_order(order_id)
                print(cancel_message)

