import psycopg2
from datetime import date
#import dashboard.config as config
from app.core.config import settings
import app.database.queries as queries

class PtoolsDB(object):
    def __init__(self):
        database = 'p_tools'
        self.conn = self.connect_to_db(database)
        self.cursor = self.conn.cursor()
    
    def connect_to_db(self, database):
        try:
            conn = psycopg2.connect(user=settings.POSTGRES_USERNAME, password=settings.POSTGRES_PASSWORD, 
                                    host='127.0.0.1', port='5432', database=database)
            return conn
        except:
            return

    def insert_followers_table(self, followers_table, followers_list):
        try:
            self.cursor.execute(queries.sql_drop_followers_table.format(table_name=followers_table))
            self.cursor.execute(queries.sql_create_followers_table.format(table_name=followers_table))
            self.cursor.executemany(
                '''INSERT INTO %s (steamid) VALUES (%%s)''' % (followers_table), [[id] for id in followers_list])
            self.conn.commit()
        except:
            self.conn.rollback()
        
    def select_followers_table(self, table_name):
        try:
            self.cursor.execute(f'SELECT * FROM {table_name};')
            followers_steamids = self.cursor.fetchall()
            return followers_steamids
        except:
            self.conn.rollback()
    
    def select_followers_data_table(self):
        try:
            self.cursor.execute('SELECT * FROM followers_data ORDER BY date DESC;')
            followers_data = self.cursor.fetchall()
            return followers_data
        except:
            self.conn.rollback()

    def update_followers_data_table(self, time_seconds, len_followers_list, followers_table_name):
        try:
            followers_data_table = [date.today().strftime('%Y-%m-%d'), len_followers_list, time_seconds, followers_table_name]
            self.cursor.execute(queries.sql_update_followers_data_table, (tuple(followers_data_table), *followers_data_table[1:]))
            self.conn.commit()
        except:
            self.conn.rollabck()

    def close_connection(self):
        self.conn.close()

'''
time_seconds = 410
conn.close()
cursor.rowcount
cursor.statusmessage
conn.closed
'''