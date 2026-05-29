# A simple inventory management system that allows you to add products, calculate total inventory value, and save/load inventory data to/from a CSV file.
# The code defines a Product class to represent individual products and an Inventory class to manage the collection of products. 
# The Inventory class includes methods for adding products, calculating total value, and saving/loading data using the csv module.
# The code also demonstrates the use of static methods and class methods in Python, as well as the difference between them.

import csv

class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def total_value(self) -> float:
        return sum(product.price * product.quantity for product in self.products)
    
    def save_to_csv(self, filename: str):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Quantity'])
            for product in self.products:
                writer.writerow([product.name, product.price, product.quantity])
    
    def load_from_csv(self, filename: str):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            self.products = [Product(name, float(price), int(quantity)) for name, price, quantity in reader]

products = [
    Product("Laptop", 999.99, 10),
    Product("Smartphone", 499.99, 20),
    Product("Headphones", 199.99, 15)
]
inventory = Inventory()
for product in products:
    inventory.add_product(product)
print(f"Total inventory value: ${inventory.total_value():.2f}")
inventory.save_to_csv('inventory.csv')
print("Inventory saved to 'inventory.csv'.")
inventory.load_from_csv('inventory.csv')
print("Inventory loaded from 'inventory.csv':")
for product in inventory.products:
    print(f"{product.name}: ${product.price:.2f} x {product.quantity}")

# The @staticmethod decorator is used to define a method that belongs to the class rather than an instance of the class.
# A static method does not have access to the instance (self) or class (cls) variables and is typically used for utility functions that perform a task in isolation.
# In the above code, we have not used @staticmethod, but if we were to define a method that does not require access to instance or class variables, we could use @staticmethod to indicate that it is a static method.
# No, we could not use @staticmethod on load_from_csv because it needs to modify the instance variable 'products' of the Inventory class, which is not possible with a static method.
# Yes, we could use @classmethod on load_from_csv if we want to create a new instance of Inventory and populate it with products from the CSV file, but in this case, it would be more appropriate to use an instance method since we are modifying the existing instance of Inventory.

class Inventory:
    products = []

    @staticmethod
    def total_value(products) -> float:
        return sum(product.price * product.quantity for product in products)
    
    def add_product(self, product: Product):
        self.products.append(product)
    
    def save_to_csv(self, filename: str):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Quantity'])
            for product in self.products:
                writer.writerow([product.name, product.price, product.quantity])

    @classmethod
    def load_from_csv(cls, filename: str):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            cls.products = [Product(name, float(price), int(quantity)) for name, price, quantity in reader]
            return cls()

products = [
    Product("Laptop", 999.99, 10),
    Product("Smartphone", 499.99, 20),
    Product("Headphones", 199.99, 15)
]
inventory = Inventory()
for product in products:
    inventory.add_product(product)
print(f"Total inventory value: ${Inventory.total_value(inventory.products):.2f}")
inventory.save_to_csv('inventory.csv')
print("Inventory saved to 'inventory.csv'.")
loaded_inventory = Inventory.load_from_csv('inventory.csv')
print("Inventory loaded from 'inventory.csv':")
for product in loaded_inventory.products:
    print(f"{product.name}: ${product.price:.2f} x {product.quantity}") 
print(f"Total inventory value of loaded inventory: ${Inventory.total_value(loaded_inventory.products):.2f}")