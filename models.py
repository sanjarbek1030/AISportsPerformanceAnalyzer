from dataclasses import dataclass, field
from typing import Any
@dataclass
class Detection:
    bbox: tuple[float,float,float,float]; confidence: float; class_id: int; frame: int; timestamp: float; track_id: int|None=None
@dataclass
class BallState:
    x: float; y: float; timestamp: float; confidence: float; velocity_x: float=0.; velocity_y: float=0.
@dataclass
class Event:
    event_type: str; timestamp: float; frame: int; player_id: int|None=None; team_id: str|None=None; confidence: float=0.; metadata: dict[str,Any]=field(default_factory=dict)
@dataclass
class PlayerTrack:
    player_id:int; team_id:str='unknown'; positions_image:list=field(default_factory=list); positions_field:list=field(default_factory=list); timestamps:list=field(default_factory=list); bounding_boxes:list=field(default_factory=list); confidences:list=field(default_factory=list); speeds_kmh:list=field(default_factory=list); accelerations_mps2:list=field(default_factory=list); distance_m:float=0.; possession_time_s:float=0.; passes:int=0; successful_passes:int=0; shots:int=0; shots_on_target:int=0; goals:int=0; assists:int=0; sprint_count:int=0; max_speed_kmh:float=0.; average_speed_kmh:float=0.
    def add(self,x,y,t,bbox,conf,fx=None,fy=None):
        self.positions_image.append((x,y,t)); self.timestamps.append(t); self.bounding_boxes.append(bbox); self.confidences.append(conf)
        if fx is not None: self.positions_field.append((fx,fy,t))
