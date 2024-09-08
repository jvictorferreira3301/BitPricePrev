import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

def predict_future_prices(df, periods=30):
    """
    Predict future prices using LSTM model.
    
    Parameters:
    - df: DataFrame containing 'timestamp' and 'price' columns.
    - periods: Number of periods to forecast.
    
    Returns:
    - DataFrame with forecasted prices.
    """
    try:
        # Prepare data
        df = df.rename(columns={'timestamp': 'ds', 'price': 'y'})
        df['ds'] = pd.to_datetime(df['ds'])
        df = df.sort_values('ds')
        df.set_index('ds', inplace=True)
        
        # Scale the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df['y'].values.reshape(-1, 1))
        
        # Create training data
        train_data = []
        for i in range(60, len(scaled_data)):
            train_data.append(scaled_data[i-60:i, 0])
        
        train_data = np.array(train_data)
        x_train = train_data[:, :-1]
        y_train = train_data[:, -1]
        
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        
        # LSTM model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
        
        # Pprepare test data
        test_data = scaled_data[-60:]
        x_test = []
        for i in range(periods):
            x_test.append(test_data[i:i+60, 0])
            test_data = np.append(test_data, [[0]], axis=0)
        
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        
        # Make predictions
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        
        ## Create forecast DataFrame
        future_dates = pd.date_range(start=df.index.max(), periods=periods + 1)[1:]
        forecast_df = pd.DataFrame({'ds': future_dates, 'forecast': predictions.flatten()})
        
        return forecast_df
    
    except Exception as e:
        logger.error(f"Error in predicting future prices: {e}")
        return pd.DataFrame(columns=['ds', 'forecast'])

