import datetime

class OrderProcessing:
    def __init__(self, cursor):
        self.cursor = cursor  # Save the cursor for database operations

    def place_order(self, customer_id, delivery_address_id, items):
        """
        Process a new order.
        
        :param customer_id: The ID of the customer placing the order.
        :param delivery_address_id: The ID of the delivery address.
        :param items: A list of tuples where each tuple contains (ItemID, Quantity).
        :return: Order ID of the placed order.
        """
        # 1. Insert the new order
        self.cursor.execute("""
            INSERT INTO `Order` (CustomerID, DeliveryAddressID, OrderStatus)
            VALUES (%s, %s, 'In processing')
        """, (customer_id, delivery_address_id))
        
        # Get the ID of the newly created order
        order_id = self.cursor.lastrowid

        # 2. Insert order items
        for item_id, quantity in items:
            self.cursor.execute("""
                INSERT INTO OrderItem (OrderID, ItemID, Quantity)
                VALUES (%s, %s, %s)
            """, (order_id, item_id, quantity))
        
        return order_id

    def update_order_status(self, order_id, new_status):
        """
        Update the status of an order.
        
        :param order_id: The ID of the order to update.
        :param new_status: The new status of the order.
        """
        self.cursor.execute("""
            UPDATE `Order`
            SET OrderStatus = %s
            WHERE OrderID = %s
        """, (new_status, order_id))
