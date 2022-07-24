import pandas as pd
import streamlit as st


@st.cache()
def import_data():
    accepted_df = pd.read_csv('Lending_Club_Accepted_2014_2018.csv')
    rejected_df = pd.read_csv('Lending_Club_Rejected_2014_2018.csv')
    return accepted_df


# Explain why titles in histograms are repeated twice
'''
'''

accepted_df = import_data()

# plot 1: volume of loan applications by zip

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