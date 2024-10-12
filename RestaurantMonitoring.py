import time
import os
from Database import connect

class RestaurantMonitoring:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_pending_pizza_orders(self):
        """
        Fetch all pending pizza orders that have been placed but not dispatched yet.

        :return: A list of tuples containing the order details.
        """
        self.cursor.execute("""
            SELECT o.OrderID, i.ItemName, oi.Quantity
            FROM `Order` o
            JOIN OrderItem oi ON o.OrderID = oi.OrderID
            JOIN Item i ON i.ItemID = oi.ItemID
            WHERE o.OrderStatus IN ('In processing', 'Being Prepared')
              AND oi.ItemID IN (SELECT ItemID FROM Item WHERE ItemType = 'Pizza')
            ORDER BY o.OrderPlacementTime ASC
        """)
        return self.cursor.fetchall()

    def display_pending_pizza_orders(self, refresh_interval=10):
        """
        Display a list of pending pizza orders in real-time, refreshing every few seconds (set to 10sec but can be changed)

        :param refresh_interval: The frequency to refresh the display (in seconds)
        """
        try:
            while True:
                # clear console
                os.system('cls' if os.name == 'nt' else 'clear')

                # fetch pending pizza orders
                pending_orders = self.get_pending_pizza_orders()

                # display the header
                print(f"{'Order ID':<10} {'Pizza name':<40} {'Quantity':<100}")
                print("-" * 70)

                # display orders
                if not pending_orders:
                    print("Currently there are no pending pizza orders :)")
                else:
                    for order in pending_orders:
                        order_id, pizza_name, quantity = order
                        print(f"{order_id:<10} {pizza_name:<40} {quantity:<100}")

                # wait until the next refresh
                time.sleep(refresh_interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

def main():
    db = connect()
    cursor = db.cursor()

    restaurant_monitoring = RestaurantMonitoring(cursor)
    restaurant_monitoring.display_pending_pizza_orders()

if __name__ == "__main__":
    main()