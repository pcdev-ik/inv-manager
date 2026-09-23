"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
# user inputs name and function checks if it's in use or empty
def name_obj(inv, name):
    name = name.strip()
    if name in inv:
        return False, 'Item already exists.'
    if name == "":
        return False, 'Name cannot be blank.'
    else:
        return True, f'Name is {name}.'

# user inputs quantity and function checks if it's valid
def count_obj(count):
    if count is None:                                       # if count is None, reject the input
        return False, 'Quantity cannot be None.'
    if 0 <= count <= 1000000:                               # if count is within valid range, accept
        return True, f'Quantity is {count}.'
    else:
        return False, 'Quantity must be between 0 and 1,000,000.'
    
# user inputs price and function checks if it's valid
def price_obj(price):
    if price is None:                                         # if price is None, reject the input
        return False, 'Price cannot be None.'
    if price < 0:
        return False, 'Price cannot be negative.'
    return True, f'Price is ${price:.2f}.'

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

# Assign item index for chart
def assign_item_index(inv, item):
    index = 1
    for name in sorted(inv.keys()):
        if inv[name] == item:
            return index
        index += 1


# Make chart of inventory upon request | IMPURE
def chart(inv):
    print("\nInventory")
    print(f"{'Index':<6}{'Item':<25}{'Quantity':>10}{'Price':>11}{'Value':>14}")
    print("-" * 67)
    for name, item in sorted(inv.items()):
        item_value = calculate_item_value(item)
        total_value = calculate_chart_value(inv)
        item_index = assign_item_index(inv, item)
        print(f"{item_index:^6}{name:<25}{item['quantity']:>10}{item['price']:>11.2f} {item_value:>13.2f}")
    print("-" * 67)
    print(f"{'Total Inventory Value:':<53}${total_value:>12.2f}")
    # flag low stock items
    low_stock_items = [name for name, item in inv.items() if low_stock(inv, name)]        # Create list of low stock items
    if low_stock_items:                                                                   # If there are low stock items
        print("\nLow Stock:")                                                             # Print header
        for item in low_stock_items:                                                      # Print each low stock item
            print(f"- {item} ({inv[item]['quantity']} in stock)")                         # Print item name and quantity

# main
# choices
def main(): # this big function that I hate | IMPURE
    Responses1 = ["1", "add record", "add"]
    Responses2 = ["2", "view records", "view"]
    Responses3 = ["3", "quit", "exit"]
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
3. Quit""")
        main_choice = input("Please select an option: ") # user selects2
        if main_choice.lower() in Responses1:            # add record
            # Get name
            # if name passes checks, break out of the loop
            namegoodflag = False, ''
            while namegoodflag[0] != True:
                name = input("Name of Item: ")
                namegoodflag = name_obj(inventory, name)
                print(namegoodflag[1])

            # Get quantity
            quantitygoodflag = False, ''
            while quantitygoodflag[0] != True:
                try:
                    quantity = int(input("Quantity of Item: "))
                    quantitygoodflag = count_obj(quantity)
                    print(quantitygoodflag[1])
                except (TypeError, ValueError):
                    print("Please enter a valid integer for quantity.")

            # Get price
            pricegoodflag = False, ''
            while pricegoodflag[0] != True:
                try:
                    price = float(input("Price of Item: $"))
                    pricegoodflag = price_obj(price)
                    print(pricegoodflag[1])
                except ValueError:
                    print("Please enter a valid number.")
            inventory[name] = {"quantity": quantity, "price": price}

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

        # QUIT
        elif main_choice.lower() in Responses3:
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
