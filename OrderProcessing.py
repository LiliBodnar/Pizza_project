from datetime import datetime
import os
from Menu import display_menu
from AccountManagement import AccountManagement
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

    def print_order_summary(order_items, cursor, is_birthday, account, coupon_value):

        if not order_items:
            print("No items in your order.")
            return

        # Initialize total price
        total_price = Decimal('0.0')

        print("\n------------------ Order Summary ------------------")
        print(f"{'Item Name':<20} {'Quantity':<10} {'Price':<10} {'Total':<10}")
        print("-" * 60)

        # Loop through each item in the order
        for item_id, quantity in order_items:
            # Check if the item is a personalized pizza
            if item_id[0] == 9:
                # Extract ingredient IDs (flatten the list to just IDs)
                ingredient_ids = [ingr_id for ingr_id, _ in item_id[1]]  # Unpack the ingredient ID from the tuple

                # Generate query with placeholders
                placeholders = ', '.join(['%s'] * len(ingredient_ids))
                query = f""" 
                    SELECT i.IngredientName, i.Price 
                    FROM Ingredient i 
                    WHERE i.IngredientID IN ({placeholders})
                """
                cursor.execute(query, ingredient_ids)  # Pass the list of ingredient IDs (unpacked correctly)
                ingredients = cursor.fetchall()

                # Extract names and prices of selected ingredients
                ingredient_names = [ingredient[0] for ingredient in ingredients]
                ingredient_total_price = sum(ingredient[1] for ingredient in ingredients)

                # Apply 40% profit margin to the ingredient total price
                price_with_profit = Decimal(ingredient_total_price) * Decimal('1.40')

                # Calculate item total for the quantity ordered
                item_total = price_with_profit * Decimal(quantity)

                # Add to the total price
                total_price += item_total

                # Print each personalized pizza with the selected ingredients
                pizza_description = "Personalized Pizza"
                print(f"{pizza_description:<20} {quantity:<10} €{price_with_profit:.2f}  €{item_total:.2f}")

                # Print ingredients on a new line, indented for better formatting
                ingredients_line = ", ".join(ingredient_names)
                print(f"{'Ingredients:':<20} {ingredients_line}")

            else:
                # Fetch item details from the Item table for non-personalized pizzas
                cursor.execute("SELECT ItemName FROM Item WHERE ItemID = %s", (item_id[0],))
                item_name = cursor.fetchone()[0]

                # Fetch the total price for the item (based on ingredients)
                cursor.execute("""
                    SELECT SUM(i.Price) 
                    FROM IngredientList il 
                    JOIN Ingredient i ON il.IngredientID = i.IngredientID
                    WHERE il.ItemID = %s
                """, (item_id[0],))
                base_price = cursor.fetchone()[0] or Decimal('0.0')  # Handle missing prices

                # Apply 40% profit margin
                price_with_profit = base_price * Decimal('1.40')

                # Calculate item total for the quantity ordered
                item_total = price_with_profit * Decimal(quantity)

                # Add to the total price
                total_price += item_total

                # Print each item in the order with quantity, individual price, and total price
                print(f"{item_name:<20} {quantity:<10} €{price_with_profit:.2f}  €{item_total:.2f}")

        # Handle birthday bonus items
        if is_birthday:
            print("\n--- Birthday Bonus ---")
            for item_name in ['Margherita', 'Cola']:
                print(f"{item_name:<20} {'1':<10} €0.00  €0.00")

        # Check for milestone discount
        milestone = AccountManagement.check_pizza_milestone(cursor, account)
        milestone_discount = Decimal('0.0')
        if milestone:
            milestone_discount = total_price * Decimal('0.10')

        # Calculate coupon discount (if applicable)
        coupon_discount = Decimal('0.0')
        if coupon_value != 0.0:
            coupon_discount = Decimal(coupon_value) / Decimal('100.0') * total_price

        # Calculate total discounts
        total_discounts = milestone_discount + coupon_discount
        discounted_total = total_price - total_discounts

        # Apply 9% VAT
        vat = discounted_total * Decimal('0.09')

        # Calculate final total price
        final_price = discounted_total + vat

        # Print total price summary
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
            #OrderProcessing.place_order(cursor, account, items_ordered)
            print("Placing order")
        elif choice == '2':
            print("Going back to menu...")
        elif choice == '3':
            print("Thank you for using Gusto d'Italia!")
            exit()
