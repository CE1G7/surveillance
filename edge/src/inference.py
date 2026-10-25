from ultralytics import YOLO
import cv2
import numpy as np
from framebuffer import FrameBuffer
class Recognize:
    def __init__(self):
        self.model = YOLO("models/yolo26m.pt") #model fetched from huggingface

    def recognize(self,frame: np.ndarray):
        im = cv2.imread(frame)
        results = self.model.predict(source=im, save=True)
        return results
