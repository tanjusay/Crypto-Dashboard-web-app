import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv


load_dotenv()

API_ENDPOINT = "https://api.coinranking.com/v2/coins"
HEADERS = {"x-access-token": os.getenv("COINRANKING_API_KEY")}


# fetch cryptocurrency data
def get_crypto_data():
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return data["data"]["coins"]
    return []

# display cryptocurrency data
def display_crypto_data(crypto_data):
    for crypto in crypto_data:
        st.title(f"{crypto['name']} ({crypto['symbol']})")
        st.image(crypto['iconUrl'], caption=crypto['name'], use_column_width=True)
        st.subheader("Statistics")
        st.text(f"Market Cap: {crypto['marketCap']}")
        st.text(f"Price: {crypto['price']}")
        st.text(f"24h Volume: {crypto['24hVolume']}")
        st.subheader("Sparkline")
        sparkline = [float(price) for price in crypto['sparkline'].values()]
        plt.plot(sparkline)
        st.pyplot(plt)

def main():
    st.set_page_config(page_title="Crypto Dashboard")

    crypto_data = get_crypto_data()
    if crypto_data:
        display_crypto_data(crypto_data)
    else:
        st.error("Failed to fetch cryptocurrency data.")

if __name__ == "__main__":
    main()
