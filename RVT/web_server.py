import flask
import cv2
from ultralytics import YOLO

app = flask.Flask(__name__)

model = YOLO('yolov8n.pt')



@app.route('/image')
def image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    image = cv2.resize(frame, (640, 360))

    results = model(image, iou = 0.5, conf = 0.5)

    for box in results[0].boxes:
        x,y,w,h = box.xywh[0]
        cv2.rectangle(image, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), (0,0,255), 1)
        cv2.putText(image, model.names[int(box.cls)], (int(x-w/2), int(y-h/2 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    
    return flask.Response(b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n',
                            mimetype='multipart/x-mixed-replace; boundary=frame')



    


app.run(host='192.168.51.195', port=4000)