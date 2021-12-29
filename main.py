from bs4 import BeautifulSoup
import requests

from extractor import GPWBaseInfoExtractor

if __name__ == '__main__':
    page = requests.get("https://www.biznesradar.pl/notowania/KGHM")
    soup = BeautifulSoup(page.content, 'html.parser')
    gpw_extractor = GPWBaseInfoExtractor()
    print(gpw_extractor.extract(soup))
    # rows = soup.find_all('table', id="profileSummaryCurrent")
    # rows = soup.find_all('table', class_="profileSummaryCurrent")
    # rows = soup.find_all(text='Kurs:')

    print("found")



