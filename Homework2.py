import csv
import pandas as pd
import numpy as np
import wbdata

import linreg

#getting my data
countries = [i['id'] for i in wbdata.get_country(incomelevel="HIC", display=False)] #getting High income countries into a list
countries.extend([i['id'] for i in wbdata.get_country(incomelevel="UMC", display=False)]) #Upper middle income countries into list
countries.extend([i['id'] for i in wbdata.get_country(incomelevel="MIC", display=False)]) #Middle income countries into list
indicators = {"EN.ATM.CO2E.PC": "CO2PC", "SE.TER.CUAT.BA.ZS": "Bach_Percent", "NY.GDP.PCAP.CD": "gdppc"} #getting my indicators into a dictionary
df = wbdata.get_dataframe(indicators, country=countries, convert_date=True) #pulling data off of wbdata
df.to_csv('hw2.csv') #write csv

df.dropna(inplace= True) #drop missing values
depv = np.array(df.iloc[:, :1]).reshape((df.shape[0], 1)) #separating my dependent variable array
expv = np.hstack((np.ones((df.shape[0],1)),np.array(df.iloc[:,1:]))) #separating my explanatory variables in an array

#scaling all my variables
depv = (depv-depv.mean())/depv.std()
expv[:, 1:] = (expv[:, 1:] - expv[:, 1:].mean(0))/expv[:, 1:].std(0)

linreg.linreg(depv, expv)

