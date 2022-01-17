from extractor import GPWIndicatorsExtractor, GPWProfitLossExtractor, GPWBalanceExtractor, GPWDividendExtractor, \
    GPWCompanyExtractor, GPWBaseInfoExtractor, GPWStockMarketInfoExtractor
from configuration import conf_properties

if __name__ == '__main__':

    gpw_company_extractor = GPWCompanyExtractor(
        GPWBaseInfoExtractor(),
        GPWIndicatorsExtractor(),
        GPWProfitLossExtractor(),
        GPWBalanceExtractor(),
        GPWDividendExtractor()
    )
    gpw_stock_market_info_extractor = GPWStockMarketInfoExtractor(gpw_company_extractor)
    companies = gpw_stock_market_info_extractor.extract(conf_properties.get_url())
    print("found")
