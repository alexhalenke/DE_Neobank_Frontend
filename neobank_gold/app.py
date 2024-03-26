import streamlit as st
import pandas as pd
import numpy as np

# Function to plot bar chart using Streamlit
def plot_bar_chart(df):
    device_counts = df['Device_Type'].value_counts()
    st.bar_chart(device_counts)

# Function to plot bar chart for total users per country
def plot_country_bar_chart(df):
    country_counts = df['Country'].value_counts().sort_values(ascending=False)
    st.bar_chart(country_counts)

def finance_dashboard():
    st.markdown("## Unique users per device type")
    plot_bar_chart(df_device)

def marketing_dashboard():
    st.markdown("## Total users per country")
    plot_country_bar_chart(df_country)

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
    department = st.sidebar.radio('Select Department', ['Finance', 'Marketing'])

    if department == 'Finance':
        finance_dashboard()
    elif department == 'Marketing':
        marketing_dashboard()

if __name__ == "__main__":
    main()
