# Sensor for SdID '3'

from gpiozero import DistanceSensor as distsense
from time import sleep
import mysql.connector #install mysql package on raspberry pi

if __name__ =="__main__":
    sensor = distsense(trigger = 18, echo = 24)
    dis_vec = [False]*6 


#____________________________________________________________________________________________ HIDE

#MySQL Initialization
	
	mydb = mysql.connector.connect(
    host="parkwaydb.cvwsvf6gxkqf.us-east-2.rds.amazonaws.com",
    user="admin",
    passwd="admin123",
    database="parkwaydatabase"
    )
    mycursor = mydb.cursor()
#_____________________________________________________________________________________________ HIDE


#Continuous Loop
    while True:
        sleep(3)
        distance = round((sensor.distance*100),2)
        print (distance)
        
        if sum(dis_vec)==5 and distance <90:
            print("Change status to occupied")
            mycursor.execute("INSERT INTO spot_description (spot_status) VALUES (1) where SdID = 3")
            print(dis_vec)
            mydb.commit()

        if sum(dis_vec)==1 and distance>=90:
            print("Change status to unoccupied")
            mycursor.execute("INSERT INTO spot_description (spot_status) VALUES (0) where SdID = 3")
            print(dis_vec)
            mydb.commit()

        if distance <90 :
            dis_vec.append(True)
        else:
            dis_vec.append(False)

        dis_vec.pop(0)

