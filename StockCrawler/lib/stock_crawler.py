from bs4 import BeautifulSoup
from .crawling import get_source_from_url
from .date import get_today_stock_date_format, calculate_start_date

KOSPI_SISE_RISE_URL = "https://finance.naver.com/sise/sise_rise.nhn?sosok=0"
KOSDAQ_SISE_RISE_URL = "https://finance.naver.com/sise/sise_rise.nhn?sosok=1"
DETAIL_STOCK_BASE_URL = "https://finance.naver.com"
DAILY_STOCK_PRICE_URL = "https://finance.naver.com/item/sise_day.nhn?code={0}&page={1}"


class StockInfo:
    def __init__(
        self,
        stock_detail_link="",
        code="",
        name="",
        current_stock_price="",
        day_increase="",
        fluctuation="",
        trading_volumn="",
        bid="",
        ask="",
        amount_buying="",
        amount_selling="",
        per="",
        roe="",
        obj=None,
    ):
        """
            Choose passing params or passing an obj. obj have to have all of params itself.
        """
        if obj:
            self.stock_detail_link = obj["stock_detail_link"]
            self.code = obj["code"]
            self.name = obj["name"]
            self.current_stock_price = obj["current_stock_price"]
            self.day_increase = obj["day_increase"]
            self.fluctuation = obj["fluctuation"]
            self.trading_volumn = obj["trading_volumn"]
            self.bid = obj["bid"]
            self.ask = obj["ask"]
            self.amount_buying = obj["amount_buying"]
            self.amount_selling = obj["amount_selling"]
            self.per = obj["per"]
            self.roe = obj["roe"]
        else:
            self.stock_detail_link = stock_detail_link
            self.code = code
            self.name = name
            self.current_stock_price = current_stock_price
            self.day_increase = day_increase
            self.fluctuation = fluctuation
            self.trading_volumn = trading_volumn
            self.bid = bid
            self.ask = ask
            self.amount_buying = amount_buying
            self.amount_selling = amount_selling
            self.per = per
            self.roe = roe

    def fetch_daily_stock_prices(self, page=1):
        """
            Fetch daily stock prices information from the web stock detail page
            and returns dictionary list.
        """
        html = get_source_from_url(DAILY_STOCK_PRICE_URL.format(self.code, page))
        soup = BeautifulSoup(html, "html.parser")
        price_trs = soup.find("table").find_all("tr")[1:]

        daily_stock_price_list = []

        for price_tr in price_trs:
            price_tds = price_tr.find_all("td")

            if len(price_tds) < 7:
                continue

            daily_stock_price_info = {
                "date": price_tds[0].find("span").text.strip(),
                "closing_price": price_tds[1].find("span").text.strip(),
                "daily_increase": price_tds[2].find("span").text.strip(),
                "market_value": price_tds[3].find("span").text.strip(),
                "rising_falling_type": "rising"
                if price_tds[2].find("img")["alt"] == "상승"
                else "하락",
                "high_price": price_tds[4].find("span").text.strip(),
                "low_price": price_tds[5].find("span").text.strip(),
                "trading_volumn": price_tds[6].find("span").text.strip(),
            }
            daily_stock_price_list.append(daily_stock_price_info)

        return daily_stock_price_list

    def calculate_continous_stock_list(self):
        """
        Calculates a stock list that contains continuous high stocks from today to past,
        then returns the stock list 
        """
        page = 1

        # TODO: Keep working!
        while True:
            daily_stock_prices = self.fetch_daily_stock_prices(page)



class StockCrawler:
    def __init__(self):
        self.soup = None

    def _fetch_stock_list(self, url):
        """
            Fetch the StockInfo list from url(KOSPI | KOSDAQ).
        """
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

                temp_obj_for_stock_info = {
                    "stock_detail_link": "{0}{1}".format(
                        DETAIL_STOCK_BASE_URL, stock_tds[1].find("a")["href"].strip()
                    ),
                    "code": stock_tds[1].find("a")["href"].split("code=")[-1],  # 종목코드
                    "name": stock_tds[1].find("a").text.strip(),  # 종목명
                    "current_stock_price": stock_tds[2].text.strip(),  # 현재가
                    "day_increase": stock_tds[3].find("span").text.strip(),  # 전일비
                    "fluctuation": stock_tds[4].find("span").text.strip(),  # 등락률
                    "trading_volumn": stock_tds[5].text.strip(),  # 거래량
                    "bid": stock_tds[6].text.strip(),  # 매수호가
                    "ask": stock_tds[7].text.strip(),  # 매도호가
                    "amount_buying": stock_tds[8].text.strip(),  # 매수총잔량
                    "amount_selling": stock_tds[9].text.strip(),  # 매도총잔량
                    "per": stock_tds[10].text.strip(),  # PER
                    "roe": stock_tds[11].text.strip(),  # ROE
                }

                stock_info = StockInfo(obj=temp_obj_for_stock_info)
                stock_info_list.append(stock_info)

            return stock_info_list
        else:
            return None

    def fetch_kospi_list(self):
        """
            Returns the StockInfo list of KOSPI
        """
        return self._fetch_stock_list(KOSPI_SISE_RISE_URL)

    def fetch_kosdaq_list(self):
        """
            Returns the StockInfo list of KOSDAQ
        """
        return self._fetch_stock_list(KOSDAQ_SISE_RISE_URL)
