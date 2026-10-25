from framebuffer import FrameBuffer
from inference import Recognize
from worker import Worker
from EventManager import EventManager
def main():
    frame_buffer = FrameBuffer()
    recognizer = Recognize()
    event_manager = EventManager()
    worker = Worker(recognizer=recognizer,framebuffer=frame_buffer, eventmanager=event_manager)
    worker.start()
    

if __name__ == "__main__":
    main()