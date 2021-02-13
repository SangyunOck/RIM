from Fund import *
from Asset import *
from Profit import *
from Tools import *
from RIM import *


class Calc:
    def __init__(self, data, code, linked):
        fund = Fund(data)
        asset = Asset(data, code)
        profit = Profit(data)

        operating_profit_rate, trend_ROA = get_expected_value_4val(profit.get_operating_profit(),
                                                                   asset.get_facility_investment(),
                                                                   asset.get_working_capital(),
                                                                   sum(
                                                                       profit.get_quarter_operating_profit()),
                                                                   "영업자산이익률")

        # 영업자산이익 구하기 완료
        operating_profit = operating_profit_rate * (asset.get_facility_investment()[3] + asset.get_working_capital()[3])
        self.__ROA = operating_profit_rate
        self.__ROA_trend = trend_ROA

        quarter_operating_profit = sum(profit.get_quarter_operating_profit())
        quarter_interest_expense = sum(profit.get_quarter_interest_expense())
        quarter_income_tax_expense = sum(profit.get_quarter_income_tax_expense())
        quarter_net_income = sum(profit.get_quarter_net_income())
        quarter_controlling_net_income = sum(profit.get_quarter_controlling_net_income())
        quarter_non_controlling_net_income = sum(profit.get_quarter_non_controlling_net_income())

        data1 = []
        for i in range(4):
            data1.append(get_non_operating_profit(profit.get_operating_profit()[i], profit.get_interest_expense()[i],
                                                  profit.get_income_tax_expense()[i], profit.get_net_income()[i]))

        data3 = quarter_net_income - quarter_operating_profit + quarter_interest_expense + quarter_income_tax_expense
        non_operating_profit_rate, trend_non_operating_profit_rate = get_expected_value_4val(data1,
                                                                                             asset.get_financial_investment(),
                                                                                             asset.get_surplus_fund(),
                                                                                             data3, "비영업자산이익률")

        # 비영업이익 구하기 완료
        non_operating_profit = (asset.get_financial_investment()[3] + asset.get_surplus_fund()[
            3]) * non_operating_profit_rate

        # 이자비용 구하기 완료
        external_borrowing_rate = get_expected_value_3val(profit.get_interest_expense(), fund.get_external_borrowing(),
                                                          quarter_interest_expense)
        interest_expense = fund.get_external_borrowing()[3] * external_borrowing_rate

        check = operating_profit + non_operating_profit - interest_expense
        if check <= 0:
            income_tax_expense = 0
        elif check < 200:
            income_tax_expense = check * 0.2 - 0.2
        elif check < 3000:
            income_tax_expense = check * 0.22 - 4.2
        else:
            income_tax_expense = check * 0.25 - 94.2

        net_income = operating_profit + non_operating_profit - interest_expense - income_tax_expense
        if quarter_controlling_net_income + quarter_non_controlling_net_income <= 0:
            controlling_ratio = 1
        else:
            controlling_ratio = quarter_controlling_net_income / (
                    quarter_controlling_net_income + quarter_non_controlling_net_income)

        # 지배주주순이익
        controlling_net_income = net_income * controlling_ratio

        if linked == "연결":
            # val : 주주몫(자기자본)
            val = fund.get_retained_profit()[3] + fund.get_shareholder_investment()[3]
            if val > 0:
                ROE = controlling_net_income / val
            else:
                ROE = 0
        else:
            val = fund.get_retained_profit()[3] + fund.get_shareholder_investment()[3]
            if val > 0:
                ROE = net_income / net_income / val
            else:
                ROE = 0

        self.ROE = ROE

        soup = get_snap_shot_soup(code)

        rim = RIM(soup)
        category = rim.get_category()
        sell_price_2, reduce_10_2, reduce_20_2 = rim.get_RIM_price(fund.get_quarter_retained_profit()[3] +
                                                                   fund.get_quarter_shareholder_investment()[3],
                                                                   self.ROE, 0.0791)

        self.__prices = (sell_price_2, reduce_10_2, reduce_20_2)
        self.__category = category
        self.__allocation = rim.get_allocation_rate()

    def get_prices(self):
        return self.__prices

    def get_ROA(self):
        return self.__ROA

    def get_category(self):
        return self.__category

    def get_ROA_trend(self):
        return self.__ROA_trend

    def get_allocation(self):
        return self.__allocation
