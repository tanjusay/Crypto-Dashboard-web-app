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
        if data["status"] == "success" and data["data"]["stats"]["total"] > 0:
            st.write(data)
            return data["data"]["coins"][0]
    return None


def display_sidebar():
    crypto_names = ["bitcoin", "ethereum", "litecoin"]  # Add more cryptocurrency names as needed

    st.sidebar.title("Cryptocurrencies")
    selected_crypto = st.sidebar.selectbox("Select a cryptocurrency", crypto_names)

    return selected_crypto


# Function to display cryptocurrency data in main section
def display_main_section(crypto_name):
    crypto_data = get_crypto_data(crypto_name)

    if crypto_data:
        # Display cryptocurrency name and image URL
        st.title(crypto_data["name"])
        st.image(crypto_data["iconUrl"], caption=crypto_data["name"], use_column_width=True)

        # Display bar chart of cryptocurrency prices
        st.subheader("Price Chart")
        history = crypto_data.get("history")
        if history:
            dates = []
            prices = []
            for item in history:
                dates.append(item["timestamp"])
                prices.append(item["price"])
            fig, ax = plt.subplots()
            ax.bar(dates, prices)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.set_title(f"{crypto_data['name']} Price Chart")
            plt.xticks(rotation=45)
            st.pyplot(fig)



def main():
    st.set_page_config(page_title="Cryptocurrency Dashboard")

    selected_crypto = display_sidebar()
    display_main_section(selected_crypto)


if __name__ == "__main__":
    main()
