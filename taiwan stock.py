import os
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plotly.graph_objs import Scatter, Layout
from plotly.offline import plot


# 更改日期格式(民國 -> 西元)
def covert_date(date):
    date_str = str(date)
    year_str = date_str[:3]
    real_year = str(int(year_str) + 1911)
    real_date = real_year + date_str[4:6] + date_str[7:9]
    return real_date


# 更改月份格式(二位數)
def twodigit(x):
    if x < 10:
        month_str = "0" + str(x)
    else:
        month_str = str(x)

    return month_str


url_base = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20"
url_tail = "01&stockNo=00878&response=json&_=1685778130643"

driver = webdriver.Chrome()

file_name = "taiwan stock.csv"

if not os.path.isfile(file_name):
    
    # 開啟 csv 檔
    with open(file_name, "a", encoding="utf-8", newline="") as f:
        
        # 從 2022 年開始
        n = 22
        while True:
            try:
                for i in range(1, 13):
                    link = url_base + str(n) + twodigit(i) + url_tail
                    driver.get(link)

                    data = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/pre")))
                    
                    # 取得文字
                    data_text = data.text
                    
                    # 文字為 json 格式
                    data_json = json.loads(data_text)
                    
                    # 建立 csv 檔寫入器
                    f_write = csv.writer(f)

                    if i == 1 and n == 22:
                        
                        # 第一列寫入項目名稱
                        f_write.writerow(data_json["fields"])
                        
                        # 圖片標題
                        title = data_json["title"]

                    for data in data_json["data"]:
                        
                        # 寫入項目內容
                        f_write.writerow(data)
            
            except:
                break

            n += 1

# 使用 pandas 讀取 csv 檔
pd_stock = pd.read_csv(file_name, encoding="utf-8")

# 關閉 copywarning
pd.options.mode.chained_assignment = None

for i in range(len(pd_stock["日期"])):
    pd_stock["日期"][i] = covert_date(pd_stock["日期"][i])

# 日期轉換成 datetime 類型
pd_stock["日期"] = pd.to_datetime(pd_stock["日期"])

# 載入字體
plt.rcParams["font.sans-serif"] = "mingliu"
plt.rcParams["axes.unicode_minus"] = False

data = [Scatter(x=pd_stock["日期"], y=pd_stock["開盤價"], name="開盤價"),
        Scatter(x=pd_stock["日期"], y=pd_stock["收盤價"], name="收盤價"),
        Scatter(x=pd_stock["日期"], y=pd_stock["最低價"], name="最低價"),
        Scatter(x=pd_stock["日期"], y=pd_stock["最高價"], name="最高價")]

pd_stock.plot(kind="line",
              figsize=(12, 6),
              x="日期",
              y=["開盤價", "收盤價", "最低價", "最高價"])

driver.quit()

plot({"data": data,
      "layout": Layout(title=title[8:])}, auto_open=True)

plt.show()
