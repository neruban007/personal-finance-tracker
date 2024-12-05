import os
import csv
from datetime import datetime
import json
import matplotlib.pyplot as plt

class PersonalFinanceTracker:
    def __init__(self, data_file='finance_data.json'):
        """
        Initialize the Personal Finance Tracker
        
        Args:
            data_file (str): Path to the JSON file storing financial data
        """
        self.data_file = data_file
        self.transactions = self.load_data()

    def load_data(self):
        """
        Load existing financial data from JSON file
        
        Returns:
            list: List of financial transactions
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def save_data(self):
        """
        Save financial data to JSON file
        """
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=4)

    def add_transaction(self, amount, category, description, transaction_type):
        """
        Add a new financial transaction
        
        Args:
            amount (float): Transaction amount
            category (str): Transaction category
            description (str): Transaction description
            transaction_type (str): Either 'income' or 'expense'
        """
        transaction = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'amount': amount,
            'category': category,
            'description': description,
            'type': transaction_type
        }
        self.transactions.append(transaction)
        self.save_data()
        print("Transaction added successfully!")

    def generate_monthly_report(self):
        """
        Generate a monthly financial report with income, expenses, and balance
        
        Returns:
            dict: Monthly financial summary
        """
        monthly_summary = {}
        for transaction in self.transactions:
            month = transaction['date'][:7]
            if month not in monthly_summary:
                monthly_summary[month] = {'income': 0, 'expenses': 0}
            
            if transaction['type'] == 'income':
                monthly_summary[month]['income'] += transaction['amount']
            else:
                monthly_summary[month]['expenses'] += transaction['amount']
        
        return monthly_summary

    def visualize_expenses(self):
        """
        Create a pie chart of expenses by category
        """
        expense_categories = {}
        for transaction in self.transactions:
            if transaction['type'] == 'expense':
                category = transaction['category']
                amount = transaction['amount']
                expense_categories[category] = expense_categories.get(category, 0) + amount
        
        plt.figure(figsize=(10, 6))
        plt.pie(expense_categories.values(), labels=expense_categories.keys(), autopct='%1.1f%%')
        plt.title('Expense Distribution by Category')
        plt.axis('equal')
        plt.savefig('expense_breakdown.png')
        plt.close()
        print("Expense visualization saved as 'expense_breakdown.png'")

    def export_to_csv(self, filename='transactions.csv'):
        """
        Export all transactions to a CSV file
        
        Args:
            filename (str): Name of the CSV file to export
        """
        keys = self.transactions[0].keys() if self.transactions else []
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.transactions)
        print(f"Transactions exported to {filename}")

def main():
    tracker = PersonalFinanceTracker()

    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Monthly Report")
        print("4. Visualize Expenses")
        print("5. Export Transactions")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            amount = float(input("Enter income amount: "))
            category = input("Enter income category: ")
            description = input("Enter description: ")
            tracker.add_transaction(amount, category, description, 'income')

        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            description = input("Enter description: ")
            tracker.add_transaction(amount, category, description, 'expense')

        elif choice == '3':
            report = tracker.generate_monthly_report()
            for month, data in report.items():
                print(f"\nMonth: {month}")
                print(f"Total Income: ${data['income']:.2f}")
                print(f"Total Expenses: ${data['expenses']:.2f}")
                print(f"Balance: ${data['income'] - data['expenses']:.2f}")

        elif choice == '4':
            tracker.visualize_expenses()

        elif choice == '5':
            tracker.export_to_csv()

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Requirements
# pip install matplotlib
