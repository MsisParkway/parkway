from time import sleep
import mysql.connector #install mysql package on raspberry pi

if __name__ =="__main__":
#MySQL initialization

    mydb = mysql.connector.connect(
    host="parkwaydb.cvwsvf6gxkqf.us-east-2.rds.amazonaws.com",
    user="admin",
    passwd="admin123",
    database="parkwaydatabase"
    )
    mycursor = mydb.cursor()

#Continuous Loop for input

    while True:
        sleep(2)
        print("Testing...")
        mycursor.execute("SELECT SdID, Spot_Status FROM spot_description;")
        query_list = mycursor.fetchall() # returns nested list
        mydb.commit()

        
