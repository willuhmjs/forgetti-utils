from ultralytics import YOLO

# gotta play around with ultralytics config to make this work
# change the dir in the files if theres a problem
# this code is really for a private project so i dont care about reusability

model = YOLO("yolov8n.yaml")
model.train(data="dataset/data.yaml", epochs=125, imgsz=640, device=0, save_period=50)
metrics = model.val()
path = model.export(format="tfjs");