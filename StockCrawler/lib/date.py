from datetime import datetime, timedelta


def format_to_stock_date(year, month, day):
    return "{}.{:02d}.{:02d}".format(year, month, day)


def get_today_stock_date_format():
    now = datetime.now()
    return format_to_stock_date(now.year, now.month, now.day)
