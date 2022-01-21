from extractor import SimpleStockPage
from datetime import date


class SimpleStockAnalyser:
    def analyse(self, stock_page: SimpleStockPage) -> bool:
        current_year = date.today().year
        dividends = stock_page.dividends().get_dividends()
        last_dividend = 0.0
        if current_year in dividends:
            last_dividend = dividends[current_year]
        elif current_year-1 in dividends:
            last_dividend = dividends[current_year-1]
        dividend_stock_price_ratio = float(last_dividend.value_per_share())/float(stock_page.current_price())

        return dividend_stock_price_ratio > 0.05
