import datetime

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


    def get_customer_id(self, account_id):
        """
        Get the CustomerID associated with the given AccountID.
        
        :param account_id: The ID of the account.
        :return: CustomerID if found, None otherwise.
        """
        self.cursor.execute("""
            SELECT CustomerID FROM Customer WHERE AccountID = %s
        """, (account_id,))
        
        result = self.cursor.fetchone()
        return result[0] if result else None

    def apply_discount(self, customer_id):
        """
        Check if the customer is eligible for a discount based on the number of pizzas they've ordered.
        
        :param customer_id: The ID of the customer.
        :return: Discount percentage (if any).
        """
        self.cursor.execute("""
            SELECT NumberOfPizzas FROM Customer WHERE CustomerID = %s
        """, (customer_id,))
        
        num_pizzas = self.cursor.fetchone()[0]
        
        if num_pizzas > 10:
            return 10  # 10% discount
        else:
            return 0  # No discount
