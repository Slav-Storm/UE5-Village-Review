"""Incremental V2 state engine. No V1/T2/T3 imports, no outcome target.

Commands: init, inspect, step. Each step independently records ACTION selection,
then REACTION selection, then advances existing commitments to the next event.
No call loops over the whole massacre. Human review can inspect every boundary.
"""
import json, math, hashlib, copy, sys
from pathlib import Path
import numpy as np
from shapely.geometry import Point, LineString, Polygon, mapping
from shapely.ops import unary_union
import spatial_v2 as sp

HERE=Path(__file__).resolve().parent; OUT=HERE/'package'; STATE=HERE/'state.json'
RULE=json.loads((OUT/'v2_rules.json').read_text()); H=sp.H
def dump(p,o,pretty=False):p.write_text(json.dumps(o,ensure_ascii=False,indent=2 if pretty else None,separators=None if pretty else (',',':'))+'\n',encoding='utf-8')
def alive(S,g=None):return [p for p in S['people'].values() if p['alive'] and (g is None or p['group']==g)]
def count(S):
    a=alive(S);return {'alive':len(a),'fatalities':170-len(a),'injured':sum(p['injured'] for p in a)}
def gp(S,gid):return S['groups'][gid]
def pos(S,g,t=None):
    if isinstance(g,str):g=gp(S,g)
    t=S['time'] if t is None else t;m=g.get('motion')
    if m:return sp.along(m['path'],max(0,t-m['start'])*m['speed'])
    return g['xy']
def actor_pos(S,name,t=None):
    t=S['time'] if t is None else t
    if name=='Witch':return sp.witch_at(t,S['witch_route'])[:2]
    a=S['actors'][name];m=a.get('motion')
    return sp.along(m['path'],max(0,t-m['start'])*m['speed']) if m else a['xy']
def member_pos(S,p,t=None):
    q=pos(S,p['group'],t);g=gp(S,p['group']);ids=g['members'];i=ids.index(p['id']);off=[(i%3-1)*.65,(i//3)*.65-.4]
    # Single-person / named source point remains exact; larger group offsets
    # merely resolve bodies inside the already assigned 1-3 m activity patch.
    if len(ids)==1:return q
    proposed=[q[0]+off[0],q[1]+off[1]]
    if not sp.RIM.covers(Point(proposed)):
        toward=np.array(sp.RIM.centroid.coords[0])-np.array(q);toward/=np.linalg.norm(toward) or 1
        proposed=(np.array(q)+toward*(.65+.35*i)).tolist()
    if g.get('building') and not sp.ROOFS[g['building']].covers(Point(proposed)):return q
    return proposed
def state_snapshot(S):
    return {'time':S['time'],'population':count(S),'actors':{k:actor_pos(S,k) for k in ['Blood','Bone','Witch']},
      'groups':{k:{'members':[p['id'] for p in alive(S,k)],'xy':pos(S,k),'building':g.get('building'),'intention':g['intention'],'knowledge':copy.deepcopy(g['knowledge'])} for k,g in S['groups'].items() if alive(S,k)},'blood_power':power(S),'mayor_state':S['mayor_state']}

def init():
    S={'schema':'village.v2.simulation.1','time':90.,'cycle':0,'groups':{},'people':{},'events':[],'movements':[],'knowledge_ledger':[],'resource_sources':[],'resource_draws':[],'power_history':[],'actor_plans':[],'cycles':[],'seeds':[], 'witch_route':sp.witch_route(),'mayor_state':'alive at home, emergency unexplained','bell_started':False,'pending':[],'closed':False,'branch_policy':'No post-T90 V1 inputs. No fatality target. Each step selects only from current evidence.'}
    for old in H['groups']:
        g=copy.deepcopy(old);g.update({'motion':None,'reacted':False,'last_reaction':90.,'last_warning':{},'refuge_attempts':0,'threat_events':[],'trait':int(hashlib.sha256(g['id'].encode()).hexdigest()[:4],16)%5})
        S['groups'][g['id']]=g
        for i,pid in enumerate(g['members']):
            d=g['dead'];S['people'][pid]={'id':pid,'group':g['id'],'origin':g['cohort'],'role':g['role'],'micro':g['micro'],'alive':not bool(d),'injured':g['injured'],'injured_since':56 if g['injured'] else None,'injury_treated':False,'fatality':None,'blood_generated':0.}
            p=S['people'][pid]
            p['role_detail']=('parent' if i==0 else 'child') if g['micro']=='M05' else ('caregiver' if i==0 else 'child') if g['micro']=='M09' else g['role']
            if d:
                p['fatality']={'time':d['t'],'actor':d['actor'],'event':d['event'],'xy':g['xy'],'intention':g['role'],'witnesses':'preserved T1/Step2B record','exposure':'approved pre90'}
                add_source(S,pid,g['xy'],1.,d['t'],d['event'])
            elif g['injured']:add_source(S,pid,member_pos(S,p),.15+.006*(90-56),56,'E03 injury through +90')
    S['actors']={'Blood':{'xy':H['actors']['Blood'],'motion':None,'ready':90.,'mode':'selecting concentration','carry':0.,'cooldown':0},'Bone':{'xy':H['actors']['Bone'],'motion':None,'ready':90.,'mode':'watching M05','last_targets':[],'recognition':None,'guard_stage':0,'interest':None}}
    S['initial_snapshot']=state_snapshot(S);S['snapshots']=[copy.deepcopy(S['initial_snapshot'])]
    dump(OUT/'v2_initial_state.json',S['initial_snapshot'],True);save(S);return S

def add_source(S,pid,q,amount,t,event):
    p=S['people'][pid];amount=min(amount,max(0,1.-p['blood_generated']))
    if amount<=.000001:return
    p['blood_generated']+=amount
    sid=f'RS{len(S["resource_sources"])+1:04d}'
    S['resource_sources'].append({'id':sid,'person':pid,'xy':list(q),'created':t,'event':event,'volume':amount,'remaining':amount})

def power(S,t=None,q=None):
    t=S['time'] if t is None else t;q=actor_pos(S,'Blood',t) if q is None else q;a=S['actors']['Blood'];br=RULE['blood'];radius=br['control_radius_base_m'];accessible=a['carry']
    # Reach grows only when an already accessible source increases capacity.
    # Iterate this local frontier; it is still capped and never village-wide.
    for _ in range(4):
        sources=[r for r in S['resource_sources'] if r['created']<=t and sp.dist(q,r['xy'])<=radius and r['remaining']>1e-6]
        accessible=a['carry']+sum(r['remaining'] for r in sources);s=1-math.exp(-accessible/br['saturation_scale_units']);radius=32+40*s
    emotional=1+.22*max(0,min(1,(t-S['witch_route']['arrival'])/20))
    label='Awakened' if accessible<2 else 'Fed' if accessible<12 else 'Saturated' if accessible<32 else 'Deluge'
    return {'time':t,'xy':q,'accessible_units':round(accessible,5),'carried_units':round(a['carry'],5),'state':label,'saturation':s,'emotion_multiplier':emotional,'control_m':min(82,radius*emotional),'sense_m':min(78,(23+44*s)*emotional),'range_m':min(37,(13+19*s)*emotional),'width_m':min(26,(6+16*s)*emotional),'pressure':(1.15+2.4*s)*emotional,'source_ids':[r['id'] for r in sources],'movement_speed_m_s':1.5}

def signatures(S):
    """Simulator returns a coarse sensory signal, never exact headcounts to Blood.
    Members remain in an audit-only evidence partition, unavailable to selector.
    """
    b=actor_pos(S,'Blood');pw=power(S);raw=[]
    # Combine physical co-location BEFORE thresholding. A refuge's signal must
    # not depend on how T0 happened to divide its occupants into origin groups.
    physical=[]
    for gid,g in S['groups'].items():
        members=alive(S,gid)
        if not members:continue
        q=pos(S,g);building=g.get('building')
        match=next((x for x in physical if (building and x['building']==building) or (not building and not x['building'] and sp.dist(x['q'],q)<6)),None)
        if match:
            n=len(match['members']);m=len(members);match['q']=[(match['q'][i]*n+q[i]*m)/(n+m) for i in range(2)];match['members']+=members;match['gids'].append(gid);match['noisy']|=g.get('noise_until',0)>S['time']
        else:physical.append({'q':q,'building':building,'members':members,'gids':[gid],'noisy':g.get('noise_until',0)>S['time']})
    for cluster in physical:
        q=cluster['q'];d=sp.dist(b,q);members=cluster['members'];building=cluster['building']
        if d>pw['sense_m']:continue
        visible=not building and sp.sight(b,q)
        noisy=cluster['noisy'];bleeding=sum(p['injured'] and not p['injury_treated'] for p in members)
        # Density is a physical field. A single quiet person has weak signal.
        density=min(3.5,math.sqrt(len(members)))
        cover=.3 if building=='Church' else (.55 if building=='MayorHall' else .65 if building else 1.)
        singleton=.20 if len(members)==1 and not bleeding and not noisy else 1.
        field=density*cover*singleton*(1-d/pw['sense_m'])**.8*(1+pw['saturation']*.8)
        if bleeding:field+=min(1.6,bleeding*.4)*max(0,1-d/pw['sense_m'])
        if visible:field+=density*.7*max(.2,1-d/55)
        if noisy and d<42:field+=.65
        if field<.48:continue
        raw.append({'q':q,'field':field,'gids':cluster['gids'],'members':[p['id'] for p in members],'visible':visible,'bleeding':bool(bleeding),'noisy':noisy,'building':building})
    # Merge nearby signals, not all origin-cohort members across the map.
    used=set();out=[]
    for i,r in sorted(enumerate(raw),key=lambda x:-x[1]['field']):
        if i in used:continue
        near=[(j,z) for j,z in enumerate(raw) if j not in used and sp.dist(z['q'],r['q'])<8]
        for j,z in near:used.add(j)
        weight=sum(z['field'] for _,z in near);q=[sum(z['q'][k]*z['field'] for _,z in near)/weight for k in range(2)];q=[round(v/2)*2 for v in q]
        band='dense' if weight>=4.8 else 'substantial' if weight>=2.5 else 'small'
        strength=3 if band=='dense' else 2 if band=='substantial' else 1
        cues=[]
        if any(z['visible'] for _,z in near):cues.append('visible movement/presence')
        if any(z['bleeding'] for _,z in near):cues.append('nearby bleeding signature')
        if any(z['noisy'] for _,z in near):cues.append('local voices/activity')
        if any(z['building'] for _,z in near):cues.append('attenuated living-blood presence behind structure; no exact census')
        out.append({'id':f'SIG{len(out)+1:02d}','bearing_xy':q,'density_band':band,'strength_band':strength,'distance_m':round(sp.dist(b,q),2),'cues':cues,'audit_only_source_groups':[gid for _,z in near for gid in z['gids']],'audit_only_members':[p for _,z in near for p in z['members']]})
    return out

def perceived_score(sig):
    # No audit member/headcount access here. Concentration dominates travel cost.
    return sig['strength_band']*10-sig['distance_m']*.10+(1.4 if 'nearby bleeding signature' in sig['cues'] else 0)

def event(S,actor,kind,q,description,**extra):
    eid=f'V2E{len(S["events"])+1:03d}';e={'id':eid,'time':round(S['time'],6),'actor':actor,'kind':kind,'xy':list(q),'description':description,**extra,'fatalities':[],'injuries':[],'witnesses':[]};S['events'].append(e);return e
def learn(S,gid,category,text,eid,mode):
    g=gp(S,gid);rec={'time':S['time'],'recipient_group':gid,'category':category,'content':text,'source':eid,'mode':mode}
    key=(gid,category,text,eid)
    if any((r['recipient_group'],r['category'],r['content'],r['source'])==key for r in S['knowledge_ledger'][-150:]):return
    S['knowledge_ledger'].append(rec)
    if category in ['Blood','Bone']:g['knowledge'][category]=text
    elif category=='barrier':
        if mode=='direct':g['knowledge']['barrier_stage']=4
        g['knowledge']['barrier_evidence']=text;g['knowledge']['warnings'].append(rec)
    elif category=='Witch':g['knowledge']['Witch'].append(rec)
    elif category=='deaths':g['knowledge']['deaths'].append(rec)
    else:g['knowledge']['warnings'].append(rec)

def receive(S,e,radius=35,loud=False):
    for gid,g in S['groups'].items():
        if not alive(S,gid):continue
        q=pos(S,g);d=sp.dist(q,e['xy']);inside=g.get('building');same=inside and sp.ROOFS[inside].distance(Point(e['xy']))<2
        direct=(d<radius and not inside and sp.sight(q,e['xy'])) or (same and d<12)
        if gid in e.get('contact_groups',[]):direct=True
        if direct:
            e['witnesses'].append(gid);g['threat_events'].append(e['id']);g['last_threat']={'time':S['time'],'xy':e['xy'],'actor':e['actor'],'kind':e['kind'],'event':e['id']}
            if e['actor']=='Barrier':learn(S,gid,'barrier','direct reactive strike at boundary',e['id'],'direct')
            elif e['actor'] in ['Blood','Bone']:learn(S,gid,e['actor'],f'direct {e["kind"]} at {e["xy"]}',e['id'],'direct')
            identified=[]
            for pid in e['fatalities']:
                f=S['people'][pid]['fatality'];death_building=f.get('building')
                if inside and inside==death_building or (not inside and not death_building and sp.dist(q,f['xy'])<22 and sp.sight(q,f['xy'])):identified.append(pid)
            if identified:learn(S,gid,'deaths',','.join(identified),e['id'],'direct')
            if e['actor'] in ['Blood','Bone','Barrier']:g['knowledge']['routes'].append({'time':S['time'],'xy':e['xy'],'status':'locally dangerous event observed; no claim about all other routes','event':e['id']})
        elif loud and d<85:
            learn(S,gid,'sound','heavy crash / screams; cause and exact victims not visible',e['id'],'heard')
            if d<38:g['last_threat']={'time':S['time'],'xy':e['xy'],'actor':'unknown','kind':'nearby crash','event':e['id']}

def kill(S,p,e,exposure):
    if not p['alive']:return
    if p['role']=='Mayor' and e['actor']!='Witch':raise RuntimeError('Mayor exposed to non-Witch event: genuine rule contradiction, inspect before continuing')
    q=e['xy'] if e['actor']=='Barrier' else member_pos(S,p);p['alive']=False;p['fatality']={'time':S['time'],'event':e['id'],'actor':e['actor'],'xy':q,'building':gp(S,p['group']).get('building'),'intention':gp(S,p['group'])['intention'],'exposure':exposure,'witnesses':[]};e['fatalities'].append(p['id']);add_source(S,p['id'],q,1-p['blood_generated'],S['time'],e['id'])
    g=gp(S,p['group'])
    if not alive(S,g['id']) and g.get('motion'):
        m=g['motion'];where=pos(S,g);m['actual_end']=S['time'];m['actual_end_xy']=where;m['interruption']='all travelling members killed';g['motion']=None;g['xy']=where
def injure(S,p,e,exposure):
    if p['injured']:return
    p['injured']=True;p['injured_since']=S['time'];p['injury_exposure']=exposure;e['injuries'].append(p['id']);add_source(S,p['id'],member_pos(S,p),.15,S['time'],e['id'])
def seal_event(S,e,loud=False,radius=35):
    receive(S,e,radius,loud)
    for pid in e['fatalities']:
        S['people'][pid]['fatality']['witnesses']=[r['recipient_group'] for r in S['knowledge_ledger'] if r['source']==e['id'] and r['category']=='deaths' and pid in r['content'].split(',')]
    e['population_after']=count(S)
    if e['fatalities'] or e['kind'] in ['deliberate object strike','guard recognition','guard torment','Witch ignored appeal','bell','Witch secures Mayor','Mayor final death']:
        S['seeds'].append({'event':e['id'],'time':e['time'],'xy':e['xy'],'before_activity':[S['people'][p]['fatality']['intention'] for p in e['fatalities']],'seed':e['description'],'existing_features':[k for k,g in sp.GEOM.items() if sp.F[k]['category'] in ['building','outbuilding','proxy','civic_proxy','stairs'] and g.distance(Point(e['xy']))<5][:12],'production_state':'Planning association only; no final asset, gore or corpse pose.'})

def set_actor_motion(S,name,target,speed,why):
    a=S['actors'][name];start=actor_pos(S,name);pts=sp.path(start,target);duration=sp.length(pts)/speed
    a['xy']=start;a['motion']={'start':S['time'],'end':S['time']+duration,'path':pts,'speed':speed,'why':why};return duration

def plan_blood(S):
    a=S['actors']['Blood'];now=S['time']
    if now<a['ready']-.001:return {'actor':'Blood','continues':a['mode'],'until':a['ready']}
    a['xy']=actor_pos(S,'Blood');a['motion']=None
    sigs=signatures(S);pw=power(S);S['power_history'].append(pw)
    if not sigs:
        # Search follows last personally perceived activity, never hidden census.
        a['ready']=now+8;a['mode']='listen / sample local blood field'
        return {'actor':'Blood','decision':'observe; no meaningful perceived concentration','candidates':[],'power':pw,'until':a['ready']}
    chosen=max(sigs,key=perceived_score);target=chosen['bearing_xy'];distance=sp.dist(a['xy'],target)
    entry={'actor':'Blood','decision_time':now,'candidates':sigs,'selected':chosen['id'],'basis':'coarse perceived density, bleeding, distance and accessible approach; no audit headcounts used','power':pw}
    if distance<=pw['range_m']*.84:
        a['mode']='windup toward perceived concentration';a['ready']=now+3.5
        S['pending'].append({'time':a['ready'],'kind':'blood_strike','target':target,'selection':entry})
        e=event(S,'Blood','visible windup',a['xy'],'Blood gathers accessible environmental blood and turns toward a locally perceived concentration.',aim=target,power=pw);receive(S,e,30,False);e['population_after']=count(S)
        entry['decision']='windup / one strike';entry['event']=e['id']
    else:
        # Approach on a walkable path to an exterior bearing. Stop for new input
        # after at most 9 seconds; does not obtain the target's later position.
        exterior=sp.exit_point(target);pts=sp.path(a['xy'],exterior);advance=min(sp.length(pts),13.5,max(2,distance-pw['range_m']*.75));to=sp.along(pts,advance)
        duration=set_actor_motion(S,'Blood',to,1.5,'approach '+chosen['density_band']+' living-blood concentration');a['ready']=now+duration;a['mode']='heavy approach';entry['decision']='approach';entry['path']=a['motion'];
    S['actor_plans'].append(entry);return entry

def bone_signals(S):
    b=actor_pos(S,'Bone');out=[]
    for gid,g in S['groups'].items():
        if not alive(S,gid):continue
        q=pos(S,g);d=sp.dist(b,q);visible=not g.get('building') and d<36 and sp.sight(b,q)
        bell_sound=g['profile']=='caretaker' and S['bell_started'] and not g.get('motion') and sp.dist(q,[23.5,86.1])<1
        sound=(g.get('noise_until',0)>S['time'] and d<27) or (bell_sound and d<45)
        if not (visible or sound):continue
        stimulus='moving person' if g.get('motion') else 'watcher / arrested movement'
        if g['profile']=='entrance_guard':stimulus='guard in direct sight'
        elif g['profile'] in ['family','M05']:stimulus='protective gesture'
        elif bell_sound:stimulus='continuing ordinary bell pulls at the entrance'
        elif sound:stimulus=g.get('noise_kind','local voice / door movement')
        score=(2 if g.get('motion') else 0)+(3 if sound else 0)+(2 if g['profile'] in ['family','M05'] else 0)-d*.04
        out.append({'group':gid,'xy':q,'distance':d,'stimulus':stimulus,'visible':visible,'score':score})
    return out

def plan_bone(S):
    a=S['actors']['Bone'];now=S['time']
    if now<a['ready']-.001:return {'actor':'Bone','continues':a['mode'],'until':a['ready']}
    a['xy']=actor_pos(S,'Bone');a['motion']=None;signals=bone_signals(S);guard=next(g for g in S['groups'].values() if g['profile']=='entrance_guard')
    recognized=next((x for x in signals if x['group']==guard['id'] and x['visible']),None)
    if recognized and a['recognition'] is None:
        a['recognition']={'time':now,'guard':guard['id'],'xy':recognized['xy']};a['guard_stage']=1
        e=event(S,'Bone','guard recognition',a['xy'],'Bone recognizes the entrance guard who killed the son. He deliberately reveals himself and withholds the available precise kill.',target_group=guard['id'],attention_trigger='direct sight of the recognized guard',dialogue_opportunity='fragmented child/Witch memory only; no finished lines')
        seal_event(S,e);a['ready']=now+9;a['mode']='prolonged recognition / observe guard';return {'actor':'Bone','decision':'recognize and observe, do not kill','event':e['id'],'signals':signals}
    if a['recognition'] and alive(S,guard['id']) and a['guard_stage']<6:
        q=pos(S,guard);stage=a['guard_stage'];elapsed=now-a['recognition']['time']
        # Tracking requires a seen retreat or a recent noisy physical cue.
        recent=recognized or (guard.get('motion') and now-guard['motion']['start']<25)
        if recent:
            target=sp.exit_point([q[0]+(-3 if stage%2 else 3),q[1]-2]);duration=set_actor_motion(S,'Bone',target,6.,'follow recognized guard retreat / change angle')
            action_time=max(now+max(duration,1),a['recognition']['time']+48 if stage>=5 else now)
            a['mode']='recognized guard fixation';a['ready']=max(now+max(duration,7 if stage<4 else 9),action_time+2)
            S['pending'].append({'time':action_time,'kind':'bone_guard','group':guard['id'],'stage':stage,'elapsed_at_decision':elapsed})
            if stage<5:a['guard_stage']+=1
            return {'actor':'Bone','decision':'change angle / prolong guard confrontation','attention_trigger':'recognized guard retreat, fear and protective actions','stage':stage,'path':a['motion'],'signals':signals,'held_observation_until':action_time}
    if now==90:
        a['ready']=94.;a['mode']='M05 sustained torment'
        S['pending'].append({'time':92.,'kind':'bone_threat','group':next(g['id'] for g in S['groups'].values() if g['micro']=='M05'),'why':'blackout makes the parent tighten their protective hold; Bone chooses the coop board beside them rather than either person'})
        return {'actor':'Bone','decision':'continue M05 torment; exact object hit','attention_trigger':'existing parent/child protective movement','until':94.}
    recent_targets=a['last_targets'][-2:];options=[x for x in signals if x['group'] not in recent_targets]
    if not options:options=signals
    if options:
        chosen=max(options,key=lambda x:x['score']);gid=chosen['group'];q=chosen['xy'];g=gp(S,gid)
        if g['profile']=='entrance_guard' and not a['recognition']: # sound alone cannot recognize identity
            action='observe'
        elif a.get('interest')==gid and a.get('interest_visits',0)>=1 and sp.dist(a['xy'],q)<12:
            action='kill'
        else:
            # Attention changes, deliberate misses and long observation are
            # tied to stimuli, not a kill quota or house-clearing iterator.
            action='threat' if chosen['stimulus'] in ['protective gesture','door/shutter'] else ('observe' if g.get('building') or not g.get('motion') else 'stalk')
        if action=='kill' and g['profile']=='entrance_guard':action='observe'
        a['interest_visits']=a.get('interest_visits',0)+1 if a.get('interest')==gid else 1;a['interest']=gid
        to=sp.exit_point([q[0]-3,q[1]+2]);duration=set_actor_motion(S,'Bone',to,6.5,chosen['stimulus']);hold=6 if action=='stalk' else 10
        a['ready']=now+max(duration,2)+hold;a['mode']=action+' '+gid;a['last_targets'].append(gid)
        S['pending'].append({'time':now+max(duration,1),'kind':'bone_'+('kill' if action=='kill' else 'threat' if action=='threat' else 'observe'),'group':gid,'why':chosen['stimulus']})
        rec={'actor':'Bone','decision':action,'attention_trigger':chosen['stimulus'],'target_group':gid,'path':a['motion'],'signals':signals};S['actor_plans'].append(rec);return rec
    # Unidentified public sound can attract him to investigate a location,
    # never furnish exact occupants/guard identities.
    visited=a.setdefault('investigated_sounds',[])
    cues=[e for e in S['events'] if e['id'] not in visited and e['time']>now-35 and e['kind'] in ['bell','blood strike'] and sp.dist(a['xy'],e['xy'])<100]
    caretaker=next(g for g in S['groups'].values() if g['profile']=='caretaker')
    if S['bell_started'] and alive(S,caretaker['id']) and not caretaker.get('motion') and sp.dist(pos(S,caretaker),[23.5,86.1])<1 and 'continuing bell' not in visited and sp.dist(a['xy'],[23.5,86.1])<100:
        cues.append({'id':'continuing bell','xy':[23.5,84.4],'kind':'continuing emergency bell'})
    if cues:
        cue=cues[-1];visited.append(cue['id']);q=sp.exit_point(cue['xy']);duration=set_actor_motion(S,'Bone',q,7.,'investigate personally heard '+cue['kind']);a['ready']=now+duration+5;a['mode']='sound investigation';return {'actor':'Bone','decision':'investigate sound, not known population','attention_trigger':cue['id'],'path':a['motion']}
    a['ready']=now+11;a['mode']='still vantage / loses interest';return {'actor':'Bone','decision':'observe; no new locally meaningful stimulus','signals':[]}

def move_group(S,g,target,why,speed=None,building=None,purpose=None):
    if not alive(S,g['id']):return
    start=pos(S,g);old=g.get('motion')
    if old and sp.dist(old['target'],target)<1 and old['purpose']==purpose:return
    if old:old['actual_end']=S['time'];old['actual_end_xy']=start;old['interruption']=why
    injured=any(p['injured'] for p in alive(S,g['id']));speed=speed or (.6 if injured else 1.45 if g['profile'] in ['family','M05'] else 1.9)
    pts=sp.path(start,target,g.get('building'),building);duration=sp.length(pts)/speed
    mid=f'V2M{len(S["movements"])+1:04d}'
    m={'id':mid,'group':g['id'],'members':[p['id'] for p in alive(S,g['id'])],'start':S['time'],'end':S['time']+duration,'path':pts,'speed':speed,'target':target,'destination_building':building,'purpose':purpose,'why':why,'source_building':g.get('building')}
    g['xy']=start;g['motion']=m;g['building']=None;g['intention']=why;g['last_reaction']=S['time'];g['noise_until']=S['time']+min(6,duration);g['noise_kind']='footsteps / calling';S['movements'].append(m)

def shelter(S,g,building,why):
    if g.get('building')==building:g['intention']=why;return
    move_group(S,g,sp.centre(building),why,building=building,purpose='shelter')

def choose_refuge(S,g,threat=None):
    # Familiar nearby choices only; no planner lookup of refuge occupancy or
    # the attacker's next target. Church/estate may be attractive authority.
    q=pos(S,g);known=[g.get('home'),'Church','Tavern','UpperCottage','RearCottage','Farmstead_West' if q[0]>0 else 'Farmstead_South']
    opts=[]
    for k in dict.fromkeys(x for x in known if x):
        p=sp.centre(k);d=sp.dist(q,p)
        if d>75:continue
        avoid=0 if threat is None else max(0,30-sp.dist(p,threat))*2
        if threat and sp.dist(p,threat)<9:continue
        opts.append((d+avoid-(7 if k==g.get('home') else 0),k))
    return min(opts)[1] if opts else None

def warnings(S):
    # Speech is short-range and has a real recipient at current positions.
    living=[g for g in S['groups'].values() if alive(S,g['id'])]
    for g in living:
        if not g.get('noise_until',0)>S['time']:continue
        for h in living:
            if g['id']==h['id'] or sp.dist(pos(S,g),pos(S,h))>7:continue
            if g.get('building')!=h.get('building') and not sp.sight(pos(S,g),pos(S,h),ignore=[x for x in [g.get('building'),h.get('building')] if x]):continue
            k=g['knowledge'];bar=k['barrier_stage']>=4 or 'reported' in k['barrier_evidence']
            if bar and 'reactive' not in h['knowledge']['barrier_evidence']:
                learn(S,h['id'],'barrier','reported lethal reactive boundary; not personally witnessed',g['id'],'reported');h['last_warning_time']=S['time']
            for name in ['Blood','Bone']:
                if k[name].startswith('direct') and not h['knowledge'][name].startswith(('direct','reported')):learn(S,h['id'],name,'reported '+k[name],g['id'],'reported')

def react(S):
    now=S['time'];decisions=[];warnings(S)
    for gid,g in S['groups'].items():
        if not alive(S,gid):continue
        if g.get('building'):
            nearby=[h['id'] for h in S['groups'].values() if alive(S,h['id']) and h.get('building')==g['building']]
            known={r.get('group') for r in g['knowledge']['family']}
            for other in nearby:
                if other not in known:g['knowledge']['family'].append({'time':now,'group':other,'status':'seen alive in same household/refuge; association does not invent kinship'})
    for gid,g in list(S['groups'].items()):
        people=alive(S,gid)
        if not people:continue
        q=pos(S,g);profile=g['profile'];initial=not g['reacted'];g['reacted']=True
        if profile=='mayor':
            g['intention']='remains within his own mansion; demands a local explanation' if S['mayor_state'].startswith('alive') else S['mayor_state'];continue
        if S['mayor_state']=='secured by Witch' and g.get('building')=='MayorHall':
            g['intention']='recoils from the personal confrontation; no escape outcome assigned';continue
        # Continuous motion already committed by a previous reaction does not
        # need to be reselected at every review boundary.
        latest=g.get('last_threat');fresh=latest and latest['time']>g.get('handled_threat',-1)
        barbad='reactive' in g['knowledge']['barrier_evidence']
        if barbad and g.get('motion') and g['motion']['purpose']=='boundary':
            m=g['motion'];m['actual_end']=now;m['actual_end_xy']=q;m['interruption']='local reactive-boundary knowledge';g['motion']=None;g['xy']=q
            safe=choose_refuge(S,g,latest['xy'] if latest else None)
            if safe:shelter(S,g,safe,'turns back after local boundary evidence; seeks familiar cover')
            continue
        if profile=='caretaker' and initial:
            move_group(S,g,[23.5,86.1],'moves to accessible bell rope to signal a public emergency',speed=1.25,building='Church',purpose='bell');continue
        if profile=='entrance_guard':
            if S['actors']['Bone']['recognition'] and now>=S['actors']['Bone']['recognition']['time']:
                if fresh:
                    g['handled_threat']=latest['time'];g['noise_until']=now+8;g['noise_kind']='guard shout / protective gesture'
                    # Knows local uphill way from his ordinary post. Fear and
                    # recognition push successive retreats, not a fixed route.
                    target=sp.DOORS['MayorHall'] if q[1]>112 else [-4,100]
                    move_group(S,g,target,'recognized guard retreats uphill, tries to keep Bone away from nearby people',speed=1.8,purpose='guard retreat')
                continue
            if initial:g['intention']='holds ordinary entrance post and calls to service side';g['noise_until']=now+5;continue
            if S['bell_started'] and not g.get('investigated'):
                g['investigated']=True;move_group(S,g,[18,80],'bell confirms public emergency; entrance guard descends toward callers at the upper junction',speed=1.55,purpose='investigate');continue
        if profile=='service_guard':
            if initial:move_group(S,g,sp.DOORS['MayorHall'],'service guard carries his own enclosure observation to the house',speed=1.6,purpose='report');continue
            if not g.get('motion') and not g.get('service_report'):
                g['service_report']=now;g['noise_until']=now+6;g['intention']='reports strange enclosing wall; does not know barrier attack behaviour';continue
            if g.get('service_report') and now-g['service_report']>12 and not g.get('escorting'):
                g['escorting']=True;move_group(S,g,[-15,130],'returns to service access to organize staff and incoming cart',speed=1.5,purpose='service');continue
        if profile=='house_guard' and initial:g['intention']='guards house threshold and listens for service guard report';g['noise_until']=now+5;continue
        if profile=='delivery' and initial:move_group(S,g,[-14,130],'cart crew takes enclosure concern and provisions to estate service access',speed=1.,purpose='delivery');continue
        if profile=='stable' and initial:g['intention']='settles frightened animals and calls to incoming cart';g['noise_until']=now+15;g['noise_kind']='animals / stable gate';continue
        if profile=='estate_staff' and initial:g['intention']='stays with household work interrupted; listens to reports';continue
        if profile in ['house_guard','service_guard','stable','estate_staff','delivery'] and not fresh:continue
        # A direct imminent threat can interrupt a prior intention.
        if fresh:
            g['handled_threat']=latest['time'];d=sp.dist(q,latest['xy']);kind=latest['kind'];actor=latest['actor']
            if profile=='M05' and actor=='Bone':
                if now<105:g['intention']='parent holds child still at coop, knowing Bone is watching';continue
            if actor=='Barrier':
                g['noise_until']=now+12;safe=choose_refuge(S,g,latest['xy'])
                if safe:shelter(S,g,safe,'witnessed boundary strike; retreats to shelter and warns within earshot')
                elif q[1]<-85:shelter(S,g,'Farmstead_West' if q[0]>=0 else 'Farmstead_South','turns back along the familiar farmland approach after boundary strike; no nearby safe shelter is known')
                else:
                    toward=np.array(sp.RIM.centroid.coords[0])-np.array(q);toward/=np.linalg.norm(toward) or 1
                    move_group(S,g,(np.array(q)+toward*8).tolist(),'recoils into clearing from lethal contact while searching for a familiar way',speed=1.7,purpose='recoil')
                continue
            if (actor in ['Blood','Bone'] and d<35) or (actor=='unknown' and d<24):
                g['noise_until']=now+5
                if g.get('building') and kind=='visible windup':
                    # Only people who actually see/hear immediately adjacent
                    # gathering may attempt an exit; not every hidden group.
                    if g['trait'] in [0,1]:g['intention']='keeps quiet behind closed door despite adjacent disturbance';continue
                safe=choose_refuge(S,g,latest['xy'])
                if safe and safe!=g.get('building'):
                    shelter(S,g,safe,'surviving child seeks household cover after the parent is struck' if profile=='M05' and len(people)==1 else 'leaves locally threatened position for familiar cover; no knowledge of later target');g['refuge_attempts']+=1;continue
                if not g.get('building'):
                    v=np.array(q)-np.array(latest['xy']);v=v/(np.linalg.norm(v) or 1);target=(np.array(q)+v*8).tolist()
                    if sp.RIM.contains(Point(target)):move_group(S,g,sp.exit_point(target),'short recoil from directly witnessed threat',speed=1.45 if profile in ['family','M05'] else 2.4,purpose='recoil');continue
        if g.get('motion'):continue
        if initial:
            if profile=='M05':g['intention']='stays behind coop with child as Bone watches';continue
            if profile=='M04':shelter(S,g,g['home'],'water carriers seek their familiar home after Bone left');continue
            if profile=='smith':g['intention']='smith calls across work yard, apprentice reaches for a shutter';g['noise_until']=now+6;g['noise_kind']='shutter / metal clatter';continue
            if profile=='injured':g['intention']='calls for help near interrupted stall; cannot move safely alone';g['noise_until']=now+12;continue
            if profile=='helper':
                injured_groups=[h for h in S['groups'].values() if any(p['injured'] for p in alive(S,h['id'])) and sp.dist(q,pos(S,h))<22]
                if injured_groups:
                    h=min(injured_groups,key=lambda h:sp.dist(q,pos(S,h)));move_group(S,g,pos(S,h),'tries to support the locally visible injured stall users',speed=1.65,purpose='help');g['help_group']=h['id'];continue
            if profile=='forest':move_group(S,g,sp.nearest_rim(q,[-1,0]),'tests familiar forest working trail beyond the observed sheet',speed=1.65,purpose='boundary');continue
            if profile=='edge':move_group(S,g,sp.nearest_rim(q,[1,0]),'tries nearby woodland exit after blackout; boundary behaviour unknown',speed=1.8,purpose='boundary');continue
            if profile=='escape':
                direction=[0,-1] if q[1]<30 else [-1,0];move_group(S,g,sp.nearest_rim(q,direction),'tries the known approach or nearby clearing exit, not knowing contact is lethal',speed=2.15,purpose='boundary');continue
            if profile=='authority':move_group(S,g,[18,80],'seeks help toward church and the road to the Mayor',speed=1.7,purpose='authority');continue
            if profile=='farm':
                if 'remaining field' in g['role'] or 'middle-strip' in g['role']:
                    move_group(S,g,sp.nearest_rim(q,[-1,0] if q[0]<0 else [1,0]),'field workers try the near field edge toward woodland',speed=1.7,purpose='boundary')
                elif not g.get('building'):shelter(S,g,g['home'],'farm workers return to their household to find family and understand darkness')
                else:g['intention']='farmhouse household draws together at home; distant emergency has no identified local attacker'
                continue
            if profile=='tavern':
                if not g.get('building'):shelter(S,g,'Tavern','tavern workers/customers draw inside together after nearby violence')
                else:g['intention']='customers pause conversation and shelter together behind tavern walls'
                continue
            if g.get('home') and not g.get('building'):shelter(S,g,g['home'],'returns to household/family rather than unexplained darkness');continue
            g['intention']='household stays together inside and listens; exact threat unknown'
        # Later decisions need a new local cue or completion of prior task.
        if g.get('help_group') and not g.get('motion') and not g.get('helped'):
            h=gp(S,g['help_group']);remaining=alive(S,h['id']);g['helped']=True
            if remaining and sp.dist(q,pos(S,h))<3:
                refuge=choose_refuge(S,g,actor_pos(S,'Blood'))
                if refuge:
                    shelter(S,g,refuge,'supports injured neighbour toward nearby cover')
                    move_group(S,h,sp.centre(refuge),'accepts help toward cover with injured companions',speed=.6,building=refuge,purpose='supported retreat')
            continue
        if profile=='smith' and now>97 and not g.get('left_work'):
            g['left_work']=True;shelter(S,g,'WeaverCottage','shuts work yard and heads toward household after no useful reply');continue
        if profile=='M05' and now>105 and S['actors']['Bone'].get('interest')!=gid and sp.dist(actor_pos(S,'Bone'),q)>10:
            shelter(S,g,'Cottage_04','surviving child uses Bone looking away to reach the household' if len(people)==1 else 'parent uses Bone looking away to reach the family household');continue
        if profile=='household' and g.get('building') and S['bell_started'] and now>112 and not g.get('bell_response'):
            g['bell_response']=True
            if g['trait']==4 and g['cohort'] in ['P10','P11','P12']:
                shelter(S,g,'Church','household chooses public church shelter after emergency bell; no promise of safety')
        decisions.append({'group':gid,'position':pos(S,g),'intention':g['intention'],'knowledge':copy.deepcopy(g['knowledge'])})
    # Civilians may appeal to a familiar calm neighbour. No guilty knowledge
    # is bestowed merely because the planner knows who she is.
    w=actor_pos(S,'Witch')
    for gid,g in S['groups'].items():
        if not alive(S,gid) or g.get('building') or g.get('witch_appealed') or sp.dist(pos(S,g),w)>5:continue
        if g['profile'] in ['mayor','entrance_guard']:continue
        g['witch_appealed']=True;learn(S,gid,'Witch','called to familiar calm woman; ignored, no explanation of responsibility','direct proximity','direct')
        e=event(S,'Witch','Witch ignored appeal',w,'A nearby villager calls to the Witch; she keeps walking without helping or explaining.',civilian_group=gid);e['population_after']=count(S);S['seeds'].append({'event':e['id'],'time':now,'xy':w,'seed':e['description'],'production_state':'dialogue intention only, no written lines'})
    return decisions

def blood_strike(S,item):
    a=S['actors']['Blood'];q=actor_pos(S,'Blood');target=item['target'];pw=power(S);v=np.array(target)-np.array(q);v/=np.linalg.norm(v) or 1;n=np.array([-v[1],v[0]])
    length=pw['range_m'];width=pw['width_m'];pts=[(np.array(q)-n*width*.22).tolist(),(np.array(q)+v*length-n*width*.5).tolist(),(np.array(q)+v*length+n*width*.5).tolist(),(np.array(q)+n*width*.22).tolist()];foot=Polygon(pts)
    e=event(S,'Blood','blood strike',q,'One deliberate pressure surge follows the selected physical concentration. Existing nearby blood is available for reuse; the force envelope is a planning requirement.',aim=target,footprint=mapping(foot),power=pw,selection_time=item['selection']['decision_time'])
    structural=[]
    for pid,p in S['people'].items():
        if not p['alive']:continue
        pp=member_pos(S,p);point=Point(pp)
        if not foot.covers(point):continue
        g=gp(S,p['group']);building=g.get('building');d=sp.dist(q,pp);pressure=pw['pressure']*(1-.30*d/length)
        attenuation=.80 if building=='Church' else .60 if building=='MayorHall' else .48 if building else 0
        barriers=[k for k,r in sp.ROOFS.items() if k!=building and LineString([q,pp]).intersection(r).length>1]
        pressure-=attenuation+min(1.4,.5*len(barriers))
        exposure={'pressure':round(pressure,3),'building_cover':building,'intervening_structures':barriers,'distance':round(d,2),'source_envelope':e['id']}
        if pressure>=1.25:kill(S,p,e,exposure)
        elif pressure>=.7:injure(S,p,e,exposure)
    for k,r in sp.ROOFS.items():
        if foot.intersection(r).area>.4 and pw['pressure']>1.6:structural.append({'feature':k,'intersected_area_m2':round(foot.intersection(r).area,2),'requirement':'local impacted wall/roof bay failure; not automatic whole-house demolition'})
    e['structural_requirements']=structural
    w=actor_pos(S,'Witch')
    if foot.covers(Point(w)):
        e['witch_intersection']={'xy':w,'effect':'supernatural blood splits/melds around Witch, continues beyond; no dodge or injury'}
        for gid,g in S['groups'].items():
            if alive(S,gid) and not g.get('building') and sp.dist(pos(S,g),w)<24 and sp.sight(pos(S,g),w):learn(S,gid,'Witch','saw wave part around the walking woman; responsibility is an inference, not automatic certainty',e['id'],'direct')
    seal_event(S,e,True,38);a['ready']=S['time']+7;a['mode']='recover pressure / sample changed local field'

def process_bone(S,item):
    gid=item['group'];people=alive(S,gid);a=S['actors']['Bone'];b=actor_pos(S,'Bone')
    if not people:return
    g=gp(S,gid);q=pos(S,g);d=sp.dist(b,q);kind=item['kind']
    if kind=='bone_guard':
        stage=item['stage'];elapsed=S['time']-a['recognition']['time'];intendkill=stage>=5 and elapsed>=42
        if intendkill and d<=12:
            e=event(S,'Bone','son-killer guard final strike',q,'After sustained recognition, threats and allowed retreats, Bone deliberately kills the entrance guard with one precise intended hit.',target_group=gid,attention_trigger='recognized guard, prolonged personal encounter concludes',recognition_elapsed_s=elapsed)
            kill(S,people[0],e,{'exact_intended_hit':True,'range_m':d});seal_event(S,e);a['guard_stage']=6;return
        e=event(S,'Bone','guard torment',q,'Bone chooses an object beside the recognized guard, allows another retreat and makes his personal recognition increasingly apparent.',target_group=gid,attention_trigger='recognized guard fear/protective retreat',stage=stage,recognition_elapsed_s=elapsed,dialogue_opportunity='broken child/Witch memory fragments, no finished exposition')
        seal_event(S,e);return
    if kind=='bone_kill' and d<=12:
        e=event(S,'Bone','precise attack',q,'Bone concludes this attention encounter with a deliberate precise hit, not a systematic clearance.',attention_trigger=item['why'],target_group=gid)
        kill(S,people[0],e,{'exact_intended_hit':True,'range_m':d});seal_event(S,e);return
    if kind=='bone_threat' and d<=15:
        e=event(S,'Bone','deliberate object strike',[q[0]+1.1,q[1]-.7],'An exact intended hit on adjacent board/ground. The apparent near-miss deliberately leaves the person alive.',attention_trigger=item['why'],target_group=gid);seal_event(S,e);return
    e=event(S,'Bone','observation / stalking',b,'Bone watches, follows the visible movement or loses the original angle; no off-screen hit is assumed.',attention_trigger=item['why'],target_group=gid,range_m=d);receive(S,e,17,False);e['population_after']=count(S)

def complete_motions(S):
    now=S['time']
    for gid,g in S['groups'].items():
        m=g.get('motion')
        if not m or m['end']>now+.00001:continue
        g['xy']=m['target'];g['motion']=None;g['building']=m['destination_building'];m['actual_end']=now;m['actual_end_xy']=g['xy'];m['interruption']=None
        if not alive(S,gid):continue
        if m['purpose']=='boundary':
            if 'reactive' in g['knowledge']['barrier_evidence']:
                g['intention']='halts before deliberate contact after local warning';continue
            e=event(S,'Barrier','reactive contact',g['xy'],'The leading villager physically tests the opaque boundary on a locally chosen escape attempt. The boundary reacts only at that contact.',contact_groups=[gid],attempt=m['why'],movement=m['id'])
            g['knowledge']['barrier_stage']=3;people=alive(S,gid);kill(S,people[0],e,{'physical_contact':True,'rim_distance_m':sp.RIM.boundary.distance(Point(g['xy']))});seal_event(S,e,False,25)
        elif m['purpose']=='bell' and not S['bell_started']:
            S['pending'].append({'time':now+2.,'kind':'bell','group':gid});g['intention']='grasps accessible ordinary ground-floor bell rope'
        elif m['purpose']=='shelter':g['noise_until']=now+4;g['noise_kind']='door/shutter';g['intention']='inside chosen refuge / household; tries to close entrance and quiet companions'
        elif m['purpose']=='authority':g['noise_until']=now+10;g['noise_kind']='calls for help / asks about guards';g['intention']='calls at upper junction for church or guard assistance'
    for name in ['Blood','Bone']:
        a=S['actors'][name];m=a.get('motion')
        if m and m['end']<=now+.00001:a['xy']=m['path'][-1];m['actual_end']=m['end'];a['motion']=None

def advance_resources(S,t):
    old=S['time'];dt=t-old
    for p in alive(S):
        if p['injured'] and not p['injury_treated'] and p['blood_generated']<.65:add_source(S,p['id'],member_pos(S,p,(old+t)/2),min(.006*dt,.65-p['blood_generated']),t,'ongoing bleeding')
    pw=power(S,t);a=S['actors']['Blood'];capacity=8+18*pw['saturation'];available=max(0,capacity-a['carry']);budget=min(available,dt*1.2)
    # Moving blood conservation: transfer volume from a nearby real source,
    # never count it simultaneously in the puddle and carried volume.
    for r in sorted(S['resource_sources'],key=lambda r:sp.dist(actor_pos(S,'Blood',t),r['xy'])):
        if budget<=1e-6:break
        if r['created']>t or r['remaining']<=1e-6 or sp.dist(actor_pos(S,'Blood',t),r['xy'])>pw['control_m']:continue
        take=min(r['remaining'],budget);r['remaining']-=take;a['carry']+=take;budget-=take
        S['resource_draws'].append({'time':t,'source':r['id'],'amount':take,'from':r['xy'],'to':actor_pos(S,'Blood',t),'distance_m':sp.dist(actor_pos(S,'Blood',t),r['xy']),'control_m':pw['control_m']})

def advance(S):
    now=S['time'];due=[now+8,S['witch_route']['terminal']]
    if S['witch_route']['arrival']>now+.0001:due.append(S['witch_route']['arrival'])
    due += [x['time'] for x in S['pending'] if x['time']>now+.0001]
    due += [g['motion']['end'] for g in S['groups'].values() if g.get('motion') and g['motion']['end']>now+.0001 and alive(S,g['id'])]
    due += [a['ready'] for a in S['actors'].values() if a['ready']>now+.0001]
    t=min(due);advance_resources(S,t);S['time']=t;complete_motions(S)
    process=[x for x in S['pending'] if x['time']<=t+.00001];S['pending']=[x for x in S['pending'] if x['time']>t+.00001]
    for item in sorted(process,key=lambda x:x['time']):
        if item['kind']=='blood_strike':blood_strike(S,item)
        elif item['kind'].startswith('bone_'):process_bone(S,item)
        elif item['kind']=='bell' and alive(S,item['group']):
            S['bell_started']=True;S['bell_time']=t;e=event(S,'Civilian','bell',[23.5,86.1],'Caretaker starts repeated ordinary bell pulls after reaching the ground-floor rope, continuing until interrupted or leaving the rope. Signal means PUBLIC EMERGENCY only.',group=item['group']);e['population_after']=count(S)
            for gid,g in S['groups'].items():
                if alive(S,gid) and sp.dist(pos(S,g),e['xy'])<250:learn(S,gid,'sound','public emergency bell; no attacker, location, barrier rule or safe-route information',e['id'],'heard')
    if abs(t-S['witch_route']['arrival'])<.0001:
        S['mayor_state']='secured by Witch';e=event(S,'Witch','Witch secures Mayor',[2,146],'Witch reaches the Mayor by her own continuous walk and prevents his escape. Begins deliberate approximately one-minute psychological confrontation; exact restraint method reserved.',topics=['she holds him responsible','he hears continuing village emergency','she deliberately saved him for last','rage and imposed helplessness, not remorseful spirit exposition']);e['population_after']=count(S)
    if abs(t-S['witch_route']['terminal'])<.0001:
        p=next(p for p in alive(S) if p['role']=='Mayor');e=event(S,'Witch','Mayor final death',[2,146],'At the end of the fixed sixty-second confrontation, Witch personally kills Mayor. Exact cinematic method remains unauthored. No survivor census informed her timing.')
        kill(S,p,e,{'personal_terminal_event':True,'confrontation_s':60});seal_event(S,e,False,12);S['mayor_state']='killed personally by Witch; primary event ended';S['closed']=True
    S['power_history'].append(power(S));S['snapshots'].append(state_snapshot(S))

def save(S):dump(STATE,S)
def inspect(S):
    b=S['actors']['Bone'];guard=next(g for g in S['groups'].values() if g['profile']=='entrance_guard')
    return {'time':round(S['time'],3),'population':count(S),'actors':{k:actor_pos(S,k) for k in ['Blood','Bone','Witch']},'blood':{k:v for k,v in power(S).items() if k!='source_ids'},'blood_signatures':[{k:v for k,v in x.items() if not k.startswith('audit')} for x in signatures(S)],'bone':{'mode':b['mode'],'recognition':b['recognition'],'guard_stage':b['guard_stage'],'signals':bone_signals(S)},'guard':{'xy':pos(S,guard),'alive':len(alive(S,guard['id'])),'intention':guard['intention']},'last_events':[{k:e[k] for k in ['id','time','actor','kind','description','fatalities']} for e in S['events'][-5:]],'arrival':S['witch_route']['arrival'],'terminal':S['witch_route']['terminal'],'closed':S['closed']}

def step(S):
    if S['closed']:raise RuntimeError('Terminal reached; no further simulation permitted')
    index=S['cycle']+1;start=S['time'];before=state_snapshot(S);e0=len(S['events']);m0=len(S['movements']);k0=len(S['knowledge_ledger']);d0=len(S['resource_draws'])
    action={'cycle':index,'phase':'ACTION','decision_time':start,'input_state':before,'Blood':plan_blood(S),'Bone':plan_bone(S),'Witch':'continuous destination walk or fixed sixty-second confrontation','Barrier':'only pending physical contacts, no inward decisions'}
    dump(OUT/f'v2_C{index:03d}_action.json',action)
    reaction={'cycle':index,'phase':'REACTION','decision_time':start,'input_events':[e['id'] for e in S['events'] if e['time']>=start-.001],'decisions':react(S),'movement_commitments':copy.deepcopy(S['movements'][m0:]),'knowledge_transfers':copy.deepcopy(S['knowledge_ledger'][k0:])}
    advance(S);reaction['resolution_until']=S['time'];reaction['resolved_events']=copy.deepcopy(S['events'][e0:]);reaction['population_after']=count(S)
    dump(OUT/f'v2_C{index:03d}_reaction.json',reaction)
    S['cycles'].append({'id':index,'start':start,'end':S['time'],'events':[e['id'] for e in S['events'][e0:]],'population':count(S),'action_file':f'v2_C{index:03d}_action.json','reaction_file':f'v2_C{index:03d}_reaction.json','new_resource_draws':len(S['resource_draws'])-d0})
    S['cycle']=index;save(S);return inspect(S)

if __name__=='__main__':
    command=sys.argv[1] if len(sys.argv)>1 else 'inspect';S=init() if command=='init' else json.loads(STATE.read_text())
    result=step(S) if command=='step' else inspect(S)
    print(json.dumps(result,ensure_ascii=False,indent=2))
