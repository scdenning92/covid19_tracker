#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:19:51 2020

@author: chris
"""

import pandas as pd


## Read NYT case and death data per state per day
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
df = pd.read_csv(url)

## need to do roundabout way of getting daily differences
states = df['state'].unique().tolist()
out = []
for s in states:
    minidf = df[df['state']==s]
    minidiff = minidf[['date', 'cases', 'deaths']].sort_values(['date'])
    minidiff = minidiff.set_index('date').diff().reset_index()
    minidiff['state'] = s
    minidiff = minidiff[['date', 'state', 'cases', 'deaths']]
    out.append(minidiff)
df = pd.concat(out)



##
##  Create country df and create 7-day moving average for state level and national
##
rolling = df.set_index('date').groupby('state').rolling(7)[['cases', 'deaths']].mean().reset_index()
rolling = rolling.dropna(how='any')

national = df[['date', 'cases', 'deaths']].groupby('date').sum().reset_index()
nationalrolling = national.set_index('date').rolling(7)[['cases', 'deaths']].mean().reset_index()

##
##  Find weekly difference in 7-day average by state (first derivative over a week)
##

for s in states:
    print(s)
    minidf = rolling[rolling['state']==s]
    plt.plot(minidf['cases'])
    plt.show()





