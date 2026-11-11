import os
import threading

import cv2

from framebuffer import FrameBuffer

# Makes OpenCV's FFmpeg backend act as the RTMP server instead of a client.
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "listen;1"


# shortcut: FFmpeg listen mode accepts one publisher at a time; run mediamtx/nginx-rtmp if multiple drones must stream at once.
class RTMPServer:
    def __init__(self, framebuffer: FrameBuffer, url: str = "rtmp://0.0.0.0:1935/live/stream"):
        self.framebuffer = framebuffer
        self.url = url
        self.thread = threading.Thread(target=self.run, daemon=True)
        self._stop = threading.Event()

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.thread.join()

    def run(self):
        # Re-listen after a publisher disconnects or the open times out (~30s with no publisher).
        while not self._stop.is_set():
            cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
            while cap.isOpened() and not self._stop.is_set():
                ok, frame = cap.read()
                if not ok:
                    break
                self.framebuffer.set_frame(frame)
            cap.release()
