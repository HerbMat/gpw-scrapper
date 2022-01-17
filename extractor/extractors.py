from bs4 import BeautifulSoup
from extractor import StockPage
from typing import TypeVar, Protocol, List

T = TypeVar('T')


class InfoExtractor(Protocol[T]):
    def extract(self, soup: BeautifulSoup) -> T:
        pass


class CompanyExtractor:
    def extract(self, url: str) -> StockPage:
        pass


class StockMarketInfoExtractor:
    def extract(self, url: str) -> List[StockPage]:
        pass

