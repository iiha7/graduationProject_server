from socket import *
from threading import *
import time
import random
#import Threshold_Values.py
import os
import cv2
import numpy as np
from joblib import load
import picamera



class ClientThread(Thread):
    def __init__(self, cSocket, cAddress):
        Thread.__init__(self)
        self.cSocket = cSocket
        self.cAddress = cAddress
        print("Connection successful from ", self.cAddress)

    
    def openCamera (self):
        print("camera opened")
        # Define the path to the trained model
        model_path = 'svm_fire_detection.joblib'

        # Define the labels for your classes
        classes = ['fire', 'non-fire']

        # Define the image size
        img_size = (64, 64)

        # Load the trained model
        model = load(model_path)

        # Initialize the camera
        camera = picamera.PiCamera()

        # Set camera resolution
        camera.resolution = (img_size[0], img_size[1])

        # Define the path to the directory to save captured images
        save_dir = 'newdirectory'

        # Create the save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Capture image from the camera
        image_name = f"image_{time.time()}.jpg"
        save_path = os.path.join(save_dir, image_name)
        camera.capture(save_path)
        camera.close()

        # Read and preprocess the captured image
        img = cv2.imread(save_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, img_size)
        img = img.reshape(1, -1) / 255.0  # flatten and normalize the image data

        # Make a prediction
        pred = model.predict(img)[0]
        label = classes[pred]
            
        
        
        if label == 'fire' :
            return 1
        else:
            return 0
            

     
        
    
    
    def isAbovethreshhold (self,tempList,humdList):
        
        index=0
        
        #preparing the values by removing new line char
        for i in humdList:
            humdList[index] = i.replace('\n','')
            index+=1
        
        
        index =0
        for i in tempList:
            if float(tempList[index]) >25 or float(humdList[index])>50:
                return True
            index+=1
        
        return False
        
        
    
    def run(self):
        clientMsg = ""

        images = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg", "image6.jpg", "image7.jpg",
                  "image8.jpg", "image9.jpg",
                  "image10.jpg", "image11.jpg", "image12.jpg", "image13.jpg", "image14.jpg", "image15.jpg",
                  "image16.jpg", "image17.jpg", "image18.jpg"]


        while "!DISCONNECT" not in clientMsg:
            #read the file begin
            file= open('putty.log', "r")
            records = file.readlines()
            file.close()
            records.reverse()
            first = 0
            second = 0
            third = 0
            arr = []
            for i in records:
                if i.split(";")[0] == '5.0' and first == 0:
                    first = 1
                    arr.append(i)
                elif i.split(";")[0] == '2.0' and second == 0:
                    second = 1
                    arr.append(i)
                elif i.split(";")[0] == '66.145' and third == 0:
                    third = 1
                    arr.append(i)
                elif first==1 and second == 1 and third == 1:
                    break
            
            sen1 = arr[0].split(";")
            sen2 = arr[1].split(";")
            sen3 = arr[2].split(";")
            #read the file end
            
            #prepare values to be sent ot Threshold
            tempList = [sen1[1],sen2[1],sen3[1]]
            humdList = [sen1[-1],sen2[-1],sen3[-1]]
            
            if self.isAbovethreshhold(tempList,humdList):
                fire_notification = self.openCamera()
            
            else:
                fire_notification = 0
            
            
            #pass values to Threshold API begin
            #Threshold_Values.isAboveThreshold() => uses internet
            #pass values to Threshold API end
            
            
            #check if we have to open cam begin
            
            #check if we have to open cam end
            
            
            # if image is fire then set fire Notification as 1 and send the image
            
            # else ,set it as 0 dont send the image 
            
            
    

            accuracy = str(random.randint(0, 99)) + "%"
            image_number = random.randint(0, 17)
            image_name = images[image_number]



            send_list = [[[accuracy,image_name,str(fire_notification)],sen1,sen2,sen3]]

            send_str = ''.join(str(item) for item in send_list)
            self.cSocket.send(send_str.encode())

            clientMsg = self.cSocket.recv(1024).decode()

            print(clientMsg)

            time.sleep(2) # The time will be arranged


        print("Disconnected from ", self.cAddress)
        self.cSocket.close()


if __name__ == "__main__":
    HOST = "169.254.252.160"
    PORT = 5000

    socket = socket(AF_INET, SOCK_STREAM)
    socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    socket.bind((HOST, PORT))
    while True:
        socket.listen()
        cSocket, cAddress = socket.accept()
        newClient = ClientThread(cSocket, cAddress)
        newClient.start()
