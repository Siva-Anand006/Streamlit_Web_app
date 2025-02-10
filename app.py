import streamlit as st
import pandas as pd
import numpy as np

# Set the title of the app
st.title("Simple Streamlit App")

# Create a text input for user name
name = st.text_input("Enter your name:", "")

# Display a welcome message
if name:
    st.write(f"Hello, {name}! Welcome to this simple Streamlit app. 🎉")

# Generate random data for a chart
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

# Display a line chart
st.line_chart(chart_data)

# Add a button
if st.button("Click me!"):
    st.success("You clicked the button! 🚀")
