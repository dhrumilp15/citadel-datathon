import pandas as pd
import streamlit as st
from urllib.request import urlopen
import plotly.express as px
import json


@st.cache()
def import_data():
    accepted_df = pd.read_csv('data/Lending_Club_Accepted_2014_2018.csv')
    # fix the zipcode column (ZIPXX -> ZIP)
    accepted_df['zip_code'] = accepted_df['zip_code'].str[:3]

    # import the geoJSON file that includes the map of zip3 regions
    with urlopen('https://raw.githubusercontent.com/mathbiol/sparcs/master/zip3.geojson') as response:
        zip3_regions = json.load(response)
    return accepted_df, zip3_regions


st.title("Geographical Analysis")
st.header("Volume of Loan Applications by Zip Code")

accepted_df, zip3_regions = import_data()

# volume of loan applications by zip
# take the zip codes only and count the no. of times they occur
volume = accepted_df['zip_code'].value_counts()

# plot the data
fig = px.choropleth(
    data_frame=volume,
    geojson=zip3_regions,
    locations=volume.index,
    featureidkey='properties.ZIP',
    color=volume.values,
    color_continuous_scale='Viridis',
    range_color=(0, 20000),
    scope='usa',
    labels={'count': 'loan acceptances'}
)

fig.update_layout(margin={"r": 0,"t": 0,"l": 0,"b": 0})
st.plotly_chart(fig)

# find average interest rate by zip

st.header("Average Interest Rate by Zip Code")

zip_int = accepted_df[['zip_code', 'int_rate']]

zip_int = zip_int.groupby(['zip_code'])['int_rate'].mean().reset_index()

# plot the data
fig = px.choropleth(
    data_frame=zip_int,
    geojson=zip3_regions,
    locations=zip_int.zip_code,
    featureidkey='properties.ZIP',
    color=zip_int.int_rate,
    color_continuous_scale='Viridis',
    range_color=(6, 21),
    scope='usa',
    labels={'count':'loan acceptances'}
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# Loan amount and occupation type => Sankey
