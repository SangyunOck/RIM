from Tools import get_value_by_name, get_sum_int


class Asset:
    def __init__(self, data, code):
        self.code = code

        # 설비투자
        facility_investment = [
            get_value_by_name(data, "재무상태표", "유형자산", "연간"),
            get_value_by_name(data, "재무상태표", "무형자산", "연간"),
            get_value_by_name(data, "재무상태표", "비유동생물자산", "연간"), ]
        self.__facility_investment = get_sum_int(facility_investment)

        # 운전자산
        working_capital = [get_value_by_name(data, "재무상태표", "재고자산", "연간"),
                           get_value_by_name(data, "재무상태표", "유동생물자산", "연간"),
                           get_value_by_name(data, "재무상태표", "매출채권및기타유동채권", "연간"),
                           get_value_by_name(data, "재무상태표", "당기법인세자산", "연간"),
                           get_value_by_name(data, "재무상태표", "계약자산", "연간"),
                           get_value_by_name(data, "재무상태표", "반품(환불)자산", "연간"),
                           get_value_by_name(data, "재무상태표", "배출권", "연간"),
                           get_value_by_name(data, "재무상태표", "기타유동자산", "연간"),
                           get_value_by_name(data, "재무상태표", "장기매출채권및기타비유동채권", "연간"),
                           get_value_by_name(data, "재무상태표", "이연법인세자산", "연간"),
                           get_value_by_name(data, "재무상태표", "장기당기법인세자산", "연간"),
                           get_value_by_name(data, "재무상태표", "기타비유동자산", "연간"), ]
        self.__working_capital = get_sum_int(working_capital)

        # 금융투자
        financial_investment = [get_value_by_name(data, "재무상태표", "투자부동산", "연간"),
                                get_value_by_name(data, "재무상태표", "장기금융자산", "연간"),
                                get_value_by_name(data, "재무상태표", "관계기업등지분관련투자자산", "연간"), ]

        self.__financial_investment = get_sum_int(financial_investment)

        # 여유자금
        surplus_fund = [get_value_by_name(data, "재무상태표", "현금및현금성자산", "연간"),
                        get_value_by_name(data, "재무상태표", "유동금융자산", "연간"), ]
        self.__surplus_fund = get_sum_int(surplus_fund)

        # 기타
        etc_asset = [get_value_by_name(data, "재무상태표", "매각예정비유동자산및처분자산집단", "연간"),
                     get_value_by_name(data, "재무상태표", "기타금융업자산", "연간"), ]
        self.__etc_asset = get_sum_int(etc_asset)

    def get_facility_investment(self):
        return self.__facility_investment

    def get_working_capital(self):
        return self.__working_capital

    def get_financial_investment(self):
        return self.__financial_investment

    def get_surplus_fund(self):
        return self.__surplus_fund

    def get_etc_asset(self):
        return self.__etc_asset
