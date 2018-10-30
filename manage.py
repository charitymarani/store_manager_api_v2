import os
import psycopg2
import datetime
from psycopg2.extras import RealDictCursor
from flask import Flask
from werkzeug.security import generate_password_hash
from instance.config import app_config



# ENVIRONMENT = os.environ['ENV']
# url = app_config[ENVIRONMENT].CONNECTION_STRING


class DbSetup(object):
    '''class to setup db connection'''
    def __init__(self, config_name):
        #create connection to database
        self.connection_string = app_config[config_name].CONNECTION_STRING
        self.conn = psycopg2.connect(self.connection_string)
        

    def connection(self):
        
        return self.conn

    def create_tables(self):
        conn = self.connection()
        curr = self.cursor()
        queries = self.tables()
        for query in queries:
            curr.execute(query)
        conn.commit()
        print("created admin")
       
        
    def drop_tables(self):
        table1="""DROP TABLE IF EXISTS products CASCADE"""
        table2="""DROP TABLE IF EXISTS sales CASCADE"""
        table3="""DROP TABLE IF EXISTS users CASCADE"""
        table4="""DROP TABLE IF EXISTS blacklist CASCADE"""

        conn=self.connection()
        curr=self.cursor()
        queries=[table1,table2,table3,table4]
        for query in queries:
            curr.execute(query)
        conn.commit()
        print("Droped")
       
    def create_default_admin(self):
        conn =self.connection()
        curr = self.cursor()
        pwh = generate_password_hash('1234admin')
        a_query="SELECT * FROM users WHERE username=%s"
        curr.execute(a_query,('defaultadmin',))
        admin=curr.fetchone()
        if not admin:
            query = "INSERT INTO users(name, username, email, password,role)\
                VALUES(%s,%s,%s,%s,%s)"

            curr.execute(query, ('Charity', 'defaultadmin',
                                'admin@gmail.com', pwh, 'admin'))
            conn.commit()
     
    def cursor(self):
        '''method to allow objects execute SQL querries on the db instance'''
        cur = self.connection().cursor(cursor_factory=RealDictCursor)
        return cur

    def commit(self):
        '''commits changes to db'''
        conn = self.connection()
        conn.commit()

    def tables(self):
        
        query1 = """CREATE TABLE IF NOT EXISTS products (
            product_id integer PRIMARY KEY,
            name varchar(200) NOT NULL,
            purchase_price integer NOT NULL,
            category varchar(200) NOT NULL,
            selling_price integer NOT NULL,
            low_limit integer NOT NULL,
            quantity integer NOT NULL,
            description varchar(200),
            date_created TIMESTAMP )
            """
        query2 = """CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY NOT NULL,
            name varchar(200) NOT NULL,
            username varchar(200) NOT NULL,
            email varchar(100) NOT NULL,
            role varchar(200) NOT NULL,
            password varchar(300) NOT NULL,
            date_created TIMESTAMP )
            """
        query3 = """CREATE TABLE IF NOT EXISTS sales (
            sale_id serial PRIMARY KEY NOT NULL,
            item varchar(200) NOT NULL,
            items_count integer NOT NULL,
            price integer NOT NULL,
            created_by varchar(200) NOT NULL,
            date_created TIMESTAMP)
            """
        query4 = '''CREATE TABLE IF NOT EXISTS blacklist(
                    token_id SERIAL PRIMARY KEY NOT NULL,
                    json_token_identifier   VARCHAR(500) NOT NULL)'''
        queries = [query1, query2, query3, query4]
        return queries
