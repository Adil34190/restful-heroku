"""
API REST POUR LE MSPR
Auteurs: EL HAJJAJI Adil, ALASTUEY Arthur, HABANS Paul, DELAITRE Romain
Les routes importantes:

GET:
-/coupons/<int:coupon_id>
-/users/<string:pseudo>+<string:password>

POST
-/users/<string:email>+<string:pseudo>+<string:password>
"""

import os
from flask import Flask, render_template, jsonify, abort #Package permettant de créer un serveur local d'application
import mysql.connector #Package permettant de se connecter à une base de donnée mysql
from mysql.connector import Error
import pdb

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

#Variables ou seront stockés les objets JSON
les_tables = dict()
coupons = list()

conn = 0


###
# Routes de l'API
###
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/users')
def users():
    #Affichage de tous les utilisateurs enregistrés en base
    p_tables, p_users = getUsers()
    return p_tables

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/coupons/')
def tables():
     #Affichage de tous les coupons enregistrés en base   
    p_tables, p_coupons = getCoupons()
    return p_tables

@app.route('/coupons/<int:coupon_id>' , methods=['GET'])
def get_coupon(coupon_id):
    #Récupération des coupons en base
    p_tables, p_coupons = getCoupons()
    #Filtrage des coupons en fonction de l'id saisi dans l'url
    coupon = [coupon for coupon in p_coupons if coupon['id'] == coupon_id]
    if len(coupon) == 0:
        #Si aucun coupon n'est trouvé
        abort(404)
    return jsonify({'coupon': coupon[0]})

@app.route('/users/<string:pseudo>+<string:password>' , methods=['GET'])
def get_user(pseudo,password):
    #Récupération des utilisateurs en base
    p_tables, p_coupons = getUsers()
    #Filtrage des utilisteurs en fonction du pseudo et mot de passe saisi dans l'url
    coupon = [coupon for coupon in p_coupons if coupon['pseudo'] == pseudo and coupon['password'] == password]
    if len(coupon) == 0:
        #Si aucun utilisateur n'est trouvé
        abort(404)
    return jsonify({'utilisateur': coupon[0]})

@app.route('/users/<string:email>+<string:pseudo>+<string:password>' , methods=['POST'])
def post_user(email,pseudo,password):
    #Ajout d'un utilisteur dans la base de donnée
    result = PostUsers(email,pseudo,password)
    if result == 0:
        #result = 0, donc l'email saisi dans l'url éxiste déja en base
        abort(403)
    #Affichage des utilisateurs après ajout
    p_tables, p_users = getUsers()
    return p_tables


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

"""Les erreurs retournés:
404 : Aucun Utilisateur/Coupon correspondant aux conditions n'a été trouvé
403 : L'email saisi dans la réquète POST éxiste déja en base : l'utilisateur n'est donc pas crée
"""

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(error):
    """Mail already exists"""
    return "this mail already exists", 403

def getCoupons():    
    
    #Connexion à la base de donnée mysql
    name = 'MSPR_TP'
    conn = mysql.connector.connect(host='mysql.montpellier.epsi.fr', database=name, user='adil.elhajjaji', password='518TPB', port = '5206' )

    #Si la connexion est établie
    if conn.is_connected():
        l_les_tables = dict()
        l_coupons = list()
        print("connécté")
        cursor = conn.cursor(dictionary=True)
        #Récupération sous forme de JSON des données en base selon la requête
        cursor.execute("SELECT * FROM Coupons")
        for row in cursor:
            l_coupons.append(row)        
        l_les_tables["coupons"] = l_coupons
        return [l_les_tables, l_coupons]
        conn.close()

def getUsers():

    #Connexion à la base de donnée mysql
    name = 'MSPR_TP'
    conn = mysql.connector.connect(host='mysql.montpellier.epsi.fr', database=name, user='adil.elhajjaji', password='518TPB', port = '5206' )

    #Si la connexion est établie
    if conn.is_connected():
        l_les_tables = dict()
        l_users = list()
        print("connécté")
        cursor = conn.cursor(dictionary=True)

        #Récupération sous forme de JSON des données en base selon la requête
        cursor.execute("SELECT * FROM Utilisateurs")
        for row in cursor:
            l_users.append(row)
        l_les_tables["utilisateurs"] = l_users
        return [l_les_tables, l_users]
        conn.close()

def PostUsers(email, pseudo, password):

    #Connexion à la base de donnée mysql
    name = 'MSPR_TP'
    conn = mysql.connector.connect(host='mysql.montpellier.epsi.fr', database=name, user='adil.elhajjaji', password='518TPB', port = '5206' )

    #Si la connexion est établie
    if conn.is_connected():
        l_les_tables = dict()
        l_coupons = list()
        print("connécté")
        cursor = conn.cursor(dictionary=True)

        #Récupération des utilisateurs ayant comme email celui saisi dans l'url
        query = "SELECT email from `Utilisateurs` WHERE email = '" + email +"'"
        cursor.execute(query)
        rows = cursor.fetchall()

        #Si aucun utilisateur n'est trouvé
        if not rows:
            #Création d'un utilisateur avec les données saisis dans l'url
            query = "INSERT INTO `Utilisateurs` (pseudo, email, password) VALUES ('" + pseudo + "','" + email + "','" + password + "')"
            cursor.execute(query)
            conn.commit()
            print(cursor.rowcount, "Record inserted successfully into Utilisateurs table")
            cursor.close()
            return 1
        else:
            #Si un utilisateur est trouvé
            print("this email already exists")
            return 0
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
