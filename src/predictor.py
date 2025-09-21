import pandas as pd
import numpy as np
import streamlit as st
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

def calculate_technical_indicators(df):
    """Calculate technical indicators for the cryptocurrency data."""
    df = df.copy()
    
    # Moving averages
    df['MA_7'] = df['price'].rolling(window=7).mean()
    df['MA_21'] = df['price'].rolling(window=21).mean()
    df['MA_50'] = df['price'].rolling(window=50).mean()
    
    # RSI (Relative Strength Index)
    delta = df['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_middle'] = df['price'].rolling(window=20).mean()
    bb_std = df['price'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
    df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
    
    # Price volatility (standard deviation)
    df['volatility'] = df['price'].rolling(window=10).std()
    
    # Daily returns
    df['returns'] = df['price'].pct_change()
    
    return df

def predict_lstm(df, periods=30, epochs=50):
    """Predict future prices using LSTM model with improved architecture."""
    try:
        # Prepare data
        df_work = df.copy()
        df_work = df_work.rename(columns={'timestamp': 'ds', 'price': 'y'})
        df_work['ds'] = pd.to_datetime(df_work['ds'])
        df_work = df_work.sort_values('ds').reset_index(drop=True)
        
        # Scale the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df_work['y'].values.reshape(-1, 1))
        
        # Create training data with look-back window of 60 days
        look_back = 60
        if len(scaled_data) < look_back + 10:  # Ensure we have enough data
            return pd.DataFrame(columns=['ds', 'forecast', 'model'])
            
        X, y = [], []
        for i in range(look_back, len(scaled_data)):
            X.append(scaled_data[i-look_back:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        # Split into train and validation sets
        train_size = int(len(X) * 0.8)
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]
        
        # Build improved LSTM model
        model = Sequential([
            LSTM(100, return_sequences=True, input_shape=(look_back, 1)),
            Dropout(0.2),
            LSTM(100, return_sequences=True),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        # Train model with validation
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_data=(X_val, y_val),
            verbose=0
        )
        
        # Make predictions for future periods
        last_sequence = scaled_data[-look_back:]
        predictions = []
        
        for _ in range(periods):
            # Reshape for prediction
            current_sequence = last_sequence.reshape((1, look_back, 1))
            next_pred = model.predict(current_sequence, verbose=0)[0, 0]
            predictions.append(next_pred)
            
            # Update sequence for next prediction
            last_sequence = np.append(last_sequence[1:], next_pred)
        
        # Inverse transform predictions
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = scaler.inverse_transform(predictions)
        
        # Create forecast DataFrame
        last_date = df_work['ds'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods)
        forecast_df = pd.DataFrame({
            'ds': future_dates,
            'forecast': predictions.flatten(),
            'model': 'LSTM'
        })
        
        # Calculate validation metrics
        val_predictions = model.predict(X_val, verbose=0)
        val_predictions = scaler.inverse_transform(val_predictions.reshape(-1, 1))
        val_actual = scaler.inverse_transform(y_val.reshape(-1, 1))
        
        mae = mean_absolute_error(val_actual, val_predictions)
        rmse = np.sqrt(mean_squared_error(val_actual, val_predictions))
        r2 = r2_score(val_actual, val_predictions)
        
        return forecast_df, {'MAE': mae, 'RMSE': rmse, 'R²': r2, 'history': history}
    
    except Exception as e:
        st.error(f"Erro no modelo LSTM: {e}")
        return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}

def predict_linear_regression(df, periods=30):
    """Predict future prices using Linear Regression."""
    try:
        df_work = df.copy()
        df_work = calculate_technical_indicators(df_work)
        df_work = df_work.dropna()
        
        if len(df_work) < 50:
            return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}
        
        # Create features
        features = ['MA_7', 'MA_21', 'MA_50', 'RSI', 'volatility', 'returns']
        X = df_work[features].values
        y = df_work['price'].values
        
        # Split data
        train_size = int(len(X) * 0.8)
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]
        
        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Validation metrics
        val_predictions = model.predict(X_val)
        mae = mean_absolute_error(y_val, val_predictions)
        rmse = np.sqrt(mean_squared_error(y_val, val_predictions))
        r2 = r2_score(y_val, val_predictions)
        
        # Generate future predictions (simplified approach)
        last_features = X[-1].reshape(1, -1)
        predictions = []
        
        for _ in range(periods):
            pred = model.predict(last_features)[0]
            predictions.append(pred)
            # Use last prediction to estimate next features (simplified)
            last_features[0, 0] = pred  # Update moving average feature
        
        # Create forecast DataFrame
        last_date = df_work['timestamp'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods)
        forecast_df = pd.DataFrame({
            'ds': future_dates,
            'forecast': predictions,
            'model': 'Linear Regression'
        })
        
        return forecast_df, {'MAE': mae, 'RMSE': rmse, 'R²': r2}
    
    except Exception as e:
        st.error(f"Erro no modelo de Regressão Linear: {e}")
        return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}

def predict_random_forest(df, periods=30):
    """Predict future prices using Random Forest."""
    try:
        df_work = df.copy()
        df_work = calculate_technical_indicators(df_work)
        df_work = df_work.dropna()
        
        if len(df_work) < 50:
            return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}
        
        # Create features
        features = ['MA_7', 'MA_21', 'MA_50', 'RSI', 'volatility', 'returns']
        X = df_work[features].values
        y = df_work['price'].values
        
        # Split data
        train_size = int(len(X) * 0.8)
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Validation metrics
        val_predictions = model.predict(X_val)
        mae = mean_absolute_error(y_val, val_predictions)
        rmse = np.sqrt(mean_squared_error(y_val, val_predictions))
        r2 = r2_score(y_val, val_predictions)
        
        # Generate future predictions
        last_features = X[-1].reshape(1, -1)
        predictions = []
        
        for _ in range(periods):
            pred = model.predict(last_features)[0]
            predictions.append(pred)
            # Update features for next prediction
            last_features[0, 0] = pred
        
        # Create forecast DataFrame
        last_date = df_work['timestamp'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods)
        forecast_df = pd.DataFrame({
            'ds': future_dates,
            'forecast': predictions,
            'model': 'Random Forest'
        })
        
        return forecast_df, {'MAE': mae, 'RMSE': rmse, 'R²': r2}
    
    except Exception as e:
        st.error(f"Erro no modelo Random Forest: {e}")
        return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}

def predict_future_prices(df, periods=30, model_type='LSTM'):
    """
    Predict future prices using the specified model.
    
    Parameters:
    - df: DataFrame containing 'timestamp' and 'price' columns.
    - periods: Number of periods to forecast.
    - model_type: Type of model to use ('LSTM', 'Linear', 'RandomForest', 'All')
    
    Returns:
    - DataFrame with forecasted prices and metrics dictionary.
    """
    if model_type == 'LSTM':
        return predict_lstm(df, periods)
    elif model_type == 'Linear':
        return predict_linear_regression(df, periods)
    elif model_type == 'RandomForest':
        return predict_random_forest(df, periods)
    elif model_type == 'All':
        # Run all models and return combined results
        lstm_forecast, lstm_metrics = predict_lstm(df, periods, epochs=20)  # Reduced epochs for speed
        linear_forecast, linear_metrics = predict_linear_regression(df, periods)
        rf_forecast, rf_metrics = predict_random_forest(df, periods)
        
        # Combine forecasts
        all_forecasts = []
        if not lstm_forecast.empty:
            all_forecasts.append(lstm_forecast)
        if not linear_forecast.empty:
            all_forecasts.append(linear_forecast)
        if not rf_forecast.empty:
            all_forecasts.append(rf_forecast)
        
        if all_forecasts:
            combined_forecast = pd.concat(all_forecasts, ignore_index=True)
            all_metrics = {
                'LSTM': lstm_metrics,
                'Linear Regression': linear_metrics,
                'Random Forest': rf_metrics
            }
            return combined_forecast, all_metrics
        else:
            return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}
    else:
        st.error("Tipo de modelo inválido!")
        return pd.DataFrame(columns=['ds', 'forecast', 'model']), {}

