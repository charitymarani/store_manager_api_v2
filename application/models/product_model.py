'''/models/product_model.py'''
import datetime
from .base_model import BaseModel


class Products(BaseModel):
    def put(self, product_id, name, category, purchase_price, selling_price, quantity, low_limit, description):
        '''Add a new product'''
        result = self.select_with_condition(
            'products', 'product_id', product_id)
        result2 = self.select_with_condition('products', 'name', name)
        if "message" not in result or "message" not in result2:
            resp = dict(
                message="The product already exists,you can update product quantity instead")
            return dict(response=resp, status_code=409)
        date = datetime.datetime.now()
        query = """INSERT INTO products(product_id, name, category, purchase_price, selling_price, quantity, low_limit, description,date_created)

        self.cursor.execute(query, (product_id, name, category, purchase_price,
                                    selling_price, quantity, low_limit, description, date))

        self.conn.commit()

        return dict(response=dict(message=name + ", Posted!"), status_code=201)
    
    def get_all_products(self):
        '''get all products'''
        result = self.select_no_condition('products', 'product_id')
        return result

    def get_product_by_id(self, product_id):
        '''get single product'''
        result = self.select_with_condition(
            'products', 'product_id', product_id)
        return result

    def update_product(self, product_id, name, category, purchase_price, selling_price, quantity, low_limit, description):
        query = """UPDATE products 
                  SET name= %s, category= %s ,purchase_price= %s, selling_price= %s, quantity= %s, low_limit= %s, description= %s 
                  WHERE product_id= %s
                """
        self.cursor.execute(query, (name, category, purchase_price,
                                    selling_price, quantity, low_limit, description, product_id))
        self.conn.commit()

        return dict(response=dict(message="Product updated successfully!"), status_code=200)

    def delete_product(self, product_id):
        result = self.select_with_condition(
            'products', 'product_id', product_id)
        if "message" in result:
            return result
        self.cursor.execute(
            "DELETE FROM products WHERE product_id = %s", (product_id,))
        self.conn.commit()
        return dict(response=dict(message="product has been deleted!"), status_code=200)
