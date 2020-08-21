#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
get_ipython().system('conda install -c conda-forge geopy --yes ')


# In[99]:


from geopy.geocoders import Nominatim 
import folium 
import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import json # library to handle JSON files

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

#import types
#from botocore.client import Config
#import ibm_boto3

import types
import pandas as pd



print('Libraries imported.')


# # Data Import

# ## Montreal

# In[100]:


Montreal_Boroughs_Neighborhoods = pd.read_excel('Montreal_BN.xlsx')
Montreal_Boroughs_Neighborhoods.head()


# In[101]:


for index, row in Montreal_Boroughs_Neighborhoods.iterrows():
    #address = ('Montreal, QC')
    address = (Montreal_Boroughs_Neighborhoods.loc[index,'Neighborhood'] + ' ' + Montreal_Boroughs_Neighborhoods.loc[index,'Borough'] + ', ' + 'Montreal, QC')
    #print(address)
   

    try:
        geolocator = Nominatim(user_agent="mtl")
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude
        #print(index)
        #print(address, latitude, longitude)
        Montreal_Boroughs_Neighborhoods.at[index,'Latitude'] = latitude
        Montreal_Boroughs_Neighborhoods.at[index,'Longitude'] = longitude
    except Exception as inst:
        print(address, inst)


# In[102]:


Montreal_Boroughs_Neighborhoods


# In[103]:


#manual input for some neighborhoods

#vieux montreal
Montreal_Boroughs_Neighborhoods.at[32,'Latitude']= 45.506185
Montreal_Boroughs_Neighborhoods.at[32,'Longitude']= -73.552501

#golden square mile
Montreal_Boroughs_Neighborhoods.at[35,'Latitude']= 45.500720
Montreal_Boroughs_Neighborhoods.at[35,'Longitude']= -73.576759

#Monkland Village
Montreal_Boroughs_Neighborhoods.at[2,'Latitude']= 45.473579
Montreal_Boroughs_Neighborhoods.at[2,'Longitude']= -73.624739

#Cote St-Paul
Montreal_Boroughs_Neighborhoods.at[16,'Latitude']= 45.458284
Montreal_Boroughs_Neighborhoods.at[16,'Longitude']= -73.588441

#Cité Jardin
Montreal_Boroughs_Neighborhoods.at[24,'Latitude']= 45.570745
Montreal_Boroughs_Neighborhoods.at[24,'Longitude']= -73.562063


#Hochelaga-Maisonneuve
Montreal_Boroughs_Neighborhoods.at[19,'Latitude']= 45.548629
Montreal_Boroughs_Neighborhoods.at[19,'Longitude']= -73.542369

#Le Village
Montreal_Boroughs_Neighborhoods.at[31,'Latitude']= 45.518436
Montreal_Boroughs_Neighborhoods.at[31,'Longitude']= -73.557311


#Parc La Fontaine
Montreal_Boroughs_Neighborhoods.at[5,'Latitude']= 45.528877
Montreal_Boroughs_Neighborhoods.at[5,'Longitude']= -73.571184

#Ville-Émard
Montreal_Boroughs_Neighborhoods.at[17,'Latitude']= 45.454925
Montreal_Boroughs_Neighborhoods.at[17,'Longitude']= -73.598675

#Angus
Montreal_Boroughs_Neighborhoods.at[22,'Latitude']= 45.546780
Montreal_Boroughs_Neighborhoods.at[2,'Longitude']= -73.563897


Montreal_Boroughs_Neighborhoods.drop(Montreal_Boroughs_Neighborhoods.index[[30]])


# # Vancouver

# In[104]:


Vancouver_Boroughs_Neighborhoods  = pd.read_excel('Vancouver_BN.xlsx')
Vancouver_Boroughs_Neighborhoods.head()


# In[105]:


for index, row in Vancouver_Boroughs_Neighborhoods.iterrows():
    address = (Vancouver_Boroughs_Neighborhoods.loc[index,'Neighborhood'] + ' Vancouver, BC')
    try:
        geolocator = Nominatim(user_agent="van_explorer")
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude
        Vancouver_Boroughs_Neighborhoods.at[index,'Latitude'] = latitude
        Vancouver_Boroughs_Neighborhoods.at[index,'Longitude'] = longitude
    except Exception as inst:
        print(address, inst)

Vancouver_Boroughs_Neighborhoods


# In[106]:


#manual input for Coal Harbour
Vancouver_Boroughs_Neighborhoods.at[0,'Latitude']= 49.289719
Vancouver_Boroughs_Neighborhoods.at[0,'Longitude']= -123.124657

#manual input for Greektown
Vancouver_Boroughs_Neighborhoods.at[37,'Latitude']= 49.264222
Vancouver_Boroughs_Neighborhoods.at[37,'Longitude']= -123.175944

#manual input for Fairview
Vancouver_Boroughs_Neighborhoods.at[16,'Latitude']= 49.263489
Vancouver_Boroughs_Neighborhoods.at[16,'Longitude']= -123.131395


#manual input for English bay
Vancouver_Boroughs_Neighborhoods.at[3,'Latitude']= 49.287306
Vancouver_Boroughs_Neighborhoods.at[3,'Longitude']= -123.142238

#manual input for Marpole
Vancouver_Boroughs_Neighborhoods.at[20,'Latitude']= 49.211044
Vancouver_Boroughs_Neighborhoods.at[20,'Longitude']= -123.140427


# # Draw neighborhood maps
# 

# In[107]:


# create map of Mont using latitude and longitude values
map_Montreal = folium.Map(location=[45.567428,-73.659098], zoom_start=11)

# add markers to map
for lat, lng, Borough, Neighborhood in zip(Montreal_Boroughs_Neighborhoods['Latitude'], Montreal_Boroughs_Neighborhoods['Longitude'], Montreal_Boroughs_Neighborhoods['Borough'], Montreal_Boroughs_Neighborhoods['Neighborhood']):
    label = '{}, {}'.format(Neighborhood, Borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Montreal)  
    
map_Montreal


# In[108]:


# create map of Vancouver using latitude and longitude values
map_Vancouver = folium.Map(location=[49.290375, -123.129281], zoom_start=11)

# add markers to map
for lat, lng, Borough, Neighborhood in zip(Vancouver_Boroughs_Neighborhoods['Latitude'], Vancouver_Boroughs_Neighborhoods['Longitude'], Vancouver_Boroughs_Neighborhoods['Borough'], Vancouver_Boroughs_Neighborhoods['Neighborhood']):
    label = '{}, {}'.format(Neighborhood, Borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Vancouver)  
    
map_Vancouver


# # Analysis

# #### Define Foursquare credentials

# In[1]:


CLIENT_ID = '' # your Foursquare ID
CLIENT_SECRET = '' # your Foursquare Secret
VERSION = '' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# #### Let's create a function to find out each venues in a neighborhood¶
# 

# In[110]:


def getHoodVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        #print(name)
        LIMIT = 80 # limit of number of venues returned by Foursquare API
        radius = 500 # define radius    
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood',                   'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# #### run the above function on the two cities to gather venues info

# In[111]:


Montreal_venues = getHoodVenues(names=Montreal_Boroughs_Neighborhoods['Neighborhood'],
                                   latitudes=Montreal_Boroughs_Neighborhoods['Latitude'],
                                   longitudes=Montreal_Boroughs_Neighborhoods['Longitude']
                                  )
Vancouver_venues = getHoodVenues(names=Vancouver_Boroughs_Neighborhoods['Neighborhood'],
                                   latitudes=Vancouver_Boroughs_Neighborhoods['Latitude'],
                                   longitudes=Vancouver_Boroughs_Neighborhoods['Longitude']
                                  )


# In[112]:


print("Montreal venues: ", Montreal_venues['Neighborhood'].shape)

print("Vancouver venues: ", Vancouver_venues['Neighborhood'].shape)

Montreal_venues.head()


# #### Let's merge the data from the three cities to compare them¶
# 

# In[127]:



Twocitieshoods = Montreal_Boroughs_Neighborhoods

Twocitieshoods = Twocitieshoods.append(Vancouver_Boroughs_Neighborhoods)


Twocitieshoods.head()


# In[128]:


Twocitiesvenues = Montreal_venues
Twocitiesvenues = Twocitiesvenues.append(Vancouver_venues)

# Let's re-categorize the venues to have less and obtain better results
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Accessories Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['American Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Art Gallery'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Arts & Crafts Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Asian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Athletics & Sports'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Australian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Auto Workshop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Automotive Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['BBQ Joint'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bagel Shop'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bakery'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bank'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Beach'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Beer Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Beer Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Belgian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bike Rental / Bike Share'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bistro'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Boat or Ferry'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bookstore'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Boutique'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bowling Alley'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Boxing Gym'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Brazilian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Breakfast Spot'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Brewery'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bridal Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bubble Tea Shop'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Burger Joint'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Burrito Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bus Line'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bus Station'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bus Stop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Business Service'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Butcher'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Café'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cajun / Creole Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Canal'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Candy Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Caribbean Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cheese Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Chinese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Chocolate Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Church'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Circus'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Clothing Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cocktail Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Coffee Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Comedy Club'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Concert Hall'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Construction & Landscaping'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Convenience Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cosmetics Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Creperie'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cuban Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Deli / Bodega'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Department Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dessert Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dim Sum Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Diner'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Discount Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dog Run'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Donut Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dumpling Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Electronics Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['English Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Ethiopian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Falafel Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Farmers Market'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Fast Food Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Filipino Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Fish & Chips Shop'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Fish Market'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Flower Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Food'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Food & Drink Shop'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Food Court'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Food Truck'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['French Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Fried Chicken Joint'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Frozen Yogurt Shop'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Furniture / Home Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gaming Cafe'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Garden'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gas Station'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gastropub'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['German Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gift Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gourmet Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Greek Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Grocery Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gun Range'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gun Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gym'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gym / Fitness Center'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gym Pool'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Harbor / Marina'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hardware Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hawaiian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Health Food Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Historic Site'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hobby Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hockey Arena'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hookah Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hostel'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hotel'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hotel Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hotpot Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Ice Cream Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Indian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Indie Movie Theater'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Indonesian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Irish Pub'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Italian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Japanese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Jewelry Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Juice Bar'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Karaoke Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Korean Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Latin American Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Leather Goods Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Lebanese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Lingerie Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Liquor Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Lounge'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Mac & Cheese Joint'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Malay Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Marijuana Dispensary'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Market'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Massage Studio'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Medical Center'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Mediterranean Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(["Men's Store"], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Metro Station'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Mexican Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Middle Eastern Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Miscellaneous Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Modern European Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Mongolian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Moroccan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Movie Theater'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Museum'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Music Venue'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Nail Salon'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['New American Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Nightclub'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Noodle House'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Office'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Optical Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Outdoor Sculpture'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Paper / Office Supplies Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Park'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Performing Arts Venue'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pet Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pharmacy'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pizza Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Playground'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Plaza'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Poke Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pool'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Portuguese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pub'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Racetrack'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Ramen Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Record Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Recording Studio'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Recreation Center'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Rental Car Location'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Rock Club'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Roof Deck'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Salon / Barbershop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Salvadoran Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sandwich Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sausage Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Scandinavian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Scenic Lookout'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Science Museum'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sculpture Garden'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Seafood Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Shabu-Shabu Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Shanghai Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Shipping Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Shoe Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Shopping Mall'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Skate Park'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Skating Rink'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Smoke Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Snack Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Soccer Field'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['South American Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Spa'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Spanish Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Speakeasy'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sporting Goods Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sports Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Stationery Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Steakhouse'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Supermarket'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sushi Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Szechuan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Taco Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tapas Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tea Room'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tech Startup'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tennis Court'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Thai Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Theater'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Theme Park'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Theme Park Ride / Attraction'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Thrift / Vintage Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tibetan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tiki Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Toy / Game Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Trade School'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Trail'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Turkish Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Vegetarian / Vegan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Video Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Vietnamese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Water Park'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Whisky Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Wine Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Wine Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(["Women's Store"], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Yoga Studio'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Zoo'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Board Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Boat Rental'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Botanical Garden'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cambodian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Camera Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Comfort Food Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cupcake Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dance Studio'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Event Space'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gay Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Health & Beauty Service'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Heliport'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Himalayan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['History Museum'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Hot Dog Joint'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Japanese Curry Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Library'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Martial Arts School'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Mobile Phone Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['North Indian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Persian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pie Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pool Hall'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Poutine Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Public Art'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Residential Building (Apartment / Condo)'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Russian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Salad Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['South Indian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Swiss Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tex-Mex Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Train Station'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Warehouse Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Wings Joint'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Afghan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['African Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Airport Terminal'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Amphitheater'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Antique Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Arcade'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Arepa Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Art Museum'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Auto Garage'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Baseball Field'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Baseball Stadium'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bed & Breakfast'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Beer Garden'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bike Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bridge'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Building'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Burmese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cafeteria'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Cantonese Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Climbing Gym'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['College Gym'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['College Rec Center'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Community Center'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dive Bar'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Eastern European Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Empanada Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Escape Room'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Fair'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Financial or Legal Service'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Football Stadium'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Fruit & Vegetable Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Gluten-free Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Golf Course'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Herbs & Spices Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Home Service'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['IT Services'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Inn'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Insurance Office'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Intersection'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Jazz Club'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Jewish Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Kitchen Supply Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Lake'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Laundromat'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Light Rail Station'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Molecular Gastronomy Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Motorcycle Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Opera House'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Other Great Outdoors'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Outdoor Supply Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pastry Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Peruvian Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pier'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Planetarium'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Polish Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Print Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Real Estate Office'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Rock Climbing Spot'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Shopping Plaza'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Soccer Stadium'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Social Club'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Soup Place'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Southern / Soul Food Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Sri Lankan Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Stadium'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tattoo Parlor'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tennis Stadium'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Track'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Strip Club'], 'Nightlife Spot')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Basketball Court'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Track'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Track'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['ATM'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Adult Boutique'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Rest Area'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['College Science Building'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Music Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pet Café'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pet Café'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['University'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tunnel'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Tailor Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Student Center'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Mattress Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Waterfall'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Ski Area'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['College Theater'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['General Entertainment'], 'Arts & Entertainment')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Kids Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Photography Studio'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Baby Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['School'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Pop-Up Shop'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['College Bookstore'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Carpet Store'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Post Office'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['General Travel'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Bike Trail'], 'Outdoors & Recreation')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Kebab Restaurant'], 'Food')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Dry Cleaner'], 'Shop & Service')
Twocitiesvenues['Venue Category'] = Twocitiesvenues['Venue Category'].replace(['Comic Shop'], 'Shop & Service')

print('There are {} uniques categories.'.format(len(Twocitiesvenues['Venue Category'].unique())))
Twocitiesvenues.head()


# #### Use one-hot encoding to display venues
# 

# In[129]:


# one hot encoding
Twocitiesvenues_onehot = pd.get_dummies(Twocitiesvenues[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
Twocitiesvenues_onehot['Neighborhood'] = Twocitiesvenues['Neighborhood'] 

# move neighborhood column to the first column
#fixed_columns = [Threecitiesvenues_onehot.columns[-22]] + list(Threecitiesvenues_onehot.columns[:-1])
#Threecitiesvenues_onehot = Threecitiesvenues_onehot[fixed_columns]


col_name="Neighborhood"
first_col = Twocitiesvenues_onehot.pop(col_name)
Twocitiesvenues_onehot.insert(0, col_name, first_col)

Twocitiesvenues_onehot.head()


# In[130]:


Twocitiesvenues_grouped = Twocitiesvenues_onehot.groupby('Neighborhood').sum().reset_index()
Twocitiesvenues_grouped = Twocitiesvenues_grouped 
Twocitiesvenues_grouped.head()


# #### We can find out the top venue categories per neighborhood
# 

# In[131]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# In[132]:


num_top_venues = 5

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighborhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
Twocitiesvenues_sorted = pd.DataFrame(columns=columns)
Twocitiesvenues_sorted['Neighborhood'] = Twocitiesvenues_grouped['Neighborhood']

for ind in np.arange(Twocitiesvenues_grouped.shape[0]):
    Twocitiesvenues_sorted.iloc[ind, 1:] = return_most_common_venues(Twocitiesvenues_grouped.iloc[ind, :], num_top_venues)

Twocitiesvenues_sorted.head()


# In[133]:


Twocitiesvenues_sorted1 = Twocitiesvenues_sorted

#Twocitiesvenues_sorted1.drop("Neighborhood",1)
Twocitiesvenues_sorted1 = Twocitiesvenues_sorted1.replace("Shop & Service", 0)
Twocitiesvenues_sorted1 = Twocitiesvenues_sorted1.replace("Food", 1)
Twocitiesvenues_sorted1 = Twocitiesvenues_sorted1.replace("Outdoors & Recreation", 2)
Twocitiesvenues_sorted1 = Twocitiesvenues_sorted1.replace("Nightlife Spot", 3)
Twocitiesvenues_sorted1 = Twocitiesvenues_sorted1.replace("Arts & Entertainment", 4)
Twocitiesvenues_sorted1 = Twocitiesvenues_sorted1.drop('Neighborhood',1)  
Twocitiesvenues_sorted1


# #### We can now cluster the neighborhoods to see which one from which city fit together¶
# 

# In[134]:


# set number of clusters
kclusters = 9
Twocitiesvenues_clustering = Twocitiesvenues_grouped.drop('Neighborhood', 1)
Twocitiesvenues_clustering = Twocitiesvenues_clustering * 1


# run k-means clustering
#kmeans = KMeans(n_clusters=kclusters,random_state=0).fit(Twocitiesvenues_clustering)
kmeans = KMeans(n_clusters=kclusters,random_state=0).fit(Twocitiesvenues_sorted1)
kmeans.labels_


# #### Let's put back the neighborhood and their respective city in the dataframe
# 

# In[174]:


# add clustering labels
Twocitiesvenues_sorted.insert(0, 'Cluster Labels', kmeans.labels_)

Twocitiesvenues_merged = Twocitieshoods

Twocitiesvenues_merged = Twocitiesvenues_merged.join(Twocitiesvenues_sorted.set_index('Neighborhood'), on='Neighborhood')

Twocitiesvenues_merged.head()


# #### Let's examine the clusters:¶
# 

# In[175]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 0, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# ### create map of Vancouver' Cluster 0 neighborhoods using latitude and longitude values

# In[176]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 0, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[177]:


mapVan = Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 0]
mapVan = mapVan.loc[mapVan['City'] == "Vancouver"]
mapVan


# In[182]:


# create map of Vancouver' Cluster 2 neighborhoods using latitude and longitude values
map_Vancouver = folium.Map(location=[49.290375, -123.129281], zoom_start=12)

# add markers to map
for lat, lng, Borough, Neighborhood in zip(mapVan['Latitude'], mapVan['Longitude'], mapVan['Borough'], mapVan['Neighborhood']):
    label = '{}, {}'.format(Neighborhood, Borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Vancouver)  
    
map_Vancouver


# In[173]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 1, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[154]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 2, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[155]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 3, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[156]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 4, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[157]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 5, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[158]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 6, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[159]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 7, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# In[160]:


Twocitiesvenues_merged.loc[Twocitiesvenues_merged['Cluster Labels'] == 8, Twocitiesvenues_merged.columns[[0] + [1] + [2] + list(range(5, Twocitiesvenues_merged.shape[1]))]]


# ## Let's look at spider plots of each cluster

# In[161]:


Twocitiesvenues_grouped.insert(0, 'Clusters', kmeans.labels_)
Twocitiesvenues_grouped.head()


# In[162]:


var0 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 0].mean(axis = 0)  
df0 = pd.DataFrame(var0)
df0.columns = ['0']

var1 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 1].mean(axis = 0)  
df1 = pd.DataFrame(var1)
df1.columns = ['1']

var2 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 2].mean(axis = 0)  
df2 = pd.DataFrame(var2)
df2.columns = ['2']

var3 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 3].mean(axis = 0)  
df3 = pd.DataFrame(var3)
df3.columns = ['3']

var4 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 4].mean(axis = 0)  
df4 = pd.DataFrame(var4)
df4.columns = ['4']

var5 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 5].mean(axis = 0)  
df5 = pd.DataFrame(var5)
df5.columns = ['5']

var6 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 6].mean(axis = 0)  
df6 = pd.DataFrame(var6)
df6.columns = ['6']

var7 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 7].mean(axis = 0)  
df7 = pd.DataFrame(var7)
df7.columns = ['7']

var8 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 8].mean(axis = 0)  
df8 = pd.DataFrame(var8)
df8.columns = ['8']

var9 = Twocitiesvenues_grouped.loc[Twocitiesvenues_grouped['Clusters'] == 9].mean(axis = 0)  
df9 = pd.DataFrame(var9)
df9.columns = ['9']

dftotal = df0
dftotal['1'] = df1
dftotal['2'] = df2
dftotal['3'] = df3
dftotal['4'] = df4
dftotal['5'] = df5
dftotal['6'] = df6
dftotal['7'] = df7
dftotal['8'] = df8
#dftotal['9'] = df9
dftotal = dftotal.transpose() 
dftotal["Clusters"] = dftotal["Clusters"].astype("str")
dftotal


# In[167]:


# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# ------- PART 1: Define a function that do a plot for one line of the dataset!
 
def make_spider( row, title, color):
 
    # number of variable
    categories=list(dftotal)[1:]
    N = len(categories)
 
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
 
    # Initialise the spider plot
    ax = plt.subplot(3,3,row+1, polar=True, )
 
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
 
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)
 
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0,20,40], ["0","20","40"], color="grey", size=7)
    plt.ylim(0,40)
 
    # Ind1
    values=dftotal.iloc[row].drop('Clusters').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)
 
    # Add a title
    plt.title(title, size=11, color=color, y=1.1)
 


# In[168]:


# ------- PART 2: Apply to all individuals
# initialize the figure
my_dpi=80
plt.figure(figsize=(1400/my_dpi, 1200/my_dpi), dpi=my_dpi)
 
# Create a color palette:
my_palette = plt.cm.get_cmap("Set2", len(dftotal.index))
 
# Loop to plot
for row in range(0, len(dftotal.index)):
    make_spider( row=row, title='Cluster '+dftotal['Clusters'][row], color=my_palette(row))
    
plt.show(block=False)


# ## Content-based recommender system
# 

# Let's use a content-based recommender system by asking the user his opinion of eight Montreal neighborhoods. 
# Each neighboroods is in a different cluster

# Let's prepare the user input matrix

# In[169]:


input0 = input("Out of the following neighborhoods: give a value of 2 to neighborhoods you would live in. A value of 1 if you are ambivalent. A value of 0 where you would not live. Village Monkland: ")
userinput = pd.DataFrame({'Village Monkland': [input0]})

#Parc La Fontaine  
input1= input("Parc La Fontaine: ")
userinput['Parc La Fontaine'] = input1

#Le Plateau 
input2= input("Le Plateau: ")
userinput['Le Plateau'] = input2

#Griffintown
input3= input("Griffintown: ")
userinput['Griffintown'] = input3

#Saint-Henri cluster
input4 = input("Saint-Henri: ")
userinput['Saint-Henri'] = input4

#Hochelaga-Maisonneuve  
input5= input("Hochelaga-Maisonneuve: ")
userinput['Hochelaga-Maisonneuve'] = input5


#L’Île-des-Sœurs 
input6 = input("L’Île-des-Sœurs: ")
userinput['L’Île-des-Sœurs'] = input6


#Quartier Latin 
input7 = input("Quartier Latin: ")
userinput["Quartier Latin"] = input7

#Saint-Michel 
input8 = input("Saint-Michel: ")
userinput['Saint-Michel'] = input8


userinput = userinput.astype(float)
userinput = userinput.T
userinput.columns = ['ratings']

userinput.to_numpy()


# # Let's prepare the Neighborhood matrix

# In[184]:



Twocitiesvenues_merged1 = Twocitieshoods
Twocitiesvenues_merged1 = Twocitiesvenues_merged1.join(Twocitiesvenues_grouped.set_index('Neighborhood'), on='Neighborhood')
Twocitiesvenues_merged1 = Twocitiesvenues_merged1.drop('Latitude',1).drop('Longitude',1).drop('Borough',1).drop('City',1).drop('Clusters',1)

#Let's normalize the categories
Twocitiesvenues_merged1= Twocitiesvenues_merged1[Twocitiesvenues_merged1["Neighborhood"].isin(["Parc La Fontaine","Le Plateau","Griffintown","Quartier Latin","Hochelaga-Maisonneuve","L’Île-des-Sœurs","Saint-Michel","Hochelaga-Maisonneuve","Village Monkland","Saint-Henri"])]
#Twocitiesvenues_merged1["Sum"]= Twocitiesvenues_merged1["Arts & Entertainment"] + Twocitiesvenues_merged1["Shop & Service"] + Twocitiesvenues_merged1["Outdoors & Recreation"] + Twocitiesvenues_merged1["Nightlife Spot"] + Twocitiesvenues_merged1["Food"] 
#Twocitiesvenues_merged1["Arts & Entertainment"] = Twocitiesvenues_merged1["Arts & Entertainment"] / Twocitiesvenues_merged1["Sum"]
#Twocitiesvenues_merged1["Shop & Service"] = Twocitiesvenues_merged1["Shop & Service"] / Twocitiesvenues_merged1["Sum"]
#Twocitiesvenues_merged1["Outdoors & Recreation"] = Twocitiesvenues_merged1["Outdoors & Recreation"] / Twocitiesvenues_merged1["Sum"]
#Twocitiesvenues_merged1["Nightlife Spot"] = Twocitiesvenues_merged1["Nightlife Spot"] / Twocitiesvenues_merged1["Sum"]
#Twocitiesvenues_merged1["Food"] = Twocitiesvenues_merged1["Food"] / Twocitiesvenues_merged1["Sum"]

#Twocitiesvenues_merged1 = Twocitiesvenues_merged1.drop('Sum',1)
Twocitiesvenues_merged1=Twocitiesvenues_merged1.reset_index(drop=True)
#Twocitiesvenues_merged1 = Twocitiesvenues_merged1.T
Twocitiesvenues_merged1


# In[185]:


Twocitiesvenues_merged1 = Twocitiesvenues_merged1.drop('Neighborhood',1)
Twocitiesvenues_merged1=Twocitiesvenues_merged1.to_numpy()
Twocitiesvenues_merged1


# ### Let's prepare the user profile

# we need to do a dot multiplication (Hadamard product) of the user input and the and neighborhood weighted matrix. Then we normalize the results

# In[186]:


weighted_cat = np.array(userinput) * np.array(Twocitiesvenues_merged1)
weighted_cat


# In[187]:


userprofile= pd.DataFrame(weighted_cat)
userprofile= userprofile.sum()
userprofile = pd.DataFrame(userprofile)
userprofile = userprofile.T
userprofile.columns=["Arts & Entertainment", "Food", "Nightlife Spot","Outdoors & Recreation","Shop & Service"]

userprofile


# In[188]:


userprofile["Sum"]= userprofile["Arts & Entertainment"] + userprofile["Food"] + userprofile["Nightlife Spot"] + userprofile["Outdoors & Recreation"]+ userprofile["Shop & Service"]  
userprofile["Arts & Entertainment"] = userprofile["Arts & Entertainment"] / userprofile["Sum"]
userprofile["Food"] = userprofile["Food"] / userprofile["Sum"]
userprofile["Nightlife Spot"] = userprofile["Nightlife Spot"] / userprofile["Sum"]
userprofile["Outdoors & Recreation"] = userprofile["Outdoors & Recreation"] / userprofile["Sum"]
userprofile["Shop & Service"] = userprofile["Shop & Service"] / userprofile["Sum"]
userprofile = userprofile.drop('Sum',1)
userprofile


# ### Let's find the recommendations

# We need to extract Vancouver's neighborhood and their weighted characteristics

# In[189]:


Vancouverhoods = Twocitieshoods
Vancouverhoods = Vancouverhoods.join(Twocitiesvenues_grouped.set_index('Neighborhood'), on='Neighborhood')
Vancouverhoods = Vancouverhoods.loc[Vancouverhoods['City'] == 'Vancouver']  
#Vancouverhoods = Vancouverhoods.drop('Latitude',1).drop('Longitude',1).drop('Borough',1).drop('Clusters',1).drop('City',1).drop('Neighborhood',1)

Vancouverhoods.head()


# In[190]:


userprofile = userprofile.T


# In[191]:


userprofile=userprofile.to_numpy()
Vancouverhoods = Vancouverhoods.to_numpy()


# In[192]:


#Multiply the genres by the weights and then take the weighted average
recommendationtable = np.array(userprofile) * np.array(Vancouverhoods)
recommendationtable = pd.DataFrame(recommendationtable)
#recommendationtable.sort_values('ratings', ascending=False, inplace=True)
recommendationtable.columns=["Arts & Entertainment", "Food", "Nightlife Spot","Outdoors & Recreation","Shop & Service"]
recommendationtable["Sum"]= recommendationtable["Arts & Entertainment"] + recommendationtable["Food"] + recommendationtable["Nightlife Spot"] + recommendationtable["Outdoors & Recreation"]+ recommendationtable["Shop & Service"]  

recommendationtable


# In[197]:


Vancouverhoodsrecommendations = Twocitieshoods
Vancouverhoodsrecommendations = Vancouverhoodsrecommendations.join(Twocitiesvenues_grouped.set_index('Neighborhood'), on='Neighborhood')
Vancouverhoodsrecommendations = Vancouverhoodsrecommendations.loc[Vancouverhoodsrecommendations['City'] == 'Vancouver'] 

Vancouverhoodsrecommendations = Vancouverhoodsrecommendations.join(recommendationtable['Sum'])
Vancouverhoodsrecommendations = Vancouverhoodsrecommendations.sort_values('Sum', ascending=False)
Vancouverhoodsrecommendations = Vancouverhoodsrecommendations.reset_index()
Vancouverhoodsrecommendations


# In[198]:


mapVan1 = Vancouverhoodsrecommendations[:10]


# In[199]:


# create map of Vancouver' Cluster 2 neighborhoods using latitude and longitude values
map_Vancouver = folium.Map(location=[49.290375, -123.129281], zoom_start=11)

# add markers to map
for lat, lng, Borough, Neighborhood in zip(mapVan1['Latitude'], mapVan1['Longitude'], mapVan1['Borough'], mapVan1['Neighborhood']):
    label = '{}, {}'.format(Neighborhood, Borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Vancouver)  
    
map_Vancouver


# ## Neighborhoods that are in each study
# 

# In[201]:


summary_recommendations = Vancouverhoodsrecommendations[Vancouverhoodsrecommendations["Neighborhood"].isin(["Chinatown","International Village","Gastown",])]
summary_recommendations


# In[202]:


# create map of Vancouver' Cluster 2 neighborhoods using latitude and longitude values
map_Vancouver = folium.Map(location=[49.290375, -123.129281], zoom_start=11)

# add markers to map
for lat, lng, Borough, Neighborhood in zip(summary_recommendations['Latitude'], summary_recommendations['Longitude'], summary_recommendations['Borough'], summary_recommendations['Neighborhood']):
    label = '{}, {}'.format(Neighborhood, Borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Vancouver)  
    
map_Vancouver

