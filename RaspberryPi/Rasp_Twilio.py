# Sensor for SdID '3'

from gpiozero import DistanceSensor as distsense
from time import sleep
import mysql.connector #install mysql package on raspberry pi
from twilio.rest import Client #install twilio through pip on Raspberry Pi


if __name__ =="__main__":
    sensor = distsense(trigger = 18, echo = 24)
    dis_vec = [False]*6 


#____________________________________________________________________________________________ HIDE
#Twilio Initialization

account_sid = 'AC366a7dce13a2f2f0f18fc6727ba88ace'
auth_token = 'bc8e109e23d25deb7e32dc6c2a2187e0'
client = Client(account_sid, auth_token)


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

        #check if car is still at the parking space
        data = []
        mycursor.execute("SELECT u.mobile" 
                        "FROM reservation r" 
                        "JOIN spot_description s on s.sdid=r.sdid"
                        "JOIN user u on u.userid = r.guserid "
                        "WHERE timediff(now(),r.reservationenddatetime) BETWEEN '07:05:00' AND '07:07:00' AND s.spot_status=1 AND sdid=3;")
        data.append(mycursor.fetchall())
        mydb.commit()

        if not data[0]:
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to='+14086462243',
            from_='+12058581270'
            )

        message = client.messages.create(
            body='IMPORTANT REMINDER!\nYour reservation time is Up. Please remove your car.',
            from_='+12058581270',
            to='+14086462243'
            )


