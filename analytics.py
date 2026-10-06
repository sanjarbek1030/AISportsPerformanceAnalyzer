from pathlib import Path
import json,pandas as pd,numpy as np
class ReportGenerator:
    def __init__(self,d):self.d=Path(d);self.d.mkdir(parents=True,exist_ok=True)
    def players(self,ps):
        return [{'player_id':p.player_id,'team':p.team_id,'playing_time':p.timestamps[-1]-p.timestamps[0] if p.timestamps else 0,'distance_km':p.distance_m/1000,'average_speed_kmh':p.average_speed_kmh,'max_speed_kmh':p.max_speed_kmh,'sprints':p.sprint_count,'possession_seconds':p.possession_time_s,'passes':p.passes,'successful_passes':p.successful_passes,'shots':p.shots,'shots_on_target':p.shots_on_target,'goals':p.goals,'assists':p.assists,'interceptions':None} for p in ps.values()]
    def write(self,ps,events,tracks,meta):
        rows=self.players(ps); pd.DataFrame(rows).to_csv(self.d/'player_statistics.csv',index=False)
        teams={}
        for p in ps.values():teams.setdefault(p.team_id,[]).append(p)
        total=sum(p.possession_time_s for p in ps.values()); tr=[]
        for k,v in teams.items():
            ds=[p.distance_m/1000 for p in v]; poss=sum(p.possession_time_s for p in v)
            tr.append({'team':k,'possession_percentage':poss/total*100 if total else None,'total_distance_km':sum(ds),'average_distance_km':float(np.mean(ds)) if ds else 0,'passes':sum(p.passes for p in v),'successful_passes':sum(p.successful_passes for p in v),'shots':sum(p.shots for p in v),'shots_on_target':sum(p.shots_on_target for p in v),'goals':sum(p.goals for p in v),'sprints':sum(p.sprint_count for p in v)})
        pd.DataFrame(tr).to_csv(self.d/'team_statistics.csv',index=False)
        pd.DataFrame([{'timestamp':e.timestamp,'frame':e.frame,'event_type':e.event_type,'player_id':e.player_id,'team_id':e.team_id,'confidence':e.confidence,'metadata':json.dumps(e.metadata)} for e in events]).to_csv(self.d/'event_log.csv',index=False)
        pd.DataFrame(tracks).to_csv(self.d/'player_tracks.csv',index=False)
        (self.d/'match_report.json').write_text(json.dumps({'video':meta,'players':rows,'teams':tr,'events':[e.__dict__ for e in events]},indent=2),encoding='utf8')
