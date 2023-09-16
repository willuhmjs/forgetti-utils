from roboflow import Roboflow
from dotenv import load_dotenv
import os
PROJ = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
rf = Roboflow(api_key=os.getenv("ROBOFLOW"))
project = rf.workspace().project("wfpfopt")

# will look for a file named "dataset" in the project directory
project.version(6).deploy("yolov8", f"{PROJ}/dataset/runs/detect/train/")