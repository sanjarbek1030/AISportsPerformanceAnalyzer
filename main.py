import logging,cv2,math
from config import Config
from models import PlayerTrack,BallState,Event
from detectors import PlayerDetector,BallDetector
from field_mapper import FieldMapper
from analytics import ReportGenerator

def main():
    logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(message)s')
    c=Config(); c.ensure(); cap=cv2.VideoCapture(c.input_video)
    if not cap.isOpened():raise FileNotFoundError(f'Cannot open {c.input_video}')
    fps=cap.get(cv2.CAP_PROP_FPS); w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    writer=cv2.VideoWriter(c.output_video,cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
    if not writer.isOpened():raise RuntimeError('Cannot create output video')
    pd=PlayerDetector(c); bd=BallDetector(c); mapper=FieldMapper(c.field_width_m,c.field_height_m,c.calibration_image_points)
    players={}; events=[]; tracks=[]; frame_no=0; last_ball=None
    while True:
        ok,frame=cap.read()
        if not ok:break
        t=frame_no/fps if fps else 0
        dets=pd.track(frame,frame_no,t)
        for d in dets:
            pid=d.track_id; p=players.setdefault(pid,PlayerTrack(pid)); x=(d.bbox[0]+d.bbox[2])/2; y=d.bbox[3]; f=mapper.image_to_field(x,y)
            p.add(x,y,t,d.bbox,d.confidence,f[0] if f else None,f[1] if f else None)
            cv2.rectangle(frame,(int(d.bbox[0]),int(d.bbox[1])),(int(d.bbox[2]),int(d.bbox[3])),(255,120,50),2)
            cv2.putText(frame,f'ID {pid}',(int(d.bbox[0]),max(15,int(d.bbox[1])-5)),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2)
            tracks.append({'frame':frame_no,'timestamp':t,'player_id':pid,'team':p.team_id,'image_x':x,'image_y':y,'field_x':f[0] if f else None,'field_y':f[1] if f else None,'speed_kmh':None,'confidence':d.confidence})
        balls=bd.detect(frame,frame_no,t); ball=max(balls,key=lambda x:x.confidence) if balls else None
        if ball:
            bx=(ball.bbox[0]+ball.bbox[2])/2; by=(ball.bbox[1]+ball.bbox[3])/2
            vx=vy=0
            if last_ball:
                dt=t-last_ball.timestamp
                if dt>0:vx=(bx-last_ball.x)/dt;vy=(by-last_ball.y)/dt
            last_ball=BallState(bx,by,t,ball.confidence,vx,vy); cv2.circle(frame,(int(bx),int(by)),6,(255,255,255),2)
        cv2.putText(frame,f'TIME {int(t//60):02d}:{int(t%60):02d}',(15,35),cv2.FONT_HERSHEY_SIMPLEX,.8,(255,255,255),2)
        writer.write(frame); frame_no+=1
    cap.release(); writer.release(); ReportGenerator(c.output_dir).write(players,events,tracks,{'path':c.input_video,'width':w,'height':h,'fps':fps,'frames':count,'duration_seconds':count/fps if fps else 0})
    logging.info('Completed: %s',c.output_dir)
if __name__=='__main__':main()
