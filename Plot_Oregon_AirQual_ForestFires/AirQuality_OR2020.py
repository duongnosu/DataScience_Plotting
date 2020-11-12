
import matplotlib.dates as mdates
from datetime import date as dt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook
%matplotlib inline
#######
s_date = date(2020, 2, 19)
e_date = date(2020, 10, 13)
delta = s_date - e_date
print(delta.days)
s = date(2020, 6, 13)
e = date(2020, 8, 13)
d = e-s
print(d.days)

######

# https://apps.odf.oregon.gov/DIVISIONS/protection/fire_protection/fires/FIRESlist.asp
# OR Fire Report


def get_clean_fire():
    df_fire = pd.read_csv('OR_Fire.csv')

    df_clean = df_fire[['Report Date', 'Total Acres']]
    df_clean = df_clean.rename(columns={"Report Date": "Date", "Total Acres": "Total Burnt"})

    df_clean['Date'] = pd.to_datetime(df_clean['Date'])

    #s = df.resample('M', on='last_payout')['amount'].sum()
    df_clean = df_clean.resample('D', on='Date')['Total Burnt'].sum()
    #df_clean = df_clean['Total'].groupby(df_clean['Date'].dt.to_period('D')).sum()

    # df_fire = df_fire.drop(['Fire Year', 'Fire Name', 'Legal', 'Fire Number',
    #                         'District', 'Unit', 'County', 'Fuel Model', 'General Cause'], axis=1).dropna()

    # df_fire['Report Date'] = pd.to_datetime(df_fire['Report Date'])
    #
    # #df_fire['Report Date'] = pd.to_datetime(df_fire['Report Date']).dt.date.value_counts().rename('sum').to_frame()
    #
    # #df_fire.set_index('Report Date')
    # df_fire['Total Acres'] = df_fire[df_fire['Total Acres'] != 0]
    # df_fire = df_fire.sort_values(by='Report Date', ascending=True)
    # df_fire = df_fire.rename(columns={"Report Date": "Date", "Total Acres": "Total"})
    # df_fire = df_fire['Total'].groupby(df_fire['Date'].dt.to_period('D')).sum()

    return df_clean.loc[s_date:e_date]


df_fire = get_clean_fire()

df_fire = df_fire.to_frame()
df_fire = df_fire[0:238]

df_fire.tail(1)
test = pd.date_range(start=s_date, end=e_date).difference(df_fire.index)
test

# Corvallis ID  AQS 410030013
# Corvallis CBSA Code 18700
# Oregon State Code 41 |Benton 3|
# unit ug/m3 LC


def get_AQI_OR():
    df_pm25 = pd.read_csv('OR_PM25_2020.csv')

    df_pm25 = df_pm25[(df_pm25['Site ID'] == 410030013)]

    df_clean = df_pm25[['Date', 'Daily Mean PM2.5 Concentration',
                        'DAILY_AQI_VALUE']]
    df_clean = df_clean.set_index(pd.DatetimeIndex(df_clean['Date']))

    # This will filled the date with no data to 0
    return df_clean.loc[s_date:e_date].resample('D').sum()


df_OR = get_AQI_OR()
df_OR
test2 = pd.date_range(start=s_date, end=e_date).difference(df_OR.index)
test2


def get_AQI_MI():
    df_pm25 = pd.read_csv('MI_ANN_PM25_2020.csv')

    df_clean = df_pm25[['Date', 'Daily Mean PM2.5 Concentration',
                        'DAILY_AQI_VALUE']]
    df_clean = df_clean.set_index(pd.DatetimeIndex(df_clean['Date']))

    return df_clean


#
df_MI = get_AQI_MI()
#

# Graph


def graph_f():
    fig, ax1 = plt.subplots(figsize=(9, 6))

    color = 'tab:red'
    ax1.set_xlabel('Date in 2020')
    ax1.set_ylabel('Daily PM2.5 in ug/m3', color=color)

    ax1.tick_params(axis='y', labelcolor=color)
    ##
    xfmt = mdates.DateFormatter('%b')
    months = mdates.MonthLocator()
    ax1.xaxis.set_major_locator(months)
    ax1.xaxis.set_major_formatter(xfmt)

    ax1.plot(df_fire.index, df_OR['DAILY_AQI_VALUE'], color=color, alpha=0.9)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    #

    color = 'tab:blue'
    ax2.set_ylabel('Burned area in acres', color=color)  # we already handled the x-label with ax1
    ax2.xaxis.set_major_locator(months)
    ax2.xaxis.set_major_formatter(xfmt)
    ax2.plot(df_fire.index, df_fire['Total Burnt'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title("Corvallis air quality vs forest fire in OR")
    plt.xticks(rotation=90)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.axis('equal')
    plt.show()


g = graph_f()


###########################################################################

###########################################################################
plt.figure(figsize=(10, 6))
ax = plt.gca()

df_MI.plot(x='Date', y='DAILY_AQI_VALUE', ax=ax, kind='line', color='blue', label='Ann Arbor, MI ')

df_OR.plot(x='Date', y='DAILY_AQI_VALUE', ax=ax, kind='line',
           color='orange', label='Corvallis, OR ')
plt.ylabel('AQI value in ug/m3')
# df.plot(x='Report Date', y='Total Acres', ax=ax, kind='bar')
plt.title('Outdoor Airquality PM2.5 Pollutant')
plt.legend(loc='upper left')
# plt.savefig('AS4.png')
plt.show()

df_clean.plot(kind='line', colormap='viridis')
