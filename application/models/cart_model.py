'''/models/product_model.py'''
import datetime
from .base_model import BaseModel


class Carts(BaseModel):
    '''class containg cart related actions '''

    def put(self, created_by, cart_item, count):
        '''Add product to cart'''
        date_created = datetime.datetime.now()
        item = self.select_with_condition('carts', 'cart_item', cart_item)
        if "message" in item:
            product = self.select_with_condition('products', 'name', cart_item)
            if "message" in product:
                return {"message": "The item you want to add to cart does not exist"}
            query = """INSERT INTO
                    carts  (created_by,cart_item,count,price,date_created)
                    VALUES(%s,%s,%s,%s,%s)"""
            product=self.select_with_condition('products','name',cart_item)
            price=product["selling_price"]
            total_price = count*price
            self.cursor.execute(
                query, (created_by, cart_item, count, total_price, date_created))
            self.conn.commit()
            quantity = product["quantity"]
            new_quantity = quantity-count
            query2 = """UPDATE products SET quantity=%s WHERE name=%s"""
            self.cursor.execute(query2, (new_quantity, cart_item))
            self.conn.commit()
            return {"message": "{} added to cart".format(cart_item)}
        product=self.select_with_condition('products','name',cart_item)
        price=product["selling_price"]
        item_count = item["count"]
        new_count = item_count + count
        new_price = new_count*price
        product = self.select_with_condition('products', 'name', cart_item)
        qty = product["quantity"]
        new_qty = qty-count
        query = """UPDATE carts SET count=%s,price=%s WHERE cart_item=%s"""
        self.cursor.execute(query, (new_count, new_price, cart_item))
        self.conn.commit()
        query3 = """UPDATE products SET quantity=%s WHERE name=%s"""
        self.cursor.execute(query3, (new_qty, cart_item))
        self.conn.commit()
        return {"message": "{} updated in cart".format(cart_item)}

    def get_all_cart_items(self, created_by):
        '''get entire cart'''
        result = self.select_all_with_condition(
            'carts', 'created_by', created_by)
        if "message" in result:
            return {"message": "The cart is currently empty"}
        return result

    def get_cart_item_by_id(self, cart_item_id):
        '''get single cart item'''
        result = self.select_with_condition(
            'carts', 'cart_item_id', cart_item_id)
        return result

    def update_cart_item(self, cart_item_id, count):
        item = self.get_cart_item_by_id(cart_item_id)
        item_name = item["cart_item"]
        price = self.select_with_condition(
            'products', 'name', item_name)["selling_price"]
        new_price = count*price
        query = """UPDATE carts
                  SET count=%s,price=%s
                  WHERE cart_item_id= %s
                """
        self.cursor.execute(query, (count, new_price, cart_item_id))
        self.conn.commit()

        return dict(message="Cart item updated successfully!", status_code=200)

    def delete_cart_item(self, cart_item_id):
        result = self.get_cart_item_by_id(cart_item_id)
        if "message" in result:
            return result
        cart_item = result["cart_item"]
        cart_qty = result["count"]
        product = self.select_with_condition('products', 'name', cart_item)
        qty = product["quantity"]
        new_qty = qty+cart_qty
        query = "UPDATE products SET quantity= %s WHERE name =%s;"
        self.cursor.execute(query, (new_qty, cart_item))
        self.conn.commit()
        self.cursor.execute(
            "DELETE FROM carts WHERE cart_item_id = %s;", (cart_item_id,))
        self.conn.commit()
        return dict(message="Cart item has been deleted!", status_code=200)

    def delete_cart(self, created_by):
        cart = self.get_all_cart_items(created_by)
        for i in range(len(cart)):
            item_id = cart[i]["cart_item_id"]
            self.delete_cart_item(item_id)
        self.conn.commit()
        self.cursor.execute("ALTER SEQUENCE carts_cart_item_id_seq RESTART WITH 1")
        self.conn.commit()
        return dict(message="Cart has been deleted!", status_code=200)
