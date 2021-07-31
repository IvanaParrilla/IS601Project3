# from typing import List, Dict
from flask import Flask, render_template, request
import simplejson as json
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'housingPrices'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/table', methods=['GET'])
def table():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM zillow')
    result = cursor.fetchall()
    return render_template('table.html', houses=result)


# @app.route('/search', methods=['POST', 'GET'])
# def search():
#     cursor = mysql.get_db().cursor()
#     input_data = (request.form.get('square_feet'), request.form.get('min_price'), request.form.get('max_price'))
#     sql_query = """SELECT * FROM zillow WHERE living_space_sqft >= %s AND list_price >= %s AND list_price <= %s"""
#     cursor.execute(sql_query, input_data)
#     result = cursor.fetchall()
#     return render_template('search.html', houses=result)


@app.route('/api/v1/houses', methods=['GET'])
def api_zillow() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM zillow')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
