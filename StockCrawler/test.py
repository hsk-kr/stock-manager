from lib.crawling import get_source_from_url
from lib.stock_crawler import StockCrawler
from lib.fileio import save_text_to_file

# https://finance.naver.com/item/sise_day.nhn?code=180640&page=2

if __name__ == "__main__":
    sc = StockCrawler()
    t = sc.fetch_kosdaq_list()
    r = t[0].fetch_daily_stock_prices()
    print(r)
    # source = get_source_from_url(t[0].stock_detail_link)
    # save_text_to_file(source)
