import sqlite3

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()


class Menu:
	def __init__(self, id=None, name=None, tag=None, price=None):
		self.id = id
		self.name = name
		self.tag= tag
		self.price = price


# class Burger(Menu):
# 	pass
#
#
# class Extras(Menu):
# 	pass
#
#
# class Drinks(Menu):
# 	pass


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS products(ID REAL, name TEXT, tag TEXT, price REAL)')


def dynamic_data_entry(id, name, tag, price):
	create_table()
	c.execute("INSERT INTO products(ID,name,tag,price) VALUES (?,?,?,?)", (id, name, tag, price))
	conn.commit()

# burgers data build-up
# dynamic_data_entry(1,'Classic','CL',20.00)
# dynamic_data_entry(2,'Bacon','B',23.00)
# dynamic_data_entry(3,'Cheese','CH',22.00)
# dynamic_data_entry(4,'BBQ','BBQ',24.00)
# dynamic_data_entry(5,'HOT','HOT',24.00)
# dynamic_data_entry(6,'Cheese&Bacon','CHB',25.00)
# dynamic_data_entry(7,'Koza','K',25.00)
# dynamic_data_entry(8,'Boski Wloski','BW',27.00)
# dynamic_data_entry(9,'Gruba Bula','GB',29.00)


c.close()
conn.close()
