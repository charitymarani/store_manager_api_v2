'''/models/product_model.py'''
from .base_model import BaseModel


class Products(BaseModel):
    def put(self, product_id, name, category, purchase_price, selling_price, quantity, low_limit, description):
        '''Add a new product'''
        # self.cursor.execute("SELECT * FROM products WHERE product_id = (%s);", (product_id, ))
        result = self.select_with_condition(
            'products', 'product_id', product_id)
        if "message" not in result:
            resp = dict(
                message="The product Id you entered is being used for another product")
            return dict(response=resp, status_code=409)
        query = """INSERT INTO products(product_id, name, category, purchase_price, selling_price, quantity, low_limit, description)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)RETURNING product_id;"""
        self.cursor.execute(query, (product_id, name, category, purchase_price,
                                    selling_price, quantity, low_limit, description))

        self.conn.commit()

        return dict(response=dict(message=name + ", Posted!"), status_code=201)
    def get_all_products(self):
        '''get all products'''
        result=self.select_no_condition('products','product_id')
        
        return result
