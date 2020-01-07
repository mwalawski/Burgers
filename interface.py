import tkinter as tk
import tkinter.ttk as ttk
from operations import Operations


class StyledLabel(tk.Label):
	def __init__(self, *args, **kwargs):
		tk.Label.__init__(self, *args, **kwargs)
		self.config(bg='#2b3138', fg='white', font='TkDefaultFont 9 bold')


class Interface(Operations):
	def __init__(self):
		Operations.__init__(self)

	def create_top_bar(self):
		top_bar_frame = tk.Frame(self.root, bg='#2b3138', height=250, width=320)
		top_bar_frame.grid(row=0, column=7, rowspan=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		self.order_summary_list = tk.Text(top_bar_frame, width=39, height=14)
		self.order_summary_list.grid(row=0, column=0, padx=5, pady=15)

	def create_menu_bar(self):
		menu_bar_frame = tk.Frame(self.root, bg='#2b3138')
		menu_bar_frame.grid(row=0, column=0, rowspan=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		self.entries = [] #list to access ordering spinboxes
		for count, query in enumerate(self.c.execute('SELECT product_id, name FROM products ORDER BY  product_id')):
			label = StyledLabel(menu_bar_frame, text=query[1])
			label.grid(row=2 * (count // 3), column=count % 3, pady=15, padx=15)
			ordered_amount = tk.Spinbox(menu_bar_frame, from_=0, to=50, width=5, font=10,
							  command=lambda: self.update_summary_list())
			ordered_amount.grid(row=2 * (count // 3) + 1, column=count % 3, ipady=5, padx=25)
			self.entries.append((query[0], ordered_amount))
			for number in range(10):
				ordered_amount.bind("<KeyRelease-" + str(number) + ">", self.update_summary_list)

	def create_data_bar(self):
		data_bar_frame = tk.Frame(self.root, bg='#2b3138')
		data_bar_frame.grid(row=10, column=0, columnspan=7, padx=5, pady=5, sticky='nesw')

		order_id_label = StyledLabel(data_bar_frame, text='Order Number:')
		order_id_label.grid(row=0, column=0, sticky='e', padx=20)
		self.order_id_entry = tk.Entry(data_bar_frame, width=23, state='disabled', disabledbackground='white',
									   disabledforeground='black')
		self.order_id_entry.grid(row=0, column=1, padx=20, pady=16, sticky='e')

		customer_phone_label = StyledLabel(data_bar_frame, text='Phone Number:')
		customer_phone_label.grid(row=1, column=0, padx=20, sticky='e')
		self.customer_phone_entry = tk.Entry(data_bar_frame, width=23)
		self.customer_phone_entry.grid(row=1, column=1, padx=20, pady=16, sticky='e')

		order_hour_label = StyledLabel(data_bar_frame, text='Hour:')
		order_hour_label.grid(row=2, column=0, padx=20, sticky='e')
		self.order_hour_combobox = ttk.Combobox(data_bar_frame)
		self.order_hour_combobox.grid(row=2, column=1, padx=20, pady=16, sticky='e')
		self.order_hour_combobox.config(state='readonly')

		self.checkbox_var = tk.IntVar()
		overbook_box = tk.Checkbutton(data_bar_frame, variable=self.checkbox_var,
									  command=lambda: self.update_summary_list(), bg='#2b3138')
		overbook_box.grid(row=2, column=2, pady=4)
		overbook_text = StyledLabel(data_bar_frame, text='OB')
		overbook_text.grid(row=2, column=2, sticky='n', ipadx=3)

		button_frame = tk.Frame(data_bar_frame, bg='#2b3138')
		button_frame.grid(row=3, column=0, columnspan=3)

		next_button = tk.Button(button_frame, text='Add New', command=lambda: self.add_order_to_database())
		next_button.grid(row=3, column=0, padx=8, pady=25)

		summary_button = tk.Button(button_frame, text='Update Order', command=lambda: self.update_order_to_database())
		summary_button.grid(row=3, column=1, padx=8, pady=25)

		clear_button = tk.Button(button_frame, text='Clear All', command=lambda: self.clear_all())
		clear_button.grid(row=3, column=2, padx=8, pady=25)

		delete_button = tk.Button(button_frame, text='Delete Order', command=lambda: self.delete_order())
		delete_button.grid(row=3, column=3, padx=8, pady=25)

	def create_order_bar(self):
		order_bar_frame = tk.Frame(self.root, bg='#2b3138')
		order_bar_frame.grid(row=10, column=7, columnspan=7, padx=5, pady=5, sticky='nesw')

		label = StyledLabel(order_bar_frame, text='Filter orders by hour :')
		label.grid(row=0, column=1, sticky='w', padx=15, pady=8)

		self.filter_order_hour_combo = ttk.Combobox(order_bar_frame, width=5)
		self.filter_order_hour_combo.grid(row=0, column=1, sticky='e')
		self.filter_order_hour_combo['values'] = [x for x in range(13, 22)]
		self.filter_order_hour_combo.bind('<<ComboboxSelected>>', self.set_filter_order_minute_combo)

		self.filter_order_minute_combo = ttk.Combobox(order_bar_frame, width=5)
		self.filter_order_minute_combo.grid(row=0, column=2, sticky='w')
		self.filter_order_minute_combo.bind('<<ComboboxSelected>>', self.set_order_box)

		self.order_box = tk.Listbox(order_bar_frame)
		self.order_box.grid(row=1, column=0, columnspan=3, padx=5, sticky='nesw', ipadx=95, ipady=10)
		self.order_box.bind('<<ListboxSelect>>', self.pass_selected_order_box)
