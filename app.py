import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="NFHS India Dashboard", layout="wide")
st.title("📊 National Family Health Survey (NFHS) Dashboard")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey (2).csv")
    return df



# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filter Data")

# Select State (if exists)

year_col = [col for col in df.columns if "year" in col.lower()]

filtered_df = df.copy()

if state_col:
    states = st.sidebar.multiselect(
        "Select State(s)",
        options=sorted(df[state_col[0]].dropna().unique()),
        default=sorted(df[state_col[0]].dropna().unique())
    )
    filtered_df = filtered_df[filtered_df[state_col[0]].isin(states)]

if year_col:
    years = st.sidebar.multiselect(
        "Select Year(s)",
        options=sorted(df[year_col[0]].dropna().unique()),
        default=sorted(df[year_col[0]].dropna().unique())
    )
    filtered_df = filtered_df[filtered_df[year_col[0]].isin(years)]

# -----------------------------
# Raw Data View
# -----------------------------
with st.expander("📂 View Raw Data"):
    st.dataframe(filtered_df)

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📌 Key Metrics")

numeric_cols = filtered_df.select_dtypes(include="number").columns

if len(numeric_cols) >= 3:
    col1, col2, col3 = st.columns(3)
    col1.metric(numeric_cols[0], round(filtered_df[numeric_cols[0]].mean(), 2))
    col2.metric(numeric_cols[1], round(filtered_df[numeric_cols[1]].mean(), 2))
    col3.metric(numeric_cols[2], round(filtered_df[numeric_cols[2]].mean(), 2))

# -----------------------------
# Visualization Section
# -----------------------------
st.subheader("📈 Visual Analysis")

if len(numeric_cols) > 0:

    selected_metric = st.selectbox(
        "Select Indicator to Visualize",
        numeric_cols
    )

    chart_type = st.radio(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Histogram"]
    )

    if state_col and chart_type == "Bar Chart":
        fig = px.bar(
            filtered_df,
            x=state_col[0],
            y=selected_metric,
            color=state_col[0],
            title=f"{selected_metric} by State"
        )

    elif year_col and chart_type == "Line Chart":
        grouped = filtered_df.groupby(year_col[0])[selected_metric].mean().reset_index()
        fig = px.line(
            grouped,
            x=year_col[0],
            y=selected_metric,
            markers=True,
            title=f"{selected_metric} Trend Over Time"
        )

    else:
        fig = px.histogram(
            filtered_df,
            x=selected_metric,
            title=f"Distribution of {selected_metric}"
        )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No numeric columns available for visualization.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
