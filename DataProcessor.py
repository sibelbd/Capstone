import pandas as pd
import matplotlib.pyplot as plt

class DataProcessor:
    # Test Arena
        # Create dataframe
        df = pd.read_csv('templates/avocado_wrangled.csv', parse_dates=['Date'])

        df = df.loc[(df['region'] == 'West') & (df['type'] == 'organic')]


        print(df)

        df.plot(x="Date", y="AveragePrice", kind='scatter', color='green', rot=90)

        plt.show()


    # Descriptive Methods

    ### Average Avocado Price Nationally Throughout The Years

    ###

    # Predictive Methods