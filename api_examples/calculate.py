#Python 3.12.1 (tags/v3.12.1:2305ca5, Dec  7 2023, 22:03:25) [MSC v.1937 64 bit (AMD64)] on win32

import requests
import urllib.parse

# abstract
# 数値計算・関数の微分・xの関数に数値代入を行う。
# 使う機能によってurlが異なるので注意。


# 数値計算
url = "http://www.rurihabachi.com/web/webapi/calculator/json"
params = {'exp': '20 + 2'}

# 微分の場合
#url = "http://www.rurihabachi.com/web/webapi/differentiation/json"
#params = {'function': 'x^2+x+2', 'variable': 'x'} #variable未指定の場合、xで偏微分

#　関数への代入
# url = "http://www.rurihabachi.com/web/webapi/functionx/json"
# params = {'fx': 'x^2+(a+b)x+ab', 'xfrom': '2', 'xto': '2', 'a': '1', 'b': '3'} #xfrom, xto 両方の入力が必要


# リクエストヘッダー（必要に応じて）
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# リクエストの実行
response = requests.post(url, data=params, headers=None)

# 結果の取得と表示
if response.status_code == 200:
    result = response.json()
    print("Result:", result)
else:
    print("Error:", response.status_code)

    
