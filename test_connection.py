import mysql.connector
import os

host = os.environ.get("host", "0.0.0.0")
port = os.environ.get("port", "3305")
print("host: " + host + "port: " + port)
connection = mysql.connector.connect(
  host=host,
  port=port,
  user="fynd_acad",
  password="fynd123",
  database="fynd_acad"
)

if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)
    print("hello")