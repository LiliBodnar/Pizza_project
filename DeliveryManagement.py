import threading
import time
import datetime
import os

def clear_screen():
    if os.name == 'nt':  
        os.system('cls')
    else: 
        os.system('clear')

class DeliveryManagement:
    def __init__(self, cursor):
        self.cursor = cursor  

    def get_order_status(self, order_id):
        """
        Retrieve the current status of the order, its estimated delivery time and the window for order cancellation.
        
        :param order_id: The ID of the order.
        :return: Dictionary with 'OrderStatus', 'EstimatedDeliveryTime' and "RemainingTime" to cancel order.
        """
        self.cursor.execute("""
            SELECT o.OrderStatus, o.OrderPlacementTime, od.EstimatedDeliveryTime
            FROM `Order` o
            LEFT JOIN OrderDelivery od ON o.OrderID = od.OrderID
            WHERE o.OrderID = %s
        """, (order_id,))
        
        result = self.cursor.fetchone()
        
        if result:
            order_status, start_time, estimated_delivery_time = result
            
            order_status, start_time, estimated_delivery_time = result
            if start_time:
                
                time_elapsed = (datetime.datetime.now() - start_time).total_seconds()
                
                time_remaining_seconds = max(0, 300 - time_elapsed) 
                
                if time_remaining_seconds > 0:
                    minutes, seconds = divmod(int(time_remaining_seconds), 60)
                    time_remaining_str = f"{minutes:02}:{seconds:02}"
                else:
                    time_remaining_str = "Thank you for ordering, the window for cancellation is now closed."
            else:
                time_remaining_str = "05:00"
        print(f"Order Status: {order_status}")
        print(f"Estimated Delivery Time: {estimated_delivery_time}")

        if not result:
            print(f"We couldn't find your order: {order_id}")
        return None
    
    def cancel_order(self, order_id):
        """
        Cancel the order if it was placed within 5 minutes and update the delivery person's availability.
        
        :param order_id: The ID of the order.
        :return: Status message indicating wheter tha cancellation was successful.
        """
        self.cursor.execute("""
            SELECT OrderStatus, OrderPlacementTime
            FROM `Order`
            WHERE OrderID = %s
        """, (order_id,))
        
        order_data = self.cursor.fetchone()
        
        if not order_data:
            return (f"We couldn't find your order: {order_id}")

        order_status, order_placement_time = order_data

        if order_status in ['On the way', 'Delivered']:
            return "Order cannot be canceled at this stage."


        if (datetime.datetime.now() - order_placement_time).total_seconds() < 300 :
        
            self.cursor.execute("""
                UPDATE `Order`
                SET OrderStatus = 'Cancelled'
                WHERE OrderID = %s
            """, (order_id,))
        else:
            return "Order cannot be canceled as the window for cancellation is closed."        

        self.cursor.execute("""
                SELECT SUM(oi.Quantity), o.CustomerID
                FROM `Order` o
                JOIN OrderItem oi ON o.OrderID = oi.OrderID
                JOIN Customer c ON o.CustomerID = c.CustomerID
                WHERE o.OrderID = %s AND ItemID IN (SELECT ItemID FROM Item WHERE ItemType = 'Pizza')
            """, (order_id,))

        number_of_pizzas, customer_id = self.cursor.fetchone()

        self.cursor.execute("""
                UPDATE Customer
                SET NumberOfPizzas = NumberOfPizzas - %s
                WHERE CustomerID = %s
            """, (number_of_pizzas, customer_id))

        self.cursor.connection.commit()
        
        print("Order has been successfully canceled.")
        return

    def assign_and_group_orders(self, order_id):
        """
        Assign and group orders based on the number of pizzas and proximity of order placement time.
        
        :param order_id: The ID of the current order to assign.
        :return: Message wheter the order was successfully assigned or not.
        """
        
        self.cursor.execute("""
            SELECT SUM(oi.Quantity) AS PizzaCount, o.OrderPlacementTime, a.AreaID
            FROM `Order` o
            JOIN OrderItem oi ON o.OrderID = oi.OrderID
            JOIN DeliveryAddress da ON o.DeliveryAddressID = da.DeliveryAddressID
            JOIN AreaPostalCode a ON da.PostalCode = a.PostalCode
            WHERE o.OrderID = %s AND oi.ItemID IN (SELECT ItemID FROM Item WHERE ItemType = 'Pizza')
        """, (order_id,))
        
        order_details = self.cursor.fetchone()
        
        pizza_count, order_placement_time, area_id = order_details
        if pizza_count is None:
            pizza_count = 0 

        if not order_details:
             print("Order not found.")
       
        
        if pizza_count >= 3:
            delivery_person_id = self.find_available_delivery_person(area_id)
            if delivery_person_id:
                self.assign_order_to_delivery_person(order_id, delivery_person_id)
                print(f"Order {order_id} was assigned to delivery person {delivery_person_id}.")
            else:
                print("Sorry, currently no delivery person is available in this area.")

        
        self.cursor.execute("""
            SELECT o.OrderID, SUM(oi.Quantity) AS PizzaCount
            FROM `Order` o
            JOIN OrderItem oi ON o.OrderID = oi.OrderID
            JOIN DeliveryAddress da ON o.DeliveryAddressID = da.DeliveryAddressID
            WHERE o.OrderStatus = 'On the way' 
              AND da.PostalCode IN (SELECT PostalCode FROM AreaPostalCode WHERE AreaID = %s) 
              AND ABS(TIMESTAMPDIFF(MINUTE, o.OrderPlacementTime, %s)) <= 3
              AND oi.ItemID IN (SELECT ItemID FROM Item WHERE ItemType = 'Pizza')
            GROUP BY o.OrderID
        """, (area_id, order_placement_time))

        matching_orders = self.cursor.fetchall()

        
        for matched_order_id, matched_pizza_count in matching_orders:
            if order_id != matched_order_id and pizza_count + matched_pizza_count <= 3:
                self.cursor.execute("""
                    SELECT DeliveryPersonID
                    FROM OrderDelivery
                    WHERE OrderID = %s
                """, (matched_order_id,))
                delivery_person_id = self.cursor.fetchone()
                if delivery_person_id:
                    
                    self.assign_order_to_delivery_person(order_id, delivery_person_id)
                    print(f"Order {order_id} was assigned to delivery person {delivery_person_id} together with order {matched_order_id}")
 #TODO DELETE "together with order {matched_order_id}" FROM RETURN MESSAGE AFTER TESTING

        
        delivery_person_id = self.find_available_delivery_person(area_id)
        if delivery_person_id:
            self.assign_order_to_delivery_person(order_id, delivery_person_id)
            print(f"Order {order_id} assigned to delivery person {delivery_person_id}.")
        
        return "Sorry, currently no delivery person available in this area. Please wait."

    def find_available_delivery_person(self, area_id):
        """
        Find an available delivery person in a given area.
        
        :param area_id: Area code to search for available delivery persons.
        :return: DeliveryPersonID if available or None otherwise.
        """
        self.cursor.execute("""
            SELECT dp.DeliveryPersonID
            FROM DeliveryPerson dp
            JOIN DeliveryPersonArea dpa ON dp.DeliveryPersonID = dpa.DeliveryPersonID
            WHERE dpa.AreaID = %s AND dp.Availability = 'Available'
            LIMIT 1
        """, (area_id,))
        
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def assign_order_to_delivery_person(self, order_id, delivery_person_id):
        """
        Assign an order to a specific delivery person and update their availability.
        
        :param order_id: The ID of the order to assign.
        :param delivery_person_id: The ID of the delivery person to whom the order will be assigned.
        """
        
        self.cursor.execute("""
            INSERT INTO OrderDelivery (OrderID, DeliveryPersonID, DeliveryStartTime, EstimatedDeliveryTime)
            VALUES (%s, %s, %s, %s)
        """, (order_id, delivery_person_id, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(minutes=30)))

        
        self.cursor.execute("""
            UPDATE `Order`
            SET OrderStatus = 'On the way'
            WHERE OrderID = %s
        """, (order_id,))

        
        self.cursor.execute("""
            UPDATE DeliveryPerson
            SET Availability = 'Not available'
            WHERE DeliveryPersonID = %s
        """, (delivery_person_id,))

        self.cursor.connection.commit()

        delivery_thread = threading.Thread(target=self.update_delivery_status, args=(order_id, delivery_person_id))
        delivery_thread.start()

    def update_delivery_status(self, order_id, delivery_person_id):
        """
        Automatically updates deliveries status after the delivery time has passed.
        """
        time.sleep(2 * 20)  # 30-minute delivery time
        clear_screen()
      
        self.cursor.execute("""
            UPDATE `Order`
            SET OrderStatus = 'Delivered'
            WHERE OrderID = %s
        """, (order_id,))

        self.cursor.execute("""
            UPDATE DeliveryPerson
            SET Availability = 'Available'
            WHERE DeliveryPersonID = %s
            AND NOT EXISTS (
                SELECT 1 
                FROM OrderDelivery od
                JOIN `Order` o ON o.OrderID = od.OrderID
                WHERE od.DeliveryPersonID = %s
                AND o.OrderStatus = 'On the way'
                AND o.OrderID != %s
            )                           
        """, (delivery_person_id, delivery_person_id, order_id))

        self.cursor.connection.commit()
        print(f"Order {order_id} has been delivered.")
        print('Enter 2 to exit: ')



    # ORDER LIFELINE
    # take order: default: 'In processing'
    # 0.min:   'Being prepared' -> odred confirmed
    # 0-5min:  'Being prepared' -> cancellation available
    # 5-10min: 'Being prepared' -> cancellation no longer available
    # 10.min:  'On the way' -> assign to delivery person (change delivery person's availability)
    #  -> check for number of pizzas: n
    #  -> if n>=3 : assign order directly to a delivery person
    #  -> else: check for area code and previous orders placed WITHIN 3min
    #       -> check pizza count: m
    #       -> if n+m<=3 : assign second order to that delivery person
    #       -> else: assign order to a delivery person
    # 10-40min: 'On the way' -> delivery
    # 40.min  : 'Delivered'  -> 1. change order status (automatically by scheduler -updated every minute)
    #                        -> 2. change back delivery person's availability (automatically by scheduler)
