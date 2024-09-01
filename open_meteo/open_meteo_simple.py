import time
from decimal import Decimal
from pprint import pprint
import requests
import requests_cache
from retry_requests import retry


def get_forecast(latitude: Decimal = 56.33, longitude: Decimal = 44, days: int = 10):
    cache_session = requests_cache.CachedSession('.cache_simple', expire_after=3600)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": days,
        "wind_speed_unit": "ms",
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m", "wind_speed_100m",
                   "wind_direction_10m", "wind_direction_100m", "cape", "windspeed_925hPa", "windspeed_850hPa",
                   "winddirection_925hPa", "winddirection_850hPa", "wind_gusts_10m", "cloud_cover", "cloud_cover_low"],
        "models": ["gfs_global"] # "gfs_global" up to 16 days, "ecmwf_ifs025" up to 10 days
    }
    responses = cache_session.get(url, params=params)
    return responses.json()  # responses.json() извлекает JSON-данные из объекта Response и возвращает в виде словаря
    # TODO: Handle different keywords for different models and levels.
    # TODO: Enum of keywords.


if __name__ == '__main__':
    t0 = time.perf_counter()
    forecast = get_forecast()
    pprint(forecast)
    t1 = time.perf_counter()
    print(f'{t1 - t0:.3f}')
