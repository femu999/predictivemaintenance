import random

import streamlit as st
import folium
from streamlit_folium import folium_static, st_folium
import pandas as pd

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

construction_years = {}
for name, coords in substations.items():
    construction_years[name] = 1985 + (((coords[0]) * 777) % 35)

for name, coords in lines.items():
    construction_years[name] = 1985 + (((coords[0][0]) * 777) % 35)

asset_list = list(substations.keys()) #+ list(lines.keys())

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

st.header("Zustandprognose der Betriebsmittel - was möchtest du wissen?")
worst_equipments = st.button("Zeige kritische Betriebsmittelzustände")
map_equipments = st.button("Zeige Geografische Betriebsmittelübersicht")

# Sidebar für Benutzereingaben
st.sidebar.header('Benutzereingaben')

def user_input_features():
    st.header("Kritische Auslastung > 95%")
    equipment_id = st.selectbox('Geräte-ID', asset_list)
    temperature = st.slider('Temperatur (°C)', -20, 100, 25)
    humidity = st.slider('Luftfeuchtigkeit (%)', 0, 100, 50)
    vibration = st.slider('Vibration (mm/s)', 0.0, 10.0, 1.0)
    load = st.slider('Last (%)', 0, 100, 98)
    data = {'equipment_id': equipment_id,
            'temperature': temperature,
            'humidity': humidity,
            'vibration': vibration,
            'load': load}
    features = pd.DataFrame(data, index=[0])
    return features


def get_color_by_construction_year(year):
    """
    Return a color based on the construction year of the equipment.

    Parameters:
    year (int): The construction year of the equipment.

    Returns:
    str: A color ('red', 'yellow', 'green') based on the construction year.
    """
    if year < 1989:
        return 'red'
    elif 1989 <= year <= 1999:
        return 'orange'
    else:
        return 'green'

#df = user_input_features()

def user_input_simulation():
    year = st.sidebar.slider('Prognose Zustand im Jahr', 2024, 2040, 2024)
    data = {'year': year}
    features = pd.DataFrame(data, index=[0])
    return year

year = user_input_simulation()

# Check if the variable is already in session_state
if 'show_map' not in st.session_state:
    st.session_state.show_map = False  # Set the initial value

if 'show_crit' not in st.session_state:
    st.session_state.show_crit = False  # Set the initial value

if worst_equipments:
    st.session_state.show_map = False
    st.session_state.show_crit = True

if map_equipments:
    st.session_state.show_map = True
    st.session_state.show_crit = False

# Create a map centered around Essen
map_center = [51.4556, 7.0116]
m = folium.Map(location=map_center, zoom_start=13, tiles='cartodbpositron')


# Add substations to the map
for name, coords in substations.items():

    html = f"""
        <table style="width:100%">
          <tr>
            <th>Name</th>
            <th>{name}</th>
          </tr>
          <tr>
            <td>Koordinaten</td>
            <td>{coords}</td>
          </tr>
          <tr>
            <td>Hersteller</td>
            <td>NKT</td>
          </tr>
          <tr>
            <td>Baujahr</td>
            <td>{int(construction_years[name])}</td>
          </tr>
          <tr>
            <td>Status</td>
            <td>{get_color_by_construction_year(construction_years[name] - (year - 2024))}</td>
          </tr>
        </table>
        """
    iframe = folium.IFrame(html, width=300, height=200)
    popup = folium.Popup(iframe, max_width=2650)
    folium.CircleMarker(location=coords, popup=popup, tooltip=name, color=get_color_by_construction_year(construction_years[name] - (year - 2024)),fill=True).add_to(m)

# Add lines to the map with different colors
for name, coords in lines.items():
    html = f"""
            <table style="width:100%">
              <tr>
                <th>Name</th>
                <th>{name}</th>
              </tr>
              <tr>
                <td>Koordinaten</td>
                <td>{coords}</td>
              </tr>
              <tr>
                <td>Hersteller</td>
                <td>NKT</td>
              </tr>
              <tr>
                <td>Baujahr</td>
                <td>{int(construction_years[name])}</td>
              </tr>
              <tr>
                <td>Status</td>
                <td>{get_color_by_construction_year(construction_years[name] - (year - 2024))}</td>
              </tr>
            </table>
            """
    iframe = folium.IFrame(html, width=300, height=200)
    popup = folium.Popup(iframe, max_width=2650)
    folium.PolyLine(locations=coords, popup=popup, tooltip=name, color=get_color_by_construction_year(construction_years[name] - (year - 2024)), weight=5, opacity=1).add_to(m)

if st.session_state.show_crit:
    df = user_input_features()

if st.session_state.show_map:
    st_folium(m)


    # Display the map in Streamlit


    st.text("rot - älter 35 Jahre")
    st.text("gelb - älter 25 Jahre")
    st.text("grün - jünger 25 Jahre")