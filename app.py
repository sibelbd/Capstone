from flask import Flask, jsonify, render_template
from flask_fontawesome import FontAwesome
import pandas as pd

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

if __name__ == '__main__':
    app.run()
