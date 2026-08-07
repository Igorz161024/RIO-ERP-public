from backend.modules.db import insert_product, update_product, delete_product

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        insert_product(name, price, quantity)

    def __str__(self):
        return f"Product(name={self.name}, price={self.price}, quantity={self.quantity})"

    def update(self, product_id, name=None, price=None, quantity=None):
        update_product(product_id, name, price, quantity)

    def delete(self, product_id):
        delete_product(product_id)
