# Safegraph-OSMnx-HERE
Code for paper on incorporating state of the art geospatial data sets on complex networks to predict disruptions stemming from cyberattacks on road network infrastructures


Usage:

1.	pre-processing.ipynb: Pre-processing of safegraph and osmnx data. Incorporates functions from trips.py for generating disruptions from 3 classes of cyber-attacks (random, route, targeted)
2.	trips.py: Given a graph G, ODs from safegraph, routes - compute shortest time trips and accessory methods 
3.	osm-here.ipynb: get shortest-time paths corresponding to SafeGraph ODs on OSMnx network, and traffic speeds from HERE API. Also uses trips.py for functions
4.	Using trips, output requested files for visualizations/visualizations themselves (.py)


Data Available on request (HERE traffic speeds, SafeGraph ODs, SafeGraph census data)
