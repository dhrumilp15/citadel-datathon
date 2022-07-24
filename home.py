import streamlit as st
import os

st.title("An analysis of the Effects of Financial Climate on Lending Club Loans")

st.markdown('''
- Geographical Analysis: An analysis of loans by zip code
- Sentiment Analysis: Capturing market sentiment using several models for sentiment analysis
- Histograms: Analyzing correlations between employment and loan applications

Made with 💖 by Raveesh Mehta, Dhrumil Patel, Bradley Moon, Nathan Chi''')
# insert the gh readme here

from get_data import download_file

file_ids = ['1--mpdq14luzIlPG8W5W3ESxV9P1xw8W-', '1Az_BSkNInzeNRs7sUsHCaP_sN-yc8cxC', '1wRe4v5p9B6UbYJkclHcvlkh5g4AR24lk']
file_urls = ['analyst_ratings_monthly_avg_sentiment.csv', 'partner_headlines_monthly_avg_sentiment.csv', 'df_cleaned_new.tsv']

for id, url in zip(file_ids, file_urls):
    if not os.path.exists(url):
        file = download_file(id).decode()
        with open(os.path.join('data', url), 'w') as f:
            f.write(file)
