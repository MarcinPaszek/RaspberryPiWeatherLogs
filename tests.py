import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import bs4
import re
import json
import os
from pytz import timezone
#from gpiozero import CPUTemperature
import datetime
#from datetime import tzinfo

# get date and time
timeNow=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
localTimeZone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

#
numberOfForecasts=5
cpuTemp=round(CPUTemperature().temperature,1) #float with 1 decimal point, deg C 
# get weather from the API openweathermap. It's free, you just have to register
baseurl='https://api.openweathermap.org/'
weather_url='data/2.5/weather?id=3086732&appid=<YOUR INDIVIDUAL KEY HERE>'
forecast_url='data/2.5/forecast?id=3086732&appid=<YOUR INDIVIDUAL KEY HERE>'
url=baseurl+weather_url
uClient=urlopen(url)
page_weather_json=uClient.read()
uClient.close()
jsonWeather = json.loads(page_weather_json)

url=baseurl+forecast_url
uClient=urlopen(url)
page_forecast_json=uClient.read()
uClient.close()
jsonForecast = json.loads(page_forecast_json)

listForecastsDateStamps=[]
for forecastIdex in range(len(jsonForecast["list"])):
    listForecastsDateStamps.append(jsonForecast["list"][forecastIdex]["dt"])
iteratorForecastsDateStamps=iter(listForecastsDateStamps)
futureForecastDateStamp=0
while(futureForecastDateStamp<=jsonWeather["dt"]):
    futureForecastDateStamp=next(iteratorForecastsDateStamps)
#currentWeatherTime=datetime.datetime.fromtimestamp(jsonWeather["dt"],localTimeZone).strftime("%d.%m.%Y %H:%M")

listForecastTimes=[]
listTemperatureForecasts=[]
listHumidityForecasts=[]
listWeatherForecasts=[]
#temperature=list((x["main"]["temp"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0]
for i in range(numberOfForecasts):
    listTemperatureForecasts.append(round(list((x["main"]["temp"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0]-273,1))
    listHumidityForecasts.append(list((x["main"]["humidity"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0])
    listWeatherForecasts.append(list((x["weather"][0]["main"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0])
    listForecastTimes.append(datetime.datetime.fromtimestamp(futureForecastDateStamp,localTimeZone).strftime("%d.%m.%Y %H:%M"))
    futureForecastDateStamp=next(iteratorForecastsDateStamps)
print(listTemperatureForecasts,listHumidityForecasts,listWeatherForecasts)
print(listForecastTimes)


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
numberOfRecords=len(worksheet.col_values(1))
for i in range(numberOfForecasts):
    worksheet.delete_row(numberOfRecords-i)

index=len(worksheet.col_values(1))+1
worksheet.insert_row(row,index)
index=index+1

for i in range(numberOfForecasts):
    row=[listForecastTimes[i],'N.D',listTemperatureForecasts[i],listHumidityForecasts[i],listWeatherForecasts[i]]
    worksheet.insert_row(row,index)
    index=index+1


