import datetime

class DeliveryManagement:
    def __init__(self, cursor):
        self.cursor = cursor  # Save the cursor for database operations

    def calculate_delivery_time(self, start_time, estimated_minutes):
        """
        Calculate the estimated delivery time based on the start time and estimated duration.
        
        :param start_time: The time the delivery starts (datetime object).
        :param estimated_minutes: Estimated delivery time in minutes.
        :return: Estimated delivery time (datetime object).
        """
        return start_time + datetime.timedelta(minutes=estimated_minutes)

    def assign_delivery_person(self, area_id):
        """
        Assign a delivery person based on the delivery area and availability.
        
        :param area_id: The AreaID where the delivery is needed.
        :return: DeliveryPersonID if available, None otherwise.
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
            delivery_person_id = result[0]
        
