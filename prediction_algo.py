from datetime import datetime
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import region_filterer
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
from sklearn.metrics import mean_squared_error


def get_prediction(region, date):
    model_fit = create_predictive_model(region)

    # forecast
    if date != "":
        # forecast data for future date
        # get last date in dataset
        last_date_in_data = pd.read_csv('./templates/avocado.csv', parse_dates=['Date'])['Date'].max()

        # subtract last date of dataset from future week
        future_week = datetime.strptime(date, '%Y-%m-%d')
        num_of_steps_to_future = (future_week - last_date_in_data).days // 7

        # increment forecast by weeks many steps to return the future prediction
        # steps is the number of weeks into the future that must be predicted
        forecast = model_fit.forecast(steps=num_of_steps_to_future)[0]
        array_length = len(forecast)
        # return last step
        return int(round(forecast[array_length - 1]))
    else:
        # forecast data for today
        # get last date in dataset
        last_date_in_data = pd.read_csv('./templates/avocado.csv', parse_dates=['Date'])['Date'].max()

        # subtract last date of dataset from future week
        future_week = datetime.today()
        num_of_steps_to_future = (future_week - last_date_in_data).days // 7

        # increment forecast by weeks many steps to return the future prediction
        # steps is the number of weeks into the future that must be predicted
        forecast = model_fit.forecast(steps=num_of_steps_to_future)[0]
        array_length = len(forecast)
        # return last step
        return int(round(forecast[array_length - 1]))


def create_predictive_model(region):
    series = get_series(region)
    # uncomment these when modifying ML algo to view graphs (1/3)
    # test_stationarity(series)
    # smoothing_data(series)
    # moving_avg_data(series)
    # series_diff = difference_data(series)
    # decompose_data(series)
    # plot_acf_pacf(series_diff)
    model_fit = train_model(series)

    return model_fit


def get_series(region):
    # load dataset
    series = pd.read_csv('./templates/avocado.csv', parse_dates=['Date'])
    # filter all prices from atlanta for all time and set date as the index to turn data into a time series
    series = region_filterer.filter_region_all_time_df(series, region, "Total Volume").set_index('Date')

    # uncomment these when modifying ML algo to view graphs (2/3)
    # print(series.head())
    # print(series.dtypes)
    # plt.plot(series)
    # plt.show()

    return series


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


def smoothing_data(series):
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


def moving_avg_data(series):
    # exponentially weighted moving average
    expweighted_avg = series.ewm(halflife=12, ignore_na=False, min_periods=0, adjust=True).mean()
    plt.plot(series)
    plt.plot(expweighted_avg, color='red')
    plt.show()

    series_ewma_diff = series - expweighted_avg
    test_stationarity(series_ewma_diff)


def difference_data(series):
    # Take first difference:
    series_diff = series - series.shift()
    plt.plot(series_diff)
    plt.show()
    series_diff.dropna(inplace=True)
    test_stationarity(series_diff)
    return series_diff


def decompose_data(series):
    decomposition = seasonal_decompose(series, period=30)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # Plot decomposition
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


def plot_acf_pacf(series_diff):
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


def train_model(series):
    X = series.values
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(1, 0, 1))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        # for modifying ML
        # print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
    # for modifying ML
    # print('Test MSE: %.3f' % error)

    # uncomment these when modifying ML algo to view graphs (3/3)
    # # plot
    # plt.plot(test)
    # plt.plot(predictions, color='red')
    # plt.show()

    return model_fit
