def str_to_float(str_num):
    if str_num == "N/A":
        return 0
    return float(str_num.replace(",", "").replace("%", ""))
