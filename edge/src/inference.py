from ultralytics import YOLO
import cv2
import numpy as np
from framebuffer import FrameBuffer
class Recognize:
    def __init__(self):
        self.model = YOLO("models/yolo26m.pt") #model fetched from huggingface

    def recognize(self,frame: np.ndarray):
        results = self.model.predict(source=frame, save=True)
        return results


def main():
    r = Recognize()
    res = r.recognize()
    print(f"Result: {res}")


if __name__ == "__main__":
    main()