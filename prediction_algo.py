from datetime import datetime
from pmdarima import auto_arima
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import region_filterer
# Fit a SARIMAX(0, 1, 1)x(2, 1, 1, 12) on the training set
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
from sklearn.metrics import mean_squared_error

# load dataset
series = pd.read_csv('./templates/avocado_wrangled.csv', parse_dates=['Date'])
# filter dataframe
# sample region name
region = "Atlanta "
# filter all prices from atlanta for all time and set date as the index to turn data into a time series
series = region_filterer.filter_region_all_time_df(series, region, "AveragePrice").set_index('Date')

print(series.head())
print(series.dtypes)
plt.plot(series)
plt.show()

# # ETS Decomposition
# result = seasonal_decompose(series['AveragePrice'],
#                             model='multiplicative', period=7)
#
# # ETS plot
# result.plot()
#
# # Fit auto_arima function to AirPassengers dataset
# stepwise_fit = auto_arima(series['AveragePrice'], start_p=1, start_q=1,
#                           max_p=3, max_q=3, m=12,
#                           start_P=0, seasonal=True,
#                           d=None, D=1, trace=True,
#                           error_action='ignore',  # we don't want to know if an order does not work
#                           suppress_warnings=True,  # we don't want convergence warnings
#                           stepwise=True)  # set to stepwise
#
# # To print the summary
# stepwise_fit.summary()
#
# size = int(len(series.values) * 0.66)
#
# # Split data into train / test sets
# train = series.iloc[:size]
# test = series.iloc[size:]
#
# model = SARIMAX(train['AveragePrice'],
#                 order=(0, 0, 0),
#                 seasonal_order=(0, 1, 0, 12), freq="QS-OCT")
#
# result = model.fit()
# result.summary()
#
# start = len(train)
# end = len(train) + len(test) - 1
#
#
# predictions = result.predict(start, end,
#                              typ='levels').rename("Predictions")
#
# # plot predictions and actual values
# predictions.plot(legend=True)
# test['AveragePrice'].plot(legend=True)



def test_stationarity(timeseries):
    # Determing rolling statistics
    rolmean = timeseries.rolling(window=12, center=False).mean()
    rolstd = timeseries.rolling(window=12, center=False).std()

    # Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)


#
#
# test_stationarity(series)
# Smoothing with moving average
moving_avg = series.rolling(window=12, center=False).mean()
plt.plot(series)
plt.plot(moving_avg, color='red')
plt.show()

series_moving_avg_diff = series - moving_avg
print(series_moving_avg_diff.head(12))
series_moving_avg_diff.dropna(inplace=True)
print(series_moving_avg_diff.head())

test_stationarity(series_moving_avg_diff)

# exponentially weighted moving average
expweighted_avg = series.ewm(halflife=12, ignore_na=False, min_periods=0, adjust=True).mean()
plt.plot(series)
plt.plot(expweighted_avg, color='red')
plt.show()

series_ewma_diff = series - expweighted_avg
test_stationarity(series_ewma_diff)

# Take first difference:
series_diff = series - series.shift()
plt.plot(series_diff)
plt.show()

series_diff.dropna(inplace=True)
test_stationarity(series_diff)

decomposition = seasonal_decompose(series, period=30)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(series, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

series_decompose = residual
series_decompose.dropna(inplace=True)
print(series_decompose.describe())
test_stationarity(series_decompose)

plot_acf(series_diff, lags=20)
plot_pacf(series_diff, lags=20)

plt.show()

lag_acf = acf(series_diff, nlags=12)
lag_pacf = pacf(series_diff, nlags=12, method='ols')

# Plot ACF:
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(series_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(series_diff)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')

# Plot PACF:
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(series_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(series_diff)), linestyle='--', color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.show()

X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(2, 1, 0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()

# get last date of dataset

# get future date

# subtract last date of dataset from future week

# get date difference in weeks

# increment forecast by weeks many steps to return the future prediction

# steps is the number of weeks into the future that must be predicted
forecast = model_fit.forecast(steps=12)[0]
print(forecast)
