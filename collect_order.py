menu = ['B', 'BBQ', 'CL', 'CH', 'CHB']
menu_order = {item: 0 for item in menu}
orders = {}


class Order:
	id = 0

	def __init__(self, hour=None, food=None, phone=None):
		self.hour = hour
		self.food = food
		self.phone = phone
		self.id = Order.id
		Order.id += 1


def pick_order():
	print("Hello! Your order will be collected in 2 steps:",sep='\n')
	print("First, type name of your burger and then, give the amount.\n")
	print("Each bun has own name tag given below",sep='\n')
	print("CL - Classic","CH - Cheeseburger","CHB - Cheese&Bacon","B - Bacon","BBQ - Barbecue\n",sep='\n')
	tag = input("Please input burger tag: ")
	amount = input("Give the amount: ")
	menu_order[tag] = amount
	phone = input("Great! Please enter phone number: ")
	hour = input("What is estimated time of your arrival?: ")
	order = Order(hour, menu_order, phone)
	orders[order.id]=dict(order=order.food,phone=order.phone,hour=order.hour)

	print(orders)
	test=input("To make another order type Y (Yes): ")
	if test=="Y":
		pick_order()
	else:
		print("See you at {}".format(order.hour))

	print(dir(order))
pick_order()

# #counttest:
# order=Order()
# print(order.id)


# from datetime import timedelta

# #ordertimetable
# for i in range(0,465,15):
# 	print([str(timedelta(minutes=810+i))[:-3],0,0,0,0,0,0,0,0])
