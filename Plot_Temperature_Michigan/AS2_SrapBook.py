

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# For IPython notebook implementation
# %matplotlib notebook

# Read data for a specific region
initial_df = pd.read_csv('fb44')

# Keep data only for 1 station: 'CA006114979' & Sort values by date
CA006114979_station = initial_df[initial_df['ID'] == 'CA006114979']
CA006114979_station = CA006114979_station.sort_values(by='Date')
# Divide Data_Value by 10 to get the actual value in degree celcius
CA006114979_station["Temp_deg_Cel"] = CA006114979_station['Data_Value']/10
# Remove Feb 29th data from this set
CA006114979_station = CA006114979_station[~(CA006114979_station['Date'].str.endswith(r'02-29'))]
date_time = pd.DatetimeIndex(CA006114979_station['Date'])

# Separate 2015 data in another dataframe
station_2015 = CA006114979_station[(CA006114979_station['Date'].str.startswith(r'2015-'))]
station_before_2015 = CA006114979_station[~(CA006114979_station['Date'].str.startswith(r'2015-'))]

station_before_2015['Year'], station_before_2015['Month-Date'] = zip(
    *station_before_2015['Date'].apply(lambda x: (x[:4], x[5:])))
station_2015['Year'], station_2015['Month-Date'] = zip(
    *station_2015['Date'].apply(lambda x: (x[:4], x[5:])))

# print(station_2015)
# print(station_before_2015)

# Get minimum and maximum temperature for each day of the year for the period 2005 to 2014
mintemp_before2015 = station_before_2015[(station_before_2015['Element'] == 'TMIN')].groupby(
    'Month-Date').aggregate({'Temp_deg_Cel': np.min})
maxtemp_before2015 = station_before_2015[(station_before_2015['Element'] == 'TMAX')].groupby(
    'Month-Date').aggregate({'Temp_deg_Cel': np.max})

# print(mintemp_before2015)
# print(maxtemp_before2015)

# Separate the minimum and maximum temperatures in two dataframes
mintemp_2015 = station_2015[(station_2015['Element'] == 'TMIN')].groupby(
    'Month-Date').aggregate({'Temp_deg_Cel': np.min})
maxtemp_2015 = station_2015[(station_2015['Element'] == 'TMAX')].groupby(
    'Month-Date').aggregate({'Temp_deg_Cel': np.max})

# Rename columns
mintemp_2015 = mintemp_2015.rename(index=str, columns={'Temp_deg_Cel': 'Temp_deg_Cel_15'})
maxtemp_2015 = maxtemp_2015.rename(index=str, columns={'Temp_deg_Cel': 'Temp_deg_Cel_15'})

# print(mintemp_2015)
# print(maxtemp_2015)

# Concatenate the two data frames - before 2015 & 2015 temp data
result_mintemp = pd.concat([mintemp_before2015, mintemp_2015], axis=1)
result_maxtemp = pd.concat([maxtemp_before2015, maxtemp_2015], axis=1)

# print(result_mintemp)
# print(result_maxtemp)

# Identify the indexes for minimum and maximum temperature outliers
minimum_temp_outlier = np.where(
    result_mintemp['Temp_deg_Cel_15'] < result_mintemp['Temp_deg_Cel'])[0]
maximum_temp_outlier = np.where(
    result_maxtemp['Temp_deg_Cel_15'] > result_maxtemp['Temp_deg_Cel'])[0]

print(minimum_temp_outlier)
print(maximum_temp_outlier)

# Plot the minimum and maximum temperature
fig = plt.figure(1, figsize=(11, 6))
plt.subplot(111)
plt.plot(mintemp_before2015.values, lw=1, color='blue')
plt.plot(maxtemp_before2015.values, lw=1, color='red')
plt.xlabel("Day of the year")
plt.ylabel("Temperature in degree Celcius")
plt.title("Record low & high temperature for each day of the year (2005-2014) \n Recorded by station at Markdale, Ontario")
plt.fill_between(range(len(mintemp_before2015)),
                 mintemp_before2015['Temp_deg_Cel'], maxtemp_before2015['Temp_deg_Cel'], color="grey", alpha=0.5)

# Scatter plot to show the outliers above max temp or below min temp for the year 2015 compared to the period 2005-2014
#X_index = minimum_temp_outlier.index
min_temp = plt.scatter(minimum_temp_outlier, result_mintemp.iloc[minimum_temp_outlier]
                       ['Temp_deg_Cel_15'], alpha=0.9, color='aqua', edgecolors='black', marker='v')
max_temp = plt.scatter(maximum_temp_outlier, result_maxtemp.iloc[maximum_temp_outlier]
                       ['Temp_deg_Cel_15'], alpha=0.9, color='orange', edgecolors='black', marker='^')

plt.legend((min_temp, max_temp),
           ("2015 minimum temp. below record low temp. from period 2005-2014",
            "2015 maximum temp. above record high temp. from period 2005-2014"),
           loc='lower right')

fig.savefig('temp_plot.png')
