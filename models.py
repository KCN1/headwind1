from decimal import Decimal
import datetime
from pydantic import BaseModel

from typing import List, Union, Optional, Dict, OrderedDict


class Forecast(BaseModel):
    date: Union[datetime.date, str] = datetime.date(2024, 8, 1)
    time: Union[datetime.time, str] = datetime.time(4, 0)
    temperature: Optional[Decimal] = None
    temperature_80m: Optional[Decimal] = None
    temperature_120m: Optional[Decimal] = None
    temperature_180m: Optional[Decimal] = None
    wind_direction: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    wind_gusts: Optional[Decimal] = None
    cloud_cover: Optional[Decimal] = None
    cloud_cover_low: Optional[Decimal] = None
    precipitation: Optional[Decimal] = None
    precipitation_probability: Optional[Decimal] = None
    pbl_height: Optional[Decimal] = None
    cape: Optional[Decimal] = None
    weather_code: Optional[Union[int, str]] = None
    is_day: Optional[bool] = None


class HourlyForecast(BaseModel):
    temperature: Optional[Decimal] = None
    wind_direction: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    wind_gusts: Optional[Decimal] = None
    cloud_cover: Optional[Decimal] = None
    cloud_cover_low: Optional[Decimal] = None
    precipitation: Optional[Decimal] = None
    pbl_thickness: Optional[Decimal] = None


class DailyForecast(BaseModel):
    # date: datetime.date = datetime.date(2024, 9, 1)
    forecast_list: Optional[OrderedDict[datetime.time, HourlyForecast]] = None


class NewForecast(BaseModel):
    daily_forecast_list: Optional[OrderedDict[datetime.date, DailyForecast]] = None
    # TODO: {date: {time: HourlyForecast}}
    # TODO: Unified Enum or dictionary of keywords for each source, model and level

