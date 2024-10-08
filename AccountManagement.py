import datetime
import os

def clear_screen():
    # Check the operating system and clear the screen accordingly
    if os.name == 'nt':  # 'nt' is for Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

class AccountManagement:
    def __init__(self, cursor):
        self.cursor = cursor  # Save the cursor for database operations

    def login(self):
        """
        Customer login functionality.
    
        Allows three attempts to enter correct username and password.
        Ends the program if all attempts are incorrect.
        """
        attempts = 3  # Allow three attempts

        for _ in range(attempts):
            username = input("Enter your username: ")
            password = input("Enter your password: ")
        
            # Query to check if username and password match
            self.cursor.execute("""
                SELECT AccountID, Password FROM Account WHERE Username = %s
            """, (username,))
        
            result = self.cursor.fetchone()
        
            if result and result[1] == password:
                account_id = result[0]
                # Fetch the customer's first name
                self.cursor.execute("""
                    SELECT CustomerID, FirstName FROM Customer WHERE AccountID = %s
                """, (account_id,))
                customer_result = self.cursor.fetchone()
                print("Login successful!")
                
                if customer_result:
                    customer_id = customer_result[0]
                    first_name = customer_result[1]
                    return {"AccountID": account_id, "CustomerID": customer_id, "FirstName": first_name}
                
            else:
                print("Incorrect username or password. Please try again.")
    
        print("Too many failed attempts. Program will exit now.")
        exit()  # End the program after 3 failed attempts
        
    def signup(self):
        """
        Customer sign-up functionality.
    
        Collect user details and create new account and customer records in the database.
        """
        clear_screen()
        
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
    
        # Ensure valid gender input
        gender = input("Enter 'm' for male and 'f' for female: ").lower()
        while gender not in ['m', 'f']:
            print("Invalid input. Please enter 'm' for male or 'f' for female.")
            gender = input("Enter 'm' for male and 'f' for female: ").lower()
    
        # Validate birthdate format (YYYY-MM-DD)
        birthdate = input("Enter your birth date (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return
    
        phone_number = input("Enter your phone number: ")
        
        try:
            # 1. Create an Account record
            self.cursor.execute("""
                INSERT INTO Account (Username, Password)
                VALUES (%s, %s)
            """, (username, password))
    
            account_id = self.cursor.lastrowid  # Get the newly created AccountID
    
            # 2. Create a Customer record linked to the Account
            self.cursor.execute("""
                INSERT INTO Customer (AccountID, FirstName, LastName, Gender, Birthdate, Phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (account_id, first_name, last_name, gender, birthdate, phone_number))
    
            customer_id = self.cursor.lastrowid  # Get the newly created CustomerID

            self.cursor.connection.commit()
    
            print("Sign-up successful!")
            return {"AccountID": account_id, "CustomerID": customer_id, "FirstName": first_name}
        
        except Exception as e:
            print(f"Error during sign-up: {e}")
            self.cursor.connection.rollback()

    
    def check_address(self, account):
        customer_id = account['CustomerID']

        # Check if the customer already has a delivery address
        self.cursor.execute("""
            SELECT da.DeliveryAddressID, da.StreetName, da.HouseNumber, da.PostalCode
            FROM CustomerDeliveryAddress cda
            JOIN DeliveryAddress da ON cda.DeliveryAddressID = da.DeliveryAddressID
            WHERE cda.CustomerID = %s
        """, (customer_id,))
        address = self.cursor.fetchone()

        if address:
            # Address exists, ask the customer if they want to keep or change it
            print("Your current delivery address is:")
            print(f"Street: {address[1]}, House Number: {address[2]}, Postal Code: {address[3]}")
            change_address = input("Do you want to change your delivery address? (yes/no): ").strip().lower()

            if change_address == 'no':
                # Return the existing address as a dictionary, accessed via indices
                return {
                    "DeliveryAddressID": address[0], 
                    "StreetName": address[1], 
                    "HouseNumber": address[2], 
                    "PostalCode": address[3]
                }
            else:
                print("Please enter the new delivery address.")
        else:
            # No address found, ask for a new one
            print("No delivery address found. Please provide your delivery address.")

        # Ask for new address details
        street_name = input("Street Name: ").strip()
        house_number = input("House Number: ").strip()
        postal_code = input("Postal Code: ").strip()

        # Check if postal code exists in the Area table
        self.cursor.execute("""
            SELECT AreaID FROM Area WHERE PostalCode = %s
        """, (postal_code,))
        area = self.cursor.fetchone()

        if not area:
            # Insert the postal code into the Area table if it doesn't exist
            self.cursor.execute("""
                INSERT INTO Area (PostalCode) VALUES (%s)
            """, (postal_code,))
            area_id = self.cursor.lastrowid
        else:
            area_id = area[0]

        # Insert the new address into the DeliveryAddress table
        self.cursor.execute("""
            INSERT INTO DeliveryAddress (StreetName, HouseNumber, PostalCode)
            VALUES (%s, %s, %s)
        """, (street_name, house_number, postal_code))
        new_address_id = self.cursor.lastrowid

        # Link the new address to the customer in CustomerDeliveryAddress
        self.cursor.execute("""
            INSERT INTO CustomerDeliveryAddress (CustomerID, DeliveryAddressID)
            VALUES (%s, %s)
        """, (customer_id, new_address_id))

        self.cursor.connection.commit()

        # Return the new address information
        return {
            "DeliveryAddressID": new_address_id,
            "StreetName": street_name,
            "HouseNumber": house_number,
            "PostalCode": postal_code
        }


    def view_account(cursor, account):
        customer_id = account['CustomerID']
    
        # Fetch the customer details and associated delivery address
        cursor.execute("""
            SELECT a.Username, c.FirstName, c.LastName, c.Phone, c.Birthdate,
                da.StreetName, da.HouseNumber, da.PostalCode, c.NumerOfPizzas
            FROM Customer c
            JOIN Account a ON c.AccountID = a.AccountID
            LEFT JOIN CustomerDeliveryAddress cda ON c.CustomerID = cda.CustomerID
            LEFT JOIN DeliveryAddress da ON cda.DeliveryAddressID = da.DeliveryAddressID
            WHERE c.CustomerID = %s
        """, (customer_id,))
    
        customer_info = cursor.fetchone()

        if customer_info:
            username, first_name, last_name, phone, birthdate, street, house_number, postal_code, number_of_pizzas = customer_info

            print(f"Username: {username}")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Phone Number: {phone}")
            print(f"Birthdate: {birthdate}")
            if street and house_number and postal_code:
                print(f"Delivery Address: {street}, {house_number}, Postal Code: {postal_code}")
            else:
                print("No delivery address found.")

            # Call the function to display pizza milestone
            AccountManagement.check_pizza_milestone(cursor, account)

            # Offer options to update phone or address
            update_option = input("Would you like to update your phone number or delivery address? (phone/address/none): ").strip().lower()
        
            if update_option == "phone":
                new_phone = input("Enter new phone number: ").strip()
                AccountManagement.update_phone_number(cursor, customer_id, new_phone)
            elif update_option == "address":
                AccountManagement.check_address(cursor, account)
        else:
            print("Customer information not found.")

    # Update phone number function
    def update_phone_number(cursor, customer_id, new_phone):
        cursor.execute("""
            UPDATE Customer
            SET Phone = %s
            WHERE CustomerID = %s
        """, (new_phone, customer_id))
        print("Phone number updated successfully.")

    def check_pizza_milestone(cursor, account):
        customer_id = account['CustomerID']

        cursor.execute("""
            SELECT c.NumberOfPizzas
            FROM Customer c
            WHERE c.CustomerID = %s
        """, (customer_id,))

        pizzas = cursor.fetchone()

        if pizzas and pizzas[0] is not None:
            pizzas_count = int(pizzas[0])
        else:
            pizzas_count = 0

        # Calculate the milestone dynamically
        milestone = ((pizzas_count // 10) + 1) * 10
        pizzas_to_go = milestone - pizzas_count
    
        print(f"Pizza purchases: {pizzas_count}/{milestone}")
    
        if pizzas_to_go == 0:
            print(f"Congratulations! You've reached {milestone} pizzas. Enjoy your discount!")
            return True
        else:
            print(f"Only {pizzas_to_go} more pizzas to reach {milestone} pizzas for a discount!")
            return False


