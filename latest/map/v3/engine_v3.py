"""V3 causal planner. No V1/V2 inputs. Geometry and T90 refinements only.
ACTION observations/decisions precede separately logged REACTION intentions.
Motion and stream fronts advance on a shared one-second clock between events.
This is an authored-rule scenario, not an empirically calibrated crowd model.
"""
from geometry_v3 import *
from collections import Counter
import argparse, hashlib
OUT=ROOT/"run"
def hash01(key):return int(hashlib.sha256(str(key).encode()).hexdigest()[:8],16)/0xffffffff
class Sim:
 def __init__(self,s):self.s=s;self.t=s["t"];self.P=s["people"];self.G=s["groups"]
 def living(self,g):return[p for p in g["members"] if self.P[p]["alive"]]
 def gid(self,p):return next((g for g in self.G.values() if p in g["members"]),None)
 def event(self,kind,actor,p,text,**kw):
  e={"id":f"E{len(self.s['events'])+1:04d}","t":round(self.t,3),"phase":"ACTION","kind":kind,"actor":actor,"xy":list(p),"text":text,**kw}
  self.s["events"].append(e);return e
 def know(self,p,key,value,source,mode="direct"):
  old=self.P[p]["knowledge"].get(key)
  if old==value:return
  self.P[p]["knowledge"][key]=value
  self.s["knowledge_ledger"].append({"t":round(self.t,3),"person":p,"field":key,"old":old,"new":value,"source":source,"mode":mode})
 def witnesses(self,p,r=24,shelter=None):
  return [pid for pid,q in self.P.items() if q["alive"] and dist(p,q["xy"])<=r and
    ((shelter and q["shelter"]==shelter) or (q["shelter"] is None and visible(p,q["xy"])))]
 def alert(self,e,r=35):
  for g in self.G.values():
   ids=self.living(g)
   if not ids:continue
   d=dist(g["xy"],e["xy"])
   if d>r:continue
   inside=g["shelter"]
   seen=(not inside and visible(g["xy"],e["xy"])) or e.get("shelter")==inside and inside
   if not seen and d>r*.65:continue
   if e["id"] not in g["events_seen"]:g["alarm"]={"kind":e["kind"],"xy":e["xy"],"event":e["id"],"t":self.t,"seen":bool(seen)}
   if e["id"] not in g["events_seen"]:
    g["events_seen"].append(e["id"]);g["decision_due"]=min(g["decision_due"],self.t+(3 if seen else 7))
   if e["actor"] in ["Blood","Bone"]:
    for pid in ids:
     self.know(pid,e["actor"],("direct: " if seen else "heard: ")+e["text"][:95],e["id"],"direct" if seen else "heard")
 def casualty(self,pid,attacker,cause,exposure,death=True,witnesses=None):
  p=self.P[pid]
  if not p["alive"]:return
  if pid==self.s["mayor_id"] and attacker!="Witch":raise RuntimeError("Mayor casualty contradiction")
  if not death and p["injured"]:return
  w=witnesses if witnesses is not None else self.witnesses(p["xy"],22,p["shelter"])
  if pid in w:w.remove(pid)
  was=p["injured"];units=(.78 if was else 1) if death else .22
  c={"id":f"K{len(self.s['casualties'])+1:03d}","person":pid,"t":round(self.t,3),"xy":p["xy"][:],"type":"death" if death else "injury",
   "intention":p["intention"],"attacker":attacker,"cause":cause,"exposure":exposure,"witnesses":w,
   "knowledge_change":f"Only listed direct witnesses receive {attacker} event knowledge; subsequent warnings are separate.","blood_units":units,"source_history":False}
  self.s["casualties"].append(c)
  self.s["sources"].append({"id":c["id"],"person":pid,"xy":p["xy"][:],"t":self.t,"units":units,"collected":False})
  if death:p["alive"]=False;p["death"]={"t":self.t,"attacker":attacker}
  else:p["injured"]=True;p["injury_time"]=self.t
  for wpid in w:
   if attacker=="Barrier":self.know(wpid,"barrier",4,c["id"])
   else:self.know(wpid,attacker,"direct: "+cause,c["id"])
  return c
 def move(self,g,destination,intention,kind="flee",shelter=None,endpoint=None):
  ids=self.living(g)
  if not ids:return
  start=g["xy"][:]
  # Every indoor departure crosses an estimated doorway before open-ground routing.
  pre=[]
  if g["shelter"]:
   h=g["shelter"];side="rear" if kind=="flee" else "front"
   pre=[start,DOORS[h][side]]
  ground=path(pre[-1] if pre else start,destination)
  ps=pre+ground if pre else ground
  speed=.65 if any(self.P[p]["injured"] for p in ids) else 2.3 if kind=="flee" else 1.25
  if any("child" in self.P[p]["role"] for p in ids):speed=min(speed,1.5)
  g["shelter"]=None;g["intention"]=intention
  g["motion"]={"path":ps,"travel":0,"speed":speed,"shelter_end":shelter,"endpoint":endpoint,"start":self.t}
  g["decision_due"]=self.t+length(ps)/speed+3
  m={"id":f"M{len(self.s['movements'])+1:04d}","start":self.t,"planned_end":self.t+length(ps)/speed,
   "people":ids,"path":ps,"intention":intention,"kind":kind,"destination_shelter":shelter,"group":g["id"],"actual_end":None}
  self.s["movements"].append(m);g["motion"]["record"]=m["id"]
  for p in ids:self.P[p]["shelter"]=None;self.P[p]["intention"]=intention
 def stopmotion(self,g,reason):
  m=g["motion"]
  if m:
   rec=next(x for x in self.s["movements"] if x["id"]==m["record"])
   rec["actual_end"]=self.t;rec["end_xy"]=g["xy"][:];rec["end_reason"]=reason
  g["motion"]=None
 def enter(self,g,h):
  # Entry refusal is fear, never automatically malicious.
  occupants=[q for q in self.G.values() if q["shelter"]==h and self.living(q)]
  if self.s["compromised"].get(h,0)>1 and occupants and g["compromises"]==0:
   g["decision_due"]=self.t+3;g["alarm"]={"kind":"refused_entry","xy":g["xy"],"event":"entry","t":self.t,"seen":True}
   e=self.event("refused_entry","Civilians",g["xy"],"Frightened occupants keep a compromised door shut.",shelter=h,people=self.living(g));e["phase"]="REACTION"
   return
  g["shelter"]=h;g["xy"]=list(center(h));g["plan"]="shelter";g["decision_due"]=self.t+18
  for p in self.living(g):self.P[p]["shelter"]=h;self.P[p]["xy"]=g["xy"][:];self.P[p]["intention"]="shelter and listen"
  for st in self.s["streams"]:
   if st["active"] and st["shelter"]==h and st["threshold_seen"]:self.compromise(g,"blood_stream",st["tip"],st["id"]+"-entry")
 def advance(self,dt):
  self.t+=dt;self.s["t"]=self.t
  for g in list(self.G.values()):
   m=g["motion"]
   if not m or not self.living(g):continue
   m["travel"]+=m["speed"]*dt;g["xy"]=along(m["path"],m["travel"])
   for p in self.living(g):self.P[p]["xy"]=g["xy"][:]
   if m["travel"]>=length(m["path"]):
    target=m["shelter_end"];endpoint=m["endpoint"];self.stopmotion(g,"arrived")
    if "take " in g["intention"]:
     e=self.event("theft_completed","Civilians",g["xy"],g["intention"]+"; portable goods now carried.",people=self.living(g));e["phase"]="REACTION"
     for pid in self.living(g):self.P[pid]["carried_goods"]="stolen portable goods / monopolised supplies"
    if target:self.enter(g,target)
    if endpoint=="barrier":g["contact_due"]=self.t+2;g["intention"]="test apparent edge / push through toward outside"
    if endpoint=="bell":
     if self.s["bell"] is None:
      self.s["bell"]=self.t;e=self.event("bell","Caretaker",g["xy"],"Ground-floor rope: public emergency only.",people=self.living(g));e["phase"]="REACTION"
      for pid,p in self.P.items():
       if p["alive"]:self.know(pid,"bell","heard: public emergency",e["id"],"heard")
     self.enter(g,"Church")
  for name in ["blood","bone"]:
   a=self.s[name];m=a.get("motion")
   if m:
    m["travel"]+=m["speed"]*dt;a["xy"]=along(m["path"],m["travel"])
    if m["travel"]>=length(m["path"]):a["motion"]=None
  w=self.s["witch"];times=w["times"];pts=w["route"]
  if self.t>=times[-1]:w["xyz"]=pts[-1]
  else:
   i=next(i for i in range(len(times)-1) if times[i]<=self.t<times[i+1]);u=(self.t-times[i])/(times[i+1]-times[i])
   w["xyz"]=[pts[i][j]+(pts[i+1][j]-pts[i][j])*u for j in range(3)]
 def actor_move(self,name,target,speed):
  a=self.s[name];ps=path(a["xy"],target);a["motion"]={"path":ps,"travel":0,"speed":speed}
  return ps
 def power(self):
  b=self.s["blood"];r=b["resource"]
  # Resource capacity saturates; rage is an independent modest gain, never a speed boost.
  q=1-math.exp(-r/15);rage=self.t>=self.s["witch"]["arrival"]
  return {"resource":r,"q":q,"rage":rage,"radius":24+50*q+(8 if rage else 0),
    "slots":2+int(6*q)+(1 if rage else 0),"stream_speed":.8+.8*q+(.2 if rage else 0),
    "budget":55+300*q+(75 if rage else 0),"reach":11+19*q+(4 if rage else 0),
    "halfwidth":3.5+5.5*q+(1.5 if rage else 0),
    "label":"AWAKENED" if r<2 else "FED" if r<10 else "SATURATED" if r<25 else "DELUGE"}
 def resource(self):
  b=self.s["blood"];pw=self.power()
  for src in self.s["sources"]:
   if src["collected"]:continue
   # Physical collection by the primary mass or an already continuous stream front/trail.
   reach=dist(src["xy"],b["xy"])<8 and visible(src["xy"],b["xy"])
   via=None
   for st in self.s["streams"]:
    if st["active"] and dist(b["xy"],st["root"])<pw["radius"] and LineString(st["realised"]).distance(Point(src["xy"]))<1.2:
     reach=True;via=st["id"];break
   if reach:
    src["collected"]=True;src["collected_t"]=self.t;src["via"]=via or "primary mass"
    before=b["resource"];b["resource"]=min(48,b["resource"]+src["units"])
    self.event("resource","Blood",src["xy"],"Physically accessible spilled blood joins controllable mass.",source=src["id"],via=src["via"],units=src["units"],before=before,after=b["resource"])
 def streams(self,dt):
  b=self.s["blood"];pw=self.power()
  for st in self.s["streams"]:
   if not st["active"]:continue
   if dist(b["xy"],st["root"])+st["travel"]>pw["radius"] or self.t-st["last_response"]>55:
    st["active"]=False;st["end"]=self.t;st["end_reason"]="control distance or weak-response withdrawal";continue
   st["travel"]=min(st["length"],st["travel"]+pw["stream_speed"]*dt);tip=along(st["path"],st["travel"])
   realised=[];remaining=st["travel"]
   for a,c in zip(st["path"],st["path"][1:]):
    realised.append(a)
    d=dist(a,c)
    if remaining<=d:break
    remaining-=d
   realised.append(tip);st["realised"]=realised;st["tip"]=tip
   h=st["shelter"]
   if st["travel"]>=st["threshold_distance"] and not st["threshold_seen"]:
    st["threshold_seen"]=True
    occ=[g for g in self.G.values() if g["shelter"]==h and self.living(g)]
    # Only occupants physically near the floor/door perceive infiltration.
    for g in occ:
     self.compromise(g,"blood_stream",tip,st["id"])
    self.event("stream_threshold","Blood",tip,"Thin blood reaches an estimated threshold; visible infiltration may compromise shelter.",stream=st["id"],shelter=h,affected_groups=[g["id"] for g in occ])
   near=[p for p in self.P.values() if p["alive"] and dist(p["xy"],tip)<3.2 and (p["shelter"]==h or p["shelter"] is None)]
   n=len(near)
   signal="none" if n==0 else "faint" if n==1 else "presence" if n<5 else "dense"
   if n==1 and hash01(near[0]["id"]+h)>.3:signal="none"
   if signal!=st["signal"]:
    st["signal"]=signal
    self.event("stream_response","Blood",tip,"Search response: "+signal+" (coarse cue only).",stream=st["id"],shelter=h)
   if signal in ["presence","dense"]:st["last_response"]=self.t
  active=[s for s in self.s["streams"] if s["active"]]
  if self.t<b.get("next_stream",90) or len(active)>=pw["slots"]:return
  budget=pw["budget"]-sum(s["length"] for s in active)
  # Candidate choice uses geometry and unvisited access, NEVER hidden occupancy.
  candidates=[]
  for h,d in DOORS.items():
   if h=="MayorHall" or self.t-b["visited"].get(h,-1000)<65:continue
   if dist(b["xy"],d["front"])>pw["radius"]*.8:continue
   if any(s["shelter"]==h and s["active"] for s in active):continue
   score=dist(b["xy"],d["front"])+hash01(h)*5
   candidates.append((score,h))
  for _,h in sorted(candidates):
   ground=path(b["xy"],DOORS[h]["front"]);full=ground+[list(center(h))]
   n=length(full)
   if n>pw["radius"] or n>budget:continue
   st={"id":f"S{len(self.s['streams'])+1:03d}","start":self.t,"root":b["xy"][:],"shelter":h,
    "path":full,"length":n,"threshold_distance":length(ground),"travel":0,"tip":b["xy"][:],"realised":[b["xy"][:],b["xy"][:]],
    "active":True,"signal":"none","threshold_seen":False,"last_response":self.t,
    "continuity":"Starts at primary mass; grows along ground path, crosses estimated threshold, then floor. Root remains linked by primary mass movement trail; range withdrawal applies."}
   self.s["streams"].append(st);b["visited"][h]=self.t;b["next_stream"]=self.t+4
   self.event("stream_start","Blood",b["xy"],"New surface search branch toward an untested nearby access.",stream=st["id"],shelter=h);break
 def compromise(self,g,kind,p,event):
  if event in g["events_seen"]:return
  g["events_seen"].append(event);g["compromises"]+=1
  if g["shelter"]:self.s["compromised"][g["shelter"]]=max(self.s["compromised"].get(g["shelter"],0),g["compromises"])
  g["alarm"]={"kind":kind,"xy":list(p),"event":event,"t":self.t,"seen":True}
  g["decision_due"]=min(g["decision_due"],self.t+3)
  for pid in self.living(g):self.know(pid,"shelter","direct: "+kind,event)
 def blood(self):
  b=self.s["blood"];pw=self.power()
  if b["charge"]:
   if self.t<b["charge"]["at"]:return
   target=b["charge"];b["charge"]=None;b["ready"]=self.t+7
   a=np.array(b["xy"]);z=np.array(target["xy"]);v=z-a;d=np.linalg.norm(v);v/=max(d,.01)
   e=self.event("blood_attack","Blood",b["xy"],"Deliberate pressure strike toward the perceived concentration.",target=target["xy"],cue=target["cue"],power=pw,path=[b["xy"][:],list(a+v*min(pw["reach"],d+5))],shelter=target.get("shelter"))
   victims=[]
   for pid,p in self.P.items():
    if not p["alive"]:continue
    rel=np.array(p["xy"])-a;f=float(rel@v);side=abs(float(v[0]*rel[1]-v[1]*rel[0]))
    if f<-.5 or f>pw["reach"] or side>pw["halfwidth"]:continue
    walls=sum(LineString([b["xy"],p["xy"]]).crosses(g.buffer(-.4)) for g in BUILD.values())
    if walls>1:continue
    if walls and pw["q"]<.22:continue
    if pid==self.s["mayor_id"]:raise RuntimeError("Blood corridor reaches Mayor: genuine spatial contradiction")
    # Cover, wave edge and intended line govern exposure; no desired casualty count.
    severity=(1-side/pw["halfwidth"])*(.85+.5*pw["q"])-walls*.25
    if severity<.22:continue
    if severity>=.48:self.casualty(pid,"Blood","pressure strike at physical concentration","direct corridor / light-structure failure",True);victims.append(pid)
    elif not p["injured"]:self.casualty(pid,"Blood","edge of pressure strike","partial cover / corridor margin",False);victims.append(pid)
   e["affected_people"]=victims
   w=self.s["witch"]["xyz"]
   rel=np.array(w[:2])-a
   if 0<float(rel@v)<pw["reach"] and abs(float(v[0]*rel[1]-v[1]*rel[0]))<pw["halfwidth"]:
    self.event("witch_immunity","Witch",w[:2],"Blood divides around the calm Witch and rejoins beyond; she keeps walking.",attack=e["id"])
   self.alert(e,52);self.s["last_major"]=self.t
   for g in self.G.values():
    if self.living(g) and g["shelter"] and dist(g["xy"],target["xy"])<15:self.compromise(g,"nearby pressure / damaged refuge",target["xy"],e["id"])
   return
  if self.t<b["ready"]:return
  cues=[]
  for g in self.G.values():
   ids=self.living(g)
   if not ids or g["shelter"]:continue
   d=dist(b["xy"],g["xy"])
   if d>48 or not visible(b["xy"],g["xy"]):continue
   density=1 if len(ids)==1 else 2 if len(ids)<5 else 4
   # A cluster is a visible spatial pattern, not an exact headcount query.
   moving=bool(g["motion"]);inj=any(self.P[p]["injured"] for p in ids)
   score=density*9+(5 if moving else 0)+(7 if inj else 0)-d*.35
   if score>0:cues.append((score,g["xy"][:],"visible "+("dense " if density==4 else "")+("aid/bleeding" if inj else "human activity"),None))
  for st in self.s["streams"]:
   if not st["active"] or st["signal"] not in ["presence","dense"]:continue
   d=dist(b["xy"],st["tip"])
   score=(38 if st["signal"]=="dense" else 23)-d*.30
   cues.append((score,DOORS[st["shelter"]]["front"],"physical stream "+st["signal"],st["shelter"]))
  if not cues:return
  _,target,cue,h=max(cues,key=lambda c:c[0])
  prior=[e for e in self.s["events"] if e["kind"]=="blood_attack" and e.get("shelter")==h and not e.get("affected_people")]
  blocked=h and sum(LineString([b["xy"],center(h)]).crosses(g.buffer(-.4)) for g in BUILD.values())>1
  # Two unproductive impacts give Blood local evidence that an intervening structure is absorbing pressure.
  reassess=bool(blocked and len(prior)>=2)
  if dist(target,b["xy"])<=pw["reach"]-3 and not reassess:
   b["motion"]=None;b["charge"]={"at":self.t+5,"xy":list(center(h)) if h else target,"cue":cue,"shelter":h}
   self.event("blood_commit","Blood",b["xy"],"Commits to "+cue+"; five-second build-up.",target=target,shelter=h)
  elif not b["motion"] or b.get("target")!=h or dist(target,b["motion"]["path"][-1])>8:
   ps=self.actor_move("blood",target,1.55);b["target"]=h
   self.event("blood_move","Blood",b["xy"],"Flanks the intervening structure after repeated obstructed pressure." if reassess else "Slow approach toward "+cue+".",path=ps,target=target,shelter=h,reassessment=reassess)
 def barrier(self):
  for g in self.G.values():
   if not self.living(g) or g.get("contact_due",1e9)>self.t:continue
   g.pop("contact_due",None)
   ids=self.living(g);lead=ids[0]
   if self.P[lead]["knowledge"]["barrier"]>=4 or self.P[lead]["knowledge"]["barrier_report"]:continue
   e=self.event("barrier_contact","Barrier",g["xy"],"A civilian physically tests the boundary; local reactive strike.",people=ids,prior_barrier=self.P[lead]["knowledge"]["barrier"])
   w=self.witnesses(g["xy"],28)
   self.casualty(lead,"Barrier","contact-reactive boundary strike","deliberate physical push / crossing test",True,w)
   e["victim"]=lead;e["direct_witnesses"]=w
   for p in w:self.know(p,"barrier",4,e["id"])
   for q in self.G.values():
    if self.living(q) and any(p in w for p in q["members"]):
     q["decision_due"]=self.t+2;q["alarm"]={"kind":"barrier_attack","xy":g["xy"],"event":e["id"],"t":self.t,"seen":True}
   self.s["last_major"]=self.t
 def bone(self):
  b=self.s["bone"];guard=self.P[self.s["entrance_guard_id"]]
  if self.t<b["ready"]:return
  if guard["alive"] and not b["guard_recognised"] and guard["shelter"] is None and dist(b["xy"],guard["xy"])<28 and visible(b["xy"],guard["xy"]):
   b["guard_recognised"]=True;b["guard_start"]=self.t;b["guard_stage"]=0;b["focus"]=guard["id"];b["stage"]="guard";b["motion"]=None
   self.event("recognition","Bone",b["xy"],"Locally sees the entrance guard; fragmented recognition changes his attention.",target=guard["id"],target_xy=guard["xy"],dialogue_opportunity="broken child / original confrontation fragments; no final words")
  if b["stage"]=="guard":
   if not guard["alive"]:raise RuntimeError("Son-killer guard died before personal resolution")
   d=dist(b["xy"],guard["xy"])
   if d>11 or not visible(b["xy"],guard["xy"]):
    if not b["motion"]:
     ps=self.actor_move("bone",guard["xy"],8);self.event("bone_burst","Bone",b["xy"],"Repositions to regain the recognised guard's sightline.",path=ps,trigger="guard moved out of sight")
    return
   b["motion"]=None;n=b["guard_stage"];elapsed=self.t-b["guard_start"]
   if n>=5 and elapsed>=40:
    self.casualty(guard["id"],"Bone","deliberate precise final strike after personal torment","recognised guard within acquired line",True)
    e=self.event("guard_final","Bone",guard["xy"],"Kills the recognised entrance guard personally after prolonged, consequential torment.",duration=elapsed,target=guard["id"])
    self.alert(e,28);b["stage"]="idle";b["focus"]=None;b["ready"]=self.t+5;self.s["last_major"]=self.t;return
   # Guard's actual protective effort is locally visible; other people are not staged here.
   protected=[p for p,q in self.P.items() if q["alive"] and p!=guard["id"] and q["shelter"] is None and dist(q["xy"],guard["xy"])<7 and visible(b["xy"],q["xy"])]
   if protected and n in [2,4] and "protect" in guard["intention"]:
    victim=min(protected,key=lambda p:dist(self.P[p]["xy"],guard["xy"]))
    self.casualty(victim,"Bone","precise attack on a person the entrance guard is trying to protect","local protective gesture exploited",n==4)
    e=self.event("guard_protected_person_harmed","Bone",self.P[victim]["xy"],"Spares the guard while harming a person within his protective reach.",target=victim,guard=guard["id"],injury=n!=4)
   else:
    e=self.event("guard_torment","Bone",guard["xy"],["Deliberately reveals himself to the guard.","Precise near-hit damages the guard's equipment.","Cuts the retreat-side railing beside the guard.","Appears from another angle and lets the guard retreat.","Strikes beside the hand reaching to help; deliberately spares the guard."][n%5],target=guard["id"],trigger="guard watches, retreats or attempts protection",deliberate_miss=True)
   self.alert(e,25);g=self.gid(guard["id"]);g["decision_due"]=self.t+3
   b["guard_stage"]+=1;b["ready"]=self.t+8+(n%3)*2;return
  if b["focus"]:
   p=self.P[b["focus"]];g=self.gid(p["id"])
   if not p["alive"]:b["focus"]=None;b["stage"]="idle";return
   d=dist(b["xy"],p["xy"])
   h=p["shelter"]
   target=DOORS[h]["rear"] if h else p["xy"]
   if d>11 or (not h and not visible(b["xy"],p["xy"])):
    if not b["motion"]:
     ps=self.actor_move("bone",target,8);self.event("bone_burst","Bone",b["xy"],"Short burst toward the current human stimulus.",path=ps,trigger=b.get("trigger","M05 protective parent / coop motion"),target=p["id"])
    return
   b["motion"]=None
   if b["stage"] in ["opening","approach"]:
    if h:
     e=self.event("bone_object_strike","Bone",DOORS[h]["rear"],"Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side.",shelter=h,target=p["id"],trigger=b.get("trigger"))
     for gg in self.G.values():
      if gg["shelter"]==h:self.compromise(gg,"Bone precision strike at refuge",DOORS[h]["rear"],e["id"])
    else:
     e=self.event("bone_near_hit","Bone",p["xy"],"Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now.",target=p["id"],trigger=b.get("trigger","M05 parent moving between child and Bone"),deliberate_miss=True)
     self.compromise(g,"Bone deliberate near-hit",p["xy"],e["id"])
    self.alert(e,19);b["stage"]="response";b["ready"]=self.t+6;return
   # Response-based resolution: indoor silence can frustrate acquisition; outdoors acquired targets are vulnerable.
   if h:
    e=self.event("bone_abandon","Bone",b["xy"],"After changing the shelter's decision state, loses interest in the unexposed occupants.",target=p["id"],trigger="no acquired person at the threatened opening")
   else:
    moving=bool(g["motion"]);val=hash01(str(p["id"])+str(int(b.get("focus_start",90))))
    if val<.46:
     self.casualty(p["id"],"Bone","precise strike following the civilian's response","acquired exposed person",True)
     e=self.event("bone_kill","Bone",p["xy"],"Precisely kills the acquired person following their movement / protective response.",target=p["id"],trigger="human response, not repeated Blood noise")
    elif val<.68:
     self.casualty(p["id"],"Bone","precise disabling injury during pursuit","acquired exposed person",False)
     e=self.event("bone_injury","Bone",p["xy"],"Deliberately injures the acquired person; nearby people must reconsider help or flight.",target=p["id"])
    else:
     e=self.event("bone_flush","Bone",p["xy"],"Cuts off the nearer cover with another exact object strike, then allows flight.",target=p["id"],trigger="person choosing cover / running")
     self.compromise(g,"Bone cut off cover",p["xy"],e["id"])
    self.alert(e,24)
   b["seen"][p["id"]]=self.t;b["focus"]=None;b["stage"]="idle";b["ready"]=self.t+3
   self.s["last_major"]=self.t;return
  candidates=[]
  for gid,g in self.G.items():
   ids=self.living(g)
   if not ids:continue
   h=g["shelter"];d=dist(b["xy"],g["xy"])
   if d>52:continue
   stim=None;score=0
   if not h and visible(b["xy"],g["xy"]):
    if g["motion"]:stim="human movement along "+g["intention"];score=19
    elif g.get("alarm") and self.t-g["alarm"]["t"]<20:stim="frightened human reaction";score=14
    elif any("child" in self.P[p]["role"] for p in ids):stim="protective posture beside child";score=15
    else:stim="person watches from an exposed position";score=6
   if h:
    pulsing=any(st["active"] and st["shelter"]==h and st["signal"] in ["presence","dense"] for st in self.s["streams"])
    if pulsing and visible(b["xy"],DOORS[h]["front"],[h]):stim="visible search stream pulses at threshold; Bone recognises interest";score=22
   if not stim:continue
   pid=min(ids,key=lambda p:b["seen"].get(p,-1000))
   novelty=max(.05,min(1,(self.t-b["seen"].get(pid,-1000))/55))
   score=(score+hash01(pid+str(int(self.t)//20))*12)*novelty-d*.22
   candidates.append((score,pid,stim))
  if not candidates:
   if b["motion"]:return
   if self.t<b.get("scan_after",self.t+0):
    return
   # Loss of human stimuli prompts a quick architectural vantage change, not a census sweep.
   vantages=[[-30,32],[14,53],[-37,70],[38,65],[15,86],[-2,108]]
   visited=b.setdefault("vantage_visits",{})
   options=[(hash01(str(v)+str(int(self.t)//17))*22+min(60,self.t-visited.get(str(v),-1000))*.4-dist(b["xy"],v)*.25,v)
    for v in vantages if dist(b["xy"],v)>9]
   _,v=max(options);visited[str(v)]=self.t;b["scan_after"]=self.t+10
   ps=self.actor_move("bone",v,8)
   self.event("bone_vantage","Bone",b["xy"],"Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction.",path=ps,trigger="no acquired human stimulus; attention shifts to an open elevated sightline")
   return
  if candidates:
   _,pid,stim=max(candidates);b["focus"]=pid;b["stage"]="approach";b["focus_start"]=self.t;b["trigger"]=stim
   self.event("bone_attention","Bone",b["xy"],"Attention changes: "+stim,target=pid,target_xy=self.P[pid]["xy"])
 def choose_shelter(self,g,avoid=None):
  options=[]
  for h in BUILD:
   if h=="MayorHall" or h==avoid:continue
   d=dist(g["xy"],DOORS[h]["front"])
   if d>75:continue
   # Familiar home / public refuge preference; no occupancy oracle.
   public=h in ["Tavern","Church","NorthBarn","SouthBarn"]
   familiar=h==g["home"]
   danger=self.s["compromised"].get(h,0) if any(x["shelter"]==h and x["threshold_seen"] and dist(x["tip"],g["xy"])<12 for x in self.s["streams"]) else 0
   score=d-(12 if familiar else 5 if public else 0)+danger*18
   options.append((score,h))
  return min(options)[1] if options else "Church"
 def split(self,g,stay,flee,reason):
  ids=self.living(g)
  if not stay or not flee:return None
  new_id=f"G{len(self.G)+1:03d}"
  ng={**g,"id":new_id,"members":flee[:],"events_seen":g["events_seen"][:],"split_from":g["id"],"motion":None,"decision_due":self.t}
  g["members"]=[p for p in g["members"] if p not in flee];self.G[new_id]=ng
  self.s["decisions"].append({"t":self.t,"phase":"REACTION","group":g["id"],"people":ids,"decision":"disagreement splits group","reason":reason,"stay":stay,"leave":flee,"new_group":new_id,"xy":g["xy"][:]})
  return ng
 def destination(self,g,reason,force=False):
  ids=self.living(g);p=self.P[ids[0]]
  k=p["knowledge"];loc=g["xy"];n=g["compromises"]
  # Direct/report barrier knowledge changes routes only for these recipients.
  flee_edge=(p["personality"]=="escape-minded" and (force or g["home"] is None)) or (n>=2 and hash01(g["id"])<.28)
  if flee_edge and k["barrier"]<4 and not k["barrier_report"]:
   bp=xy(nearest_points(Point(loc),BARRIER.boundary)[1]);v=np.array(bp)-np.array(loc);v/=max(.01,np.linalg.norm(v));dest=list(np.array(bp)-v*.25)
   self.move(g,dest,"try nearby forest/field edge; lethal response unknown","flee",endpoint="barrier")
   for pid in ids:self.know(pid,"barrier",max(1,self.P[pid]["knowledge"]["barrier"]),"visible perimeter on chosen route")
  elif p["personality"]=="authority-seeking" and loc[1]>55 and n>0:
   self.move(g,[2,122],"seek estate guards / authority","flee")
  else:
   h=self.choose_shelter(g,g["shelter"] if force else None)
   self.move(g,DOORS[h]["rear"] if force else DOORS[h]["front"],reason,"flee" if force else "walk",shelter=h)
 def reaction(self):
  # Transfers are person-level, sight / shared-room limited, and warning reports stay reports.
  if int(self.t)%8==0:
   for pid,p in self.P.items():
    if not p["alive"]:continue
    for qid,q in self.P.items():
     if qid==pid or not q["alive"] or dist(p["xy"],q["xy"])>5:continue
     if p["shelter"]!=q["shelter"]:continue
     if p["shelter"] is None and not visible(p["xy"],q["xy"]):continue
     if p["knowledge"]["barrier"]>=4 and not q["knowledge"]["barrier_report"]:
      self.know(qid,"barrier_report",True,"warning from "+pid,"report")
     for key in ["Blood","Bone"]:
      if p["knowledge"][key].startswith("direct") and q["knowledge"][key]=="unknown":
       self.know(qid,key,"report: "+p["knowledge"][key][8:],"warning from "+pid,"report")
  for g in list(self.G.values()):
   ids=self.living(g)
   if not ids or self.t<g["decision_due"] or self.t<g.get("wait_until",0):continue
   p=self.P[ids[0]];k=p["knowledge"];alarm=g["alarm"]
   if p["id"]==self.s["mayor_id"]:
    g["decision_due"]=self.t+30;g["intention"]="remain with household guard in hall; seeking reports";p["intention"]=g["intention"];continue
   # Current motion continues until an actual new threat interrupts it.
   if g["motion"] and (not alarm or alarm["t"]<g["motion"]["start"]):continue
   self.stopmotion(g,"fresh local decision")
   dec={"t":round(self.t,3),"phase":"REACTION","group":g["id"],"people":ids,"xy":g["xy"][:],"shelter":g["shelter"],
    "stimulus":alarm if alarm else "blackout / ongoing public emergency","knowledge_used":{x:k[x] for x in ["Blood","Bone","barrier","barrier_report"]}}
   if p["id"]==self.s["entrance_guard_id"]:
    if self.s["bone"]["guard_recognised"]:
     others=[q for q in self.P.values() if q["alive"] and q["id"]!=p["id"] and q["shelter"] is None and dist(q["xy"],g["xy"])<17]
     if others:
      q=min(others,key=lambda q:dist(q["xy"],g["xy"]));self.move(g,q["xy"],"protect nearby civilian / hold a retreat line","walk")
      dec["decision"]="attempt protection despite personal pursuit";g["decision_due"]=self.t+7
     else:
      self.move(g,[g["xy"][0]+4,g["xy"][1]+10],"retreat uphill while keeping Bone in sight","flee");dec["decision"]="controlled terrified retreat";g["decision_due"]=self.t+8
    elif g["plan"]=="undecided":
     self.move(g,[-3,95],"investigate lower emergency from staircase base","walk");g["plan"]="investigate";dec["decision"]="leave estate gate to obtain local information"
    else:
     visible_people=[q for q in self.P.values() if q["alive"] and q["origin"]!="P16" and q["shelter"] is None and dist(q["xy"],g["xy"])<30]
     if visible_people:
      q=min(visible_people,key=lambda q:dist(q["xy"],g["xy"]));self.move(g,q["xy"],"protect / question local civilians","walk");dec["decision"]="respond to visible people"
     else:self.move(g,[15,80],"investigate toward church / lower cries","walk");dec["decision"]="advance toward audible emergency"
    g["alarm"]=None;self.s["decisions"].append(dec);continue
   if p["id"]==self.s["service_guard_id"] and g["plan"]=="undecided":
    self.move(g,[-41.34,155.6],"check paused provisions delivery and cart route","walk");g["plan"]="service";dec["decision"]="inspect service approach";self.s["decisions"].append(dec);continue
   if p["id"]==self.s["house_guard_id"]:
    g["decision_due"]=self.t+20;dec["decision"]="remain protecting hall; no remote knowledge";self.s["decisions"].append(dec);continue
   if p["micro"]=="M13" and self.s["bell"] is None:
    self.move(g,[23.5,86],"pull accessible emergency bell rope","walk",endpoint="bell");dec["decision"]="blackout and lower disturbance justify ordinary alarm";self.s["decisions"].append(dec);continue
   if p["personality"]=="opportunist" and not p.get("exploited"):
    p["exploited"]=True
    if p["origin"]=="P08":
     self.move(g,[-5,53],"take unattended market valuables for private gain","walk");g["wait_until"]=self.t+8
    else:
     self.move(g,[-26,-56],"take shared handcart and monopolise stored supplies","walk");g["wait_until"]=self.t+9
    dec["decision"]=p["motive"];dec["moral_class"]="intentional exploitation, independent of survival refusals"
    self.s["decisions"].append(dec);self.event("opportunism","Civilians",g["xy"],p["motive"],people=ids)["phase"]="REACTION";continue
   if g["shelter"]:
    if alarm and alarm["kind"] in ["blood_stream","Bone precision strike at refuge","nearby pressure / damaged refuge"]:
     # Conflicting dispositions within the same house are preserved as split groups.
     stay=[pid for pid in ids if self.P[pid]["personality"] in ["cautious","kin-first"]]
     flee=[pid for pid in ids if pid not in stay]
     if any("child" in self.P[pid]["role"] for pid in ids): # existing supervised child micro-group stays together
      flee=ids[:] if p["personality"]!="cautious" or g["compromises"]>1 else [];stay=[pid for pid in ids if pid not in flee]
     ng=self.split(g,stay,flee,"visible infiltration / precision damage: silence versus another exit")
     if ng:self.destination(ng,"leave compromised shelter by another opening",True)
     if stay:
      g["plan"]="silent_deeper";g["decision_due"]=self.t+17;dec["decision"]="remain deeper / barricade; opening a door seems worse"
      for pid in stay:self.P[pid]["intention"]="remain silent deeper in compromised shelter"
      # Interior refinement: move 2m away from the visible entrance, within the existing footprint.
      h=g["shelter"];c=np.array(center(h));v=c-np.array(DOORS[h]["front"]);v/=max(.01,np.linalg.norm(v));deep=list(c+v*2)
      if BUILD[h].covers(Point(deep)):
       g["xy"]=deep
       for pid in self.living(g):self.P[pid]["xy"]=deep[:]
     else:self.destination(g,"leave compromised shelter by another opening",True);dec["decision"]="leave compromised refuge"
    else:
     g["plan"]="shelter";g["decision_due"]=self.t+17;dec["decision"]="stay with household / listen; no locally observed reason to expose self"
    g["alarm"]=None;self.s["decisions"].append(dec);continue
   if p["origin"]=="P08" and any(self.P[pid]["injured"] for pid in ids) and g["plan"]=="undecided":
    self.move(g,[-8,54],"help wounded toward nearest frontage","walk",shelter="Cottage_13");g["plan"]="aid"
    dec["decision"]="wounded seek assistance and nearby cover"
   elif p["origin"]=="P08" and g["plan"]=="undecided" and p["personality"]=="kin-first":
    self.move(g,[3,50],"help injured at civic strike edge","walk");g["plan"]="aid";dec["decision"]="visible injured prompt a local rescue attempt";g["decision_due"]=self.t+7
   elif alarm and alarm["kind"]=="barrier_attack":
    self.destination(g,"withdraw from witnessed lethal boundary",True);dec["decision"]="leave boundary and seek cover; direct B4 stays local"
   elif p["micro"]=="M05":
    self.destination(g,"parent and child seek cover" if len(ids)>1 else "surviving child retreats toward familiar cover",True);dec["decision"]="respond to Bone using the surviving micro-group members"
   else:
    self.destination(g,"seek familiar home / nearby refuge",bool(alarm))
    dec["decision"]="seek local refuge or perceived escape using current knowledge"
   g["alarm"]=None;g["last_decision"]=self.t;self.s["decisions"].append(dec)
  # An approach to the Witch is an observation, not instant attribution of guilt.
  w=self.s["witch"]["xyz"]
  if self.t<self.s["witch"]["arrival"]:
   for pid,p in self.P.items():
    if p["alive"] and p["shelter"] is None and dist(p["xy"],w)<4 and p["knowledge"]["Witch"]=="ordinary neighbour; cause unknown":
     self.know(pid,"Witch","direct: calm neighbour ignores plea; responsibility unknown","local path encounter")
     e=self.event("witch_plea","Civilians",p["xy"],"Calls to the familiar Witch while she continues uphill without answering.",people=[pid]);e["phase"]="REACTION"
 def snapshot(self):
  self.s["snapshots"].append({"t":round(self.t,3),"alive":sum(p["alive"] for p in self.P.values()),"injured":sum(p["alive"] and p["injured"] for p in self.P.values()),
   "blood":{**self.power(),"xy":self.s["blood"]["xy"][:]},"bone_xy":self.s["bone"]["xy"][:],"witch_xyz":self.s["witch"]["xyz"][:],
   "people":{pid:{"xy":p["xy"][:],"alive":p["alive"],"injured":p["injured"],"shelter":p["shelter"],"barrier":p["knowledge"]["barrier"],"barrier_report":p["knowledge"]["barrier_report"]} for pid,p in self.P.items()},
   "stream_tips":[{"id":st["id"],"travel":st["travel"],"active":st["active"],"signal":st["signal"]} for st in self.s["streams"]]})
 def run_cycle(self):
  start=self.t;ei=len(self.s["events"]);di=len(self.s["decisions"]);ki=len(self.s["casualties"]);mi=len(self.s["movements"]);wi=len(self.s["knowledge_ledger"])
  if not self.s["snapshots"]:self.snapshot()
  while not self.s["closed"]:
   end=self.s["witch"]["end"];dt=min(1,end-self.t)
   self.advance(dt)
   w=self.s["witch"]
   if self.t>=w["arrival"] and not w["secured"]:
    w["secured"]=True;self.event("mayor_secured","Witch",w["xyz"][:2],"Reaches and secures the Mayor; sixty-second confrontation begins. No survivor-count knowledge.",arrival=w["arrival"])
   if self.t>=end-.00001:
    self.casualty(self.s["mayor_id"],"Witch","personal final killing after sixty-second confrontation","secured Mayor; cinematic method reserved",True,[])
    self.event("mayor_final","Witch",w["xyz"][:2],"Mayor personally killed by Witch. Primary simulation closes; no later casualties.")
    self.s["closed"]=True;break
   # ACTION: physical fronts and supernatural decisions, from current local state.
   self.resource();self.streams(dt);self.blood();self.bone();self.barrier()
   # REACTION: separate local reception and civilian decisions; motions never freeze.
   self.reaction()
   if self.t-start>=15 or (self.s["last_major"]>start and self.t-start>=5):break
  self.snapshot();self.s["cycle"]+=1
  n=self.s["cycle"]
  common={"cycle":n,"start":start,"end":self.t,"canonical_clock":"continuous; parallel motion advances between separately evaluated action/reaction decisions"}
  (OUT/f"C{n:02d}_action.json").write_text(json.dumps({**common,"events":[e for e in self.s["events"][ei:] if e["phase"]=="ACTION"],"casualties":self.s["casualties"][ki:]},indent=2))
  (OUT/f"C{n:02d}_reaction.json").write_text(json.dumps({**common,"decisions":self.s["decisions"][di:],"events":[e for e in self.s["events"][ei:] if e["phase"]=="REACTION"],"movements":self.s["movements"][mi:],"knowledge":self.s["knowledge_ledger"][wi:]},indent=2))
  (OUT/"state.json").write_text(json.dumps(self.s))
  print(json.dumps({"cycle":n,"start":start,"end":self.t,"alive":sum(p["alive"] for p in self.P.values()),"injured":sum(p["alive"] and p["injured"] for p in self.P.values()),
   "events":[(e["t"],e["kind"],e["text"],e.get("affected_people")) for e in self.s["events"][ei:] if e["kind"] not in ["resource","stream_start","stream_response"]],
   "blood":self.power(),"bone":self.s["bone"]["stage"],"new_casualties":len(self.s["casualties"])-ki,"closed":self.s["closed"]},default=str))
if __name__=="__main__":
 s=json.loads((OUT/"state.json").read_text());sim=Sim(s);sim.run_cycle()


