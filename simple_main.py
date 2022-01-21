from extractor import GPWIndicatorsExtractor, GPWProfitLossExtractor, GPWBalanceExtractor, GPWDividendExtractor, \
    GPWCompanyExtractor, GPWBaseInfoExtractor, GPWStockMarketInfoExtractor, SimpleStockPage, SimpleGPWCompanyExtractor
from configuration import conf_properties
from datetime import date
from analyser import SimpleStockAnalyser

if __name__ == '__main__':

    gpw_company_extractor = SimpleGPWCompanyExtractor(
        GPWBaseInfoExtractor(),
        GPWIndicatorsExtractor(),
        GPWDividendExtractor()
    )
    main_page = ''
    dividend_page = ''
    with open('kghm-main.html', 'r') as main:
        main_page = main.read()
    with open('kghm-dividend.html', 'r') as dividend:
        dividend_page = dividend.read()
    stock_page = gpw_company_extractor.extract(main_page, dividend_page, 'KGHM')
    simple_stock_analyser = SimpleStockAnalyser()
    result = simple_stock_analyser.analyse(stock_page)
    print("found")
