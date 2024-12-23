import pandas as pd  # Import pandas library for data manipulation
import csv  # Import csv library for handling CSV files
from datetime import datetime  # Import datetime for date handling
from data_entry import *  # Custom module for user input handling
import matplotlib.pyplot as plt


class CSV:
    # Define the CSV file and column structure
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Initialize the CSV file if it doesn't exist."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """Add a new transaction entry to the CSV file."""
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

        print("Entry added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Retrieve transactions within a given date range and display a summary."""
        # Read the CSV file into a DataFrame
        df = pd.read_csv(cls.CSV_FILE)
        # Ensure 'amount' is treated as numeric
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        # Convert 'date' column to datetime
        df['date'] = pd.to_datetime(df['date'], format=cls.FORMAT)
        # Parse input start_date and end_date
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        # Filter transactions within the date range
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            # Print the filtered transactions
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}:")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))

            # Summarize income, expense, and savings
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Income: {total_income:.2f}")
            print(f"Expense: {total_expense:.2f}")
            print(f"Net Saving: {(total_income - total_expense):.2f}")

        return filtered_df


def add():
    """Handle the addition of a new transaction."""
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or ENTER for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    """Plot income and expenses over time."""
    df.set_index('date', inplace=True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df['amount'], label='Income', color='g')
    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='r')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)

    # Ask user whether to save or show the plot
    choice = input("Do you want to save the plot? (y/n): ").lower()
    if choice == "y":
        plt.savefig("income_expense_plot.png")
        print("Plot saved as 'income_expense_plot.png'.")
    else:
        plt.show()


def main():
    """Main program loop to handle user choices."""
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            filtered_df = CSV.get_transactions(start_date, end_date)
            if not filtered_df.empty:
                plot_transactions(filtered_df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
