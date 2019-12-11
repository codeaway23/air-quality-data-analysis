import pandas as pd
import numpy as np

max_aqi = pd.read_pickle('processed/Max_aqi')
min_aqi = pd.read_pickle('processed/Min_aqi')
avg_aqi = pd.read_pickle('processed/Avg_aqi')

max_aqi.dropna(subset=max_aqi.columns[[9]],how='any',inplace=True)
avg_aqi.dropna(subset=max_aqi.columns[[9]],how='any',inplace=True)
min_aqi.dropna(subset=max_aqi.columns[[9]],how='any',inplace=True)

states = max_aqi['state'].values

max_aqi.drop(['station'], axis=1, inplace=True)
min_aqi.drop(['station'], axis=1, inplace=True)
avg_aqi.drop(['station'], axis=1, inplace=True)

def LocationDF(aqi_df,stations):

    states = [] 
    for i in range(len(aqi_df['state'].values)): 
	    if aqi_df['state'].values[i] not in states: 
	    	states.append(aqi_df['state'].values[i][0]) 
	
    aqi_df.drop(['state'], axis=1, inplace=True)

    cols = aqi_df.columns    
    loc_arr = np.zeros((len(states),len(cols)))
    aqi_arr = np.nan_to_num(aqi_df.values)

    for i in range(len(states)):
        k = 0
        for j in range(len(aqi_df)):
            if stations[j] == states[i]:
                loc_arr[i,:] = loc_arr[i,:] + aqi_arr[j,:]
                k = k+1        
        loc_arr[i,:] = loc_arr[i,:]/k

    loc_arr = loc_arr.astype(np.int64)

    location_df = pd.DataFrame(loc_arr,index=np.arange(len(states)),columns=cols)
    location_df['states'] = states
    
    return location_df

max_loc = LocationDF(max_aqi,states)
min_loc = LocationDF(min_aqi,states)
avg_loc = LocationDF(avg_aqi,states)

all_cols = max_loc.columns.levels[0].tolist()
cols = all_cols[0:7] + all_cols[11:14]

max_loc_df = pd.DataFrame(max_loc.values, columns=cols)
min_loc_df = pd.DataFrame(min_loc.values, columns=cols)
avg_loc_df = pd.DataFrame(avg_loc.values, columns=cols)

max_loc_df.set_index('states', drop=True, inplace=True)
min_loc_df.set_index('states', drop=True, inplace=True)
avg_loc_df.set_index('states', drop=True, inplace=True)

max_loc_df.to_pickle('processed/Max_locwise')
min_loc_df.to_pickle('processed/Min_locwise')
avg_loc_df.to_pickle('processed/Avg_locwise')

