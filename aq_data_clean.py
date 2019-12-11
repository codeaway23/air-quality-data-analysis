from lxml import etree
import pandas as pd
import numpy as np

aq_xml = etree.parse("data/data_aqi_cpcb.xml")
root = aq_xml.getroot()
country = root.getchildren()

states = []
stations = []
data = []

for state in country:
    k=0
    for city in state:
        for station in city:
            j=0
            for poll_ind in station:    
                pollutants = []
                params = ["Max","Min","Avg"]
                states.append(state[k].get("id"))
                stations.append(station[j].get("id"))
                for i in range(len(poll_ind)):
                    pollutants.append(poll_ind[i].get("id"))                                    
                df = 'df'+ station[j].get("id")
                df = pd.DataFrame(index=[params],columns=[pollutants])
                for i in range(len(poll_ind)):
                    df.ix['Max',pollutants[i]] = poll_ind[i].get("Max")
                    df.ix['Min',pollutants[i]] = poll_ind[i].get("Min")
                    df.ix['Avg',pollutants[i]] = poll_ind[i].get("Avg")
                data.append(df)
                j=j+1
        k=k+1

result = pd.concat(data,keys=stations)
result.reset_index(inplace=True)
result.replace('NA',np.nan,inplace=True)
result.rename(columns={'level_0':'station','level_1':'stat_type'},inplace=True)

cols = list(result.columns.levels[0])
r,c = result.shape

result.to_pickle('processed/AQI_data')

aqi_data = pd.read_pickle('processed/AQI_data')

cols = list(aqi_data.columns.levels[0])
pollutants = cols[:7]
aqi_data[pollutants] = aqi_data[pollutants].apply(pd.to_numeric)
aqi_data[['station','stat_type']] = aqi_data[['station','stat_type']].astype('str')

max_ind = []
min_ind = []
avg_ind = []

for i in range(int(aqi_data['stat_type'].count()/3)):
    max_ind.append(int(3*i))
    min_ind.append(int(3*i+1))
    avg_ind.append(int(3*i+2))
    
max_aqi = aqi_data.drop(min_ind+avg_ind, axis=0)
min_aqi = aqi_data.drop(max_ind+avg_ind, axis=0)
avg_aqi = aqi_data.drop(min_ind+max_ind, axis=0)

max_aqi.reset_index(inplace=True)
max_aqi.drop(['index','stat_type'], axis=1,inplace=True) 
min_aqi.reset_index(inplace=True) 
min_aqi.drop(['index','stat_type'], axis=1,inplace=True) 
avg_aqi.reset_index(inplace=True) 
avg_aqi.drop(['index','stat_type'], axis=1,inplace=True) 

max_aqi['state'] = pd.Series(np.asarray(states),index=max_aqi.index)
min_aqi['state'] = pd.Series(np.asarray(states),index=min_aqi.index)
avg_aqi['state'] = pd.Series(np.asarray(states),index=avg_aqi.index)

max_aqi.to_pickle('processed/Max_aqi')
min_aqi.to_pickle('processed/Min_aqi')
avg_aqi.to_pickle('processed/Avg_aqi')
