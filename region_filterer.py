def filter_region_all_time_df(data, region, type_of_info):
    region_filtered_data = data.loc[(data['region'] == region[:-1]) & (data['type'] == 'conventional')]

    # convert dates back to string
    region_filtered_data.loc[:, 'Date'] = region_filtered_data['Date'].dt.strftime('%Y-%m-%d')

    region_filtered_data = region_filtered_data[['Date', type_of_info]]
    region_filtered_data = region_filtered_data.sort_values(by='Date')
    return region_filtered_data


def filter_region_timeperiod_df(data, region, type_of_info, startdate, enddate):
    region_filtered_data = data.loc[
        (data['region'] == region[:-1]) & (data['Date'] > startdate.strftime('%Y-%m-%d')) & (
                data['Date'] < enddate.strftime('%Y-%m-%d')) & (data['type'] == 'conventional')]

    # convert dates back to string
    region_filtered_data.loc[:, 'Date'] = region_filtered_data['Date'].dt.strftime('%Y-%m-%d')

    region_filtered_data = region_filtered_data[['Date', type_of_info]]
    region_filtered_data = region_filtered_data.sort_values(by='Date')

    return region_filtered_data

def return_data_as_json(region_filtered_data):
    region_filtered_data.columns = ['x', 'y']
    return region_filtered_data.to_json(orient='records')
