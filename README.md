# AI Sports Performance Analyzer

Production-oriented football video analytics baseline based on the supplied specification.

## Implemented foundation
- YOLO person detection + persistent ByteTrack IDs
- bottom-center player ground point
- optional homography field mapping
- dedicated optional soccer-ball model
- ball state and velocity
- original video resolution/FPS output
- player-track CSV
- player/team/event CSV report structure
- JSON match report
- logging and explicit failure handling

## Important reliability rule
Do not treat uncalibrated pixel distances as meters. Configure four field landmarks before enabling physical distance/speed analytics. Do not use a generic COCO detector as a serious soccer-ball detector; supply a soccer-ball model trained for the target footage.

## Run
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

Input: `input/sports_input.mp4`
Ball model: `models/soccer_ball.pt`
Outputs: `output/`

## Production roadmap
1. player detection/tracking
2. calibration + movement
3. ball tracking + possession
4. pass/shot/goal state machines
5. heatmaps + tactical metrics
6. ReID, jersey OCR, pose, temporal action recognition

The supplied specification calls for conservative inference. This project therefore leaves unsupported statistics null instead of fabricating them.
