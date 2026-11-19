from framebuffer import FrameBuffer
from inference import Recognize
from worker import Worker
from streaming import RTMPServer
def main():
    frame_buffer = FrameBuffer(24,30)
    rtmp_server = RTMPServer(frame_buffer)
    recognizer = Recognize()
    worker = Worker(recognizer=recognizer,framebuffer=frame_buffer)
    rtmp_server.start()
    worker.start()
    

if __name__ == "__main__":
    main()
