import server_socket
import threading
import os
import time

class Steer(object):

    def __init__(self, client):
        self.client = client
        self.line = 'NONE'
        self.state = 'NONE'
        self.speed = '50'
        self.point = 'NO'
        self.pointlist = [0,0,0,0,0,0]
        self.x1 = [0,0]
        self.x2 = [0,0]
        

    def Set_Line(self, line) :
        self.line = line

    def Set_objPoint(self, pointlist):
        self.x1 = [pointlist[1],pointlist[2]+pointlist[4]]
        self.x2 = [pointlist[1]+pointlist[3],pointlist[2]+pointlist[4]]
        self.pointlist = pointlist

    def Control(self) :
        self.client.send('w'.encode()) #기본적으로 앞으로 가게 설정

        os.system('cls') #CMD 창 CLEAR
        #상태 출력
        print('상태 : ', self.state)
        print('장애물 : ', self.point)
        print('X1 : ', self.x1)
        print('X2 : ', self.x2)
        print('pointlist : ', self.pointlist )

#        if self.point == 'Yes':
#             self.client.send('o'.encode())
#             print('음성출력')
            
        self.point = 'No'
   
        if self.point == 'No':
            self.client.send('w'.encode())
            print('FOWARD')

        if 160 < self.x2[0]<=214:
            if self.x2[1]>=100:
                self.client.send('a'.encode())
                print('LEFT')	
                self.point = 'Yes'
                

                        
        elif 214<self.x2[0]<=320:
            if (45*self.x2[0])/53 +190 <=self.x2[1]:
                self.client.send('a'.encode())
                print('LEFT')
                self.point = 'Yes'
                        
        elif 0<=self.x1[0]<106:
            if (-45*self.x1[0])/53 +190 <= self.x1[1]:
                self.client.send('d'.encode())
                print('RIGHT')
                self.point = 'Yes'
                        

        elif 106<self.x1[0]<=160:
            if self.x1[1]>=100:
                self.client.send('d'.encode())
                print('RIGHT')
                self.point = 'Yes'
                        
        elif 'turn_right_yes' in self.obj_list :
            self.client.send('td'.encode())
            print("RIGHT")   
            self.point = 'No'
        elif self.line == 2:                
            self.client.send('w'.encode())
            self.point = 'No'
            print("FORWARD")
        elif self.line == 0:
            self.client.send('a'.encode())
            self.point = 'No'
            print("LEFT")
        elif self.line == 1:
            self.client.send('d'.encode())
            self.point = 'No'
            print("RIGHT")
            
        
        else :
            print("WAIT..")
            self.point = 'No'

        self.microphone = ''
