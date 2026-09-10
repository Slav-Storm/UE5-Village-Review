"""Run a bounded causal window, stop early on a casualty or recognition.
This orchestrator never compares V1 and never supplies future state to policy.
"""
import json, sys
import engine_v2 as e
S=json.loads(e.STATE.read_text());start=S['time'];limit=float(sys.argv[1]) if len(sys.argv)>1 else 12
before=len(S['events']);cycle=S['cycle'];fatal=e.count(S)['fatalities']
while not S['closed'] and S['time']<start+limit and S['cycle']<cycle+16:
    old=len(S['events']);e.step(S)
    fresh=S['events'][old:]
    if any(x['fatalities'] or x['kind'] in ['guard recognition','Witch secures Mayor','Mayor final death'] for x in fresh):break
e.save(S)
print(json.dumps({'window':[start,S['time']],'cycles':[cycle+1,S['cycle']],'population':e.count(S),'actors':{k:e.actor_pos(S,k) for k in ['Blood','Bone','Witch']},'blood_power':{k:v for k,v in e.power(S).items() if k not in ['source_ids','saturation']},'events':[{k:v for k,v in x.items() if k in ['id','time','actor','kind','xy','description','fatalities','injuries','target_group','attention_trigger','recognition_elapsed_s']} for x in S['events'][before:]],'guard':{'recognition':S['actors']['Bone']['recognition'],'stage':S['actors']['Bone']['guard_stage']},'latest_Blood_decisions':[{k:v for k,v in a.items() if k in ['decision_time','decision','selected','path']} for a in S['actor_plans'] if a['actor']=='Blood'][-2:],'closed':S['closed']},ensure_ascii=False,indent=2))
