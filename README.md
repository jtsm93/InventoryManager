# InventoryManager
InventoryManager is a web application written in Python, Flask, HTML, CSS and MySQL where the user can add and remove products to an inventory that is meant to represent the products that the user currently has at home.

# Installing and Running the program
This program requires flask, python3 and the corresponding mysql connector for python3.

To run the program in a linux environment go to the inventorymanager folder and enter the following commands:

	- export FLASK_APP=app.py
	- export FLASK_ENV=app.py
	- flask run

This should produce a webaddress "Running on ...." in the command line. Copy the address and open it in your internet browser.

# How to Use the program

 # 1. View inventory/products
 - To view which products are currently in the inventory go
    to the inventory page and under "Inventory" choose which category you
    want to view and the click "submit"
    
 - To view which products are available to add to the inventory go
   to the products page and under "Products" choose categoty and click "submit"

  # 2. Adding a product to the inventory
 - Go to "Add product to inventory" on the products page
 - Enter the name of the product you want to add
 - Enter how many items of the product you want to add

  # 3. Removing a product from the inventory
 - Go to "Remove a product from the inventory" on the inventory page
 - Enter the name of the product you want to remove
 - Enter how many items you want to remove

  # 4. Remove all products from the inventory
 - Go to "Clear inventory" on the inventory page and click "Clear"
