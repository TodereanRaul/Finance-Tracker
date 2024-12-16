# This file will collect the data from user
from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {
    "I": "Income",
    "E": "Expense"
}

def get_date(prompt, allow_default=False):
    # Prompt the user for a date input
    date_str = input(prompt)
    
    # If allowing default and no input is given, return today's date
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        # Attempt to parse the input string into a date object
        valid_date = datetime.strptime(date_str, date_format)
        # Return the date in the specified format
        return valid_date.strftime(date_format)
    
    except ValueError:
        # If the input is not a valid date, inform the user and prompt again
        print("Invalid date format. Please use DD-MM-YYYY")
        return get_date(prompt, allow_default)

def get_amount():
    # Start a try block to handle potential exceptions
    try:
        # Prompt the user to enter an amount and convert it to a float
        amount = float(input("Enter the amount: "))
        
        # Check if the entered amount is less than or equal to zero
        if amount <= 0:
            # Raise a ValueError if the amount is not a positive value
            raise ValueError("Amount must be a non-negative non-zero value.")
        
        # If the amount is valid, return it
        return amount
    
    # Catch any ValueError that occurs in the try block
    except ValueError as e:
        # Print the error message to inform the user of the issue
        print(e)
        
        # Recursively call get_amount() to prompt the user for input again
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. Please enter ('I' for Income or 'E' for Expense): ")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")