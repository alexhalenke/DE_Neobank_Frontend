import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery
import os
import altair as alt
import plotly.graph_objects as go

project = "sylvan-apogee-402010"

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

    df = run_query(f"SELECT total_amount, year, transactions_type, transaction_group, direction, month FROM `{project}.neobank_Gold_Tier.amt_trx_mart` order by year, month")
    data = pd.DataFrame(df, columns=['total_amount', 'transaction_group', 'year', 'month', 'direction', 'transactions_type'])
    year_filter = st.multiselect('Select Year', options=list(data['year'].unique()), default=list(data['year'].unique()))
    month_filter = st.multiselect('Select Month', options=list(data['month'].unique()), default=list(data['month'].unique()))
    #direction_filter = st.multiselect('Select direction', options=list(data['direction'].unique()), default=list(data['direction'].unique()))
    transaction_filter = st.multiselect('Select type of transaction', options=list(data['transactions_type'].unique()), default=list(data['transactions_type'].unique()))
    filtered_data = data[ data['year'].isin(year_filter) & data['month'].isin(month_filter) & data['transactions_type'].isin(transaction_filter) ]
    # Filtrer les données sur les frais
    filtered_fee_data = data[data['transaction_group'] == 'FEE']
    filtered_ohter_data = data[data['transaction_group'] == 'OTHER TRX']


    col1,col2,col3 = st.columns(3)
    lnk = '<img src="https://fonts.gstatic.com/s/i/materialicons/star/v10/24px.svg" width="50" height="50">'
    lnk2 = '<img src="https://fonts.gstatic.com/s/i/materialicons/monetization_on/v10/24px.svg" width="50" height="50">'
    lnk3 = '<img src="https://fonts.gstatic.com/s/i/materialicons/account_balance/v10/24px.svg" width="50" height="50">'
    with col1:
        st.markdown("<h4>Total transactions amount </h4>", unsafe_allow_html=True)
        wch_colour_box = (226, 223, 210)
        # wch_colour_box = (255, 255, 255)
        wch_colour_font = (0, 0, 0)
        fontsize = 30
        valign = "left"
        iconname = "star"
        i = round(data["total_amount"].sum(),1)

        htmlstr = f"""
            <p style='background-color: rgb(
                {wch_colour_box[0]},
                {wch_colour_box[1]},
                {wch_colour_box[2]}, 0.75
            );
            color: rgb(
                {wch_colour_font[0]},
                {wch_colour_font[1]},
                {wch_colour_font[2]}, 0.75
            );
            font-size: {fontsize}px;
            border-radius: 7px;
            padding-top: 40px;
            padding-bottom: 40px;
            line-height:25px;
            display: flex;
            align-items: center;
            justify-content: center;'>
             <i class='{iconname}' style='font-size: 40px; color: #FAF9F6;'></i>&nbsp;{i}</p>
        """
        st.markdown(lnk+htmlstr, unsafe_allow_html=True)
    with col2:
        st.markdown("<h4>Total transactions fees </h4>", unsafe_allow_html=True)
        wch_colour_box = (226, 223, 210)
        # wch_colour_box = (255, 255, 255)
        wch_colour_font = (0, 0, 0)
        fontsize = 50
        valign = "center"
        iconname = "dollars"
        i2 = round(filtered_fee_data["total_amount"].sum(),1)

        htmlstr2 = f"""
            <p style='background-color: rgb(
                {wch_colour_box[0]},
                {wch_colour_box[1]},
                {wch_colour_box[2]}, 0.75
            );
            color: rgb(
                {wch_colour_font[0]},
                {wch_colour_font[1]},
                {wch_colour_font[2]}, 0.75
            );
            font-size: {fontsize}px;
            border-radius: 7px;
            padding-top: 40px;
            padding-bottom: 40px;
            line-height:25px;
            display: flex;
            align-items: center;
            justify-content: center;'>
            <i class='{iconname}' style='font-size: 20px; color: #FAF9F6;'></i>&nbsp;{i2}</p>
        """
        st.markdown(lnk2+htmlstr2, unsafe_allow_html=True)
    with col3:
        st.markdown("<h4>Total transactions without fees  </h4>", unsafe_allow_html=True)
        wch_colour_box = (226, 223, 210)
        # wch_colour_box = (255, 255, 255)
        wch_colour_font = (0, 0, 0)
        fontsize = 30
        valign = "right"
        iconname = "bank"
        i3 = round(filtered_ohter_data["total_amount"].sum(),1)

        htmlstr3 = f"""
            <p style='background-color: rgb(
                {wch_colour_box[0]},
                {wch_colour_box[1]},
                {wch_colour_box[2]}, 0.75
            );
            color: rgb(
                {wch_colour_font[0]},
                {wch_colour_font[1]},
                {wch_colour_font[2]}, 0.75
            );
            font-size: {fontsize}px;
            border-radius: 7px;
            padding-top: 40px;
            padding-bottom: 40px;
            line-height:25px;
            display: flex;
            align-items: center;
            justify-content: center;'>
            <i class='{iconname}' style='font-size: 20px; color: #FAF9F6;'></i>&nbsp;{i3}</p>
        """
        st.markdown(lnk3+htmlstr3, unsafe_allow_html=True)

    #plotting Total amount of transactions per type
    fig = px.bar(filtered_data, x='transactions_type', y='total_amount', color='transaction_group')
    fig['layout']['yaxis'].update(autorange = True)

    #CSS STYLE
    PLOT_BGCOLOR ="#FAF9F6"
    #"#E5E4E2"

    st.markdown(
        f"""
        <style>
        .stPlotlyChart {{
        outline: 10px solid {PLOT_BGCOLOR};
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
        }}
        </style>
        """, unsafe_allow_html=True
    )


    fig.update_layout(
    paper_bgcolor=PLOT_BGCOLOR,
    plot_bgcolor=PLOT_BGCOLOR,
    title_text="Transactions",
    margin=dict(pad=0, r=20, t=50, b=60, l=60)
)

    st.plotly_chart(fig)
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    st.button('Show detail values', on_click=click_button)
    if st.session_state.clicked:

        st.write(filtered_data)

def moving_average_transactions():
    df2 = run_query(f"SELECT year, month, direction, moving_avg FROM `{project}.neobank_Gold_Tier.moving_avg_trx_mart` order by  year, month")
    data2 = pd.DataFrame(df2, columns=['year', 'month', 'direction', 'moving_avg'])
    year_filter2 = st.multiselect('Select Year', options=list(data2['year'].unique()), default=list(data2['year'].unique()), key='year_filter2')
    #month_filter2 = st.multiselect('Select Month', options=list(data2['month'].unique()), default=list(data2['month'].unique()), key='month_filter2')
    #direction_filter = st.multiselect('Select direction', options=list(data2['direction'].unique()), default=list(data2['direction'].unique()))
    filtered_data2 = data2[ data2['year'].isin(year_filter2)  ]

    fig2 = px.line(filtered_data2, x='month', y="moving_avg", color='direction')
    PLOT_BGCOLOR ="#FAF9F6"
    st.markdown(
        f"""
        <style>
        .stPlotlyChart {{
        outline: 10px solid {PLOT_BGCOLOR};
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
        }}
        </style>
        """, unsafe_allow_html=True
    )


    fig2.update_layout(
    paper_bgcolor=PLOT_BGCOLOR,
    plot_bgcolor=PLOT_BGCOLOR,
    title_text="Transactions",
    margin=dict(pad=0, r=20, t=50, b=60, l=60)
)
    st.plotly_chart(fig2)




def unique_number_users() :
    import plotly.graph_objects as go
    df4 = run_query(f"SELECT total_customers, device_type FROM `{project}.neobank_Gold_Tier.customers_by_device_type_mart`")
    data4 = pd.DataFrame(df4, columns=['total_customers', 'device_type'])
    labels = data4 ['device_type']
    values = data4['total_customers']
    fig4 = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 insidetextorientation='radial'
                                )])
    PLOT_BGCOLOR ="#FAF9F6"
    st.markdown(
        f"""
        <style>
        .stPlotlyChart {{
        outline: 10px solid {PLOT_BGCOLOR};
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
        }}
        </style>
        """, unsafe_allow_html=True
    )


    fig4.update_layout(
    paper_bgcolor=PLOT_BGCOLOR,
    plot_bgcolor=PLOT_BGCOLOR,
    title_text="Unique Users",
    margin=dict(pad=0, r=20, t=50, b=60, l=60)
)

    st.plotly_chart(fig4)


def customers_by_notif() :

    df3 = run_query(f"SELECT total_customers, notification_reason, channel FROM `{project}.neobank_Gold_Tier.unique_customers_mart`")
    data3 = pd.DataFrame(df3, columns=['total_customers', 'notification_reason','channel'])
    fig3 = px.funnel(data3, x='total_customers', y='notification_reason', color='channel')
    PLOT_BGCOLOR ="#FAF9F6"
    st.markdown(
        f"""
        <style>
        .stPlotlyChart {{
        outline: 10px solid {PLOT_BGCOLOR};
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
        }}
        </style>
        """, unsafe_allow_html=True
    )


    fig3.update_layout(
    paper_bgcolor=PLOT_BGCOLOR,
    plot_bgcolor=PLOT_BGCOLOR,
    title_text="Notification reason",
    margin=dict(pad=0, r=20, t=50, b=60, l=60)
)

    st.plotly_chart(fig3)

def agesegmentation() :
    df4 = run_query(f"SELECT total_customers, average_amount_by_age, age_band FROM `{project}.neobank_Gold_Tier.customers_age_mart`")
    data4 = pd.DataFrame(df4, columns=['total_customers', 'average_amount_by_age','age_band'])

    base = alt.Chart(data4).encode(x='age_band')

    bar = base.mark_bar().encode(y='total_customers')

    line =  base.mark_line(color='red').encode(
        y2='average_amount_by_age'
    )

    chart = (bar + line).properties(width=600)
    PLOT_BGCOLOR ="#FAF9F6"
    st.markdown(
        f"""
        <style>
        .stAltairChart {{
        outline: 10px solid {PLOT_BGCOLOR};
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
        }}
        </style>
        """, unsafe_allow_html=True
    )

    fig= st.altair_chart(chart, use_container_width=True)
    fig.update_layout(
    paper_bgcolor=PLOT_BGCOLOR,
    plot_bgcolor=PLOT_BGCOLOR,
    title_text="Age Segmentation",
    margin=dict(pad=0, r=20, t=50, b=60, l=60)
)


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
    st.markdown("# Neobank Transactions Analysis Dashboard")

    if department == 'Finance':
        st.markdown("## Total amount of **transactions** per type")
        st.markdown("> *this chart illustrates the amount of transactions recorded during a year/month for neobank customer's activities*")
        total_amt_transaction_type()
        st.markdown("## Moving average of transactions")
        st.markdown("> *this chart illustrates the moving average recorded during a year/month for neobank customer's activities*")
        moving_average_transactions()

    elif department == 'Marketing':
        st.markdown("## Total users per device type")
        st.markdown("> *this chart illustrates the unique number of users per device*")
        unique_number_users()

        st.markdown("## Number of customers by notification type")
        st.markdown("> *this chart illustrates the Number of customers by notification type*")
        customers_by_notif()

        st.markdown("## Age Segmentation")
        st.markdown("> *this chart illustrates the Number of customers by notification type*")
        agesegmentation()

    elif department == 'Interactive requests':
        st.markdown("## Total users per country")
        plot_country_bar_chart(df_country)

if __name__ == "__main__":
    main()
