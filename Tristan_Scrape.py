#Python File for parsing National Park Weather Data

import tabula
import pandas as pd
import numpy as np
import os
from termcolor import colored

ParkNames  = ['Acadia NP', 'Arches NP', 'Badlands NP', 'Big Bend NP', 'Biscayne NP', 'Black Canyon of the Gunnison NP',
              'Bryce Canyon NP', 'Canyonlands NP', 'Capitol Reef NP', 'Carlsbad Caverns NP', 'Channel Islands NP', 'Congaree NP',
              'Crater Lake NP', 'Cuyahoga Valley NP', 'Death Valley NP', 'Denali NP & PRES', 'Dry Tortugas NP', 'Everglades NP',
              'Gates of the Arctic NP & PRES', 'Glacier Bay NP & PRES', 'Glacier NP', 'Grand Canyon NP', 'Grand Teton NP', 'Great Basin NP',
              'Great Sand Dunes NP & PRES', 'Great Smoky Mountains NP', 'Guadalupe Mountains NP', 'Haleakala NP', 'Hawaii Volcanoes NP', 'Hot Springs NP',
              'Isle Royale NP', 'Joshua Tree NP', 'Katmai NP & PRES', 'Kenai Fjords NP', 'Kings Canyon NP', 'Kobuk Valley NP', 'Lake Clark NP & PRES',
              'Lassen Volcanic NP', 'Mammoth Cave NP', 'Mesa Verde NP', 'Mount Rainier NP', 'National Park of American Samoa', 'North Cascades NP',
              'Olympic NP', 'Petrified Forest NP', 'Pinnacles NP', 'Redwood NP', 'Rocky Mountain NP', 'Saguaro NP', 'Sequoia NP', 'Shenandoah NP',
              'Theodore Roosevelt NP', 'Virgin Islands NP', 'Voyageurs NP', 'Wind Cave NP', 'Wrangell-St. Elias NP & PRES', 'Yellowstone NP',
              'Yosemite NP', 'Zion NP']

Months = ['Jan', 'Feb', "Mar", 'Apr', 'May', 'Jun', 'Jul', 'Aug','Sep','Oct','Nov','Dec','Jan', 'Feb', "Mar", 'Apr', 'May', 'Jun', 'Jul', 'Aug','Sep','Oct','Nov','Dec']

N = pd.DataFrame(columns=ParkNames, index = Months)
#print N

data = "C:/Users/tkschule/Desktop/NOAANPTemps/Saguaro NP.pdf"
df = tabula.read_pdf(data,  encoding = "ISO-8859-1")
df.columns = df.iloc[4]
df.drop(df.index[[0,1,2,3,4,5,18]], inplace = True)
try:
    df2 = df[['Month','Daily Max','Daily Min']]
except:
    df2 = df[['Month', 'Daily Max', 'DailyMin']]

print df2
df2 = df2.set_index(['Month'])

S = df2['Daily Max']
#print type(S)
#print S

#N.merge(s.to_frame(), left_index=True, right_index=True)

pdfDir = "C:/Users/tkschule/Desktop/NOAANPTemps/"


def convertMultiple(pdfDir):
    if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in
    for pdf in os.listdir(pdfDir): #iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        filename = pdf.split(".")[0]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf
            #print pdfFilename
            #print filename
            df = tabula.read_pdf(pdfFilename, encoding="ISO-8859-1")
            df.columns = df.iloc[4]
            df.drop(df.index[[0, 1, 2, 3, 4, 5, 18]], inplace=True)

            try:
                Temps = df[['Month', 'Daily Max', 'Daily Min']]
                Temps = Temps.set_index(['Month'])
                AllMax[filename] = Temps['Daily Max']
                print "Max", filename
            except:
                try:
                    Temps = df[['Month', 'Daily Max', 'DailyMin']]
                    Temps = Temps.set_index(['Month'])
                    AllMax[filename] = Temps['Daily Max']
                    print "Max", filename
                except:
                    print colored(("Error with", filename), 'red')
                    AllMax[filename] = 0

            try:
                AllMin[filename] = Temps['Daily Min']
                print "Min", filename
            except:
                try:
                    AllMin[filename] = Temps['DailyMin']
                    print "Min", filename
                except:
                    print colored(("Error with", filename), 'red')
                    AllMin[filename] = 0

AllMax = pd.DataFrame()
AllMin = pd.DataFrame()
#result['A'] = df2['Daily Max']

print "\n RESULTTT HIGH: "
convertMultiple(pdfDir)
result = AllMax.append(AllMin)
print colored(result,'cyan')
AllMax.columns=ParkNames
AllMin.columns=ParkNames
result.columns=ParkNames
AllMax.to_csv("Daily Max Temps NP.csv")
AllMin.to_csv("Daily Min Temps NP.csv")
result.to_csv("NP Monthly Temperatures.csv")