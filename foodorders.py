#from datetime import timedelta

menu=['B','BBQ','CL','CH','CHB']


class Order:
	id=0
	def __init__(self,hour=None,food=None,phone=None):
		self.hour=hour
		self.food=food
		self.phone=phone
		self.id=Order.id
		Order.id+=1


def pickuporder():

	print("""
Hello! Your order will be collected in 2 steps:
First, type nametag of your burger and then, give the amount.

Each bun has own nametag given below:
CL- Classic
CH - Cheeseburger
CHB - Cheese&Bacon
B - Bacon
BBQ - Barbercue
""")

	burgtag=input("Please input burger tag: ")
	amount=input("Give the amount: ")
	{item:0 for item in menu}[burgtag]=amount

	print("""Great! Now, please enter your phone number and estimated time of your arrival""")
	phone=input("Enter phone number")
	hour=input()
	order=Order(hour,menu_dict,phone)






order=Order()

print(order.food)

pickuporder()



# #counttest:
# order=Order()
# print(order.id)

# #ordertimetable
# for i in range(0,465,15):
# 	print([str(timedelta(minutes=810+i))[:-3],0,0,0,0,0,0,0,0])