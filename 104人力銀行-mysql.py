# --------------------------------------------------
# 104人力銀行, 搜尋: python, 地區: 六都, 經歷要求: 1年以下, 更新日期: 二週內
# 爬取: 職務名稱, 公司名稱, 公司類別, 工作地點, 學歷要求, 薪資
# 存進 mysql, 資料庫: pythondb, 資料表: 104人力銀行
# ------------------------------------------------------------

import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------------------------------------
# 連線資料庫: pythondb

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='0000',
                       db='pythondb')

# --------------------------------------------------
# 建立資料表: 104人力銀行

cursor = conn.cursor()

sql = '''create table if not exists 104人力銀行(
職務名稱 varchar(200),
公司名稱 varchar(100),
公司類別 varchar(100),
工作地點 varchar(10),
學歷要求 varchar(10),
薪資 varchar(100)
);
'''

cursor.execute(sql)
conn.commit()

# --------------------------------------------------
# 104人力銀行, 搜尋: python, , 地區: 六都, 經歷要求: 1年以下, 更新日期: 二週內

url = '''https://www.104.com.tw/jobs/search/?ro=0&isnew=7&keyword=python
&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001016000%2C600
1001000%2C6001002000%2C6001005000%2C6001008000%2C6001014000&order=14&asc
=0&page=1&jobexp=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0
&recommendJob=1&hotJob=1
'''

driver = webdriver.Chrome()
driver.get(url)

print('loading...')

page_select = WebDriverWait(driver, 10)\
    .until(EC.presence_of_element_located((By.CLASS_NAME, 'page-select')))\
    .text.split('\n')  # 總頁數

for _ in range(min(60, len(page_select))):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

    try:  # 第 16 頁開始需手動載入
        more_page = driver.find_elements(By.CLASS_NAME, 'js-more-page')
        more_page[-1].click()  # 手動載入
    except:
        continue

job_item = driver.find_elements(By.CLASS_NAME, 'js-job-item')

i = 0

for item in job_item:
    if item.get_attribute('data-jobsource') != 'hotjob_chr':  # 判斷是否為廣告
        item_title = item.get_attribute('data-job-name')  # 職務名稱
        item_company = item.get_attribute('data-cust-name')  # 公司名稱
        item_sort = item.get_attribute('data-indcat-desc')  # 公司類別
        item_intro = item.find_element(By.CLASS_NAME, 'job-list-intro')\
            .text.split()  # [地點, 經歷, 學歷]
        item_tag = item.find_element(By.CLASS_NAME, 'b-tag--default')\
            .text  # 薪資

        sql = f'''insert into 
        104人力銀行 (職務名稱, 公司名稱, 公司類別, 工作地點, 學歷要求, 薪資) values
        (%s, %s, %s, %s, %s, %s)
        '''

        cursor.execute(sql, (item_title, item_company, item_sort,
                             item_intro[0], item_intro[2], item_tag))
        conn.commit()
        i += 1

        if i % 20 == 0:
            print(f'處理第 {str(i // 20)} 頁完畢! (共 {str(i)} 筆資料)')

if i % 20 != 0:
    print(f'處理第 {str(i // 20 + 1)} 頁完畢! (共 {str(i)} 筆資料)')

conn.close()
print("end!")
driver.quit()
