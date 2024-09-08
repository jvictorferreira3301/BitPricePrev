from darts import TimeSeries
 from darts.models import ExponentialSmoothing
 
  def forecast_prices(df):
    series = TimeSeries.from_dataframe(df, 'timestamp', 'price')
     model = ExponentialSmoothing()
  model.fit(series)
  future = model.predict(60)
   return future
