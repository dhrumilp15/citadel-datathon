import streamlit as st
import os

st.title("An analysis of the Effects of Financial Climate on Lending Club Loans")

st.markdown('''
- Geographical Analysis: An analysis of loans by zip code
- Sentiment Analysis: Capturing market sentiment using several models for sentiment analysis
- Employment Analysis: Analyzing correlations between employment and loan applications
''')
# insert the gh readme here

from get_data import download_file

file_ids = [
    '1--mpdq14luzIlPG8W5W3ESxV9P1xw8W-',
    '1Az_BSkNInzeNRs7sUsHCaP_sN-yc8cxC',
    '1wRe4v5p9B6UbYJkclHcvlkh5g4AR24lk',
    '13gBGdMSDBGx6BefbW_DcWwokhK_7UZVY',
    '1kkb3hi7YyYJLfvj0Aw-Xqj1ZaNAl8_Zr',
]

file_urls = [
    'analyst_ratings_monthly_avg_sentiment.csv',
    'partner_headlines_monthly_avg_sentiment.csv',
    'df_cleaned_new.tsv',
    'Lending_Club_Accepted_2014_2018.csv',
    'Lending_Club_Rejected_2014_2018.csv',
]

with st.spinner("Downloading data"):
    for id, url in zip(file_ids, file_urls):
        fp = os.path.join('data', url)
        if not os.path.exists(fp):
            file = download_file(id).decode()
            with open(fp, 'w') as f:
                f.write(file)
