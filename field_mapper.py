import cv2,numpy as np
class FieldMapper:
    def __init__(self,w,h,points=None):
        self.w,self.h=w,h; self.H=None
        if points and len(points)==4:
            src=np.float32(points); dst=np.float32([[0,0],[w,0],[w,h],[0,h]])
            self.H=cv2.getPerspectiveTransform(src,dst)
    @property
    def calibrated(self): return self.H is not None
    def image_to_field(self,x,y):
        if self.H is None:return None
        p=cv2.perspectiveTransform(np.float32([[[x,y]]]),self.H)[0,0]; return float(p[0]),float(p[1])
