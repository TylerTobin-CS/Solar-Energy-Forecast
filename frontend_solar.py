#Front end for solar forecasting

import backend_solar as backend_solar
from tkinter import *
import tkinter.messagebox
import datetime
from datetime import date
import csv
from tkinter import Menu
import os
from tkinter import filedialog, messagebox, ttk
import tkinter.font as font
import random


def main():
    root = Tk()
    app = welcome(root)
    
class welcome:
    #The first window that appears the user containing the navigation for UI aswell as methods for navigation

    def __init__(self, master):
        #Constructor method will create GUI layout for login screen such as: Frames, Buttons, Labels and entry boxes

        self.energyForecast = backend_solar.backend()
        self.Location = self.energyForecast.getLocation()
        
        self.master = master
        self.master.title("TTS Solar Forecast")
        self.master.geometry('480x200+0+0')
        self.frame = Frame(self.master)
        self.frame.pack()
        self.master.configure(background='gray40')
        self.frame.configure(background='gray40')

        self.header = Label(self.frame, text = "Solar Forecast", bg = "gray40", fg = "#34c9eb", font = ("helvetica new", 25), pady = 15)
        self.header.grid(row = 0, column = 0, columnspan = 2)
        
        self.genButton = Button(self.frame, text = "Forecast", width = 15, bg = "gray60", fg = "#34c9eb", command = self.forecastWindow)
        self.genButton.grid(row = 1, column = 0)

        self.viewButton = Button(self.frame, text = "Saved", width = 15, bg = "black", fg = "#34c9eb", command = self.viewWindow)
        self.viewButton.grid(row = 1, column = 1)

        self.settingsButton = Button(self.frame, text = "Settings", width = 15, bg = "gray25", fg = "#34c9eb", command = self.settingsWindow)
        self.settingsButton.grid(row = 2, column = 0, columnspan = 2)

        self.infoLabel = Label(self.frame, text = "Tysco Technology Solutions (TTS)", bg = "gray40", fg = "grey", font = ("helvetica new", 15))
        self.infoLabel.grid(row = 3, column = 0, columnspan = 2, pady = 15)

    #Preset navigation in the super class:

    def forecastWindow(self):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = forecast(self.newWindow)

    def viewWindow(self):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = viewPrevious(self.newWindow)

    def settingsWindow(self):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = settings(self.newWindow)

    def goHome(self):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = welcome(self.newWindow)

#===============================================================================================

class settings(welcome):
    #Settings provides the ability to change the metrics used and to show or hide temperture readings
    
    def __init__(self, master):
        

        
        self.master = master
        self.master.title("TTS Solar Forecast")
        self.master.geometry('480x480+0+0')
        self.frame = Frame(self.master)
        self.frame.pack()
        self.master.configure(background='gray40')
        self.frame.configure(background='gray40')

        self.header = Label(self.frame, text = "Settings", bg = "gray40", fg = "#34c9eb", font = ("helvetica new", 25), pady = 15)
        self.header.grid(row = 0, column = 0, columnspan = 3)

        self.metricsKwLabel = Label(self.frame, text = "Wattage", bg = "gray40", fg = "#34c9eb")
        self.metricsKwLabel.grid(row = 1, column = 0, pady = 15, padx = 30)

        self.kWhYesBut = Button(self.frame, text = "KW", width = 10, bg = "gray25", fg = "#34c9eb", command = self.showKwatt)
        self.kWhYesBut.grid(row =1, column = 1, pady = 15, padx = 5)

        self.kWhNoBut = Button(self.frame, text = "W", width = 10, bg = "gray25", fg = "#34c9eb", command = self.showNwatt)
        self.kWhNoBut.grid(row =1, column = 2, pady = 15, padx = 5)

        self.showTempLabel = Label(self.frame, text = "Show temperature", bg = "gray40", fg = "#34c9eb")
        self.showTempLabel.grid(row = 2, column = 0, pady = 15, padx = 30)

        self.tempYesBut = Button(self.frame, text = "Show", width = 10, bg = "gray25", fg = "#34c9eb", command = self.showTemp)
        self.tempYesBut.grid(row = 2, column = 1, pady = 15, padx = 5)

        self.tempNoBut = Button(self.frame, text = "Hide", width = 10, bg = "gray25", fg = "#34c9eb", command = self.hideTemp)
        self.tempNoBut.grid(row = 2, column = 2, pady = 15, padx = 5)


        self.saveBut = Button(self.frame, text = "SAVE", command = self.save, width = 12, fg = "#34c9eb")
        self.saveBut.grid(row = 3, column = 1, columnspan = 2, pady = 5)

        self.homeButton = Button(self.frame, text = "HOME", command = self.goHome, width = 12, fg = "#34c9eb")
        self.homeButton.grid(row = 3, column = 0, columnspan = 2, pady = 5)

        self.infoLabel = Label(self.frame, text = "Tysco Technology Solutions (TTS)", bg = "gray40", fg = "grey", font = ("helvetica new", 15))
        self.infoLabel.grid(row = 4, column = 0, columnspan = 3, pady = 10)

        self.file = open('preferences.csv')
        self.reader = csv.reader(self.file)
        self.fileData = list(self.reader)

        #Incase the user needs to change one entity load them both
        self.wattPref = self.fileData[0][0]
        self.tempPref = self.fileData[0][1]
        
    #When corresponding button is pressed change value to a key of 1 and 0
    def showKwatt(self):
        self.wattPref = 0
        messagebox.showinfo("showinfo", "Changed to kW")
        return self.wattPref

    def showNwatt(self):
        self.wattPref = 1
        messagebox.showinfo("showinfo", "Changed to W")
        return self.wattPref

    def showTemp(self):
        self.tempPref = 1
        messagebox.showinfo("showinfo", "Showing")
        return self.tempPref

    def hideTemp(self):
        self.tempPref = 0
        messagebox.showinfo("showinfo", "Hidden")
        return self.tempPref

    def save(self):
        
        #Overwrite what is in csv and write preference

        data = [str(self.wattPref), str(self.tempPref)]

        with open('preferences.csv', 'w') as self.savedFile:

            self.writer = csv.writer(self.savedFile)
            self.writer.writerow(data)

        self.savedFile.close()
        messagebox.showinfo("showinfo", "Saved")

#===============================================================================================

class forecast(welcome):

    #Forecast is using the backend to provide a score and calculate the solar forecast right now

    def __init__(self, master):
        
        self.energyForecast = backend_solar.backend()
        self.location = self.energyForecast.getLocation()
        self.kWhText = self.energyForecast.kWhTextPref()
        self.tempShow = self.energyForecast.tempPrefShow()
        self.temperatureShow = self.energyForecast.getTemperature()

        if self.kWhText == "0":
            self.kWhTextStart = "kWh per day: "
        elif self.kWhText == "1":
            self.kWhTextStart = "Wh per day: "

        else:
            self.kWhTextStart = "error"

        self.master = master
        self.master.title("TTS Solar Forecast")
        self.master.geometry('480x480+0+0')
        self.frame = Frame(self.master)
        self.frame.pack()
        self.master.configure(background='gray40')
        self.frame.configure(background='gray40')

        self.header = Label(self.frame, text = "Solar Forecast (Now)", bg = "gray40", fg = "#34c9eb", font = ("helvetica new", 25), pady = 15)
        self.header.grid(row = 0, column = 0, columnspan = 2)

        self.locationLabel = Label(self.frame, text = "Location: ", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.locationLabel.grid(row = 1, column = 0)

        self.locationDisplay = Label(self.frame, text = self.location, pady = 10, bg = "gray40", fg = "#34c9eb")
        self.locationDisplay.grid(row = 1, column = 1)

        self.panelWattStr = StringVar()

        self.panelWattLabel = Label(self.frame, text = "Enter System/Panel Wattage: ", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.panelWattLabel.grid(row = 2, column = 0)

        self.panelWattEntry = Entry(self.frame, textvariable = self.panelWattStr, bg = "gray40", fg = "white")
        self.panelWattEntry.grid(row = 2, column = 1)

        self.kWhPerDayLabel = Label(self.frame, text = self.kWhTextStart, pady = 10, bg = "gray40", fg = "#34c9eb")
        self.kWhPerDayLabel.grid(row = 3, column = 0)

        self.kWhPerDayDisplay = Label(self.frame, text = "----", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.kWhPerDayDisplay.grid(row = 3, column = 1)

        self.efficiencyLabel = Label(self.frame, text = "Efficiency: ", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.efficiencyLabel.grid(row = 4, column = 0)

        self.efficiencyDisplay = Label(self.frame, text = "----", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.efficiencyDisplay.grid(row = 4, column = 1)
        
        self.panelPowerLabel = Label(self.frame, text = "Panel after Efficiency: ", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.panelPowerLabel.grid(row = 5, column = 0)

        self.panelPowerDisplay = Label(self.frame, text = "----", pady = 10, bg = "gray40", fg = "#34c9eb")
        self.panelPowerDisplay.grid(row = 5, column = 1)

        self.genButton = Button(self.frame, text = "GENERATE", command = self.update, width = 15)
        self.genButton.grid(row = 6, column = 0)

        self.saveButton = Button(self.frame, text = "SAVE", width = 15, command = self.saveResult)
        self.saveButton.grid(row = 6, column = 1)

        self.viewButton = Button(self.frame, text = "VIEW OTHER", width = 15, command = self.viewWindow)
        self.viewButton.grid(row = 7, column = 1)
        
        self.genButton = Button(self.frame, text = "HOME", command = self.goHome, width = 15)
        self.genButton.grid(row = 7, column = 0)

        self.tempNowLabel = Label(self.frame, text = "Temperature: ", bg = "gray40", fg = "#34c9eb")
        self.tempNowLabel.grid(row = 8, column = 0)

        self.tempNowDisplay = Label(self.frame, text = self.temperatureShow, bg = "gray40", fg = "#34c9eb")
        self.tempNowDisplay.grid(row = 8, column = 1)

        if self.tempShow == "1":
            self.tempNowLabel.grid(row = 8, column = 0)

        elif self.tempShow == "0":
            self.tempNowLabel.grid_forget()
            self.tempNowDisplay.configure(text = "")

        else:
            print("error")

    def update(self):

        self.panelWatt = self.panelWattStr.get()
        self.efficiency = self.energyForecast.calculateScore()

        if self.panelWatt == '':
            self.panelWatt = 0
        elif self.panelWatt.isnumeric() == False:
            self.panelWatt = 0
        else:
            self.kWhTextEnd = "error"
            self.kWhPerDay = float(self.energyForecast.predictedEnergy2(self.panelWatt))
            if self.kWhText == "0":
                self.kWhTextEnd = " kWh"
                
            elif self.kWhText == "1":
                self.kWhTextEnd = " Wh"
                self.kWhPerDay = self.kWhPerDay * 1000

            else:
                self.kWhTextEnd = "error"
        
            self.kWhPerDayDisplay.configure(text = str(round(self.kWhPerDay, 2)) + self.kWhTextEnd)

            self.efficiencyDisplay.configure(text = str(self.efficiency) + "%")
        
            self.panelPowerDisplay.configure(text = str(int(float(self.panelWatt) * (self.efficiency / 100))) + "W" ) 
        
    def saveResult(self):

        self.today = date.today()

        #open new csv
        #save date

        #save kwh
        #save efficiency

        data = [self.today, str(round(self.kWhPerDay, 2)), str(self.efficiency), str(self.panelWatt)]

        with open('saved.csv', 'w') as self.savedFile:

            self.writer = csv.writer(self.savedFile)
            self.writer.writerow(data)

        self.savedFile.close()
        messagebox.showinfo("showinfo", "Saved")

    def goHome(self):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = welcome(self.newWindow)
    
#===============================================================================================    

class viewPrevious(welcome):
    
    #ViewPrevious gives th euser the ability to view saved forecasts from another time

    def __init__(self, master):

        self.master = master
        self.master.title("TTS Solar Forecast")
        self.master.geometry('480x480+0+0')
        self.frame = Frame(self.master)
        self.frame.pack()
        self.master.configure(background='gray40')
        self.frame.configure(background='gray40')

        self.header = Label(self.frame, text = "Previous Forecasts", bg = "gray40", fg = "#34c9eb", font = ("helvetica new", 25), pady = 15)
        self.header.grid(row = 0, column = 0, columnspan = 2)

        self.file = open('saved.csv')
        self.reader = csv.reader(self.file)
        self.fileData = list(self.reader)

        self.listOfData = []
        for x in list(range(0, len(self.fileData))):
            self.listOfData.append(self.fileData[x][0])

        self.userStockChoice = Listbox(self.frame)
        self.userStockChoice.grid(row = 1, column = 0)
        #Inserting the data to the list box for the first time of loading the window
        for x, y in enumerate(self.listOfData):
            self.userStockChoice.insert(x, y)

        self.dateLabel = Label(self.frame, text = "Date: ", bg = "gray40", fg = "#34c9eb")
        self.dateLabel.grid(row = 2, column = 0)

        self.dateDisplay = Label(self.frame, text = "----", bg = "gray40", fg = "#34c9eb")
        self.dateDisplay.grid(row = 2, column = 1)

        self.kWhLabel = Label(self.frame, text = "kWh:", bg = "gray40", fg = "#34c9eb")
        self.kWhLabel.grid(row = 3, column = 0)

        self.kWhDisplay = Label(self.frame, text = "----", bg = "gray40", fg = "#34c9eb")
        self.kWhDisplay.grid(row = 3, column = 1)

        self.effLabel = Label(self.frame, text = "Efficiency: ", bg = "gray40", fg = "#34c9eb")
        self.effLabel.grid(row = 4, column = 0)

        self.effDisplay = Label(self.frame, text = "----", bg = "gray40", fg = "#34c9eb")
        self.effDisplay.grid(row = 4, column = 1)

        self.systemLabel = Label(self.frame, text = "System: ", bg = "gray40", fg = "#34c9eb")
        self.systemLabel.grid(row = 5, column = 0)

        self.systemDisplay = Label(self.frame, text = "----", bg = "gray40", fg = "#34c9eb")
        self.systemDisplay.grid(row = 5, column = 1)

        self.updateButton = Button(self.frame, text = "VIEW", command = self.updatePrev, width = 15, bg = "black", fg = "#34c9eb")
        self.updateButton.grid(row = 6, column = 0, padx = 5)

        self.DeleteButton = Button(self.frame, text = "DELETE", command = self.deletePrev, width = 15, bg = "black", fg = "#34c9eb")
        self.DeleteButton.grid(row = 6, column = 1, padx = 5)

        self.homeButton = Button(self.frame, text = "HOME", command = self.goHome, width = 15, bg = "black", fg = "#34c9eb")
        self.homeButton.grid(row = 7, column = 0, padx = 5, columnspan = 2)

    def updatePrev(self):
        try:
            self.index = self.userStockChoice.curselection()[0]
            self.dateDisplay.config(text = self.fileData[self.index][0])
            self.kWhDisplay.config(text = self.fileData[self.index][1])
            self.effDisplay.config(text = self.fileData[self.index][2])
            self.systemDisplay.config(text = self.fileData[self.index][3])

        except ValueError:
            print("Error Execpetion caught!")

    def deletePrev(self):

        #Creating an index of curser selcetion to know what to delete
        self.index = self.userStockChoice.curselection()[0]
        self.indexCode = str(self.fileData[self.index][3])

        tempList = list()
        with open('saved.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            
            for row in reader:
                tempList.append(row)
                
                for field in row:
                    if field == self.indexCode:
                        tempList.remove(row)
                        
        with open('saved.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(tempList)

        #Once the entity is deleted, the list box with updated info is displayed on top of the old
        file = open('saved.csv')
        reader = csv.reader(file)
        self.fileData = list(reader)
        self.listOfData = []
        
        for x in list(range(0, len(self.fileData))):
            self.listOfData.append(self.fileData[x][0])
            
        self.userStockChoice = Listbox(self.frame)
        self.userStockChoice.grid(row = 1, column = 0)
        #Inserting the data from listOfData in to the list box
        for x, y in enumerate(self.listOfData):
            self.userStockChoice.insert(x, y)

main()

