import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def calculate_rsi(prices, window=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculate Bollinger Bands."""
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)."""
    exp1 = prices.ewm(span=fast).mean()
    exp2 = prices.ewm(span=slow).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_stochastic(high, low, close, k_window=14, d_window=3):
    """Calculate Stochastic Oscillator."""
    lowest_low = low.rolling(window=k_window).min()
    highest_high = high.rolling(window=k_window).max()
    k_percent = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d_percent = k_percent.rolling(window=d_window).mean()
    return k_percent, d_percent

def identify_support_resistance(df, window=20):
    """Identify potential support and resistance levels."""
    prices = df['price']
    
    # Find local minima (support) and maxima (resistance)
    support_levels = []
    resistance_levels = []
    
    for i in range(window, len(prices) - window):
        # Check for local minimum (support)
        if prices.iloc[i] == prices.iloc[i-window:i+window+1].min():
            support_levels.append((df.iloc[i]['timestamp'], prices.iloc[i]))
        
        # Check for local maximum (resistance)
        if prices.iloc[i] == prices.iloc[i-window:i+window+1].max():
            resistance_levels.append((df.iloc[i]['timestamp'], prices.iloc[i]))
    
    return support_levels, resistance_levels

def create_candlestick_chart(df, crypto_name):
    """Create a candlestick chart with technical indicators."""
    # Simulate OHLC data from price data (simplified)
    df = df.copy()
    df['open'] = df['price'].shift(1)
    df['high'] = df[['price', 'open']].max(axis=1)
    df['low'] = df[['price', 'open']].min(axis=1)
    df['close'] = df['price']
    
    # Calculate technical indicators
    df['rsi'] = calculate_rsi(df['close'])
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = calculate_bollinger_bands(df['close'])
    df['macd'], df['macd_signal'], df['macd_histogram'] = calculate_macd(df['close'])
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{crypto_name} - Preço e Bandas de Bollinger', 'RSI', 'MACD'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Preço'
        ),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['bb_upper'], 
                   line=dict(color='red', width=1), name='BB Superior'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['bb_middle'], 
                   line=dict(color='blue', width=1), name='BB Média'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['bb_lower'], 
                   line=dict(color='red', width=1), name='BB Inferior'),
        row=1, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['rsi'], 
                   line=dict(color='purple'), name='RSI'),
        row=2, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # MACD
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['macd'], 
                   line=dict(color='blue'), name='MACD'),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['macd_signal'], 
                   line=dict(color='red'), name='Signal'),
        row=3, col=1
    )
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['macd_histogram'], 
               name='Histogram'),
        row=3, col=1
    )
    
    fig.update_layout(
        title=f'Análise Técnica - {crypto_name}',
        xaxis_title='Data',
        height=800,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="Preço (R$)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    
    return fig

def get_trading_signals(df):
    """Generate basic trading signals based on technical indicators."""
    signals = []
    
    if len(df) < 50:
        return signals
    
    # Calculate indicators
    df['rsi'] = calculate_rsi(df['price'])
    df['ma_short'] = df['price'].rolling(window=10).mean()
    df['ma_long'] = df['price'].rolling(window=30).mean()
    
    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest
    
    # RSI signals
    if latest['rsi'] < 30:
        signals.append(("🟢 COMPRA", "RSI indica sobrevenda (RSI < 30)", "green"))
    elif latest['rsi'] > 70:
        signals.append(("🔴 VENDA", "RSI indica sobrecompra (RSI > 70)", "red"))
    
    # Moving Average signals
    if latest['ma_short'] > latest['ma_long'] and previous['ma_short'] <= previous['ma_long']:
        signals.append(("🟢 COMPRA", "Cruzamento dourado das médias móveis", "green"))
    elif latest['ma_short'] < latest['ma_long'] and previous['ma_short'] >= previous['ma_long']:
        signals.append(("🔴 VENDA", "Cruzamento da morte das médias móveis", "red"))
    
    # Price trend signals
    recent_prices = df['price'].tail(5)
    if recent_prices.is_monotonic_increasing:
        signals.append(("📈 ALTA", "Tendência de alta consistente", "blue"))
    elif recent_prices.is_monotonic_decreasing:
        signals.append(("📉 BAIXA", "Tendência de baixa consistente", "orange"))
    
    return signals

def create_volume_analysis(df):
    """Create volume analysis chart."""
    if 'volume' not in df.columns:
        return None
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Preço', 'Volume'),
        row_heights=[0.7, 0.3]
    )
    
    # Price chart
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['price'], 
                   line=dict(color='blue'), name='Preço'),
        row=1, col=1
    )
    
    # Volume chart
    colors = ['red' if df.iloc[i]['price'] < df.iloc[i-1]['price'] 
              else 'green' for i in range(1, len(df))]
    colors.insert(0, 'gray')  # First bar color
    
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['volume'], 
               marker_color=colors, name='Volume'),
        row=2, col=1
    )
    
    fig.update_layout(
        title='Análise de Volume',
        height=600,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="Preço (R$)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_xaxes(title_text="Data", row=2, col=1)
    
    return fig

def calculate_price_levels(df):
    """Calculate key price levels."""
    prices = df['price']
    
    current_price = prices.iloc[-1]
    high_52w = prices.tail(365).max() if len(prices) >= 365 else prices.max()
    low_52w = prices.tail(365).min() if len(prices) >= 365 else prices.min()
    
    # Support and resistance levels
    support_levels, resistance_levels = identify_support_resistance(df)
    
    levels = {
        'current_price': current_price,
        'high_52w': high_52w,
        'low_52w': low_52w,
        'support_levels': support_levels[-3:] if len(support_levels) >= 3 else support_levels,
        'resistance_levels': resistance_levels[-3:] if len(resistance_levels) >= 3 else resistance_levels,
    }
    
    return levels
