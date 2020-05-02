from lib.stock_api import fetch_not_analyzed_data, analyze_data, push_analyzed_data_to_server

if __name__ == "__main__":
    data = fetch_not_analyzed_data()
    data = analyze_data(data)
    rst = push_analyzed_data_to_server(data)
    print(rst)
