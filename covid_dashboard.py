import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide")

# Title and description
st.title("🦠 COVID-19 Global Data Dashboard")
st.markdown("Live updates on COVID-19 cases around the world.")

# API URL
API_URL = "https://api.covid19api.com/summary"

# Function to fetch data
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        countries_data = data['Countries']
        df = pd.DataFrame(countries_data)
        return df
    else:
        st.error("Failed to fetch data.")
        return pd.DataFrame()

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data:")
country_list = df['Country'].sort_values().tolist()
selected_countries = st.sidebar.multiselect("Select countries:", country_list, default=["United States", "India", "Brazil"])

# Filter data
if selected_countries:
    filtered_df = df[df['Country'].isin(selected_countries)]
else:
    filtered_df = df

# Global Key Metrics
st.subheader("🌎 Global Numbers")
col1, col2, col3 = st.columns(3)
col1.metric("Total Confirmed", f"{df['TotalConfirmed'].sum():,}")
col2.metric("Total Deaths", f"{df['TotalDeaths'].sum():,}")
col3.metric("Total Recovered", f"{df['TotalRecovered'].sum():,}")

# Bar Chart
st.subheader("📊 Cases by Country (Selected)")
fig = px.bar(filtered_df, 
             x='Country', 
             y='TotalConfirmed', 
             color='Country', 
             title="Total Confirmed COVID-19 Cases by Country")
st.plotly_chart(fig, use_container_width=True)

# Map Visualization
st.subheader("🗺️ Map View (Top 20 Countries by Cases)")
top20 = df.sort_values(by="TotalConfirmed", ascending=False).head(20)
fig_map = px.scatter_geo(top20,
                         locations="CountryCode",
                         locationmode="ISO-3",
                         size="TotalConfirmed",
                         hover_name="Country",
                         title="COVID-19 Spread (Top 20 Countries)",
                         projection="natural earth",
                         color="TotalConfirmed")
st.plotly_chart(fig_map, use_container_width=True)

# Data Table
st.subheader("📄 Raw Data Table (Filtered)")
st.dataframe(filtered_df[['Country', 'TotalConfirmed', 'TotalDeaths', 'TotalRecovered']].sort_values(by="TotalConfirmed", ascending=False))
