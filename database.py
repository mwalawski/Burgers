from os import path
import sqlite3


class Database:
	def __init__(self):
		if not path.exists('orders.db'):
			self.connect_db()
			self.menu_entry(1, 'Classic', 'CL', 20.00)
			self.menu_entry(2, 'Bacon', 'B', 23.00)
			self.menu_entry(3, 'Cheese', 'CH', 22.00)
			self.menu_entry(4, 'BBQ', 'BBQ', 24.00)
			self.menu_entry(5, 'Hot', 'HOT', 24.00)
			self.menu_entry(6, 'Smokey', 'S', 25.00)
			self.menu_entry(7, 'Goaty', 'G', 25.00)
			self.menu_entry(8, 'Italian', 'IT', 27.00)
			self.menu_entry(9, 'DoubleM', 'DM', 29.00)
		else:
			self.connect_db()

		self.conn.commit()

	def connect_db(self):
		self.conn = sqlite3.connect('orders.db')
		self.c = self.conn.cursor()
		self.create_table()

	def create_table(self):
		self.c.execute("PRAGMA foreign_keys=ON")

		self.c.execute('''CREATE TABLE IF NOT EXISTS orders(
		order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
		hour TEXT NOT NULL, 
		phone TEXT)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS products(
		product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
		name TEXT NOT NULL, 
		tag TEXT,
		price REAL NOT NULL)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS quantity(
		quantity_id INTEGER PRIMARY KEY AUTOINCREMENT, 
		product_id INTEGER NOT NULL, 
		amount INTEGER NOT NULL,
		order_id INTEGER NOT NULL REFERENCES orders (order_id) ON DELETE CASCADE,
		FOREIGN KEY (product_id) REFERENCES products (product_id))''')
		self.conn.commit()

	def menu_entry(self, id, name, tag, price):
		self.c.execute("INSERT INTO products(product_id,name,tag,price) VALUES (?,?,?,?)", (id, name, tag, price))
		self.conn.commit()
