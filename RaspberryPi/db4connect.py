#Code not working
import pymysql.cursors

connection = pymysql.connect(host='db4free.net',
                             user='parkway',
                             password='capstone',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM parkway.new_table"
        #cursor.execute(sql, (2,'Bendre'))
        result = cursor.fetchone()
        print(result)

    connection.commit()
finally:
    connection.close()
