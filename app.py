from flask import Flask, render_template, request, redirect

from mysql.connector import (connection)

app = Flask(__name__)

app.static_folder = 'static'

# This function is used to connect to the productinventory database
def connect_to_database():
		
	dbconn = connection.MySQLConnection(
		user='inventorymanageruser',
		password='abc123',
		host='localhost',
		database='productinventory'
		)
			
	return dbconn

# This is the function for the default home page 
# for the website were the index.html file will be rendered.
@app.route('/')
def home():
    return render_template('index.html')
	
# This is the function for the menu which is shared,
# by all pages in the application and is visible on,
# the column on the left hand side.
@app.route('/index/menu', methods=["POST", "GET"])
@app.route('/inventory/menu', methods=["POST", "GET"])
@app.route('/products/menu', methods=["POST", "GET"])
def menu():

	if request.form['submit_button'] == 'Home':
		return render_template('index.html')
	
	if request.form['submit_button'] == 'Inventory':
		return render_template('inventory.html')
	
	if request.form['submit_button'] == 'Products':
		return render_template('products.html')
		
# This is the function for the choose category button,
# on the inventory page.
@app.route('/inventory/choosecategory', methods=["POST", "GET"])
def choose_inventory_category():
		
	# Gets the selected category option which,
	# can be 'All', 'Condiments', 'Beverages' or,
	# 'Baked goods'.
	selected_category = request.form.get('category')
	
	if request.form['submit_button'] == 'Submit':
	
		# Establishes a connection to the database,
		# and creates buffered cursor which will fetch,
		# the entire result set and buffer the rows.
		conn = connect_to_database()
		cursor = conn.cursor(buffered=True)
	
		if selected_category == 'All':
		
			# Gets all the product names (with quantity),
			# from the inventory table irregardless of category.
			cursor.execute("SELECT product_name, quantity \
							FROM inventory \
							INNER JOIN products \
							ON inventory.product_id=products.product_id;")
			tuples = cursor.fetchall()
			
			# Creates an array of records where each,
			# record will include the name of the product and,
			# the quantity on the form "Productname, Quantity"
			records = []
			for tuple in tuples:
				product_name = tuple[0]
				quantity = tuple[1]
				records.append(product_name + ", " + str(quantity))
						
			cursor.close()
			conn.close()
			return render_template('inventory.html', rows=records, categoryoption=selected_category)
		else:
		
			# Gets all the product names (with quantity),
			# from the inventory with the selected category.
			cursor.execute("SELECT product_name, quantity \
							FROM \
							(SELECT products.product_name, products.product_id, inventory.quantity  \
							FROM inventory  \
							INNER JOIN products \
							ON inventory.product_id=products.product_id) AS allproductsininventory \
							INNER JOIN \
							(SELECT product_id \
							 FROM products \
							 INNER JOIN categories \
							 ON categories.category_id=products.category_id \
							 WHERE category_name='" + selected_category + "') AS allproductsincategory \
							 ON allproductsininventory.product_id=allproductsincategory.product_id;")				
			tuples = cursor.fetchall()
			
			# Creates an array of records where each,
			# record will include the name of the product and,
			# the quantity on the form "Productname, Quantity"
			records = []		
			for tuple in tuples:
				product_name = tuple[0]
				quantity = tuple[1]
				records.append(product_name + ", " + str(quantity))
				
			cursor.close()
			conn.close()
			return render_template('inventory.html', rows=records, categoryoption=selected_category)
		
		return render_template('inventory.html')

# This is the function for the choose category button,
# on the products page.
@app.route('/products/choosecategory', methods=["POST", "GET"])
def choose_product_category():
		
	# Gets the selected category option which,
	# can be 'All', 'Condiments', 'Beverages' or,
	# 'Baked goods'.
	selected_category = request.form.get('category')
	
	if request.form['submit_button'] == 'Submit':
		
		# Establishes a connection to the database,
		# and creates buffered cursor which will fetch,
		# the entire result set and buffer the rows.
		conn = connect_to_database()
		cursor = conn.cursor(buffered=True)
		
		if selected_category == 'All':
		
			# Gets all the product names from the products,
			# table irregardless of category.
			cursor.execute("SELECT product_name FROM products;")
			tuples = cursor.fetchall()
			
			# Creates an array of records where each,
			# record will include the name of the product.
			records = []
			for tuple in tuples:
				product_name = tuple[0]
				records.append(product_name)
							
			cursor.close()
			conn.close()
			return render_template('products.html', rows=records, categoryoption=selected_category)
		else:
		
			# Gets all the product names from the products,
			# table with the selected category.
			cursor.execute("SELECT product_name \
							FROM products \
							INNER JOIN categories \
							ON products.category_id=categories.category_id \
							WHERE category_name='" + selected_category + "';")
			tuples = cursor.fetchall()
			
			# Creates an array of records where each,
			# record will include the name of the product.
			records = []
			for tuple in tuples:
				product_name = tuple[0]
				records.append(product_name)
			
			cursor.close()
			conn.close()
			return render_template('products.html', rows=records, categoryoption=selected_category)
		
		return render_template('products.html')
		
# This is the function for adding a product to the inventory,
# which is done on the products page.
@app.route('/products/add', methods=["POST", "GET"])
def add_product():
		
	# Gets the name of the product the user has entered
	product_name = request.form['product_name']
	
	# Gets the quantity that the user has entered
	quantity_amount = request.form['quantity']
	
	if request.form['submit_button'] == 'Add':
		
		# Establishes a connection to the database,
		# and creates buffered cursor which will fetch,
		# the entire result set and buffer the rows.
		conn = connect_to_database()
		conn = connect_to_database()
		cursor = conn.cursor(buffered=True)

		# Gets the product id
		get_product_id_command = "SELECT product_id FROM products WHERE product_name='{0}';". format(product_name)
		cursor.execute(get_product_id_command)		
		product_id_tuple = cursor.fetchone()
		
		# If the product doesn't exist or wasn't entered by the user
		if product_id_tuple == None:
			cursor.close()
			conn.close()
			error_message = "Invalid product name"
			return render_template('products.html', error_addproduct=error_message)
		
		# If the quantity wasn't set
		if quantity_amount == '':
			cursor.close()
			conn.close()
			error_message = "Quantity must be set"
			return render_template('products.html', error_addquantity=error_message)
		
		# Gets the category id of the product
		get_category_id_command = "SELECT category_id \
							  FROM products \
							  WHERE product_name='{}';". format(product_name)
		cursor.execute(get_category_id_command)
		category_id_tuple = cursor.fetchone()
		category_id = int(''.join(map(str, category_id_tuple)))
		
		# Checks if the product already exists in the inventory
		product_id = int(''.join(map(str, product_id_tuple)))
		check_if_exists_command = "SELECT inventory.product_id \
								FROM products \
								INNER JOIN inventory \
								ON products.product_id=inventory.product_id \
								WHERE inventory.product_id={};".format(product_id)
		cursor.execute(check_if_exists_command)
		exists_tuple = cursor.fetchone()
			
		# If it doesn't exist, it needs to be inserted into the inventory
		# Else if it exists, it needs to be updated with the new added quantity
		if exists_tuple == None:

			# Inserts the values in to the inventory table		
			insert_command = "INSERT INTO inventory (product_id, category_id, quantity) \
							 VALUES({},{},{});". format(product_id, category_id, quantity_amount)
			cursor.execute(insert_command)
			conn.commit()
			cursor.close()
			conn.close()
			success_message = "Product was successfully added"
			return render_template('products.html', success_addproduct=success_message)
		else:
			
			# Gets the current quantity of the product
			get_current_quantity_command = "SELECT quantity FROM inventory WHERE product_id={};".format(product_id)
			cursor.execute(get_current_quantity_command)
			current_quantity_tuple = cursor.fetchone()
			current_quantity = int(''.join(map(str, current_quantity_tuple)))
			
			# Converts the added quantity to an int
			added_quantity = int(''.join(map(str, quantity_amount)))
			
			# Calculates the new quantity
			new_quantity = current_quantity + added_quantity
			
			# Updates the product with the new quantity
			update_command = "UPDATE inventory SET quantity = {} WHERE product_id = {};".format(new_quantity, product_id)
			cursor.execute(update_command)
			conn.commit()
			cursor.close()
			conn.close()
			success_message = "Product was successfully added"
			return render_template('products.html', success_addproduct=success_message)
		
		return render_template('products.html')

# This is the function for removing a product from the inventory
@app.route('/inventory/remove', methods=["POST", "GET"])
def remove_product():
		
	# Gets the name of the product the user has entered
	product_name = request.form['product_name']

	# Gets the quantity that the user has entered
	quantity_amount = request.form['quantity']
		
	if request.form['submit_button'] == 'Remove':
		
		# Establishes a connection to the database,
		# and creates buffered cursor which will fetch,
		# the entire result set and buffer the rows.
		conn = connect_to_database()
		cursor = conn.cursor(buffered=True)
		
		# Gets the product id
		get_product_id_command = "SELECT product_id FROM products WHERE product_name='{0}';". format(product_name)
		cursor.execute(get_product_id_command)		
		product_id_tuple = cursor.fetchone()
		
		# If the product name is invalid or wasn't entered by the user
		if product_id_tuple == None:
			cursor.close()
			conn.close()			
			error_message = "Invalid product name"
			return render_template('inventory.html', error_removeproduct=error_message)
		
		# If the quantity wasn't set
		if quantity_amount == '':
			cursor.close()
			conn.close()
			error_message = "Quantity must be set"
			return render_template('inventory.html', error_removequantity=error_message)
			
		# Checks if the product exists in the inventory
		product_id = int(''.join(map(str, product_id_tuple)))
		check_if_exists_command = "SELECT inventory.product_id \
								FROM products \
								INNER JOIN inventory \
								ON products.product_id=inventory.product_id \
								WHERE inventory.product_id={};".format(product_id)
		cursor.execute(check_if_exists_command)
		exists_tuple = cursor.fetchone()
		
		# If it doesn't exist it can't be removed
		if exists_tuple == None:
			cursor.close()
			conn.close()
			error_message = "Product doesn't exist in inventory"
			return render_template('inventory.html', error_removeproduct=error_message)
		
		# Gets the current quantity of the product
		get_current_quantity_command = "SELECT quantity FROM inventory WHERE product_id={};".format(product_id)
		cursor.execute(get_current_quantity_command)
		current_quantity_tuple = cursor.fetchone()
		current_quantity = int(''.join(map(str, current_quantity_tuple)))
		
		# Converts the removed quantity to an int
		removed_quantity = int(''.join(map(str, quantity_amount)))
		
		# Calculates the new quantity
		new_quantity = current_quantity - removed_quantity
				
		if new_quantity < 0:
			# If, the new quantity is negative, the user has removed to many products
			cursor.close()
			conn.close()
			error_message = "You removed to many items. Try removing a smaller amount."
			return render_template('inventory.html', error_removequantity=error_message)
		elif new_quantity == 0:
			# Else If, the new quantity is zero, the product will be removed from the inventory
			delete_command = "DELETE FROM inventory WHERE product_id={};".format(product_id)
			cursor.execute(delete_command)
			conn.commit()
			cursor.close()
			conn.close()
			success_message = "Product was successfully removed"
			return render_template('inventory.html', success_removeproduct=success_message)
		else:
			# Else, Updates the tuple with the new (decreased) quantity
			update_command = "UPDATE inventory SET quantity = {} WHERE product_id = {};".format(new_quantity, product_id)
			cursor.execute(update_command)
			conn.commit()
			cursor.close()
			conn.close()
			success_message = "Product was successfully removed"
			return render_template('inventory.html', success_removeproduct=success_message)
			
	return render_template('inventory.html')
	
# This is the function for removing a product from the inventory
@app.route('/inventory/clear', methods=["POST", "GET"])
def clear_inventory():
	
	if request.form['submit_button'] == 'Clear':
	
		# Connects to database and creates a cursor
		conn = connect_to_database()
		cursor = conn.cursor()
		
		# Deletes all products in inventory
		delete_all_products_in_inventory_command = "DELETE FROM inventory;"
		cursor.execute(delete_all_products_in_inventory_command)

		conn.commit()
		cursor.close()
		conn.close()
		
		success_message = "Inventory was successfully cleared."
		return render_template('inventory.html', success_clearinventory=success_message)
	
	return render_template('inventory.html')
		
		
		
		
		
		
		
		
		
		
		
		