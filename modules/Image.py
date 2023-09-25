from modules.ImageBase import ImageBase
from PIL import Image as PILImage
import io
from requests import get
import numpy as np
class Image(ImageBase):
    def __init__(self):
        self.image = None
    def loadFromPath(self,path: str):
        self.image = PILImage.open(open(path, 'rb'))
        self.image.seek(0)
    def loadFromByte(self, image_data: bytes):
        self.image = PILImage.open(io.BytesIO(image_data))
        self.image.seek(0)
    def loadFromURL(self, url: str):
        self.loadFromByte(get(url).content)
    def size(self):
        return np.array(self.image).shape
    def showImage(self):
        self.image.show()