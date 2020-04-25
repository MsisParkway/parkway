from gpiozero import DistanceSensor as distsense
from time import sleep
import mysql.connector #install mysql package on raspberry pi

if __name__ =="__main__":
    sensor = distsense(trigger = 18, echo = 24)
    dis_vec = [False]*6 

#MySQL initialization

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin123",
    database="test_newdb"
    )
    mycursor = mydb.cursor()

#Continuous Loop for input

    while True:
        sleep(2)
        distance = round((sensor.distance*100),2)
        #print ("Distance: {}cm ".format(distance), end = ' ') #check why this is printing together
        
        check = sum(dis_vec)
        if sum(dis_vec)==5 and distance <100:
        	print("Change status to occupied") #run update into query
            #mycursor.execute("INSERT INTO new_table (id, mobile) VALUES ('12',84735);")
            #mydb.commit()

        if sum(dis_vec)==1 and distance>100:
        	print("Change status to unoccupied")
            #mycursor.execute("INSERT INTO new_table (id, mobile) VALUES ('12',84735);")
            #mydb.commit()

        if distance <100 :
            dis_vec.append(True)
        else:
            dis_vec.append(False)

        dis_vec.pop(0)        
        




        



        
        

        
    
