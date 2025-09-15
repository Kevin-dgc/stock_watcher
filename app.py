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
    pause = 1
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
    
    time.sleep(30*pause)
    
    for i in range(len(symbols)):
        prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
        
    time.sleep(30*pause)
    
    for i in range(29):
        for i in range(len(symbols)):
            prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
        time.sleep(60*pause) # wait 1 min 5 times end at (10)

    # checks one more end of day time
    time.sleep(21600*pause)
    for i in range(len(symbols)):
            prices[i].append(yf.Ticker(symbols[i]).info.get('regularMarketPrice'))
    
    
    #print(prices)
    saveToJson_CustomFormat(prices)
    

def saveToJson(total_info):
    data_in_json = {}
    
    for list in total_info:
        key = str(list[0])
        vals = list[1:]
        data_in_json[key] = vals

    filename = "stock_data.json"
    with open(filename, "w") as file:
        json.dump(data_in_json, file, indent=4)

def saveToJson_CustomFormat(total_info):
   
    data_in_json = {}
    
    for stock_list in total_info:
        if stock_list: 
            key = str(stock_list[0]) 
            vals = stock_list[1:] 
            data_in_json[key] = vals
    
    filename = "stock_data.json"
    with open(filename, "w") as file:
        file.write("{\n")
        items = list(data_in_json.items())
        for i, (symbol, prices) in enumerate(items):
            prices_str = ",".join(str(p) if p is not None else "null" for p in prices)
            line = f'"{symbol}": [{prices_str}]'
            if i < len(items) - 1:
                line += ","
            file.write(line + "\n")
        file.write("}")
    
    #print(f"Successfully saved data for {len(data_in_json)} stocks to {filename}")
        

# grabInfo()
runProgram()
    
    
    
    
    
    