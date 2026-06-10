import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🌍 Global Cyber Attack Intelligence Dashboard")

# Load data
data = pd.read_csv("cyber_real.csv")

# Filter FIRST (important)
st.sidebar.header("Filter Data")

selected_country = st.sidebar.selectbox(
    "🌍 Select Country",
    ["All"] + sorted(data["Country"].dropna().unique())
)

if selected_country != "All":
    filtered_data = data[data["Country"] == selected_country]
else:
    filtered_data = data

# Show dataset
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_data.head())

# Dashboard
st.subheader("📊 Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.metric("🌍 Total Countries", filtered_data["Country"].nunique())
with col2:
    st.metric("⚠️ Total Attacks", len(filtered_data))

# Chart 1
with col1:
    st.write("### Attack Types")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=filtered_data, x="Attack Type", ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# Chart 2
with col2:
    st.write("### Top 10 Countries by Attacks")

    top_countries = filtered_data["Country"].value_counts().nlargest(10).index

    fig2, ax2 = plt.subplots()
    sns.countplot(
        data=filtered_data[filtered_data["Country"].isin(top_countries)],
        x="Country",
        ax=ax2
    )

    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Chart 3
st.write("### Attack Trend Over Years")
fig3, ax3 = plt.subplots()
sns.countplot(data=filtered_data, x="Year", ax=ax3)
st.pyplot(fig3)

import plotly.express as px

st.write("### 🌍 Global Attack Distribution")

# Count attacks per country
country_counts = filtered_data["Country"].value_counts().reset_index()
country_counts.columns = ["Country", "Attacks"]

# Create world map
fig_map = px.choropleth(
    country_counts,
    locations="Country",
    locationmode="country names",
    color="Attacks",
    color_continuous_scale="Reds",
    title="Cyber Attacks by Country"
)

st.plotly_chart(fig_map, use_container_width=True)