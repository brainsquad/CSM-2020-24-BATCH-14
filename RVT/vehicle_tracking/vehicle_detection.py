import ultralytics
import cv2
import os
from PIL import Image
import os
import numpy as np

from .feature_extraction import compare_images

# Load YOLO
model_path = os.path.join(os.path.dirname(__file__), '..\models\detection.pt')

model = ultralytics.YOLO(model_path)

def detect_vehicles(frame):
    # Perform object detection

    detected_vehicles = []
    results = model(frame)

    # create a new image with bounding boxes and labels 
    output_img = frame
    labels = model.names
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        vehicle_img = output_img[y1:y2, x1:x2]
        
        

        detected_vehicles.append((output_img, labels[int(box.cls)]))
        

    return detected_vehicles



def get_similarity_of_frame(frame):
    frame = np.array(frame)
    detected_vehicles = detect_vehicles(frame)
    similarities = []

    query_image = Image.open(os.path.join(os.path.dirname(__file__), '..\query_images\query.png'))
    

    for vehicle in detected_vehicles:
        detected_image = vehicle[0]
        detected_image = Image.fromarray(detected_image)
        similarity = compare_images(query_image, detected_image)
        similarities.append(similarity)
    
    return similarities