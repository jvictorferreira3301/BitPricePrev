import requests
import pandas as pd
import streamlit as st

@st.cache_data
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=brl"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[crypto_id]['brl']
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("Erro 429: Muitas requisições. Por favor, tente novamente mais tarde.")
        else:
            st.error(f"Erro ao obter o preço: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter o preço: {e}")
        return None

@st.cache_data
def get_historical_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=brl&days=30"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("Erro 429: Muitas requisições. Por favor, tente novamente mais tarde.")
        else:
            st.error(f"Erro ao obter dados históricos: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter dados históricos: {e}")
        return None
