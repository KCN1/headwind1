import datetime
import json
import re
from pprint import pprint
from typing import List, Dict, Union
import requests

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
    assert len(urls) == 10, f'Something is wrong on date selection page: {urls}'
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


def get_data(data_arr):
    for time_val, data_val in zip(data_arr.time.data, getattr(data_arr, data_arr.name).data):
        yield (converter.time(time_val),
               Decimal.from_float(float(getattr(converter, data_arr.name)(data_val))).quantize(Decimal('1.0')))


class Forecast(BaseModel):
    latitude: float
    longitude: float
    levels: List[Decimal]
    forecast_data: Dict[str, Union[List[Decimal], Dict[Decimal, List[Decimal]]]] = Field(default_factory=dict)


def main():

    latitude = 56.33
    longitude = 44
    utc_offset = 3

    data_keys = ['ugrd10m', 'vgrd10m', 'ugrdprs', 'vgrdprs']
    levels = [950, 900]
    forecast_days = 5

    lat_index = round(latitude * 4) + 360
    lon_index = (round(longitude * 4) + 1440) % 1440
    lev_indices = [AVAIL_LEVELS.index(min(AVAIL_LEVELS, key=lambda x: abs(x - lev))) for lev in levels]
    url = get_dataset_url()
    pydap_dataset = open_url(url)
    forecast = {}
    for data_key in data_keys:
        dataset = pydap_dataset[data_key]
        if len(dataset.shape) == 4:
            for lev_index in lev_indices:
                data_arr = dataset[0:8 * forecast_days + 1, lev_index, lat_index, lon_index]  # HERE COMES THE DATA!
                for datime, data_piece in get_data(data_arr):
                    forecast[datime].setdefault(data_key, {}).update({AVAIL_LEVELS[lev_index]: data_piece})
        elif len(dataset.shape) == 3:
            data_arr = dataset[0:8 * forecast_days + 1, lat_index, lon_index]  # HERE COMES THE DATA!
            for datime, data_piece in get_data(data_arr):
                forecast.setdefault(datime, {}).update({data_key: data_piece})
        else:
            raise ValueError(f'Number of data columns dataset.shape = {dataset.shape} should be either 3 or 4.')
    forecast_local = {key + datetime.timedelta(hours=utc_offset): value for key, value in forecast.items()}
    pprint(forecast_local)


if __name__ == '__main__':
    main()
