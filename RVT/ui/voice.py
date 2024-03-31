from flask import Flask, request, render_template, Response
import serial 
import time 
import json


arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1) 

def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    time.sleep(0.05) 
    data = arduino.readline() 
    return data

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def send_command():
    if request.method == 'POST':
        command = request.form['command']
        if command == "start":
            write_read("0")
            return render_template('voice.html', status="Started")

        elif command == "stop":
            write_read("1")
            return render_template('voice.html', status="Stopped")

        else:
            return render_template('voice.html', status="Invalid command")

    else:
        return render_template('voice.html', status="No command")
    
    return render_template('voice.html', status="No command")

    


if __name__ == '__main__':
    app.run(host="192.168.12.195")
    # pass
        

