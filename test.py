import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Assuming df is your DataFrame
df = pd.read_csv('RBLX.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate the rolling mean
rolling_mean = df['Close'].rolling(window=20).mean()

# Function to update the plot based on user input
def update_plot(start_date, end_date, plot_type):
    subset = df[start_date:end_date]
    
    plt.figure(figsize=(12, 6))
    
    if plot_type == 'line':
        plt.plot(subset['Close'], label='Closing Price', marker='o')
        plt.title('Closing Price Over Time')
    elif plot_type == 'candlestick':
        ax = plt.subplot()
        ax.grid(True)
        ax.set_axisbelow(True)
        ax.set_title('Candlestick Chart')
        ax.plot(subset.index, subset['Close'], label='Closing Price', marker='o')
        ax.plot(subset.index, subset['Open'], label='Opening Price', marker='o')
        ax.plot(subset.index, subset['High'], label='High Price', marker='o')
        ax.plot(subset.index, subset['Low'], label='Low Price', marker='o')
        ax.legend()
        ax.xaxis_date()

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot()

# Streamlit app
st.title('Financial Data Analysis with Streamlit')

# Create interactive widgets
start_date_widget = st.date_input('Start Date', min_value=df.index.min(), max_value=df.index.max(), value=df.index.min())
end_date_widget = st.date_input('End Date', min_value=df.index.min(), max_value=df.index.max(), value=df.index.max())
plot_type_widget = st.selectbox('Plot Type', ['line', 'candlestick'], index=0)

# Create an interactive plot
update_plot(start_date_widget, end_date_widget, plot_type_widget)

# Display bar chart
st.bar_chart(df['Volume'])
st.title('Volume Over Time')

# Display line chart with moving average
st.line_chart(pd.DataFrame({'Close': df['Close'], '20-day Moving Avg': rolling_mean}))
st.title('Closing Price with 20-day Moving Average')

# Select a specific date range for analysis
start_date = '2022-01-01'
end_date = '2022-01-31'
subset = df[start_date:end_date]

# Calculate the percentage change in closing prices
subset['Change'] = subset['Close'].pct_change() * 100

# Classify changes as positive, negative, or neutral
positive_threshold = 0.5
negative_threshold = -0.5

subset['Change_Category'] = pd.cut(subset['Change'], bins=[float('-inf'), negative_threshold, positive_threshold, float('inf')],
                                   labels=['Negative', 'Neutral', 'Positive'], include_lowest=True)

# Count the occurrences of each category
change_counts = subset['Change_Category'].value_counts()

# Create a pie chart using Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(change_counts, labels=change_counts.index, colors=['red', 'gray', 'green'], autopct='%1.1f%%', startangle=140)
ax.set_title('Distribution of Closing Price Changes')

# Display the pie chart using st.pyplot()
st.pyplot(fig)
