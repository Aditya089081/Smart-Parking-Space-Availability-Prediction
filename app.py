

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

# Load the dataset
df = pd.read_excel("car_parking_dataset.xlsx")
df['Entry_Time'] = pd.to_datetime(df['Entry_Time'])
df['is_weekend_entry'] = (df['Entry_Time'].dt.weekday >= 5).astype(int)

# Simulated prediction function (replace with real model later)
def make_prediction(vehicle_type, duration, parking_slot, parking_level, payment_status):
    price = random.randint(10, 50)
    
    if duration > 120:
        availability = "Not Available"
    else:
        availability = "Available"
        
    return price, availability

# Function: dynamic plot that changes per prediction
def plot_prediction_impact(vehicle_type):
    categories = ['Car', 'Bike', 'Truck', 'Bus']
    counts = [random.randint(10, 50) for _ in categories]
    
    fig, ax = plt.subplots()
    sns.barplot(x=categories, y=counts, palette='viridis', ax=ax)
    ax.set_title("Vehicle Type Count (Dynamic)")
    ax.set_xlabel("Vehicle Type")
    ax.set_ylabel("Count")
    return fig

# Function: static boxplot
def plot_boxplot_by_parking_level():
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x='Parking_Level', y='Amount_Charged', palette='coolwarm', ax=ax)
    ax.set_title("Amount Charged by Parking Level")
    ax.set_xlabel("Parking Level")
    ax.set_ylabel("Amount Charged")
    return fig

# Function: static countplot (Weekday vs Weekend)
def plot_weekend_entries():
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='is_weekend_entry', ax=ax)
    ax.set_title("Entries on Weekdays vs Weekends")
    ax.set_xlabel("Day Type")
    ax.set_ylabel("Number of Entries")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Weekday', 'Weekend'])
    return fig

# Streamlit UI
st.title("🚗 Parking Availability Prediction System")

# User input
vehicle_type = st.selectbox("Vehicle Type", ["Car", "Bike", "Truck", "Bus"])
duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=30)
parking_slot = st.selectbox("Parking Slot", ["Slot 1", "Slot 2", "Slot 3", "Slot 4"])
parking_level = st.selectbox("Parking Level", df["Parking_Level"].unique())
payment_status = st.selectbox("Payment Status", ["Paid", "Unpaid"])

if st.button("Predict"):
    price, availability = make_prediction(vehicle_type, duration, parking_slot, parking_level, payment_status)

    st.success(f"Predicted Price: ₹{price}")
    st.info(f"Space Availability: {availability}")

    st.subheader(" Vehicle Type Distribution")
    fig1 = plot_prediction_impact(vehicle_type)
    st.pyplot(fig1)

    st.subheader(" Amount Charged by Parking Level")
    fig2 = plot_boxplot_by_parking_level()
    st.pyplot(fig2)

    st.subheader(" Entries on Weekdays vs Weekends")
    fig3 = plot_weekend_entries()
    st.pyplot(fig3)
