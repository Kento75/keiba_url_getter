import sqlite3
from contextlib import closing

dbname = './db/keiba_url.db'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    # executeメソッドでSQL文を実行する
    create_table = '''create table keiba_result_urls (page_id integer, race_id varchar(20),
                      target_url varchar(255), race_result_url varchar(255), race_date date)'''
    c.execute(create_table)

print('終了')
