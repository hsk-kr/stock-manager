import requests, traceback

WORKER_API_URL = "http://52.78.84.79:8888/api/worker/"


def req_create_worker():
    """
        Request the create worker API and then returns worker primary key.
        It used for request other APIs. (crawling_activity_api, db_api, etc.)
        If it get an error, returns None
    """
    try:
        res = requests.post(WORKER_API_URL)
    except:
        traceback.print_exc()
        return None

    if res.status_code == 201:
        return res.json()["id"]
        return None
    else:
        return None

        # return res.json()
