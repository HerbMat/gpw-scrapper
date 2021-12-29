from bs4 import BeautifulSoup
from extractor import Indicators, BalanceAccount, ProfitLossAccount, Dividends, StockPage
from typing import TypeVar, Protocol


T = TypeVar('T')


class InfoExtractor(Protocol[T]):
    def extract(self, soup: BeautifulSoup) -> T:
        pass


class Extractor:
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

    def extract(self, soup: BeautifulSoup) -> StockPage:
        return StockPage(
            self._base_info_extractor.extract(soup),
            self._indicators_extractor.extract(soup),
            self._profit_loss_extractor.extract(soup),
            self._balance_extractor.extract(soup),
            self._dividend_extractor.extract(soup)
        )
