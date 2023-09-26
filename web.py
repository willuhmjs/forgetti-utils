from flask import Flask, Response
import numpy as np
import cv2
import json
import threading
from ultralytics import YOLO
from collections import deque

# Initialize Flask app
app = Flask(__name__)

# Function to generate frames from the YOLO predictions
def generate_frames():
    while True:
        if len(frames) > 0:
            frame = frames.popleft()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Function to run YOLO predictions and generate frames
def run_yolo():
    model = YOLO("best.pt")
    source = "URL_HERE"
    results = model.predict(source=source, verbose=False, show=False, stream=True, conf=0.55)
    for r in results:
        j = json.loads(r.tojson())
        img = r.plot()
        _, buffer = cv2.imencode('.jpg', img)
        frame_bytes = buffer.tobytes()
        if len(j) > 0:
            confidence = round(j[0]["confidence"], 2)
            if confidence >= 0.7:
                print(f'Sure detection found @ {confidence}')
            elif confidence >= 0.55:
                print(f'Possible detection found @ {confidence}')
        frames.append(frame_bytes)
        # Keep only the last 10 frames in the queue
        while len(frames) > 10:
            frames.popleft()

# Start running YOLO predictions in a separate thread
frames = deque()
threading.Thread(target=run_yolo, args=()).start()

# Serve the generated frames to each user
@app.route('/')
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)