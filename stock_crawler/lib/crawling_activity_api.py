import requests

CRAWLING_ACTIVITY_API_URL = "http://52.78.84.79:8888/api/crawleractivity/"


CA_CRAWLING_START = "Start to crawling / type: {0} min_daily_increase_per: {1} avg_trading_volumn: {2} min_stock_price: {3} max_stock_price: {4}"
CA_START_TO_FETCH_KOSPI_LIST = "Start to fetch Kospi list."
CA_FETCH_KOSPI_LIST_DONE = "Kospi crawling done."
CA_START_TO_FETCH_KOSDAQ_LIST = "Start to fetch kosdaq list."
CA_FETCH_KOSDAQ_LIST_DONE = "Kosdaq crawling done."
CA_START_TO_VALIDATE_KOSPI = "Start to validate Kospi list."
CA_VALIDATE_KOSPI_DONE = "Kospi validation done."
CA_START_TO_VALIDATE_KOSDAQ = "Start to validate Kosdaq list."
CA_VALIDATE_KOSDAQ_DONE = "Kosdaq validation done."
CA_CRAWLING_DONE = "Crawling done."
CA_ERROR = "Occur an error / {}"


def log_activity(worker_id, activity):
    """
        Insert an activity to database
        returns True it requested successfully otherwise returns False
    """
    print("log:{}".format(activity))
    data = {"worker_id": worker_id, "activity": activity}

    try:
        res = requests.post(url=CRAWLING_ACTIVITY_API_URL, data=data)
        if res.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
