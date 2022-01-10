import numpy as np
import cv2
import threading
import detect
from model import NeuralNetwork


class CollectTrainingData(object):

    def __init__(self, client, steer):        

        self.client = client        
        self.steer = steer
        # model create
        self.model = NeuralNetwork()
        self.model.load_model(path = 'model_data/video_model_5.h5')          

    def collect(self):

        print("Start video stream")        

        stream_bytes = b' '  
 
        while True :            
            stream_bytes += self.client.recv(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')

            if first != -1 and last != -1:
                try:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]

                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    #rgb = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    cv2.line(image,(0,190),(106,100),(255,0,0),1)
                    cv2.line(image,(320,190),(214,100),(255,0,0),1)
                    #rgb2 = rgb.copy()
                    #roi2 = rgb2[120:240, :] #for line roi
                    roi = image[120:240, :]                    


                    #화면 출력
                    cv2.waitKey(1)
                    #cv2.imshow('Origin', rgb)
                    #cv2.imshow('roi', roi)
                    #cv2.imshow('GRAY', image)
                    
                    #yolo 적용
                    cv2.imwrite('./testimg/two.jpg', image)
                    pointlist = detect.run(source = 'testimg') #pointlist = [분류 클래스 name, x, y, w, h, 정확도] 형태
                    cv2.waitKey(1)
                    
                    # reshape the roi image into a vector
                    image_array = np.reshape(roi, (-1, 120, 320, 1))    
                    
                    # neural network makes prediction
                    self.steer.Set_objPoint(pointlist)
                    self.steer.Set_Line(self.model.predict(image_array))                   
                    self.steer.Control()
                except:
                    continue

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break




























