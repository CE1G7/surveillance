import numpy as np
import cv2

# Implemented as a queue of 1 depth for now
class FrameBuffer:
    def __init__(self):
        self.frame = cv2.imread("images/image.png")

    def set_frame(self,frame: np.ndarray):
        self.frame = frame

    def get_frame(self):
        return self.frame