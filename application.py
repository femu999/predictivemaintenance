import streamlit as st
import folium
from streamlit_folium import folium_static, st_folium

# Define the coordinates for the substations and lines
substations = {
    "Umspannwerk 1": (51.4556, 7.0116),
    "Umspannwerk 2": (51.4500, 7.0200),
    "Verteilerstation 1": (51.4600, 7.0000),
    "Verteilerstation 2": (51.4650, 7.0150),
    "Verteilerstation 3": (51.4700, 7.0250)
}

lines = {
    "Leitung A": [
        (51.4556, 7.0116),  # Umspannwerk 1
        (51.4570, 7.0080),  # Kreuzung Gladbecker Straße / Grillostraße
        (51.4600, 7.0000)   # Verteilerstation 1
    ],
    "Leitung B": [
        (51.4500, 7.0200),  # Umspannwerk 2
        (51.4525, 7.0150),  # Kreuzung Altenessener Straße / Gladbecker Straße
        (51.4650, 7.0150)   # Verteilerstation 2
    ],
    "Leitung C": [
        (51.4650, 7.0150),  # Verteilerstation 2
        (51.4675, 7.0200),  # Kreuzung Gladbecker Straße / Bismarckstraße
        (51.4700, 7.0250)   # Verteilerstation 3
    ],
    "Leitung D": [
        (51.4556, 7.0116),  # Umspannwerk 1
        (51.4600, 7.0000)   # Verteilerstation 1
    ],
    "Leitung E": [
        (51.4500, 7.0200),  # Umspannwerk 2
        (51.4650, 7.0150)   # Verteilerstation 2
    ],
    "Leitung F": [
        (51.4600, 7.0000),   # Verteilerstation 1
        (51.4650, 7.0150)   # Verteilerstation 2
    ],
    "Leitung G": [
        (51.4650, 7.0150),   # Verteilerstation 2
        (51.4700, 7.0250)   # Verteilerstation 3
    ]
}

# Define colors for the lines
line_colors = {
    "Leitung A": 'green',
    "Leitung B": 'yellow',
    "Leitung C": 'red',
    "Leitung D": 'green',
    "Leitung E": 'yellow',
    "Leitung F": 'red',
    "Leitung G": 'green'
}

# Create a Streamlit app
st.title("Visualisierung des Stromnetzes in Essen")

# Create a map centered around Essen
map_center = [51.4556, 7.0116]
m = folium.Map(location=map_center, zoom_start=13, tiles='cartodbpositron')

# Add substations to the map
for name, coords in substations.items():
    folium.Marker(location=coords, popup=name, icon=folium.Icon(color='blue')).add_to(m)

# Add lines to the map with different colors
for name, coords in lines.items():
    folium.PolyLine(locations=coords, color=line_colors[name], weight=2.5, opacity=1).add_to(m)

# Display the map in Streamlit
st_folium(m)