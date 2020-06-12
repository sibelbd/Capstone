from flask import Flask, jsonify, render_template, request
from flask_fontawesome import FontAwesome
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='Home')


@app.route('/price.html')
def price():
    return render_template('price.html', title='Home')


@app.route('/regions.html')
def regions():
    return render_template('regions.html', title='Home')

@app.route('/_get_all_regions')
def get_all_regions():
    # find all unique regions in dataset
    data = pd.read_csv('./templates/avocado_wrangled.csv')
    regions = data.region.unique()

    # remove invalid regions
    regions = [x for x in regions if x not in ['GreatLakes', 'Midsouth', 'Northeast', 'NorthernNewEngland', 'Plains', 'SouthCentral', 'Southeast', 'West', 'TotalUS']]
    return jsonify(regions)


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
        type_of_info = filters_list[5]
        enddate = None

    # list of filtered datasets to send back
    datasets = []

    # Convert time period to number of days and startdate to the correct format (YYYY-MM-DD) to (MM-DD-YYYY)
    startdate = datetime.strptime(startdate, '%Y-%m-%d')
    print(startdate)

    if timeperiod == "One Month ":
        enddate = startdate + relativedelta(months=+6)
        print(enddate)
    elif timeperiod == "One Year ":
        enddate = startdate + relativedelta(years=+1)
    elif timeperiod == "All Time ":
        # if of all time avoid filtering data for time
        enddate = None

    # pull data into pandas dataframe
    data = pd.read_csv('./templates/avocado_wrangled.csv', parse_dates=['Date'])

    # Get dataset for region 1
    # Check for if time period is all time or not
    if timeperiod == "All Time ":
        # region 1 filtering
        region1_filtered_data = data.loc[(data['region'] == region1) & (data['Date'] > startdate.strftime("%m/%d/%Y")) & (data['Date'] < enddate.strftime("%m/%d/%Y"))]

        # optional region 2 filtering
        if region2 != "None " and region2 != "Select a Region":


        # optional region 3 filtering

        # return jsonified array of dataset

    else:

        # region 1 filtering

        # optional region 2 filtering

        # optional region 3 filtering

        # return jsonified array of datasets


    #
    # # filter dataframe
    # region1_filtered_data = data.loc[(data['region'] == region1) & (data['Date'] > startdate) & (data['Date'] < )]


if __name__ == '__main__':
    app.run()
