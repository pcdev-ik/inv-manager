#!/usr/bin/env python3
"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
'''
IMPORTS
'''
from pprint import pprint # not a clue why I'm required to use this
import math
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

def getchoice(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice == "":
            print("Input cannot be blank. Please enter a valid option.")
            continue
        return choice

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
            pandalibrary = pd.read_csv(file, index_col=0)                       # Load CSV into df

            # checks for compatibility
            required_fields = {"quantity", "price", "index"}                    
            missing_fields = required_fields.difference(pandalibrary.columns)   # Checks required fields against actual fields
            if missing_fields:
                raise ValueError(
                    f"Missing required columns: {', '.join(sorted(missing_fields))}."
                )
            if not pandalibrary.index.is_unique:
                raise ValueError("Item names must be unique.")

            loaded_inventory = pandalibrary.to_dict(orient='index')             # Load potential inv
            validated_inventory = {}
            indices = set()
            for raw_name, item in loaded_inventory.items():
                name = str(raw_name).strip()
                if not name:
                    raise ValueError("Item names cannot be blank.")
                if len(name) > 500:
                    raise ValueError(f"Item name '{name}' exceeds 500 characters.")
                if name in validated_inventory:
                    raise ValueError(f"Duplicate item name '{name}'.")

                try:
                    quantity = float(item["quantity"])
                    price = float(item["price"])
                    index = float(item["index"])
                except (KeyError, TypeError, ValueError) as error:
                    raise ValueError(
                        f"Item '{name}' must have numeric quantity, price, and index values."
                    )

                if (
                    not math.isfinite(quantity)         # if SOMEHOW you input something infinite
                    or not quantity.is_integer()        # or it's not an integer at all
                    or not 0 <= quantity <= 1_000_000   # or it's negative/too large
                ):
                    raise ValueError(                   # reject
                        f"Item '{name}' quantity must be an integer between 0 and 1,000,000."
                    )
                if not math.isfinite(price) or price < 0:   #reject infinity again
                    raise ValueError(f"Item '{name}' price must be finite and non-negative.")
                if (
                    not math.isfinite(index)
                    or not index.is_integer()
                    or index < 1
                    or index in indices
                ):
                    raise ValueError(f"Item '{name}' must have a unique positive integer index.")

                indices.add(index)
                item.update(
                    quantity=int(quantity),
                    price=price,
                    index=int(index),
                )
                validated_inventory[name] = item

            calculate_chart_value(validated_inventory)
            return (validated_inventory, f"Inventory loaded from '{filename}'.")

    # file corrupted or not found error handling
    except pd.errors.EmptyDataError:
        if inv:  # if the inventory is not empty
            return (inv, f"File '{filename}' is empty or corrupted. Keeping current inventory.")
        if not inv:  # if the inventory is empty
            return ({}, f"File '{filename}' is empty or corrupted. Starting with an empty inventory.")
    except (pd.errors.ParserError, ValueError) as error:
        return (
            inv,
            f"File '{filename}' is invalid ({error}). Keeping current inventory.",
        )
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
    if not math.isfinite(price):
        return (False, "Price must be a finite number.")          # if price is infinite, reject
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
    try:
        calculate_item_value({"quantity": quantity, "price": price})
    except ValueError as error:
        return (False, str(error))

    return (True, f"Item '{name}' with quantity {quantity} and price ${price:.2f} is valid. Adding to inventory.")

# Add an item to the inventory
def add_item(inv, name, quantity, price):
    name = name.strip()
    item_valid, validation_message = validate_item(inv, name, quantity, price)
    if not item_valid:
        return (False, validation_message)

    next_index = max(
        (item.get("index", 0) for item in inv.values()),
        default=0,
    ) + 1
    new_item = {"quantity": quantity, "price": price, "index": next_index}
    try:
        calculate_chart_value({**inv, name: new_item})
    except ValueError as error:
        return (False, str(error))
    inv[name] = new_item
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
    updated_item = {
        **item,
        "quantity": updated_quantity,
        "price": updated_price,
    }
    updated_inventory = {
        item_name: updated_item if item_name == name else current_item
        for item_name, current_item in inv.items()
    }
    if updated_name != name:
        del updated_inventory[name]
        updated_inventory[updated_name] = updated_item
    try:
        calculate_chart_value(updated_inventory)
    except ValueError as error:
        return (False, str(error))
    inv.clear()
    inv.update(updated_inventory)
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
    value = item["quantity"] * item["price"]
    return value

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
        if name not in inv:
            return False, f"Item '{name}' was not found in inventory."
        if qty <= 0:
            return False, "Order quantity must be greater than 0."
        if qty > inv[name]["quantity"]:
            return False, f"Not enough stock for '{name}'. Only {inv[name]['quantity']} available."

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
            if not selected:                                                            # check if anything was ordered
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

        remaining_quantity = inv[item_name]["quantity"] - selected.get(item_name, 0)
        if qty <= 0 or qty > remaining_quantity:                                        # well you have to order SOMETHING...
            if qty <= 0:
                print("Order quantity must be greater than 0.")
            else:
                print(
                    f"Not enough stock for '{item_name}'. "
                    f"Only {remaining_quantity} more available for this order."
                )
            continue

        selected[item_name] = selected.get(item_name, 0) + qty
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
CHARTS
'''
# Item value highest-lowest
def calculate_item_values(inv):
    return dict(
        sorted(
            (
                (name, calculate_item_value(item))  # return the name and the value
                for name, item in inv.items()       # for every item in the inventory
            ),
            key=lambda entry: entry[1],             # sorted by the value
            reverse=True,                           # high to low
        )
    )

# Get chart average value
def calculate_average_item_value(inv):
    if not inv:
        raise ValueError("Cannot calculate an average for an empty inventory.") # interrupt possible divide by 0 by forcing valueerror
    return calculate_chart_value(inv) / len(inv) # make the average

# Group records by stock
def group_records_by_stock(inv):
    groups = {"high_stock": {}, "low_stock": {}, "in_stock": {}}
    for name, item in inv.items():
        quantity = item["quantity"]
        if quantity < 5:
            groups["low_stock"][name] = item
        elif quantity >= 20:
            groups["high_stock"][name] = item
        else:
            groups["in_stock"][name] = item
    return groups

# Determine what contributes the most to the inventory
def calculate_value_percentages(inv):
    total_value = calculate_chart_value(inv)
    if total_value == 0:
        raise ValueError("Cannot calculate percentages when total inventory value is zero.")

    percentages = (
        (name, calculate_item_value(item) / total_value * 100)
        for name, item in inv.items()
    )
    return dict(sorted(percentages, key=lambda entry: entry[1], reverse=True))

# Determine the highest of each value
def calculate_highscores(inv):
    records = list(inv.items())
    first_added = min(records, key=lambda entry: entry[1].get("index", 0))[0]
    most_recent = max(records, key=lambda entry: entry[1].get("index", 0))[0]
    most_valuable = max(records, key=lambda entry: calculate_item_value(entry[1]))[0]
    least_valuable = min(records, key=lambda entry: calculate_item_value(entry[1]))[0]
    most_expensive = max(records, key=lambda entry: entry[1]["price"])[0]
    least_expensive = min(records, key=lambda entry: entry[1]["price"])[0]
    most_stocked = max(records, key=lambda entry: entry[1]["quantity"])[0]
    least_stocked = min(records, key=lambda entry: entry[1]["quantity"])[0]
    return (
        first_added,
        most_recent,
        most_valuable,
        least_valuable,
        most_expensive,
        least_expensive,
        most_stocked,
        least_stocked,
    )

# THE BIG CHART
def the_big_chart(inv):
    chartoptions = getchoice("""What would you like to see?
Write your option(s) separated by spaces. Use the option form (like "-dc") NOT the plaintext form (like "Default Chart").
1. Default Chart                    -dc
2. Item value highest-lowest        -iv
3. Number of records                -n
4. Average item value              -acv
5. Total chart value                -cv
6. Group records by stock           -gr
7. Percentage of inventory value    -p
8. Highest Metrics                  -h
""")
    selected_options = set(chartoptions.split()) # turns the typed options into a set

    def option_selected(*aliases):
        return any(alias in selected_options for alias in aliases) # if anything in the list matches the given option, returns True

    if option_selected("1", "chart", "-dc"):
        chart(inv)

    if option_selected("2", "-iv"):
        calcdict = calculate_item_values(inv)
        print("\nItem Values")
        print(f"{'Item':<25}{'Value':>14}")
        print("-" * 39)
        for name, value in calcdict.items():
            print(f"{name:<25}${value:>13.2f}")
        print("-" * 39)
        print(f"{'Total Item Value:':<25}${sum(calcdict.values()):>12.2f}")

    if option_selected("3", "number", "-n"):
        print(f"\nNumber of Records: {len(inv)}")

    if option_selected("4", "average", "-acv"):
        print(f"\nAverage item value: ${calculate_average_item_value(inv):.2f}")
        
    if option_selected("5", "value", "-cv"):
        print(f"\nInventory value: ${calculate_chart_value(inv):.2f}")

    if option_selected("6", "group", "stock", "-gr"):
        groups = group_records_by_stock(inv)
        stock_labels = (
            ("high_stock", "High stock (20 or more)"),
            ("in_stock", "In stock (5-19)"),
            ("low_stock", "Low stock (under 5)"),
        )
        print("\nRecords by Stock")
        for group_name, label in stock_labels:
            records = sorted(
                groups[group_name].items(),
                key=lambda entry: entry[1].get("index", 0),
            )
            print(f"\n{label} - {len(records)} record(s)")
            print(f"{'Item':<25}{'Quantity':>10}")
            print("-" * 35)
            if records:
                for name, item in records:
                    print(f"{name:<25}{item['quantity']:>10}")
            else:
                print("No records.")
        
    if option_selected("7", "percentage", "-p"):
        print("\nPercentage of Inventory Value")
        if calculate_chart_value(inv) == 0:
            print("Cannot create percentage chart: total inventory value is zero.")
        else:
            percentages = calculate_value_percentages(inv)
            print(f"{'Item':<25}{'Value':>14}{'Share':>10}  Distribution")
            print("-" * 67)
            for name, percentage in percentages.items():
                value = calculate_item_value(inv[name])
                bar_length = max(1, round(percentage / 100 * 40)) if percentage else 0
                print(
                    f"{name:<25}${value:>12.2f}{percentage:>9.2f}%  "
                    f"{'#' * bar_length}"
                )

    if option_selected("8", "highscore", "-h"):
        (
            first_added,
            most_recent,
            most_valuable,
            least_valuable,
            most_expensive,
            least_expensive,
            most_stocked,
            least_stocked,
        ) = calculate_highscores(inv)
        print("METRICS")
        print("First Item Added (Index 1): " + first_added)
        print("Most Recent Addition: " + most_recent)
        print("Most Valuable Item: " + most_valuable)
        print("Least Valuable Item: " + least_valuable)
        print("Most Expensive Item: " + most_expensive)
        print("Least Expensive Item: " + least_expensive)
        print("Most Stocked Item: " + most_stocked)
        print("Least Stocked Item: " + least_stocked)

    print("\n")

        


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
                while True:
                    smladv = input("""What would you like to view?
1. Simple Chart
2. Advanced Chart
3. Go Back
""").lower().strip()
                    if smladv in ["1", "simple chart", "simple"]:
                        chart(inventory)                         # Print item name and quantity
                        break
                    if smladv in ["2", "advanced chart", "advanced"]:
                        the_big_chart(inventory)                 # Enter hell i.e. (print the big chart)
                        break
                    if smladv in ["3", "back", "exit", "go back"]:
                        break
 

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
    main()
