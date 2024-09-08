from prophet import Prophet

def predict_future_prices(df, periods=30):
    """
    Predict future prices using Prophet model.
    """
    # Prepare data for Prophet (it needs 'ds' and 'y' columns)
  df_prophet = df.rename(columns={'timestamp': 'ds', 'price': 'y'})
    
    # Initialize and train the model
    model = Prophet()
    model.fit(df_prophet)

    # Create a dataframe to hold future dates for prediction
    future = model.make_future_dataframe(periods=periods)
    
    # Make predictions
    forecast = model.predict(future)
    
    return forecast