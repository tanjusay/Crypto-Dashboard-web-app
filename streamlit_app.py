import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CoinRanking API endpoint and headers
API_ENDPOINT = "https://api.coinranking.com/v2/coins"
HEADERS = {"x-access-token": os.getenv("COINRANKING_API_KEY")}

# Function to get cryptocurrency data
def get_crypto_data(crypto_name):
    params = {"symbol": crypto_name}
    response = requests.get(API_ENDPOINT, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return data["data"]["coins"][0]
    return None

# Function to display cryptocurrency data
def display_crypto_data(crypto):
    st.title(crypto['name'].capitalize())

    # Display cryptocurrency icon
    st.image(crypto['iconUrl'], caption=crypto['name'].capitalize(), use_column_width=True)

    # Display cryptocurrency price
    st.subheader("Price")
    st.write(crypto['price'])

    # Display sparkline chart
    st.subheader("Sparkline")
    sparkline = [float(price) for price in crypto['sparkline']]
    fig, ax = plt.subplots()
    ax.plot(sparkline)
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="Cryptocurrency Dashboard")

    crypto_name = "bitcoin"  # Replace with the desired cryptocurrency name
    crypto_data = get_crypto_data(crypto_name)

    if crypto_data:
        display_crypto_data(crypto_data)
    else:
        st.error("Failed to retrieve cryptocurrency data.")

if __name__ == "__main__":
    # Disable the PyplotGlobalUseWarning
    st.set_option('deprecation.showPyplotGlobalUse', False)
    main()
