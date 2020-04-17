from lib.crawling import get_source_from_url
from lib.stock_crawler import StockCrawler
from lib.fileio import save_text_to_file

# https://finance.naver.com/item/sise_day.nhn?code=180640&page=2

if __name__ == "__main__":
    sc = StockCrawler()
    kospi_list = sc.fetch_kospi_list()
    kosdaq_list = sc.fetch_kosdaq_list()

    rst_log = ""

    for stock in kospi_list:
        val_rst = stock.validate_continuous_stock_list(2, 300000, 3000, 100000)
        rst_log += "{}\t{}\t{}\r\n".format("True" if val_rst["validation_result"]
                                           else "False", val_rst["message"], stock.stock_detail_link)

    save_text_to_file(rst_log)
    # source = get_source_from_url(t[0].stock_detail_link)
    # save_text_to_file(source)
