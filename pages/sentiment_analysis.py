import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import google
from googleapiclient.discovery import build
import requests

@st.cache
def make_means(*dfs):
    means = []
    for df in dfs:
        average_sentiment = df.groupby('month_year').mean()
        average_sentiment['averaged_sentiment'] = (average_sentiment.huggingface_sentiment + average_sentiment.spacy_sentiment) / 2
        means.append(average_sentiment)
    return means

@st.cache
def load_data():
    analyst_ratings = pd.read_csv('data/analyst_ratings_monthly_avg_sentiment.csv')
    partner_headlines = pd.read_csv('data/partner_headlines_monthly_avg_sentiment.csv')
    analyst_means, headline_means = make_means(analyst_ratings, partner_headlines)
    return analyst_means, headline_means

def show_data(df):
    months = df.index
    fig, ax = plt.subplots(figsize=(50, 30), dpi=300)
    ax.plot(months, df.huggingface_sentiment)
    ax.plot(months, df.spacy_sentiment)
    ax.plot(months, df.averaged_sentiment)
    plt.legend(['distilRoBERTa Sentiment', 'SpaCy Sentiment', 'Averaged Sentiment'], prop={'size': 40})
    plt.title('Average Monthly Sentiment', fontsize=50)
    plt.xlabel('Time', fontsize=50)
    plt.ylabel('Sentiment', fontsize=50)
    plt.xticks(rotation=90)
    st.pyplot(fig)

analyst_means, headline_means = load_data()

st.title("Sentiment Analysis")
st.subheader("Average Monthly Sentiment of Analyst Ratings")
show_data(analyst_means)

st.markdown("It's worth pointing out that the distilRoBERTa-predicted sentiment has significantly more variance than the "
            "SpaCy-predicted sentiment")

st.subheader("Average Monthly Sentiment of News Headlines")
show_data(headline_means)
