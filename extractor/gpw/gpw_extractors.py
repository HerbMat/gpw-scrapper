from typing import Iterable, List
from urllib.parse import urlparse, ParseResult
import requests
from bs4 import BeautifulSoup, Tag
from extractor import InfoExtractor, Indicators, ProfitLossAccount, ProfitLossReport, BalanceAccount, BalanceReport, \
    Dividend, Dividends, StockPage, CompanyExtractor, StockMarketInfoExtractor


class GPWBaseInfoExtractor(InfoExtractor[float]):
    def extract(self, soup: BeautifulSoup) -> float:
        return soup.find(text='Kurs').parent.parent.next_sibling.findChild().contents[0]


class GPWIndicatorsExtractor(InfoExtractor[Indicators]):
    def extract(self, soup: BeautifulSoup) -> Indicators:
        return Indicators(
            self._extract_price_earnings_ratio(soup),
            self._extract_operational_earnings_ratio(soup),
            self._extract_price_value_ratio(soup),
            self._extract_price_income_ratio(soup)
        )

    def _extract_price_earnings_ratio(self, soup: BeautifulSoup) -> float:
        return self._extract_indicator('C/Z', soup)

    def _extract_operational_earnings_ratio(self, soup: BeautifulSoup) -> float:
        return self._extract_indicator('C/ZO', soup)

    def _extract_price_value_ratio(self, soup: BeautifulSoup) -> float:
        return self._extract_indicator('C/WK', soup)

    def _extract_price_income_ratio(self, soup: BeautifulSoup) -> float:
        return self._extract_indicator('C/P', soup)

    def _extract_indicator(self, indicator_name: str, soup: BeautifulSoup) -> float:
        indicator = soup.find(text=indicator_name)
        if indicator is None:
            return -1
        return float(indicator.parent.parent.next_sibling.next_sibling.findChild().findChild().contents[0].replace(" ", ""))


class GPWProfitLossExtractor(InfoExtractor[ProfitLossAccount]):
    def extract(self, soup: BeautifulSoup) -> ProfitLossAccount:
        years = self._get_years(soup)
        params_length = len(years)
        profit_loss_account = ProfitLossAccount()
        if params_length == 0:
            return profit_loss_account
        incomes = self._get_incomes(soup, params_length)
        profits = self._get_profits(soup, params_length)
        net_profits = self._get_net_profits(soup, params_length)
        try:
            for i in range(params_length):
                profit_loss_report = ProfitLossReport(years[i], incomes[i], profits[i], net_profits[i])
                profit_loss_account.add(profit_loss_report)
        except IndexError:
            return profit_loss_account
        return profit_loss_account

    def _get_years(self, soup: BeautifulSoup) -> List:
        year_row = soup.find(class_='report-table')
        if year_row is None:
            return []
        year_elements = year_row.findChildren('th')
        year_elements.pop(0)
        year_elements.pop()
        return [year_element.contents[0].strip() for year_element in year_elements]

    def _get_incomes(self, soup: BeautifulSoup, length: int) -> Iterable:
        return self._get_indicators_value(soup, length, 'IncomeRevenues')

    def _get_profits(self, soup: BeautifulSoup, length: int) -> Iterable:
        return self._get_indicators_value(soup, length, 'IncomeGrossProfit')

    def _get_net_profits(self, soup: BeautifulSoup, length: int) -> Iterable:
        return self._get_indicators_value(soup, length, 'IncomeNetProfit')

    def _get_indicators_value(self, soup: BeautifulSoup, length: int, field_name: str):
        indicator_table_row = soup.find(class_='report-table').find('tr', {'data-field': field_name})
        if indicator_table_row is None:
            return [None for i in range(length)]
        # raport_elements = indicator_table_row.findChildren('td', {'class': 'h'})
        income_elements = indicator_table_row.findChildren('td', {'class': 'h'})
        income_elements = income_elements[-length:]
        return [self._map_to_value(income_element) for income_element in income_elements]

    def _map_to_value(self, tag: Tag):
        value_el = tag.findChild('span', {'class': 'value'})
        if value_el is None:
            return None
        return value_el.findChild().findChild().contents[0]


class GPWBalanceExtractor(InfoExtractor[BalanceAccount]):
    def extract(self, soup: BeautifulSoup) -> BalanceAccount:
        years = self._get_years(soup)
        params_length = len(years)
        balance_account = BalanceAccount()
        if params_length == 0:
            return balance_account
        assets = self._get_assets(soup, params_length)
        long_term_obligations = self._get_long_term_obligations(soup, params_length)
        short_term_obligations = self._get_short_term_obligations(soup, params_length)
        for i in range(params_length):
            balance_report = BalanceReport(years[i], assets[i], short_term_obligations[i], long_term_obligations[i])
            balance_account.add(balance_report)
        return balance_account

    def _get_years(self, soup: BeautifulSoup) -> List:
        year_row = soup.find(class_='report-table')
        if year_row is None:
            return []
        year_elements = year_row.findChildren('th')
        year_elements.pop(0)
        year_elements.pop()
        return [year_element.contents[0].strip() for year_element in year_elements]

    def _get_assets(self, soup: BeautifulSoup, length: int) -> Iterable:
        return self._get_indicators_value(soup, length, 'BalanceNoncurrentAssets')

    def _get_long_term_obligations(self, soup: BeautifulSoup, length: int) -> Iterable:
        return self._get_indicators_value(soup, length, 'BalanceNoncurrentLiabilities')

    def _get_short_term_obligations(self, soup: BeautifulSoup, length: int) -> Iterable:
        return self._get_indicators_value(soup, length, 'BalanceCurrentLiabilities')

    def _get_indicators_value(self, soup: BeautifulSoup, length: int, field_name: str):
        indicator_row = soup.find(class_='report-table').findChild('tr', {'data-field': field_name})
        if indicator_row is None:
            return [None for i in range(length)]
        income_elements = indicator_row.findChildren('td', {'class': 'h'})
        income_elements = income_elements[-length:]
        return [self._map_to_value(income_element) for income_element in income_elements]

    def _map_to_value(self, tag: Tag):
        value_el = tag.findChild('span', {'class': 'value'})
        if value_el is None:
            return None
        return value_el.findChild().findChild().contents[0]


class GPWDividendExtractor(InfoExtractor[Dividends]):
    def extract(self, soup: BeautifulSoup) -> Dividends:
        table = soup.find_all(class_='table-c')
        dividends = Dividends()
        if len(table) == 0:
            return dividends
        elements = table[0].findChildren('tr')
        elements.pop(0)
        for element in elements:
            dividend_table_row_elements = element.findChildren('td')
            year = int(dividend_table_row_elements[0].contents[0])
            dividend_per_share = self._convert_value_to_float(dividend_table_row_elements[2].findChildren()[0].contents[0])
            dividend_value = self._convert_value_to_int(dividend_table_row_elements[3].findChildren()[0].contents[0])
            dividend = Dividend(year, dividend_per_share, dividend_value)
            dividends.add(dividend)
        return dividends

    def _convert_value_to_float(self, value: str) -> float:
        if value == '-':
            return 0
        return float(value)

    def _convert_value_to_int(self, value: str) -> int:
        if value == '-':
            return 0
        return int(value.replace(" ", ""))


class GPWCompanyExtractor(CompanyExtractor):
    def __init__(self,
                 base_info_extractor: InfoExtractor[float],
                 indicators_extractor: InfoExtractor[Indicators],
                 profit_loss_extractor: InfoExtractor[ProfitLossAccount],
                 balance_extractor: InfoExtractor[BalanceAccount],
                 dividend_extractor: InfoExtractor[Dividends]):
        self._base_info_extractor = base_info_extractor
        self._indicators_extractor = indicators_extractor
        self._profit_loss_extractor = profit_loss_extractor
        self._balance_extractor = balance_extractor
        self._dividend_extractor = dividend_extractor

    def extract(self, url: str) -> StockPage:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            base_info = self._base_info_extractor.extract(soup)
            indicators = self._indicators_extractor.extract(soup)
            base_url = urlparse(url)
            profit_loss_url = self._build_new_url(base_url, soup.find_all(text='ANALIZA FINANSOWA')[0].parent['href'])
            profit_loss_page = requests.get(profit_loss_url)
            soup = BeautifulSoup(profit_loss_page.content, 'html.parser')
            profit_loss_report = self._profit_loss_extractor.extract(soup)
            balance_url = self._build_new_url(base_url, soup.find_all(text='BILANS')[0].parent['href'])
            balance_page = requests.get(balance_url)
            soup = BeautifulSoup(balance_page.content, 'html.parser')
            balance_report = self._balance_extractor.extract(soup)
            dividend_url = self._build_new_url(base_url, soup.find_all(text='DYWIDENDY')[0].parent['href'])
            dividend_page = requests.get(dividend_url)
            soup = BeautifulSoup(dividend_page.content, 'html.parser')
            dividends = self._dividend_extractor.extract(soup)
            return StockPage(
                url,
                base_info,
                indicators,
                profit_loss_report,
                balance_report,
                dividends
            )
        except IndexError as e:
            raise e
        except AttributeError as e:
            raise e

    def _build_new_url(self, base_url: ParseResult, new_path: str):
        return base_url.scheme + "://" + base_url.hostname + new_path


class GPWStockMarketInfoExtractor(StockMarketInfoExtractor):

    def __init__(self, company_info_extractor: CompanyExtractor):
        self._company_info_extractor = company_info_extractor

    def extract(self, url: str) -> List[StockPage]:
        base_url = urlparse(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        company_rows = soup.find_all('table', class_='qTableFull')[0].findChildren(class_='soid')
        company_infos = []
        for company_row in company_rows:
            company_path = company_row.findChildren()[0].findChildren()[0]['href']
            company_url = self._build_new_url(base_url, company_path)
            company_infos.append(self._company_info_extractor.extract(company_url))
        return company_infos

    def _build_new_url(self, base_url: ParseResult, new_path: str):
        return base_url.scheme + "://" + base_url.hostname + new_path
