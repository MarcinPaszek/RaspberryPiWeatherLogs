from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import bs4
import re
import json
import subprocess
from collections import defaultdict
import os
import csv
from gpiozero import CPUTemperature
import datetime

# get date and time
timeNow=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
cpuTemp=round(CPUTemperature().temperature,1) #float with 1 decimal point, deg C 

# get weather from the API openweathermap. It's free, you just have to register
baseurl='https://api.openweathermap.org/'
my_url='data/2.5/weather?lat=50.1889514&lon=18.1937972&appid=<YOUR INDIVIDUAL API KEY HERE>'
url=baseurl+my_url
uClient=urlopen(url)
page_json=uClient.read()
uClient.close()
jsonWeather = json.loads(page_json)

#  format weather into variables
outsideTemperature=round(jsonWeather["main"]['temp']-273,1)
outsideWeather=jsonWeather["weather"][0]["main"]
outsideHumidity=jsonWeather["main"]['humidity']
#print(str(outsideTemperature)+"°C",str(outsideHumidity)+"%",outsideWeather)

# save/export data with the format of choice. For a start, CSV
if((os.path.isfile('./'+'WeatherLogs'+'.csv'))==False): #create csv file and write header row
    listHeader=['Time','CPU temperature [°C]', 'Outside temperature [°C]', 'Outside humidity [%]', 'Outside weather']
    with open(('WeatherLogs'+'.csv'), 'w', newline='') as csvfile:
        csvWriter=csv.writer(csvfile)
        csvWriter.writerow(listHeader)
        csvfile.close()

csvrow=[]
csvrow.append(timeNow)
csvrow.append(cpuTemp)
csvrow.append(outsideTemperature)
csvrow.append(outsideHumidity)
csvrow.append(outsideWeather)
with open(('WeatherLogs'+'.csv'), 'a') as csvfile:
    csvWriter=csv.writer(csvfile)
    csvWriter.writerow(csvrow)
