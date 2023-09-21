from ultralytics import YOLO

# Load a model
model = YOLO('runs/detect/train4/weights/best.pt')  # load a custom trained

# Export the model
model.export(format='tfjs')
