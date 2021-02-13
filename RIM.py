import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np


class RIM:
    def __init__(self, fn_soup):
        self.fn_soup = fn_soup

    def get_total_stock_treasury_stock(self):
        total = int(1e9)
        treasury = 0
        data = self.fn_soup.findAll(class_='us_table_ty1 table-hb thbg_g h_fix zigbg_no')[0].findAll('tr')
        for row in data:
            name = row.find('div')
            if name and name.text.strip() == "발행주식수(보통주/ 우선주)":
                total = int(row.find(class_='r').text.split('/')[0].strip().replace(',', '')) + int(
                    row.find(class_='r').text.split('/')[1].strip().replace(',', ''))

        data = self.fn_soup.findAll(class_='us_table_ty1 h_fix zigbg_no notres')[1].findAll('tr')
        for row in data:
            name = row.find('div')
            if name and "자기주식" in name.text.strip():
                treasury = int(row.findAll(class_='r')[1].text.replace(',', '').replace('\xa0', '0'))

        return total, treasury

    def get_category(self):
        data = self.fn_soup.find('span', {'class': 'stxt stxt2'})
        category = data.text.strip('FICS  ').strip()

        return category

    def get_RIM_price(self, capital, ROE, demand):
        today = datetime.today()
        # criterion_year: 최근 결산연도
        ROE_annual, criterion_year = self.get_value_by_name_from_snapshot('ROE(%)(지배주주순이익(연율화) / 지배주주지분(평균)) * 100ROE',
                                                                          "연간")
        ROE_quarter, _ = self.get_value_by_name_from_snapshot('ROE(%)(지배주주순이익(연율화) / 지배주주지분(평균)) * 100ROE', "분기")
        total_stock, treasury_stock = self.get_total_stock_treasury_stock()

        try:
            # 컨센 없음
            if int(list(ROE_annual.keys())[-1].split('/')[0]) < datetime.today().year:
                start_year = int(list(ROE_quarter.keys())[-1].split('/')[0])
                start_month = int(list(ROE_quarter.keys())[-1].split('/')[1])
                ROE_quarter_data = list(ROE_quarter.values())[-4:]
                ROE_raw = 0.0
                for weight, val in enumerate(ROE_quarter_data):
                    ROE_raw += float(val.replace(',', '')) * (int(weight) + 1)
                ROE_raw /= 1000
                capital_raw = int(
                    list(self.get_value_by_name_from_snapshot('지배주주지분', "분기")[0].values())[-1].strip().replace(',', ''))


            else:
                # 컨센 있음
                start_year = int(list(ROE_annual.keys())[-1].split('/')[0])
                start_month = int(list(ROE_annual.keys())[-1].split('/')[1])
                ROE_raw = float(list(ROE_annual.values())[-1]) / 100
                capital_raw = int(
                    list(self.get_value_by_name_from_snapshot('지배주주지분', "연간")[0].values())[-1].strip().replace(',', ''))

            time_delta = (datetime(year=start_year, month=start_month, day=30) - today).days / 365
            duration = criterion_year + 10 - start_year if start_month == 12 else criterion_year + 11 - start_year

            reduce_0_1, reduce_10_1, reduce_20_1 = self.get_RIM_price_calc(capital, ROE, demand, time_delta,
                                                                           total_stock, treasury_stock,
                                                                           duration)

            reduce_0_2, reduce_10_2, reduce_20_2 = self.get_RIM_price_calc(capital_raw, ROE_raw, demand, time_delta,
                                                                           total_stock, treasury_stock,
                                                                           duration)

            return round((reduce_0_1 * 1.5 + reduce_0_2) / 2.5), round((reduce_10_1 * 1.5 + reduce_10_2) / 2.5), round(
                (reduce_20_1 * 1.5 + reduce_20_2) / 2.5)

        except Exception:
            return -1, -1, -1

    def get_RIM_price_calc(self, capital, ROE, demand, timedelta, total_stock, treasury_stock, duration):
        surplus_profit_none = []
        surplus_profit_reduce_10 = []
        surplus_profit_reduce_20 = []

        capital_calc_none = capital
        capital_calc_reduce_10 = capital
        capital_calc_reduce_20 = capital

        surplus_profit_rate_none = ROE - demand
        surplus_profit_rate_reduce_10 = ROE - demand
        surplus_profit_rate_reduce_20 = ROE - demand

        for i in range(duration):
            surplus_profit_rate_none *= 1
            ROE_calc_none = surplus_profit_rate_none + demand
            surplus_profit_none.append(capital_calc_none * (ROE_calc_none - demand))
            capital_calc_none += capital_calc_none * ROE_calc_none

            surplus_profit_rate_reduce_10 *= 0.9
            ROE_calc_reduce_10 = surplus_profit_rate_reduce_10 + demand
            surplus_profit_reduce_10.append(capital_calc_reduce_10 * (ROE_calc_reduce_10 - demand))
            capital_calc_reduce_10 += capital_calc_reduce_10 * ROE_calc_reduce_10

            surplus_profit_rate_reduce_20 *= 0.8
            ROE_calc_reduce_20 = surplus_profit_rate_reduce_20 + demand
            surplus_profit_reduce_20.append(capital_calc_reduce_20 * (ROE_calc_reduce_20 - demand))
            capital_calc_reduce_20 += capital_calc_reduce_20 * ROE_calc_reduce_20

        total_value = (np.npv(demand, surplus_profit_none) + capital)
        reduce_10_value = (np.npv(demand, surplus_profit_reduce_10) + capital)
        reduce_20_value = (np.npv(demand, surplus_profit_reduce_20) + capital)

        total_value_price = round(total_value * int(1e8) / (total_stock - treasury_stock) / (1 + demand) ** timedelta)
        reduce_10_price = round(reduce_10_value * int(1e8) / (total_stock - treasury_stock) / (1 + demand) ** timedelta)
        reduce_20_price = round(reduce_20_value * int(1e8) / (total_stock - treasury_stock) / (1 + demand) ** timedelta)

        return total_value_price, reduce_10_price, reduce_20_price

    def get_value_by_name_from_snapshot(self, name, data_type):
        try:
            if data_type == "연간":
                data_1 = self.fn_soup.find('div', {'id': 'highlight_D_Y'}).findAll('tr')
                data_2 = self.fn_soup.find('div', {'id': 'highlight_B_Y'}).findAll('tr')
            elif data_type == "분기":
                data_1 = self.fn_soup.find('div', {'id': 'highlight_D_Q'}).findAll('tr')
                data_2 = self.fn_soup.find('div', {'id': 'highlight_B_Q'}).findAll('tr')

            if data_1[2].text.replace('\xa0', '').split(' ').count('') <= data_2[2].text.replace('\xa0', '').split(
                    ' ').count(''):
                data = data_1
                linked = "연결"

            else:
                data = data_2
                linked = "별도"

            if name == "지배주주지분":
                if linked == "연결":
                    keyword = "지배주주지분"
                elif linked == "별도":
                    keyword = "자본총계"

            else:
                keyword = name

            for content in data:
                if content.find('th').text.strip() == keyword:
                    value = [i.text.replace('\xa0', '0') for i in content.findAll('td')]

            date_temp = data[1].findAll('th', {'scope': 'col'})
            date = [i.text for i in date_temp[:5]]
            criterion_year = int(date[-1].split('/')[0])
            date += [i.find(class_='txt_acd').text.strip('(E)') for i in date_temp[5:8]]

            return {year: val for year, val in zip(date, value) if val != '0'}, criterion_year
        except Exception:
            return None, None

    def get_allocation_rate(self):
        data = self.fn_soup.findAll('div', {'id': 'highlight_D_Y'})[0].findAll('tr')
        for content in data:
            name = content.find('span', {'class': 'txt_acd'})
            if name and name.text == "배당수익률":
                temp = [i.text for i in content.findAll('td') if i.text != '\xa0']
                if len(temp):
                    return float(temp[-1])
                else:
                    return 0
