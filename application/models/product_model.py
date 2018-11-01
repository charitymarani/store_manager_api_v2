'''/models/product_model.py'''
import datetime
from .base_model import BaseModel


class Products(BaseModel):
    def put(self, product_code, name, category, purchase_price, selling_price, quantity, low_limit, description):
        '''Add a new product'''
        result = self.select_with_condition(
            'products', 'product_code', product_code)
        result2 = self.select_with_condition('products', 'name', name)
        if "message" not in result or "message" not in result2:
            return dict(
                message="The product already exists,you can update product quantity instead",status_code=409)
        date = datetime.datetime.now()
        query = """INSERT INTO products(product_code, name, category, purchase_price, selling_price, quantity, low_limit, description,date_created)
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s);"""

        self.cursor.execute(query, (product_code, name, category, purchase_price,
                                    selling_price, quantity, low_limit, description, date))

        self.conn.commit()

        return dict(message=name + ", Posted!", status_code=201)

    def get_all_products(self):
        '''get all products'''
        result = self.select_no_condition('products', 'product_code')
        return result

    def get_product_by_id(self, product_code):
        '''get single product'''
        result = self.select_with_condition(
            'products', 'product_code', product_code)
        return result

    def update_product(self, product_code, name, category, purchase_price, selling_price, quantity, low_limit, description):
        query = """UPDATE products 
                  SET name= %s, category= %s ,purchase_price= %s, selling_price= %s, quantity= %s, low_limit= %s, description= %s 
                  WHERE product_code= %s
                """
        self.cursor.execute(query, (name, category, purchase_price,
                                    selling_price, quantity, low_limit, description, product_code))
        self.conn.commit()

        return dict(message="Product updated successfully!", status_code=200)

    def delete_product(self, product_code):
        result = self.select_with_condition(
            'products', 'product_code', product_code)
        if "message" in result:
            return result
        self.cursor.execute(
            "DELETE FROM products WHERE product_code = %s", (product_code,))
        self.conn.commit()
        return dict(message="product has been deleted!", status_code=200)
