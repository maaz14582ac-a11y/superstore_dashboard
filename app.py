import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Global Superstore Business Dashboard")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Global_Superstore2.csv", encoding="latin-1")
    return df

df = load_data()

# ---------------------------
# Data Cleaning
# ---------------------------
df.dropna(inplace=True)
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]

# ---------------------------
# KPI Calculations
# ---------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# ---------------------------
# KPI Display
# ---------------------------
col1, col2 = st.columns(2)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")

# ---------------------------
# Charts
# ---------------------------
st.subheader("🏆 Top 5 Customers by Sales")

fig, ax = plt.subplots()
top_customers.plot(kind="bar", ax=ax)
ax.set_ylabel("Sales")
ax.set_xlabel("Customer")
ax.set_title("Top 5 Customers")

st.pyplot(fig)

# ---------------------------
# Data Preview
# ---------------------------
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_df.head(20))
