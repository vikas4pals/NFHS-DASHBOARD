import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="NFHS India Dashboard", layout="wide")

st.title("📊 All India National Family Health Survey Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("/mnt/data/All India National Family Health Survey.csv")
    return df

df = load_data()

# Show raw data
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)

# Sidebar Filters
st.sidebar.header("Filter Options")

# Select State (if column exists)
if "State" in df.columns:
    states = st.sidebar.multiselect(
        "Select State(s)",
        options=df["State"].unique(),
        default=df["State"].unique()
    )
    df = df[df["State"].isin(states)]

# Select Year (if column exists)
if "Year" in df.columns:
    years = st.sidebar.multiselect(
        "Select Year(s)",
        options=df["Year"].unique(),
        default=df["Year"].unique()
    )
    df = df[df["Year"].isin(years)]

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

numeric_cols = df.select_dtypes(include='number').columns

if len(numeric_cols) >= 3:
    col1.metric(numeric_cols[0], round(df[numeric_cols[0]].mean(), 2))
    col2.metric(numeric_cols[1], round(df[numeric_cols[1]].mean(), 2))
    col3.metric(numeric_cols[2], round(df[numeric_cols[2]].mean(), 2))

st.subheader("📈 Data Visualization")

# Select column to visualize
selected_column = st.selectbox(
    "Select Indicator",
    numeric_cols
)

# Bar chart by state (if state column exists)
if "State" in df.columns:
    fig = px.bar(
        df,
        x="State",
        y=selected_column,
        color="State",
        title=f"{selected_column} by State"
    )
else:
    fig = px.histogram(
        df,
        x=selected_column,
        title=f"Distribution of {selected_column}"
    )

st.plotly_chart(fig, use_container_width=True)

# Time trend (if Year exists)
if "Year" in df.columns:
    st.subheader("📊 Trend Over Time")

    if "State" in df.columns:
        trend_df = df.groupby(["Year"])[selected_column].mean().reset_index()
    else:
        trend_df = df.groupby("Year")[selected_column].mean().reset_index()

    fig2 = px.line(
        trend_df,
        x="Year",
        y=selected_column,
        markers=True,
        title=f"{selected_column} Trend Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)
