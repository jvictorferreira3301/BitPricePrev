import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_fetcher import (get_historical_data, get_crypto_info, get_crypto_list, 
                         get_market_overview, get_trending_cryptos, get_price_comparison, format_currency)
from predictor import predict_future_prices, calculate_technical_indicators
from technical_analysis import (create_candlestick_chart, get_trading_signals, 
                               create_volume_analysis, calculate_price_levels)
from in_utils import get_not_so_random_quote
import numpy as np
from datetime import datetime, timedelta

def create_metrics_cards(crypto_info, df):
    """Create metrics cards for the dashboard."""
    if not crypto_info or df is None or df.empty:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    current_price = crypto_info['market_data']['current_price']['brl']
    change_24h = crypto_info['market_data']['price_change_percentage_24h']
    market_cap = crypto_info['market_data']['market_cap']['brl']
    volume_24h = crypto_info['market_data']['total_volume']['brl']
    
    with col1:
        st.metric(
            label="� Preço Atual",
            value=format_currency(current_price),
            delta=f"{change_24h:.2f}%" if change_24h else None
        )
    
    with col2:
        st.metric(
            label="📊 Cap. de Mercado",
            value=format_currency(market_cap)
        )
    
    with col3:
        st.metric(
            label="📈 Volume 24h",
            value=format_currency(volume_24h)
        )
    
    with col4:
        # Calculate volatility from historical data
        if len(df) > 1:
            volatility = df['price'].pct_change().std() * 100
            st.metric(
                label="📊 Volatilidade",
                value=f"{volatility:.2f}%"
            )

def create_price_charts(df, crypto_name):
    """Create comprehensive price charts."""
    if df is None or df.empty:
        return
    
    # Main price chart with moving averages
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=df['timestamp'], 
        y=df['price'],
        mode='lines',
        name='Preço',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Add moving averages if we have enough data
    if len(df) >= 50:
        df['ma_7'] = df['price'].rolling(window=7).mean()
        df['ma_21'] = df['price'].rolling(window=21).mean()
        df['ma_50'] = df['price'].rolling(window=50).mean()
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['ma_7'],
            mode='lines',
            name='MA 7 dias',
            line=dict(color='orange', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['ma_21'],
            mode='lines',
            name='MA 21 dias',
            line=dict(color='red', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['ma_50'],
            mode='lines',
            name='MA 50 dias',
            line=dict(color='green', width=1)
        ))
    
    fig.update_layout(
        title=f'📈 Histórico de Preços - {crypto_name}',
        xaxis_title='Data',
        yaxis_title='Preço (R$)',
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_forecast_comparison_chart(forecasts, crypto_name, periods):
    """Create a chart comparing different forecast models."""
    if forecasts.empty:
        st.error("Nenhuma previsão disponível")
        return
    
    fig = go.Figure()
    
    models = forecasts['model'].unique()
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, model in enumerate(models):
        model_data = forecasts[forecasts['model'] == model]
        fig.add_trace(go.Scatter(
            x=model_data['ds'],
            y=model_data['forecast'],
            mode='lines+markers',
            name=f'{model}',
            line=dict(color=colors[i % len(colors)], width=2)
        ))
    
    fig.update_layout(
        title=f'🔮 Comparação de Modelos de Previsão - {crypto_name} ({periods} dias)',
        xaxis_title='Data',
        yaxis_title='Preço Previsto (R$)',
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_trading_signals(df, crypto_name):
    """Display trading signals in a nice format."""
    signals = get_trading_signals(df)
    
    if not signals:
        st.info("📊 Nenhum sinal de trading identificado no momento.")
        return
    
    st.subheader("🎯 Sinais de Trading")
    
    for signal_type, description, color in signals:
        if color == "green":
            st.success(f"**{signal_type}**: {description}")
        elif color == "red":
            st.error(f"**{signal_type}**: {description}")
        elif color == "blue":
            st.info(f"**{signal_type}**: {description}")
        elif color == "orange":
            st.warning(f"**{signal_type}**: {description}")

def show_market_overview():
    """Display market overview in sidebar."""
    market_data = get_market_overview()
    
    if market_data:
        st.sidebar.subheader("🌍 Visão Geral do Mercado")
        
        total_market_cap = market_data.get('total_market_cap', {}).get('brl', 0)
        total_volume = market_data.get('total_volume_24h', {}).get('brl', 0)
        btc_dominance = market_data.get('market_cap_percentage', {}).get('btc', 0)
        
        st.sidebar.metric("Cap. Total do Mercado", format_currency(total_market_cap))
        st.sidebar.metric("Volume Total 24h", format_currency(total_volume))
        st.sidebar.metric("Dominância do Bitcoin", f"{btc_dominance:.1f}%")

def show_trending_cryptos():
    """Display trending cryptocurrencies."""
    trending = get_trending_cryptos()
    
    if trending:
        st.sidebar.subheader("🔥 Trending")
        for crypto in trending[:5]:
            name = crypto.get('item', {}).get('name', 'Unknown')
            rank = crypto.get('item', {}).get('market_cap_rank', 'N/A')
            st.sidebar.write(f"#{rank} {name}")

def main():
    """Main function to run the enhanced Streamlit app."""
    st.set_page_config(
        page_title="BitPricePrev - Análise e Previsão de Criptomoedas",
        page_icon="₿📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #f39c12;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f39c12;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("# ⚙️ Configurações")
        
        # Cryptocurrency selection
        crypto_list = get_crypto_list()
        crypto_display = st.selectbox(
            "🪙 Selecione a Criptomoeda",
            options=list(crypto_list.keys()),
            format_func=lambda x: crypto_list[x],
            index=0
        )
        
        # Time period selection
        period_options = {
            30: "30 dias",
            90: "90 dias", 
            180: "180 dias",
            365: "1 ano"
        }
        
        selected_period = st.selectbox(
            "📅 Período Histórico",
            options=list(period_options.keys()),
            format_func=lambda x: period_options[x],
            index=3
        )
        
        # Forecast settings
        st.markdown("### 🔮 Configurações de Previsão")
        forecast_days = st.slider("Dias para previsão", 1, 90, 30)
        
        model_options = {
            'LSTM': 'LSTM (Deep Learning)',
            'Linear': 'Regressão Linear',
            'RandomForest': 'Random Forest',
            'All': 'Todos os Modelos'
        }
        
        selected_model = st.selectbox(
            "🤖 Modelo de Previsão",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            index=0
        )
        
        st.divider()
        
        # Market overview and trending
        show_market_overview()
        show_trending_cryptos()
        
        # Crypto info display
        crypto_info = get_crypto_info(crypto_display)
        if crypto_info:
            st.markdown("### ℹ️ Informações")
            if 'image' in crypto_info and 'large' in crypto_info['image']:
                st.image(crypto_info['image']['large'], width=80)
            
            st.markdown(f"**{crypto_info['name']}**")
            
            if 'description' in crypto_info and 'en' in crypto_info['description']:
                description = crypto_info['description']['en']
                if len(description) > 150:
                    description = description[:150] + "..."
                st.write(description)
            
            if 'links' in crypto_info:
                links = crypto_info['links']
                if 'homepage' in links and links['homepage'] and links['homepage'][0]:
                    st.markdown(f"🌐 [Site Oficial]({links['homepage'][0]})")
    
    # Main content
    st.markdown('<div class="main-header">₿ BitPricePrev</div>', unsafe_allow_html=True)
    st.markdown("### 🚀 Análise Avançada e Previsão de Criptomoedas")
    
    st.markdown("""
    Plataforma completa para análise técnica e previsão de preços de criptomoedas,
    utilizando múltiplos modelos de machine learning e indicadores técnicos avançados.
    """)
    
    # Load data
    with st.spinner('📊 Carregando dados...'):
        df = get_historical_data(crypto_display, days=selected_period)
        crypto_info = get_crypto_info(crypto_display)
    
    if df is not None and crypto_info:
        crypto_name = crypto_info['name']
        
        # Metrics cards
        create_metrics_cards(crypto_info, df)
        
        st.divider()
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Análise de Preços",
            "🔮 Previsões",
            "📊 Análise Técnica",
            "📋 Indicadores",
            "📊 Comparação"
        ])
        
        with tab1:
            st.markdown('<div class="section-header">📈 Análise de Preços</div>', unsafe_allow_html=True)
            
            # Price charts
            create_price_charts(df, crypto_name)
            
            # Volume analysis if available
            if 'volume' in df.columns:
                st.subheader("📊 Análise de Volume")
                volume_chart = create_volume_analysis(df)
                if volume_chart:
                    st.plotly_chart(volume_chart, use_container_width=True)
            
            # Price statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("� Estatísticas do Período")
                price_stats = df['price'].describe()
                st.dataframe(price_stats.round(2))
            
            with col2:
                st.subheader("🎯 Níveis Importantes")
                levels = calculate_price_levels(df)
                st.metric("Preço Atual", format_currency(levels['current_price']))
                st.metric("Máxima 52s", format_currency(levels['high_52w']))
                st.metric("Mínima 52s", format_currency(levels['low_52w']))
        
        with tab2:
            st.markdown('<div class="section-header">🔮 Previsões de Preços</div>', unsafe_allow_html=True)
            
            with st.spinner('🤖 Gerando previsões...'):
                forecast_result = predict_future_prices(df, forecast_days, selected_model)
                
                if isinstance(forecast_result, tuple):
                    forecast, metrics = forecast_result
                else:
                    forecast = forecast_result
                    metrics = {}
            
            if not forecast.empty:
                # Forecast chart
                create_forecast_comparison_chart(forecast, crypto_name, forecast_days)
                
                # Model performance metrics
                if metrics:
                    st.subheader("📏 Métricas dos Modelos")
                    
                    if selected_model == 'All':
                        # Display metrics for all models
                        metrics_df = pd.DataFrame(metrics).T
                        if not metrics_df.empty:
                            # Remove 'history' column if it exists
                            display_metrics = metrics_df.drop(columns=['history'], errors='ignore')
                            st.dataframe(display_metrics.round(4))
                    else:
                        # Display metrics for single model
                        if 'MAE' in metrics:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("MAE", f"{metrics['MAE']:.2f}")
                            with col2:
                                st.metric("RMSE", f"{metrics['RMSE']:.2f}")
                            with col3:
                                st.metric("R²", f"{metrics['R²']:.4f}")
                
                # Forecast table
                st.subheader("📋 Tabela de Previsões")
                if selected_model == 'All':
                    # Group by date and show all models
                    pivot_forecast = forecast.pivot(index='ds', columns='model', values='forecast')
                    st.dataframe(pivot_forecast.round(2))
                else:
                    display_forecast = forecast[['ds', 'forecast']].copy()
                    display_forecast['forecast'] = display_forecast['forecast'].round(2)
                    display_forecast.columns = ['Data', 'Preço Previsto (R$)']
                    st.dataframe(display_forecast)
            else:
                st.error("❌ Não foi possível gerar previsões. Verifique os dados históricos.")
        
        with tab3:
            st.markdown('<div class="section-header">📊 Análise Técnica Avançada</div>', unsafe_allow_html=True)
            
            # Technical analysis chart
            tech_chart = create_candlestick_chart(df, crypto_name)
            st.plotly_chart(tech_chart, use_container_width=True)
            
            # Trading signals
            display_trading_signals(df, crypto_name)
        
        with tab4:
            st.markdown('<div class="section-header">📋 Indicadores Técnicos</div>', unsafe_allow_html=True)
            
            # Calculate and display technical indicators
            df_with_indicators = calculate_technical_indicators(df)
            
            if len(df_with_indicators) > 0:
                latest_data = df_with_indicators.iloc[-1]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("📈 Médias Móveis")
                    if 'MA_7' in latest_data:
                        st.metric("MA 7 dias", format_currency(latest_data['MA_7']))
                        st.metric("MA 21 dias", format_currency(latest_data['MA_21']))
                        st.metric("MA 50 dias", format_currency(latest_data['MA_50']))
                
                with col2:
                    st.subheader("🎯 Osciladores")
                    if 'RSI' in latest_data:
                        rsi_value = latest_data['RSI']
                        rsi_status = "Sobrecompra" if rsi_value > 70 else "Sobrevenda" if rsi_value < 30 else "Neutro"
                        st.metric("RSI (14)", f"{rsi_value:.2f}", delta=rsi_status)
                
                with col3:
                    st.subheader("📊 Volatilidade")
                    if 'volatility' in latest_data:
                        st.metric("Volatilidade", f"{latest_data['volatility']:.2f}")
                    if 'returns' in latest_data:
                        st.metric("Retorno Diário", f"{latest_data['returns']*100:.2f}%")
        
        with tab5:
            st.markdown('<div class="section-header">📊 Comparação de Criptomoedas</div>', unsafe_allow_html=True)
            
            # Multi-select for comparison
            comparison_cryptos = st.multiselect(
                "Selecione criptomoedas para comparar:",
                options=list(crypto_list.keys()),
                default=[crypto_display],
                format_func=lambda x: crypto_list[x]
            )
            
            if len(comparison_cryptos) > 1:
                comparison_df = get_price_comparison(comparison_cryptos)
                
                if not comparison_df.empty:
                    st.dataframe(comparison_df, use_container_width=True)
                    
                    # Comparison charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = px.bar(comparison_df, x='cryptocurrency', y='price', 
                                   title='Comparação de Preços')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(comparison_df, x='cryptocurrency', y='change_24h', 
                                   title='Variação 24h (%)')
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecione pelo menos 2 criptomoedas para comparar.")
    
    else:
        st.error("❌ Erro ao carregar dados. Verifique sua conexão com a internet.")
    
    # Footer with random quote
    st.divider()
    
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
        <div class='dance' style='text-align: center; font-family: "Hack", Courier, monospace; 
             font-size: 18px; color: #f39c12; margin: 2rem 0;'>
            💫 {random_quote} 💫
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()