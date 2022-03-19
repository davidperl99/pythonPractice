from datetime import date
from tkinter.tix import COLUMN
import urllib
import json
import urllib.request
import requests
import folium
import osmnx as ox
import geopandas
import os



base_url = "https://data.gov.il/api/3/action/datastore_search?resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&limit=300&q="
search_date = f"{date.today().year}-{date.today().month:02d}"
data_url = base_url + search_date


response = requests.get(data_url)
response_dict = json.loads(response.content)
assert response_dict['success'] is True
datasets = response_dict['result']
#print(datasets)

israel_location = [31.0461, 34.8516]
m = folium.Map(location=israel_location, zoom_start=7, tiles='cartodbpositron')


ox.config(use_cache=True, log_console=True)
def get_city_polygon(city_name):
    try:
        gdf = ox.geocode_to_gdf(city_name)
        return gdf
    except ValueError:
        return (ox.geocode_to_gdf('washington'))

def get_color(color):
    if (color=="צהוב"): return 'yellow'
    elif (color == 'אדום'): return 'red'
    elif (color=='כתוב'): return 'orange'
    else: return 'green'


city_list = []
grade_list = []
i=0
for City_Name in datasets['records']:
    city_list.insert(i, datasets['records'][i]['City_Name'])
    grade_list.insert(i, datasets['records'][i]['colour'])
    
    gdf = get_city_polygon(city_list[i])
    color = get_color(grade_list[i])
    c = folium.Choropleth(geo_data=gdf, fill_color=f"{color}", line_color=f"{color}", line_weight=2)
    c.add_to(m)

    i = i + 1

cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
m1 = world.explore(
    #column = "pop_est",
    scheme = "naturalbreaks",
    legend = True, 
    k= 10, 
    legend_kwds = dict(colorbar=False),
    name = "countries"
)

cities.explore(
    m = m1, 
    color = 'red', 
    marker_kwds = dict(radius = 10, fill = True), 
    tooltip = 'name', 
    tooltip_kwds = dict(labels=False),
    name = 'cities'
)

folium.TileLayer('Stamen Toner', control=True).add_to(m1)
folium.LayerControl().add_to(m1)

dirname = os.path.dirname(os.path.abspath(__file__))
m1.save(dirname, 'test3.html')

m.save(dirname, 'covid3.html')

print (grade_list)











"""
print(data_url)
# store the response of URL
response = urllib.request.urlopen(data_url)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())
  
# print the json response
print(len(data_json))

print("---------------------------")
"""