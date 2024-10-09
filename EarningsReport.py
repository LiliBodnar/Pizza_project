import matplotlib.pyplot as plt
from Database import connect

class EarningsReport:
    def __init__(self, cursor):
        self.cursor = cursor 

    def generate_earnings_report(self, month, year, gender=None, min_age=None, max_age=None):
        # Query to get the total price from orders
        self.cursor.execute("""
            SELECT 
                SUM(o.TotalPrice),  -- Total price (includes VAT and profit)
                COUNT(DISTINCT c.CustomerID)
            FROM 
                `Order` o
            JOIN 
                Customer c ON o.CustomerID = c.CustomerID
            WHERE 
                MONTH(o.OrderPlacementTime) = %s 
                AND YEAR(o.OrderPlacementTime) = %s 
                AND (c.Gender = %s OR %s IS NULL)
                AND (TIMESTAMPDIFF(YEAR, c.Birthdate, CURDATE()) BETWEEN %s AND %s)
        """, (month, year, gender, gender, min_age, max_age))

        total_price, total_customers = self.cursor.fetchone()

        # Step 1: Calculate ingredient cost
        ingredient_cost = total_price / 1.49  # 1.40 profit margin and 1.09 VAT combined

        # Step 2: Calculate profit (40% margin)
        profit = ingredient_cost * 0.40

        # Return the profit, total earnings, and customer count
        return profit, total_price, total_customers

    def display_earnings_report(self, report):
        profit, total_earnings, total_customers = report
        print("Monthly Earnings Report")
        print("========================")
        print(f"Total Earnings: ${total_earnings:.2f}")
        print(f"Profit (40% margin): ${profit:.2f}")
        print(f"Total Customers: {total_customers}")
        print("========================")

    def plot_earnings_report(self, report):
        # Plot a bar chart for the total earnings (without VAT) vs. profit
        months = [f"{row[0]}/{row[1]}" for row in report]  # Month/Year format
        total_earnings = [row[2] for row in report]

        plt.figure(figsize=(10, 5))
        plt.bar(months, total_earnings, color='skyblue')
        plt.title('Monthly Earnings Report')
        plt.xlabel('Month/Year')
        plt.ylabel('Total Earnings ($)')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def get_user_input(self):
        # Get inputs from the user for month, year, and filters
        try:
            month = int(input("Enter the month (1-12): "))
            year = int(input("Enter the year (e.g., 2024): "))
            gender = input("Enter gender (male, female, other) or leave blank for all: ").strip() or None
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
        user_input = self.get_user_input()
        if user_input:
            month, year, gender, min_age, max_age = user_input
            report = self.generate_earnings_report(month, year, gender, min_age, max_age)
            self.display_earnings_report(report)


def main():
    db = connect()  # Your DB connection function
    cursor = db.cursor()

    earnings_report = EarningsReport(cursor)
    earnings_report.run()


if __name__ == "__main__":
    main()
