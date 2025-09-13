from bs4 import BeautifulSoup
from datetime import date, datetime
from zoneinfo import ZoneInfo
import time
import requests
import json
import yfinance as yf

def runProgram():
    while True:
        cur_time = datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York"))
        if cur_time.hour == 9 and cur_time.minute == 30:
            grabInfo()
            # waits 17 hours
            time.sleep(60000)
        time.sleep(1)

def grabInfo():
    prices = [[], [], [], [], []]
    symbols = []
    
    website = "https://stockanalysis.com/markets/gainers/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(website, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    events = soup.find_all('td', class_="sym svelte-1ro3niy")
    short_events = events[:5]
    
    for event in short_events:
        a_tag = event.find('a')
        if a_tag:
            symbols.append(a_tag.text)

    #print(symbols)
    
    for i in range(len(symbols)):
        prices[i].append(symbols[i])
        prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
    
    time.sleep(30)
    
    for i in range(len(symbols)):
        prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
        
    time.sleep(30)
    
    for i in range(29):
        for i in range(len(symbols)):
            prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
        time.sleep(60) # wait 1 min 5 times end at (10)

    # checks one more end of day time
    time.sleep(21600)
    for i in range(len(symbols)):
            prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
    
    
    #print(prices)
    saveToJson(prices)
    

def saveToJson(total_info):
    data_in_json = {}
    
    for list in total_info:
        key = str(list[0])
        vals = list[1:]
        data_in_json[key] = vals

        filename = "stock_data.json"
        with open(filename, "w") as file:
            json.dump(data_in_json, file, indent=4)


# grabInfo()
runProgram()
    
    
    
    
    
    