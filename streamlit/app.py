import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="OLA Ride Analytics Dashboard",
    page_icon="🚖",
    layout="wide"
)

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("OLA_SQL.csv")
    return df

df = load_data()

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.title("🚖 OLA Dashboard")

vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

payment = st.sidebar.multiselect(
    "Payment Method",
    df["Payment_Method"].dropna().unique(),
    default=df["Payment_Method"].dropna().unique()
)

df = df[
    (df["Vehicle_Type"].isin(vehicle))
    &
    (df["Payment_Method"].isin(payment))
]

# ---------------------------
# KPIs
# ---------------------------
total_rides = len(df)

total_revenue = df["Booking_Value"].sum()

success_rides = (df["Booking_Status"] == "Success").sum()

success_rate = round(
    (success_rides / total_rides) * 100,
    2
)

avg_customer_rating = round(
    df[df["Customer_Rating"] > 0]["Customer_Rating"].mean(),
    2
)

# ---------------------------
# Title
# ---------------------------
st.title("🚖 OLA Ride Analytics Dashboard")

# ---------------------------
# KPI Row
# ---------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Rides", f"{total_rides:,}")
c2.metric("Revenue", f"₹{total_revenue:,.0f}")
c3.metric("Successful Rides", f"{success_rides:,}")
c4.metric("Success Rate", f"{success_rate}%")
c5.metric("Avg Rating", avg_customer_rating)

# ---------------------------
# Row 1
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    revenue_vehicle = (
        df.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue_vehicle,
        x="Vehicle_Type",
        y="Booking_Value",
        title="Revenue by Vehicle Type"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    status = (
        df["Booking_Status"]
        .value_counts()
        .reset_index()
    )

    status.columns = [
        "Booking_Status",
        "Count"
    ]

    fig = px.pie(
        status,
        names="Booking_Status",
        values="Count",
        title="Booking Status Breakdown"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Row 2
# ---------------------------
col3, col4 = st.columns(2)

with col3:

    payment_data = (
        df.groupby("Payment_Method")["Booking_Value"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        payment_data,
        x="Payment_Method",
        y="Booking_Value",
        title="Revenue by Payment Method"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:

    ratings = (
        df[df["Customer_Rating"] > 0]
        .groupby("Vehicle_Type")["Customer_Rating"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        ratings,
        x="Vehicle_Type",
        y="Customer_Rating",
        title="Average Customer Rating"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Cancellation Analysis
# ---------------------------
st.subheader("Cancellation Analysis")

col5, col6 = st.columns(2)

with col5:

    customer_cancel = (
        df["Canceled_Rides_by_Customer"]
        .value_counts()
        .reset_index()
    )

    customer_cancel.columns = [
        "Reason",
        "Count"
    ]

    fig = px.pie(
        customer_cancel,
        names="Reason",
        values="Count",
        title="Customer Cancellation Reasons"
    )

    st.plotly_chart(fig, use_container_width=True)

with col6:

    driver_cancel = (
        df["Canceled_Rides_by_Driver"]
        .value_counts()
        .reset_index()
    )

    driver_cancel.columns = [
        "Reason",
        "Count"
    ]

    fig = px.pie(
        driver_cancel,
        names="Reason",
        values="Count",
        title="Driver Cancellation Reasons"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Raw Data
# ---------------------------
st.subheader("Dataset Preview")

st.dataframe(df.head(100))