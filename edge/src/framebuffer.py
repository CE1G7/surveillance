import numpy as np


# Implemented as a queue of 1 depth for now
class FrameBuffer:
    def __init__(self):
        self.frame = None

    def set_frame(self,frame: np.ndarray):
        self.frame = frame

    def get_frame(self):
        return self.frame