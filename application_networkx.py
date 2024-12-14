import streamlit as st
import pandas as pd
import networkx as nx
import folium
from streamlit_folium import folium_static

# Daten für Knoten und Kanten
nodes = {
    "Umspannwerk 1": (51.4500, 7.0167),
    "Umspannwerk 2": (51.4700, 7.0000),
    "Verteilerstation 1": (51.4600, 7.0100),
    "Verteilerstation 2": (51.4550, 7.0200),
    "Endverbraucher 1": (51.4520, 7.0150),
    "Endverbraucher 2": (51.4650, 7.0050)
}

edges = [
    ("Umspannwerk 1", "Verteilerstation 1"),
    ("Umspannwerk 1", "Verteilerstation 2"),
    ("Umspannwerk 2", "Verteilerstation 1"),
    ("Verteilerstation 1", "Endverbraucher 1"),
    ("Verteilerstation 2", "Endverbraucher 2")
]

# Erstellen eines Graphen
G = nx.Graph()

for node, (lat, lon) in nodes.items():
    G.add_node(node, pos=(lon, lat))

G.add_edges_from(edges)

# Streamlit App
st.title("Visualisierung eines Dummy-Stromnetzes in Essen")

# Erstellen einer Folium-Karte
m = folium.Map(location=[51.45, 7.01], zoom_start=13)

# Hinzufügen von Knoten zur Karte
for node, (lat, lon) in nodes.items():
    folium.Marker([lat, lon], popup=node).add_to(m)

# Hinzufügen von Kanten zur Karte
for edge in edges:
    start = nodes[edge[0]]
    end = nodes[edge[1]]
    folium.PolyLine([start, end], color="blue").add_to(m)

# Anzeige der Karte in Streamlit
folium_static(m)

# Anzeige der Knoten und Kanten
st.subheader("Knoten (Umspannwerke, Verteilerstationen, Endverbraucher)")
st.write(pd.DataFrame(nodes.items(), columns=["Knoten", "Koordinaten"]))

st.subheader("Kanten (Leitungen)")
st.write(pd.DataFrame(edges, columns=["Von", "Nach"]))