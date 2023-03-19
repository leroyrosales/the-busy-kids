from flask import Flask, render_template
import folium
import pandas

app = Flask(__name__)

data = pandas.read_csv('Airbnb_Texas_Rentals.csv')

'''
Columns
'Unnamed: 0', 'average_rate_per_night', 'bedrooms_count', 'city',
       'date_of_listing', 'description', 'latitude', 'longitude', 'title',
       'url'
'''

lat = list(data['latitude'])
long = list(data['longitude'])
url = list(data['url'])
description = list(data['description'])

map = folium.Map(
    location=[30.4418495, -97.7894251],
    zoom_start=10,
    tiles="Stamen Terrain"
)

html = """
%s <br/>
<a href="%s" target="_blank">View this AirBnb</a><br>
"""

fg = folium.FeatureGroup(name="Texas Map")

for lt, ln, url, description in zip(lat, long, url, description):
    iframe = folium.IFrame(html=html % (
        description, url), width=200, height=100)
    fg.add_child(folium.Marker(
        [lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color="green")))

map.add_child(fg)

map.save('templates/index.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
