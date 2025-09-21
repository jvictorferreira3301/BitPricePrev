# Configurações da aplicação BitPricePrev

# API Configuration
API_BASE_URL = "https://api.coingecko.com/api/v3"
REQUEST_TIMEOUT = 10
CACHE_TTL = 300  # 5 minutes

# Model Configuration
LSTM_EPOCHS = 50
LSTM_BATCH_SIZE = 32
LOOKBACK_WINDOW = 60
TRAIN_TEST_SPLIT = 0.8

# Technical Analysis Configuration
RSI_PERIOD = 14
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
STOCHASTIC_K = 14
STOCHASTIC_D = 3

# UI Configuration
DEFAULT_FORECAST_DAYS = 30
MAX_FORECAST_DAYS = 90
DEFAULT_HISTORICAL_DAYS = 365

# Color scheme for charts
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8'
}

# Supported cryptocurrencies (ID: Display Name)
SUPPORTED_CRYPTOS = {
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
