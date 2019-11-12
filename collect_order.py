import sqlite3
import time

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
    c.execute('CREATE TABLE IF NOT EXISTS orders(ID REAL, product REAL, amount REAL, hour REAL, phone TEXT)')


def dynamic_data_entry(id, product, amount, hour, phone):
    create_table()
    c.execute("INSERT INTO orders(ID, product, amount, hour, phone) VALUES (?,?,?,?,?)", (id, product, amount, hour, phone))
    conn.commit()

def check_availabilty(order_amount, burger_limit=8):
    current_time = (time.ctime(time.time())[11:16])
    c.execute('SELECT hour FROM orders WHERE hour<? GROUP BY hour HAVING SUM(amount+?)<=?',(current_time, order_amount, burger_limit))
    return [hour[0] for hour in c.fetchall()]

def checkout():
    order_id=input('Enter your order ID: ')
    c.execute('SELECT SUM(p.price*o.amount) FROM products p, orders o WHERE o.ID=? AND o.product=p.ID',(order_id))
    return c.fetchall()[0][0]


def pick_order():
    order = Order()

    print("Hello! Your order will be collected in 2 steps:")
    print("First, type name of your burger and then, give the amount.\n")
    print("Each bun has own name id given below")
    print("1 - Classic", "3 - Cheeseburger", "6 - Cheese&Bacon", "2 - Bacon", "4 - BBQ\n", sep='\n')
    tag = int(input("Please input burger id: "))
    amount = input("Give the amount: ")

    print("Right now we can prepare your burgers at: ")
    for count, value in enumerate(check_availabilty(amount), start=1):
        print(count, '-', value)

    chosen_hour=int(input("Choose preferred hour by typing its number "))-1
    order.phone = input("Please enter phone number: ")
    order.hour = check_availabilty(amount)[chosen_hour]


    dynamic_data_entry(order.id, tag, amount, order.hour, order.phone)


    def service():
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

#     service()
#
#
# pick_order()

print(checkout())
""""----------------------------------------------------------------"""
