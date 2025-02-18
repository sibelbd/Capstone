import json

from flask import Flask, jsonify, render_template, request
from flask_fontawesome import FontAwesome
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import region_filterer
import prediction_algo

app = Flask(__name__)
fa = FontAwesome(app)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='Home')


@app.route('/volume.html')
def price():
    return render_template('volume.html', title='Home')


@app.route('/regions.html')
def regions():
    return render_template('regions.html', title='Home')


@app.route('/_get_all_regions')
def get_all_regions():
    # find all unique regions in dataset
    data = pd.read_csv('./templates/avocado.csv')
    regions = data.region.unique()

    # remove invalid regions
    regions = [x for x in regions if
               x not in ['GreatLakes', 'Midsouth', 'Northeast', 'NorthernNewEngland', 'Plains', 'SouthCentral',
                         'Southeast', 'West', 'TotalUS', 'California']]
    return jsonify(regions)


@app.route('/predict_volume', methods=['GET', 'POST'])
def predict_volume():
    if request.method == "POST":
        prediction_data = request.get_json(force=True)['html_data']
        region = prediction_data[0]
        date = prediction_data[1]

    return str(prediction_algo.get_prediction(region, date))


@app.route('/fill_pie', methods=['GET', 'POST'])
def fill_pie():
    data = pd.read_csv('./templates/avocado.csv')
    regions = ['GreatLakes', 'Midsouth', 'Northeast', 'NorthernNewEngland', 'Plains', 'SouthCentral',
                         'Southeast', 'West', 'California']
    data_per_region = []
    for region in regions:
        region_data = data.loc[(data['region'] == region) & (data['Date'] == data['Date'].max()) & (data['type'] == 'conventional')]
        region_volume = region_data['Total Volume'].to_string(index=False)
        data_per_region.append(region_volume)

    return jsonify(data_per_region)


@app.route('/region_graph_filters', methods=['GET', 'POST'])
def return_filtered_dataset():
    if request.method == "POST":
        filters_list = request.get_json(force=True)['html_data']
        print(filters_list)

        region1 = filters_list[0]
        region2 = filters_list[1]
        region3 = filters_list[2]
        timeperiod = filters_list[3]
        startdate = filters_list[4]
        type_of_info = filters_list[5][:-1]
        enddate = None

    # list of filtered datasets to send back
    datasets = []

    # Convert time period to number of days and startdate to the correct format (YYYY-MM-DD) to (MM-DD-YYYY)
    startdate = datetime.strptime(startdate, '%Y-%m-%d')
    print(startdate)

    if timeperiod == "Three Months ":
        enddate = startdate + relativedelta(months=+3)
        print(enddate)
    elif timeperiod == "One Year ":
        enddate = startdate + relativedelta(years=+1)
    elif timeperiod == "All Time ":
        # if of all time avoid filtering data for time
        enddate = None

    # pull data into pandas dataframe
    data = pd.read_csv('./templates/avocado.csv', parse_dates=['Date'])

    # Check for type of data needed
    if type_of_info == "Price":
        # Check for if time period is all time or not
        if timeperiod != "All Time ":
            return time_period_graph_data(data, "AveragePrice", region1, region2, region3, startdate, enddate, datasets)
        else:
            return all_time_graph_data(data, "AveragePrice", region1, region2, region3, datasets)
    elif type_of_info == "Volume":
        # Check for if time period is all time or not
        if timeperiod != "All Time ":
            return time_period_graph_data(data, "Total Volume", region1, region2, region3, startdate, enddate, datasets)
        else:
            return all_time_graph_data(data, "Total Volume", region1, region2, region3, datasets)


def time_period_graph_data(data, type_of_info, region1, region2, region3, startdate, enddate, datasets):
    # region 1 filtering
    datasets.append(region_filterer.return_data_as_json(
        region_filterer.filter_region_timeperiod_df(data, region1, type_of_info, startdate, enddate)))

    # optional region 2 filtering
    if region2 != "None " and region2 != "Select a Region":
        datasets.append(region_filterer.return_data_as_json(
            region_filterer.filter_region_timeperiod_df(data, region2, type_of_info, startdate, enddate)))

    # optional region 3 filtering
    if region3 != "None " and region3 != "Select a Region":
        datasets.append(region_filterer.return_data_as_json(
            region_filterer.filter_region_timeperiod_df(data, region3, type_of_info, startdate, enddate)))

    # return jsonified array of dataset
    return jsonify(datasets)


def all_time_graph_data(data, type_of_info, region1, region2, region3, datasets):
    # region 1 filtering
    datasets.append(
        region_filterer.return_data_as_json(region_filterer.filter_region_all_time_df(data, region1, type_of_info)))

    # optional region 2 filtering
    if region2 != "None " and region2 != "Select a Region":
        datasets.append(
            region_filterer.return_data_as_json(region_filterer.filter_region_all_time_df(data, region2, type_of_info)))

    # optional region 3 filtering
    if region3 != "None " and region3 != "Select a Region":
        datasets.append(
            region_filterer.return_data_as_json(region_filterer.filter_region_all_time_df(data, region3, type_of_info)))

    return jsonify(datasets)


@app.route('/get_top_volume_results', methods=['GET', 'POST'])
def get_volume_results():
    data = pd.read_csv('./templates/avocado.csv', parse_dates=['Date'])
    excluded_regions = ['GreatLakes', 'Midsouth', 'Northeast', 'NorthernNewEngland', 'Plains', 'SouthCentral',
                         'Southeast', 'West', 'TotalUS', 'California']
    data = data.loc[data['Date'] == data['Date'].max()]
    data = data[~data.region.isin(excluded_regions)]

    top_volume = data.nlargest(5, 'Total Volume')[['region', 'Total Volume']]

    return top_volume.to_json(orient='records')


@app.route('/get_top_price_results', methods=['GET', 'POST'])
def get_price_results():
    data = pd.read_csv('./templates/avocado.csv', parse_dates=['Date'])
    data = data.loc[data['Date'] == data['Date'].max()]
    excluded_regions = ['GreatLakes', 'Midsouth', 'Northeast', 'NorthernNewEngland', 'Plains', 'SouthCentral',
                         'Southeast', 'West', 'TotalUS', 'California']
    data = data[~data.region.isin(excluded_regions)]
    top_price = data.nlargest(5, 'AveragePrice')[['region', 'AveragePrice']]

    return top_price.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
