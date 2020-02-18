"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
les_tables = dict()
coupons = list()

name = 'MSPR_TP'
conn = mysql.connector.connect(host='mysql.montpellier.epsi.fr', database=name, user='adil.elhajjaji', password='518TPB', port = '5206' )

if conn.is_connected():

    print("connécté")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Coupons")

    for row in cursor:
        coupons.append(row)

    les_tables["coupons"] = coupons
    print(les_tables)

    #les_tables = jsonify({'tables' : les_tables})
    conn.close()

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html', bdd_name = name)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/tables/')
def tables():
    """Render the website's table page."""
    #return render_template('tables.html', table = les_tables)
    return les_tables

@app.route('/tables/coupons/<int:coupon_id>' , methods=['GET'])
def get_coupon(coupon_id):
    coupon = [coupon for coupon in coupons if coupon['id'] == coupon_id]
    if len(coupon) == 0:
        abort(404)
    return jsonify({'coupon': coupon[0]})


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
