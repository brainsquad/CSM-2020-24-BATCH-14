from flask import Flask, request, render_template, Response
from PIL import Image
import io
import cv2
import numpy as np
import base64
import requests
import os

from vehicle_detection.detect_vehicles import detect_vehicles

# Assuming you have a function `detect_objects` that takes an image and returns an image with detected objects
# from object_detection import detect_objects

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if image is not empty

        if 'vehicle_number' in request.form and request.form['vehicle_number'] != '':
            vehicle_number = request.form['vehicle_number']
            print(vehicle_number)
            return render_template('number_dashboard.html', vehicle_number=vehicle_number)

        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']
        image = Image.open(file.stream)  # open image
        npimg = np.array(image)  # convert to numpy array
        img = cv2.cvtColor(npimg, cv2.COLOR_RGB2BGR)  # convert to opencv image (BGR)
        base64_img, label = detect_vehicles(img)

        
        # files={'upload': cv2.imencode('.png', img)[1]}
        # response = requests.post(
        #             'https://api.platerecognizer.com/v1/plate-reader/',
        #             headers={'Authorization': 'Token faa4d2de857f75368d089929c9d6b81ccd83f1c5'},
        #             files=files)

        # print(response.json())

        # # save the base64 image to a file 
        
        # with open('query_images/image.png', 'wb') as f:
        #     f.write(base64.b64decode(base64_img))




        return render_template('dashboard.html', image=base64_img)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)