# Create an inference to detect vehicles using YOLO model for given image


import cv2
import numpy as np
import base64
from ultralytics import YOLO 

# Load YOLO
model = YOLO('../models/detection.pt')

def detect_vehicles(image):
    # Perform object detection
    results = model(image)[0]

    # create a new image with bounding boxes and labels 
    output_img = image
    boxes = results.boxes 
    labels = results.names
    for box in boxes:
        x1,y1,x2,y2 = box.xyxy[0]
        x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)

        vehicle_img = output_img[y1:y2, x1:x2]
        
        if model.names[int(box.cls)] == 'vehicle':
            output_img = vehicle_img
            break
        else:
            output_img = image 
        
        

    # convert image to base64
    _, img_encoded = cv2.imencode('.png', output_img)  # encode image as png
    img_base64,label = base64.b64encode(img_encoded).decode('utf-8'),labels[int(boxes[0].cls)]
    return img_base64,label



