import requests


def get_source_from_url(url, encoding="euc-kr"):
    res = requests.get(url)
    res.encoding = encoding
    return res.text
