# Sensor for SdID '3'

from gpiozero import DistanceSensor as distsense
from time import sleep
import mysql.connector #install mysql package on raspberry pi

if __name__ =="__main__":
    sensor = distsense(trigger = 18, echo = 24)
    dis_vec = [False]*6 

#MySQL initialization

    mydb = mysql.connector.connect(
    host="INSERT_AWS_ENDPOINT",
    user="admin",
    passwd="admin123",
    database="parkwaydatabase"
    )
    mycursor = mydb.cursor()

#Continuous Loop for input

    while True:
        sleep(2)
        distance = round((sensor.distance*100),2)
        #print ("Distance: {}cm ".format(distance), end = ' ') #check why this is printing together
        
        # check = sum(dis_vec)
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