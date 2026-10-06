from dataclasses import dataclass,field
from pathlib import Path
import torch
@dataclass
class Config:
    input_video='input/sports_input.mp4'; output_video='output/sports_analysis.mp4'; output_dir='output'
    player_model='yolo11n.pt'; ball_model='models/soccer_ball.pt'; confidence_threshold=.35; ball_confidence_threshold=.20; iou_threshold=.50; tracker='bytetrack.yaml'
    device:str=field(default_factory=lambda:'cuda' if torch.cuda.is_available() else 'cpu')
    field_width_m=105.; field_height_m=68.; calibration_image_points:list=field(default_factory=list)
    possession_radius_m=2.; possession_confirm_frames=5; possession_release_frames=4
    max_human_speed_kmh=38.; smoothing_window=7; trail_length=50; detection_interval=1; debug_mode=False
    def ensure(self): Path(self.output_dir).mkdir(parents=True,exist_ok=True)
