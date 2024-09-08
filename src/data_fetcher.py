import requests
import pandas as pd
import streamlit as st

@st.cache_data
def get_historical_data(crypto_id):
    """
    Fetch the historical price data of the cryptocurrency from the CoinGecko API.
    """
    url= f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=brl&days=365"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro ao obter dados históricos: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter dados históricos: {e}")
        return None

@st.cache_data
def get_crypto_info(crypto_id):
    """
    Fetch the information of the cryptocurrency from the CoinGecko API.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro ao obter informações da criptomoeda: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter informações da criptomoeda: {e}")
        return None
