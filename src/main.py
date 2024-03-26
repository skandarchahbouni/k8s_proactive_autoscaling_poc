import requests
import pandas as pd


def fetch_prometheus_data(prometheus_url, query, start_time, end_time, step):
    try:
        params = {"query": query, "start": start_time, "end": end_time, "step": step}
        response = requests.get(prometheus_url + "/api/v1/query_range", params=params)
        if response.status_code == 200:
            resp = response.json()
            return resp.get("data").get("result")[0].get("values")
        else:
            print(
                f"Failed to fetch data from Prometheus. Status code: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from Prometheus: {e}")
        return None


# Replace 'http://localhost:9090' with your Prometheus server URL
prometheus_url = "http://localhost:9090"
query = "rate(python_request_operations_total[1m])"
start_time = "2024-03-23T10:42:56.00Z"
end_time = "2024-03-23T10:51:28.00Z"
step = "15s"

data = fetch_prometheus_data(prometheus_url, query, start_time, end_time, step)

if data:
    values = data.get("data").get("result")[0].get("values")
    df = pd.DataFrame(data, columns=["timespmp", "value"])
    print(df)
else:
    print("Failed to fetch data from Prometheus.")
