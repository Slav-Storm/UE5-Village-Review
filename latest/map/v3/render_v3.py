"""Render the closed V3 layers against the unchanged surveyed map."""
from pathlib import Path
import json,math,textwrap,collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon
from matplotlib.collections import PatchCollection
from shapely.geometry import shape,Point,LineString
from PIL import Image
P=Path(__file__).resolve().parent
s=json.loads((P/"v3_simulation.json").read_text());base=json.loads((P.parent/"map_data.json").read_text())
trace=json.loads((P/"v3_actor_trace.json").read_text());pockets=json.loads((P/"v3_pockets.json").read_text())
seeds=json.loads((P/"v3_story_seeds.json").read_text());M=json.loads((P/"v3_metrics.json").read_text())
F={f["id"]:f for f in base["features"]};B={k:shape(v["geometry"]) for k,v in F.items() if v["category"] in ("building","outbuilding")}
D=[c for c in s["casualties"] if c["type"]=="death"];E=s["events"];C={"Blood":"#b63639","Bone":"#80579d","Barrier":"#cb7729","Witch":"#326fa3"}
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"svg.fonttype":"none","axes.spines.top":False,"axes.spines.right":False})
def xy(g):return list(g.coords)[0]
def distance(a,b):return math.dist(a[:2],b[:2])
def trim(ps,n):
 out=[ps[0]]
 for a,b in zip(ps,ps[1:]):
  d=distance(a,b)
  if n<=d:
   out.append([a[i]+(b[i]-a[i])*n/max(d,.0001) for i in range(2)]);return out
  out.append(b);n-=d
 return out
def line(ax,ps,color,lw=1,alpha=1,style="-",arrow=False):
 if len(ps)<2:return
 a=np.array(ps);ax.plot(a[:,0],a[:,1],color=color,lw=lw,alpha=alpha,ls=style)
 if arrow and distance(ps[-2],ps[-1])>.15:ax.annotate("",xy=ps[-1],xytext=ps[-2],arrowprops={"arrowstyle":"-|>","color":color,"lw":lw,"mutation_scale":9,"alpha":alpha})
def base_map(ax,extent=(-85,85,-168,185),labels=True):
 colors={"burial_reserve":"#eeead6","cemetery_area":"#ddd6e3","estate_area":"#e3e8df","building":"#b6b6b1","outbuilding":"#cfccc4","agriculture":"#e0dfbd","cemetery":"#d6d2d9","forest":"#ccd7c9","boundary":"#878477"}
 # Polygon categories retain source outlines. Tiny production proxies are omitted for clarity.
 patches=[];fc=[]
 for f in sorted(base["features"],key=lambda x:x["category"] in ["building","outbuilding"]):
  g=shape(f["geometry"]);cat=f["category"]
  if g.geom_type=="Polygon" and (cat in ("building","outbuilding","cemetery_area","burial_reserve","estate_area") or f["id"].startswith("area_")):
   patches.append(PatchPolygon(np.array(g.exterior.coords),closed=True));fc.append(colors.get(cat,"#e5e4d8"))
  if cat=="forest" or "tree" in cat.lower():
   c=g.centroid;ax.plot(c.x,c.y,".",ms=1.5,color="#b0bca8",alpha=.65,zorder=0)
 if patches:ax.add_collection(PatchCollection(patches,facecolor=fc,edgecolor="#9c9d92",lw=.35,zorder=1))
 for f in base["features"]:
  if f["category"] in ["route_reference","footpath_reference"]:
   g=shape(f["geometry"]);a=np.array(g.coords);w=f.get("width_m",2)
   ax.plot(a[:,0],a[:,1],color="#fffefa",lw=max(.4,w*.50),zorder=2)
   ax.plot(a[:,0],a[:,1],color="#b5ae9d",lw=.45,zorder=2)
 for f in base["features"]:
  cat=f["category"];g=shape(f["geometry"])
  if cat in ["grave","grave_open"]:
   c=g.centroid;ax.plot(c.x,c.y,".",ms=1.5,color="#7f7683",zorder=3)
  if cat=="stairs" and g.geom_type=="Polygon":
   ax.add_patch(PatchPolygon(np.array(g.exterior.coords),fc="#b6b6ae",ec="#73786d",lw=.3,zorder=3))
  if cat=="contour" and g.geom_type=="LineString":
   line(ax,list(g.coords),"#d3d1bf",.45,.55)
 barrier=s["streams"] # geometry in original approved T1 only
 t1=json.loads((P.parent/"t1_simulation.json").read_text());ring=t1["barrier"]["geometry"]["coordinates"][0]
 line(ax,ring,C["Barrier"],1.2,.8,"--")
 ax.set_xlim(extent[0],extent[1]);ax.set_ylim(extent[2],extent[3]);ax.set_aspect("equal");ax.set_facecolor("#f7f6ee")
 ax.set_xlabel("East / map X (m)");ax.set_ylabel("North / uphill / map Y (m)");ax.grid(alpha=.14,lw=.5)
 if labels:
  select={"village_gate":"Gate","village_centre":"Centre","tavern":"Tavern","blacksmith":"Forge","witch_house":"Witch home","church":"Church","mayor_mansion":"Mayor"}
  for lm in base["landmarks"]:
   if lm["id"] in select:
    x,y=lm["xy"];ax.text(x+1,y+2,select[lm["id"]],fontsize=7,color="#343c3c",zorder=6,bbox={"facecolor":"white","alpha":.74,"edgecolor":"none","pad":1})
 x=extent[0]+7;y=extent[3]-20
 ax.annotate("N",xy=(x,y),xytext=(x,y-12),ha="center",fontsize=10,arrowprops={"arrowstyle":"-|>","lw":1.2})
 scaley=extent[2]+8;scalex=extent[0]+8
 ax.plot([scalex,scalex+20],[scaley,scaley],color="#333",lw=2);ax.text(scalex+10,scaley+2,"20 m",ha="center",fontsize=8)
def sheet(title,subtitle,extent=(-85,85,-168,185)):
 fig=plt.figure(figsize=(10,13.3));fig.patch.set_facecolor("#faf9f4")
 fig.text(.055,.965,title,fontsize=19,weight="bold",color="#263239")
 fig.text(.055,.933,subtitle,fontsize=10,color="#4d5b61")
 ax=fig.add_axes([.075,.09,.59,.81]);base_map(ax,extent)
 fig.text(.055,.025,"V3 • Independent T+90 branch • 2D planning only • No UE changes\nSurvey geometry preserved. Door/interior/sight assumptions are approximate. Mayor is final death at +373.923.",fontsize=8,color="#526067")
 return fig,ax
def notes(fig,heading,paragraphs,y=.87):
 fig.text(.70,y,heading,fontsize=12,weight="bold");y-=.035
 for text in paragraphs:
  wrapped=textwrap.fill(text,42)
  fig.text(.70,y,wrapped,fontsize=9,va="top",linespacing=1.45,color="#35444c")
  y-=.021*(wrapped.count("\n")+1)+.025
def mark(ax,p,n,color,size=48):
 ax.scatter(*p,s=size,c=color,edgecolors="white",linewidths=.6,zorder=9)
 ax.annotate(str(n),p,xytext=(5,5),textcoords="offset points",fontsize=8,weight="bold",color=color,zorder=10,bbox={"facecolor":"#fffdf5","edgecolor":"none","alpha":.85,"pad":1})
def save(fig,name):
 fig.savefig(P/(name+".svg"),metadata={"Date":None},facecolor=fig.get_facecolor())
 fig.savefig(P/(name+".png"),dpi=160,facecolor=fig.get_facecolor())
 im=Image.open(P/(name+".png")).convert("RGB").quantize(colors=192)
 im.save(P/(name+".png"),optimize=True);plt.close(fig)
def actor_path(ax,actor,alpha=.9,lw=1.6):
 line(ax,[r[actor.lower()][:2] for r in trace],C[actor],lw,alpha)
def casualty_points(ax,actor=None,alpha=.85):
 for c in D:
  if actor and c["attacker"]!=actor:continue
  ax.scatter(*c["xy"],s=14,c=C[c["attacker"]],marker="x",alpha=alpha,zorder=5)
def attack(ax,e,alpha=.15):
 if not e.get("path"):return
 a=np.array(e["path"][0]);b=np.array(e["path"][-1]);v=b-a;v/=max(.01,np.linalg.norm(v));perp=np.array([-v[1],v[0]])*e["power"]["halfwidth"]
 ax.add_patch(PatchPolygon([a-perp,a+perp,b+perp,b-perp],fc=C["Blood"],ec=C["Blood"],alpha=alpha,lw=.6,zorder=4))
 line(ax,e["path"],C["Blood"],1,.65,arrow=True)
# 01
fig,ax=sheet("V3 / FULL CHRONOLOGY","57 dead • 113 alive • Failed near-total-massacre test")
for a in C:
 if a!="Barrier":actor_path(ax,a,alpha=.65)
casualty_points(ax)
selected=[next(e for e in E if e["kind"]==k) for k in ["blood_attack","barrier_contact","recognition","guard_final","mayor_final"]]
for i,e in enumerate(selected,1):mark(ax,e["xy"],i,C.get(e["actor"],"#333"))
notes(fig,"Five anchors",[f'{i}. +{e["t"]:.1f} — {e["text"]}' for i,e in enumerate(selected,1)]+["Blood: solid red. Bone: purple movement, separate incidents. Witch: blue uphill route. Orange: reactive boundary.","Early sources and all seven pre90 deaths remain unchanged."])
save(fig,"01_v3_full_chronology")
# 02
fig,ax=sheet("V3 / BLOOD INCIDENTS","Executed body path and pressure envelopes",(-65,75,-25,135))
actor_path(ax,"Blood")
for e in E:
 if e["kind"]=="blood_attack":attack(ax,e)
casualty_points(ax,"Blood")
notes(fig,"Concentration",[ "45 total Blood deaths; 41 after +90.","Targets come from visible activity, aid/bleeding, or physically delivered coarse stream signals.","15 executed strikes. Several intersect no person because people move or another structure absorbs pressure.","+286: after obstructed pressure, Blood flanks the intervening shed; body speed remains 1.55 m/s.","Envelopes are provisional force requirements, not finished destroyed buildings."])
save(fig,"02_v3_blood_incidents")
# 03
fig,ax=sheet("V3 / BLOOD RESOURCE","Accessible spilled blood drives local power; no timed level-ups",(-65,75,-25,135))
for src in s["sources"]:
 ax.scatter(*src["xy"],s=15+src["units"]*18,facecolors=C["Blood"] if src["collected"] else "none",edgecolors=C["Blood"],alpha=.7,zorder=5)
actor_path(ax,"Blood");notes(fig,"Resource ledger",["Filled: collected source. Hollow: still at its recorded site.","57 generated units = 21.66 collected + 35.34 remaining.","FED at T90; SATURATED later. DELUGE is never reached in this run.","Final rage adds reach/branches/pressure. Body speed stays fixed."])
ch=fig.add_axes([.70,.17,.26,.23]);ts=[90]+[x["t"] for x in s["snapshots"][1:]];rs=[4.88]+[x["blood"]["resource"] for x in s["snapshots"][1:]]
ch.step(ts,rs,where="post",color=C["Blood"]);ch.axvline(s["witch"]["arrival"],ls="--",color=C["Witch"]);ch.set_xlabel("Seconds");ch.set_ylabel("Collected / accessible start units");ch.grid(alpha=.2)
save(fig,"03_v3_blood_power")
# 04 four snapshots, exact saved times.
fig,axs=plt.subplots(2,2,figsize=(10,12.5));fig.patch.set_facecolor("#faf9f4")
fig.suptitle("V3 / PHYSICAL SEARCH NETWORK",fontsize=19,weight="bold",y=.98)
for ax,t in zip(axs.ravel(),[137,254,320,s["t"]]):
 snap=min(s["snapshots"],key=lambda q:abs(q["t"]-t));base_map(ax,(-60,75,-20,115),False)
 states={x["id"]:x for x in snap["stream_tips"]}
 for st in s["streams"]:
  if st["id"] in states:
   q=states[st["id"]];line(ax,trim(st["path"],q["travel"]),C["Blood"] if q["active"] else "#aaa39a",1.5 if q["active"] else .6,.9 if q["active"] else .4)
 for pid,p in snap["people"].items():
  if p["alive"]:ax.plot(*p["xy"],".",ms=2.5,color="#3c6777",alpha=.7)
 ax.plot(*snap["blood"]["xy"],"s",color=C["Blood"],ms=7)
 ax.set_title(f'T+{snap["t"]:.1f} • {snap["alive"]} alive',fontsize=12)
fig.subplots_adjust(left=.08,right=.96,top=.94,bottom=.1,wspace=.23,hspace=.21)
fig.text(.07,.04,"Red: active physical branches. Grey: reached but withdrawn trails. Blue: living population.\nOnly realised path lengths are shown; planned unvisited extensions are omitted. 29 commitments; 13 tested footprints.",fontsize=9)
save(fig,"04_v3_search_network")
#05
fig,ax=sheet("V3 / BONE INCIDENT PATTERN","Attention, consequences and short bursts; no building-clearance itinerary",(-65,75,-25,145))
actor_path(ax,"Bone",.30,.7)
bone_events=[e for e in E if e["actor"]=="Bone" and e["kind"] not in ["bone_burst","bone_vantage","bone_attention"]]
for e in bone_events:
 ax.scatter(*e["xy"],s=27,c=C["Bone"],marker="x" if "kill" in e["kind"] or e["kind"]=="guard_final" else "o",alpha=.72,zorder=6)
for e in E:
 if e["kind"]=="bone_burst":
  # Bursts are separately visible; actual continuous trace is faint context only.
  a=e["xy"];line(ax,e["path"],C["Bone"],.8,.32,"--")
notes(fig,"Attention consequences",["6 total Bone fatalities; 3 after +90.","7 deliberate near-hit incidents, 5 flushes, 5 shelter object-strikes; several victims reach cover before an acquired human strike.","Human flight and visible search responses attract attention. Ordinary repeated Blood crashes do not.","Personal guard encounter: +203 to +254.","Faint solid trace: executed positions. Dashed bursts: commitments, sometimes interrupted.","Important failure: repeated pressure/abandonment remains too weak. No quota kills are added."])
save(fig,"05_v3_bone_incidents")
#06
fig,ax=sheet("V3 / SON-KILLER GUARD","Recognition → prolonged personal torment → precise final killing",(-20,25,90,146))
gids=[s["entrance_guard_id"],"P12-09"];raw=json.loads((P/"v3_initial_state.json").read_text())
# Guard path reconstructed from its executed commitments; truncation ends at death.
guard_trace=json.loads((P/"v3_guard_trace.json").read_text())
line(ax,[r["guard"] for r in guard_trace if r["t"]<=254],"#b58a35",2,.9)
guard=[e for e in E if e["kind"] in ["recognition","guard_torment","guard_protected_person_harmed","guard_final"]]
mark(ax,guard[0]["xy"],"A",C["Bone"]);mark(ax,[2,122],"B",C["Bone"]);mark(ax,[6,132],"C",C["Bone"])
notes(fig,"Local, personal sequence",["A / +203: Bone sees and recognises the entrance guard.","B / +205–243: reveals himself, strikes equipment and allows retreat. The guard tries to protect P12-09.","+223: deliberately injures P12-09 while sparing the guard.","+243: kills the same protected civilian. No second invented victim.","C / +254: precise personal guard death after 51 seconds.","Dialogue opportunities remain fragments of recognition; no finished lines or extra historical guilt."])
save(fig,"06_v3_guard_sequence")
#07
fig,ax=sheet("V3 / SHELTER MOVEMENT","Committed travel clipped at arrival, interruption, death or terminal")
for mv in s["movements"]:
 end=min(mv.get("actual_end") or s["t"],s["t"],mv["planned_end"])
 # If all movers died, the last death terminates the group line.
 deadtimes=[s["people"][p].get("death",{}).get("t",s["t"]) for p in mv["people"]]
 end=min(end,max(deadtimes))
 lengthsum=sum(distance(a,b) for a,b in zip(mv["path"],mv["path"][1:]))
 n=lengthsum*max(0,(end-mv["start"]))/max(.001,mv["planned_end"]-mv["start"])
 forced="compromised" in mv["intention"]
 line(ax,trim(mv["path"],n),"#7f4591" if forced else "#5989a0",1.4 if forced else .55,.8 if forced else .22)
for x in pockets:ax.scatter(*x["xy"],s=8*x["count"],facecolors="none",edgecolors="#376950",alpha=.7,zorder=5)
notes(fig,"Separate decisions",["148 movement commitments. 9 intra-group splits. 15 departures explicitly leave compromised shelters.","Purple: leave compromised shelter. Blue: other executed movement. Green rings: final survivors by occupied footprint.","Some stay silent/deeper while others choose another exit. Refugees can arrive at already probing blood.","Large farm and residential pockets remain untouched. The policy fails to expose enough of the village."])
save(fig,"07_v3_shelter_movement")
#08
fig,ax=sheet("V3 / BOUNDARY KNOWLEDGE","Independent contacts; direct experience and warnings stay separate")
contacts=[e for e in E if e["kind"]=="barrier_contact"]
for i,e in enumerate(contacts,1):mark(ax,e["xy"],i,C["Barrier"])
for p in s["people"].values():
 if p["alive"]:
  k=p["knowledge"]
  if k["barrier"]==4:ax.scatter(*p["xy"],s=25,c=C["Barrier"],marker="^",zorder=7)
  elif k["barrier_report"]:ax.scatter(*p["xy"],s=18,c="#3a8894",marker="o",zorder=6)
notes(fig,"Five local discoveries",[f'{i}. +{e["t"]:.0f}: {e["victim"]}; {len(e["direct_witnesses"])} witnesses at contact.' for i,e in enumerate(contacts,1)]+["14 distinct direct witnesses; 22 warning recipients during the run. Counts include people who later die.","Triangles: surviving direct witnesses. Blue dots: surviving report recipients.","Contacts 4 and 5 follow compromised-shelter departures. No global lethal-boundary knowledge."])
save(fig,"08_v3_barrier_knowledge")
#09
fig,ax=sheet("V3 / WITCH DESTINATION","Preserved ascent, creator immunity, no civilian hunting",(-60,65,-25,165))
t1=json.loads((P.parent/"t1_simulation.json").read_text());w0=next(a for a in t1["actors"] if a["id"]=="witch")
line(ax,w0["geometry"]["coordinates"],"#9ebfd1",1.1)
actor_path(ax,"Witch",1,2)
for t in [90,180,258.245,s["witch"]["arrival"]]:
 r=min(trace,key=lambda r:abs(r["t"]-t));mark(ax,r["witch"][:2],f"+{t:.0f}",C["Witch"])
notes(fig,"Route clock",["237.601 m remaining 3D travel.","Road/court 1.1 m/s; stairs 0.85 m/s. Saved height seam included.","Arrival +313.923. Sixty-second confrontation ends +373.923.","Two water-carrier pleas at +91 are ignored. Calmness does not reveal responsibility.","No actual Blood envelope crosses her position in this branch."])
ch=fig.add_axes([.71,.16,.25,.22]);ch.plot(s["witch"]["times"],[p[2] for p in s["witch"]["route"]],color=C["Witch"]);ch.set_xlabel("Seconds");ch.set_ylabel("Gate-relative height (m)");ch.grid(alpha=.2)
save(fig,"09_v3_witch_route")
#10 timeline plus estate context
fig=plt.figure(figsize=(10,11.5));fig.patch.set_facecolor("#faf9f4")
fig.text(.07,.955,"V3 / MAYOR'S FINAL MINUTE",fontsize=19,weight="bold")
ax=fig.add_axes([.08,.40,.50,.47]);base_map(ax,(-30,32,100,164),False)
for p in s["witch"]["route"]:
 pass
line(ax,[p[:2] for p in s["witch"]["route"]],C["Witch"],2);mark(ax,[2,146],"Arrival / final",C["Witch"])
notes(fig,"Subjects, not dialogue",["Her lover and son. His authority and failure. Refusal of escape. She saved him until last.","Pauses while suffering continues outside. Active rage, not remorseful-spirit exposition.","The Mayor cannot escape. Exact restraint/execution mechanism remains open.","Estate staff/guard reactions are under-modelled and need review."],.86)
ax2=fig.add_axes([.10,.15,.82,.16]);arr=s["witch"]["arrival"]
ax2.broken_barh([(0,60)],(.5,.5),facecolors="#8fb3cc");ax2.text(30,.75,"Witch secures Mayor / deliberate confrontation",ha="center",fontsize=10)
for e in E:
 if e["kind"]=="blood_attack" and e["t"]>arr:
  count=sum(c["type"]=="death" and c["attacker"]=="Blood" and abs(c["t"]-e["t"])<.01 for c in s["casualties"])
  ax2.plot(e["t"]-arr,.35,"v",color=C["Blood"]);ax2.text(e["t"]-arr,.15,f'+{e["t"]:.0f}\n{count} deaths',ha="center",fontsize=9)
ax2.axvline(60,color=C["Witch"]);ax2.set_xlim(-1,63);ax2.set_ylim(-.1,1.3);ax2.set_yticks([]);ax2.set_xlabel("Seconds after arrival at +313.923");ax2.set_title("15 Blood deaths during the minute; Mayor is the final death at its end.",fontsize=11)
fig.text(.08,.04,"No survivor-count knowledge. No further deaths or post-event actor behaviour simulated.\nRage improves local streams/pressure; its unique casualty contribution is not isolated by a counterfactual.",fontsize=9)
save(fig,"10_v3_mayor_minute")
#11
fig,ax=plt.subplots(2,1,figsize=(10,10),gridspec_kw={"height_ratios":[2,1.2]});fig.patch.set_facecolor("#faf9f4")
fig.suptitle("V3 / CASUALTY PROGRESSION",fontsize=19,weight="bold")
times=sorted(set([0,90,s["t"]]+[c["t"] for c in D]))
for actor in C:
 ax[0].step(times,[sum(c["attacker"]==actor and c["t"]<=t for c in D) for t in times],where="post",label=actor,color=C[actor],lw=2)
ax[0].axvline(90,ls="--",color="#777");ax[0].axvline(arr,ls="--",color=C["Witch"]);ax[0].set_ylabel("Cumulative fatalities");ax[0].legend();ax[0].grid(alpha=.2)
ax[1].step(times,[170-sum(c["t"]<=t for c in D) for t in times],where="post",color="#386c53",lw=2);ax[1].set_ylabel("Living residents");ax[1].set_xlabel("Canonical seconds");ax[1].set_ylim(0,175);ax[1].grid(alpha=.2)
fig.text(.1,.03,"Final: Blood 45 • Bone 6 • Barrier 5 • Witch 1 = 57 fatalities; 113 survive, none injured.\nA surviving majority is an explicit failed narrative test. No cleanup fatalities are invented.",fontsize=11)
fig.subplots_adjust(left=.10,right=.94,top=.91,bottom=.13,hspace=.3)
save(fig,"11_v3_casualty_progression")
#12
fig,ax=sheet("V3 / FINAL AFTERMATH","T+373.923 • 57 fatalities / 113 survivors • No later actions")
casualty_points(ax,alpha=.5)
for i,x in enumerate(pockets,1):
 badge=[x["xy"][0]+9,x["xy"][1]-2] if x["shelter"]=="MayorHall" else x["xy"]
 ax.scatter(*badge,s=12*x["count"],c="#43845c",alpha=.7,edgecolors="white",zorder=6)
 ax.text(badge[0],badge[1],str(x["count"]),ha="center",va="center",fontsize=7,color="white",weight="bold",zorder=7)
for a in ["Blood","Bone","Witch"]:mark(ax,s[a.lower()]["xyz"][:2] if a=="Witch" else s[a.lower()]["xy"],a,C[a],65)
notes(fig,"Survivors are retained",["Green count = living people at that footprint. Crosses = fatal event positions, not corpse poses.","29 survivor pockets. No injured survivors.","Farms, western/upper households and parts of the east were not reached by this local search policy.","Some compromised refuges shed occupants while quieter individuals remained.","MayorHall: four other people remain alive. Their final confrontation responses need further authored review.","No survivor identity is promoted to permanent lore."])
save(fig,"12_v3_final_aftermath")
#13
fig,ax=sheet("V3 / ENVIRONMENTAL STORY SEEDS","Causal opportunities only; no produced damage, props or corpse poses")
palette={"stream_threshold":"#bd5959","blood_attack":C["Blood"],"barrier_contact":C["Barrier"],"theft_completed":"#ae9438","mayor_secured":C["Witch"],"witch_plea":C["Witch"]}
for seed in seeds:
 color=palette.get(seed["category"],C["Bone"]);ax.scatter(*seed["xy"],s=22,c=color,alpha=.65,zorder=5)
notes(fig,"Evidence to author later",["Searching trails beneath doors; accumulated blood at found refuges.","Shelter splits, changed exits and interrupted aid.","Deliberate precision holes and damaged cover edges.","Guard equipment and the same protected villager harmed in two stages.","Two opportunists carry stolen goods; neither receives a moral-judgment death.","Independent boundary tests and two escapes prompted by compromised shelters.","Final private confrontation; room staging remains unassigned.","74 linked opportunities in v3_story_seeds.json."])
save(fig,"13_v3_story_seeds")
print("Rendered thirteen PNG/SVG pairs.")
