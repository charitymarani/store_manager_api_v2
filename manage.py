from os import getenv
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask
from werkzeug.security import generate_password_hash


class DbSetup():
    '''set up database actions'''

    def connection(self):
        ''' db connection method'''
        db_name = getenv('DB_NAME')
        db_user = getenv('DB_USER')
        db_password = getenv('DB_PASSWORD')
        db_host = getenv('DB_HOST')
        con = psycopg2.connect(
            dbname=db_name, host=db_host, port=5432, user=db_user,  password=db_password)
        return con

    def create_tables(self):
        conn = self.connection()
        curr = conn.cursor()
        queries = self.tables()
        for query in queries:
            curr.execute(query)
        print('created')
        conn.commit()
        curr.close()
        conn.close()
    def create_default_admin(self):
        conn=self.connection()
        curr=conn.cursor(cursor_factory=RealDictCursor)
        pwh=generate_password_hash("1234@admin")
        query="INSERT INTO users(name, username, email, password,role)\
                VALUES(%s,%s,%s,%s,%s)\
                ON CONFLICT (username)\
                DO NOTHING;"
                
        curr.execute(query,('Charity','defaultadmin','admin@gmail.com',pwh,'admin'))
        print("created default admin")
        conn.commit()
        curr.close()
        conn.close()
    

    def drop_tables(self):
        t1 = """DROP TABLE IF EXISTS products CASCADE"""
        t2 = """DROP TABLE IF EXISTS sales CASCADE"""
        t3 = """DROP TABLE IF EXISTS users CASCADE"""
        t4 = """DROP TABLE IF EXISTS blacklist CASCADE"""

        conn = self.connection()
        curr = conn.cursor()
        queries = [t1, t2, t3, t4]
        for query in queries:
            curr.execute(query)
        print("dropped")
        conn.commit()
        curr.close()
        conn.close()

    def cursor(self):
        '''method to allow objects execute SQL querries on the db instance'''
        cur = self.connection().cursor(cursor_factory=RealDictCursor)
        return cur

    def commit(self):
        '''commits changes to db'''
        conn = self.connection()
        conn.commit()

    def tables(self):

        q1 = """CREATE TABLE IF NOT EXISTS products (
            product_id integer PRIMARY KEY,
            name varchar(20) NOT NULL,
            purchase_price integer,
            category varchar(20),
            selling_price integer,
            low_limit integer NOT NULL,
            quantity integer NOT NULL,
            description varchar(20),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        q2 = """CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY NOT NULL,
            name varchar(20) NOT NULL,
            username varchar(20) UNIQUE NOT NULL,
            email varchar(100) NOT NULL,
            role varchar(20) NOT NULL,
            password varchar(300) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        q3 = """CREATE TABLE IF NOT EXISTS sales (
            sale_id serial PRIMARY KEY NOT NULL,
            items varchar(20) NOT NULL,
            items_count integer NOT NULL,
            price integer NOT NULL,
            created_by varchar(20) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        q4 = '''CREATE TABLE IF NOT EXISTS blacklist(
                    token_id SERIAL PRIMARY KEY NOT NULL,
                    json_token_identifier   VARCHAR(500) NOT NULL)'''
        queries = [q1, q2, q3, q4]
        return queries
