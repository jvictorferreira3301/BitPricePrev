import streamlit as st
import plotly.express as px
from crypto_data import get_crypto_price, get_historical_data
from forecast import forecast_prices

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
