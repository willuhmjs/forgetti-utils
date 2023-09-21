from ultralytics import YOLO

# Load a model
model = YOLO('runs/detect/train/weights/epoch125.pt')  # load a partially trained model

# Resume training
results = model.train(resume=True)
metrics = model.val()
path = model.export(format="tfjs");