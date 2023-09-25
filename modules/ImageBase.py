from abc import ABC, abstractmethod

class ImageBase(ABC):
    @abstractmethod
    def loadFromPath():
        pass
    @abstractmethod
    def loadFromByte():
        pass
    def loadFromURL():
        pass
    