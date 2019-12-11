import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

max_loc_df = pd.read_pickle('processed/Max_locwise')
min_loc_df = pd.read_pickle('processed/Min_locwise')
avg_loc_df = pd.read_pickle('processed/Avg_locwise')

max_loc_df.sort_values(['AQI'], inplace=True)
min_loc_df.sort_values(['AQI'], inplace=True)
avg_loc_df.sort_values(['AQI'], inplace=True)

avg_loc_df.plot(y=["CO", "PM2.5", "PM10"], kind="bar")
plt.title('CO, PM2.5 and PM10 concentrations per state')
plt.show()

avg_loc_df.plot(y=["AQI"], kind="bar")
plt.title('States v/s AQI')
plt.show()

avg_loc_df.head(5).plot(y=["CO", "PM2.5", "PM10"], kind="bar")
plt.title('Cleanest states and their pollutants')
plt.show()

avg_loc_df.tail(5).plot(y=["CO", "PM2.5", "PM10"], kind="bar")
plt.title('Most polluted states and their pollutants')
plt.show()

