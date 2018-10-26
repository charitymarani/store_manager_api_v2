'''/models/sales_model.py'''
from .base_model import BaseModel
class Sales(BaseModel):
    def put(self,created_by,items,items_count,price):
        '''Add a new sales record'''
        query = """INSERT INTO sales(created_by, items, items_count, price)
                VALUES(%s, %s, %s, %s)RETURNING sale_id;"""
        self.cursor.execute(query, (created_by,items,items_count,price))
        self.conn.commit()
        return dict(response=dict(message="A sale has been created successfully"), status_code=201)
    def get_all_sales(self):
        '''get all sales'''
        result=self.select_no_condition('sales','sale_id')
        return result
    def get_sale_by_id(self,sale_id):
        '''get single sales record'''
        result=self.select_with_condition('sales','sale_id',sale_id)
        return result
    def get_who_created_sale(self,sale_id):
        '''get attendant who created a sales record'''
        result =self.select_with_condition('sales','sale_id',sale_id)
        creator=result["created_by"]
        return creator