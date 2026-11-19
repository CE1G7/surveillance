from inference import Recognize
from framebuffer import FrameBuffer
from framebuffer import Frame
import threading
import requests
import cv2
class Worker:
    def __init__(self,recognizer: Recognize, framebuffer: FrameBuffer):
        self.recognizer = recognizer
        self.framebuffer = framebuffer
        self.thread = threading.Thread(target=self._run)
        self._stop = threading.Event()

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.thread.join()

    def _run(self):
        while not self._stop.is_set():
            frame = self.framebuffer.get_frame()
            if frame is None:  # no stream connected yet
                self._stop.wait(0.1)
                continue
            res = self.recognizer.recognize(frame.image)
            if(res):
                print("detection")
                print(res[0])
                #self.framebuffer.get_clip(frame,2)
            else:
                print("No result")