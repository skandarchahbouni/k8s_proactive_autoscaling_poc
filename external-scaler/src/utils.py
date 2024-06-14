import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ----- Functions
def fetch_prometheus_data(
    prometheus_url: str, query: str, start_time: str, end_time: str, step: str
) -> list | None:
    try:
        params = {"query": query, "start": start_time, "end": end_time, "step": step}
        response = requests.get(prometheus_url + "/api/v1/query_range", params=params)
        if response.status_code == 200:
            resp = response.json()
            return resp.get("data").get("result")[0].get("values")
        else:
            logging.error(
                f"Failed to fetch data from Prometheus. Status code: {response.status_code}"
            )
            return None
    except requests.exceptions.ConnectionError:
        logging.error("A connection error occurred. [fetch_prometheus_data function]")
    except requests.exceptions.Timeout:
        logging.error("The request timed out. [fetch_prometheus_data function]")
    except requests.exceptions.HTTPError as _:
        logging.error("HTTP Error. [fetch_prometheus_data function]")
    except requests.exceptions.RequestException as _:
        logging.error("An error occurred. [fetch_prometheus_data function]")
    except IndexError:
        logging.error("IndexError [fetch_prometheus_data function]")
    except KeyError:
        logging.error("KeyError [fetch_prometheus_data function]")
    except Exception:
        logging.error("Exception [fetch_prometheus_data function]")
    return None


def convert_to_dataframe(data: list) -> pd.DataFrame:
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["timespmp", "value"])
    # Convert 'timespmp' column to datetime
    df["timespmp"] = pd.to_datetime(df["timespmp"], unit="s")
    # Convert 'value' column to float
    df["value"] = df["value"].astype(float)
    # Set 'timespmp' column as index
    df.set_index("timespmp", inplace=True)
    return df


def get_closest_three_minutes_ago_value(
    df: pd.DataFrame, period: int, step: str
) -> float:
    # Futur time
    fiteen_seconds_later = datetime.now() + timedelta(seconds=int(step[:-1]))
    # Subtract 3 minutes
    three_minutes_ago = fiteen_seconds_later - timedelta(minutes=period)
    # Convert to pandas Timestamp object
    three_minutes_ago_pandas = pd.Timestamp(three_minutes_ago)
    # Query the closest datetime index value
    iloc_idx = df.index.get_indexer([three_minutes_ago_pandas], method="nearest")[0]
    value = df.iloc[iloc_idx]["value"]
    return value


def simulate_prediction(prometheus_url: str, query: str, period: int, step: str) -> int:
    current_time = datetime.now(timezone.utc)
    three_minutes_ago = current_time - timedelta(minutes=period)
    current_time_formatted = current_time.strftime("%Y-%m-%dT%H:%M:%S.00Z")
    three_minutes_ago_formatted = three_minutes_ago.strftime("%Y-%m-%dT%H:%M:%S.00Z")
    data = fetch_prometheus_data(
        prometheus_url=prometheus_url,
        query=query,
        start_time=three_minutes_ago_formatted,
        end_time=current_time_formatted,
        step=step,
    )
    if not data:
        return
    # convert to dataframe
    df = convert_to_dataframe(data)
    # simulate prediction
    value = get_closest_three_minutes_ago_value(df=df, period=period, step=step)
    return int(value)


# -------- just for testing
# if __name__ == "__main__":
#     prometheus_url = "http://localhost:9090"
#     query = "sum(rate(python_request_operations_total[1m]))"
#     period = 3
#     step = "15s"

#     # try:
#     #     predicted_value = simulate_prediction(
#     #         prometheus_url=prometheus_url, query=query, period=period, step=step
#     #     )
#     # except Exception as _:
#     #     print("Exception")

#     predicted_value = simulate_prediction(
#         prometheus_url=prometheus_url, query=query, period=period, step=step
#     )
