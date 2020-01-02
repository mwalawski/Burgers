from os import path
from interface import *
from database import *

class App(Interface):
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('Food Order')
		self.root.config(bg='#454c54')
		self.create_top_bar()
		self.create_menu_bar()
		self.create_order_bar()
		self.create_data_bar()
		self.root.mainloop()


if __name__ == '__main__':
	if not path.exists('orders.db'):
		create = Database()
	run = App()
