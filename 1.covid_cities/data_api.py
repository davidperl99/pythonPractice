from datetime import date
from tkinter.tix import COLUMN
import urllib
import json
import urllib.request
import requests
import folium
import osmnx as ox
import geopandas


base_url = "https://data.gov.il/api/3/action/datastore_search?resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&limit=300&q="
search_date = f"{date.today().year}-{date.today().month:02d}"
data_url = base_url + search_date


response = requests.get(data_url)
response_dict = json.loads(response.content)
assert response_dict['success'] is True
datasets = response_dict['result']

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
    if (color == "צהוב"):
        return 'yellow'
    elif (color == 'אדום'):
        return 'red'
    elif (color == 'כתום'):
        return 'orange'
    else:
        return 'green'


city_list = []
grade_list = []
date_list = []
i = 0
for City_Name in datasets['records']:
    city_list.insert(i, datasets['records'][i]['City_Name'])
    grade_list.insert(i, datasets['records'][i]['colour'])
    date_list.insert(i, datasets['records'][i]['Date'])

    gdf = get_city_polygon(f"{city_list[i]} ישראל")
    color = get_color(grade_list[i])
    c = folium.Choropleth(
        geo_data=gdf, fill_color=f"{color}", line_color=f"{color}", line_weight=2)
    c.add_child(folium.Popup(
        f"<h4> <b> {city_list[i]} </b> </h4> <br/> {grade_list[i]}<br/>{date_list[i]}", max_width=len(f"<h4> {city_list[i]}")*20))
    c.add_to(m)

    i = i + 1


m.save('covid.html')
