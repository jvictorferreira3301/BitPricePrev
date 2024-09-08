import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from darts import TimeSeries
from darts.models import ExponentialSmoothing

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

def forecast_prices(df):
    series = TimeSeries.from_dataframe(df, 'timestamp', 'price')
    model = ExponentialSmoothing()
    model.fit(series)
    future = model.predict(60)
    return future

def main():
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
        
        st.header(f"Previsão de preços futuros de {crypto_id.capitalize()}")
        try:
            future = forecast_prices(df)
            future_df = future.pd_dataframe()
            fig_future = px.line(future_df, x='time', y='value', title=f'Previsão de preços de {crypto_id.capitalize()}')
            st.plotly_chart(fig_future)
        except Exception as e:
            st.error(f"Erro ao gerar previsão: {e}")
    
    if st.button("Atualizar"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()

