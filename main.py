import json
from pprint import pprint

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from decimal import Decimal
import datetime

from fastapi.templating import Jinja2Templates
from typing import List, Union, Optional, Dict, OrderedDict
import parse
from collections import OrderedDict as OrdDict
from open_meteo import open_meteo_simple

from models import Forecast


def get_forecast(lat: Decimal = 56.33, lon: Decimal = 44, days: int = 10):
    forecasts_dict = open_meteo_simple.get_forecast(lat, lon)['hourly']  # from open-meteo
    # forecasts_dict_noaa = parse.parse(latitude=lat, longitude=lon, data_keys=['hpblsfc'], forecast_days=days)  # from NOAA
    forecasts = OrdDict()

    # TODO: How to get a variable by keyword? Dictionary, Enum, NamedTuple, getattr or new dataclass {name, key, value}
    for (dt_str, temperature, temperature_80m, temperature_120m, wind_direction, wind_speed, wind_gusts,
         cloud_cover, cloud_cover_low, precipitation, precipitation_probability, weather_code, pbl_height, is_day) in zip(
            forecasts_dict['time'], forecasts_dict["temperature_2m"], forecasts_dict['temperature_80m'],
            forecasts_dict['temperature_120m'], forecasts_dict["wind_direction_10m"], forecasts_dict["wind_speed_10m"],
            forecasts_dict['wind_gusts_10m'], forecasts_dict['cloud_cover'], forecasts_dict['cloud_cover_low'],
            forecasts_dict['precipitation'], forecasts_dict['precipitation_probability'], forecasts_dict['weather_code'],
            forecasts_dict['boundary_layer_height'], forecasts_dict['is_day']):
        dt_dt = datetime.datetime.fromisoformat(dt_str)

        forecast = Forecast(date=dt_dt.date(), time=dt_dt.time(), temperature=temperature, temperature_80m=temperature_80m,
                            temperature_120m=temperature_120m, wind_direction=wind_direction,
                            wind_speed=round(wind_speed, 1) if wind_speed else wind_speed, wind_gusts=wind_gusts,
                            cloud_cover=cloud_cover, cloud_cover_low=cloud_cover_low, precipitation=precipitation,
                            precipitation_probability=precipitation_probability, weather_code=str(weather_code), pbl_height=pbl_height, is_day=is_day)

        forecasts[dt_dt] = forecast

    # for dt_str, pbl_thickness in zip(forecasts_dict_noaa['time'], forecasts_dict_noaa['hpblsfc']):
    #     dt_dt = datetime.datetime.fromisoformat(dt_str)
    #     if dt_dt in forecasts:
    #         forecasts[dt_dt].pbl_thickness = pbl_thickness

    return forecasts


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def get_root(request: Request, lat: Decimal = 56.33, lon: Decimal = 44):
    forecasts = get_forecast(lat, lon)
    with open('static/descriptions.json') as descr_json:
        descriptions = json.load(descr_json)

    return templates.TemplateResponse(request=request, name='index.html',
                                      context={'forecasts': forecasts, 'descriptions': descriptions})


@app.get('/api/')
def get_api():
    return RedirectResponse('/api/v1/forecast')


@app.get('/api/forecast')
def get_api_forecast():
    return RedirectResponse('/api/v1/forecast')


@app.get('/api/v1/forecast', response_class=JSONResponse)
def get_api_v1(lat: Decimal, lon: Decimal, keywords: List[str] = Query(default=['tmp2m']), levels: List[int] = Query(default=[1000])):
    # forecast = parse.parse(latitude=lat, longitude=lon, utc_offset=utc_offset, data_keys=keyword, levels=lev, forecast_days=days)
    forecast = open_meteo_simple.get_forecast(lat, lon)
    return forecast


if __name__ == '__main__':
    pprint(get_forecast())
