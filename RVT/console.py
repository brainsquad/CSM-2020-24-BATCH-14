import cv2

image = cv2.imread('images/frame.png')
base64_img = cv2.imencode('.png', image)[0]
files={'upload':base64_img}

print(files)