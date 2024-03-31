import serial 
import time 
import random
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1) 
def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    time.sleep(0.05) 
    data = arduino.readline() 
    return data


direction = 0

while True: 
    if arduino.in_waiting > 0: 
        myData = arduino.readline().decode('utf-8').strip()
        if myData == "/getCount":
            if direction == 0:
                url = "traffic_video.mp4"
                direction = 1
            elif direction == 1:
                url = "main_gate_maincar.mp4"
                direction = 2
            elif direction == 2:
                url = "traffic_video.mp4"
                direction = 3
            elif direction == 3:
                url = "main_gate_maincar.mp4"
                direction = 0
            cap = cv2.VideoCapture(url)
            ret, frame = cap.read()
            cap.release()
            
            results = model(frame)

            cnt = len(results[0].boxes)



            # cnt = random.randint(1, 3)
            print("Count is: ", cnt * 1.5)
            print("Sending to arduino")
            arduino.write(bytes(str(cnt)+"\n", 'utf-8'))
            time.sleep(0.05)
        else:
            if int(myData) < 10:
                myData = "0" + str(myData)
            print(myData,end='\r')
            time.sleep(0.05)
    

