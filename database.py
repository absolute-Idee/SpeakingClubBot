from itertools import chain
from operator import sub
import psycopg2
from setuptools import Command

class MyDatabase():
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='bot_db' password='postgres'")
            self.conn.autocommit = True
            print('Connection successsful')
            self.cursor = self.conn.cursor()
            create_table_query = '''CREATE TABLE IF NOT EXISTS users
                                    (
                                    CHAT_ID         INT     PRIMARY KEY     NOT NULL    UNIQUE,
                                    SUBSCRIPTION    bool,
                                    LANGUAGE        VARCHAR(50)); '''
            self.cursor.execute(create_table_query)
            #self.conn.commit()
            print('Table created')
        except:
            print("Unable to connect to the database")
        
    def get_subscriptions(self):
    # get all active subscribers
        with self.conn:
            self.cursor.execute(""" SELECT * FROM users WHERE SUBSCRIPTION = true """)
            result = self.cursor.fetchall()
            return result

    def add_subscriber(self, chat_id, language, subscription = True):
        with self.conn:
            command = """ INSERT INTO users (CHAT_ID, SUBSCRIPTION, LANGUAGE) VALUES (%s,%s,%s) """
            values = (chat_id, subscription, language)
            return self.cursor.execute(command, values)

    def update_subscription(self, chat_id, subscription):
        with self.conn:
            command = """ UPDATE users SET SUBSCRIPTION = %s WHERE CHAT_ID = %s """
            return self.cursor.execute(command,(subscription, chat_id))

    def check_subscriber(self, chat_id):
        with self.conn:
            command = """ SELECT SUBSCRIPTION FROM users WHERE CHAT_ID = %s """
            self.cursor.execute(command,(chat_id,))
            result = bool(self.cursor.fetchone())
            return result

    def check_user(self, chat_id):
        with self.conn:
            command = """ SELECT COUNT(chat_id) FROM users WHERE CHAT_ID = %s """
            self.cursor.execute(command,(chat_id,))
            result = self.cursor.fetchone()
            return result

    def get_language(self, chat_id):
        with self.conn:
            command = """ SELECT LANGUAGE FROM users WHERE CHAT_ID = %s """
            self.cursor.execute(command, (chat_id,))
            result = self.cursor.fetchone()
            return result
        
    def update_language(self, chat_id, language):
        with self.conn:
            command = """ UPDATE users SET LANGUAGE = %s WHERE CHAT_ID = %s """
            return self.cursor.execute(command, (language, chat_id))
            


    def close(self):
        self.cursor.close()
        self.conn.close()