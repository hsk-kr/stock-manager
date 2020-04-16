from lib.crawling import get_source_from_url
from lib.stock_crawler import StockCrawler
from lib.fileio import save_text_to_file

if __name__ == "__main__":
    sc = StockCrawler()
    t = sc.fetch_kosdaq_list()
    source = get_source_from_url(t[0]["링크"])
    save_text_to_file(source)
