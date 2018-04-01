import csv
import sqlite3
from contextlib import closing

dbname = './db/keiba_url.db'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    with open('./csv/url_list.csv', 'r') as f:
        b = csv.reader(f)
        for t in b:
            print(t)
            # tableに各行のデータを挿入する。
            c.execute('INSERT INTO keiba_result_urls VALUES (?,?,?,?,?);', t)

    conn.commit()


print("**********************************")
print("*********   処理終了   ***********")
print("**********************************")