from ultralytics import YOLO
import cv2

model = YOLO("best.pt")
results = model.predict(source="spaghetti.png", show=True)
#results = model.predict(source="http://raspberrypi.local/webcam/?action=stream", show=True)
#results = model.predict(source="https://youtu.be/JGpCGOMgk5g", show=True)
print(results)