import re
from bs4 import BeautifulSoup
import requests
import time

# Get currency from internet
def currency():
    global currency_number
    url = 'https://www.tgju.org/profile/price_dollar_rl'
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    currency_number = str(soup.find(attrs={'value'}).get_text())
    currency_number = currency_number.strip()
    currency_number = [float(s) for s in re.findall(r'-?\d+\.?\d*', currency_number)]
    currency_number = f"{round(currency_number[0])},{round(currency_number[1])}"

# Next CD Hope
def cd_next_hop():
    global time_cd
    global time_now
    global time_cd_currency
    time_now = time.gmtime()
    time_now = f'{time_now[3]}{time_now[4]}{time_now[5]}'
    time_cd = time_now
    time_cd = (int(time_cd) + time_cd_currency)
    currency()

# Calc cd time
def currency_cd():
    global time_cd
    global time_now
    if time_cd == "":
        cd_next_hop()
    else:
        if int(time_cd) < int(time_now):
            cd_next_hop()
        else:
            time_now = time.gmtime()
            time_now = f'{time_now[3]}{time_now[4]}{time_now[5]}'