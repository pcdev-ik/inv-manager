#!/usr/bin/env python3
"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
'''
IMPORTS
'''
from pprint import pprint # not a clue why I'm required to use this
import pandas as pd
import signal
import sys

'''
BASIC INPUT HANDLER
'''
def getinput(prompt):
    while True:
        endvalue = input(prompt)
        if endvalue.lower() in ["y", "yes"]:
            return True
        if endvalue.lower() in ["n", "no"]:
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

'''
SIGINT HANDLER
'''
# Handle SIGINT (Ctrl+C)
def sighandler(sig, frame):
    print("\n Interrupt received. Exiting program...")
    sys.exit(0)
signal.signal(signal.SIGINT, sighandler)

'''
FILE MANAGEMENT
'''
# Auto-save asker
def autosave_asker():
    while True:
        response = input("Would you like to turn on auto-save? (Y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True, 'Auto-save is enabled. Your inventory will be saved automatically after each change.'
        elif response in ['n', 'no']:
            return False, 'Auto-save is disabled.'
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

# Auto-saver
def autosaver(checkresult, inventory, filename):
    if checkresult:                                                 # Check if auto-save is enabled
        if filename == "":
            return                                                  # If filename is empty, do not attempt to save
        save_records(inventory, filename)
        print(f"Inventory auto-saved to '{filename}'.")

# Save inventory to a CSV file
def save_records(record, filename):
    pandalibrary = pd.DataFrame.from_dict(record, orient='index')   # Convert inventory dictionary to df (turns item names into row labels)
    pandalibrary.to_csv(filename)                                   # Save DataFrame to CSV file

# Name inventory function for saving to a CSV file
def name_inventory(name):
    name = name.strip()
    if not name:
        name = "inventory.csv"
    elif not name.endswith(".csv"):
        name += ".csv"
    return name

# Load inventory from a csv file using a with statement
def load_records(filename, inv):
    try:
        with open(filename, 'r') as file:
            pandalibrary = pd.read_csv(file, index_col=0)  # Load CSV into df
            loaded_inventory = pandalibrary.to_dict(orient='index')
            return (loaded_inventory, f"Inventory loaded from '{filename}'.")

    # file corrupted or not found error handling
    except pd.errors.EmptyDataError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' is empty or corrupted. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' is empty or corrupted. Starting with an empty inventory.")
    except FileNotFoundError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' not found. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' not found. Starting with an empty inventory.")
        
'''
ADD ITEM TO INVENTORY
'''
# user inputs name and function checks if it's valid
def name_obj(inv, name):
    name = name.strip()
    if name in inv:
        return (False, "Item already exists.")
    if name == "":
        return (False, "Name cannot be blank.")
    if len(name) > 500:
        return (False, "Name cannot exceed 500 characters.")
    return (True, f"Name is {name}.")

# user inputs quantity and function checks if it's valid
def count_obj(count):
    if count is None:                                             # if there's nothing there, reject
        return (False, "Quantity cannot be None.")
    if 0 <= count <= 1000000:                                     # if count is within range, accept
        return (True, f"Quantity is {count}.")
    return (False, "Quantity must be between 0 and 1,000,000.")

# user inputs price and function checks if it's valid
def price_obj(price):
    if price is None:                                             # if price is empty, reject
        return (False, "Price cannot be None.")
    if price < 0:
        return (False, "Price cannot be negative.")               # if price is negative, reject
    return (True, f"Price is ${price:.2f}.")

# Full validation function for adding an item to the inventory
def validate_item(inv, name, quantity, price):
    name_valid, name_msg = name_obj(inv, name)
    quantity_valid, quantity_msg = count_obj(quantity)
    price_valid, price_msg = price_obj(price)

    if not name_valid:
        return (False, name_msg)
    if not quantity_valid:
        return (False, quantity_msg)
    if not price_valid:
        return (False, price_msg)

    return (True, f"Item '{name}' with quantity {quantity} and price ${price:.2f} is valid. Adding to inventory.")

# Add an item to the inventory
def add_item(inv, name, quantity, price):
    name = name.strip()
    item_valid, validation_message = validate_item(inv, name, quantity, price)
    if not item_valid:
        return (False, validation_message)

    inv[name] = {"quantity": quantity, "price": price, "index": len(inv) + 1}  # Assign index based on current inventory size and create attributes
    return (True, f"The item '{name}' has been added with a quantity of {quantity} and a price of ${price:.2f}.")

# Edit an item in the inventory
def edit_item(inv, name):
    if name not in inv:
        return (False, f"Item '{name}' was not found.")

    updated_name = name
    change_name = getinput("Would you like to change the name? (Y/n): ")
    if change_name:
        while True:
            updated_name = input(f"New name for '{name}': ").strip()
            inventory_without_item = {
                item_name: item for item_name, item in inv.items() if item_name != name
            }
            name_valid, name_msg = name_obj(inventory_without_item, updated_name)
            if name_valid:
                break
            print(name_msg)

    updated_quantity = inv[name]["quantity"]
    change_quantity = getinput("Would you like to change the quantity? (Y/n): ")
    if change_quantity:
        while True:
            try:
                updated_quantity = int(input(f"New quantity for '{updated_name}': "))
            except ValueError:
                print("Please enter a valid integer for quantity.")
                continue
            quantity_valid, quantity_msg = count_obj(updated_quantity)
            if quantity_valid:
                break
            print(quantity_msg)

    updated_price = inv[name]["price"]
    change_price = getinput("Would you like to change the price? (Y/n): ")
    if change_price:
        while True:
            try:
                updated_price = float(input(f"New price for '{updated_name}': $"))
            except ValueError:
                print("Please enter a valid number for price.")
                continue
            price_valid, price_msg = price_obj(updated_price)
            if price_valid:
                break
            print(price_msg)

    item = inv[name]
    item["quantity"] = updated_quantity
    item["price"] = updated_price
    if updated_name != name:
        del inv[name]
        inv[updated_name] = item
    return (
        True,
        f"Item '{name}' updated to '{updated_name}' with quantity "
        f"{updated_quantity} and price ${updated_price:.2f}.",
    )

'''
CHART CREATION
'''
# check if an item within an inventory is low stock (under 5)
def low_stock(inv, name):
    if name in inv:
        return inv[name]["quantity"] < 5
    return False

# Calculate item value for chart
def calculate_item_value(item):
    return item["quantity"] * item["price"]

# Calculate chart value
def calculate_chart_value(inv):
    total_value = 0
    for item in inv.values():
        total_value += calculate_item_value(item)
    return total_value

# Make chart of inventory upon request | IMPURE
def chart(inv):
    sorted_items = sorted(inv.items(), key=lambda entry: entry[1].get("index", 0))                          # makes sure the items are listed by index
    print("\nInventory")
    print(f"{'Index':<6}{'Item':<25}{'Quantity':>10}{'Price':>11}{'Value':>14}")
    print("-" * 67)
    for name, item in sorted_items:
        item_value = calculate_item_value(item)                                                             # Calculate the value of the item
        total_value = calculate_chart_value(inv)                                                            # Calculate the total value of the inventory
        item_index = item["index"]                                                                          # Call index
        print(f"{item_index:^6}{name:<25}{item['quantity']:>10}{item['price']:>11.2f} {item_value:>13.2f}") # print rows
    print("-" * 67)
    print(f"{'Total Inventory Value:':<53}${total_value:>12.2f}")
    # flag low stock items
    low_stock_items = [name for name, item in inv.items() if low_stock(inv, name)]                          # Create list of low stock items
    if low_stock_items:                                                                                     # If there are low stock items
        print("\nLow Stock:")                                                                               # Print header
        for item in low_stock_items:                                                                        # Print each low stock item
            print(f"- {item} ({inv[item]['quantity']} in stock)")                                           # Print item name and quantity

# Delete an item from the inventory
def delete_record(inv, name):
    name = name.strip()
    if name == "":
        return (False, "Name cannot be blank.")
    if name not in inv:
        return (False, f"Item '{name}' was not found.")
    del inv[name]
    return (True, f"Item '{name}' has been deleted.")
    

# Check whether a response is a yes answer
def is_yes(answer):
    return answer.strip().lower() in ["yes", "y"]

'''
ORDER FUNCTIONS
'''
# Create available items list for order chart
def available_items(inv):
    return [name for name, item in inv.items() if item["quantity"] > 0]

# Validate whether a requested order quantity is allowed
def is_valid_order_quantity(inv, name, qty):
    return name in inv and qty > 0 and qty <= inv[name]["quantity"]

# Build a summary of the selected order items
def build_order_summary(selected):
    return [{"item": name, "quantity": qty} for name, qty in selected.items()]

# Remove item from inventory after order is created
def remove_item_from_inv(inv, name, qty):
    if name not in inv:
        return False, f"Item '{name}' was not found in inventory."
    if qty <= 0:
        return False, "Order quantity must be greater than 0."
    if qty > inv[name]["quantity"]:
        return False, f"Not enough stock for '{name}'. Only {inv[name]['quantity']} available."

    inv[name]["quantity"] -= qty
    if inv[name]["quantity"] == 0:
        del inv[name]
    return True, f"{qty} of '{name}' removed from inventory."

# Apply the confirmed order to inventory
def apply_order(inv, selected):
    for name, qty in selected.items():
        removed, message = remove_item_from_inv(inv, name, qty)
        if not removed:
            return False, message
    return True, "Order created and inventory updated."

# Create an order | IMPURE
def create_order(inv):                                                                  
    if not inv: # if inventory is empty
        return False, "The inventory is empty." # print rejection

    selected = {}   # create empty set
    while True:
        print("\nAvailable items:")
        for name in sorted(available_items(inv)):
            print(f"- {name} ({inv[name]['quantity']} in stock)({selected.get(name, 0)} in order)" if name in selected else f"- {name} ({inv[name]['quantity']} in stock)")

        item_name = input("Enter item name to add to order (or 'done' to finish): ").strip()
        if item_name.lower() == "done":
            if not selected:                                            # check if anything was ordered
                return False, "No items were selected for the order."   
            break

        if item_name == "":
            print("Name cannot be blank.")
            continue
        if item_name not in inv:
            print(f"Item '{item_name}' was not found.")
            continue

        try:
            qty = int(input(f"How many {item_name}(s) would you like to order? "))
        except ValueError:
            print("Please enter a valid integer for quantity.")
            continue

        if not is_valid_order_quantity(inv, item_name, qty):
            if qty <= 0:
                print("Order quantity must be greater than 0.")
            else:
                print(f"Not enough stock for '{item_name}'. Only {inv[item_name]['quantity']} available.")
            continue

        selected[item_name] = qty
        print(f"Added {qty} {item_name} to the order.")

    summary = build_order_summary(selected)
    print("\nOrder Summary:")
    pprint(summary) # obligatory

    confirm = input("Confirm this order? (yes/no): ")
    if not is_yes(confirm):
        return False, "Order cancelled."

    return apply_order(inv, selected)

'''
SEARCH FUNCTION
'''
# case-insensitive search for an item in the inventory
def search_item(inv, search_name):
    search_name = search_name.strip().lower()
    if not search_name:
        return []

    matches = [
        (name, item)
        for name, item in inv.items()
        if search_name in name.lower()
    ]
    return matches




'''
MAIN MENU
'''
# choices
def main(): # this big function that I hate | IMPURE
    autosavecheck = False, "Auto-save is disabled."  # Initialize auto-save check
    filename = ""
    Responses1 = ["1", "add record", "add"]
    Responses2 = ["2", "view records", "view"]
    Responses3 = ["3", "edit record", "edit"]
    Responses4 = ["4", "delete record", "delete"]
    Responses5 = ["5", "create order", "order"]
    Responses6 = ["6", "import records", "import"]
    Responses7 = ["7", "export records", "export"]
    Responses8 = ["8", "quit", "exit"]
    inventory = {}  
    while True: # main menu loop
        print(r"""
.-. .-. .----..-..-.   .-.
| | | |{ {__  | ||  `.'  |
\ \_/ /.-._} }| || |\ /| |
 `---' `----' `-'`-' ` `-'
Very Simple Inventory Manager
1. Add Record
2. View Records
3. Edit Record
4. Delete Record
5. Create Order
6. Import Records
7. Export Records
8. Quit""")
        main_choice = input("Please select an option: ") # user selects2
        if main_choice.lower() in Responses1:            # add record
            while True:
                name = input("Name of Item: ")
                try:
                    quantity = int(input("Quantity of Item: "))
                except (TypeError, ValueError):
                    print("Please enter a valid integer for quantity.")
                    continue

                try:
                    price = float(input("Price of Item: $"))
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                item_valid, validation_message = add_item(inventory, name, quantity, price)
                print(validation_message)
                if item_valid:
                    autosaver(autosavecheck[0], inventory, filename)  # Auto-save if enabled
                    break

        # VIEW RECORDS
        elif main_choice.lower() in Responses2:          # view records
            if not inventory:                            # if the inventory is empty
                print("The inventory is empty.")
            # MAKE CHART
            else:
                chart(inventory)                         # Print item name and quantity
            # SEARCH RECORDS
            search_choice = input("Would you like to search for an item? (Y/n): ").strip().lower()
            if search_choice in ['y', 'yes']:
                while True:
                    search_name = input("Search: ").strip()
                    matches = search_item(inventory, search_name)
                    if matches:
                        for name, item in matches:
                            print(f"Item: {name}, Quantity: {item['quantity']}, Price: ${item['price']:.2f}")
                    else:
                        print(f"No items found matching '{search_name}'.")
                    reSearch_choice = input("Would you like to search for another item? (Y/n): ").strip().lower()
                    if reSearch_choice not in ['y', 'yes']:
                        print("Returning to main menu.")
                        break
            

        # EDIT RECORDS
        elif main_choice.lower() in Responses3:          # edit records
            if not inventory:
                print("The inventory is empty.")
            else:
                editchoice = input("Would you like to see a list of items? (Y/n): ").strip().lower()
                if editchoice in ['y', 'yes']:
                    chart(inventory)
                name_to_edit = input("Name of Item to edit: ").strip()
                if name_to_edit not in inventory:
                    print(f"Item '{name_to_edit}' was not found.")
                else:
                    updated, message = edit_item(inventory, name_to_edit)
                    print(message)
                    if updated:
                        autosaver(autosavecheck[0], inventory, filename)
            
        # DELETE RECORDS
        elif main_choice.lower() in Responses4:
            if not inventory:
                print("The inventory is empty.")
            else:
                name_to_delete = input("Name of Item to delete: ").strip()
                if name_to_delete == "":
                    print("Name cannot be blank.")
                elif name_to_delete not in inventory:
                    print(f"Item '{name_to_delete}' was not found.")
                else:
                    confirm = input(f"Are you sure you want to delete '{name_to_delete}'? (yes/no): ")
                    if is_yes(confirm):
                        result = delete_record(inventory, name_to_delete)
                        print(result[1])
                        if result[0]:
                            autosaver(autosavecheck[0], inventory, filename)
                    else:
                        print(f"Deletion cancelled for '{name_to_delete}'.")

        # CREATE ORDER
        elif main_choice.lower() in Responses5:
            order_created, message = create_order(inventory)
            print(message)
            if order_created:
                autosaver(autosavecheck[0], inventory, filename)

        # IMPORT RECORDS
        elif main_choice.lower() in Responses6:
            filename = input("Enter filename to import inventory (default: inventory.csv): ")
            filename = name_inventory(filename)
            inventory, message = load_records(filename, inventory)
            print(message)
            autosavecheck = autosave_asker()
            print(autosavecheck[1])

        # EXPORT RECORDS
        elif main_choice.lower() in Responses7:
            if not inventory:
                print("The inventory is empty.")
            else:
                potentialname = input("Enter filename to save inventory (default: inventory.csv): ")
                filename = name_inventory(potentialname)
                save_records(inventory, filename)
                print(f"Inventory saved to '{filename}'.")
                autosavecheck = autosave_asker()
                print(autosavecheck[1])

        # QUIT
        elif main_choice.lower() in Responses8:
            if inventory:       # Check if the user created any records
                confirm = input("Would you like to save your inventory? (Y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    potentialname = input("Enter filename to save inventory (default: inventory.csv): ")
                    filename = name_inventory(potentialname)
                    save_records(inventory, filename)
                    print(f"Inventory saved to '{filename}'.")
                    autosavecheck = autosave_asker()
                    print(autosavecheck[1])
                    print("Goodbye!")
                    break
                if confirm in ['n', 'no']:
                    print("Goodbye!")
                    break
            if not inventory:   # Just exit if there's no inventory
                print("Goodbye!")
                break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()#!/usr/bin/env python3
"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
'''
IMPORTS
'''
from pprint import pprint # not a clue why I'm required to use this
import pandas as pd
import signal
import sys

'''
SIGINT HANDLER
'''
# Handle SIGINT (Ctrl+C)
def sighandler(sig, frame):
    print("\n Interrupt received. Exiting program...")
    sys.exit(0)

signal.signal(signal.SIGINT, sighandler)

'''
FILE MANAGEMENT
'''
# Save inventory to a CSV file
def save_records(record, filename):
    pandalibrary = pd.DataFrame.from_dict(record, orient='index')  # Convert inventory dictionary to df (turns item names into row labels)
    pandalibrary.to_csv(filename)  # Save DataFrame to CSV file

# Name inventory function for saving to a CSV file
def name_inventory(name):
    name = name.strip()
    if not name:
        name = "inventory.csv"
    elif not name.endswith(".csv"):
        name += ".csv"
    return name

# Load inventory from a csv file using a with statement
def load_records(filename, inv):
    try:
        with open(filename, 'r') as file:
            pandalibrary = pd.read_csv(file, index_col=0)  # Load CSV into df
            return pandalibrary.to_dict(orient='index')  # Convert df back to dictionary
    # file corrupted or not found error handling
    except pd.errors.EmptyDataError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' is empty or corrupted. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' is empty or corrupted. Starting with an empty inventory.")
    except FileNotFoundError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' not found. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' not found. Starting with an empty inventory.")

# Save record file
'''
ADD ITEM TO INVENTORY
'''
# user inputs name and function checks if it's valid
def name_obj(inv, name):
    name = name.strip()
    if name in inv:
        return (False, "Item already exists.")
    if name == "":
        return (False, "Name cannot be blank.")
    if len(name) > 500:
        return (False, "Name cannot exceed 500 characters.")
    return (True, f"Name is {name}.")

# user inputs quantity and function checks if it's valid
def count_obj(count):
    if count is None:                                             # if there's nothing there, reject
        return (False, "Quantity cannot be None.")
    if 0 <= count <= 1000000:                                     # if count is within range, accept
        return (True, f"Quantity is {count}.")
    return (False, "Quantity must be between 0 and 1,000,000.")

# user inputs price and function checks if it's valid
def price_obj(price):
    if price is None:                                             # if price is empty, reject
        return (False, "Price cannot be None.")
    if price < 0:
        return (False, "Price cannot be negative.")               # if price is negative, reject
    return (True, f"Price is ${price:.2f}.")

'''
CHART CREATION
'''
# check if an item within an inventory is low stock (under 5)
def low_stock(inv, name):
    if name in inv:
        return inv[name]["quantity"] < 5
    return False

# Calculate item value for chart
def calculate_item_value(item):
    return item["quantity"] * item["price"]

# Calculate chart value
def calculate_chart_value(inv):
    total_value = 0
    for item in inv.values():
        total_value += calculate_item_value(item)
    return total_value

# Make chart of inventory upon request | IMPURE
def chart(inv):
    sorted_items = sorted(inv.items(), key=lambda entry: entry[1].get("index", 0))                          # makes sure the items are listed by index
    print("\nInventory")
    print(f"{'Index':<6}{'Item':<25}{'Quantity':>10}{'Price':>11}{'Value':>14}")
    print("-" * 67)
    for name, item in sorted_items:
        item_value = calculate_item_value(item)                                                             # Calculate the value of the item
        total_value = calculate_chart_value(inv)                                                            # Calculate the total value of the inventory
        item_index = item["index"]                                                                          # Call index
        print(f"{item_index:^6}{name:<25}{item['quantity']:>10}{item['price']:>11.2f} {item_value:>13.2f}") # print rows
    print("-" * 67)
    print(f"{'Total Inventory Value:':<53}${total_value:>12.2f}")
    # flag low stock items
    low_stock_items = [name for name, item in inv.items() if low_stock(inv, name)]                          # Create list of low stock items
    if low_stock_items:                                                                                     # If there are low stock items
        print("\nLow Stock:")                                                                               # Print header
        for item in low_stock_items:                                                                        # Print each low stock item
            print(f"- {item} ({inv[item]['quantity']} in stock)")                                           # Print item name and quantity

# Delete an item from the inventory
def delete_record(inv, name):
    name = name.strip()
    if name == "":
        return (False, "Name cannot be blank.")
    if name not in inv:
        return (False, f"Item '{name}' was not found.")
    del inv[name]
    return (True, f"Item '{name}' has been deleted.")

# Check whether a response is a yes answer
def is_yes(answer):
    return answer.strip().lower() in ["yes", "y"]

'''
ORDER FUNCTIONS
'''
# Create available items list for order chart
def available_items(inv):
    return [name for name, item in inv.items() if item["quantity"] > 0]

# Validate whether a requested order quantity is allowed
def is_valid_order_quantity(inv, name, qty):
    return name in inv and qty > 0 and qty <= inv[name]["quantity"]

# Build a summary of the selected order items
def build_order_summary(selected):
    return [{"item": name, "quantity": qty} for name, qty in selected.items()]

# Remove item from inventory after order is created
def remove_item_from_inv(inv, name, qty):
    if name not in inv:
        return False, f"Item '{name}' was not found in inventory."
    if qty > inv[name]["quantity"]:
        return False, f"Not enough stock for '{name}'. Only {inv[name]['quantity']} available."

    inv[name]["quantity"] -= qty
    if inv[name]["quantity"] == 0:
        del inv[name]
    return True, f"{qty} of '{name}' removed from inventory."

# Apply the confirmed order to inventory
def apply_order(inv, selected):
    for name, qty in selected.items():
        removed, message = remove_item_from_inv(inv, name, qty)
        if not removed:
            return False, message
    return True, "Order created and inventory updated."

# Create an order | IMPURE
def create_order(inv):                                                                  
    if not inv: # if inventory is empty
        return False, "The inventory is empty." # print rejection

    selected = {}   # create empty set
    while True:
        print("\nAvailable items:")
        for name in sorted(available_items(inv)):
            print(f"- {name} ({inv[name]['quantity']} in stock)")

        item_name = input("Enter item name to add to order (or 'done' to finish): ").strip()
        if item_name.lower() == "done":
            if not selected:                                            # check if anything was ordered
                return False, "No items were selected for the order."   
            break

        if item_name == "":
            print("Name cannot be blank.")
            continue
        if item_name not in inv:
            print(f"Item '{item_name}' was not found.")
            continue

        try:
            qty = int(input(f"How many {item_name}(s) would you like to order? "))
        except ValueError:
            print("Please enter a valid integer for quantity.")
            continue

        if not is_valid_order_quantity(inv, item_name, qty):
            if qty <= 0:
                print("Order quantity must be greater than 0.")
            else:
                print(f"Not enough stock for '{item_name}'. Only {inv[item_name]['quantity']} available.")
            continue

        selected[item_name] = qty
        print(f"Added {qty} {item_name} to the order.")

    summary = build_order_summary(selected)
    print("\nOrder Summary:")
    pprint(summary) # obligatory

    confirm = input("Confirm this order? (yes/no): ")
    if not is_yes(confirm):
        return False, "Order cancelled."

    return apply_order(inv, selected)

'''
MAIN MENU
'''
# choices
def main(): # this big function that I hate | IMPURE
    Responses1 = ["1", "add record", "add"]
    Responses2 = ["2", "view records", "view"]
    Responses3 = ["3", "delete record", "delete"]
    Responses4 = ["4", "create order", "order"]
    Responses5 = ["5", "import records", "import"]
    Responses6 = ["6", "export records", "export"]
    Responses7 = ["7", "quit", "exit"]
    inventory = {}  
    while True: # main menu loop
        print(r"""
.-. .-. .----..-..-.   .-.
| | | |{ {__  | ||  `.'  |
\ \_/ /.-._} }| || |\ /| |
 `---' `----' `-'`-' ` `-'
Very Simple Inventory Manager
1. Add Record
2. View Records
3. Delete Record
4. Create Order
5. Import Records
6. Export Records
7. Quit""")
        main_choice = input("Please select an option: ") # user selects2
        if main_choice.lower() in Responses1:            # add record
            # Get name
            # if name passes checks, break out of the loop
            namegoodflag = (False, "")
            while not namegoodflag[0]:
                name = input("Name of Item: ")
                namegoodflag = name_obj(inventory, name)
                print(namegoodflag[1])

            # Get quantity
            quantitygoodflag = (False, "")
            while not quantitygoodflag[0]:
                try:
                    quantity = int(input("Quantity of Item: "))
                    quantitygoodflag = count_obj(quantity)
                    print(quantitygoodflag[1])
                except (TypeError, ValueError):
                    print("Please enter a valid integer for quantity.")

            # Get price
            pricegoodflag = (False, "")
            while not pricegoodflag[0]:
                try:
                    price = float(input("Price of Item: $"))
                    pricegoodflag = price_obj(price)
                    print(pricegoodflag[1])
                except ValueError:
                    print("Please enter a valid number.")
            inventory[name] = {"quantity": quantity, "price": price, "index": len(inventory) + 1}  # Assign index based on current inventory size and create attributes

            # summary
            print(f"The item {name} has been added with a quantity of {quantity} and a price of ${price:.2f}")
            print(f"The total value of {name} in stock is ${(quantity * price):.2f}")


        # VIEW RECORDS
        elif main_choice.lower() in Responses2:          # view records
            if not inventory:                            # if the inventory is empty
                print("The inventory is empty.")
            # MAKE CHART
            else:
                chart(inventory)                         # Print item name and quantity

        # DELETE RECORDS
        elif main_choice.lower() in Responses3:
            if not inventory:
                print("The inventory is empty.")
            else:
                name_to_delete = input("Name of Item to delete: ").strip()
                if name_to_delete == "":
                    print("Name cannot be blank.")
                elif name_to_delete not in inventory:
                    print(f"Item '{name_to_delete}' was not found.")
                else:
                    confirm = input(f"Are you sure you want to delete '{name_to_delete}'? (yes/no): ")
                    if is_yes(confirm):
                        result = delete_record(inventory, name_to_delete)
                        print(result[1])
                    else:
                        print(f"Deletion cancelled for '{name_to_delete}'.")

        # CREATE ORDER
        elif main_choice.lower() in Responses4:
            _, message = create_order(inventory)
            print(message)

        # IMPORT RECORDS
        elif main_choice.lower() in Responses5:
            filename = input("Enter filename to import inventory (default: inventory.csv): ")
            filename = name_inventory(filename)
            inventory = load_records(filename, inventory)[0]  # Load records and update inventory
            print(load_records(filename, inventory)[1])  # Print the message from load_records

        # EXPORT RECORDS
        elif main_choice.lower() in Responses6:
            if not inventory:
                print("The inventory is empty.")
            else:
                potentialname = input("Enter filename to save inventory (default: inventory.csv): ")
                filename = name_inventory(potentialname)
                save_records(inventory, filename)
                print(f"Inventory saved to '{filename}'.")

        # QUIT#!/usr/bin/env python3
"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
'''
IMPORTS
'''
from pprint import pprint # not a clue why I'm required to use this
import pandas as pd
import signal
import sys

'''
SIGINT HANDLER
'''
# Handle SIGINT (Ctrl+C)
def sighandler(sig, frame):
    print("\n Interrupt received. Exiting program...")
    sys.exit(0)

signal.signal(signal.SIGINT, sighandler)

'''
FILE MANAGEMENT
'''
# Save inventory to a CSV file
def save_records(record, filename):
    pandalibrary = pd.DataFrame.from_dict(record, orient='index')  # Convert inventory dictionary to df (turns item names into row labels)
    pandalibrary.to_csv(filename)  # Save DataFrame to CSV file

# Name inventory function for saving to a CSV file
def name_inventory(name):
    name = name.strip()
    if not name:
        name = "inventory.csv"
    elif not name.endswith(".csv"):
        name += ".csv"
    return name

# Load inventory from a csv file using a with statement
def load_records(filename, inv):
    try:
        with open(filename, 'r') as file:
            pandalibrary = pd.read_csv(file, index_col=0)  # Load CSV into df
            return pandalibrary.to_dict(orient='index')  # Convert df back to dictionary
    # file corrupted or not found error handling
    except pd.errors.EmptyDataError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' is empty or corrupted. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' is empty or corrupted. Starting with an empty inventory.")
    except FileNotFoundError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' not found. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' not found. Starting with an empty inventory.")

# Save record file
'''
ADD ITEM TO INVENTORY
'''
# user inputs name and function checks if it's valid
def name_obj(inv, name):
    name = name.strip()
    if name in inv:
        return (False, "Item already exists.")
    if name == "":
        return (False, "Name cannot be blank.")
    if len(name) > 500:
        return (False, "Name cannot exceed 500 characters.")
    return (True, f"Name is {name}.")

# user inputs quantity and function checks if it's valid
def count_obj(count):
    if count is None:                                             # if there's nothing there, reject
        return (False, "Quantity cannot be None.")
    if 0 <= count <= 1000000:                                     # if count is within range, accept
        return (True, f"Quantity is {count}.")
    return (False, "Quantity must be between 0 and 1,000,000.")

# user inputs price and function checks if it's valid
def price_obj(price):
    if price is None:                                             # if price is empty, reject
        return (False, "Price cannot be None.")
    if price < 0:
        return (False, "Price cannot be negative.")               # if price is negative, reject
    return (True, f"Price is ${price:.2f}.")

'''
CHART CREATION
'''
# check if an item within an inventory is low stock (under 5)
def low_stock(inv, name):
    if name in inv:
        return inv[name]["quantity"] < 5
    return False

# Calculate item value for chart
def calculate_item_value(item):
    return item["quantity"] * item["price"]

# Calculate chart value
def calculate_chart_value(inv):
    total_value = 0
    for item in inv.values():
        total_value += calculate_item_value(item)
    return total_value

# Make chart of inventory upon request | IMPURE
def chart(inv):
    sorted_items = sorted(inv.items(), key=lambda entry: entry[1].get("index", 0))                          # makes sure the items are listed by index
    print("\nInventory")
    print(f"{'Index':<6}{'Item':<25}{'Quantity':>10}{'Price':>11}{'Value':>14}")
    print("-" * 67)
    for name, item in sorted_items:
        item_value = calculate_item_value(item)                                                             # Calculate the value of the item
        total_value = calculate_chart_value(inv)                                                            # Calculate the total value of the inventory
        item_index = item["index"]                                                                          # Call index
        print(f"{item_index:^6}{name:<25}{item['quantity']:>10}{item['price']:>11.2f} {item_value:>13.2f}") # print rows
    print("-" * 67)
    print(f"{'Total Inventory Value:':<53}${total_value:>12.2f}")
    # flag low stock items
    low_stock_items = [name for name, item in inv.items() if low_stock(inv, name)]                          # Create list of low stock items
    if low_stock_items:                                                                                     # If there are low stock items
        print("\nLow Stock:")                                                                               # Print header
        for item in low_stock_items:                                                                        # Print each low stock item
            print(f"- {item} ({inv[item]['quantity']} in stock)")                                           # Print item name and quantity

# Delete an item from the inventory
def delete_record(inv, name):
    name = name.strip()
    if name == "":
        return (False, "Name cannot be blank.")
    if name not in inv:
        return (False, f"Item '{name}' was not found.")
    del inv[name]
    return (True, f"Item '{name}' has been deleted.")

# Check whether a response is a yes answer
def is_yes(answer):
    return answer.strip().lower() in ["yes", "y"]

'''
ORDER FUNCTIONS
'''
# Create available items list for order chart
def available_items(inv):
    return [name for name, item in inv.items() if item["quantity"] > 0]

# Validate whether a requested order quantity is allowed
def is_valid_order_quantity(inv, name, qty):
    return name in inv and qty > 0 and qty <= inv[name]["quantity"]

# Build a summary of the selected order items
def build_order_summary(selected):
    return [{"item": name, "quantity": qty} for name, qty in selected.items()]

# Remove item from inventory after order is created
def remove_item_from_inv(inv, name, qty):
    if name not in inv:
        return False, f"Item '{name}' was not found in inventory."
    if qty > inv[name]["quantity"]:
        return False, f"Not enough stock for '{name}'. Only {inv[name]['quantity']} available."

    inv[name]["quantity"] -= qty
    if inv[name]["quantity"] == 0:
        del inv[name]
    return True, f"{qty} of '{name}' removed from inventory."

# Apply the confirmed order to inventory
def apply_order(inv, selected):
    for name, qty in selected.items():
        removed, message = remove_item_from_inv(inv, name, qty)
        if not removed:
            return False, message
    return True, "Order created and inventory updated."

# Create an order | IMPURE
def create_order(inv):                                                                  
    if not inv: # if inventory is empty
        return False, "The inventory is empty." # print rejection

    selected = {}   # create empty set
    while True:
        print("\nAvailable items:")
        for name in sorted(available_items(inv)):
            print(f"- {name} ({inv[name]['quantity']} in stock)")

        item_name = input("Enter item name to add to order (or 'done' to finish): ").strip()
        if item_name.lower() == "done":
            if not selected:                                            # check if anything was ordered
                return False, "No items were selected for the order."   
            break

        if item_name == "":
            print("Name cannot be blank.")
            continue
        if item_name not in inv:
            print(f"Item '{item_name}' was not found.")
            continue

        try:
            qty = int(input(f"How many {item_name}(s) would you like to order? "))
        except ValueError:
            print("Please enter a valid integer for quantity.")
            continue

        if not is_valid_order_quantity(inv, item_name, qty):
            if qty <= 0:
                print("Order quantity must be greater than 0.")
            else:
                print(f"Not enough stock for '{item_name}'. Only {inv[item_name]['quantity']} available.")
            continue

        selected[item_name] = qty
        print(f"Added {qty} {item_name} to the order.")

    summary = build_order_summary(selected)
    print("\nOrder Summary:")
    pprint(summary) # obligatory

    confirm = input("Confirm this order? (yes/no): ")
    if not is_yes(confirm):
        return False, "Order cancelled."

    return apply_order(inv, selected)

'''
MAIN MENU
'''
# choices
def main(): # this big function that I hate | IMPURE
    Responses1 = ["1", "add record", "add"]
    Responses2 = ["2", "view records", "view"]
    Responses3 = ["3", "delete record", "delete"]
    Responses4 = ["4", "create order", "order"]
    Responses5 = ["5", "import records", "import"]
    Responses6 = ["6", "export records", "export"]
    Responses7 = ["7", "quit", "exit"]
    inventory = {}  
    while True: # main menu loop
        print(r"""
.-. .-. .----..-..-.   .-.
| | | |{ {__  | ||  `.'  |
\ \_/ /.-._} }| || |\ /| |
 `---' `----' `-'`-' ` `-'
Very Simple Inventory Manager
1. Add Record
2. View Records
3. Delete Record
4. Create Order
5. Import Records
6. Export Records
7. Quit""")
        main_choice = input("Please select an option: ") # user selects2
        if main_choice.lower() in Responses1:            # add record
            # Get name
            # if name passes checks, break out of the loop
            namegoodflag = (False, "")
            while not namegoodflag[0]:
                name = input("Name of Item: ")
                namegoodflag = name_obj(inventory, name)
                print(namegoodflag[1])

            # Get quantity
            quantitygoodflag = (False, "")
            while not quantitygoodflag[0]:
                try:
                    quantity = int(input("Quantity of Item: "))
                    quantitygoodflag = count_obj(quantity)
                    print(quantitygoodflag[1])
                except (TypeError, ValueError):
                    print("Please enter a valid integer for quantity.")

            # Get price
            pricegoodflag = (False, "")
            while not pricegoodflag[0]:
                try:
                    price = float(input("Price of Item: $"))
                    pricegoodflag = price_obj(price)
                    print(pricegoodflag[1])
                except ValueError:
                    print("Please enter a valid number.")
            inventory[name] = {"quantity": quantity, "price": price, "index": len(inventory) + 1}  # Assign index based on current inventory size and create attributes

            # summary
            print(f"The item {name} has been added with a quantity of {quantity} and a price of ${price:.2f}")
            print(f"The total value of {name} in stock is ${(quantity * price):.2f}")


        # VIEW RECORDS
        elif main_choice.lower() in Responses2:          # view records
            if not inventory:                            # if the inventory is empty
                print("The inventory is empty.")
            # MAKE CHART
            else:
                chart(inventory)                         # Print item name and quantity

        # DELETE RECORDS
        elif main_choice.lower() in Responses3:
            if not inventory:
                print("The inventory is empty.")
            else:
                name_to_delete = input("Name of Item to delete: ").strip()
                if name_to_delete == "":
                    print("Name cannot be blank.")
                elif name_to_delete not in inventory:
                    print(f"Item '{name_to_delete}' was not found.")
                else:
                    confirm = input(f"Are you sure you want to delete '{name_to_delete}'? (yes/no): ")
                    if is_yes(confirm):
                        result = delete_record(inventory, name_to_delete)
                        print(result[1])
                    else:
                        print(f"Deletion cancelled for '{name_to_delete}'.")

        # CREATE ORDER
        elif main_choice.lower() in Responses4:
            _, message = create_order(inventory)
            print(message)

        # IMPORT RECORDS
        elif main_choice.lower() in Responses5:
            filename = input("Enter filename to import inventory (default: inventory.csv): ")
            filename = name_inventory(filename)
            inventory = load_records(filename, inventory)[0]  # Load records and update inventory
            print(load_records(filename, inventory)[1])  # Print the message from load_records

        # EXPORT RECORDS
        elif main_choice.lower() in Responses6:
            if not inventory:
                print("The inventory is empty.")
            else:
                potentialname = input("Enter filename to save inventory (default: inventory.csv): ")
                filename = name_inventory(potentialname)
                save_records(inventory, filename)
                print(f"Inventory saved to '{filename}'.")

        # QUIT
        elif main_choice.lower() in Responses7:
            if inventory:       # Check if the user created any records
                confirm = input("Would you like to save your inventory? (Y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    potentialname = input("Enter filename to save inventory (default: inventory.csv): ")
                    filename = name_inventory(potentialname)
                    save_records(inventory, filename)
                    print(f"Inventory saved to '{filename}'. Goodbye!")
                if confirm in ['n', 'no']:
                    print("Goodbye!")
                    break
            if not inventory:   # Just exit if there's no inventory
                print("Goodbye!")
                break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
        elif main_choice.lower() in Responses7:
            if inventory:       # Check if the user created any records
                confirm = input("Would you like to save your inventory? (Y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    potentialname = input("Enter filename to save inventory (default: inventory.csv): ")
                    filename = name_inventory(potentialname)
                    save_records(inventory, filename)
                    print(f"Inventory saved to '{filename}'. Goodbye!")
                if confirm in ['n', 'no']:
                    print("Goodbye!")
                    break
            if not inventory:   # Just exit if there's no inventory
                print("Goodbye!")
                break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
