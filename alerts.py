import os
import csv
import sys
import json
import time
import requests
import datetime
import config
import gtts
from playsound import playsound

save_path = "C:/Users/peter/Py Projects/CoinMarketAPI/Project2/audiofiles/"

tts = gtts.gTTS("ALERT ALERT ALERT")
tts.save(save_path + "alert.mp3")

parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD'
}

headers = {
    'Accepts': 'application.json',
    'X-CMC_PRO_API_KEY': config.coin_marketcap_api_key
}

base_url = 'https://pro-api.coinmarketcap.com'

print()
print('ALERTS TRACKING...')
print()

already_hit_symbols = []

while True:
    with open("my_alerts.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if '\ufeff' in line[0]:
                line[0] = line[0][1:].upper()
            else:
                line[0] = line[0].upper()

            symbol = line[0]
            amount = line[1]

            quote_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + parameters['convert'] + '&symbol=' + symbol

            request = requests.get(quote_url, headers=headers)

            results = request.json()

            currency = results['data'][symbol]

            name = currency['name']
            price = currency['quote'][parameters['convert']]['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                now = datetime.datetime.now()
                current_time = now.strftime("%I.%M%p")
                print(name + ' hit ' + amount + ' at ' + current_time)
                alert_file_name = symbol + ' ' + current_time + '.mp3'
                
                playsound(save_path + "alert.mp3")
                tts = gtts.gTTS(name + ' hit ' + amount)
                tts.save(save_path + alert_file_name)
                playsound(save_path + alert_file_name)
                already_hit_symbols.append(symbol)
                time.sleep(2)
                os.remove(save_path + alert_file_name)
    
    print('...')
    
    time.sleep(10)