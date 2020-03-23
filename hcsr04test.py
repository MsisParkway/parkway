from gpiozero import DistanceSensor as distsense
from time import sleep


def occupied():
    print("Status: Occupied")
def unoccupied():
    print("Status: Unccupied")

if __name__ =="__main__":
    sensor = distsense(trigger = 18, echo = 24)
    status = 0

    while True:
        sleep(2)
        distance = round((sensor.distance*100),2)
        print ("Distance: {}cm ".format(distance), end = ' ')
        if(distance<60):
            occupied()
        else: unoccupied()
        
        

        
    
