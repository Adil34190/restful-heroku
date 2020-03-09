import mysql.connector
from mysql.connector import Error

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