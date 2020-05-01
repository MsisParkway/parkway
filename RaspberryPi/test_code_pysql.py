import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="admin123",
  database="test_newdb"
)
mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE new_table (id VARCHAR(100) PRIMARY KEY, mobile INT)")

mycursor.execute("INSERT INTO new_table (id, mobile) VALUES ('12',84735);")

mydb.commit()
