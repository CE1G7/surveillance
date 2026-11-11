from framebuffer import FrameBuffer
from inference import Recognize
from worker import Worker
from EventManager import EventManager
from streaming import RTMPServer
def main():
    frame_buffer = FrameBuffer(None)
    rtmp_server = RTMPServer(frame_buffer)
    recognizer = Recognize()
    event_manager = EventManager()
    worker = Worker(recognizer=recognizer,framebuffer=frame_buffer, eventmanager=event_manager)
    rtmp_server.start()
    worker.start()
    

if __name__ == "__main__":
    main()
