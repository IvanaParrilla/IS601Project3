# from typing import List, Dict
from flask import Flask, render_template, Response, request
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
# def search(zipcode):
#     cursor = mysql.get_db().cursor()
#     input_data = (request.form.get('square_feet'), request.form.get('min_price'), request.form.get('max_price'))
#     sql_query = """SELECT * FROM zillow WHERE zip = zipcode"""
#     cursor.execute(sql_query, input_data)
#     result = cursor.fetchall()
#     return render_template('search.html', houses=result)


@app.route('/api/v1/table', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM zillow')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/search/<zipcode>', methods=['GET'])
def api_retrieve(zipcode) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM zillow WHERE zip=%s', zipcode)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# @app.route('/api/v1/update/<zipcode>')
# def api_edit(zipcode) -> str:
#     cursor = mysql.get_db().cursor()
#     content = request.json
#     input_data = (content['living_space_sqft'], content['beds'], content['baths'], content['zip'], content['year'],
#                   content['list_price'], zipcode)
#     sql_update_query = """UPDATE zillow t SET t.living_space_sqft = %s, t.beds = %s, t.baths = %s, t.zip =
#             %s, t.year = %s, t.list_price = %s"""
#     cursor.execute(sql_update_query, input_data)
#     mysql.get_db().commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp


@app.route('/api/v1/zillow', methods=['PUT'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    input_data = (content['living_space_sqft'], content['beds'], content['baths'], content['zip'],
                  content['year'], content['list_price'])
    sql_insert_query = """INSERT INTO zillow (living_space_sqft,beds,baths,zip,year,list_price) 
                        VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
