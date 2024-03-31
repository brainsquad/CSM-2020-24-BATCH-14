import flask
import cv2


app = flask.Flask(__name__)

@app.route('/video')
def video():

    cap = cv2.VideoCapture('http://192.168.51.195:3999/video')

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return flask.Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='192.168.51.195', port=3999 , threaded= True, processes=1)
