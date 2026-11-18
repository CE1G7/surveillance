import numpy as np
import cv2
from collections import deque
from itertools import islice
# Implemented as a queue of 1 depth for now
class Frame:
    def __init__(self,id,image):
        self.id = id
        self.image = image

class FrameBuffer:
    def __init__(self,fps,queue_len_s):
        self.current_frame = None
        self.buffer = deque(maxlen=fps*queue_len_s)
        self.ite = -1
        self.fps = fps

    def set_frame(self,frame_in: np.ndarray):
        self.ite +=1
        self.current_frame = Frame(self.ite,frame_in)
        self.buffer.appendleft(cv2.imencode(".jpg",frame_in)[1])

    def get_frame(self):
        return self.current_frame

    def get_clip(self,frame: Frame, length: int):
        frames = len*self.fps
        buffer_len = len(self.buffer)
        diff = self.ite - frame.id
        index_end_clip = diff
        index_start_clip = diff + frames
        if(buffer_len<index_start_clip):
            return None
        return self.decode(index_end_clip,index_start_clip)
    
    def decode(self,i_end,i_start):
        frames = list(islice(self.buffer,i_end,i_start))
        frames.reverse()
        decoded = []
        for frame in frames:
            decoded.append(cv2.imdecode(frame,cv2.IMREAD_COLOR))
        h, w = decoded[0].shape[:2]
        out = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (w, h))
        for d in decoded:
            out.write(d)
        out.release()
        return True