import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

def total_amt_transaction_type():

    df = run_query("SELECT total_amount, year, transactions_type, transaction_group, direction, month FROM `sylvan-apogee-402010.neobank_Gold_Tier.amt_trx_mart` order by year, month")
    data = pd.DataFrame(df, columns=['total_amount', 'transaction_group', 'year', 'month', 'direction', 'transactions_type'])
    year_filter = st.multiselect('Select Year', options=list(data['year'].unique()), default=list(data['year'].unique()))
    month_filter = st.multiselect('Select Month', options=list(data['month'].unique()), default=list(data['month'].unique()))
    #direction_filter = st.multiselect('Select direction', options=list(data['direction'].unique()), default=list(data['direction'].unique()))
    transaction_filter = st.multiselect('Select type of transaction', options=list(data['transactions_type'].unique()), default=list(data['transactions_type'].unique()))
    filtered_data = data[ data['year'].isin(year_filter) & data['month'].isin(month_filter) & data['transactions_type'].isin(transaction_filter) ]
    st.write(filtered_data)

    fig = px.bar(filtered_data, x='transactions_type', y='total_amount', color='transaction_group')
    fig['layout']['yaxis'].update(autorange = True)
    st.plotly_chart(fig)

def moving_average_transactions():
    df2 = run_query("SELECT year, month, direction, moving_avg FROM `sylvan-apogee-402010.neobank_Gold_Tier.moving_avg_trx_mart` order by  year, month")
    data2 = pd.DataFrame(df2, columns=['year', 'month', 'direction', 'moving_avg'])
    year_filter2 = st.multiselect('Select Year', options=list(data2['year'].unique()), default=list(data2['year'].unique()), key='year_filter2')
    #month_filter2 = st.multiselect('Select Month', options=list(data2['month'].unique()), default=list(data2['month'].unique()), key='month_filter2')
    #direction_filter = st.multiselect('Select direction', options=list(data2['direction'].unique()), default=list(data2['direction'].unique()))
    filtered_data2 = data2[ data2['year'].isin(year_filter2)  ]
    st.write(filtered_data2)


    fig2 = px.bar(filtered_data2, x='month', y="moving_avg", color='direction')
    st.plotly_chart(fig2)
# Function to plot bar chart using Streamlit
def plot_bar_chart(df):
    device_counts = df['Device_Type'].value_counts()
    st.bar_chart(device_counts)

# Function to plot bar chart for total users per country
def plot_country_bar_chart(df):
    country_counts = df['Country'].value_counts().sort_values(ascending=False)
    st.bar_chart(country_counts)
# Generate demo data for device type
np.random.seed(0)
data_device = {
    'User_ID': np.arange(1000),
    'Device_Type': np.random.choice(['Desktop', 'Mobile', 'Tablet'], size=1000)
}
df_device = pd.DataFrame(data_device)

# Generate demo data for country
np.random.seed(0)
data_country = {
    'User_ID': np.arange(1000),
    'Country': np.random.choice(['USA', 'UK', 'Canada', 'Australia', 'Germany'], size=1000)
}
df_country = pd.DataFrame(data_country)
# Main Streamlit app
def main():
    st.sidebar.title('Departments')
    department = st.sidebar.radio('Select Department', ['Finance', 'Marketing', 'Interactive requests'])
    st.markdown("# Neobank Transaction Analysis Dashboard")
    if department == 'Finance':
        st.markdown("## Total amount of **transactions** per type")
        st.markdown("> *this chart illustrates the amount of transactions recorded during a year/month for neobank customer's activities*")
        total_amt_transaction_type()
        st.markdown("## Moving average of transactions")
        st.markdown("> *this chart illustrates the moving average recorded during a year/month for neobank customer's activities*")
        moving_average_transactions()
    elif department == 'Marketing':
        st.markdown("## Total users per country")
        plot_country_bar_chart(df_country)
    elif department == 'Interactive requests':
        st.markdown("## Total users per country")
        plot_country_bar_chart(df_country)

if __name__ == "__main__":
    main()
