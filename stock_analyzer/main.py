import sys
from lib.stock_api import fetch_not_analyzed_data, analyze_data, push_analyzed_data_to_server

if __name__ == "__main__":
    data = fetch_not_analyzed_data()
    if data == None:
        print("Failed to execute fetch_not_anaylzed_data().")
        sys.exit(0)

    data = analyze_data(data)
    rst = push_analyzed_data_to_server(data)

    if rst:
        print("Success to push analayzed data to the server.")
    else:
        print("Failed to push analyzed data to the server.")
