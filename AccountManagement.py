import datetime
import os

def clear_screen():
    if os.name == 'nt':  
        os.system('cls')
    else:  
        os.system('clear')

class AccountManagement:
    def __init__(self, cursor):
        self.cursor = cursor  

    def get_username(self):
        while True:
            username = input("Enter your username: ")
            if username:  
                return username
            print("Username cannot be empty. Please try again.")

    def get_password(self):
        while True:
            password = input("Enter your password: ")
            if password:  
                return password
            print("Password cannot be empty. Please try again.")

    def login(self):
        """ Customer login functionality. """
        attempts = 3 

        for _ in range(attempts):
            username = self.get_username()
            password = self.get_password()
        
            self.cursor.execute("""
                SELECT AccountID, Password FROM Account WHERE Username = %s
            """, (username,))
        
            result = self.cursor.fetchone()
        
            if result and result[1] == password:
                account_id = result[0]
                
                self.cursor.execute("""
                    SELECT CustomerID, FirstName FROM Customer WHERE AccountID = %s
                """, (account_id,))
                customer_result = self.cursor.fetchone()
                print("Login successful!")
                
                if customer_result:
                    customer_id = customer_result[0]
                    first_name = customer_result[1]
                    return {"AccountID": account_id, "CustomerID": customer_id, "FirstName": first_name}
                
            print("Incorrect username or password. Please try again.")
    
        print("Too many failed attempts. Program will exit now.")
        exit() 
        
    def signup(self):
        """ Customer sign-up functionality. """
        clear_screen()
        
        username = self.get_username()
        
        self.cursor.execute("SELECT * FROM Account WHERE Username = %s", (username,))
        if self.cursor.fetchone():
            print("Username already exists. Please choose a different one.")
            return
        
        password = self.get_password()
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")

        gender = input("Enter 'm' for male and 'f' for female: ").lower()
        while gender not in ['m', 'f']:
            print("Invalid input. Please enter 'm' for male or 'f' for female.")
            gender = input("Enter 'm' for male and 'f' for female: ").lower()
    
        while True:
            birthdate = input("Enter your birth date (YYYY-MM-DD): ")
            try:
                datetime.datetime.strptime(birthdate, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
        phone_number = input("Enter your phone number: ")
        
        try:
            self.cursor.execute("""
                INSERT INTO Account (Username, Password)
                VALUES (%s, %s)
            """, (username, password))
    
            account_id = self.cursor.lastrowid
    
            self.cursor.execute("""
                INSERT INTO Customer (AccountID, FirstName, LastName, Gender, Birthdate, Phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (account_id, first_name, last_name, gender, birthdate, phone_number))
    
            customer_id = self.cursor.lastrowid 

            self.cursor.connection.commit()
    
            print("Sign-up successful!")
            return {"AccountID": account_id, "CustomerID": customer_id, "FirstName": first_name}
        
        except Exception as e:
            print(f"Error during sign-up: {e}")
            self.cursor.connection.rollback()
    
    def check_address(self, account):
        customer_id = account['CustomerID']

        self.cursor.execute("""
            SELECT da.DeliveryAddressID, da.StreetName, da.HouseNumber, da.PostalCode
            FROM CustomerDeliveryAddress cda
            JOIN DeliveryAddress da ON cda.DeliveryAddressID = da.DeliveryAddressID
            WHERE cda.CustomerID = %s
        """, (customer_id,))
        address = self.cursor.fetchone()

        if address:
            print("Your current delivery address is:")
            print(f"Street: {address[1]}, House Number: {address[2]}, Postal Code: {address[3]}")
            change_address = input("Do you want to change your delivery address? (yes/no): ").strip().lower()

            if change_address == 'no':
                return {
                    "DeliveryAddressID": address[0], 
                    "StreetName": address[1], 
                    "HouseNumber": address[2], 
                    "PostalCode": address[3]
                }
            else:
                print("Please enter the new delivery address.")
        else:
            print("No delivery address found. Please provide your delivery address.")

        street_name = input("Street Name: ").strip()
        house_number = input("House Number: ").strip()
        postal_code = input("Postal Code: ").strip()

        self.cursor.execute("""
            SELECT AreaID FROM Area WHERE PostalCode = %s
        """, (postal_code,))
        area = self.cursor.fetchone()

        if not area:
            self.cursor.execute("""
                INSERT INTO Area (PostalCode) VALUES (%s)
            """, (postal_code,))
            area_id = self.cursor.lastrowid
        else:
            area_id = area[0]

        self.cursor.execute("""
            INSERT INTO DeliveryAddress (StreetName, HouseNumber, PostalCode)
            VALUES (%s, %s, %s)
        """, (street_name, house_number, postal_code))
        new_address_id = self.cursor.lastrowid

        self.cursor.execute("""
            INSERT INTO CustomerDeliveryAddress (CustomerID, DeliveryAddressID)
            VALUES (%s, %s)
        """, (customer_id, new_address_id))

        self.cursor.connection.commit()

        return {
            "DeliveryAddressID": new_address_id,
            "StreetName": street_name,
            "HouseNumber": house_number,
            "PostalCode": postal_code
        }


    def view_account(cursor, account):
        customer_id = account['CustomerID']
    
        cursor.execute("""
            SELECT a.Username, c.FirstName, c.LastName, c.Phone, c.Birthdate,
                da.StreetName, da.HouseNumber, da.PostalCode, c.NumberOfPizzas
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

            update_option = input("Would you like to update your phone number or delivery address? (phone/address/none): ").strip().lower()
        
            if update_option == "phone":
                new_phone = input("Enter new phone number: ").strip()
                AccountManagement.update_phone_number(cursor, customer_id, new_phone)
            elif update_option == "address":
                AccountManagement.check_address(cursor, account)
        else:
            print("Customer information not found.")

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
            SELECT c.MilestoneCount
            FROM Customer c
            WHERE c.CustomerID = %s
        """, (customer_id,))

        pizzas_missing = cursor.fetchone()

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

        if pizzas_missing and pizzas_missing[0] is not None:
            pizzas_missing = int(pizzas_missing[0])
        else:
            pizzas_missing = 0

        print(f"Pizza purchases: {pizzas_count}")

        if pizzas_missing == 0:
            print(f"Congratulations! You ordered 10 pizzas from us. Enjoy your 10% discount!")

            cursor.execute("""
                UPDATE Customer
                SET MilestoneCount = 10
                WHERE CustomerID = %s
            """, (customer_id,))

            return True
        else:
            print(f"Only {pizzas_missing} more pizzas to get a discount!")
            return False

