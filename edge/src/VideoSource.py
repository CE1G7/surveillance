from abc import ABC, abstractmethod

class VideoSource(ABC):
    @abstractmethod
    def read_frame(self):
        pass

    @abstractmethod
    def 