from Calc import *
from Tools import getCompanyDict, get_now_price, get_company_type, check_if_black_list
import requests
from bs4 import BeautifulSoup
import time
from DB import *


class Main:
    def __init__(self):
        company = getCompanyDict()
        codes = list(company.keys())
        contents = list(company.values())

        self.db = DB()
        count = 1
        for code, content in zip(codes, contents):
            print(str(count) + '/' + str(len(codes)), code, *content)
            count += 1
            try:
                self.process(code, *content, "연결")
                time.sleep(0.1)

            except ZeroDivisionError:
                try:
                    self.process(code, *content, "별도")
                    time.sleep(0.1)
                except IndexError:
                    pass

            except IndexError:
                pass

        self.db.saveData()

    def process(self, code, name, category, product, linked):
        fn_web = None

        if linked == "연결":
            time.sleep(0.1)
            while fn_web is None:
                try:
                    fn_web = requests.get(
                        "http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A" + code + "&cID=&MenuYn=Y&ReportGB=D&NewMenuID=103&stkGb=701")
                except:
                    pass
        else:
            time.sleep(0.1)
            while fn_web is None:
                try:
                    fn_web = requests.get(
                        "http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A" + code + "&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701")
                except:
                    pass

        fn_soup = BeautifulSoup(fn_web.content, "html.parser")

        # data-> 0: 포괄손익계산서, 1: 재무상태표, 2: 현금흐름표
        data = fn_soup.findAll(class_="ul_co1_c pd_t1")

        calc = Calc(data, code, linked)
        company_type = get_company_type(*calc.get_prices(), get_now_price(code), calc.get_ROA())
        # if calc.get_ROA() >= 0.1 and calc.get_allocation() >= 1:
        if not check_if_black_list(calc.get_category()):
            if company_type == "low":
                self.db.addCompany("low", code, name, *calc.get_prices(), get_now_price(code), category, product,
                                   round(calc.get_ROA(), 2), round(calc.get_ROA_trend(), 2))

            elif company_type == "between":
                self.db.addCompany("between", code, name, *calc.get_prices(), get_now_price(code), category, product,
                                   round(calc.get_ROA(), 2), round(calc.get_ROA_trend(), 2))


if __name__ == '__main__':
    main = Main()
