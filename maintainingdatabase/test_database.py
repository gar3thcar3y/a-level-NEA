import mysql.connector


db = mysql.connector.connect(
    host = "localhost",
    user = "admin",
    passwd = "password1",
)

mycursor = db.cursor()

#mycursor.execute("CREATE DATABASE testdatabase")
