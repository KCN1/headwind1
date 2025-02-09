import csv
import json
from time import sleep
from decimal import Decimal
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from urllib.request import urlretrieve


def stable(lat: Decimal = 56, lon: Decimal = 44):
    my_options = Options()
    my_options.page_load_strategy = 'none'
    my_options.add_argument("--headless")
    browser = webdriver.Chrome(options=my_options)
    try:
        browser.get('https://www.ready.noaa.gov/READYcmet.php')
        sleep(1)
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.NAME, "Lat"))).send_keys(lat)
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.NAME, "Lon"))).send_keys(lon)
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                "input[type='submit'][title='Continue'][value='Continue']"))).click()
        sleep(1)
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "table.jobGrid>tbody>tr:nth-child(7) select"))).click()
        sleep(1)
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                             "table.jobGrid>tbody>tr:nth-child(7) select>option[value='GFS0p25|GFS0p25']"))).click()  # main stability from 0.25 deg GFS
        # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                      "table.jobGrid>tbody>tr:nth-child(7) select>option[value='GFS|GFS']"))).click() # longer time range stability from 1 deg GFS
        sleep(1)
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    "table.jobGrid>tbody>tr:nth-child(7) input[value='Go']"))).click()
        sleep(1)
        metcycle = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                    "select[name='metcyc']>option:first-child"))).get_attribute('value')
        # print(metcycle)
        with open('metcycle.json', 'r') as fp:
            tmp = json.load(fp)
            metcycle0 = tmp['metcycle']
            lat0 = tmp['lat']
            lon0 = tmp['lon']
        if metcycle != metcycle0 or lat != lat0 or lon != lon0:
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                        "input[type='submit'][value='Next>>']"))).click()
            sleep(1)
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "select[name='nhrs']"))).click()
            sleep(1)
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "select[name='nhrs']>option:last-child"))).click()  # longest time range available
            sleep(1)
            # WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            #                                                 "input[type='RADIO'][name='adddata'][value='1']"))).click()
            # time.sleep(1)
            img1 = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "img[alt='Security Code']"))).get_attribute("src")

            urlretrieve(img1, 'imgfp1.gif')
            im1 = Image.open('imgfp1.gif').convert('RGB')
            im2 = im1.filter(ImageFilter.MedianFilter(5))
            im3 = im2.filter(ImageFilter.GaussianBlur(2))
            im4 = ImageEnhance.Brightness(im3).enhance(2)
            im5 = ImageEnhance.Contrast(im4).enhance(2)

            txt1 = pytesseract.image_to_string(
                im5, config='-l eng -c tessedit_char_whitelist=123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ').strip()

            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                        "input#password1"))).send_keys(txt1)
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "input[type='submit'][value='Get Stability']"))).click()
            sleep(1)
            try:
                a = browser.find_element(By.CSS_SELECTOR, "td#bestOf.mainPanel h2")
                if a.text == 'ERROR!':
                    print('text recognition failed')
                    raise TimeoutException
            except NoSuchElementException:
                pass
            link1 = WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.LINK_TEXT,
                                                                                "Text Results"))).get_attribute('href')
            urlretrieve(link1, 'tab_stab.txt') # TODO: hardcoding to get rid of
            print(link1)
            with open('metcycle.json', 'w') as fp:
                tmp = {'metcycle': metcycle, 'lat': lat, 'lon': lon}
                json.dump(tmp, fp)
        else:
            print(f'Cached result: new metcycle {metcycle} is equal to old metcycle {metcycle0}.')
    except TimeoutException:
        print('timeout')
    finally:
        browser.quit()


def read_data():
    with open('tab_stab.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
        for row in spamreader:
            if len(row) > 6 and '.' in row[0]:
                tmp = list(map(int, row[1:6]))
                row[0] = datetime(year=tmp[0] + 2000, month=tmp[1], day=tmp[2], hour=tmp[3], minute=tmp[4])
                print(row[0], row[6])


if __name__ == '__main__':
    stable(56, 44)
    read_data()
