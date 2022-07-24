import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

@st.cache
def load_data():
    analyst_ratings = pd.read_csv('data/analyst_ratings_monthly_avg_sentiment.csv')
    partner_headlines = pd.read_csv('data/partner_headlines_monthly_avg_sentiment.csv')
    plt.rc('axes', labelsize=12)
    return analyst_ratings, partner_headlines


def show_data(df):
    months = df.month_year.sort_values().unique()
    fig, ax = plt.subplots(figsize=(50, 30), dpi=300)
    average_sentiment = df.groupby('month_year').mean()
    average_sentiment['averaged_sentiment'] = (average_sentiment.huggingface_sentiment + average_sentiment.spacy_sentiment) / 2
    ax.plot(months, average_sentiment.huggingface_sentiment)
    ax.plot(months, average_sentiment.spacy_sentiment)
    ax.plot(months, average_sentiment.averaged_sentiment)
    plt.legend(['distilRoBERTa Sentiment', 'SpaCy Sentiment', 'Averaged Sentiment'], prop={'size': 40})
    plt.title('Average Monthly Sentiment', fontsize=50)
    plt.xlabel('Time', fontsize=50)
    plt.ylabel('Sentiment', fontsize=50)
    plt.xticks(rotation=90)
    st.pyplot(fig)
    return average_sentiment


analyst_ratings, partner_headlines = load_data()

st.title("Sentiment Analysis")
st.subheader("Average Monthly Sentiment of Analyst Ratings")
show_data(analyst_ratings)

st.markdown("It's worth pointing out that the distilRoBERTa-predicted sentiment has significantly more variance than the "
            "SpaCy-predicted sentiment")

st.subheader("Average Monthly Sentiment of News Headlines")
show_data(partner_headlines)
