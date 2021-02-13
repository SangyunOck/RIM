import sqlite3
import pandas as pd

FILE_PATH = 'C:/Users/OckSangYun/Desktop/'


class DB:
    def __init__(self):
        self.nice_company_codes = []
        self.nice_company_names = []
        self.nice_company_ROA = []
        self.nice_company_ROA_trend = []
        self.nice_company_now_price = []
        self.nice_company_proper_buy_price = []
        self.nice_company_proper_sell1_price = []
        self.nice_company_proper_sell2_price = []
        self.nice_company_delta = []
        self.nice_company_category = []

        self.nice_company_between_codes = []
        self.nice_company_between_names = []
        self.nice_company_between_ROA = []
        self.nice_company_between_ROA_trend = []
        self.nice_company_between_now_price = []
        self.nice_company_between_proper_buy_price = []
        self.nice_company_between_proper_sell1_price = []
        self.nice_company_between_proper_sell2_price = []
        self.nice_company_between_delta = []
        self.nice_company_between_category = []

    def addCompany(self, company_type, code, name, sell_price, reduce_10, reduce_20, now_price, category, ROA,
                   ROA_trend):

        delta = round((reduce_20 / now_price - 1) * 100, 2)

        if company_type == "low":
            self.nice_company_codes.append(code)
            self.nice_company_names.append(name)
            self.nice_company_ROA.append(ROA)
            self.nice_company_ROA_trend.append(ROA_trend)
            self.nice_company_now_price.append(now_price)
            self.nice_company_proper_buy_price.append(reduce_20)
            self.nice_company_proper_sell1_price.append(reduce_10)
            self.nice_company_proper_sell2_price.append(sell_price)
            self.nice_company_category.append(category)
            self.nice_company_delta.append(delta)
            print("좋은 회사 발견 ! : " + name, sell_price, reduce_10, reduce_20, now_price)

        elif company_type == "between":
            self.nice_company_between_codes.append(code)
            self.nice_company_between_names.append(name)
            self.nice_company_between_ROA.append(ROA)
            self.nice_company_between_ROA_trend.append(ROA_trend)
            self.nice_company_between_now_price.append(now_price)
            self.nice_company_between_proper_buy_price.append(reduce_20)
            self.nice_company_between_proper_sell1_price.append(reduce_10)
            self.nice_company_between_proper_sell2_price.append(sell_price)
            self.nice_company_between_category.append(category)
            self.nice_company_between_delta.append(delta)
            print("좋은 회사 발견 ! : " + name, sell_price, reduce_10, reduce_20, now_price)

    def saveData(self):
        con = sqlite3.connect(FILE_PATH + "nice_company_list.db")

        nice_company_pd = pd.DataFrame({'종목코드': self.nice_company_codes,
                                        '종목명': self.nice_company_names,
                                        '종목분류': self.nice_company_category,
                                        'ROA': self.nice_company_ROA,
                                        'ROA_추세': self.nice_company_ROA_trend,
                                        '현재가': self.nice_company_now_price,
                                        '매수적정가': self.nice_company_proper_buy_price,
                                        '매도적정가1': self.nice_company_proper_sell1_price,
                                        '매도적정가2': self.nice_company_proper_sell2_price,
                                        '매수적정가괴리율': self.nice_company_delta})

        nice_company_between_pd = pd.DataFrame({'종목코드': self.nice_company_between_codes,
                                                '종목명': self.nice_company_between_names,
                                                '종목분류': self.nice_company_between_category,
                                                'ROA': self.nice_company_between_ROA,
                                                'ROA_추세': self.nice_company_between_ROA_trend,
                                                '현재가': self.nice_company_between_now_price,
                                                '매수적정가': self.nice_company_between_proper_buy_price,
                                                '매도적정가1': self.nice_company_between_proper_sell1_price,
                                                '매도적정가2': self.nice_company_between_proper_sell2_price,
                                                '매수적정가괴리율': self.nice_company_between_delta})

        nice_company_pd.to_sql("nice_company_lowPrice", con)
        nice_company_between_pd.to_sql("nice_company_between_pd", con)
        con.commit()
        con.close()
