import sys
import uuid

from lib.crawling import get_source_from_url
from lib.stock_crawler import StockCrawler
from lib.crawling_activity_api import *
from lib.dbapi import insert_stock

# https://finance.naver.com/item/sise_day.nhn?code=180640&page=2

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            "manager.py [kospi|kosdaq|all] [min_daily_increase_per] [avg_trading_volumn] [min_stock_price] [max_stock_price]")
        sys.exit(0)

    try:
        stock_type = sys.argv[1]
        min_daily_increase_per = float(sys.argv[2])
        avg_trading_volumn = float(sys.argv[3])
        min_stock_price = float(sys.argv[4])
        max_stock_price = float(sys.argv[5])
        work_uuid = uuid.uuid4()

        # start crawling
        log_activity(work_uuid, CA_CRAWLING_START.format(
            stock_type, min_daily_increase_per, avg_trading_volumn, min_stock_price, max_stock_price))

        sc = StockCrawler()

        if stock_type == "kospi" or stock_type == "all":
            # fetching Kospi list
            log_activity(work_uuid, CA_START_TO_FETCH_KOSPI_LIST)
            kospi_list = sc.fetch_kospi_list()
            log_activity(work_uuid, CA_FETCH_KOSPI_LIST_DONE)

        if stock_type == "kosdaq" or stock_type == "all":
            # fetching Kosdaq list
            log_activity(work_uuid, CA_START_TO_FETCH_KOSDAQ_LIST)
            kosdaq_list = sc.fetch_kosdaq_list()
            log_activity(work_uuid, CA_FETCH_KOSDAQ_LIST_DONE)

        if stock_type == "kospi" or stock_type == "all":
            # validation Kospi list
            log_activity(work_uuid, CA_START_TO_VALIDATE_KOSPI)
            for stock in kospi_list:
                val_rst = stock.validate_continuous_stock_list(
                    min_daily_increase_per, avg_trading_volumn, min_stock_price, max_stock_price)
                insert_stock(work_uuid, "kospi", stock.get_stock_info_as_dict(
                ), stock.continuous_stock_list, val_rst["result"], val_rst["message"])

            log_activity(work_uuid, CA_VALIDATE_KOSPI_DONE)

        if stock_type == "kosdaq" or stock_type == "all":
            # validation Kospi list
            log_activity(work_uuid, CA_START_TO_VALIDATE_KOSDAQ)
            for stock in kosdaq_list:
                val_rst = stock.validate_continuous_stock_list(
                    min_daily_increase_per, avg_trading_volumn, min_stock_price, max_stock_price)
                insert_stock("kosdaq", stock.get_stock_info_as_dict(
                ), stock.continuous_stock_list, val_rst["result"], val_rst["message"])

            log_activity(work_uuid, CA_VALIDATE_KOSDAQ_DONE)

        log_activity(work_uuid, CA_CRAWLING_DONE)
    except Exception as e:
        log_activity(work_uuid, CA_ERROR.format(e))
