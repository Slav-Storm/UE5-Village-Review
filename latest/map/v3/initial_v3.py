from geometry_v3 import *
from collections import Counter
import hashlib,datetime
OUT=ROOT/"run";OUT.mkdir(exist_ok=True)
people={};groups={};counts=Counter();micros={}
def add(c,n,p,role,home=None,inside=False,micro=None,knowledge=None,dead=None,injured=False):
 ids=[]
 for j in range(n):
  counts[c]+=1;pid=f"{c}-{counts[c]:02d}";ids.append(pid)
  people[pid]={"id":pid,"origin":c,"t0_reference":c,"micro":micro,"role":role,"xy":list(p),"home":home,
    "shelter":home if inside else None,"alive":dead is None,"injured":injured,"injury_time":56 if injured else None,
    "knowledge":{"emergency":True,"Blood":"unknown","Bone":"unknown","barrier":0,"barrier_report":False,"Witch":"ordinary neighbour; cause unknown","warnings":[]},
    "intention":role,"personality":["kin-first","cautious","authority-seeking","practical","escape-minded"][int(hashlib.sha256(pid.encode()).hexdigest()[:4],16)%5]}
  if knowledge:people[pid]["knowledge"].update(knowledge)
  if dead:people[pid]["death"]=dead
 if micro:micros.setdefault(micro,[]).extend(ids)
 gid=f"G{len(groups)+1:03d}"
 groups[gid]={"id":gid,"members":ids,"xy":list(p),"home":home,"shelter":home if inside else None,"intention":role,
  "motion":None,"decision_due":94+len(groups)%7,"compromises":0,"events_seen":[],"not_before":90,"last_decision":90,
  "plan":"undecided","split_from":None,"wait_until":0,"alarm":None}
 return ids
def indoor(c,homes,nums):
 for h,n in zip(homes,nums):add(c,n,center(h),"household preparing evening food / domestic work",h,True)
add("P01",3,[5.8,-61.8],"returning long-field workers",knowledge={"Blood":"report: violence downhill from village"})
add("P01",2,[38,-52],"finish middle strip rows")
add("P01",1,[9.2,-36.3],"orchard worker delivering lower-road warning",knowledge={"Bone":"report: two people attacked on approach"})
add("P02",2,[-25.4,-51.3],"returning western field pair",knowledge={"barrier":1})
add("P02",2,[-37,-74],"finish western rows",knowledge={"barrier":1})
add("P02",1,[-19.2,-59.6],"pasture gate keeper",micro="M02",knowledge={"barrier":1})
add("P02",1,[-19.2,-59.6],"second animal keeper",knowledge={"barrier":1})
indoor("P03",["Farmstead_West"],[3])
add("P03",4,[18,-54],"barn and agricultural yard activity","Farmstead_West",knowledge={"Bone":"report: approach violence"})
indoor("P04",["Farmstead_South"],[3])
add("P04",2,[-24.7,-59.8],"barn storage pair","Farmstead_South",micro="M03")
opportunist2=add("P04",1,[-29,-50],"yard goods worker","Farmstead_South")[0]
add("P05",1,[-.7454818255,-11.1165664894],"homeward handcart worker",micro="M01",dead={"t":4,"attacker":"Bone"})
add("P05",1,[-1.1954818255,-11.6665664894],"homeward partner",micro="M01",dead={"t":6,"attacker":"Bone"})
add("P05",4,[-1.52628730005,-19.2598640571],"recoiled returning workers",knowledge={"Bone":"direct: first two quiet killings"})
indoor("P06",["NeedleHouse","CollapsedCellarCottage","Cottage_04","Cottage_09"],[2,2,3,1])
for p in people.values():
 if p["home"]=="Cottage_04":p["knowledge"]["Bone"]="report: parent warned from yard"
add("P06",2,[11,25],"lower household yard work","NeedleHouse")
add("P06",2,[25,13],"lower household garden work","CollapsedCellarCottage")
add("P06",2,[-34.3,9.2],"parent and child hiding at coop","Cottage_04",micro="M05",knowledge={"Bone":"direct: deliberate near-hit and stalking"})
add("P07",2,[-39.5,11.7],"smith and apprentice finishing cart wheel","Blacksmith",micro="M07",knowledge={"Blood":"heard: large violent crash"})
add("P07",1,[-28.4017671378,37.6234790712],"forge assistant on homeward walk",dead={"t":45,"attacker":"Bone"})
add("P07",1,[-28,18],"forge customer","Blacksmith",knowledge={"Blood":"heard: large violent crash"})
add("P08",2,[-18,35],"water pair at road edge",micro="M04",knowledge={"Bone":"direct: assistant killed","Blood":"heard: public strike"})
add("P08",2,[-3.6,49],"other well users",dead={"t":56,"attacker":"Blood"})
add("P08",2,[2,48],"stall users",dead={"t":56,"attacker":"Blood"})
add("P08",4,[3,50],"injured stall users needing help",injured=True,knowledge={"Blood":"direct: struck by first public wave"})
add("P08",1,[-11,52],"warning frontage neighbour",knowledge={"Blood":"direct: first public strike"})
add("P08",5,[6,56],"frontage neighbours",knowledge={"Blood":"direct: first public strike"})
add("P08",3,[22.5953376421,40.7978692258],"departed centre passers",knowledge={"Blood":"heard: crash behind"})
opportunist1=add("P08",1,[-2,55],"goods porter",knowledge={"Blood":"direct: first public strike"})[0]
add("P08",6,[7,46],"junction goods and passing group",knowledge={"Blood":"direct: first public strike"})
add("P09",7,center("Tavern"),"one staff member and six indoor early customers","Tavern",True,knowledge={"Blood":"report: porch reports violence; identities unclear"})
add("P09",4,[1.4,42],"tavern porch customers","Tavern",knowledge={"Blood":"direct: civic strike"})
add("P09",3,[14.1,30],"two tavern staff and delivery worker","Tavern",micro="M06",knowledge={"Blood":"heard: civic crash"})
indoor("P10",["CrookedCottage","Cottage_01","Cottage_06","Cottage_07","Cottage_12"],[3,3,3,3,2])
add("P10",2,[29.7,32],"shared-yard neighbours","CrookedCottage",micro="M08",knowledge={"Blood":"heard: civic crash"})
add("P10",5,[37.7,51.9],"four children with caregiver","Cottage_07",micro="M09",knowledge={"Blood":"heard: civic crash"})
add("P10",1,[30,20],"old-quarter yard work","Cottage_06")
add("P10",2,[27,49],"old-quarter alley walkers","Cottage_12")
indoor("P11",["CrushedHome","RearCottage","EndRowCottage","WeaverCottage","Cottage_02","Cottage_05","Cottage_10"],[2]*7)
add("P11",1,[-22,58.4],"carrying firewood","CrushedHome",micro="M10",knowledge={"Blood":"heard: civic strike"})
for h in ["RearCottage","EndRowCottage","WeaverCottage","Cottage_05","Cottage_10"]:
 add("P11",1,DOORS[h]["rear"],"western household yard work",h,knowledge={"Blood":"heard: civic strike"})
add("P11",2,[-36,69],"western neighbours walking between yards","RearCottage")
indoor("P12",["AbandonedCottage","UpperCottage","SealedCellarCottage","Cottage_03","Cottage_11"],[2]*5)
for h in ["UpperCottage","SealedCellarCottage","Cottage_03"]:add("P12",1,DOORS[h]["rear"],"upper household yard activity",h)
add("P12",1,[-18.995464369,96.903367205],"upper homeward walker","UpperCottage")
add("P13",1,[23.5,83.7],"church caretaker at public threshold","Church",micro="M13",knowledge={"Blood":"heard: destructive crash; visible lower disturbance"})
indoor("P14",["SplitRoofCottage","Cottage_08"],[2,2])
add("P14",2,[61,54],"eastern animal yard work","SplitRoofCottage",knowledge={"barrier":1})
add("P14",1,[57,75],"eastern household yard work","Cottage_08",knowledge={"barrier":1})
add("P15",3,[-47.0088105554,70.3155604468],"returning forest workers",micro="M11",knowledge={"barrier":2})
mayor=add("P16",1,[2,146],"Mayor inside hall","MayorHall",True)[0]
entrance_guard=add("P16",1,[2,124],"entrance guard at formal estate gate","MayorHall",knowledge={"barrier":2})[0]
service_guard=add("P16",1,[-22,132],"service guard at cart access","MayorHall")[0]
house_guard=add("P16",1,[5,142],"house guard inside hall","MayorHall",True)[0]
add("P16",3,[8,145],"house staff","MayorHall",True)
add("P16",1,[-11,132],"estate stable worker","MayorHall")
add("P17",2,[-41.3394326163,155.5952872518],"paused provisions delivery",micro="M12",knowledge={"barrier":2})
for c in T0["population_clusters"]:assert counts[c["id"]]==c["count"],(c["id"],counts[c["id"]],c["count"])
assert len(people)==170
# Ordinary later-life kin are not invented: these are activity/household associations only.
for pid,p in people.items():
 if p["micro"]=="M05":p["role"]="parent at coop" if pid==micros["M05"][0] else "child at coop"
 if p["micro"]=="M09":p["role"]="caregiver with children" if pid==micros["M09"][0] else "child with caregiver"
p=people[opportunist1];p["personality"]="opportunist";p["motive"]="take portable unattended market valuables for private gain"
p=people[opportunist2];p["personality"]="opportunist";p["motive"]="take household handcart and monopolise stored goods"
config={
 "branch":"V3 independent from approved T90", "seed":30910,
 "blood_walk_m_s":1.55,"bone_burst_m_s":8.0,"human_walk_m_s":1.25,"human_flight_m_s":2.3,"assisted_injured_m_s":.65,
 "stream_front_m_s":[.8,1.8],"stream_radius_m":[24,82],"stream_slots":[2,9],"stream_budget_m":[55,430],
 "stream_presence_radius_m":3.2,"stream_idle_withdraw_s":32,
 "blood_charge_s":5,"blood_recovery_s":7,"blood_attack_range_m":[11,34],"blood_halfwidth_m":[3.5,10.5],
 "blood_carried_resource_cap":48,"fatal_resource_units":1.0,"injury_resource_units":.22,
 "resource_note":"Relative accessible-volume bookkeeping; not litres, biological estimates, or a gameplay buff. Each person contributes at most one fatal source; prior injury remainder avoids double counting.",
 "sensing":"Visible/activity cues or a physically completed search path; indoor headcounts never passed to Blood's decision scoring.",
 "bone_novelty":"Repeated monster impacts discounted; human fleeing, door movement, protection and visible pulsing stream response retain value.",
 "witch_road_speed":1.1,"witch_stair_speed":.85,"mayor_confrontation_s":60,
 "calibration":"Working physical strengths fixed before running; no casualty/count target in decision code.",
 "identity_note":"Pre90 sources label cohorts/microgroups, not each resident. Pxx-nn are new stable V3 person-level refinements of those existing counts, not additional villagers or V1/V2 person-ledger imports."}
pts,times,kinds=witch_route()
state={"t":90.,"people":people,"groups":groups,"micro_members":micros,"blood":{"xy":[-2.2088023688951393,44.52432308637402],"motion":None,"charge":None,"ready":90,"resource":0,"visited":{},"target":None},
 "bone":{"xy":[-37.5,8.8],"motion":None,"focus":micros["M05"][0],"stage":"opening","ready":90,"seen":{},"guard_recognised":False},
 "witch":{"xyz":pts[0],"route":pts,"times":times,"kinds":kinds,"arrival":times[-1],"end":times[-1]+60,"secured":False},
 "mayor_id":mayor,"entrance_guard_id":entrance_guard,"service_guard_id":service_guard,"house_guard_id":house_guard,
 "opportunists":[opportunist1,opportunist2],"streams":[],"sources":[],"events":[],"casualties":[],"knowledge_ledger":[],"movements":[],"decisions":[],"snapshots":[],
 "cycle":0,"cycle_start":90,"last_major":90,"bell":None,"closed":False,"config":config,"compromised":{}}
for p in people.values():
 if not p["alive"] or p["injured"]:
  dead=not p["alive"];t=p["death"]["t"] if dead else 56;a=p["death"]["attacker"] if dead else "Blood"
  state["sources"].append({"id":"PRE-"+p["id"],"xy":p["xy"],"t":t,"units":1 if dead else .22,"collected":False,"person":p["id"]})
  state["casualties"].append({"id":"PRE-"+p["id"],"person":p["id"],"t":t,"xy":p["xy"],"type":"death" if dead else "injury","attacker":a,"intention":p["intention"],
    "cause":"Approved pre90 "+("fatality" if dead else "injury"),"exposure":"approved T1/Bone history","witnesses":micros["M04"] if t==45 else [],
    "knowledge_change":"Preserved approved local awareness overlay","blood_units":1 if dead else .22,"source_history":True})
state["casualties"].sort(key=lambda e:e["t"])
for p in people.values():
 if p["shelter"]:p["xy"]=list(center(p["shelter"]))
# All exact moving micro-group endpoints retained; static indoor allocation is explicit.
(OUT/"initial_state.json").write_text(json.dumps(state,indent=2))
(OUT/"state.json").write_text(json.dumps(state))
(OUT/"parameters.json").write_text(json.dumps(config,indent=2))
(OUT/"door_assumptions.json").write_text(json.dumps(DOORS,indent=2))
print("Census",len(people),sum(p["alive"] for p in people.values()),sum(p["alive"] and p["injured"] for p in people.values()))
print("IDs",mayor,entrance_guard,service_guard,house_guard,"opportunists",state["opportunists"])
print("Witch arrival",times[-1],"final",times[-1]+60)
