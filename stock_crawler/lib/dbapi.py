import requests

STOCK_API_URL = "http://52.78.84.79:8888/api/stock/"


def insert_stock(work_uuid, stock_type, stockinfo, continuous_stock_list, validation_result, validation_message):
    """
        Request an API to insert Stock Information to database
        returns True if it's executed successfully otherwise returns False

        Args:
            work_uuid (str): work uuid
            stock_type (str): kospia | kosdaq
            stockinfo (StockInfo)
            continuous_stock_list (list): calculated by StockInfo class
            validation_result (boolean): result of the validate_continuous_stock_list method
            validation_message (string): message of the validate_continuous_stock_list method
    """
    data = {
        "work_uuid": work_uuid,
        "name": stockinfo["name"],
        "code": stockinfo["code"],
        "stock_type": stock_type,
        "stock_detail_link": stockinfo["stock_detail_link"],
        "current_stock_price": stockinfo["current_stock_price"],
        "day_increase": stockinfo["day_increase"],
        "fluctuation": stockinfo["fluctuation"],
        "trading_volumn": stockinfo["trading_volumn"],
        "bid": stockinfo["bid"],
        "ask": stockinfo["ask"],
        "amount_buying": stockinfo["amount_buying"],
        "amount_selling": stockinfo["amount_selling"],
        "per": stockinfo["per"],
        "roe": stockinfo["roe"],
        "continuous_stock_list": continuous_stock_list,
        "validation_result": validation_result,
        "validation_message": validation_message,
    }

    try:
        res = requests.post(url=STOCK_API_URL, data=data)
        if res.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
