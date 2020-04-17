from bs4 import BeautifulSoup
from .crawling import get_source_from_url
from .date import get_today_stock_date_format
from .number import str_to_float

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
        html = get_source_from_url(
            DAILY_STOCK_PRICE_URL.format(self.code, page))
        soup = BeautifulSoup(html, "html.parser")
        price_trs = soup.find("table").find_all("tr")[1:]

        daily_stock_price_list = []

        for price_tr in price_trs:
            price_tds = price_tr.find_all("td")

            if len(price_tds) < 7:
                continue

            daily_stock_price_info = {
                "date": price_tds[0].find("span").text.strip(),
                "closing_price": str_to_float(price_tds[1].find("span").text),
                "daily_increase": str_to_float(price_tds[2].find("span").text),
                "market_value": str_to_float(price_tds[3].find("span").text),
                "is_rising": False if price_tds[2].find("img") == None else (
                    True
                    if price_tds[2].find("img")["src"].split("/")[-1].find("up") >= 0
                    else False),
                "high_price": str_to_float(price_tds[4].find("span").text),
                "low_price": str_to_float(price_tds[5].find("span").text),
                "trading_volumn": str_to_float(price_tds[6].find("span").text),
            }
            daily_stock_price_list.append(daily_stock_price_info)

        return daily_stock_price_list

    def calculate_continuous_stock_list(self):
        """
        Calculates a stock list that contains continuous high stocks from today to past,
        then returns the stock list and It has the stock list in a class instance's variable
        named 'continuous_stock_list'.
        """
        page = 1

        continuous_stock_list = []
        loop = True

        while loop:
            daily_stock_prices = self.fetch_daily_stock_prices(page)

            for sp in daily_stock_prices:
                if sp["is_rising"]:
                    continuous_stock_list.append(sp)
                else:
                    loop = False
                    break
            page += 1

        self.continuous_stock_list = continuous_stock_list
        return continuous_stock_list

    def validate_continuous_stock_list(self, min_daily_increase_per, avg_trading_volumn, min_stock_price, max_stock_price, force=False):
        """
            Validate weather the stock list is able to be trust.
            The stock has to be satisfied all of conditions and length of the list has to be greater than 1.
            It uses a continuous_stock_list that made by calculate_continuous_stock_list function,
            If you call this function before call the calculate_continuous_stock_list, It calls calculate_continuous_stock_List function.

            Args:
                min_daily_increase_per: A percentage how much closing price has increased compared to previous closing price. 
                                         Every day, the percentages have to be greater than or equal to this.
                avg_trading_volumn: An average volumn between dates that increasing has to be greater than or equal to this.
                min_stock_price: The stock price of last day has to be greater than or equal to this.
                max_stock_price: The stock price of last day has to be less than or equal to this.
                force: If you don't want to use the continuous_stock_list that made by calculate_continuous_stock_list function before,
                        Set this to True, so then this function calls calculate_continuous_stock_list at first.

            Returns:
                dict: {
                    "validation_result": False,
                    "message": String # Why It failed to validate
                }
                bool: If the stock list has to be validated, It returns True otherwise False.
        """
        try:
            continuous_stock_list = self.continuous_stock_list
            has_init = True
        except AttributeError:
            has_init = False

        if not has_init or force:
            self.calculate_continuous_stock_list()
            continuous_stock_list = self.continuous_stock_list

        def _make_result(validation_result, message):
            return {
                "validation_result": validation_result,
                "message": message
            }

        ct_stock_list_length = len(continuous_stock_list)

        if ct_stock_list_length < 2:
            return _make_result(False, "A length of the stock list less than 2.")

        if continuous_stock_list[0]["closing_price"] < min_stock_price:
            return _make_result(False, "A closing price({:0.1f}) of last of the stock list less than min_stock_price({:0.1f})".format(continuous_stock_list[0]["closing_price"], min_stock_price))
        elif continuous_stock_list[0]["closing_price"] > max_stock_price:
            return _make_result(False, "A closing price({:0.1f}) of last of the stock list greater than max_stock_price({:0.1f})".format(continuous_stock_list[0]["closing_price"], max_stock_price))

        total_trading_volumn = 0

        for sidx in range(ct_stock_list_length-1):
            stock = continuous_stock_list[sidx]
            prev_stock = continuous_stock_list[sidx + 1]

            increased_price = stock["closing_price"] - \
                prev_stock["closing_price"]
            increased_per = increased_price / prev_stock["closing_price"] * 100

            if increased_per < min_daily_increase_per:
                return _make_result(False, "Increased percentage({:0.1f}) less than min_daily_increase_per({:0.1f})".format(increased_per, min_daily_increase_per))

            total_trading_volumn += stock["trading_volumn"]

        total_trading_volumn += continuous_stock_list[ct_stock_list_length -
                                                      1]["trading_volumn"]
        _avg_trading_volumn = (total_trading_volumn / ct_stock_list_length)

        if _avg_trading_volumn < avg_trading_volumn:
            return _make_result(False, "An average of traiding volumn({:0.1f}) less than avg_trading_volumn({:0.1f})".format(_avg_trading_volumn, avg_trading_volumn))

        return _make_result(True, "Success to validate")


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
                        DETAIL_STOCK_BASE_URL, stock_tds[1].find("a")[
                            "href"].strip()
                    ),
                    # 종목코드
                    "code": stock_tds[1].find("a")["href"].split("code=")[-1],
                    "name": stock_tds[1].find("a").text.strip(),  # 종목명
                    # 현재가
                    "current_stock_price": str_to_float(stock_tds[2].text),
                    # 전일비
                    "day_increase": str_to_float(stock_tds[3].find("span").text),
                    # 등락률
                    "fluctuation": str_to_float(stock_tds[4].find("span").text),
                    "trading_volumn": str_to_float(stock_tds[5].text),  # 거래량
                    "bid": str_to_float(stock_tds[6].text),  # 매수호가
                    "ask": str_to_float(stock_tds[7].text),  # 매도호가
                    "amount_buying": str_to_float(stock_tds[8].text),  # 매수총잔량
                    "amount_selling": str_to_float(stock_tds[9].text),  # 매도총잔량
                    "per": str_to_float(stock_tds[10].text),  # PER
                    "roe": str_to_float(stock_tds[11].text),  # ROE
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
