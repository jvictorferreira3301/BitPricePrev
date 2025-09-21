import random
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

### Enhanced utilities for BitPricePrev

def get_not_so_random_quote():
    """Get a random inspirational/fun quote for the app."""
    quotes = [
        # Crypto & Finance
        "Don't trust, verify! ₿",
        "HODL when others FODL! 💎🙌",
        "To the moon! 🚀🌙",
        "Buy the dip! 📉➡️📈",
        "All / 21m ₿",
        "Not your keys, not your coins! 🔑",
        "Diamond hands beats paper hands! 💎>📄",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Bulls make money, bears make money, but pigs get slaughtered! 🐂🐻🐷",
        
        # Technology & Innovation
        "Innovation distinguishes between a leader and a follower.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "Technology is a tool. In terms of getting the kids working together and motivating them, the teacher is the most important.",
        "Any sufficiently advanced technology is indistinguishable from magic.",
        "The internet is becoming the town square for the global village of tomorrow.",
        
        # Inspirational
        "Freedom is the right to tell people what they do not want to hear.",
        "The more corrupt the state, the more numerous the laws.",
        "Liberty means responsibility. That is why most men dread it.",
        'Who is John Galt? 🤔',
        'Liberdade é pouco. O que desejo ainda não tem nome.',
        'Os alquimistas já estão no corredor... ⚗️',
        'Wake up, Neo... 💊',
        "Carpe diem. Seize the day! ⏰",
        
        # Pop Culture
        "May the Force be with you. ⭐",
        "I am your father. 🦹‍♂️",
        "To infinity and beyond! 🚀",
        "Houston, we have a problem. 🚀",
        "Just keep swimming. 🐠",
        "There's no place like home. 🏠",
        "E.T. phone home. 👽📞",
        "I'll be back. 🤖",
        
        # Minecraft Style (keeping the original spirit)
        "Minecraft vibes! ⛏️",
        "You are awesome! ⭐",
        "Have fun exploring! 🗺️",
        "Keep calm and mine on! ⛏️",
        "Adventure awaits! 🗺️",
        "Build something amazing! 🏗️",
        "Craft your dreams! ✨",
        "Don't give up! 💪",
        "You can do it! 🎯",
        "Stay curious! 🔍",
        "Game on! 🎮",
        "Welcome back! 👋",
        "The adventure continues! ⚔️",
        
        # Numbers & Mystery
        ">: 4 8 15 16 23 42 🔢",
        "42 is the answer! 🤖",
        "01110100 01101000 01100101 ⚡",
        
        # Fun & Motivational
        "You are not alone. 🤗",
        "Be creative! 🎨",
        "Stay safe! 🛡️",
        "Have a great time! 🎉",
        "Enjoy the journey! 🛤️",
        "See you in the stars! ⭐",
        "Code is poetry. 📝✨",
        "Debug your way to success! 🐛➡️✅",
        "Error 404: Fear not found! 😄",
        "Compiling happiness... ⚙️😊",
        "Machine learning is the new electricity! ⚡🤖"
    ]
    return random.choice(quotes)

def format_number(value, format_type='currency', currency='BRL'):
    """Format numbers for better display."""
    if pd.isna(value) or value is None:
        return 'N/A'
    
    try:
        if format_type == 'currency':
            if currency == 'BRL':
                if abs(value) >= 1e12:
                    return f"R$ {value/1e12:.2f}T"
                elif abs(value) >= 1e9:
                    return f"R$ {value/1e9:.2f}B"
                elif abs(value) >= 1e6:
                    return f"R$ {value/1e6:.2f}M"
                elif abs(value) >= 1e3:
                    return f"R$ {value/1e3:.2f}K"
                else:
                    return f"R$ {value:.2f}"
            else:
                return f"${value:,.2f}"
        
        elif format_type == 'percentage':
            return f"{value:.2f}%"
        
        elif format_type == 'number':
            if abs(value) >= 1e9:
                return f"{value/1e9:.2f}B"
            elif abs(value) >= 1e6:
                return f"{value/1e6:.2f}M"
            elif abs(value) >= 1e3:
                return f"{value/1e3:.2f}K"
            else:
                return f"{value:.2f}"
        
        else:
            return str(value)
    except:
        return str(value)

def calculate_performance_metrics(actual, predicted):
    """Calculate various performance metrics for model evaluation."""
    if len(actual) != len(predicted) or len(actual) == 0:
        return {}
    
    try:
        actual = np.array(actual)
        predicted = np.array(predicted)
        
        # Remove any NaN or infinite values
        mask = np.isfinite(actual) & np.isfinite(predicted)
        actual = actual[mask]
        predicted = predicted[mask]
        
        if len(actual) == 0:
            return {}
        
        # Calculate metrics
        mae = np.mean(np.abs(actual - predicted))
        mse = np.mean((actual - predicted) ** 2)
        rmse = np.sqrt(mse)
        
        # MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100 if np.all(actual != 0) else np.inf
        
        # R-squared
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Directional accuracy
        actual_direction = np.diff(actual) > 0
        predicted_direction = np.diff(predicted) > 0
        directional_accuracy = np.mean(actual_direction == predicted_direction) * 100 if len(actual_direction) > 0 else 0
        
        return {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'MAPE': mape,
            'R²': r2,
            'Directional_Accuracy': directional_accuracy
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
        return {}

def get_risk_level(volatility):
    """Determine risk level based on volatility."""
    if volatility < 0.02:  # Less than 2%
        return "🟢 Baixo", "green"
    elif volatility < 0.05:  # 2-5%
        return "🟡 Moderado", "orange"
    elif volatility < 0.10:  # 5-10%
        return "🟠 Alto", "red"
    else:  # More than 10%
        return "🔴 Muito Alto", "darkred"

def generate_trading_recommendation(signals):
    """Generate overall trading recommendation based on multiple signals."""
    if not signals:
        return "⚪ Neutro", "Não há sinais claros no momento."
    
    buy_signals = sum(1 for signal, _, color in signals if color == "green")
    sell_signals = sum(1 for signal, _, color in signals if color == "red")
    neutral_signals = len(signals) - buy_signals - sell_signals
    
    if buy_signals > sell_signals and buy_signals > neutral_signals:
        return "🟢 COMPRA", f"Sinais de compra: {buy_signals} | Sinais de venda: {sell_signals}"
    elif sell_signals > buy_signals and sell_signals > neutral_signals:
        return "🔴 VENDA", f"Sinais de venda: {sell_signals} | Sinais de compra: {buy_signals}"
    else:
        return "🟡 AGUARDAR", f"Sinais mistos. Compra: {buy_signals} | Venda: {sell_signals} | Neutro: {neutral_signals}"

def create_alert_system(current_price, target_price, alert_type="above"):
    """Create a simple alert system for price targets."""
    if alert_type == "above" and current_price >= target_price:
        return f"🚨 ALERTA: Preço atingiu R$ {format_number(target_price, 'currency')}!"
    elif alert_type == "below" and current_price <= target_price:
        return f"🚨 ALERTA: Preço caiu para R$ {format_number(target_price, 'currency')}!"
    return None

def get_market_sentiment(price_change_24h):
    """Determine market sentiment based on 24h price change."""
    if price_change_24h > 5:
        return "🚀 Muito Otimista", "green"
    elif price_change_24h > 2:
        return "📈 Otimista", "lightgreen"
    elif price_change_24h > -2:
        return "⚖️ Neutro", "gray"
    elif price_change_24h > -5:
        return "📉 Pessimista", "orange"
    else:
        return "💥 Muito Pessimista", "red"

def calculate_fibonacci_levels(high, low):
    """Calculate Fibonacci retracement levels."""
    diff = high - low
    levels = {
        '0%': high,
        '23.6%': high - 0.236 * diff,
        '38.2%': high - 0.382 * diff,
        '50%': high - 0.5 * diff,
        '61.8%': high - 0.618 * diff,
        '78.6%': high - 0.786 * diff,
        '100%': low
    }
    return levels

def get_crypto_emoji(crypto_id):
    """Get emoji for cryptocurrency."""
    crypto_emojis = {
        'bitcoin': '₿',
        'ethereum': 'Ξ',
        'dogecoin': '🐕',
        'binancecoin': '🟡',
        'cardano': '🔷',
        'solana': '☀️',
        'xrp': '💧',
        'polkadot': '🔴',
        'chainlink': '🔗',
        'litecoin': 'Ł',
        'avalanche-2': '🏔️',
        'polygon': '🟣',
        'cosmos': '⚛️',
        'near': '🔵',
        'algorand': '🟢',
        'fantom': '👻',
        'tron': '🚀',
        'stellar': '⭐',
        'monero': '🔒',
        'vechain': '✅'
    }
    return crypto_emojis.get(crypto_id, '🪙')

def validate_data(df):
    """Validate data quality and return issues found."""
    issues = []
    
    if df is None or df.empty:
        issues.append("DataFrame está vazio ou None")
        return issues
    
    required_columns = ['timestamp', 'price']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        issues.append(f"Colunas obrigatórias ausentes: {missing_columns}")
    
    if 'price' in df.columns:
        if df['price'].isnull().any():
            null_count = df['price'].isnull().sum()
            issues.append(f"Valores nulos na coluna 'price': {null_count}")
        
        if (df['price'] <= 0).any():
            negative_count = (df['price'] <= 0).sum()
            issues.append(f"Valores não positivos na coluna 'price': {negative_count}")
    
    if 'timestamp' in df.columns:
        if df['timestamp'].isnull().any():
            null_count = df['timestamp'].isnull().sum()
            issues.append(f"Valores nulos na coluna 'timestamp': {null_count}")
    
    return issues

def create_download_link(df, filename="crypto_data.csv"):
    """Create a download link for DataFrame as CSV."""
    csv = df.to_csv(index=False)
    return csv
