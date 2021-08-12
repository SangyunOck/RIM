from Tools import get_sum_int, get_value_by_name


class Fund:
    def __init__(self, data):
        # 신용조달
        credit_fund = [get_value_by_name(data, "재무상태표", "매입채무및기타유동채무", "연간"),
                       get_value_by_name(data, "재무상태표", "유동종업원급여충당부채", "연간"),
                       get_value_by_name(data, "재무상태표", "기타단기충당부채", "연간"),
                       get_value_by_name(data, "재무상태표", "당기법인세부채", "연간"),
                       get_value_by_name(data, "재무상태표", "계약부채", "연간"),
                       get_value_by_name(data, "재무상태표", "반품(환불)부채", "연간"),
                       get_value_by_name(data, "재무상태표", "배출부채", "연간"), 
                       get_value_by_name(data, "재무상태표", "기타유동부채", "연간"),
                       get_value_by_name(data, "재무상태표", "장기매입채무및기타비유동채무", "연간"),
                       get_value_by_name(data, "재무상태표", "비유동종업원급여충당부채", "연간"),
                       get_value_by_name(data, "재무상태표", "기타장기충당부채", "연간"),
                       get_value_by_name(data, "재무상태표", "이연법인세부채", "연간"),
                       get_value_by_name(data, "재무상태표", "장기당기법인세부채", "연간"),
                       get_value_by_name(data, "재무상태표", "기타비유동부채", "연간"), ]
        self.__credit_financing = get_sum_int(credit_fund)

        # 외부차입
        external_borrowing = [get_value_by_name(data, "재무상태표", "단기사채", "연간"),
                              get_value_by_name(data, "재무상태표", "단기차입금", "연간"),
                              get_value_by_name(data, "재무상태표", "유동성장기부채", "연간"),
                              get_value_by_name(data, "재무상태표", "유동금융부채", "연간"),
                              get_value_by_name(data, "재무상태표", "사채", "연간"),
                              get_value_by_name(data, "재무상태표", "장기차입금", "연간"),
                              get_value_by_name(data, "재무상태표", "비유동금융부채", "연간"), ]
        self.__external_borrowing = get_sum_int(external_borrowing)

        # 유보이익
        retained_profit = [get_value_by_name(data, "재무상태표", "기타포괄손익누계액", "연간"),
                           get_value_by_name(data, "재무상태표", "이익잉여금(결손금)", "연간"), ]
        self.__retained_profit = get_sum_int(retained_profit)

        # 주주투자
        shareholder_investment = [get_value_by_name(data, "재무상태표", "자본금", "연간"),
                                  get_value_by_name(data, "재무상태표", "신종자본증권", "연간"),
                                  get_value_by_name(data, "재무상태표", "자본잉여금", "연간"),
                                  get_value_by_name(data, "재무상태표", "기타자본", "연간"), ]
        self.__shareholder_investment = get_sum_int(shareholder_investment)

        # 비지배주주지분
        non_shareholder_investment = [get_value_by_name(data, "재무상태표", "비지배주주지분", "연간"), ]
        self.__non_shareholder_investment = get_sum_int(non_shareholder_investment)

        # 기타
        etc = [get_value_by_name(data, "재무상태표", "매각예정으로분류된처분자산집단에포함된부채", "연간"),
               get_value_by_name(data, "재무상태표", "기타금융업부채", "연간"), ]
        self.__etc = get_sum_int(etc)

        # 분기기준 유보이익
        quarter_retained_profit = [get_value_by_name(data, "재무상태표", "기타포괄손익누계액", "분기"),
                                   get_value_by_name(data, "재무상태표", "이익잉여금(결손금)", "분기"), ]
        self.__quarter_retained_profit = get_sum_int(quarter_retained_profit)

        # 분기기준 주주투자
        quarter_shareholder_investment = [get_value_by_name(data, "재무상태표", "자본금", "분기"),
                                          get_value_by_name(data, "재무상태표", "신종자본증권", "분기"),
                                          get_value_by_name(data, "재무상태표", "자본잉여금", "분기"),
                                          get_value_by_name(data, "재무상태표", "기타자본", "분기"), ]
        self.__quarter_shareholder_investment = get_sum_int(quarter_shareholder_investment)

    def get_credit_financing(self):
        return self.__credit_financing

    def get_external_borrowing(self):
        return self.__external_borrowing

    def get_retained_profit(self):
        return self.__retained_profit

    def get_shareholder_investment(self):
        return self.__shareholder_investment

    def get_non_shareholder_investment(self):
        return self.__non_shareholder_investment

    def get_etc(self):
        return self.__etc

    def get_quarter_retained_profit(self):
        return self.__quarter_retained_profit

    def get_quarter_shareholder_investment(self):
        return self.__quarter_shareholder_investment
