#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd 
pd.set_option('display.float_format', lambda x: '%.3f' % x)
En_in = pd.read_excel(r"D:\FILES\BD_EXCEL\En_In.xls", skiprows = 16, nrows = 227)
En_in = En_in.drop(En_in.iloc[:, 0:2], axis = 1)
En_in.columns.values[0:4] = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"]
En_in.columns.tolist()

En_in.loc[1: ,"Energy Supply":] = En_in.loc[1:, "Energy Supply":].apply(pd.to_numeric, errors ='coerce')
En_in["Energy Supply"] *= 1000000

Country = ["Republic of Korea", "United States of America", "United Kingdom of Great Britain and Northern Ireland", "China, Hong Kong Special Administrative Region"]
NewCountry = ["South Korea" , "United States", "United Kingdom", "Hong Kong"]
En_in['Country'] = En_in['Country'].replace(r"\(.*\)","", regex = True).str.strip()
En_in['Country'] = En_in['Country'].replace('\d+', '', regex = True)
En_in['Country'] = En_in['Country'].replace(Country, NewCountry  )
En_in.loc[En_in["Country"].isin(["American Samoa", "South Korea", "Bolivia", "United States" ])]

# WOKR 5
GPD = pd.read_csv(r"D:\FILES\BD_EXCEL\gpd.csv", skiprows = 4)
GPD.columns.values[:1] = ['Country']
GPD = GPD.drop(GPD.iloc[:, 4:50], axis = 1)
Country = ["Korea, Rep. ", "Iran, Islamic Rep.", "Hong Kong SAR, China"]
NewCountry = ["South Korea", "Iran", "Hong Kong"]
GPD['Country'] = GPD['Country'].replace(Country, NewCountry)
GPD.head(1)

#WORK 6 
scimagojr = pd.read_excel(r"D:\FILES\BD_EXCEL\scimagojr.xlsx")

#WORK 7
Result = pd.merge(scimagojr, En_in)
Result = pd.merge(Result, GPD.drop(GPD.iloc[:, 1:4], axis = 1))
Result = Result.set_index("Country")
Result.drop(Result.loc[Result["Rank"] > 15].index, inplace = True)
Result.head(3)

Result.shape

#WORK 8 
def task_eight():
    avgGPD = Result.iloc[:, 10:].mean(axis = 1)
    avgGPD.sort_values(ascending = False, inplace = True)
    avgGPD.name = "avgGPD"
    return avgGPD
task_eight()

#WORK 9 
def task_nine():
    listAvgGPD = task_eight().index.to_list()
    fiveGPD = Result.loc[listAvgGPD[4]]
    return (fiveGPD.name, fiveGPD[19] - fiveGPD[10])
task_nine()

def task_ten():
    maxResult = Result["% Renewable"].max()
    maxIndex = pd.to_numeric(Result["% Renewable"]).idxmax()
    return (maxIndex, maxResult)
task_ten()

def task_eleven():
    Result["Population Estimate"] = Result.apply(lambda x: x["Energy Supply"] / x["Energy Supply per Capita"], axis = 1)
    population = Result["Population Estimate"].astype(float).nlargest(6)
    listPopulationIndex = population.index.to_list()
    return(listPopulationIndex[5], population[5])
task_eleven()

def task_twelve():
    Result["Citations per Capita"] = Result.apply(lambda x: x["Citable documents"] / x["Population Estimate"], axis =1)
    carrResult = Result["Citations per Capita"].astype(float).corr(Result["Energy Supply per Capita"].astype(float), method = 'pearson')
    return carrResult
task_twelve()


def addRenewable(x, median):
    if x["% Renewable"] >= median:
        return 1
    else: return 0 

def task_thirteen():
    RenMediana = Result["% Renewable"].median()
    Result["Mediana Renewable"] = Result.apply(lambda x: addRenewable(x, RenMediana), axis = 1)
    Result.sort_values("Rank", ascending = True, inplace = True)
    return Result["Mediana Renewable"].rename().astype(int)
task_thirteen()

from statistics import mean 
ContinentDict = {'China': 'Asia',
 'United States': 'North America',
 'Japan' : 'Asia',
 'United Kingdom' : 'Europe',
 'Russian Federation': 'Europe',
 'Canada' : 'North America',
 'Germany' : 'Europe',
 'India' : 'Asia',
 'France': 'Europe',
 'South Korea': 'Asia',
 'Italy' : 'Europe',
 'Spain' : 'Europe',
 'Iran' : 'Asian',
 'Australia' : 'Australia',
 'Brazil' : 'South America'
}

ContinentList = ['Asia', 'Australia', 'Europe', 'North America', 'South America']
def Task_forteen():
    sortedContine = dict(sorted(ContinentDict.items(), key = lambda x: x[1]))
    df_Continent = pd.DataFrame(columns = ["size", "sum", "mean", "std"], index = ContinentList)
    Result['Continent'] = Result.index.map(sortedContine)
    sizeContine = Result.pivot_table(columns=['Continent'], aggfunc = 'size')
    df_Continent["size"] = sizeContine
    for i in range(len(ContinentList)):
        ContinentElem = Result.loc[Result['Continent'] == ContinentList[i], 'Population Estimate']
        df_Continent.loc[ContinentList[i], 'sum'] = ContinentElem.sum()
        df_Continent.loc[ContinentList[i], 'mean'] = ContinentElem.mean()
        df_Continent.loc[ContinentList[i], 'std'] = ContinentElem.std()
    return df_Continent
Task_forteen()


import plotly.express as px
Result["2015"] = Result["2015"].replace({pd.np.nan: 0})
fig = px.scatter(Result, x = "Rank", y = "% Renewable",
                size = "2015", text = Result.index, hover_name = Result.index, color = "Continent", size_max = 60)
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




