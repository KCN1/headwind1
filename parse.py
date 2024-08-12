import datetime
import json
import re
import time

from pprint import pprint
from typing import List, Dict, Union
import requests
from time import sleep
from pydantic import BaseModel, Field
from pydap.client import open_url
from decimal import Decimal

import converter


AVAIL_LEVELS = [1000, 975, 950, 925, 900, 850, 800, 750, 700, 650,
                600, 550, 500, 450, 400, 350, 300, 250, 200, 150,
                100, 70, 50, 40, 30, 20, 15, 10, 7, 5, 3, 2, 1,
                Decimal('0.7'), Decimal('0.4'), Decimal('0.2'),
                Decimal('0.1'), Decimal('0.07'), Decimal('0.04'),
                Decimal('0.02'), Decimal('0.01')]

URL0 = 'https://nomads.ncep.noaa.gov/dods/gfs_0p25/'
URL1 = r"http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs\d{8}"
URL2 = r"http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs\d{8}/gfs_0p25_\d{2}z.info"


def get_dataset_url():
    html = requests.get(URL0)
    urls = re.findall(URL1, html.text)
    assert len(urls) == 10, f'Something is wrong on date selection page: {html.text}'
    url = urls[-1]
    assert url == max(urls), f'Last date is not last in the list: {urls}'
    html = requests.get(url)
    urls1 = re.findall(URL2, html.text)
    if not urls1:
        url = urls[-2]
        html = requests.get(url)
        urls1 = re.findall(URL2, html.text)
    assert urls1, f'Something wrong on time selection page: {html.text}'
    url = urls1[-1]
    assert url == max(urls1), f'Last time is not last in the list: {urls1}'
    return url[:-5]  # cut '.info'


def get_value_as_decimal(data_key):
    def func(x):
        return Decimal.from_float(float(getattr(converter, data_key)(x))).quantize(Decimal('1.0'))
    return func


def get_value_as_float(data_key):
    def func(x):
        return round(float(getattr(converter, data_key)(x)), 1)
    return func


def get_time_as_datetime(utc_offset=0):
    def func(d):
        return converter.time(d) + datetime.timedelta(hours=utc_offset)
    return func


def get_time_as_str(utc_offset=0):
    def func(d):
        return (converter.time(d) + datetime.timedelta(hours=utc_offset)).isoformat(sep=' ', timespec='minutes')
    return func


def get_data(data_arr, utc_offset):
    time_vals = list(map(get_time_as_str(utc_offset=utc_offset), data_arr.time.data))
    data_vals = list(map(get_value_as_float(data_arr.name), getattr(data_arr, data_arr.name).data))
    return time_vals, data_vals


def parse(latitude, longitude, data_keys, levels, forecast_days=3, utc_offset=0):
    lat_index = round(latitude * 4) + 360
    lon_index = (round(longitude * 4) + 1440) % 1440
    lev_indices = [AVAIL_LEVELS.index(min(AVAIL_LEVELS, key=lambda x: abs(x - lev))) for lev in levels]
    lev_indices_int = list(filter(lambda x: x <= 32, lev_indices))
    url = get_dataset_url()
    pydap_dataset = open_url(url)
    with open('cache_parse.json', 'r') as cache_fp:
        cached_forecast = json.load(cache_fp)
    for keyword in ['url', 'lat_index', 'lon_index', 'forecast_days', 'forecast']:
        cached_forecast.setdefault(keyword, None)
    if (url, lat_index, lon_index, forecast_days) == tuple(map(cached_forecast.get, ['url', 'lat_index', 'lon_index',
                                                                                     'forecast_days'])):
        forecast = cached_forecast['forecast']
    else:
        forecast = {}
    for data_key in data_keys:
        dataset = pydap_dataset[data_key]
        if len(dataset.shape) == 4:
            for lev_index in lev_indices_int:
                data_single_level = {}
                if data_key not in forecast or f'{AVAIL_LEVELS[lev_index]}mb' not in forecast[data_key]:
                    sleep(1)
                    data_arr = dataset[0:8 * forecast_days, lev_index, lat_index, lon_index]  # HERE COMES THE DATA!
                    time_vals, data_vals = get_data(data_arr, utc_offset)
                    forecast.setdefault('time', time_vals)
                    assert forecast['time'][0] == time_vals[0]
                    data_single_level[f'{AVAIL_LEVELS[lev_index]}mb'] = data_vals
                    forecast.setdefault(data_key, {}).update(data_single_level)
        elif len(dataset.shape) == 3:
            if data_key not in forecast:
                sleep(1)
                data_arr = dataset[0:8 * forecast_days, lat_index, lon_index]  # HERE COMES THE DATA!
                time_vals, data_vals = get_data(data_arr, utc_offset)
                forecast.setdefault('time', time_vals)
                assert forecast['time'][0] == time_vals[0]
                forecast[data_key] = data_vals
        else:
            raise ValueError(f'Number of data columns {dataset.shape=} should be either 3 or 4.')
    cached_forecast = {'url': url, 'lat_index': lat_index, 'lon_index': lon_index,
                       'forecast_days': forecast_days, 'forecast': forecast}
    with open('cache_parse.json', 'w') as cache_fp:
        json.dump(cached_forecast, cache_fp)
    return {data_key: cached_forecast['forecast'][data_key] for data_key in data_keys+['time']}
    # TODO: Unify datasets for leveled and single-level data; new keywords for calculated data: gradient, wind etc.
    # TODO: JSON cache for each coordinate set; shorter forecasts from longer cache; 'touch cache_latlon.json'


def main():

    latitude = 56.33
    longitude = 44
    utc_offset = 3

    data_keys = ['prateavesfc', 'tmp80m', 'tmp2m', 'tmpprs', 'hpblsfc']
    levels = [950, 900]
    forecast_days = 3
    t0 = time.perf_counter()
    forecast = parse(latitude, longitude, data_keys, levels, forecast_days, utc_offset)
    t1 = time.perf_counter()
    pprint(forecast)
    print(t1 - t0)


if __name__ == '__main__':
    main()
