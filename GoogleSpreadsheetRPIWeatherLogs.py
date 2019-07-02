import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import bs4
import re
import json
import os
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
row=[timeNow,cpuTemp,outsideTemperature,outsideHumidity,outsideWeather]
#print(str(outsideTemperature)+"°C",str(outsideHumidity)+"%",outsideWeather)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)
spreadsheet=gc.open("Spreadsheet")

wlist=[]
for worksheet in spreadsheet:
    wlist.append(worksheet.title)

if('WeatherLogs' not in wlist):
    worksheet = spreadsheet.add_worksheet(title='WeatherLogs', rows="2", cols="20")
    worksheet.update_cell(1, 1, 'Time')
    worksheet.update_cell(1, 2, 'CPU Temperatue, °C')
    worksheet.update_cell(1, 3, 'Outside Temperature, °C')
    worksheet.update_cell(1, 4, 'Outside Humidity, %')
    worksheet.update_cell(1, 5, 'Outside Weather')

index=len(worksheet.col_values(1))+1
worksheet.insert_row(row,index)
