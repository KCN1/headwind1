from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from decimal import Decimal
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List, Union
import parse



class Forecast(BaseModel):
    date: datetime.date = datetime.date(2024, 8, 1)
    time: datetime.time = datetime.time(4, 0).isoformat('minutes')
    temperature: int = 15
    wind_direction: str = 'wsw'
    wind_speed: int = 2
    wind_gusts: int = 4
    precipitation: Decimal = 0.0
    pbl_thickness: Decimal = 0.0


class DailyForecast(BaseModel):
    date: datetime.date = datetime.date(2024, 8, 1)
    forecast_list: Union[List[Forecast], None] = None


forecast1 = Forecast(temperature=20)
forecast1.precipitation = Decimal('1.0')
forecasts = [forecast1]

app = FastAPI()

my_templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
    return my_templates.TemplateResponse(request=request, name='index.html', context={'forecasts': forecasts})


@app.get('/api/forecast')
def get_api():
    return RedirectResponse('/api/v1/forecast')


@app.get('/api/v1/forecast', response_class=JSONResponse)
def get_api_v1(lat: float, lon: float, keyword: List[str] = Query(), lev: List[int] = Query(default=[0]), days: int = 3, utc_offset: int = 3):
    forecast = parse.parse(latitude=lat, longitude=lon, utc_offset=utc_offset, data_keys=keyword, levels=lev, forecast_days=days)
    return forecast
