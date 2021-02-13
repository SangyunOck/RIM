from Tools import get_sum_int, get_value_by_name


class Profit:
    def __init__(self, data):
        # 영업이익
        operating_profit = [get_value_by_name(data, "포괄손익계산서", "영업이익", "연간"), ]
        self.__operating_profit = get_sum_int(operating_profit)

        # 이자비용
        interest_expense = [get_value_by_name(data, "포괄손익계산서", "이자비용", "연간"), ]
        self.__interest_expense = get_sum_int(interest_expense)

        # 법인세비용
        income_tax_expense = [get_value_by_name(data, "포괄손익계산서", "법인세비용", "연간"), ]
        self.__income_tax_expense = get_sum_int(income_tax_expense)

        # 당기순이익
        net_income = [get_value_by_name(data, "포괄손익계산서", "당기순이익", "연간"), ]
        self.__net_income = get_sum_int(net_income)

        # 지배주주순이익
        controlling_net_income = [get_value_by_name(data, "포괄손익계산서", "지배주주순이익", "연간"), ]
        self.__controlling_net_income = get_sum_int(controlling_net_income)

        # 비지배주주순이익
        non_controlling_net_income = [get_value_by_name(data, "포괄손익계산서", "비지배주주순이익", "연간"), ]
        self.__non_controlling_net_income = get_sum_int(non_controlling_net_income)

        # 분기 영업이익
        quarter_operating_profit = [get_value_by_name(data, "포괄손익계산서", "영업이익", "분기"), ]
        self.__quarter_operating_profit = get_sum_int(quarter_operating_profit)

        # 분기 이자비용
        quarter_interest_expense = [get_value_by_name(data, "포괄손익계산서", "이자비용", "분기"), ]
        self.__quarter_interest_expense = get_sum_int(quarter_interest_expense)

        # 분기 법인세비용
        quarter_income_tax_expense = [get_value_by_name(data, "포괄손익계산서", "법인세비용", "분기"), ]
        self.__quarter_income_tax_expense = get_sum_int(quarter_income_tax_expense)

        # 분기 당기순이익
        quarter_net_income = [get_value_by_name(data, "포괄손익계산서", "당기순이익", "분기"), ]
        self.__quarter_net_income = get_sum_int(quarter_net_income)

        # 분기 지배주주순이익
        quarter_controlling_net_income = [get_value_by_name(data, "포괄손익계산서", "지배주주순이익", "분기"), ]
        self.__quarter_controlling_net_income = get_sum_int(quarter_controlling_net_income)

        # 분기 비지배주주순이익
        quarter_non_controlling_net_income = [get_value_by_name(data, "포괄손익계산서", "비지배주주순이익", "분기"), ]
        self.__quarter_non_controlling_net_income = get_sum_int(quarter_non_controlling_net_income)


    def get_operating_profit(self):
        return self.__operating_profit

    def get_interest_expense(self):
        return self.__interest_expense

    def get_income_tax_expense(self):
        return self.__income_tax_expense

    def get_net_income(self):
        return self.__net_income

    def get_controlling_net_income(self):
        return self.__controlling_net_income

    def get_non_controlling_net_income(self):
        return self.__non_controlling_net_income

    def get_quarter_operating_profit(self):
        return self.__quarter_operating_profit

    def get_quarter_interest_expense(self):
        return self.__quarter_interest_expense

    def get_quarter_income_tax_expense(self):
        return self.__quarter_income_tax_expense

    def get_quarter_net_income(self):
        return self.__quarter_net_income

    def get_quarter_controlling_net_income(self):
        return self.__quarter_controlling_net_income

    def get_quarter_non_controlling_net_income(self):
        return self.__quarter_non_controlling_net_income
