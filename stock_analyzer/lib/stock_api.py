import requests

API_URL_NOT_ANALYZED_DATA = "http://52.78.84.79:8888/api/notanalyzeddata/"
API_URL_ANALYZED_DATA = "http://52.78.84.79:8888/api/analyzeddata/"


def fetch_not_analyzed_data():
    """
    Returns not analyzed data if it occurs an error returns None
    """
    api_res = requests.get(API_URL_NOT_ANALYZED_DATA)
    if api_res.status_code != 200:
        return None

    return api_res.json()


def analyze_data(data):
    """
    Returns analyzed data[{stock_id, continuous_days, last_flutuation}] from not analyzed data
    formatted that [{
      id,
      name,
      code,
      stock_type,
      stock_detail_link,
      current_stock_price,
      day_increase,
      fluctuation,
      bid,
      ask,
      amount_buying,
      amount_selling,
      continuous_stock_list,
      validation_result,
      validation_message,
      created_at,
      worker_id
    }]
    """
    analyzed_data = []

    for stock in data:
        if not stock["validation_result"]:
            continue

        analyzed_data.append({
            "stock_id": stock["id"],
            "last_fluctuation": stock["fluctuation"],
            "continuous_days": len(stock["continuous_stock_list"])
        })

    return analyzed_data


def push_analyzed_data_to_server(data):
    """
        requests the API that to insert data to db
        returns True if it's called API successfully otherwise returns False

        Args :
          - data (list): analyed data by analyze_data function
    """
    api_res = requests.post(
        API_URL_ANALYZED_DATA, json=data, headers={"Content-Type": "application/json"})
    return api_res.status_code
