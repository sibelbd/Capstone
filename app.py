from flask import Flask
from flask import render_template
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)

#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


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

if __name__ == '__main__':
    app.run()
