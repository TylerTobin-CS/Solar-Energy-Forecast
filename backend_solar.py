#notes:
#make it so that it does not give high efficiency at night
#have csv of sun hours per country then compare county code to csv then provide sun hours as variable from column 2 from csv

import requests
import json
import csv
from datetime import datetime
import geocoder

class backend:
    def __init__(self):

        #ipify API:
        self.response0 = requests.get('https://api64.ipify.org?format=json').json()

        #OpenWeatherMap API:
        self.API_URL = "https://api.openweathermap.org/data/2.5/weather?"
        self.OWM_KEY = "88d0f380ac59634bf48a81910c79629b"

        self.API_URL_SOLAR = "http://api.openweathermap.org/data/2.5/solar_radiation/history?lat=51.5098&lon=-0.1180&start=1634342400&end=1634428800appid={88d0f380ac59634bf48a81910c79629b}"

        self.temperature = 0

        #open csv to see preferences
        #read preference
        #if csv == 0 then self.kWhText = "kWh per day: "

        self.file = open('preferences.csv')
        self.reader = csv.reader(self.file)
        self.fileData = list(self.reader)

    def kWhTextPref(self):
        return self.fileData[0][0]

    def tempPrefShow(self):
        return self.fileData[0][1]

    def getLocation(self):
        self.addressIP = self.response0["ip"]
        #self.urlIP = ("https://ipapi.co/" + self.addressIP + "/json/")
        #self.updatedResponse = requests.get(self.urlIP).json()

        self.urlIP = geocoder.ip(self.addressIP)
        self.locationCity = self.urlIP.city
        self.locationLatitude = str(self.urlIP.latlng[0])
        self.locationLongitude = str(self.urlIP.latlng[1])

        #self.locationCity = self.updatedResponse.get("city")
        #self.locationLatitude = str(self.updatedResponse.get("latitude"))
        #self.locationLongitude = str(self.updatedResponse.get("longitude"))
        return self.locationCity

    def getWeatherData(self):
        self.getLocation()
        self.Report_Location = str(self.locationCity)
        self.Final_URL = self.API_URL + "lat=" + self.locationLatitude + "&lon=" + self.locationLongitude + "&appid=" + self.OWM_KEY
        self.response1 = requests.get(self.Final_URL)

        if self.response1.status_code == 200:
            
            self.data = self.response1.json()
            
            self.main = self.data['main']
            self.sys = self.data['sys']
            self.temperature = self.main['temp']
            self.humidity = self.main["humidity"]
            self.pressure = self.main['pressure']
            self.report = self.data['weather']
            self.sunHoursRise = self.sys['sunrise']
            self.sunHoursSet = self.sys['sunset']
            self.country = self.sys['country']
            return self.country

        else:
            return "Error 01"

    def getTemperature(self):
        self.getWeatherData()
        #converts the temp from kelvin to celcius
        self.temperature = str(int(self.temperature - 273.15))
        return self.temperature

    def getHumidity(self):
        #Gives humitidy in %
        return self.humidity

    def getPressure(self):
        #gives pressure in hPa
        return self.pressure

    def getReport(self):
        #Gives the weather code, list on open weather map website
        self.description = self.report[0]["id"]
        return self.description

    def calculateScore(self):
        self.getTemperature()
        self.getHumidity()
        self.getPressure()
        self.getReport()

        #==== Temperature ====

        #tempScore: temperature * set ratio of 0-36 degree range tested over 5.5% efficiency bounds
        #5.5/36 = 0.15, needs to be equal to 100% so 5.5 * 18.18

        self.TempRange = 0.15
        self.tempScore = (float(self.temperature) * self.TempRange) * 18.18

        #==== Pressure ====

        self.CumulativePercent = 16.66

        if self.pressure >= 1004 and self.pressure <= 1005:
            self.pressureScore = self.CumulativePercent * 1
            
        elif self.pressure >= 1006 and self.pressure <= 1007:
            self.pressureScore = self.CumulativePercent * 2

        elif self.pressure >= 1008 and self.pressure <= 1010:
            self.pressureScore = self.CumulativePercent * 3

        elif self.pressure >= 1011 and self.pressure <= 1013:
            self.pressureScore = self.CumulativePercent * 4

        elif self.pressure >= 1014 and self.pressure <= 1015:
            self.pressureScore = self.CumulativePercent * 5

        elif self.pressure >= 1016 and self.pressure <= 1017:
            self.pressureScore = self.CumulativePercent * 6

        elif self.pressure <= 1003 or self.pressure >= 1018:
            #disregard score as not enough data to base on
            self.pressureScore = 0

        self.pressureScore = int(self.pressureScore)

        #==== Report ====

        self.data = []
        with open("weather.csv") as self.csvFile:
            self.reader = csv.reader(self.csvFile)
            for row in self.reader:
                self.data.append(row)

                if row[0] == str(self.description):
                    self.reportScore = float(row[1])


        #==== Final Score ====
        self.tWeight = 0.15
        self.pWeight = 0.15
        self.hWeight = 0.3
        self.rWeight = 0.4

        if self.pressureScore == 0:
            self.pWeight = 0

        self.tempWeight = float(self.tempScore * self.tWeight)
        self.pressureWeight = float(self.pressureScore * self.pWeight)
        self.humidWeight = float(self.humidity * self.hWeight)
        self.reportWeight = float(self.reportScore * self.rWeight)

        self.totalWeight = self.tWeight + self.pWeight + self.hWeight + self.rWeight

        self.totalScore = (self.tempWeight + self.pressureWeight + self.humidWeight + self.reportWeight) / self.totalWeight
        
        return int(self.totalScore)

        #weighted score

    #Not using predictedEnergy1
    #def predictedEnergy1(self):
        #pass

    def predictedEnergy2(self, panelWatt):

        #CURRENT OUTPUT 
        #solar panel watts x hours of sunlight x efficiency score (0.75) = daily watt-hours

        self.getLocation()
        self.getWeatherData()
        self.getTemperature()
        self.getHumidity()
        self.getPressure()
        self.getReport()
        self.calculateScore()
        
        self.wattOfPanels = int(panelWatt)

        self.data = []
        with open("sunHrs.csv") as self.csvFile:
            self.reader = csv.reader(self.csvFile)
            for row in self.reader:
                self.data.append(row)

                if row[0] == str(self.country):
                    self.sunHrs = float(row[1])


        self.dailyOutput = float((self.wattOfPanels * self.sunHrs * (self.totalScore / 100)) / 1000)
        return self.dailyOutput

#==== Testing ====
#t = backend()
#print(t.predictedEnergy2(2000))

#print(t.kWhTextPref())
#print(t.tempPrefShow())








