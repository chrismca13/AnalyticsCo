

import pandas as pd
import numpy as np
from datetime import datetime
from meteostat import Daily, Point


# Time period
start = datetime(2023, 8, 1)
#end = datetime(2025, 1, 1)
end = datetime.now()

# Define location(s):
vancouver = Point(49.2497, -123.1193, 70)
toronto = Point(43.65, -79.38, 20)

sf = Point(37.7749, -122.4194, 20)
newyork = Point(40.7, -74, 50)
detroit = Point(42.3, -83.04, 200)
denver = Point(39.7392, -104.9903, 1608)

london = Point(51.5072, -0.1276, 21)
paris = Point(48.86, -2.35, 35)
prague = Point(50.08, 14.44, 200)

istanbul = Point(41.008, 28.978, 40)
moscow = Point(55.75, 37.62, 156)
beijing = Point(39.9042, 116.407, 40)
tokyo = Point(35.676, 139.650, 40)


# base df (with prague)
# Get daily data
data = Daily(prague, start, end)
data = data.fetch()
data['City'] = 'Prague'

cities = [vancouver, toronto, sf, newyork, detroit, denver, london, paris, istanbul, moscow, beijing, tokyo]
city_names = ['Vancouver', 'Toronto', 'San Francisco', 'NewYork', 'Detroit', 
              'Denver', 'London', 'Paris', 'Istanbul', 'Moscow', 'Beijing', 'Tokyo']


for i, j in zip(cities, city_names):
    
    data_i = Daily(i, start, end)
    data_i = data_i.fetch()
    data_i['City'] = j
    
    
    data = pd.concat([data, data_i])



# Create dictionaries to rename cities as countries, continents
city_names_2 = ['Vancouver', 'Toronto', 'San Francisco', 'NewYork', 'Detroit', 
              'Denver', 'London', 'Paris', 'Istanbul', 'Moscow', 'Beijing', 'Tokyo', 'Prague']

countries = ['Canada', 'Canada', 'USA', 'USA', 'USA', 'USA', 'UK', 
             'France', 'Turkey', 'Russia', 'China', 'Japan', 'Prague']

continents = ['North America', 'North America', 'North America', 'North America', 'North America'
             , 'North America', 'Europe', 'Europe', 'Asia', 'Europe', 'Asia', 'Asia', 'Europe']

country_dict = dict(zip(city_names_2, countries))
continent_dict = dict(zip(city_names_2, continents))

# rename using map function
data['Country'] = data['City'].map(country_dict)
data['Cont'] = data['City'].map(continent_dict)

# Pull out date from index and rename as 'Date'
data = data.reset_index()\
           .rename({'index': 'Date'}, axis = 1)

# Categorize wind directions into cardinal direction

data['wdir'] = data['wdir'].fillna(0)
data['wdir'] = data['wdir'].astype(int)

def func(row):
    if row['wdir'] >45 & row['wdir'] <135 :
        return 'East'
    elif row['wdir'] > 135 & row['wdir'] < 225:
        return 'South' 
    elif row['wdir'] > 225 & row['wdir'] < 315:
        return 'West' 
    
    else:
        return 'North'

data['Wind Direction'] = data.apply(func, axis=1)

# Code to convert date to season 
# code from: https://stackoverflow.com/questions/60285557/extract-seasons-from-datetime-pandas

date = data.Date.dt.month*100 + data.Date.dt.day
data['Season'] = (pd.cut(date,[0,321,620,922,1220,1300],
                       labels=['Winter','Spring','Summer','Autumn','Winter '])
                  .str.strip()
               )

# Below Freezing Flag

data['Below Freezing'] = np.where(data['tmin'] <= 0, 'Yes', 'No')

# Fill N/A's
data['prcp'] = data['prcp'].fillna(0)
data['snow'] = data['snow'].fillna(0)

# Convert to farenheit
data['tavg'] = (data['tavg'] * 1.8) + 32
data['tmin'] = (data['tmin'] * 1.8) + 32
data['tmax'] = (data['tmax'] * 1.8) + 32

# Convert wind to MPH for KMH
data['wspd'] = 0.6214 * data['wspd']

print(data)