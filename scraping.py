import time
import datetime
import re
import csv
import sqlite3
from contextlib import closing
import urllib.request
from bs4 import BeautifulSoup


start_url = 'https://keiba.yahoo.co.jp'

# sqlite3からページ、開催日が最も大きい値を取得
dbname = './db/keiba_url.db'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    # executeメソッドでSQL文を実行する
    sql_str = '''select max(ROWID), page_id, race_date from keiba_result_urls'''
    latest_data = c.execute(sql_str).fetchall()


latest_page_id = latest_data[0][1]
str_latest_race_date = latest_data[0][2]
latest_race_date = datetime.datetime.strptime(str_latest_race_date, '%Y/%m/%d').date()
latest_year = str(latest_race_date.year)
latest_month = str(latest_race_date.month)
now_date = datetime.datetime.today().date()
now_year = datetime.date.today().year
now_month = datetime.date.today().month

# 検索用URLの生成
url_1 = 'http://keiba.yahoo.co.jp/search/race/?sy=' + latest_year + '&sm=' + latest_month\
        + '&ey=' + now_year + '&em=' + now_month + '&gr=&b=&x=&z=&mnd=&mxd=&hid=&p='
url_2 = '&sidx=race_date&dir=1'

# ↓レース結果ページが増えるとラストページが増えるので手動で変更する必要あり
last_page = 10000

# CSVを生成（上書き処理）
with open('./csv/url_list.csv', 'w', newline='') as f:
    for p in range(1, last_page):
        horse_url_list = []
        time.sleep(5)  # スクレイピング間隔の設定なので、5秒はあまり短くしないこと
        target_url = url_1 + str(p) + url_2
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
            html_fp = urllib.request.urlopen(req)
            html = html_fp.read()
            soup = BeautifulSoup(html, "html.parser")

            # tag_select
            table = soup.find("table", {"class": "dataLs mgnBS"})
            trs = table.findAll("tr")[1: -1]
            for tr in trs:
                race_date = tr.find(text=re.compile('[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}'))
                print(datetime.datetime.strptime(race_date, '%Y/%m/%d').date())
                if latest_race_date >= now_date:
                    break

                race_result_url = start_url + tr.find("a")["href"]
                race_id = re.sub(r'[^0-9]', '', race_result_url)
                print(race_result_url)
                str_list = []
                str_list.append(str(p))
                str_list.append(race_id)
                str_list.append(target_url)
                str_list.append(race_result_url)
                str_list.append(race_date)
                row = ','.join(str_list)
                f.write(row + '\n')
            else:
                continue
            break
        except urllib.error.URLError as e:
            # 404エラーの場合は処理終了
            print('URLエラー発生:[' + target_url + ']のリクエストで発生')
            print('処理を終了します。')
            break
        except urllib.error.HTTPError as e:
            # HTTPエラー発生時は続行
            print('HTTPエラー発生:[' + target_url + ']のリクエストで発生')
            continue


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
