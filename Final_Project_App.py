
# Module Import
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# Setting-up the app UI in the wide setting
st.set_page_config(layout='wide')

# Introduction Section
st.write(
'''
# GUN VIOLENCE DATA
Following app will allow users to see casualties from gun violence in United States from 2013 - 2018.

If a user is traveling and going through a location, or looking to move-in for a new journey in life, the app can be used to educate onself about crimes caused by gun violence. 

#### Data
The original data is from: [GUN VIOLENCE ARCHIVE](https://www.gunviolencearchive.org/)

For this particular application, data were downloaded from Kaggle: [Gun Violence Data](https://www.kaggle.com/datasets/jameslko/gun-violence-data)

#### Application
The app gives each user following parameters to choose:

- State of interest
- City/County of interest
- Year of interest
'''
)

col_names = ["none", "year", "month", "state", "city_or_county", "n_killed", "n_injured", "latitude", "longitude"]
df = pd.read_csv('https://github.com/jlee7x/DE_App_Project/blob/main/Final_Project_Data.csv',names=col_names, sep="delimiter" ,header=None)
df = df.drop(columns=['none','month'])
st.dataframe(df)

# Parameter Selection Section
st.write("## Parameter Selector")

# Setting-up For Parameter Selection Layout
col1, col2, col3 = st.columns(3)
with col1:
	state_selection = st.selectbox("Select State",
				(sorted(df.state.unique())))
with col2:
	df_reduced = df[df['state']==state_selection]
	city_county_selection = st.selectbox("Select City/County",
				(sorted(df_reduced.city_or_county.unique())))
with col3:
	year_input = st.slider('Year', min_value=2013,max_value=2018,step=1)

# Visualization Section
st.write('''
## Death/Injury Information
''')

# Setting-up For 'State Death/Injury By Year' Graph
df_year_state = (df
		.groupby(['year','state'], as_index=False)
		[['n_killed','n_injured']].sum())
graph_1= df_year_state[df_year_state['state']==state_selection]

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20,4.5))

years_1 = graph_1['year']
death_1 = graph_1['n_killed']
injury_1 = graph_1['n_injured']

x_1 = np.arange(len(years_1))
width =  0.3

rects1 = ax1.bar(x_1 - width/2, death_1, width, label='Killed',color="red")
rects2 = ax1.bar(x_1 + width/2, injury_1, width, label='Injured',color='green')

ax1.set_ylabel('NO. OF CASUALTIES',fontsize =12)
ax1.set_xlabel('YEAR',fontsize =12)
ax1.set_title(f'STATE DEATH/INJURY BY YEAR: {state_selection.upper()}',fontsize=15)
ax1.set_xticks(x_1, years_1,fontsize=10)
ax1.legend(fontsize = 10)

ax1.bar_label(rects1, fmt="%d", fontsize=8, rotation=0, padding=2)
ax1.bar_label(rects2, fmt="%d", fontsize=8, rotation=0, padding=2)

# Setting-up For 'City/County Death/Injury By Year' Graph
df_year_state_city = (df
		.groupby(['year','state','city_or_county'], as_index=False)
		[['n_killed','n_injured']].sum())

graph_2 = df_year_state_city[(df_year_state_city['state']== state_selection) &
				(df_year_state_city['city_or_county']== city_county_selection)]

years_2 = graph_2['year']
death_2 = graph_2['n_killed']
injury_2 = graph_2['n_injured']

x_2 = np.arange(len(years_2))
width =  0.30

rects3 = ax2.bar(x_2 - width/2, death_2, width, label='Killed',color="orange")
rects4 = ax2.bar(x_2 + width/2, injury_2, width, label='Injured',color='blue')

ax2.set_ylabel('NO. OF CASUALTIES',fontsize =12)
ax2.set_xlabel('YEAR',fontsize =12)
ax2.set_title(f'CITY/COUNTY DEATH/INJURY BY YEAR: {city_county_selection.upper()}',fontsize=15)
ax2.set_xticks(x_2, years_2,fontsize=10)
ax2.legend(fontsize = 10)

ax2.bar_label(rects3, fmt="%d", fontsize=8, rotation=0, padding=2)
ax2.bar_label(rects4, fmt="%d", fontsize=8, rotation=0, padding=2)

fig.tight_layout()

st.write(
'''
##### *Death/Injury Graphs*:
'''
)
st.pyplot(fig)

# Seting-up for Mapbox Layout
row2_1, row2_2 = st.columns((2, 2))

# Setting-up For Mapbox of Death Location
df_killed = df[(df['year']==year_input) &
		(df['state']==state_selection) &
		(df['city_or_county']==city_county_selection) &
		(df['n_killed'] >0)]
dff_killed = df_killed[['n_killed','latitude','longitude']]
dff_killed = dff_killed.rename(columns={'latitude':'lat', 'longitude':'lon'})

fig2 = px.scatter_mapbox(
    data_frame=dff_killed,
    lat='lat',
    lon='lon',
    color='n_killed',
    size='n_killed',
    zoom = 10,
    color_continuous_scale=px.colors.sequential.Agsunset,
    mapbox_style="carto-positron",
)

with row2_1:
	st.write(
        '''
        ##### *Death Locations:*
	'''
	)
	st.plotly_chart(fig2)

# Setting-up For Mapbox of Injury Location
df_injury = df[(df['year']==year_input) &
		(df['state']==state_selection) &
		(df['city_or_county']==city_county_selection) &
		(df['n_injured'] >0)]
dff_injury = df_injury[['n_injured','latitude','longitude']]
dff_injury = dff_injury.rename(columns={'latitude':'lat', 'longitude':'lon'})

fig3 = px.scatter_mapbox(
    data_frame=dff_injury,
    lat='lat',
    lon='lon',
    color='n_injured',
    size='n_injured',
    zoom = 10,
    color_continuous_scale=px.colors.sequential.Agsunset,
    mapbox_style="carto-positron",
)

with row2_2:
	st.write(
	'''
	##### *Injury Locations:*
	'''
	)
	st.plotly_chart(fig3)

