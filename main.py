"""
I haven't made a program since a scripting class nearly a year ago (✿◕_◕)
I miss PyCharm... ( 〒▽〒)
"""
print(r"""
.-. .-. .----..-..-.   .-.
| | | |{ {__  | ||  `.'  |
\ \_/ /.-._} }| || |\ /| |
 `---' `----' `-'`-' ` `-'
 Very Simple Inventory Manager""")

# Define component functions
#  get name of items
def obj_name(inv):
    while True:
        name = str(input("Name of Item: ")).strip()
        if name in inv:
            print("Item already exists.")
        if name.strip() == "":
            print("Please enter a valid name.")
        else:
            break
    return name

def obj_count():
    while True:
        try:
            count = int(input("Quantity of Item: "))
            if count < 0:
                print("Please enter a valid quantity.")
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
                print("Price has been converted to positive.")
                price = price * -1
            return price
        except ValueError:
            print("Please enter a valid number.")

# Define big function that takes all inputs
def add_item(inv):
    name = obj_name(inv)
    count = obj_count()
    price = obj_price()
    # at the end
    print(f"The item {name} has been added with a quantity of {count} and a price of ${price}")
    print(f"The total value of {name}(s) in stock is ${count * price}.")


# main
inventory = {}
add_item(inventory)
