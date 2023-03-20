from flask import Flask, render_template, send_from_directory
import folium
from folium.plugins import MarkerCluster
import pandas
import os


app = Flask(__name__)

# data = pandas.read_csv(
#     'Airbnb_Texas_Rentals.csv',
#     header=None,
#     names=[
#         'average_rate_per_night',
#         'bedrooms_count',
#         'city',
#         'date_of_listing',
#         'description',
#         'latitude',
#         'longitude',
#         'title',
#         'url'
#     ],
#     usecols=[
#         'average_rate_per_night',
#         'description',
#         'latitude',
#         'longitude',
#         'url'
#     ]
# )

data = pandas.read_csv(
    'Airbnb_Texas_Rentals.csv',
    # header=None,
    # usecols=[0, 4, 5, 6, 8],
    nrows=5000

)

'''
Columns
'average_rate_per_night', 'bedrooms_count', 'city',
       'date_of_listing', 'description', 'latitude', 'longitude', 'title',
       'url'
'''

lat = list(data['latitude'])
long = list(data['longitude'])
url = list(data['url'])
average_rate_per_night = list(data['average_rate_per_night'])
description = list(data['description'])

map = folium.Map(
    location=[30.4418495, -97.7894251],
    zoom_start=10,
    tiles="Stamen Terrain"
)

html = """
<article style="padding-bottom:1rem;">
%s
<strong style="display: block;padding-top: 8px;">%s per night</strong>
</article>
<a href="%s" target="_blank">View this AirBnb</a>
"""

marker_cluster = MarkerCluster().add_to(map)

for lt, ln, url, average_rate_per_night, description in zip(lat, long, url, average_rate_per_night, description):
    clean_desc = str(description).replace("\\n", "<br/>")
    iframe = folium.IFrame(html=html % (
        clean_desc, average_rate_per_night, url), width=300, height=250)
    folium.Marker(
        [lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color="orange")).add_to(marker_cluster)

map.save('templates/index.html')


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
