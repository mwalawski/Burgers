import sqlite3

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()


class Order:
    id = 0

    def __init__(self, hour=None, phone=None):
        self.hour = hour
        self.food = {}
        self.phone = phone
        self.id = Order.id
        Order.id += 1


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS orders(ID REAL, product REAL, amount REAL, hour TEXT, phone TEXT)')


def dynamic_data_entry(id, product, amount, hour, phone):
    create_table()
    c.execute("INSERT INTO orders(ID, product, amount, hour, phone) VALUES (?,?,?,?,?)", (id, product, amount, hour, phone))
    conn.commit()


def pick_order():
    order = Order()

    print("Hello! Your order will be collected in 2 steps:")
    print("First, type name of your burger and then, give the amount.\n")
    print("Each bun has own name id given below")
    print("1 - Classic", "3 - Cheeseburger", "6 - Cheese&Bacon", "2 - Bacon", "4 - BBQ\n", sep='\n')
    tag = int(input("Please input burger id: "))
    amount = input("Give the amount: ")
    order.phone = input("Great! Please enter phone number: ")
    order.hour = input("What is estimated time of your arrival?: ")


    dynamic_data_entry(order.id, tag, amount, order.hour, order.phone)

    def testing():
        test = input("Type O to order another burger\nType N if you are new customer\nPress Enter to finish: ")
        if test == "N":
            pick_order()
        elif test == "O":
            tag = int(input("Please input burger id: "))
            amount = input("Give the amount: ")
            dynamic_data_entry(order.id, tag, amount, order.hour, order.phone)
            testing()
        else:
            print("-"*40, "See you at {}".format(order.hour), sep="\n")
            c.close()
            conn.close()

    testing()


pick_order()