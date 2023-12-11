sql_create_followers_data_table = '''\
CREATE TABLE IF NOT EXISTS followers_data(\
id SERIAL PRIMARY KEY, \
date DATE NOT NULL UNIQUE, \
followers  INTEGER, \
time_seconds INTEGER, \
table_name VARCHAR, \
UNIQUE(date)\
);'''

sql_update_followers_data_table = '''\
INSERT INTO followers_data (date, followers, time_seconds, table_name) \
VALUES%s \
ON CONFLICT (date) \
DO \
   UPDATE SET followers = %s, time_seconds = %s, table_name = %s;\
'''

sql_drop_followers_table = '''\
DROP TABLE IF EXISTS {table_name}\
;'''

sql_create_followers_table = '''\
CREATE TABLE IF NOT EXISTS {table_name}(\
steamid BIGINT NOT NULL
)'''