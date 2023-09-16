from roboflow import Roboflow
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# take version as an argument
version = sys.argv[1]

rf = Roboflow(api_key=os.getenv("ROBOFLOW"))

project = rf.workspace().project("wfpfopt")
dataset = project.version(version).download("yolov8", "dataset")

