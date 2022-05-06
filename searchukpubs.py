"""
Name: Anson Wu
CS230: Section 5
Data: 8000 pubs in the UK
URL: http://192.168.1.208:8501

Description: This program is designed for users to search for pubs in the UK, whether is through their local
authority, fas_ids or if the pubs are in a hotel/inn.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd



st.title("FIND YOUR GOIN' PUBS IN THE UK!!!")
st.header("Author: Anson Wu")
st.success("Explore the pubs and hope you spend a memorable trip in the United Kingdom! ")
st.image("pub.png",width = 700)

df_pubs = pd.read_csv("pubs.csv")
df_pubs.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace= True)

df_pubs = df_pubs.dropna(subset=["lat", "lon"])
df_pubs["lat"] = pd.to_numeric(df_pubs["lat"])
df_pubs["lon"] = pd.to_numeric(df_pubs["lon"])


# Query 1 the local authorities of the cities

city_list = []
for l in df_pubs.local_authority:
    if l.lower().strip() not in city_list:
        city_list.append(l.lower().strip())

sub_list = []

for l in city_list:
    sub = df_pubs[df_pubs["local_authority"].str.lower().str.strip() == l]
    sub_list.append(sub)


layer_list = []

for i in sub_list:
    layer = pdk.Layer(type = 'ScatterplotLayer',
                  data=i,
                  get_position='[lon, lat]',
                  get_radius=150,
                  get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                  pickable=True
                  )
    layer_list.append(layer)

tool_tip = {"html": "Pub's Info:<br/> <b>{name}</b> <br/> <b>{local_authority}</b>",
            "style": { "backgroundColor": "black",
                        "color": "white"}
          }

view_list = []

for vv in range(len(sub_list)):
    view_state = pdk.ViewState(
                latitude=sub_list[vv]["lat"].mean(),
                longitude=sub_list[vv]["lon"].mean(),
                zoom=10,
                pitch=0)
    view_list.append(view_state)

view_state_wholeUK = pdk.ViewState(
                latitude=df_pubs["lat"].mean(),
                longitude=df_pubs["lon"].mean(),
                zoom=6,
                pitch=0)

city_list.insert(0,"")

selected_city = st.selectbox("Plz select a Local Authority", city_list)


for i in range(len(city_list)):
    if selected_city == city_list[i]:
        if i == 0:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state_wholeUK,
                layers=layer_list,
                tooltip= tool_tip
                )
        else:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_list[i-1],
                layers=[layer_list[i-1]],
                tooltip= tool_tip
                )

        st.pydeck_chart(map)


# Query 2: Pubs in the hotel
st.write("")
st.write("")
Header = '<p style="font-family:Tangerine; color:Blue; font-size: 30px;">These are the pubs that are in the hotels or inns , you can also find them in the map with their local authority! </p>'
st.markdown(Header, unsafe_allow_html=True)

# This is to define if hotel/inn are contained in the pubs name
name_hotel = df_pubs.loc[df_pubs['name'].str.contains( "Hotel|Inn", case=False)]

# This is to show the info of all the pubs that are in a hotel or inn using dataframe slicing
# Then I use the sort_values function to sort the local_authority and name with ascending orders, so the users are easier to find the pubs
name_hotel_table = (name_hotel.loc[:,["name","address","local_authority"]])
sort_data = name_hotel_table.sort_values(['local_authority','name'], ascending = [True, True])
st.write(sort_data)


city_list2 = []
for l in name_hotel.local_authority:
    if l.lower().strip() not in city_list2:
        city_list2.append(l.lower().strip())


sub_list2 = []

for l in city_list2:
    sub2 = name_hotel[name_hotel["local_authority"].str.lower().str.strip() == l]
    sub_list2.append(sub2)


layer_list2 = []

for i in sub_list2:
    layer = pdk.Layer(type = 'ScatterplotLayer',
                  data=i,
                  get_position='[lon, lat]',
                  get_radius=300,
                  get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                  pickable=True
                  )
    layer_list2.append(layer)

tool_tip = {"html": "Pub's Info:<br/> <b>{name}</b> <br/> <b>{local_authority}</b>",
            "style": { "backgroundColor": "black",
                        "color": "white"}
          }
# For each selected local authority, I create a view state base on their mean lat and lon.
view_list2 = []

for vv in range(len(sub_list2)):
    view_state2 = pdk.ViewState(
                latitude=sub_list2[vv]["lat"].mean(),
                longitude=sub_list2[vv]["lon"].mean(),
                zoom=10,
                pitch=0)
    view_list2.append(view_state2)

# For the viewstate where nothing is selected, the view state is base on the mean lat and lon of all the pubs-in-hotel datas
view_state_hotel = pdk.ViewState(
                latitude=name_hotel["lat"].mean(),
                longitude=name_hotel["lon"].mean(),
                zoom=6,
                pitch=0)

city_list2.insert(0,"")

selected_city2 = st.selectbox("Plz select a Local Authority", city_list2)


for i in range(len(city_list2)):
    if selected_city2 == city_list2[i]:
        if i == 0:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state_hotel,
                layers=layer_list2,
                tooltip= tool_tip
                )
        else:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_list2[i-1],
                layers=[layer_list2[i-1]],
                tooltip= tool_tip
                )

        st.pydeck_chart(map)


# Query 3: Search pubs with fas_id
st.success("You can also search the pub with their fas id!")
search_fas_id = st.number_input("Please type the fas id of the pub you are looking for: ",0.00,1000000.00)

result = df_pubs.loc[df_pubs["fas_id"]==int(search_fas_id),["name","address","local_authority"]]
name = (str(result.name.values))

if name =="[]":
    st.write("Information not found")
else:
    st.write(result)
    st.write(f"The pub you are searching for is {name}.")


# Query 4 : Search pubs with name
st.write("")
st.success("You can also search the address with the pub's name!")
search_name = st.text_input("Plz type the name of the pub you are looking for:")
result_name = df_pubs.loc[df_pubs["name"]==search_name,["name","address","local_authority"]]
address = (str(result_name.address.values).lower().strip())


if address =="[]":
    st.write("")
else:
    st.write(result_name)
    st.write(f"The address of the pub you are searching for is {address}.")

