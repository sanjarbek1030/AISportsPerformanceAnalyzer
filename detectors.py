from pathlib import Path
from ultralytics import YOLO
from models import Detection
class PlayerDetector:
    def __init__(self,cfg): self.model=YOLO(cfg.player_model); self.cfg=cfg
    def track(self,frame,n,t):
        rs=self.model.track(frame,persist=True,tracker=self.cfg.tracker,conf=self.cfg.confidence_threshold,iou=self.cfg.iou_threshold,classes=[0],device=self.cfg.device,verbose=False)
        out=[]
        if not rs or rs[0].boxes is None:return out
        for b in rs[0].boxes:
            if b.id is None:continue
            q=b.xyxy[0].cpu().numpy().tolist(); out.append(Detection(tuple(map(float,q)),float(b.conf[0].cpu()),int(b.cls[0].cpu()),n,t,int(b.id[0].cpu())))
        return out
class BallDetector:
    def __init__(self,cfg): self.cfg=cfg; self.model=YOLO(cfg.ball_model) if Path(cfg.ball_model).exists() else None
    def detect(self,frame,n,t):
        if self.model is None:return []
        rs=self.model.predict(frame,conf=self.cfg.ball_confidence_threshold,device=self.cfg.device,verbose=False); out=[]
        if not rs or rs[0].boxes is None:return out
        for b in rs[0].boxes:
            q=b.xyxy[0].cpu().numpy().tolist(); out.append(Detection(tuple(map(float,q)),float(b.conf[0].cpu()),int(b.cls[0].cpu()),n,t))
        return out
