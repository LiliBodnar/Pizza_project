class AccountManagement:
    def __init__(self, cursor):
        self.cursor = cursor  # Save the cursor for database operations

    def login(self, username, password):
        """
        Customer login functionality.
        
        :param username: The username of the customer.
        :param password: The password of the customer.
        :return: A dictionary with AccountID and CustomerID if login is successful, None otherwise.
        """
        self.cursor.execute("""
            SELECT AccountID, Password FROM Account WHERE Username = %s
        """, (username,))
        
        result = self.cursor.fetchone()
        
        if result and result[1] == password:
            # Assuming you need to get the CustomerID as well
            account_id = result[0]
            customer_id = self.get_customer_id(account_id)
            return {"AccountID": account_id, "CustomerID": customer_id}  # Return both AccountID and CustomerID
        else:
            return None

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
