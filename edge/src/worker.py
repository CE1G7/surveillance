from inference import Recognize
from framebuffer import FrameBuffer
from EventManager import EventManager
import threading
import cv2
class Worker:
    def __init__(self,recognizer: Recognize, framebuffer: FrameBuffer, eventmanager: EventManager):
        self.recognizer = recognizer
        self.framebuffer = framebuffer
        self.eventmanager = eventmanager
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
            print("hello")
            if frame is None:  # no stream connected yet
                self._stop.wait(0.1)
                continue
            res = self.recognizer.recognize(frame)
            print(res)
            # plot() draws boxes + labels onto a copy of the frame with OpenCV; all highgui calls stay in this thread.
            cv2.imshow("edge", res[0].plot())
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self._stop.set()
        cv2.destroyAllWindows()