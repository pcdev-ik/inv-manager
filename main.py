"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
# Define component functions
#  get name of items
def obj_name(inv):
    while True:
        name = (input("Name of Item: ")).strip()
        if name in inv:
            print("Item already exists.")
        if name.strip() == "":
            print("Please enter a valid name.")
        else:
            break
    return name

def obj_count():
    while True:
        while True:
            try:
                count = int(input("Quantity of Item: ")) # Input always records data as a string so it must be translated
                if count > 0 and count <= 1000000:       # If value is good, break
                    break
                elif count <= 0:
                    print("Please enter a valid quantity.")
                elif count > 1000000:
                    print("Please enter a quantity less than 1,000,000.")
            except ValueError:
                print("Please enter a whole number.")
        if count >= 0:
            break
    return count

def obj_price():
    while True:
        try:
            price = float(input("Price of Item: $"))
            if price < 0:
                price = price * -1
                print(f"Price has been converted to positive.")
            return price
        except ValueError:
            print("Please enter a valid number.")

# Define big function that takes all inputs
def add_item(inv):
    name = obj_name(inv)
    count = obj_count()
    price = obj_price()
    # adds the item to the inventory dictionary
    inv[name] = {"quantity": count, "price": price}
    # summary
    print(f"The item {name} has been added with a quantity of {count} and a price of ${price:.2f}")
    print(f"The total value of {name} in stock is ${(count * price):.2f}")

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
        add_item(inventory)                          # add_item is called
    elif main_choice.lower() in Responses2:          # view records
        if not inventory:                            # if the inventory is empty
            print("The inventory is empty.")
        else:
            # make the chart
            chart(inventory)                         # Call the chart function
    elif main_choice.lower() in Responses3:                                                                            # quit
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
