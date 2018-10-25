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