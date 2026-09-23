"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
# check name validity
def name_obj(inv, name):
    if name in inv:
        return False
    if name == "":
        return False
    return True
# check quantity validity
def count_obj(count):
    if not isinstance(count, int):                          # if count isn't already an integer...
        try:
            count = int(count)                              # ...make it an integer
        except (TypeError, ValueError):                     # unless it's definitely not a number...
            return False                                    # ...then punish the user for their wrongdoing o(≧口≦)o
    if 0 < count <= 1000000:  # If value is good, break
        return True
    else:
        return False
# check price validity
def price_obj(price):
    if not isinstance(price, (int, float)): # if price isn't already a number...
        try:
            price = float(price) # ...make it a float
        except (TypeError, ValueError):
            return False
    if price < 0:
        return False
    return True

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
            namegoodflag = name_obj(inventory, name)
            if namegoodflag:
                break
            else: 
                print("Please enter a name that is not blank or already in use.")
        # Get quantity
        while True:
            try:
                quantity = int(input("Quantity of Item: "))
            except ValueError:
                print("Please enter a whole number.")
                continue
            # if quantity passes checks, break out of the loop
            quantitygoodflag = count_obj(quantity)
            if quantitygoodflag:
                break
            else:
                print("Please enter a valid quantity (1-1,000,000).")
        # Get price
        while True:
            try:
                price = float(input("Price of Item: $"))
            except ValueError:
                print("Please enter a valid number.") 
                continue
            # if price passes checks, break out of the loop
            pricegoodflag = price_obj(price)
            if pricegoodflag:
                break
            else:
                print("Please enter a valid price (greater than or equal to 0).")
        inventory[name] = {"quantity": quantity, "price": price}
        # summary
        print(f"The item {name} has been added with a quantity of {quantity} and a price of ${price:.2f}")
        print(f"The total value of {name} in stock is ${(quantity * price):.2f}")
    elif main_choice.lower() in Responses2:          # view records
        if not inventory:                            # if the inventory is empty
            print("The inventory is empty.")
        else:
            # make the chart
            print("\nInventory")
            print(f"{'Index':<6}{'Item':<25}{'Quantity':>10}{'Price':>11}{'Value':>14}")
            print("-" * 67)
            total_value = 0
            item_index =  0
            for name, item in sorted(inventory.items()):
                item_value = item["quantity"] * item["price"]
                total_value += item_value
                item_index += 1
                print(f"{item_index:^6}{name:<25}{item['quantity']:>10}{item['price']:>11.2f} {item_value:>13.2f}")
            print("-" * 67)
            print(f"{'Total Inventory Value:':<53}${total_value:>12.2f}")
            # flag low stock items
            low_stock_items = [name for name, item in inventory.items() if item["quantity"] < 5]        # Create list of low stock items
            if low_stock_items:                                                                         # If there are low stock items
                print("\nLow Stock:")                                                                   # Print header
                for item in low_stock_items:                                                            # Print each low stock item2
                    print(f"- {item} ({inventory[item]['quantity']} in stock)")                         # Print item name and quantity
   
            
    elif main_choice.lower() in Responses3:          # quit
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
