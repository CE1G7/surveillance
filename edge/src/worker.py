from inference import Recognize
from framebuffer import FrameBuffer
from EventManager import EventManager
import threading
class Worker:
    def __init__(self,recognizer: Recognize, framebuffer: FrameBuffer, eventmanager: EventManager):
        self.recognizer = recognizer
        self.framebuffer = framebuffer
        self.eventmanager = eventmanager
        self.thread = threading.Thread(target=self.run)
        self._stop = threading.Event()

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.thread.join()

    def run(self):
        while not self._stop.is_set():
            frame = self.framebuffer.get_frame()
            if frame is None:  # no stream connected yet
                self._stop.wait(0.1)
                continue
            res = self.recognizer.recognize(frame)
            print(res)