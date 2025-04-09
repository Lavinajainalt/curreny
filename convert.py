import os
import time
import sys
import json
from getpass import getpass

USER_DB_FILE = "users.json"

CURRENCY_RATES = {
    'USD': 1.00,
    'EUR': 0.91,
    'GBP': 0.79,
    'JPY': 148.42,
    'AUD': 1.52,
    'CAD': 1.35,
    'CHF': 0.87,
    'CNY': 7.19,
    'INR': 83.12,
    'NZD': 1.64

}

def cls():
    """Clear the screen and return cursor to home position"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03):
    """Print text with a typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def format_currency(amount):
    """Format currency to 2 decimal places"""
    return "{:.2f}".format(amount)

def display_currencies():
    """Display available currencies in a formatted grid"""
    print("\nAvailable currencies:")
    currencies = list(CURRENCY_RATES.keys())
    for i in range(0, len(currencies), 5):
        print(" ".join(f"{curr}" for curr in currencies[i:i+5]))

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    try:
     
        usd_amount = amount / CURRENCY_RATES[from_currency]
        final_amount = usd_amount * CURRENCY_RATES[to_currency]
        return final_amount
    except KeyError:
        return None
    except ZeroDivisionError:
        return None

def currency_converter():
    """Currency converter interface"""
    while True:
        cls()
        print("=== Currency Converter ===")
        display_currencies()
        
        try:
            print("\n")
           
            from_currency = input("\nFrom Currency (e.g., USD): ").upper()
            if from_currency == 'Q':
                return
            if from_currency not in CURRENCY_RATES:
                print("Invalid currency! Press Enter to try again...")
                input()
                continue

            to_currency = input("To Currency (e.g., EUR): ").upper()
            if to_currency == 'Q':
                return
            if to_currency not in CURRENCY_RATES:
                print("Invalid currency! Press Enter to try again...")
                input()
                continue
            
            # Get amount
            amount_str = input("Amount: ")
            if amount_str.upper() == 'Q':
                return
            amount = float(amount_str)
            if amount < 0:
                print("Amount must be positive! Press Enter to try again...")
                input()
                continue
            
            # display results
            final_amount = convert_currency(amount, from_currency, to_currency)
            if final_amount is not None:
                print("\nResult:")
                print(f"{format_currency(amount)} {from_currency} = {format_currency(final_amount)} {to_currency}")
             
                print("\nPopular conversions:")
                popular_currencies = ['USD', 'EUR', 'GBP']
                for curr in popular_currencies:
                    if curr != from_currency:
                        conv_amount = convert_currency(amount, from_currency, curr)
                        if conv_amount is not None:
                            print(f"{format_currency(amount)} {from_currency} = {format_currency(conv_amount)} {curr}")
            
            # Ask to convert again
            choice = input("\nConvert again? (y/n): ").lower()
            if choice != 'y':
                break
                
        except ValueError:
            print("Invalid amount! Press Enter to try again...")
            input()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Press Enter to try again...")
            input()

def authenticated_menu(username):
    """Menu for authenticated users"""

    currency_converter()
    
    while True:
        cls()
        print(f"Welcome, {username}!")
        print("\n1. Currency Converter")
        print("2. Settings")
        print("3. Help")
        print("4. Logout")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            currency_converter()
        elif choice == '2':
            cls()
            print_slow("Opening settings...")
            time.sleep(1)
        elif choice == '3':
            cls()
            print_slow("Loading help menu...")
            time.sleep(1)
        elif choice == '4':
            cls()
            print_slow("Logging out...")
            time.sleep(1)
            break
        else:
            print("\nInvalid option! Please try again.")
            time.sleep(1)

def signup():
    """Handle user registration"""
    cls()
    print("=== Sign Up ===")
    users = load_users()
    
    while True:
        username = input("Choose a username (or 'q' to quit): ").strip()
        if username.lower() == 'q':
            return

        if username in users:
            print("Username already exists! Please choose another one.")
            time.sleep(1)
            continue
            
        if len(username) < 3:
            print("Username must be at least 3 characters long!")
            time.sleep(1)
            continue
            
        if not username.isalnum():
            print("Username must contain only letters and numbers!")
            time.sleep(1)
            continue

        while True:
            password = getpass("Choose a password (minimum 6 characters): ")
            if len(password) < 6:
                print("Password must be at least 6 characters long!")
                continue
                
            confirm_password = getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match! Please try again.")
                continue
                
            break
        
     
        users[username] = password
        if save_users(users):
            print_slow("Account created successfully!")
            time.sleep(1)
            return
        else:
            print_slow("Error creating account. Please try again later.")
            time.sleep(1)
            return


def load_users():
    """Load users from JSON file with error handling"""
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading user database: {e}")
    return {}

def save_users(users):
    """Save users to JSON file with error handling"""
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except IOError as e:
        print(f"Error saving user database: {e}")

def login():
    """Handle user login"""
    cls()
    print("=== Login ===")
    users = load_users()
    
    attempts = 3
    while attempts > 0:
        username = input("Username (or 'q' to quit): ").strip()
        if username.lower() == 'q':
            return None
            
        password = getpass("Password: ")
        
        if username in users and users[username] == password:
            print_slow("Login successful!")
            time.sleep(0.5)
            return username
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Invalid credentials! {attempts} attempts remaining.")
            time.sleep(1)
    
    print_slow("Too many failed attempts. Please try again later.")
    time.sleep(1)
    return None

def main():
    """Main application loop"""
    while True:
        cls()
        print("=" * 40)
        print_slow("Welcome to Currency Converter")
        print("=" * 40)
        print()
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == '1':
            username = login()
            if username:
                authenticated_menu(username)
        elif choice == '2':
            signup()

        elif choice == '3':
            cls()
            print_slow("Thank you for using the application!")
            time.sleep(0.5)
            cls()
            break
        else:
            print("\nInvalid option! Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls()
        print("\nProgram terminated by user.")
        sys.exit(0)
