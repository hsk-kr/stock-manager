from bs4 import BeautifulSoup
from .crawling import get_source_from_url

KOSPI_SISE_RISE_URL = "https://finance.naver.com/sise/sise_rise.nhn?sosok=0"
KOSDAQ_SISE_RISE_URL = "https://finance.naver.com/sise/sise_rise.nhn?sosok=1"
DETAIL_STOCK_BASE_URL = "https://finance.naver.com"


class StockCrawler:
    def __init__(self):
        self.soup = None

    def _fetch_stock_list(self, url):
        html = get_source_from_url(url)
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")

        if len(tables) == 2:
            stock_trs = tables[1].find_all("tr")[1:]

            stock_info_list = []

            for stock_tr in stock_trs:
                stock_tds = stock_tr.find_all("td")

                if len(stock_tds) < 12:
                    continue

                stock_info = {
                    "링크": "{0}{1}".format(
                        DETAIL_STOCK_BASE_URL, stock_tds[1].find("a")["href"].strip()
                    )
                    if stock_tds[1].find("a")
                    else "",
                    "종목명": stock_tds[1].find("a").text.strip(),
                    "현재가": stock_tds[2].text.strip(),
                    "전일비": stock_tds[3].find("span").text.strip(),
                    "등락률": stock_tds[4].find("span").text.strip(),
                    "거래량": stock_tds[5].text.strip(),
                    "매수호가": stock_tds[6].text.strip(),
                    "매도호가": stock_tds[7].text.strip(),
                    "매수총잔량": stock_tds[8].text.strip(),
                    "매도총잔량": stock_tds[9].text.strip(),
                    "PER": stock_tds[10].text.strip(),
                    "ROE": stock_tds[11].text.strip(),
                }

                stock_info_list.append(stock_info)

            return stock_info_list
        else:
            return None

    def fetch_kospi_list(self):
        return self._fetch_stock_list(KOSPI_SISE_RISE_URL)

    def fetch_kosdaq_list(self):
        return self._fetch_stock_list(KOSDAQ_SISE_RISE_URL)
