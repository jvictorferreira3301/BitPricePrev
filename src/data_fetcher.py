import requests
import pandas as pd
import streamlit as st
import time
from datetime import datetime, timedelta

# Lista expandida de criptomoedas disponíveis
AVAILABLE_CRYPTOS = {
    'bitcoin': 'Bitcoin (BTC)',
    'ethereum': 'Ethereum (ETH)',
    'dogecoin': 'Dogecoin (DOGE)',
    'binancecoin': 'Binance Coin (BNB)',
    'cardano': 'Cardano (ADA)',
    'solana': 'Solana (SOL)',
    'xrp': 'XRP (XRP)',
    'polkadot': 'Polkadot (DOT)',
    'chainlink': 'Chainlink (LINK)',
    'litecoin': 'Litecoin (LTC)',
    'avalanche-2': 'Avalanche (AVAX)',
    'polygon': 'Polygon (MATIC)',
    'cosmos': 'Cosmos (ATOM)',
    'near': 'NEAR Protocol (NEAR)',
    'algorand': 'Algorand (ALGO)',
    'fantom': 'Fantom (FTM)',
    'tron': 'TRON (TRX)',
    'stellar': 'Stellar (XLM)',
    'monero': 'Monero (XMR)',
    'vechain': 'VeChain (VET)'
}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_historical_data(crypto_id, days=365, vs_currency='brl'):
    """
    Fetch the historical price data of the cryptocurrency from the CoinGecko API.
    
    Parameters:
    - crypto_id: ID of the cryptocurrency
    - days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, max)
    - vs_currency: Currency to get prices in (default: brl)
    
    Returns:
    - DataFrame with timestamp and price columns
    """
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days,
        'interval': 'daily' if days > 90 else 'hourly' if days > 1 else 'hourly'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'prices' not in data:
            st.error("Dados de preços não encontrados na resposta da API")
            return None
            
        prices = data['prices']
        volumes = data.get('total_volumes', [])
        market_caps = data.get('market_caps', [])
        
        # Create DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Add volume and market cap if available
        if volumes:
            volume_df = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
            volume_df['timestamp'] = pd.to_datetime(volume_df['timestamp'], unit='ms')
            df = df.merge(volume_df, on='timestamp', how='left')
        
        if market_caps:
            mcap_df = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
            mcap_df['timestamp'] = pd.to_datetime(mcap_df['timestamp'], unit='ms')
            df = df.merge(mcap_df, on='timestamp', how='left')
        
        # Add price change and percentage change
        df['price_change'] = df['price'].diff()
        df['price_change_pct'] = df['price'].pct_change() * 100
        
        return df.sort_values('timestamp').reset_index(drop=True)
        
    except requests.exceptions.Timeout:
        st.error("Timeout ao conectar com a API. Tente novamente.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("Muitas requisições. Aguarde um momento e tente novamente.")
            time.sleep(1)
        else:
            st.error(f"Erro HTTP ao obter dados históricos: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao obter dados históricos: {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado ao processar dados históricos: {e}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_crypto_info(crypto_id):
    """
    Fetch detailed information of the cryptocurrency from the CoinGecko API.
    
    Parameters:
    - crypto_id: ID of the cryptocurrency
    
    Returns:
    - Dictionary with cryptocurrency information
    """
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    params = {
        'localization': 'false',
        'tickers': 'false',
        'community_data': 'true',
        'developer_data': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.Timeout:
        st.error("Timeout ao obter informações da criptomoeda.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("Muitas requisições. Aguarde um momento.")
            time.sleep(1)
        else:
            st.error(f"Erro HTTP ao obter informações da criptomoeda: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None

@st.cache_data(ttl=300)
def get_market_overview():
    """
    Fetch general cryptocurrency market overview.
    
    Returns:
    - Dictionary with market statistics
    """
    url = "https://api.coingecko.com/api/v3/global"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('data', {})
    except Exception as e:
        st.error(f"Erro ao obter visão geral do mercado: {e}")
        return {}

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_trending_cryptos():
    """
    Fetch trending cryptocurrencies.
    
    Returns:
    - List of trending crypto data
    """
    url = "https://api.coingecko.com/api/v3/search/trending"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('coins', [])
    except Exception as e:
        st.error(f"Erro ao obter criptomoedas em tendência: {e}")
        return []

@st.cache_data(ttl=300)
def get_price_comparison(crypto_ids, vs_currency='brl'):
    """
    Get current prices for multiple cryptocurrencies for comparison.
    
    Parameters:
    - crypto_ids: List of cryptocurrency IDs
    - vs_currency: Currency to compare against
    
    Returns:
    - DataFrame with comparison data
    """
    if not crypto_ids:
        return pd.DataFrame()
    
    ids_str = ','.join(crypto_ids)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ids_str,
        'vs_currencies': vs_currency,
        'include_24hr_change': 'true',
        'include_24hr_vol': 'true',
        'include_market_cap': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        comparison_data = []
        for crypto_id in crypto_ids:
            if crypto_id in data:
                crypto_data = data[crypto_id]
                comparison_data.append({
                    'cryptocurrency': AVAILABLE_CRYPTOS.get(crypto_id, crypto_id),
                    'price': crypto_data.get(vs_currency, 0),
                    'change_24h': crypto_data.get(f'{vs_currency}_24h_change', 0),
                    'volume_24h': crypto_data.get(f'{vs_currency}_24h_vol', 0),
                    'market_cap': crypto_data.get(f'{vs_currency}_market_cap', 0)
                })
        
        return pd.DataFrame(comparison_data)
    except Exception as e:
        st.error(f"Erro ao obter comparação de preços: {e}")
        return pd.DataFrame()

def format_currency(value, currency='BRL'):
    """Format currency values for display."""
    if pd.isna(value) or value == 0:
        return 'N/A'
    
    if currency == 'BRL':
        if value >= 1e9:
            return f"R$ {value/1e9:.2f}B"
        elif value >= 1e6:
            return f"R$ {value/1e6:.2f}M"
        elif value >= 1e3:
            return f"R$ {value/1e3:.2f}K"
        else:
            return f"R$ {value:.2f}"
    else:
        return f"{value:,.2f}"

def get_crypto_list():
    """Return the list of available cryptocurrencies."""
    return AVAILABLE_CRYPTOS
