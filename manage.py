import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask
from werkzeug.security import generate_password_hash
from instance.config import app_config

ENVIRONMENT = os.environ['ENV']
url = app_config[ENVIRONMENT].CONNECTION_STRING


class DbSetup(object):
    '''class to setup db connection'''

    def connection(self, url):
        conn = psycopg2.connect(url)
        return conn

    def create_tables(self):
        conn = self.connection(url)
        curr = conn.cursor()
        queries = self.tables()
        for query in queries:
            curr.execute(query)
        conn.commit()
        curr.close()
        conn.close()
        

    def create_default_admin(self):
        conn =self.connection(url)
        curr = conn.cursor(cursor_factory=RealDictCursor)
        pwh = generate_password_hash('1234admin')
        query = "INSERT INTO users(name, username, email, password,role)\
                VALUES(%s,%s,%s,%s,%s);"

        curr.execute(query, ('Charity', 'defaultadmin',
                             'admin@gmail.com', pwh, 'admin'))
        conn.commit()
        curr.close()
        conn.close()

    def cursor(self):
        '''method to allow objects execute SQL querries on the db instance'''
        cur = self.connection(url).cursor(cursor_factory=RealDictCursor)
        return cur

    def commit(self):
        '''commits changes to db'''
        conn = self.connection(url)
        conn.commit()

    def tables(self):

        query1 = """CREATE TABLE IF NOT EXISTS products (
            product_id integer PRIMARY KEY,
            name varchar(200) NOT NULL,
            purchase_price integer,
            category varchar(200),
            selling_price integer,
            low_limit integer NOT NULL,
            quantity integer NOT NULL,
            description varchar(200),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        query2 = """CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY NOT NULL,
            name varchar(200) NOT NULL,
            username varchar(200) NOT NULL,
            email varchar(100) NOT NULL,
            role varchar(200) NOT NULL,
            password varchar(300) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        query3 = """CREATE TABLE IF NOT EXISTS sales (
            sale_id serial PRIMARY KEY NOT NULL,
            items varchar(200) NOT NULL,
            items_count integer NOT NULL,
            price integer NOT NULL,
            created_by varchar(200) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        query4 = '''CREATE TABLE IF NOT EXISTS blacklist(
                    token_id SERIAL PRIMARY KEY NOT NULL,
                    json_token_identifier   VARCHAR(500) NOT NULL)'''
        queries = [query1, query2, query3, query4]
        return queries
