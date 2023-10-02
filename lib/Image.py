from PIL import Image
import cv2
class StaticImage:
    def __init__(self, imagePath):
        self.path = imagePath
        self.image = Image.open(self.path)
    def take_frame_by_frame(self) -> Image:
        return self.image
    
class DynamicImage:
    def __init__(self, imagePath):
        self.path = imagePath
        self.last = None
        self.video = []
        self.open_Image()
    def open_Image(self):
        
        cap = cv2.VideoCapture(self.path)

        while(cap.isOpened()):
            ret, frame = cap.read()
            # print(frame, ret)
            if ret:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                self.video.append(image)
            else:
                break
        
        cap.release()
    def take_frame_by_frame(self, reset = 0) -> Image:
        if reset != 0:
            self.last == None
        if self.last == None:
            self.last = -1
        if self.last + 1 >= len(self.video):
            self.last = -1
        index = self.last + 1
        self.last = index
        return self.video[index]