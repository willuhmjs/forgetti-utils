from ultralytics import YOLO
import cv2
import json

model = YOLO("best.pt")
results = model.predict(source="https://fabbaloo.com/wp-content/uploads/2020/05/image-asset_img_5eb0af2d092e0.jpg", verbose=False, show=False, stream=True, conf=0.55)
for r in results:
    j = json.loads(r.tojson())
    img = r.plot()
    cv2.imwrite("test.jpg", img)
    if len(j) > 0:
        confidence = round(j[0]["confidence"], 2)
        if confidence >= 0.7:
            print(f'Sure detection found @ {confidence}')
        elif confidence >= 0.55:
            print(f'Possible detection found @ {confidence}')
