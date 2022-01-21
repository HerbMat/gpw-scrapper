from bs4 import BeautifulSoup

from extractor import InfoExtractor, CompanyExtractor, Dividends, Indicators


class SimpleStockPage:
    def __init__(self,
                 url: str,
                 current_price: float,
                 indicators: Indicators,
                 dividends: Dividends):
        self._url = url
        self._current_price = current_price
        self._indicators = indicators
        self._dividends = dividends

    def url(self) -> str:
        return self._url

    def current_price(self) -> float:
        return self._current_price

    def indicators(self) -> Indicators:
        return self._indicators

    def dividends(self) -> Dividends:
        return self._dividends


class SimpleGPWCompanyExtractor:
    def __init__(self,
                 base_info_extractor: InfoExtractor[float],
                 indicators_extractor: InfoExtractor[Indicators],
                 dividend_extractor: InfoExtractor[Dividends]):
        self._base_info_extractor = base_info_extractor
        self._dividend_extractor = dividend_extractor
        self._indicators_extractor = indicators_extractor

    def extract(self, main_page: str, dividend_page: str, name: str):
        try:
            soup = BeautifulSoup(main_page, 'html.parser')
            base_info = self._base_info_extractor.extract(soup)
            indicators = self._indicators_extractor.extract(soup)
            soup = BeautifulSoup(dividend_page, 'html.parser')
            dividends = self._dividend_extractor.extract(soup)
            return SimpleStockPage(
                name,
                base_info,
                indicators,
                dividends
            )
        except IndexError as e:
            raise e
        except AttributeError as e:
            raise e
