from datetime import datetime, timedelta


def format_to_stock_date(year, month, day):
    return "{}.{:02d}.{:02d}".format(year, month, day)


def get_today_stock_date_format() {
    now = datetime.now()
    return format_to_stock_date(now.year, now.month, now.day)
}


def calculate_start_date(days_to_subtract):
    """
        Calculates when did it start to keep increasing,
        If today is 2020.04.10 and you pass 3 to this function,
        It returns "2020.04.07"
    """
    d = datetime.today() - timedelta(days=days_to_subtract)
    return format_to_stock_date(d)