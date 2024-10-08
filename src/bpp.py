import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import get_historical_data, get_crypto_info
from predictor import predict_future_prices
from in_utils import get_not_so_random_quote

def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title="Previsão de Criptomoedas", page_icon="₿📈", layout="wide")

    # Sidebar
    with st.sidebar:
        st.header("Escolha da Criptomoeda")
        crypto_id = st.selectbox("Selecione a criptomoeda", ["bitcoin", "ethereum", "dogecoin"])
        st.write("Use o seletor acima para escolher qual criptomoeda deseja acompanhar.")
        
        # Fetch and display crypto info
        crypto_info = get_crypto_info(crypto_id)
        if crypto_info:
            st.image(crypto_info['image']['large'], width=100)
            st.subheader(crypto_info['name'])
            st.write(crypto_info['description']['en'][:200] + "...")

            if 'homepage' in crypto_info['links'] and crypto_info['links']['homepage'][0]:
                st.markdown(f"[Site Oficial]({crypto_info['links']['homepage'][0]})")

            if 'coingecko' in crypto_info['links']:
                st.markdown(f"[CoinGecko]({crypto_info['links']['coingecko']})")

            st.subheader("Informações Rápidas")
            st.write(f"**Preço Atual:** R$ {crypto_info['market_data']['current_price']['brl']}")
            st.write(f"**Capitalização de Mercado:** R$ {crypto_info['market_data']['market_cap']['brl']}")
            st.write(f"**Volume de Negociação (24h):** R$ {crypto_info['market_data']['total_volume']['brl']}")

    st.title("Previsão de Preços de Criptomoedas")
    st.write("""
        Esta aplicação utiliza dados históricos e modelos de séries temporais para prever os preços futuros
        de criptomoedas como **Bitcoin**, **Ethereum** e **Dogecoin**. Aproveite para explorar gráficos interativos e obter previsões para até 90 dias.
    """)

    # Show current price and history
    st.header(f"💰 Preço atual e histórico de {crypto_id.capitalize()}")
    with st.spinner('Carregando dados...'):
        df = get_historical_data(crypto_id)
    if df is not None:
    
        # Prices plot
        fig = px.line(df, x='timestamp', y='price', title=f'Preço histórico de {crypto_id.capitalize()}')
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast
        st.header(f"📈 Previsão de preços futuros de {crypto_id.capitalize()}")
        
        st.write("Previsão baseada nos dados históricos dos últimos 365 dias, utilizando o modelo LSTM.")
        
        periods = st.slider("Selecione o número de dias para previsão", 1, 90, 30)
        
        with st.spinner('Gerando previsões...'):
            forecast = predict_future_prices(df, periods)
            st.write(forecast)  # Debug print to check the forecast DataFrame
        
        # Forecast graph
        fig_forecast = px.line(forecast, x='ds', y='forecast', title=f'Previsão de preço futuro para {crypto_id.capitalize()} (Próximos {periods} dias)')
        st.plotly_chart(fig_forecast, use_container_width=True)

        #st.subheader("Tabela de Previsões")
        #st.dataframe(forecast[['ds', 'forecast']].tail(periods))
  
    st.divider()

    #if st.button("🔄 Atualizar dados"):
    #    st.experimental_rerun()
    
    random_quote = get_not_so_random_quote()

    st.markdown(
        f"""
        <style>
        @keyframes dance {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0); }}
        }}
        .dance {{
            animation: dance 1s infinite;
        }}
        </style>
        <div class='dance' style='text-align: center; font-family: "Hack", Courier, monospace; font-size: 24px; color: #ffe600;'>
            {random_quote}
        </div>
        """,
        unsafe_allow_html=True
    )
        
if __name__ == "__main__":
    main()