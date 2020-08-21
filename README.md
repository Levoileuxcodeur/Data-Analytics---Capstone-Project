# Introduction

This project idea is based on my dream to one day move from where I live to another city and be able to find a neighborhood that match my lifestyle.

When moving to a new city, it is difficult to identify which neighborhoods suit our needs without already having spent some time in the city.

Therefore, I created a tool that will allow me to identify what I like in their current neighborhood and find similar neighborhoods in an pther city of my choice.

Grouping factors amgonst will be amount of venues of different categories: Arts & Entertainment, Food shop, Shop and Service, Outdoor & Recreation & Nightlife Spot. (Those categories are Foursquare top-level categories)


# Data

For this study, I compared Montreal and Vancouver, two canadian cities.

I used the following sources to gather data:  

- Several internet pages regarding neighbordhood description
  - Montreal: https://habitermontreal.com/en/discover-the-neighbourhoods
  - Vancouver: https://www.tourismvancouver.com/vancouver/neighbourhoods/
  
- Foursquare data regarding venues of each neighborhoods :
  - https://developer.foursquare.com/docs/api-reference/venues/search/
  - https://developer.foursquare.com/docs/build-with-foursquare/categories/

Starting with the neighborhoods names, I found their latitude and longitude using the Nominatim geolocator API.
I then plotted the neighborhoods on maps using Folium to ensure the accuracy of their position. I corrected several neighborhoods center position manually in my dataset. 
For each neighboroods, I then acquired all venues within a 500 meters radius of their center using the Foursquare Search Venues API. I finally changed each venue category to fit within the five top categories defined by Foursquare: Arts & Entertainment, Food shop, Shop and Service, Outdoor & Recreation & Nightlife Spot.


# Methodology

I wanted to identify Vancouver neighborhoods that resemble Montreal neighborhoods that I like.

To do that, I used two methods to come up with recommendations: a K-means clustering algorithm and a Content-based recommendation algorithm.

#### K-Means clustering:

This Machine Learning method is unsupervised and meant to cluster data. In this method, the user decides on the number of clusters to divide the data into. The algorithm then assigns cluster centroids randomly and assign each data entry to a cluster. Calculating the distance between each point of a given cluster and the centroid of the cluster, the algorithm then moves the centroid. The algorithm loops until the centroids do not move anymore.

For each neighborhoods, I started by ordering the most common to least common categories of venues. It is interesting to understand that I decided to trim down the number of categories from approximately two hundred to five because the K-means algorithm was not able to produce clusters that objectively makes sens from my opinion, given the fact that I know Montreal and Vancouver quite well. With only five venue categories, I am asking the algorithm to work with a five dimensions matrix, which is much easier than with a two hundred dimension matrix. I initially tried to cluster the neighborhood by asking K-means to look only at the number of venues in each of the five categories. It did not yield results as convicing as clustering with most common to least common category type. 

Another interesting point is the K, or number of clusters, that I decided to use. I played with several numbers, ranging between four and twelve. Ultimately, I settled for a K of nine. To do so, I looked at tables of each cluster with each tables showing the most common venues by order. With a value of nine, each table looks composed of similar neighborhoods.


#### Content-based recommender:

This algorithm is meant to present the user "more of the same what I've liked before", which is exactly what I wanted to do in this project. 

To do so, I started by unputing which Montreal neighbordhoods I would live in, or not. I assigned a number between 2 and 0 depending id I was positive, ambivalent or negative about living in the neighborhood. The info is filed in the user input matrix.

As a second step, I prepared the neighborhood matrix. This consists of gathering the number of venues by category for each of the nine neighborhoods previously chosen.

The weighted category matrix is obtained by multiplying the user input matrix (Hadamard product) to the neighborhood matrix. This matrix shows the interest of the user about the different type of venue categories.

The user profile matrix is obtained by simply summing the columns content then normalizing numbers.

Next step consists of finding the recommendations, which are the best Vancouver neighborhoods based on the my preferences. To do that, I obtained a matrix of Vancouver neighborhoods with the sum of venues by categories. I then multilplied this matrix to the user profile matrix (Hadamard product) and summed each row. The row with the highest value represents the neighborhood that theoritically best suits the user's preferences.


# Results

Given that my favourite Montreal neighborhoods are Le Plateau and Petite-Italie:

the K-Means clustering analysis provided the following recommendations: Chinatown, Downtown Eastside, Gastown, International Village, Victory Square, West End, Marpole and Mount Pleasant.


Given my input on neighborhoods where I would live or:

the Content-based recommender provided the following top ten recommendations: South Granville, Chinatown, Granville Mall, Robson, South Main, Gastown, Yaletown, Victory Square, International Village and Commercial Drive.


As a summary of recommendations, I decided to recommend only the neighborhoods that were part of both analysis: Chinatown, International Village and Gastown. 


# Discussion

Obviously, the two studies above have limitations. 

Based on the methodology, I used a radius of 500 meters to find venues for a given neighborhood. Given that I was looking at central neighborhoods for each city, these ones are closely located which means that some venues are in more than one neighborhoods. The impact of this was that close neighborhoods ended up having really similar venue category distribution. An alternate means to find venues would have been to use the actual perimeters of each neighborhoods.

Regarding the content-based recommender, I found that the venue category distributions amongst the neighborhoods did not allow the my inputs to change a lot and have a big impact on the recommendations. This was remarkable by the fact that most neighborhoods have high numbers of food and shop & service related venues.

Given the limitations above, I found that the best recommendation possible was to recommend neighborhoods that were provided by both analysis.

# Conclusion

A lot of variables can influence the feelings a neighborhood provides to its inhabitants. Moving to a new city without knowing it makes choosing a new neighborhood very difficult. That is why I did my project on identifying Vancouver's neighborhoods that ressemble my favourites neighborhood in my city, Montreal. 

Next time I go to Vancouver, I will defitinely visit Chinatown, International Village and Gastown and try to see if my hypothesis work!
