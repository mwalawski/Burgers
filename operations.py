import time
from tkinter import messagebox
from database import Database


class Operations(Database):
	def __init__(self):
		Database.__init__(self)

	def update_summary_list(self, event=None):
		ordered_products = ''
		ordered_amount = 0
		for spinbox in self.entries:
			if spinbox[1].get() != '0' and spinbox[1].get() != '':
				self.c.execute('SELECT name FROM products WHERE  product_id=?', (spinbox[0],))
				ordered_products += "{:7}: {}\n".format(self.c.fetchall()[0][0], int(spinbox[1].get()))
			ordered_amount += int(spinbox[1].get())
		self.order_summary_list.delete('1.0', 'end')
		self.order_summary_list.insert('end', ordered_products)
		if ordered_amount != 0:
			self.check_availability(ordered_amount)

	def checkout(self, order_id):
		self.c.execute('''SELECT SUM(p.price*q.amount) 
					FROM products p, quantity q
					WHERE q.product_id=p.product_id AND q.order_id=?''',
					(int(order_id),)
					)
		checkout_text = "\n" * 3 + "-" * 38 + "\n" + "Price:  " + str(self.c.fetchall()[0][0]) + " PLN"
		self.order_summary_list.insert('end', checkout_text)

	def check_not_empty_spinbox(self):
		for spinbox in self.entries:
			if spinbox[1].get() != '0' and spinbox[1].get() != '':
				return True

	def check_not_empty_hour(self):
		if self.order_hour_combobox.get() != '' and self.order_hour_combobox.get()[0] != '*':
			return True
		else:
			self.order_hour_combobox.delete('0', 'end')
			self.order_hour_combobox.config(state='normal')
			self.order_hour_combobox.insert('end', '*SET HOUR*')
			self.order_hour_combobox.config(state='readonly')

	def add_order_to_database(self):
		self.generate_order_id()
		if self.check_not_empty_hour() == 1 and self.check_not_empty_spinbox() == 1:
			self.c.execute('INSERT INTO orders (order_id, hour, phone) VALUES (?, ?, NULLIF(?,""))',
					  (int(self.order_id_entry.get()),
					  self.order_hour_combobox.get()[0:5],
					  self.customer_phone_entry.get())
					  )
			for spinbox in self.entries:
				if spinbox[1].get() != '0' and spinbox[1].get() != '':
					self.c.execute('INSERT INTO quantity (product_id, amount, order_id) VALUES (?,?,?)',
							  (spinbox[0],
							   spinbox[1].get(),
							   int(self.order_id_entry.get()))
							  )

			self.checkout(self.order_id_entry.get())
		self.conn.commit()

	def update_order_to_database(self):
		if self.check_not_empty_hour() == 1 and self.check_not_empty_spinbox() == 1:
			self.c.execute('UPDATE orders SET hour=?, phone=NULLIF(?,"") WHERE order_id=?',
					  (self.order_hour_combobox.get()[0:5],
					   self.customer_phone_entry.get(),
					   int(self.order_id_entry.get()))
					  )
			self.c.execute('DELETE FROM quantity WHERE order_id=?', (int(self.order_id_entry.get()),))

			for spinbox in self.entries:
				if spinbox[1].get() != '0' and spinbox[1].get() != '':
					self.c.execute('INSERT INTO quantity (product_id, amount, order_id) VALUES (?,?,?)',
							  (spinbox[0],
							   spinbox[1].get(),
							   int(self.order_id_entry.get()))
							  )
			self.checkout(self.order_id_entry.get())
		self.conn.commit()

	def delete_order(self):
		if self.order_id_entry.get() != '':
			confirm_delete = messagebox.askyesno("Warning", "Do you want to delete Order #{} ?".format(
				self.order_id_entry.get()))
			if confirm_delete == True:
				self.c.execute('PRAGMA foreign_keys=ON')
				self.c.execute('DELETE FROM orders WHERE order_id=?', (int(self.order_id_entry.get()),))
				self.conn.commit()
				self.clear_all()
			else:
				pass
		self.conn.commit()

	def set_order_box(self, event=None):
		self.order_box.delete(0, 'end')
		hour = self.filter_order_hour_combo.get() + ':' + self.filter_order_minute_combo.get()
		self.c.execute('SELECT order_id FROM orders WHERE hour=?', (hour,))
		orders = self.c.fetchall()
		if len(orders) != 0:
			for item in orders:
				self.order_box.insert('end', "ORDER  #{}".format(item[0]))

	def pass_selected_order_box(self, event=None):
		selection = self.order_box.curselection()
		selected_id = ''
		if len(selection) != 0:
			for letter in self.order_box.get(selection[0]):
				if letter.isdigit():
					selected_id = selected_id + letter
			self.order_id_entry.config(state='normal')
			self.order_id_entry.delete("0", 'end')
			self.order_id_entry.insert('end', selected_id)
			self.order_id_entry.config(state='disabled')

			for spinbox in self.entries:
				spinbox[1].delete("0", 'end')
				spinbox[1].insert('end', "0")
			self.c.execute('SELECT phone, hour FROM orders WHERE order_id=?', (selected_id,))
			(phone, hour) = self.c.fetchall()[0]
			self.customer_phone_entry.delete("0", 'end')

			if phone != None:
				self.customer_phone_entry.insert('end', phone)
			self.order_hour_combobox.config(state='normal')
			self.order_hour_combobox.delete("0", 'end')
			self.order_hour_combobox.insert('end', hour)
			self.order_hour_combobox.config(state='readonly')
			self.c.execute('SELECT product_id, amount FROM quantity q WHERE order_id=?', (selected_id,))

			for product_id, amount in self.c.fetchall():
				for spinbox in self.entries:
					if spinbox[0] == product_id:
						spinbox[1].delete("0", 'end')
						spinbox[1].insert('end', str(amount))
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
			self.c.execute('SELECT IFNULL(MAX(order_id)+1,1) FROM orders')
			self.order_id_entry.insert('end', self.c.fetchall()[0][0])
			self.order_id_entry.config(state='disabled')

	def check_availability(self, order_amount, limit=10):
		all_hour_slots = [str(x // 60) + ':' + str(x % 60) + '0' if x % 60 == 0 else str(x // 60) + ':' + str(x % 60)
						  for x in range(825, 1280, 15)]
		preparation_time_gap = 15
		current_time = time.strftime('%H:%M', time.localtime(time.time() + preparation_time_gap * 60))

		for slot in all_hour_slots[:]:
			if slot < current_time:
				all_hour_slots.remove(slot)

		self.c.execute('''SELECT o.hour, SUM(q.amount)
					FROM orders o, quantity q 
					WHERE q.order_id=o.order_id AND o.hour>=?
					GROUP BY o.hour''',
				  (current_time,))

		available_hour_slots = []
		for stored_slot, stored_amount in self.c.fetchall():
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
			spinbox[1].delete("0", 'end')
			spinbox[1].insert('end', "0")
		self.order_id_entry.insert('end', "0")
		self.order_hour_combobox['values'] = []
		self.update_summary_list()

		self.order_id_entry.config(state='normal')
		self.order_id_entry.delete("0", 'end')
		self.order_id_entry.config(state='disabled')

		self.customer_phone_entry.delete("0", 'end')

		self.order_hour_combobox.config(state='normal')
		self.order_hour_combobox.delete("0", 'end')
		self.order_hour_combobox.config(state='readonly')

		self.filter_order_hour_combo.set('')
		self.filter_order_minute_combo.set('')
		self.set_filter_order_minute_combo()
		self.order_box.delete(0, 'end')
