import requests
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def get_crypto_price(crypto_id):
    """
    Fetch the current price of the cryptocurrency from the CoinGecko API.
    """
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
    """
    Fetch the historical price data of the cryptocurrency from the CoinGecko API.
    """
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

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Preço de Criptomoedas")
    
    crypto_id = st.selectbox("Selecione a criptomoeda", ["bitcoin", "ethereum", "dogecoin"])
    
    st.header(f"Preço atual de {crypto_id.capitalize()}")
    price = get_crypto_price(crypto_id)
    if price:
        st.write(f"O preço atual de {crypto_id.capitalize()} é: R$ {price}")
    
    st.header(f"Gráfico de preços históricos de {crypto_id.capitalize()}")
    df = get_historical_data(crypto_id)
    if df is not None:
        fig = px.line(df, x='timestamp', y='price', title=f'Preço histórico de {crypto_id.capitalize()}')
        st.plotly_chart(fig)
    
    if st.button("Atualizar"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
