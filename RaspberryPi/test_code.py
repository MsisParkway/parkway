from gpiozero import DistanceSensor as distsense
from time import sleep


def status_change():
    print("Status changed")


if __name__ =="__main__":
    sensor = distsense(trigger = 18, echo = 24)
    dis_vec = [False, False, False, False, False, False]
    status = 0 #True means occupied 

    while True:
        sleep(2)
        distance = round((sensor.distance*100),2)
        print ("Distance: {}cm ".format(distance), end = ' ')
        

        if distance <95 :
            dist_vec.append(True)
        else:
            dist_vec.append(False)

#        dis_vec.append(distance)
        dis_vec.pop(0)
        '''if diff < 10 and distance<95:
            status = True
            status_change()'''
        check = sum(dis_vec)
        if (check == 6) or (check == 0):
            status_change()




        """if(distance<60):
            occupied()
        else: unoccupied()"""
        
        




        



        
        

        
    
