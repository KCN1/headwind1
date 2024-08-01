import requests
import datetime
from pydap.client import open_url


def get_dataset_url():
    url0 = 'https://nomads.ncep.noaa.gov/dods/gfs_0p25/'
    html = requests.get(url0)

    last_date = datetime.date.today()
    date_path = "gfs" + last_date.strftime('%Y%m%d')

    if date_path not in html.text:
        last_date -= datetime.timedelta(days=1)
        date_path = "gfs" + last_date.strftime('%Y%m%d')
    if date_path not in html.text:
        last_date -= datetime.timedelta(days=1)
        date_path = "gfs" + last_date.strftime('%Y%m%d')

    url = url0 + date_path + '/'
    html = requests.get(url)

    for last_hour in (18, 12, 6, 0):
        time_path = 'gfs_0p25_' + str(last_hour).zfill(2) + 'z'
        if time_path + ':' in html.text:
            break
    # last_time = datetime.time(hour=last_hour)
    url += time_path
    return url


dataset_url = get_dataset_url()
print(dataset_url)
pydap_ds = open_url(dataset_url)

temperatures_ds = pydap_ds['tmp2m']

latitude = 56.33
longitude = 44

lat_index = round(latitude * 4) + 360
lon_index = (round(longitude * 4) + 1440) % 1440
forecast_days = 5

temperatures_arr = temperatures_ds[0:8*forecast_days, lat_index, lon_index]
temperatures_raw = [(dt, temp[0][0]) for (dt, temp) in zip(temperatures_arr.data[1], temperatures_arr.data[0])]
temperatures = [(datetime.date(2024, 8, 1) + datetime.timedelta(days=int(d-739100)),
                 datetime.time(hour=round(24 * (d % 1))), round(temp - 273.15, 1)) for (d, temp) in temperatures_raw]

for dt_temp in temperatures:
    print(*dt_temp)
