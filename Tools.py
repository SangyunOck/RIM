import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from RIM import *
import time
import numpy

FILE_PATH = 'C:/Users/OckSangYun/Desktop/'


def get_sum_int(data):
    return_val = [0] * 4
    for i in data:
        for j in range(4):
            return_val[j] += i[j]
    return return_val


def get_expected_value_4val(data1, data2, data3, data4, typeCheck):
    first_rate = data1[1] * 2 / (data2[0] + data3[0] + data2[1] + data3[1]) if data2[0] + data3[0] + data2[1] + data3[
        1] != 0 else 0

    second_rate = data1[2] * 2 / (data2[1] + data3[1] + data2[2] + data3[2]) if data2[1] + data3[1] + data2[2] + data3[
        2] != 0 else 0

    quarter_sum = data4
    third_rate = quarter_sum * 2 / (data2[2] + data3[2] + data2[3] + data3[3]) if data2[2] + data3[2] + data2[3] + \
                                                                                  data3[3] != 0 else 0

    if typeCheck == "영업자산이익률":
        if first_rate < second_rate < third_rate or first_rate > second_rate > third_rate:
            fourth_rate = third_rate

        else:
            fourth_rate = (first_rate * 1 + second_rate * 1.5 + third_rate * 3) / 5.5

        return fourth_rate, getTrend([1, 2, 3, 4], [first_rate, second_rate, third_rate, fourth_rate])

    elif typeCheck == "비영업자산이익률":
        weight_average = (first_rate * 1 + second_rate * 1.5 + third_rate * 3) / 5.5
        trend_1 = min(first_rate, second_rate, third_rate) if min(first_rate, second_rate, third_rate) > 0 else 0
        trend_2 = weight_average if max(first_rate, second_rate, third_rate) < 0 else 0
        standard_deviation = weight_average if numpy.std([first_rate, second_rate, third_rate]) < 0.01 else 0
        result = standard_deviation if max(trend_1, trend_2) == 0 else max(trend_1, trend_2)
        return result, getTrend([1, 2, 3, 4], [first_rate, second_rate, third_rate, weight_average])


def get_expected_value_3val(data1, data2, data3):
    result = data3 * 2 / (data2[2] + data2[3]) if data2[2] + data2[3] > 0 else 0
    return result


def get_non_operating_profit(operating_profit, interest_expense, income_tax_expense, net_income):
    return net_income - operating_profit + interest_expense + income_tax_expense


def get_value_by_name(data, data_type, name_get, is_year):
    if data_type == "포괄손익계산서":
        data_num = 0
    elif data_type == "재무상태표":
        data_num = 1
    elif data_type == "현금흐름표":
        data_num = 2

    if is_year == "연간":
        year_num = 0
    elif is_year == "분기":
        year_num = 1

    detail = data[data_num].findAll(class_="um_table")
    all_content_in_detail = detail[year_num].findAll('tr')

    returnVal = [0] * 4
    for content in all_content_in_detail:
        name = content.find('th', {'class': 'l clf'})
        if name and name.text.strip() == name_get:
            temp = [int(i.text.replace(',', '').replace('\xa0', '0')) for i in content.findAll(class_='r')[:4]]
            for i in range(4):
                returnVal[i] += temp[i]

    return returnVal


def getCompanyDict():
    con = sqlite3.connect(FILE_PATH + "total.db")
    company = pd.read_sql("select * from total", con, index_col='index')
    company_dict = {}

    for i in range(len(company)):
        content = company.iloc[i]
        company_dict[content['종목코드']] = (content['회사명'], content['업종'], content['주요제품'])
    return company_dict


def get_now_price(code):
    naver_web = None

    while naver_web is None:
        try:
            naver_web = requests.get("https://finance.naver.com/item/main.nhn?code=" + code)
        except:
            pass

    naver_soup = BeautifulSoup(naver_web.content, "html.parser")
    try:
        price = naver_soup.find("p", {"class": "no_today"}).find("span", {"class": "blind"})
        price = int(price.string.replace(",", ""))
        return price
    except Exception as e:
        print(e)
        return -1


def get_company_type(sell_price, reduce_10, reduce_20, now_price, ROA):
    if reduce_20 < reduce_10 < sell_price:
        if now_price <= reduce_20 and ROA >= 0.05:
            return "low"

        if reduce_20 <= now_price <= reduce_10 and ROA >= 0.05:
            return "between"

        else:
            return None
    else:
        return None


def check_if_black_list(category):
    if category.replace('\xa0', '').replace(' ', '') in ["증권", "부동산", "창업투자및종금", "보험", "소비자금융", "상업은행"]:
        return True
    else:
        return False


def get_snap_shot_soup(code):
    time.sleep(0.1)
    fn_web = None

    while fn_web is None:
        try:
            fn_web = requests.get(
                "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A" + code + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701")
        except:
            pass
    fn_soup = BeautifulSoup(fn_web.content, 'html.parser')
    return fn_soup


def getTrend(period, data):
    if len(period) <= 0 or len(data) <= 0:
        return 0

    avg_period = np.average(period)
    avg_value = np.average(data)

    divisor = sum([(i - avg_period) ** 2 for i in period])
    divident = sum([(i - avg_period) * (j - avg_value) for i, j in zip(period, data)])

    if divisor != 0:
        a = divident / divisor
    else:
        print("divisor :" + divisor, "divident :" + divident)
        a = 0

    return a
