import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()


class OrderMachine():
	def app(self):
		self.root = tk.Tk()
		self.root.title = "FoodOrder"
		self.create_top_bar()
		self.create_menu_bar()
		self.create_order_bar()
		self.create_data_bar()
		self.root.mainloop()

	def create_top_bar(self):
		top_bar_frame = tk.Frame(self.root, bg='#8317ff', height=250, width=320)
		top_bar_frame.grid(row=0, column=7, rowspan=7, columnspan=7, padx=5, pady=5, sticky='nesw')

	def create_menu_bar(self):
		menu_bar_frame = tk.Frame(self.root, bg='pink')
		menu_bar_frame.grid(row=0, column=0, rowspan=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		self.entries = []
		for count, query in enumerate(c.execute('SELECT id, name FROM products ORDER BY id')):
			label = tk.Label(menu_bar_frame, text=query[1])
			label.grid(row=2 *(count // 3), column=count % 3, pady=15, padx=15)
			test = tk.Spinbox(menu_bar_frame, from_=0, to=50, width=5, font=10)
			test.grid(row=2 *(count // 3) + 1, column=count % 3, ipady=5, padx=20)
			self.entries.append((query[0], test))

	def create_data_bar(self):
		data_bar_frame = tk.Frame(self.root, bg='khaki')
		data_bar_frame.grid(row=10, column=0, columnspan=7,  padx=5, pady=5, sticky='nesw')
		order_id_label = tk.Label(data_bar_frame, text="Order ID:")
		order_id_label.grid(row=0, column=0, sticky='e', padx=20)
		order_id_entry = tk.Entry(data_bar_frame)
		order_id_entry.grid(row=0, column=1, padx=20, pady=27, sticky='e')
		customer_name_label = tk.Label(data_bar_frame, text="Name:")
		customer_name_label.grid(row=1, column=0, padx=20, sticky='e')
		customer_name_entry = tk.Entry(data_bar_frame)
		customer_name_entry.grid(row=1, column=1, padx=20, sticky='e')
		customer_phone_label = tk.Label(data_bar_frame, text="Phone number:")
		customer_phone_label.grid(row=2, column=0, padx=20, sticky='e')
		customer_phone_entry = tk.Entry(data_bar_frame)
		customer_phone_entry.grid(row=2, column=1, padx=20, pady=27, sticky='e')
		order_hour_label = tk.Label(data_bar_frame, text='Hour:')
		order_hour_label.grid(row=3, column=0, padx=20, sticky='e')
		order_hour_combobox = ttk.Combobox(data_bar_frame, width=17)
		order_hour_combobox.grid(row=3, column=1, padx=20, sticky='e')

	def create_order_bar(self):
		order_bar_frame = tk.Frame(self.root, bg='magenta')
		order_bar_frame.grid(row=10, column=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		text1 = tk.Listbox(order_bar_frame)
		text1.grid(row=0, column=0, padx=5, pady=15, sticky='nesw', ipadx=95, ipady=10)
		summary_button = tk.Button(order_bar_frame, text="Summary", command=self.add_order_to_database)
		summary_button.grid(row=1, column=0, pady=5)

	def add_order_to_database(self):
		pass


if __name__ == '__main__':
	dm = OrderMachine()
	dm.app()


# entry = []
#
# for count, query in enumerate(c.execute('SELECT id, name FROM products ORDER BY id')):
# 	label = tk.Label(bottomleft, text=query[1])
# 	label.grid(row=2 * (count // 3), column=count % 3, pady=15)
# 	test = tk.Spinbox(bottomleft, from_=0, to=50, width=5, font=10)
# 	test.grid(row=2 * (count // 3) + 1, column=count % 3, ipady=5)
# 	bottomleft.grid_columnconfigure(count % 3, minsize=150)
# 	entry.append((query[0], test))
#
#
# def get_values():  # passing values from spinbox
# 	for spinbox in entry:
# 		print(spinbox[0], ' -->', spinbox[1].get())