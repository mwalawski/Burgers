import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import time
from tkinter import messagebox

conn = sqlite3.connect('testing3.db')
c = conn.cursor()


class OrderMachine():

	def app(self):
		self.root = tk.Tk()
		self.root.title("Food Order")
		self.root.config(bg='#454c54')
		self.create_top_bar()
		self.create_menu_bar()
		self.create_order_bar()
		self.create_data_bar()
		self.root.mainloop()

	def create_top_bar(self):
		top_bar_frame = tk.Frame(self.root, bg='#2b3138', height=250, width=320)
		top_bar_frame.grid(row=0, column=7, rowspan=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		self.order_summary_list = tk.Text(top_bar_frame, width=39, height=14)
		self.order_summary_list.grid(row=0, column=0, padx=5, pady=15)

	def create_menu_bar(self):
		menu_bar_frame = tk.Frame(self.root, bg='#2b3138')
		menu_bar_frame.grid(row=0, column=0, rowspan=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		self.entries = []
		for count, query in enumerate(c.execute('SELECT product_id, name FROM products ORDER BY  product_id')):
			label = tk.Label(menu_bar_frame, text=query[1], bg='#2b3138', fg='white', font='TkDefaultFont 9 bold')
			label.grid(row=2 * (count // 3), column=count % 3, pady=15, padx=15)
			test = tk.Spinbox(menu_bar_frame, from_=0, to=50, width=5, font=10,
							  command=lambda: self.update_summary_list())
			test.grid(row=2 * (count // 3) + 1, column=count % 3, ipady=5, padx=25)
			self.entries.append((query[0], test))
			for number in range(10):
				test.bind("<KeyRelease-" + str(number) + ">", self.update_summary_list)

	def create_data_bar(self):
		data_bar_frame = tk.Frame(self.root, bg='#2b3138')
		data_bar_frame.grid(row=10, column=0, columnspan=7, padx=5, pady=5, sticky='nesw')
		order_id_label = tk.Label(data_bar_frame, text="Order Number:", bg='#2b3138', fg='white',
								  font='TkDefaultFont 9 bold')
		order_id_label.grid(row=0, column=0, sticky='e', padx=20)
		self.order_id_entry = tk.Entry(data_bar_frame, state='disabled', disabledbackground='white',
									   disabledforeground='black')
		self.order_id_entry.grid(row=0, column=1, padx=20, pady=16, sticky='e')
		customer_phone_label = tk.Label(data_bar_frame, text="Phone Number:", bg='#2b3138', fg='white',
										font='TkDefaultFont 9 bold')
		customer_phone_label.grid(row=1, column=0, padx=20, sticky='e')
		self.customer_phone_entry = tk.Entry(data_bar_frame)
		self.customer_phone_entry.grid(row=1, column=1, padx=20, pady=16, sticky='e')
		order_hour_label = tk.Label(data_bar_frame, text='Hour:', bg='#2b3138', fg='white', font='TkDefaultFont 9 bold')
		order_hour_label.grid(row=2, column=0, padx=20, sticky='e')
		self.order_hour_combobox = ttk.Combobox(data_bar_frame, width=17)
		self.order_hour_combobox.grid(row=2, column=1, padx=20, pady=16, sticky='e')
		self.order_hour_combobox.config(state='readonly')

		self.checkbox_var = tk.IntVar()
		overbook_box = tk.Checkbutton(data_bar_frame, variable=self.checkbox_var,
									  command=lambda: self.update_summary_list(), bg='#2b3138')
		overbook_box.grid(row=2, column=2, pady=4)
		overbook_text = tk.Label(data_bar_frame, text='OB', bg='#2b3138', fg='white', font='TkDefaultFont 9 bold')
		overbook_text.grid(row=2, column=2, sticky='n', ipadx=3)

		button_frame = tk.Frame(data_bar_frame, bg='#2b3138')
		button_frame.grid(row=3, column=0, columnspan=3)

		next_button = tk.Button(button_frame, text="Add New", command=lambda: self.add_order_to_database())
		next_button.grid(row=3, column=0, padx=8, pady=25)
		summary_button = tk.Button(button_frame, text="Update Order", command=lambda: self.update_order_to_database())
		summary_button.grid(row=3, column=1, padx=8, pady=25)

		clear_button = tk.Button(button_frame, text="Clear All", command=lambda: self.clear_all())
		clear_button.grid(row=3, column=2, padx=8, pady=25)
		delete_button = tk.Button(button_frame, text="Delete Order", command=lambda: self.delete_order())
		delete_button.grid(row=3, column=3, padx=8, pady=25)

	def create_order_bar(self):
		order_bar_frame = tk.Frame(self.root, bg='#2b3138')
		order_bar_frame.grid(row=10, column=7, columnspan=7, padx=5, pady=5, sticky='nesw')
		label = tk.Label(order_bar_frame, text='Filter orders by hour :', bg='#2b3138', fg='white',
						 font='TkDefaultFont 9 bold')
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

	def update_summary_list(self, event=None):
		text = ''
		order_amount = 0
		for spinbox in self.entries:
			if spinbox[1].get() != '0' and spinbox[1].get() != '':
				c.execute('SELECT name FROM products WHERE  product_id=?', (spinbox[0],))
				text += "{:7}: {}\n".format(c.fetchall()[0][0], int(spinbox[1].get()))
			order_amount += int(spinbox[1].get())
		self.order_summary_list.delete("1.0", tk.END)
		self.order_summary_list.insert(tk.END, text)
		if order_amount != 0:
			self.check_availability(order_amount)

	def checkout(self, order_id):
		c.execute('''SELECT SUM(p.price*q.amount) 
					 FROM products p, quantity q
					 WHERE q.product_id=p.product_id AND q.order_id=?''',
				  (int(order_id),)
				  )

		checkout_text = "\n" * 3 + "-" * 38 + "\n" + "Price:  " + str(c.fetchall()[0][0]) + " PLN"
		self.order_summary_list.insert(tk.END, checkout_text)
		conn.commit()

	def check_not_empty_spinbox(self):
		for spinbox in self.entries:
			if spinbox[1].get() != '0' and spinbox[1].get() != '':
				return True

	def check_not_empty_hour(self):
		if self.order_hour_combobox.get() != '' and self.order_hour_combobox.get()[0] != '*':
			return True
		else:
			self.order_hour_combobox.delete("0", tk.END)
			self.order_hour_combobox.config(state='normal')
			self.order_hour_combobox.insert(tk.END, '*SET HOUR*')
			self.order_hour_combobox.config(state='readonly')

	def add_order_to_database(self):
		self.generate_order_id()

		if self.check_not_empty_hour() == 1 and self.check_not_empty_spinbox() == 1:
			c.execute('INSERT INTO orders (order_id, hour, phone) VALUES (?, ?, NULLIF(?,""))',
					  (int(self.order_id_entry.get()),
					   self.order_hour_combobox.get()[0:5],
					   self.customer_phone_entry.get())
					  )

			for spinbox in self.entries:
				if spinbox[1].get() != '0' and spinbox[1].get() != '':
					c.execute('INSERT INTO quantity (product_id, amount, order_id) VALUES (?,?,?)',
							  (spinbox[0],
							   spinbox[1].get(),
							   int(self.order_id_entry.get()))
							  )

			self.checkout(self.order_id_entry.get())

	def update_order_to_database(self):
		if self.check_not_empty_hour() == 1 and self.check_not_empty_spinbox() == 1:
			c.execute('UPDATE orders SET hour=?, phone=NULLIF(?,"") WHERE order_id=?',
					  (self.order_hour_combobox.get()[0:5],
					   self.customer_phone_entry.get(),
					   int(self.order_id_entry.get()))
					  )

			c.execute('DELETE FROM quantity WHERE order_id=?', (int(self.order_id_entry.get()),))

			for spinbox in self.entries:
				if spinbox[1].get() != '0' and spinbox[1].get() != '':
					c.execute('INSERT INTO quantity (product_id, amount, order_id) VALUES (?,?,?)',
							  (spinbox[0],
							   spinbox[1].get(),
							   int(self.order_id_entry.get()))
							  )

			self.checkout(self.order_id_entry.get())

	def delete_order(self):
		if self.order_id_entry.get() != '':
			confirm_delete = tk.messagebox.askyesno("Warning", "Do you want to delete Order #{} ?".format(
				self.order_id_entry.get()))
			if confirm_delete == True:
				c.execute("PRAGMA foreign_keys=ON")
				c.execute('DELETE FROM orders WHERE order_id=?', (int(self.order_id_entry.get()),))
				conn.commit()
				self.clear_all()
			else:
				pass

	def set_order_box(self, event=None):
		self.order_box.delete(0, tk.END)
		hour = self.filter_order_hour_combo.get() + ':' + self.filter_order_minute_combo.get()

		c.execute('SELECT order_id FROM orders WHERE hour=?', (hour,))
		orders = c.fetchall()
		if len(orders) != 0:
			for item in orders:
				self.order_box.insert(tk.END, "ORDER  #{}".format(item[0]))

	def pass_selected_order_box(self, event=None):
		selection = self.order_box.curselection()
		selected_id = ''
		if len(selection) != 0:
			for letter in self.order_box.get(selection[0]):
				if letter.isdigit():
					selected_id = selected_id + letter

			self.order_id_entry.config(state='normal')
			self.order_id_entry.delete("0", tk.END)
			self.order_id_entry.insert(tk.END, selected_id)
			self.order_id_entry.config(state='disabled')

			for spinbox in self.entries:
				spinbox[1].delete("0", tk.END)
				spinbox[1].insert(tk.END, "0")

			c.execute('SELECT phone, hour FROM orders WHERE order_id=?', (selected_id,))
			(phone, hour) = c.fetchall()[0]
			self.customer_phone_entry.delete("0", tk.END)

			if phone != None:
				self.customer_phone_entry.insert(tk.END, phone)

			self.order_hour_combobox.delete("0", tk.END)
			self.order_hour_combobox.insert(tk.END, hour)

			c.execute('SELECT product_id, amount FROM quantity q WHERE order_id=?', (selected_id,))

			for product_id, amount in c.fetchall():
				for spinbox in self.entries:
					if spinbox[0] == product_id:
						spinbox[1].delete("0", tk.END)
						spinbox[1].insert(tk.END, str(amount))
			self.update_summary_list()
			self.checkout(selected_id)

	def set_filter_order_minute_combo(self, event=None):
		self.filter_order_minute_combo.set('')
		if self.filter_order_hour_combo.get() == '13':
			self.filter_order_minute_combo['values'] = ['45']
		elif self.filter_order_hour_combo.get() == '21':
			self.filter_order_minute_combo['values'] = ['00', '15']
		elif self.filter_order_hour_combo.get() in [str(x) for x in range(14, 21)]:
			self.filter_order_minute_combo['values'] = ['00', '15', '30', '45']
		else:
			self.filter_order_minute_combo['values'] = []

	def generate_order_id(self):
		if self.order_id_entry.get() == '':
			self.order_id_entry.config(state='normal')
			c.execute('SELECT MAX(order_id)+1 FROM orders')
			self.order_id_entry.insert(tk.END, c.fetchall()[0][0])
			self.order_id_entry.config(state='disabled')

	def check_availability(self, order_amount, limit=10):
		all_hour_slots = [str(x // 60) + ':' + str(x % 60) + '0' if x % 60 == 0 else str(x // 60) + ':' + str(x % 60)
						  for x in range(825, 1280, 15)]
		preparation_time_gap = 15
		current_time = time.strftime('%H:%M', time.localtime(time.time() + preparation_time_gap * 60))

		for slot in all_hour_slots[:]:
			if slot < current_time:
				all_hour_slots.remove(slot)

		c.execute('''SELECT o.hour, SUM(q.amount)
					FROM orders o, quantity q 
					WHERE q.order_id=o.order_id AND o.hour>=?
					GROUP BY o.hour''',
				  (current_time,))

		available_hour_slots = []
		for stored_slot, stored_amount in c.fetchall():
			if stored_slot in all_hour_slots[:]:
				all_hour_slots.remove(stored_slot)
				if stored_amount + order_amount <= limit:
					available_hour_slots.append(stored_slot)
				elif self.checkbox_var.get() == 1:
					overbook = stored_amount + order_amount - limit
					available_hour_slots.append('{} + {} OVERBOOK'.format(stored_slot, overbook))
				else:
					pass

		for left_slot in all_hour_slots:
			if order_amount <= limit:
				available_hour_slots.append(left_slot)
			elif self.checkbox_var.get() == 1:
				overbook = order_amount - limit
				available_hour_slots.append('{} + {} OVERBOOK'.format(left_slot, overbook))
			else:
				pass

		self.order_hour_combobox['values'] = sorted(available_hour_slots)

	def clear_all(self):
		for spinbox in self.entries:
			spinbox[1].delete("0", tk.END)
			spinbox[1].insert(tk.END, "0")
		self.order_id_entry.insert(tk.END, "0")
		self.order_hour_combobox['values'] = []
		self.update_summary_list()

		self.order_id_entry.config(state='normal')
		self.order_id_entry.delete("0", tk.END)
		self.order_id_entry.config(state='disabled')

		self.customer_phone_entry.delete("0", tk.END)

		self.order_hour_combobox.config(state='normal')
		self.order_hour_combobox.delete("0", tk.END)
		self.order_hour_combobox.config(state='readonly')

		self.filter_order_hour_combo.set('')
		self.filter_order_minute_combo.set('')
		self.set_filter_order_minute_combo()
		self.order_box.delete(0, tk.END)


if __name__ == '__main__':
	dm = OrderMachine()
	dm.app()
