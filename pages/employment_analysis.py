import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import json
import matplotlib.pyplot as plt


@st.cache()
def import_data():
    data = pd.read_csv('data/df_cleaned_new.tsv', sep='\t', header=0)
    df_cleaned = pd.read_csv('data/df_cleaned_with_fico.tsv', sep='\t')
    df_cleaned['grade_num'] = [ord(x) - 64 for x in df_cleaned.grade]
    df_cleaned.sort_values(by='grade')
    with open('pages/to_name.json', 'r') as f:
        to_name_str = json.load(f)
    to_name = {}
    for key, val in to_name_str.items():
        to_name[int(key)] = val
    df_cleaned['minor_categories_names'] = [to_name[x] for x in df_cleaned['minor_categories']]
    df_plot = df_cleaned[['loan_amnt', 'minor_categories', 'minor_categories_names']]
    return data, df_plot

data, df_plot = import_data()

# select the necessary columns
job_amount = data[['major_categories', 'loan_amnt']]

# drop major_categories = 0, where the model was not able to identify the category
job_amount.drop(job_amount[job_amount['major_categories'] == 0].index, inplace=True)

# subtract 1 from every value in major_categories to match the sankey representation
job_amount['major_categories'] = job_amount['major_categories'] - 1

# document the labels with their index (for clarity only)
labels_index = {
    'Managers': 0,
    'Professionals': 1,
    'Technicial and Associate Professionals': 2,
    'Clerical Support Workers': 3,
    'Service/Sale Workers and Customer Service': 4,
    'Craft and Related Trade Workers': 5,
    'Plant/Machine Operators and Assemblers': 6,
    'Elementary Occupations': 7,
    'Armed Forces and Corrections/Police/Security Occupations': 8,
    'Loan Amount Above Median': 9,
    'Loan Amount Below Median': 10
}

labels = list(labels_index.keys())

# create the lists to be used in the sankey diagram

# source: add two values of each labor category, one will connect to loan_amount > median and the other for loan_amount <= median
source = [x for x in range(9)] * 2
source.sort()

# let 9 represent loan_amount > median, 10 represent loan_amount <= median
# since there are two flows from each labor category, and their indexes are assigned sequentially
target = [9, 10] * 9

# for each labor category, find the number of columns with for > and <= and append them to create the width of each flow
value = []
MEDIAN = 13500

for category in range(9):
    # select all records with this labor category
    loans_in_category = job_amount[job_amount['major_categories'] == category]

    # from all the loans of this category, find the number of loans above the median
    loans_above_median = loans_in_category[loans_in_category['loan_amnt'] > MEDIAN]

    # calculate and append the values
    total = len(loans_in_category)
    above = len(loans_above_median)
    below = total - above

    value.append(above)
    value.append(below)

figure = go.Figure(data=[go.Sankey(
    node=dict(
      pad=15,
      thickness=20,
      line=dict(color="black", width = 0.5),
      label=labels,
      #color = "blue"
    ),
    link=dict(
      source=source,
      target=target,
      value=value
  ))])

# figure.update_layout(title_text="", font_size=10)
st.title("Employment Analysis")
st.subheader("Loan Amount Distribution by Labor Type")
with st.spinner("loading plot..."):
    st.plotly_chart(figure)

st.subheader("Loan Amount by Profession")
with st.spinner("loading plot..."):
    fig, ax = plt.subplots(figsize=(50, 60))
    first_50 = df_plot[df_plot['minor_categories'] <= 50]
    ax = first_50.hist(column="loan_amnt", by="minor_categories_names",  bins=40, ax=ax)
    st.pyplot(fig)
