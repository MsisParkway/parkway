import mysql.connector as mysql

db = mysql.connect(
	host = "db4free.net",
	user = "parkway",
	passwd = "capstone"
	)
print(db)