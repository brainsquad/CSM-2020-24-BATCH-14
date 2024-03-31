from ultralytics import YOLO
import os
import cv2
import flask

# Load the model
model = YOLO('yolov8s')

# Load the video
# cap = cv2.VideoCapture('videos/video1.mp4')
# cap = cv2.VideoCapture("http://192.168.147.195:4000/video")
cap = cv2.VideoCapture(0)


# Create a Flask app
app = flask.Flask(__name__)

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            # Read the frame
            ret, frame = cap.read()
            if not ret:
                break

            # Perform the detection
            results = model(frame)
            
            for box in results[0].boxes:
                x, y, w, h = box.xyxy[0]
                cv2.rectangle(frame, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 2)
                cv2.putText(frame, f'{model.names[int(box.cls)]}', (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            
            

            # Convert the frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()

            # Yield the frame in the response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return flask.Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='192.168.51.195', port=5000)





