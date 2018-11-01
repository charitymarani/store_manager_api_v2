'''/models/sales_model.py'''
import datetime
from .base_model import BaseModel


class Sales(BaseModel):
    def put(self, created_by):
        '''Add a new sales record'''
        cart = self.select_all_with_condition(
            'carts', 'created_by', created_by)
        if "message" in cart:
            return {"message": "The cart is currently empty,add items to cart to make a sale"}
        for i in range(len(cart)):
            created_by = cart[i]['created_by']
            price = cart[i]['price']
            cart_item = cart[i]['cart_item']
            count = cart[i]['count']
            date_created = datetime.datetime.now()

            query = """INSERT INTO sales(created_by, item, items_count, price,date_created)
                    VALUES(%s, %s, %s, %s,%s)RETURNING sale_id;"""
            self.cursor.execute(
                query, (created_by, cart_item, count, price, date_created))
            self.conn.commit()
        self.cursor.execute(
            "DELETE FROM carts WHERE created_by=%s;", (created_by,))
        self.conn.commit()
        return dict(message="A sale has been created successfully", status_code=201)

    def get_all_sales(self):
        '''get all sales'''
        result = self.select_no_condition('sales', 'sale_id')
        return result

    def get_sale_by_id(self, sale_id):
        '''get single sales record'''
        result = self.select_with_condition('sales', 'sale_id', sale_id)
        return result

    def get_who_created_sale(self, sale_id):
        '''get attendant who created a sales record'''
        result = self.select_with_condition('sales', 'sale_id', sale_id)
        creator = result["created_by"]
        return creator
