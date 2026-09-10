"""Render frozen V4 editable planning layers. Run beside JSON, with ../map_data.json."""
from pathlib import Path
import json,math,textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon
from matplotlib.collections import LineCollection
from shapely.geometry import shape,LineString,Point
from collections import Counter
P=Path(__file__).resolve().parent
BASE=P.parent/"map_data.json"
if not BASE.exists():BASE=P.parent/"inputs/map_data.json"
D=json.loads((P/"v4_simulation.json").read_text());M=json.loads(BASE.read_text(encoding="utf-8-sig"));MET=json.loads((P/"v4_metrics.json").read_text())
PATHS=json.loads((P/"v4_executed_actor_paths.json").read_text());CAS=json.loads((P/"v4_casualty_audit.json").read_text());SUR=json.loads((P/"v4_survivors.json").read_text())
COL={"Blood":"#b33648","Bone":"#7454a2","Witch":"#b28c20","Barrier":"#ce6077","civil":"#247b92"}
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"svg.fonttype":"none","axes.spines.top":False,"axes.spines.right":False})
NAMES=[
("01_v4_full_chronology","Full chronology"),
("02_v4_blood_body_path","Blood body path"),
("03_v4_blood_power","Blood power and accessible resource"),
("04_v4_distributed_network","Distributed search network"),
("05_v4_search_memory_frontier","Search memory and frontier"),
("06_v4_bone_attention_route","Bone attention and relocation"),
("07_v4_bone_consequences","Bone direct and indirect consequences"),
("08_v4_guard_sequence","Son-killer guard sequence"),
("09_v4_shelter_civilian_movement","Shelters and civilian movement"),
("10_v4_structural_damage","Cumulative structural cover"),
("11_v4_barrier_knowledge","Barrier contact and local knowledge"),
("12_v4_witch_route","Witch: one destination"),
("13_v4_mayor_final_minute","Mayor: the final minute"),
("14_v4_casualty_progression","Casualty progression"),
("15_v4_final_aftermath","Final aftermath and survivors"),
("16_v4_environmental_seeds","Environmental storytelling seeds")]
FEAT={f["id"]:f for f in M["features"]}
def geom(ax,g,face="none",edge="#b7bab3",alpha=1,lw=.6):
 if g.geom_type=="Polygon":
  ax.add_patch(PatchPolygon(list(g.exterior.coords),facecolor=face,edgecolor=edge,alpha=alpha,lw=lw))
 elif g.geom_type in ["MultiPolygon","GeometryCollection"]:
  for z in g.geoms:geom(ax,z,face,edge,alpha,lw)
 elif g.geom_type in ["LineString","LinearRing"]:
  a,b=g.xy;ax.plot(a,b,color=edge,alpha=alpha,lw=lw)
 elif hasattr(g,"geoms"):
  for z in g.geoms:geom(ax,z,face,edge,alpha,lw)
def base(ax,extent=(-91,87,-168,186),labels=True):
 ax.set_facecolor("#f4f3ec")
 trees=[]
 for f in M["features"]:
  cat=f["category"];g=shape(f["geometry"])
  if cat=="forest":
   c=g.centroid;trees.append((c.x,c.y))
  elif cat in ["agriculture","cemetery_area","burial_reserve","estate_area"]:
   geom(ax,g,face={"agriculture":"#e7e3cd","cemetery_area":"#dde3df","burial_reserve":"#e9eddf","estate_area":"#e8e6de"}[cat],edge="#c4c8bc",alpha=.75)
  elif cat=="contour":geom(ax,g,edge="#d5d3c9",alpha=.5,lw=.5)
  elif cat in ["route_reference","footpath_reference"]:
   geom(ax,g,edge="#c1b8a9",lw=2 if cat=="route_reference" else .65)
  elif cat in ["building","outbuilding"]:
   geom(ax,g,face="#b9bab5",edge="#858983",lw=.6)
  elif cat in ["boundary","gate","stairs","grave_open","cellar_access"]:
   geom(ax,g,face="#dedbd5",edge="#9c9e95",lw=.6)
 if trees:ax.scatter(*zip(*trees),s=3,c="#b4c2b0",alpha=.6,rasterized=True)
 geom(ax,shape(json.loads((P.parent/"t1_simulation.json").read_text(encoding="utf-8-sig"))["barrier"]["geometry"]) if (P.parent/"t1_simulation.json").exists() else shape(json.loads((P.parent/"inputs/t1_simulation.json").read_text())["barrier"]["geometry"]),edge=COL["Barrier"],lw=1,alpha=.6)
 ax.set_xlim(extent[:2]);ax.set_ylim(extent[2:]);ax.set_aspect("equal");ax.set_xlabel("Map east / UE +Y (m)");ax.set_ylabel("Map north / UE +X (m)")
 ax.grid(alpha=.12);ax.tick_params(labelsize=8)
 if labels:
  for name,k,off in [("Mayor","MayorHall",(12,6)),("Church","Church",(8,13)),("Tavern","Tavern",(-26,-5)),("Witch home","WitchHome",(-30,-12)),("Forge","Blacksmith",(-21,0))]:
   g=shape(FEAT[k]["geometry"]).centroid
   ax.annotate(name,(g.x,g.y),xytext=off,textcoords="offset points",fontsize=8,color="#505951",bbox={"facecolor":"white","alpha":.72,"edgecolor":"none","pad":1},arrowprops={"arrowstyle":"-","color":"#8d928c","lw":.5})
 x0,x1,y0,y1=extent
 ax.plot([x0+10,x0+30],[y0+12,y0+12],color="#404a44",lw=2);ax.text(x0+20,y0+15,"20 m",ha="center",fontsize=8)
 ax.annotate("N*",xy=(x1-12,y1-10),xytext=(x1-12,y1-30),ha="center",fontsize=10,arrowprops={"arrowstyle":"-|>","color":"#3d5149"})
def shell(i,notes,extent=(-91,87,-168,186)):
 fig=plt.figure(figsize=(14,16),facecolor="#fbfaf6")
 fig.text(.045,.969,f"V4  /  {i:02}   {NAMES[i-1][1]}",fontsize=22,weight="bold",color="#243b36")
 fig.text(.045,.944,"INDEPENDENT BRANCH FROM T+90  ·  CLOSED AT T+366.001  ·  2D PLANNING ONLY",fontsize=10,color="#6c7770")
 fig.text(.045,.918,"100 dead / 70 alive  ·  Failed near-total premise  ·  See validation caveats",fontsize=12,color="#9a3745")
 ax=fig.add_axes([.06,.07,.62,.82]);base(ax,extent)
 tx=fig.add_axes([.73,.11,.235,.75]);tx.axis("off")
 text="\n\n".join(textwrap.fill(v,39) for v in notes)
 tx.text(0,1,text,va="top",fontsize=11,linespacing=1.45,color="#34443f")
 fig.text(.045,.025,"Survey: 9 Sep 2026  ·  Grey shapes are existing scene geometry  ·  *Map north means UE +X  ·  No UE changes",fontsize=9,color="#66766c")
 return fig,ax,tx
def save(fig,i):
 root=NAMES[i-1][0];fig.savefig(P/(root+".png"),dpi=100);fig.savefig(P/(root+".svg"));plt.close(fig)
def route(ax,who,lw=2,alpha=.9,lo=90,hi=1e9):
 for q in PATHS:
  if q["actor"]!=who or q["end"]<lo or q["start"]>hi:continue
  a,b=zip(*q["path"]);ax.plot(a,b,color=COL[who],lw=lw,alpha=alpha,ls="--" if who=="Bone" else "-")
  if len(q["path"])>1 and q["distance_plan_m"]>4:ax.annotate("",q["path"][-1],q["path"][-2],arrowprops={"arrowstyle":"->","color":COL[who],"alpha":alpha,"lw":lw})
def points(ax,kind,labels=False):
 events=[e for e in D["events"] if e["kind"]==kind]
 for j,e in enumerate(events):
  if not e["xy"]:continue
  ax.scatter(*e["xy"],s=28,c=COL.get(kind,"#925433"),edgecolors="white",lw=.6,zorder=8)
  if labels:ax.annotate(f"+{e['t']:.0f}",e["xy"],xytext=(5,4),textcoords="offset points",fontsize=8)
def witch(ax):
 a=D["witch"]["xyz"];ax.plot([x[0] for x in a],[x[1] for x in a],color=COL["Witch"],lw=3,zorder=7)
def blood_areas(ax):
 for e in D["events"]:
  if e["kind"]=="Blood":geom(ax,shape(e["footprint"]),face=COL["Blood"],edge=COL["Blood"],alpha=.12,lw=.7)
def network(ax,t,include_inactive=True):
 segments=[];colors=[];widths=[]
 for e in D["network"]["edges"]:
  if e["t"]>t:continue
  on=e.get("active",True)
  if not on and not include_inactive:continue
  segments.append([e["a"],e["b"]]);colors.append("#b3364899" if on else "#c7a1a555");widths.append(.75 if on else .4)
 ax.add_collection(LineCollection(segments,colors=colors,linewidths=widths))
 for n in D["network"]["nodes"]:
  if n["t"]<=t:
   ax.scatter(*n["xy"],s=75,marker="s",c=COL["Blood"],edgecolors="white",zorder=9)
   ax.text(n["xy"][0]+3,n["xy"][1]+2,n["id"],fontsize=8,color=COL["Blood"],weight="bold")
# 01
fig,ax,_=shell(1,["Purposeful Witch walk: gold. Blood body movement: red. Bone bursts: purple dashes.","Major strike footprints are translucent red. Pins locate incidents, not corpse poses.","+98 outdoor rescue concentration. +110/134 refuge and east-lane impacts. +168/176 western reacquisition. +216 lower refuge. +258/266/272 farm attacks.","+188–254 mobile guard torment. +306 Witch secures Mayor. +360 final Blood strike. +366 Mayor final death.","Every event, casualty, local warning and split remains editable in the accompanying JSON/CSV."])
blood_areas(ax);route(ax,"Blood");route(ax,"Bone",1,.6);witch(ax);points(ax,"Blood");points(ax,"Barrier");save(fig,1)
fig,ax,_=shell(2,[f"Executed body travel: {MET['body_travel_plan_m']['Blood']:.1f} plan metres; terrain allowance tracked separately.","Body path reaches centre, lower village, farms and eastern district. Western households are attacked from the junction edge.","A strong remote concentration can redirect a long walk. Search nodes do not make offensive attacks.","Only executed travel is drawn. Interrupted or post-terminal destinations are clipped.","Red envelopes are the actual coarse attack corridors. First-hit cover assumptions are conservative and materially limit casualties."])
blood_areas(ax);route(ax,"Blood",3);points(ax,"Blood",True);save(fig,2)
# 03 chart
fig,ax,_=shell(3,["Power is event-driven accessible blood resource, not a timed upgrade.","Opening: FED with five relative accessible units. New casualties contribute when physically connected.","SATURATED and DELUGE are internal labels. Movement speed stays 1.7019 m/s.","Final-minute rage further amplifies range and search, with finite caps.","Relative resource units are planning assumptions, not litres or gameplay balance."])
ax.remove();a=fig.add_axes([.09,.55,.56,.28]);b=fig.add_axes([.09,.16,.56,.28])
ts=[90]+[c["through_s"] for c in D["cycles"]];u=[5]+[c["power"]["units"] for c in D["cycles"]]
a.step(ts,u,where="post",c=COL["Blood"],lw=2);a.set_title("Accessible spilled-blood resource");a.set_ylabel("Relative units");a.grid(alpha=.2)
b.plot(ts,[18.919]+[c["power"]["reach"] for c in D["cycles"]],c=COL["Blood"],label="Attack reach (m)")
b.plot(ts,[29.0066]+[c["power"]["budget"]/10 for c in D["cycles"]],c="#60865e",label="Network budget /10 (m)")
for z in [a,b]:z.axvspan(D["witch"]["arrival_s"],D["t"],color="#ead9b0",alpha=.4);z.set_xlabel("Canonical time, seconds")
b.legend(loc="upper left",fontsize=9);b.grid(alpha=.2);save(fig,3)
# 04 four actual progression frames
fig=plt.figure(figsize=(14,16),facecolor="#fbfaf6");fig.suptitle("V4 / 04   Distributed search network progression",fontsize=20,y=.97)
for j,t in enumerate([130,216,280,D["t"]]):
 ax=fig.add_subplot(2,2,j+1);base(ax,labels=False);network(ax,t);ax.set_title(f"T+{t:.0f}  •  physically laid traces")
fig.text(.05,.025,"Squares: search-only secondary nodes. Pale traces: later withdrawn. Frames show geometry laid by that time; final active status is a separate overlay.",fontsize=9)
fig.tight_layout(rect=[0,.04,1,.95]);save(fig,4)
fig,ax,_=shell(5,[f"{MET['shelters_completed_probes']}/41 footprints received a completed threshold probe. A footprint is not automatically an occupied refuge.",f"{MET['secondary_search_nodes']} secondary nodes; {MET['search_reclaims']} low-value branch withdrawals; {MET['search_revisits']} completed revisits.","Memory colour: blue = active/several; purple = strong; grey = empty/low; amber = weak; pale red = recently dispersed.","Unsearched fronts were explored after local value fell. Old observations cannot provide live data after their branch is withdrawn.",f"8m trace-proximity yard coverage proxy: {MET['inhabited_proxy_within_8m_of_any_completed_trace_pct']}%. This is not omniscient detection."])
network(ax,D["t"])
palette={"STRONG PRESENCE":"#7454a2","ACTIVE PRESENCE":"#247b92","EMPTY / LOW VALUE":"#777c75","WEAK / UNCERTAIN":"#c79c46","RECENTLY CLEARED / DISPERSED":"#dd8e96"}
for b,q in D["network"]["searches"].items():
 if b in FEAT:ax.scatter(*q["xy"],s=40,c=palette[q["state"]],edgecolors="white",zorder=10)
save(fig,5)
fig,ax,_=shell(6,[f"Executed burst travel: {MET['body_travel_plan_m']['Bone']:.1f} plan metres across five analytical districts.","Pattern: coop / forge → farms → lower shelter → old quarter → church / guard → estate → upper return → eastern refuges / edge → church.","Each move has an attention trigger. Empty or repetitive local reactions lose value.","Purple dashes are separate bursts, not a clearance itinerary. Purple pins are consequential encounters.","Bone makes 18 direct kills including three approved pre-T90 deaths; no casualty quota was used."])
route(ax,"Bone",1.8);points(ax,"Bone");save(fig,6)
fig,ax,_=shell(7,[f"Bone direct fatalities: 18. Non-Bone deaths with a recorded Bone-caused movement chain: {MET['bone_indirect_fatalities_with_recorded_movement_chain']}.","Purple crosses = direct Bone deaths. Orange rings = deaths by another cause with Bone movement context.","An indirect chain is not reassigned kill credit and is not proof that the later death required Bone.","Examples include pressured farm flight, the driver's gate-side flight, and independently attempted eastern/upper boundaries.","All injury/death records retain person ID, intention, exposure, witnesses, direct cause and the contributing chain."])
route(ax,"Bone",.7,.3)
for c in CAS:
 if c.get("injury"):continue
 if c["killer"]=="Bone":ax.scatter(*c["xy"],marker="x",s=32,c=COL["Bone"],zorder=9)
 elif c["bone_direct_or_chain"]:ax.scatter(*c["xy"],marker="o",s=65,facecolors="none",edgecolors="#d69243",zorder=9)
save(fig,7)
fig,ax,_=shell(8,["+188: close recognition at church approach. +196: protected helper injured. +206: almost-completed rescue interrupted lethally.","+212: route denial at upper junction. +230: intentional weapon-side threat. +238: intervening service guard killed.","+248: gate latch denied. +254: entrance guard personally killed. Total 66 seconds; the sequence moves through several spaces.","The same final second as V3 is coincidental: V4 was sealed before comparison. Recognition, duration, people and route differ.","Fragmented recognition and emotional subjects only. No finalized dialogue or cinematic execution."],(-32,48,66,147))
route(ax,"Bone",1.6,.75,184,255)
gh=[q for q in D["groups"]["entrance-guard"]["history"] if 184<=q["t"]<=254]
ax.plot([q["xy"][0] for q in gh],[q["xy"][1] for q in gh],c="#247b92",lw=1.6,alpha=.7,label="Guard movement")
seen=set()
for e in D["events"]:
 if e["kind"] in ["Bone","Guard recognition"] and 184<=e["t"]<=254 and e["t"] not in seen:
  seen.add(e["t"])
  offset={188:(9,-8),196:(10,-4),206:(-40,12),212:(-46,-10),230:(14,14),238:(-43,-11),248:(12,-15),254:(13,14)}[e["t"]]
  ax.scatter(*e["xy"],c=COL["Bone"],s=45)
  ax.annotate(f"+{e['t']:.0f}",e["xy"],xytext=offset,textcoords="offset points",fontsize=9,bbox={"facecolor":"#fbfaf6","alpha":.9,"edgecolor":"none","pad":1},arrowprops={"arrowstyle":"-","lw":.5,"color":"#7454a2"})
ax.legend(loc="upper right",fontsize=8)
save(fig,8)
fig,ax,_=shell(9,[f"{MET['forced_movement_orders']} recorded forced movement orders involving {MET['people_with_forced_movement']} distinct people.","Blue lines are executed group positions through time. Family/micro memberships remain subsets of the original 170 people.","Visible probes and cumulative damage trigger fresh decisions. People may stay, argue, split, seek another home or choose a perimeter.","Refusal of entry/rescue is not automatically villainy. Only two existing people were assigned exploitative intent.","Source caveat: P02-03/04 were pinned in pasture instead of their assigned western field. Their downstream branch needs correction before canon approval."])
for g in D["groups"].values():
 if len(g["history"])>1:
  a,b=zip(*[q["xy"] for q in g["history"]]);ax.plot(a,b,c=COL["civil"],lw=.65,alpha=.28)
save(fig,9)
fig,ax,_=shell(10,["Grey = intact. Gold = damaged. Orange = breached. Dark red = heavily breached.",f"Final proxy states: {MET['structural_states']}. {MET['breached_or_heavily_breached']} structures breached or heavily breached.","Blood broad corridors and Bone narrow punctures are recorded separately. Cover loss changes subsequent exposure and civilian reactions.","Important limitation: new openings are recorded, but the roof-avoidance navigation graph is not rebuilt through those portals.","No destruction meshes, corpses or final materials were made. This is an editable requirement map."],(-72,76,-72,161))
for b,q in D["structures"].items():geom(ax,shape(FEAT[b]["geometry"]),face=["#b9bab5","#d3b56b","#d88949","#a94843"][q["state"]],edge="#6b6d62",alpha=.9,lw=.6)
save(fig,10)
fig,ax,_=shell(11,["Five actual contacts, each at the saved boundary. No inward random firing.","+130: forest crew and western field pair independently test. +280: service-cart driver. +332: eastern household and upper runner.","Direct B4 belongs only to witnesses. Spoken reports remain reports, not direct experience.","Three barrier deaths have a recorded Bone-caused movement chain; the barrier remains the direct killer.","The map's circles illustrate a local witness neighbourhood, not guaranteed sound/vision through buildings."])
for e in D["events"]:
 if e["kind"]=="Barrier":
  ax.scatter(*e["xy"],s=100,c=COL["Barrier"],marker="X",edgecolors="white");ax.annotate(f"+{e['t']:.0f}",e["xy"],xytext=(6,8),textcoords="offset points",fontsize=10)
  geom(ax,Point(e["xy"]).buffer(20),face=COL["civil"],edge=COL["civil"],alpha=.08)
save(fig,11)
fig,ax,_=shell(12,[f"Remaining route at+90: {D['witch']['length_m']:.3f}m including saved height changes. Speed 1.1 m/s.",f"Arrival +{D['witch']['arrival_s']:.3f}. Mayor secured, then 60 seconds of confrontation.","Gold is one purposeful continuous route. No diversion for civilians, attackers or destruction.","Blood naturally intersects her route at+110 and+134. It flows around her; she does not dodge.","Calmness alone does not reveal guilt to all villagers. The guard's plea is ignored; the Mayor learns responsibility privately."])
witch(ax)
for t in [90,134,188,240,280,306]:
 lengths=D["witch"]["segments_m"];remaining=(t-90)*1.1;pt=D["witch"]["xyz"][-1]
 for a,b,dd in zip(D["witch"]["xyz"],D["witch"]["xyz"][1:],lengths):
  if remaining<=dd and dd>0:pt=[a[i]+(b[i]-a[i])*remaining/dd for i in range(3)];break
  remaining-=dd
 ax.scatter(*pt[:2],c=COL["Witch"],s=55);ax.annotate(f"+{t}",pt[:2],xytext=(6,5),textcoords="offset points",fontsize=9)
save(fig,12)
fig,ax,_=shell(13,["+306.0005: Witch secures Mayor after genuine route timing. Exact restraint is reserved.","Subjects: lover, son, authority, responsibility, village suffering, helplessness, saving him until last.","Final rage strengthens connected search and pressure. It does not grant global perception or speed up Blood's body.","Within the final minute:12 Blood deaths,4 Bone deaths,2 barrier deaths, then Mayor.","The extra minute and rage are not isolated counterfactuals. The unique effect of amplification cannot be assigned to every late casualty."])
ax.remove();z=fig.add_axes([.09,.2,.56,.64]);z.set_xlim(303,369);z.set_ylim(0,5)
lanes={"Witch final death":4,"Witch arrival":4,"Blood":3,"Bone":2,"Barrier":1}
for e in D["events"]:
 if e["t"]>=D["witch"]["arrival_s"] and e["kind"] in lanes:
  y=lanes[e["kind"]];z.scatter(e["t"],y,c=COL.get(e["kind"].split()[0],COL["Witch"]),s=60);z.annotate(f"+{e['t']:.0f}",(e["t"],y),xytext=(0,10),textcoords="offset points",ha="center",fontsize=9)
z.plot([D["witch"]["arrival_s"],D["t"]],[4,4],c=COL["Witch"],lw=4);z.set_yticks([1,2,3,4],["Barrier","Bone","Blood","Witch / Mayor"]);z.set_xlabel("Canonical seconds");z.grid(alpha=.18);save(fig,13)
fig,ax,_=shell(14,["Original population 170. Seven deaths preserved through T+90.","Terminal census: 100 dead, 70 alive, 10 of the survivors injured.","Direct attribution: Blood 76; Bone 18; barrier 5; Witch 1.","Mayor is the final death at+366.0005. No later cleanup or hidden casualty is added.","This is a failed experimental outcome, not approved survivor lore and not proof the requested mechanics can never produce the premise."])
ax.remove();z=fig.add_axes([.09,.22,.56,.62])
times=sorted(set([90,D["t"]]+[c["t"] for c in CAS if c["t"]>=90]))
for killer in ["Blood","Bone","Barrier","Witch"]:
 vals=[sum(c["killer"]==killer and not c.get("injury") and c["t"]<=t for c in CAS) for t in times]
 z.step(times,vals,where="post",label=killer,c=COL[killer],lw=2)
z.step(times,[170-sum(not c.get("injury") and c["t"]<=t for c in CAS) for t in times],where="post",label="Alive",c=COL["civil"],lw=2)
z.axvspan(D["witch"]["arrival_s"],D["t"],color="#ead9b0",alpha=.3);z.legend();z.set_xlabel("Canonical seconds");z.set_ylabel("People");z.grid(alpha=.2);save(fig,14)
fig,ax,_=shell(15,["70 surviving people in 50 remaining subgroups. Ten are injured.","Teal circles: surviving positions; nearby counts are combined within 2 m for readability. Red crosses: fatal event locations, not final body poses.","Many survivors reached different small refuges, remained outside an executed corridor, or used isolated space after local warnings.","Some large shelters were found too late for Blood's body to arrive. Search coverage alone did not solve the time/access bottleneck.","The complete survivor register explains every person's last intention, local knowledge, movement history and provisional survival reason."])
for c in CAS:
 if not c.get("injury"):ax.scatter(*c["xy"],c="#c18080",marker="x",s=12,alpha=.45)
poscounts={}
for q in SUR:
 point=tuple(q["xy"])
 key=next((k for k in poscounts if math.dist(k,point)<2),point)
 poscounts[key]=poscounts.get(key,0)+1
for p,n in poscounts.items():
 ax.scatter(*p,s=28+8*n,c=COL["civil"],edgecolors="white",zorder=10);ax.text(p[0],p[1],str(n),ha="center",va="center",c="white",fontsize=7,zorder=11)
save(fig,15)
fig,ax,_=shell(16,["Future evidence only: search veins, secondary pools, repeated pressure corridors and punctured shelter entrances.","Interrupted aid at the well; the smith's unfinished repair and failed rescue; farm shelter debates and evacuation.","Mobile guard torment follows public approach, junction and formal stairs. The service guard's intervention has a separate cause.","Independent barrier discoveries, an abandoned provisions cart, stolen stall takings, and an isolated B4 witness.","Witch passes two natural Blood intersections untouched and reaches the final confrontation. No assets or corpse poses are authored."])
for j,e in enumerate(D["seeds"]):
 ax.scatter(*e["xy"],s=16,c=COL.get(e["kind"].split()[0],"#90754b"),alpha=.7)
network(ax,D["t"],False);witch(ax);save(fig,16)
(P/"map_index.json").write_text(json.dumps([{"file":n+".png","svg":n+".svg","title":t} for n,t in NAMES],indent=2))
print("Rendered sixteen PNG and SVG sheets")
