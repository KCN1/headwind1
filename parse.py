import requests
import datetime

url0 = 'https://nomads.ncep.noaa.gov/dods/gfs_0p25/'
html = requests.get(url0)

last_date = datetime.date.today()
date_key = "gfs" + last_date.strftime('%Y%m%d')

if date_key not in html.text:
    last_date -= datetime.timedelta(days=1)
    date_key = "gfs" + last_date.strftime('%Y%m%d')

url = url0 + date_key + '/'
html = requests.get(url)

for last_time in (18, 12, 6, 0):
    time_key = f'gfs_0p25_' + str(last_time).zfill(2) + 'z'
    if time_key in html.text:
        break

url += time_key + '.ascii'
# query_key = keyword + time_points + levels + coords
query_keys = ['tmpsfc[0:24][584][176]', 'hpblsfc[0:24][585][176]']

forecast_txt = requests.get(url + '?' + ','.join(query_keys)).text

print(forecast_txt)
