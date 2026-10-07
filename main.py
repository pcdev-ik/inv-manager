#!/usr/bin/env python3
"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
'''
ADD ITEM TO INVENTORY
'''
from pprint import pprint # not a clue why I'm required to use this

# user inputs name and function checks if it's valid
def name_obj(inv, name):
    name = name.strip()
    if name in inv:
        return (False, "Item already exists.")
    if name == "":
        return (False, "Name cannot be blank.")
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
            if not selected:
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
    Responses5 = ["5", "quit", "exit"]
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
5. Quit""")
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

        # QUIT
        elif main_choice.lower() in Responses5:
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
