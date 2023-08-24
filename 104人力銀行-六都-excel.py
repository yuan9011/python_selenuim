# --------------------------------------------------
# 讀取 104人力銀行.xlsx 資料成 dataframe 形式
# 繪製: 六都職缺數量圓餅圖, 六都職缺平均起薪長條圖, 六都職缺學歷要求圓餅圖
# --------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# 設定中文字型

plt.rcParams["font.sans-serif"] = "mingliu"
plt.rcParams["axes.unicode_minus"] = False

# --------------------------------------------------
# 六都職缺數量

file_name = '104人力銀行.xlsx'
df = pd.read_excel(file_name)
city = ['台北', '新北', '桃園', '台中', '台南', '高雄']  # 六都
city_count = []  # 六都職缺數量
city_salary = []  # 六都職缺平均起薪
education = ['專科', '大學', '碩士']  # 學歷
city_education = []  # 六都職缺學歷要求

for i in range(len(city)):
    df_count = df[df['工作地點'].str.contains(city[i])]
    df_salary = df[(df['工作地點'].str.contains(city[i])) &
                   (df['薪資'].str.contains('月薪'))]
    df_education1 = df[(df['工作地點'].str.contains(city[i])) &
                       (df['學歷要求'].str.contains('專科'))]
    df_education2 = df[(df['工作地點'].str.contains(city[i])) &
                       (df['學歷要求'].str.contains('大學'))]
    df_education3 = df[(df['工作地點'].str.contains(city[i])) &
                       (df['學歷要求'].str.contains('碩士'))]
    city_count.append(len(df_count))
    city_education.append([len(df_education1), len(df_education2),
                           len(df_education3)])
    salary_index = df_salary.index
    salary_total = 0

    for j in range(len(df_salary)):
        salary_item = df_salary['薪資'][salary_index[j]]\
            .replace(',', '')\
            .replace('月薪', '')\
            .replace('元', '')\
            .replace('以上', '')

        salary_num = str(salary_item).strip().split('~')  # [薪資起薪, ...]
        salary_total += int(salary_num[0])

    salary_mean = salary_total // len(df_salary)
    city_salary.append(salary_mean)

# --------------------------------------------------
# 六都職缺數量圓餅圖

plt.figure()
ser_count = pd.Series(city_count, index=city)  # 串列轉Series
plt.subplot(1, 2, 1)
plt.axis("off")

s1 = ser_count.plot(kind="pie",
                    title="六都職缺數量",
                    figsize=(12, 6),
                    autopct='%.1f%%')

print("六都職缺數量")
ser_count['總和'] = ser_count.sum()
print(ser_count)

# --------------------------------------------------
# 六都職缺平均起薪長條圖

ser_salary = pd.Series(city_salary, index=city)
plt.subplot(1, 2, 2)
plt.tight_layout()

s2 = ser_salary.plot(kind="bar",
                     title="六都職缺平均薪資",
                     figsize=(12, 6),
                     ylabel='單位: 元')

ser_salary['平均'] = ser_salary.mean()
print('\n六都職缺平均起薪')
print(ser_salary)

# --------------------------------------------------
# 六都職缺學歷要求圓餅圖

plt.figure()
ser_education = pd.DataFrame(city_education)
ser_education.index = city
ser_education.columns = education
ser_education_t = ser_education.transpose()

for i in range(len(city)):
    plt.subplot(2, len(city) // 2, i + 1)
    s = ser_education_t[city[i]].plot(kind='pie',
                                      title=city[i],
                                      figsize=(12, 6),
                                      autopct='%.1f%%',
                                      ylabel='')

print("\n六都職缺學歷要求")
print(ser_education)
plt.show()
