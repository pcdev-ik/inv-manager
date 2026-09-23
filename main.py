"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
# check name validity
def obj_name(inv, name):
    if name in inv:
        print("Item already exists.")
        return False
    if name == "":
        print("Please enter a valid name.")
        return False
    return True
# check quantity validity
def obj_count(count):
    # Validate quantity values passed in from the caller.
    if not isinstance(count, int): # if count isn't already an integer...
        try:
            count = int(count) # ...make it an integer
        except (TypeError, ValueError): # unless it's definitely not a number...
            print("Please enter a whole number.") # ...then punish the user for their wrongdoing o(≧口≦)o
            return False
    if 0 < count <= 1000000:  # If value is good, break
        return True
    if count <= 0:
        print("Please enter a valid quantity.")
        return False
    if count > 1000000:
        print("Please enter a quantity less than 1,000,000.")
        return False
# check price validity
def obj_price(price):
    # Rewrite this to call inputs outside of the function and pass them in as arguments
    if not isinstance(price, (int, float)): # if price isn't already a number...
        try:
            price = float(price) # ...make it a float
        except (TypeError, ValueError):
            print("Please enter a valid number.")
            return False
    if price < 0:
        print("Please enter a valid price.")
        return False
    return True

# Chart Maker (this is only here to clean up the code)
def chart(inv):
    print("\nInventory")
    print(f"{'Index':<6}{'Item':<25}{'Quantity':>10}{'Price':>11}{'Value':>14}")
    print("-" * 67)
    total_value = 0
    item_index =  0
    for name, item in sorted(inv.items()):
        item_value = item["quantity"] * item["price"]
        total_value += item_value
        item_index += 1
        print(f"{item_index:^6}{name:<25}{item['quantity']:>10}{item['price']:>11.2f} {item_value:>13.2f}")
    print("-" * 67)
    print(f"{'Total Inventory Value:':<53}${total_value:>12.2f}")
    # flag low stock items
    low_stock_items = [name for name, item in inv.items() if item["quantity"] < 5]        # Create list of low stock items
    if low_stock_items:                                                                   # If there are low stock items
        print("\nLow Stock:")                                                             # Print header
        for item in low_stock_items:                                                      # Print each low stock item
            print(f"- {item} ({inv[item]['quantity']} in stock)")                         # Print item name and quantity

# main
# choices
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
    main_choice = input("Please select an option: ") # user selects
    if main_choice.lower() in Responses1:            # add record
        # Get name
        while True:
            name = input("Name of Item: ").strip() # strip spaces
            # if name passes checks, break out of the loop
            namegoodflag = obj_name(inventory, name)
            if namegoodflag:
                break
        # Get quantity
        while True:
            try:
                quantity = int(input("Quantity of Item: "))
            except ValueError:
                print("Please enter a whole number.")
                continue
            # if quantity passes checks, break out of the loop
            quantitygoodflag = obj_count(quantity)
            if quantitygoodflag:
                break
        # Get price
        while True:
            try:
                price = float(input("Price of Item: $"))
            except ValueError:
                print("Please enter a valid number.") 
                continue
            # if price passes checks, break out of the loop
            pricegoodflag = obj_price(price)
            if pricegoodflag:
                break

        inventory[name] = {"quantity": quantity, "price": price}
        # summary
        print(f"The item {name} has been added with a quantity of {quantity} and a price of ${price:.2f}")
        print(f"The total value of {name} in stock is ${(quantity * price):.2f}")
    elif main_choice.lower() in Responses2:          # view records
        if not inventory:                            # if the inventory is empty
            print("The inventory is empty.")
        else:
            # make the chart
            chart(inventory)                         # Call the chart function
    elif main_choice.lower() in Responses3:          # quit
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
