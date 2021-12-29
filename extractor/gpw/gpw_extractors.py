from bs4 import BeautifulSoup
from extractor import InfoExtractor


class GPWBaseInfoExtractor(InfoExtractor[float]):
    def extract(self, soup: BeautifulSoup) -> float:
        return soup.find_all(text='Kurs')[0].parent.parent.next_sibling.findChildren()[0].contents[0]
