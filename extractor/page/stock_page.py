from typing import Dict


class Indicators:
    def __init__(self,
                 price_earnings_ratio: float,
                 price_operational_earnings_ratio: float,
                 price_value_ratio: float,
                 price_income_ratio: float):
        self._price_earnings_ratio = price_earnings_ratio
        self._price_operational_earnings_ratio = price_operational_earnings_ratio
        self._price_value_ratio = price_value_ratio
        self._price_income_ratio = price_income_ratio

    def price_earnings_ratio(self) -> float:
        return self._price_earnings_ratio

    def price_operational_earnings_ratio(self) -> float:
        return self._price_operational_earnings_ratio

    def price_value_ratio(self) -> float:
        return self._price_value_ratio

    def price_income_ratio(self) -> float:
        return self._price_income_ratio


class BalanceReport:
    def __init__(self, year: int, assets: int, short_term_obligations: int, long_term_obligations: int):
        self._year = year
        self._assets = assets
        self._short_term_obligations = short_term_obligations
        self._long_term_obligations = long_term_obligations

    def year(self) -> int:
        return self._year

    def assets(self) -> int:
        return self._assets

    def liabilities(self) -> int:
        return self._liabilities

    def short_term_obligations(self) -> int:
        return self._short_term_obligations

    def long_term_obligations(self) -> int:
        return self._long_term_obligations


class BalanceAccount:
    def __init__(self):
        self._balance_reports = {}

    def add(self, balance_report: BalanceReport):
        self._balance_reports[balance_report.year()] = balance_report

    def get_reports(self) -> Dict[int, BalanceReport]:
        return self._balance_reports


class ProfitLossReport:
    def __init__(self, year: str, income: int, earnings: int, net_earnings: int):
        self._year = year
        self._income = income
        self._earnings = earnings
        self._net_earnings = net_earnings

    def year(self) -> str:
        return self._year

    def income(self) -> int:
        return self._income

    def earnings(self) -> int:
        return self._earnings

    def net_earnings(self):
        return self._net_earnings


class ProfitLossAccount:
    def __init__(self):
        self._profitLossReports = {}

    def add(self, profit_loss_report: ProfitLossReport):
        self._profitLossReports[profit_loss_report.year()] = profit_loss_report

    def get_reports(self) -> Dict[str, ProfitLossReport]:
        return self._profitLossReports


class Dividend:
    def __init__(self, year: int, value_per_share: float, dividend_value: int):
        self._year = year
        self._value_per_share = value_per_share
        self._dividend_value = dividend_value

    def year(self) -> int:
        return self._year

    def value_per_share(self) -> float:
        return self._value_per_share

    def dividend_value(self) -> int:
        return self._dividend_value


class Dividends:
    def __init__(self):
        self._dividends = {}

    def add(self, dividend: Dividend):
        self._dividends[dividend.year()] = dividend

    def get_dividends(self) -> Dict[int, Dividend]:
        return self._dividends


class StockPage:
    def __init__(self,
                 url: str,
                 current_price: float,
                 indicators: Indicators,
                 profit_loss_account: ProfitLossAccount,
                 balance_account: BalanceAccount,
                 dividends: Dividends):
        self._url = url
        self._current_price = current_price
        self._indicators = indicators
        self._profit_loss_account = profit_loss_account
        self._balance_account = balance_account
        self._dividends = dividends

    def url(self) -> str:
        return self._url

    def current_price(self) -> float:
        return self._current_price

    def indicators(self) -> Indicators:
        return self._indicators

    def profit_loss_account(self) -> ProfitLossAccount:
        return self._profit_loss_account

    def balance_account(self) -> BalanceAccount:
        return self._balance_account

    def dividends(self) -> Dividends:
        return self._dividends
