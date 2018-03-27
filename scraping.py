import time
import urllib.request
from bs4 import BeautifulSoup


start_url = 'https://keiba.yahoo.co.jp'

# todo SQLite3のテーブル情報から最大の日付を取得して
# 　　　現在日時までの日付とを利用してURLを生成する。

url_1 = 'http://keiba.yahoo.co.jp/search/race/?sy=1986&sm=1&ey=2018&em=2&gr=&b=&x=&z=&mnd=&mxd=&hid=&p='
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
