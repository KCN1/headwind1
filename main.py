import json
from pprint import pprint

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from decimal import Decimal
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List, Union, Optional, Dict, OrderedDict
import parse
from collections import OrderedDict as ordered_dict
from open_meteo import open_meteo_simple


class Forecast(BaseModel):
    date: Union[datetime.date, str] = datetime.date(2024, 8, 1)
    time: Union[datetime.time, str] = datetime.time(4, 0)
    temperature: Optional[Decimal] = None
    wind_direction: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    wind_gusts: Optional[Decimal] = None
    precipitation: Optional[Decimal] = None
    pbl_thickness: Optional[Decimal] = None


class HourlyForecast(BaseModel):
    temperature: Optional[Decimal] = None
    wind_direction: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    wind_gusts: Optional[Decimal] = None
    precipitation: Optional[Decimal] = None
    pbl_thickness: Optional[Decimal] = None


class DailyForecast(BaseModel):
    # date: datetime.date = datetime.date(2024, 9, 1)
    forecast_list: Optional[OrderedDict[datetime.time, HourlyForecast]] = None


class NewForecast(BaseModel):
    daily_forecast_list: Optional[OrderedDict[datetime.date, DailyForecast]] = None
    # TODO: {date: {time: HourlyForecast}}
    # TODO: Enum of keywords


def get_forecast(lat: Decimal = 56.33, lon: Decimal = 44, days: int = 10):
    forecasts_dict = open_meteo_simple.get_forecast(lat, lon, days)
    forecasts_dict_noaa = parse.parse(latitude=lat, longitude=lon, data_keys=['hpblsfc'], levels=[0], forecast_days=days)
    forecasts = ordered_dict()
    for i, dt in enumerate(forecasts_dict['hourly']['time']):
        dt_dt = datetime.datetime.fromisoformat(dt)
        forecast = Forecast(date=dt_dt.date(), time=dt_dt.time(), temperature=forecasts_dict['hourly']['temperature_2m'][i],
                            wind_direction=forecasts_dict['hourly']["wind_direction_10m"][i], wind_speed=forecasts_dict['hourly']["wind_speed_10m"][i],
                            wind_gusts=forecasts_dict['hourly']['wind_gusts_10m'][i], precipitation=forecasts_dict['hourly']['precipitation'][i])
        if forecast.time.hour % 3 == 0:
            forecasts[dt_dt] = forecast
    for dt, hpblsfc in zip(forecasts_dict_noaa['time'], forecasts_dict_noaa['hpblsfc']):
        dt_dt = datetime.datetime.fromisoformat(dt)
        if dt_dt in forecasts:
            forecasts[dt_dt].pbl_thickness = hpblsfc
    return forecasts


app = FastAPI()

my_templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def get_root(request: Request, lat: Decimal = 56.33, lon: Decimal = 44, days: int = 16):
    forecasts = get_forecast(lat, lon, days)
    return my_templates.TemplateResponse(request=request, name='index.html', context={'forecasts': forecasts})


@app.get('/api/')
def get_api():
    return RedirectResponse('/api/v1/forecast')


@app.get('/api/forecast')
def get_api_forecast():
    return RedirectResponse('/api/v1/forecast')


@app.get('/api/v1/forecast', response_class=JSONResponse)
def get_api_v1(lat: Decimal, lon: Decimal, keywords: List[str] = Query(default=['tmp2m']), levels: List[int] = Query(default=[0]), days: int = 10, utc_offset: int = 3):
    # forecast = parse.parse(latitude=lat, longitude=lon, utc_offset=utc_offset, data_keys=keyword, levels=lev, forecast_days=days)
    forecast = open_meteo_simple.get_forecast(lat, lon, days)
    return forecast


if __name__ == '__main__':
    pprint(get_forecast())
