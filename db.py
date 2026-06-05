import mysql.connector

def baglan():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Serdal_23-77",
        database="ucak_bileti_takip"
    )