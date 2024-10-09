import matplotlib.pyplot as plt
import os
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

        # Return the profit, total earnings, and customer count
        return profit, total_price, total_customers, num_orders, num_items, num_pizzas
    
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

        # Ensure all months from 1 to 12 are included, filling with 0s for missing months
        all_months = list(range(1, 13))
        profits_dict = dict(zip(months, profit))  # Create a dict from months and profits
        num_orders_dict = dict(zip(months, num_orders))  # Create a dict from months and num_orders

        # Fill missing months with 0 profits and 0 orders
        profits = [profits_dict.get(m, 0.0) for m in all_months]
        num_orders = [num_orders_dict.get(m, 0) for m in all_months]

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

        # Return the months, profit, number of orders, and customer counts
        return all_months, profits, num_orders, total_male_customers, total_female_customers

    def display_earnings_report(self, report, month, year, gender, min_age, max_age):
        clear_screen()
        profit, total_earnings, total_customers, num_orders, num_items, num_pizzas = report
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

    def plot_earnings_report(self, report):

        profit, total_earnings, total_customers, num_orders, num_items, num_pizzas = report
        num_non_pizza = num_items - num_pizzas

        # Data for pie chart: pizzas vs. other items
        labels_items = ['Pizzas', 'Other Items']
        sizes_items = [num_pizzas, num_non_pizza]

        # Plotting the first pie chart for items
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
        plt.pie(sizes_items, labels=labels_items, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Pizzas vs. Other Items Ordered')

        # Show the plots
        plt.tight_layout()
        plt.show()

    def plot_yearly_earnings(self, report):
        months, profits, num_orders, total_male_customers, total_female_customers = report

        # Data for pie chart: male vs. female customers
        labels_customers = ['Male Customers', 'Female Customers']
        sizes_customers = [total_male_customers, total_female_customers]

        # Plotting the figures
        plt.figure(figsize=(12, 6))

        # Subplot for Profit
        plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
        plt.bar(months, profits, color='green')
        plt.xlabel('Month')
        plt.ylabel('Profit (€)')
        plt.title('Profit per Month')
        plt.xticks(months)  # Show month numbers on the x-axis

        # Subplot for Number of Orders
        plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
        plt.bar(months, num_orders, color='blue')
        plt.xlabel('Month')
        plt.ylabel('Number of Orders')
        plt.title('Number of Orders per Month')
        plt.xticks(months)  # Show month numbers on the x-axis

        # Adjust layout to fit pie chart
        plt.tight_layout()
        plt.show()

        # Plotting the pie chart for customer gender distribution
        plt.figure(figsize=(6, 6))  # New figure for pie chart
        plt.pie(sizes_customers, labels=labels_customers, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio
        plt.title('Customer Gender Distribution')
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
