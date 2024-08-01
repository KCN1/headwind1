from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from decimal import Decimal
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List


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
    forecast_list: List[Forecast] = []


forecast1 = Forecast(temperature=20)
forecast1.precipitation = Decimal('1.0')
forecasts = [forecast1]

app = FastAPI()

my_templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
    return my_templates.TemplateResponse(request=request, name='index.html', context={'forecasts': forecasts})


@app.get('/api/')
def get_api():
    return RedirectResponse('/api/v1/')


@app.get('/api/v1/', response_class=JSONResponse)
def get_api_v1():
    return forecasts
