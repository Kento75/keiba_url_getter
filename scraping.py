import datetime
import time
import urllib.request
from bs4 import BeautifulSoup
import sqlite3
from contextlib import closing


start_url = 'https://keiba.yahoo.co.jp'

# sqlite3からページ、開催日が最も大きい値を取得
dbname = './db/keiba_url.db'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    # executeメソッドでSQL文を実行する
    sql_str = '''create table keiba_result_urls (page_id integer, race_id varchar(20),
                      target_url varchar(255), race_result_url varchar(255), race_date date)'''
    latest_data = c.execute(sql_str)

latest_page_id = latest_data[0]
latest_race_id = latest_data[1]
latest_race_date = latest_data[2]
latest_result_url = latest_data[3]

latest_year = str(latest_race_date.year)
latest_month = str(latest_race_date.month)
latest_date = str(latest_race_date)
now_date = datetime.datetime.today()
now_year = datetime.date.today().year
now_month = datetime.date.today().month

# 検索用URLの生成
url_1 = 'http://keiba.yahoo.co.jp/search/race/?sy=' + latest_year + '&sm=' + latest_month\
        + '&ey=' + now_year + '&em=' + now_month + '&gr=&b=&x=&z=&mnd=&mxd=&hid=&p='
url_2 = '&sidx=race_date&dir=1'

# ↓レース結果ページが増えるとラストページが増えるので手動で変更する必要あり
last_page = 2

# CSVを生成（上書き処理）
with open('./csv/url_list.csv', 'w', newline='') as f:
    for p in range(1, last_page):
        horse_url_list = []
        time.sleep(5)  # スクレイピング間隔の設定なので、5秒はあまり短くしないこと
        target_url = url_1 + str(p) + url_2
        try:
            html_fp = urllib.request.urlopen(target_url)
            html = html_fp.read()
            soup = BeautifulSoup(html, "html.parser")

            # tag_select
            table = soup.find("table", {"class": "dataLs mgnBS"})
            trs = table.find_all("tr")[1: -1]
            for tr in trs:
                horse_url = start_url + tr.find("a")["href"]
                print(horse_url)
                f.write(horse_url + "\n")
        except urllib.error.URLError as e:
            # 404エラーの場合は処理終了
            print('URLエラー発生:[' + target_url + ']のリクエストで発生')
            print('処理を終了します。')
            break
        except urllib.error.HTTPError as e:
            # HTTPエラー発生時は続行
            print('HTTPエラー発生:[' + target_url + ']のリクエストで発生')
            continue

print("**********************************")
print("*********   処理終了   ***********")
print("**********************************")
