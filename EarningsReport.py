import matplotlib.pyplot as plt
import os
import matplotlib.gridspec as gridspec
from decimal import Decimal
from Database import connect

def clear_screen():
    # Check the operating system and clear the screen accordingly
    if os.name == 'nt':  # 'nt' is for Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

class EarningsReport:
    def __init__(self, cursor):
        self.cursor = cursor 

    def generate_earnings_report(self, month, year, gender=None, min_age=None, max_age=None):
        # Query to get the total price from orders
        self.cursor.execute("""
            SELECT 
                SUM(o.TotalPrice),  -- Total price (includes VAT and profit)
                COUNT(DISTINCT c.CustomerID),
                COUNT(DISTINCT o.OrderID),
                SUM(oi.Quantity)
            FROM 
                `Order` o
            JOIN 
                Customer c ON o.CustomerID = c.CustomerID
            JOIN 
                OrderItem oi ON o.OrderID = oi.OrderID
            WHERE 
                MONTH(o.OrderPlacementTime) = %s 
                AND YEAR(o.OrderPlacementTime) = %s 
                AND (c.Gender = %s OR %s IS NULL)
                AND (TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN %s AND %s)
        """, (month, year, gender, gender, min_age, max_age))

        total_price, total_customers, num_orders, num_items = self.cursor.fetchone()

        total_price = total_price or 0.0

        # Step 1: Calculate ingredient cost
        ingredient_cost = total_price / Decimal(1.49)  # 1.40 profit margin and 1.09 VAT combined

        # Step 2: Calculate profit (40% margin)
        profit = ingredient_cost * Decimal(0.40)

        self.cursor.execute("""
            SELECT 
                SUM(oi.Quantity)
            FROM 
                OrderItem oi
            JOIN 
                `Order` o ON oi.OrderID = o.OrderID
            JOIN 
                Customer c ON o.CustomerID = c.CustomerID
            JOIN 
                Item i ON oi.ItemID = i.ItemID
            WHERE 
                MONTH(o.OrderPlacementTime) = %s 
                AND YEAR(o.OrderPlacementTime) = %s 
                AND (c.Gender = %s OR %s IS NULL)
                AND (TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN %s AND %s)
                AND i.ItemType = 'Pizza'
        """, (month, year, gender, gender, min_age, max_age))
        num_pizzas, = self.cursor.fetchone()

        self.cursor.execute("""
            SELECT 
                a.AreaID, 
                COUNT(DISTINCT c.CustomerID) as customer_count
            FROM 
                Customer c
            JOIN 
                `Order` o ON c.CustomerID = o.CustomerID
            JOIN 
                CustomerDeliveryAddress cda ON c.CustomerID = cda.CustomerID
            JOIN 
                DeliveryAddress da ON cda.DeliveryAddressID = da.DeliveryAddressID
            JOIN 
                Area a ON da.PostalCode = a.PostalCode
            WHERE 
                MONTH(o.OrderPlacementTime) = %s
                AND YEAR(o.OrderPlacementTime) = %s
                AND (c.Gender = %s OR %s IS NULL)
                AND (TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN %s AND %s)
            GROUP BY 
                a.AreaID
        """, (month, year, gender, gender, min_age, max_age))

        # Fetch all results
        area_distribution = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT 
                i.ItemName, 
                COUNT(oi.ItemID) AS item_count
            FROM 
                OrderItem oi
            JOIN 
                `Order` o ON oi.OrderID = o.OrderID
            JOIN 
                Customer c ON o.CustomerID = c.CustomerID
            JOIN 
                Item i ON oi.ItemID = i.ItemID
            WHERE 
                MONTH(o.OrderPlacementTime) = %s
                AND YEAR(o.OrderPlacementTime) = %s
                AND (c.Gender = %s OR %s IS NULL)
                AND (TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN %s AND %s)
                AND i.ItemType = 'Pizza'
            GROUP BY 
                i.ItemName
        """, (month, year, gender, gender, min_age, max_age))

        # Fetch all results
        pizza_distribution = self.cursor.fetchall()

        # Return the profit, total earnings, and customer count
        return profit, total_price, total_customers, num_orders, num_items, num_pizzas, area_distribution, pizza_distribution
    
    def generate_yearly_earnings_report(self, year): 
        self.cursor.execute("""
            SELECT 
                MONTH(o.OrderPlacementTime) AS month,
                SUM(o.TotalPrice) AS total_price,
                COUNT(DISTINCT o.OrderID) AS num_orders
            FROM 
                `Order` o
            JOIN 
                Customer c ON o.CustomerID = c.CustomerID
            JOIN 
                OrderItem oi ON o.OrderID = oi.OrderID
            WHERE
                YEAR(o.OrderPlacementTime) = %s
            GROUP BY 
                MONTH(o.OrderPlacementTime)
        """, (year,))

        # Fetch all results at once
        results = self.cursor.fetchall()

        # Initialize profit list
        total_received = []
        profit = []
        num_orders = []
        months = []

        for month, monthly_total, num_order in results:
            monthly_total = monthly_total or Decimal(0.0)  # Handle None case

            # Step 1: Calculate ingredient cost
            ingredient_cost = monthly_total / Decimal(1.49)  # 1.40 profit margin and 1.09 VAT combined

            # Step 2: Calculate profit (40% margin)
            monthly_profit = ingredient_cost * Decimal(0.40)

            # Append the month and profit
            months.append(month)
            profit.append(float(monthly_profit))  # Convert to float for plotting
            num_orders.append(num_order)
            total_received.append(float(monthly_total))

        # Ensure all months from 1 to 12 are included, filling with 0s for missing months
        all_months = list(range(1, 13))
        profits_dict = dict(zip(months, profit))  # Create a dict from months and profits
        total_received_dict = dict(zip(months, total_received))
        num_orders_dict = dict(zip(months, num_orders))  # Create a dict from months and num_orders

        # Fill missing months with 0 profits and 0 orders
        profits = [profits_dict.get(m, 0.0) for m in all_months]
        num_orders = [num_orders_dict.get(m, 0) for m in all_months]
        revenues = [total_received_dict.get(m, 0.0) for m in all_months]

        # Query for male customers
        self.cursor.execute("""
            SELECT COUNT(DISTINCT c.CustomerID)  
            FROM 
                Customer c
            JOIN 
                `Order` o ON c.CustomerID = o.CustomerID
            WHERE 
                c.Gender = 'm'
        """)
        total_male_customers = self.cursor.fetchone()[0] or 0  # Handle potential None

        # Query for female customers
        self.cursor.execute("""
            SELECT COUNT(DISTINCT c.CustomerID)  
            FROM 
                Customer c
            JOIN 
                `Order` o ON c.CustomerID = o.CustomerID
            WHERE 
                c.Gender = 'f'
        """)
        total_female_customers = self.cursor.fetchone()[0] or 0  # Handle potential None

        self.cursor.execute("""
            SELECT 
                a.AreaID, 
                COUNT(DISTINCT c.CustomerID) as customer_count
            FROM 
                Customer c
            JOIN 
                `Order` o ON c.CustomerID = o.CustomerID
            JOIN 
                CustomerDeliveryAddress cda ON c.CustomerID = cda.CustomerID
            JOIN 
                DeliveryAddress da ON cda.DeliveryAddressID = da.DeliveryAddressID
            JOIN 
                Area a ON da.PostalCode = a.PostalCode
            WHERE 
                YEAR(o.OrderPlacementTime) = %s
            GROUP BY 
                a.AreaID
        """, (year,))

        # Fetch all results
        area_distribution = self.cursor.fetchall()

        # Query for customer age distribution
        self.cursor.execute("""
            SELECT 
                CASE 
                    WHEN TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) < 18 THEN 'Under 18'
                    WHEN TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                    WHEN TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                    WHEN TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                    WHEN TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                    ELSE '56+' 
                END AS age_group,
                COUNT(DISTINCT c.CustomerID) as customer_count
            FROM 
                Customer c
            JOIN 
                `Order` o ON c.CustomerID = o.CustomerID
            WHERE 
                YEAR(o.OrderPlacementTime) = %s
            GROUP BY 
                age_group
        """, (year,))

        # Fetch results
        age_distribution = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT 
                i.ItemName, 
                COUNT(oi.ItemID) AS item_count
            FROM 
                OrderItem oi
            JOIN 
                `Order` o ON oi.OrderID = o.OrderID
            JOIN 
                Item i ON oi.ItemID = i.ItemID
            WHERE 
                YEAR(o.OrderPlacementTime) = %s AND
                i.ItemType = 'Pizza'
            GROUP BY 
                i.ItemName
        """, (year,))

        # Fetch all results
        pizza_distribution = self.cursor.fetchall()

        # Return the months, profit, number of orders, and customer counts
        return all_months, profits, num_orders, total_male_customers, total_female_customers, area_distribution, revenues, age_distribution, pizza_distribution

    def display_earnings_report(self, report, month, year, gender, min_age, max_age):
        clear_screen()
        profit, total_earnings, total_customers, num_orders, num_items, num_pizzas, area_distribution, pizza_distribution = report
        print("Monthly Earnings Report")
        print(f"Month: {month}| Year: {year}| Gender: {gender}| Min.age: {min_age}| Max.age: {max_age}")
        print("========================")
        print(f"Total Earnings: ${total_earnings:.2f}")
        print(f"Profit (40% margin): ${profit:.2f}")
        print(f"Total Customers: {total_customers}")
        print(f"Total Orders: {num_orders}")
        print(f"Total Items: {num_items}")
        print(f"Total Pizzas: {num_pizzas}")
        print("========================")

    def display_yearly_earnings_report(self, report, year):
        clear_screen()
        all_months, profits, num_orders, total_male_customers, total_female_customers, area_distribution, revenues, age_distribution, pizza_distribution = report

        total_revenue = sum(revenues)

        # Calculate total profit for the year
        total_profit = sum(profits)

        # Calculate total number of orders for the year
        total_orders = sum(num_orders)

        # Calculate total number of customers for the year (male + female)
        total_customers = total_male_customers + total_female_customers

        # Print the yearly report
        print(f"{year} Earnings Report")
        print("========================")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Total Profit: ${total_profit:.2f}")
        print(f"Total Number of Orders: {total_orders}")
        print(f"Total Number of Customers: {total_customers}")
        print("========================")

    def plot_earnings_report(self, report):

        profit, total_earnings, total_customers, num_orders, num_items, num_pizzas, area_distribution, pizza_distribution = report
        num_non_pizza = num_items - num_pizzas

        # Data for pie chart: pizzas vs. other items
        labels_items = ['Pizzas', 'Other Items']
        sizes_items = [num_pizzas, num_non_pizza]

        # Data for customer distribution by area
        area_ids = [f"Area {row[0]}" for row in area_distribution]  # Label by AreaID
        area_counts = [row[1] for row in area_distribution]

        pizza_labels = [row[0] for row in pizza_distribution]  # Item types (e.g., 'Pizza', 'Drink', 'Dessert')
        pizza_sizes = [row[1] for row in pizza_distribution]   # Counts of each type

        # Create a single figure for both pie charts
        plt.figure(figsize=(12, 10))  # Adjust size as needed

        # Plot the first pie chart (Pizzas vs Other Items)
        plt.subplot(2, 2, 1)  # 1 row, 2 columns, 1st subplot
        plt.pie(sizes_items, labels=labels_items, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Pizzas vs. Other Items Ordered')

        # Plot the second pie chart (Customer Distribution by Area)
        plt.subplot(2, 2, 2)  # 1 row, 2 columns, 2nd subplot
        plt.pie(area_counts, labels=area_ids, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Customer Distribution by Area')

        # Subplot 5: Pizza Type Distribution
        plt.subplot(2, 2, 3)  
        plt.pie(pizza_sizes, labels=pizza_labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Distribution of Pizza Types Ordered')

        # Use tight_layout to adjust spacing between plots
        plt.tight_layout()

        # Show both plots in one screen
        plt.show()

    def plot_yearly_earnings(self, report):
        months, profits, num_orders, total_male_customers, total_female_customers, area_distribution, revenues, age_distribution, pizza_distribution = report

        # Data for pie chart: male vs. female customers
        labels_customers = ['Male Customers', 'Female Customers']
        sizes_customers = [total_male_customers, total_female_customers]

        # Data for customer distribution by area
        area_ids = [f"Area {row[0]}" for row in area_distribution]  # Label by AreaID
        area_counts = [row[1] for row in area_distribution]

        # Data for age distribution
        age_groups = [row[0] for row in age_distribution]  # Age groups like '18-25', '26-35'
        age_counts = [row[1] for row in age_distribution]  # Number of customers in each age group

        pizza_labels = [row[0] for row in pizza_distribution]  # Item types (e.g., 'Pizza', 'Drink', 'Dessert')
        pizza_sizes = [row[1] for row in pizza_distribution]   # Counts of each type

        # Create a figure with a custom grid layout using GridSpec
        plt.figure(figsize=(20, 14))  # Increase the figure size for more space
        gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1.5])  # Create a GridSpec layout

        # Subplot 1: Profit per Month
        plt.subplot(gs[0, 0])  # 1st row, 1st column
        plt.bar(months, profits, color='green')
        plt.xlabel('Month')
        plt.ylabel('Profit (€)')
        plt.title('Profit per Month')
        plt.xticks(months)

        # Subplot 2: Number of Orders per Month
        plt.subplot(gs[0, 1])  # 1st row, 2nd column
        plt.bar(months, num_orders, color='blue')
        plt.xlabel('Month')
        plt.ylabel('Number of Orders')
        plt.title('Number of Orders per Month')
        plt.xticks(months)

        # Subplot 3: Customer Gender Distribution
        plt.subplot(gs[1, 0])  # 2nd row, 1st column
        plt.pie(sizes_customers, labels=labels_customers, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Customer Gender Distribution')

        # Subplot 4: Customer Distribution by Area
        plt.subplot(gs[1, 1])  # 2nd row, 2nd column
        plt.pie(area_counts, labels=area_ids, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Customer Distribution by Area')

        # Subplot 5: Customer Age Distribution (spanning across the full width of the 3rd row)
        plt.subplot(gs[2, 0])  # 3rd row, spanning both columns
        plt.pie(age_counts, labels=age_groups, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Customer Age Distribution')

        plt.subplot(gs[2,1]) 
        plt.pie(pizza_sizes, labels=pizza_labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Distribution of Pizza Types Ordered')

        # Adjust layout to prevent overlap and provide spacing
        plt.subplots_adjust(wspace=0.3, hspace=0.4)  # Adjust space between plots

        # Show the complete plot
        plt.show()


    def get_user_input(self):
        # Get inputs from the user for month, year, and filters
        try:
            month = int(input("Enter the month (1-12): "))
            year = int(input("Enter the year (e.g., 2024): "))
            gender = input("Enter gender (m or f) or leave blank for all: ").strip() or None
            min_age = input("Enter minimum age or leave blank: ").strip() or None
            max_age = input("Enter maximum age or leave blank: ").strip() or None

            if min_age:
                min_age = int(min_age)
            else:
                min_age = 0  # Default minimum age

            if max_age:
                max_age = int(max_age)
            else:
                max_age = 100  # Default maximum age

            return month, year, gender, min_age, max_age
        except ValueError:
            print("Invalid input. Please try again.")
            return None

    def run(self):
        # Main interaction flow
        choice = int(input("Choose 1 for a monthly report and 2 for a yearly report: "))

        if choice == 1:
            user_input = self.get_user_input()
            if user_input:
                month, year, gender, min_age, max_age = user_input
                report = self.generate_earnings_report(month, year, gender, min_age, max_age)
                self.display_earnings_report(report, month, year, gender, min_age, max_age)
                self.plot_earnings_report(report)
        elif choice == 2:
            year = int(input("Year(e.g., 2024): "))
            clear_screen()
            report = self.generate_yearly_earnings_report(year)
            self.display_yearly_earnings_report(report, year)
            self.plot_yearly_earnings(report)
        else:
            print("Wrong input")


def main():
    db = connect()  # Your DB connection function
    cursor = db.cursor()

    earnings_report = EarningsReport(cursor)
    earnings_report.run()


if __name__ == "__main__":
    main()
