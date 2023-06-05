import os
import requests
from PIL import Image
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

# Function to get cryptocurrency icon URL
def get_crypto_icon_url(crypto_name):
    response = requests.get(f"{API_ENDPOINT}/{crypto_name}")
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return data["data"]["coin"]["iconUrl"]
    return None

def display_sidebar():
    crypto_names = ["bitcoin", "ethereum", "litecoin"]  # Add more cryptocurrency names as needed

    st.sidebar.title("Cryptocurrencies")
    selected_crypto = st.sidebar.selectbox("Select a cryptocurrency", crypto_names)

    return selected_crypto

def display_main_section(crypto_name):
    crypto_data = get_crypto_data(crypto_name)

    # Display cryptocurrency name and image
    st.title(crypto_name.capitalize())
    crypto_icon_url = get_crypto_icon_url(crypto_name)
    if crypto_icon_url:
        response = requests.get(crypto_icon_url)
        if response.status_code == 200:
            icon = Image.open(BytesIO(response.content))
            st.image(icon, caption=crypto_name.capitalize(), use_column_width=True)

    # Display bar chart of cryptocurrency prices
    st.subheader("Price Chart")
    fig, ax = plt.subplots()
    ax.bar(crypto_data["close"], crypto_data["price"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(f"{crypto_name.capitalize()} Price Chart")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="Cryptocurrency Dashboard")

    selected_crypto = display_sidebar()
    display_main_section(selected_crypto)

if __name__ == "__main__":
    main()
