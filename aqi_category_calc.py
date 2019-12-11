import pandas as pd
import numpy as np

max_aqi = pd.read_pickle('processed/Max_aqi')
min_aqi = pd.read_pickle('processed/Min_aqi')
avg_aqi = pd.read_pickle('processed/Avg_aqi')

cols = list(max_aqi.columns.levels[0])
pollutants = cols[:7]
aqi_category = ['Good','Satisfactory','Moderate','Poor','Very Poor','Severe']
brk_pts = pd.DataFrame(index=aqi_category,columns=pollutants)
brk_pts.reset_index(inplace=True)

brk_pts['CO'] = [1,2,10,17,34,np.nan]
brk_pts['NO2'] = [40,80,180,280,400,np.nan]
brk_pts['PM10'] = [50,100,250,350,430,np.nan]
brk_pts['PM2.5'] = [30,60,90,120,250,np.nan]
brk_pts['OZONE'] = [50,100,168,208,748,np.nan]
brk_pts['SO2'] = [40,80,380,800,1600,np.nan]
brk_pts['NH3'] = [200,400,800,1200,1800,np.nan]

aqimax = []
aqimin = []
aqiavg = []

for i in range(max_aqi.index.size):
    aqimax.append(np.max(max_aqi.ix[i,pollutants]))
    aqimin.append(np.max(min_aqi.ix[i,pollutants]))
    aqiavg.append(np.max(avg_aqi.ix[i,pollutants]))

max_aqi['AQI'] = pd.Series(np.asarray(aqimax),index=max_aqi.index)
min_aqi['AQI'] = pd.Series(np.asarray(aqimin),index=min_aqi.index)
avg_aqi['AQI'] = pd.Series(np.asarray(aqiavg),index=avg_aqi.index)   

def toomanyNaN(aqi_df,aqi):
    for i in range(aqi_df.index.size):
        if aqi_df.ix[i,pollutants].isnull().sum()>=4:
           aqi_df.ix[i,'AQI']=np.nan
           aqi[i] = np.nan
    return aqi_df,aqi

def targetlist(aqi):
    cat_list = []
    cat_ind = [50,100,200,300,400,500]
    aqi_category = ['Good','Satisfactory','Moderate','Poor','Very Poor','Severe']
    for rows in range(len(aqi)):
        if np.isnan(aqi[rows]):
            cat_list.append(np.nan)
        else:
            for i in range(len(cat_ind)):
                if aqi[rows]<=cat_ind[i]:
                    cat_list.append(i)
                    break
    
    return cat_list

max_aqi,aqimax = toomanyNaN(max_aqi,aqimax)
min_aqi,aqimin = toomanyNaN(min_aqi,aqimin)
avg_aqi,aqiavg = toomanyNaN(avg_aqi,aqiavg)

cat_list_max = targetlist(aqimax)
cat_list_min= targetlist(aqimin)
cat_list_avg = targetlist(aqiavg)

max_aqi['AQI_category'] = pd.Series(np.asarray(cat_list_max),index=max_aqi.index)
min_aqi['AQI_category'] = pd.Series(np.asarray(cat_list_min),index=min_aqi.index)
avg_aqi['AQI_category'] = pd.Series(np.asarray(cat_list_avg),index=avg_aqi.index)

max_aqi.to_pickle('processed/Max_aqi')
min_aqi.to_pickle('processed/Min_aqi')
avg_aqi.to_pickle('processed/Avg_aqi')


