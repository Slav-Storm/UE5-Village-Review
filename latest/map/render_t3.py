"""Render only the additive Step 4 action/reception review.
Usage: python render_t3.py MAP_DIRECTORY [T3_OUTPUT_DIRECTORY]
Edit t3_second_action.json; requires matplotlib, numpy, Pillow, shapely.
No UE calls. Prior sources are hash-protected and never rendered over.
"""
import ast,sys,json,hashlib,csv,textwrap
from pathlib import Path
from collections import Counter
import numpy as np
from shapely.geometry import shape,Point,LineString
from matplotlib.patches import Circle
from PIL import Image

HERE=Path(__file__).resolve().parent;BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE;OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
X=json.loads((OUT/'t3_second_action.json').read_text(encoding='utf-8'));T2=json.loads((BASE/'t2_civilian_reactions.json').read_text(encoding='utf-8'));T1=json.loads((BASE/'t1_simulation.json').read_text(encoding='utf-8'))
G={g['id']:g for g in T2['groups']};R={r['group_id']:r for r in X['reception']};A=X['actors'];STOP=X['scope']['canonical_stop_s'];C={c['group_id']:c for c in X['civilian_continuations']}
for n,h in X['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
source=BASE/'render_map.py';tree=ast.parse(source.read_text(encoding='utf-8'));cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in n.targets))
oldargs=sys.argv;sys.argv=['render_map.py',str(BASE)];core={'__file__':str(source)};exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(source),'exec'),core);sys.argv=oldargs
plt=core['plt'];base=core['base'];plain=core['plain'];draw=core['draw_geom'];scalebar=core['scalebar'];D=core['D'];BG=core['BG'];INK=core['INK']
# Pure presentation helpers only, never execute an older renderer's exports.
tree=ast.parse((BASE/'render_t2.py').read_text(encoding='utf-8'));wanted={'note','linearrow','north','textfig'}
from matplotlib.patches import FancyArrowPatch
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted],type_ignores=[]),'inherited_drawing_helpers','exec'),globals())
COL={'blood':'#a72c3e','bone':'#684386','witch':'#087a77','civilian':'#887342','damage':'#ab577c'}
CH={'DIRECT_EXPOSURE':'#b64030','DIRECT_WITNESS':'#a0771c','POSSIBLE_VIEW_AND_SOUND':'#8b9f48','HEARD_LOCAL_IMPACT':'#467f9e','POSSIBLE_DISTANT_SOUND':'#95a8b1','NO_SPECIFIC_UPDATE':'#65696a'}
NAMES={'DIRECT_EXPOSURE':'Physical exposure','DIRECT_WITNESS':'Direct witness','POSSIBLE_VIEW_AND_SOUND':'Possible view + sound','HEARD_LOCAL_IMPACT':'Likely local impact heard','POSSIBLE_DISTANT_SOUND':'Possible distant sound','NO_SPECIFIC_UPDATE':'No specific new report'}
wave=shape(A['blood']['wave_geometry']);force=shape(A['blood']['direct_force_geometry']);rim=shape(X['barrier']['geometry']);obs=[(f['id'],shape(f['geometry'])) for f in D['features'] if f['category'] in ['building','outbuilding']]
assert A['witch']['start_xyz_m']==T2['frozen_supernatural_state']['witch_xyz_m']
assert A['bone']['start_xy_m']==T2['frozen_supernatural_state']['bone']['xy_m']
assert A['blood']['start_xy_m']==T2['frozen_supernatural_state']['blood_xy_m']
assert X['barrier']['geometry']==T1['barrier']['geometry']
assert sum(r['surviving_count'] for r in R.values())==159
assert sum(r['injured_survivors'] for r in R.values())==4
assert len(R)==len(G)==79
assert X['population']['original']==X['population']['living_after']+X['population']['total_fatalities']
assert not X['barrier']['contacts'] and not X['barrier']['responses']
assert not X['church_bell']['ringing_executed'] and X['church_bell']['functional_bell_approved']
assert X['population']['barrier_knowledge_survivors']['B3']==X['population']['barrier_knowledge_survivors']['B4']==0
assert all(c['optimistic_contact_lower_bound_s']>STOP for c in X['barrier']['contact_candidates'])
assert not any(wave.intersection(o).area>.01 for n,o in obs)
checks=[]
for aid in ['blood','witch']:
 g=shape(A[aid]['geometry']);hits=[n for n,o in obs if g.intersection(o).length>.05];assert not hits,(aid,hits);assert rim.contains(g)
 checks.append({'id':aid,'building_crossings':hits,'plan_distance_m':round(g.length,3)})
for c in C.values():
 g=shape(c['geometry']);assert Point(g.coords[0]).distance(Point(G[c['group_id']]['end_xy_m']))<.001
 hits=[n for n,o in obs if g.intersection(o).length>.05];assert not hits,(c['group_id'],hits);assert rim.contains(g)
 checks.append({'id':c['group_id'],'building_crossings':hits,'plan_distance_m':round(g.length,3),'barrier_clearance_m':round(g.distance(rim.boundary),3)})
xyz=np.array(A['witch']['xyz_m']);actual=np.linalg.norm(np.diff(xyz,axis=0),axis=1).sum();assert abs(actual-A['witch']['distance_ground_m'])<.001
for c in X['casualties']:
 assert c['count']<=G[c['group_id']]['count'] and c['origin_cohort']==G[c['group_id']]['origin_cohort']
 assert (force if c['result']=='fatal' else wave).contains(Point(c['xy_m']))
assert all(d['event_id'] in {e['id'] for e in X['events']} for d in X['provisional_damage'])
assert all(r['next_decision'] is None for r in R.values())

def oldpos(g,t):
 p=g['timed_points']
 if t<=p[0]['t_s']:return p[0]['xy_m']
 for a,b in zip(p,p[1:]):
  if a['t_s']<=t<=b['t_s']:
   u=(t-a['t_s'])/(b['t_s']-a['t_s']);return [(1-u)*a['xy_m'][i]+u*b['xy_m'][i] for i in range(2)]
 return p[-1]['xy_m']
def pos(gid,t):
 if t<=105 or gid not in C:return oldpos(G[gid],min(105,t))
 g=shape(C[gid]['geometry']);return list(g.interpolate(g.length*(t-105)/(STOP-105)).coords)[0]
def dots(ax,prefix,reception=False,size=1):
 for gid,r in R.items():
  if r['surviving_count']==0:continue
  color=CH[r['blood_channel']] if reception else '#516769'
  mark=ax.plot(*r['xy_m'],marker='s' if G[gid]['indoor_at_90'] else 'o',mfc=color,mec=BG,mew=.3,ms=(3.4+r['surviving_count']*.22)*size,zorder=40)[0];mark.set_gid(prefix+'_population_'+gid)
  if reception and r['bone_channel']=='DIRECT_WITNESS':
   ring=Circle(r['xy_m'],1.4,fc='none',ec=COL['bone'],lw=1,zorder=43);ring.set_gid(prefix+'_bone_witness_'+gid);ax.add_patch(ring)
def actors(ax,prefix,routes=True):
 draw(ax,rim.boundary,'none',COL['blood'],1.1,28,prefix+'_barrier',ls=(0,(4,3)))
 if routes:
  for aid in ['blood','witch']:linearrow(ax,A[aid]['geometry']['coordinates'],COL[aid],prefix+'_actor_'+aid,1.65)
 for aid,m in [('blood','D'),('witch','D'),('bone','h')]:
  p=A[aid]['end_xyz_m'][:2] if aid=='witch' else A[aid]['end_xy_m'];ax.plot(*p,marker=m,ms=7,mfc=COL[aid],mec=BG,mew=.5,zorder=58)
def attack(ax,prefix):
 draw(ax,wave,COL['blood'],COL['blood'],1,31,prefix+'_wave',alpha=.19)
 draw(ax,force,COL['blood'],COL['blood'],.8,32,prefix+'_force',alpha=.16)
 for c in X['casualties']:
  ax.plot(*c['xy_m'],marker='x' if c['result']=='fatal' else '+',color=COL['blood'] if c['result']=='fatal' else '#bc732f',ms=8,mew=1.7,zorder=65)
 for d in X['provisional_damage']:
  g=shape(d['geometry']);draw(ax,g,'none',COL['damage'],1.1,51,prefix+'_damage_'+d['id'])
def save(fig,name):
 p=OUT/(name+'.png');fig.savefig(p,dpi=250,facecolor=BG);Image.open(p).convert('RGB').quantize(colors=256,dither=Image.Dither.NONE).save(p,optimize=True)
 fig.savefig(OUT/(name+'.svg'),facecolor=BG,metadata={'Title':X['title'],'Description':'Independent Step 4 action and local reception overlay; prior geometry unchanged.'});plt.close(fig)

fig=plt.figure(figsize=(24,20),facecolor=BG)
textfig(fig,.025,.974,'STEP 4  /  THE SECOND SUPERNATURAL RESPONSE',25,bold=True)
textfig(fig,.025,.946,'Canonical +90–109  ·  Responses overlap the approved civilian choices  ·  No free fifteen-second head start  ·  Stop after the +108 impact',10.3,'#60716b')
over=fig.add_axes([.025,.265,.32,.645]);base(over,D['main_extent'],'t3_over');dots(over,'over',False,.9);actors(over,'over');attack(over,'over');north(over,-105,184);scalebar(over,-103,-165,50)
for a,p,s,c in [([4,50],[-76,33],'Blood +108\nOne major surge',COL['blood']),([-33,8.3],[-75,-12],'Bone +96\nDeliberate coop hit',COL['bone']),([23.5,83.7],[67,122],'Bell exists\nOperating access unresolved\nNo ring executed','#8b792d'),([63.7,62],[91,70],'East pair remains inside\nNo barrier contact',COL['blood']),([-64.6,65],[-85,83],'West escape continues\nNo barrier contact',COL['blood'])]:note(over,a,p,s,c,7.6)
plain(over,2,151,'Mayor not reached',7.5,weight='bold');plain(over,28,-124,'FARMLAND APPROACH',7.5,weight='bold')
detail=fig.add_axes([.37,.578,.605,.325]);base(detail,[-23,31,30,59],'t3_centre',True);dots(detail,'centre');attack(detail,'centre');actors(detail,'centre')
for gid in ['R23','R27','R34','R30']:
 pp=[oldpos(G[gid],100),G[gid]['end_xy_m']]
 if gid in C:pp+=C[gid]['geometry']['coordinates'][1:]
 linearrow(detail,pp,COL['civilian'],'centre_continuing_'+gid,1)
for a,p,s,c in [([2,50],[-5.5,57],'R22 · 2 fatalities\nAlready unable to stand',COL['blood']),([3.5,51],[4.3,57],'R26 · 2 fatalities\nNeighbours helping',COL['blood']),([8,51.5],[17,55],'R34 · 2 injured\nArriving porch helpers','#b46b29'),(pos('R23',108),[24,58],'Supported pair keeps moving\nBoth beyond this sweep',COL['civilian']),([-1.2,47],[-15,47],'Blood: +98 selection\n+98–101 short advance\n+108 heavy surge',COL['blood']),([2.51,46.10],[21,39],'Witch +109\nWalk continues; no hit',COL['witch']),([-15.56,36.37],[-13.5,33],'Witch +90\nM04 calls as she walks away',COL['witch'])]:note(detail,a,p,s,c,8)
plain(detail,6,34,'TAVERN · NOT ATTACKED',8,weight='bold');scalebar(detail,17,32,5)

bone=fig.add_axes([.37,.269,.267,.266]);base(bone,[-45,-1,-18,19],'t3_bone',True);dots(bone,'bone_detail',False,1.1)
linearrow(bone,A['bone']['strike_geometry']['coordinates'],COL['bone'],'bone_precise_strike',1.5);bone.plot(*A['bone']['start_xy_m'],'h',ms=8,color=COL['bone'],zorder=55);bone.plot(*A['bone']['target_xy_m'],'x',ms=8,color=COL['damage'],zorder=59)
note(bone,[-34.3,9.2],[-30,16],'M05 · both alive\nProtection remains his focus',COL['bone'],7.5)
note(bone,[-33.0119,8.3316],[-29,0],'Exact hit on coop timber\nNo accidental miss / no injury',COL['bone'],7.5)
note(bone,[-39.5,11.7],[-40,17],'M07 can witness\nfrom close workfront','#8f793a',7.3)
plain(bone,-27.4,5.2,'Family inside\nCalls through wall',7);scalebar(bone,-43,1,5)
textfig(fig,.66,.527,'ONE CAUSAL PASS',12,bold=True)
for y,t,s in [(.503,'+90','Witch continues walking. Civilian choices begin.\nBlood reorients; Bone attends to M05.'),(.449,'+96','Bone deliberately punctures coop timber.\nThe parent and child remain alive.'),(.395,'+98–101','Blood chooses the growing eastern aid pocket\nand makes a short, deliberate advance.'),(.341,'+108','One broad surge. Four fatalities, two new injuries.\nSupported pair has continued out of its footprint.'),(.287,'+109','Local impact/sound can register. Stop now.\nNo subsequent civilian decision is chosen.')]:
 textfig(fig,.66,y,t,10,COL['blood'] if t=='+108' else INK,True);textfig(fig,.723,y,s,8.8,'#60716b')
textfig(fig,.025,.224,'159 LIVING  /  4 INJURED AMONG THEM',12,bold=True)
textfig(fig,.025,.202,'Four new fatalities. Two previously injured people die; two helpers are newly injured.\nThe surviving injury count stays four. Event marks are not final corpse poses.',9,'#60716b')
textfig(fig,.54,.223,'BARRIER: NO CONTACT  /  B3 = 0  /  B4 = 0',12,bold=True)
textfig(fig,.54,.201,'Earliest optimistic contact bound is after +122 at the same pace.\nDo not extend this pass merely to demonstrate the barrier.',9,'#60716b')
textfig(fig,.025,.145,'READING THE ACTION',11,bold=True)
textfig(fig,.025,.124,'Red: Blood advance / broad force envelope. Darker red: central force. Violet: one precise Bone incident. Teal: the unchanged main-road Witch route.\nOchre: already-chosen civilian motion. Pink: damage only where these actions physically intersect existing objects.',9,'#60716b')
textfig(fig,.025,.076,'The Witch is about 1 m behind the wave envelope at impact; no split/meld event is forced. No building footprint is intersected by this strike.',9,'#60716b')
textfig(fig,.025,.047,'Same healthy survey, map north = UE +X / uphill. Horizontal metres. No UE edits, final damage assets, full escape paths or Step 5 reactions.',9,'#60716b')
save(fig,'10_T3_second_action')

fig=plt.figure(figsize=(24,20),facecolor=BG)
textfig(fig,.025,.974,'STEP 4  /  WHO RECEIVES WHICH EVENT?',25,bold=True)
textfig(fig,.025,.945,'Local sight and sound at the +109 handoff  ·  Global alarm is not global understanding  ·  No post-event warning journeys or civilian decisions',10.3,'#60716b')
ax=fig.add_axes([.025,.228,.435,.683]);base(ax,D['main_extent'],'t3_reception')
for radius,color in [(85,'#94a8b5'),(45,'#517e9f')]:
 p=Circle([4,50.5],radius,fc='none',ec=color,lw=1.2,ls=(0,(3,3)),zorder=25);p.set_gid('listening_review_band_'+str(radius));ax.add_patch(p)
actors(ax,'reception',False);dots(ax,'reception',True,1.25)
ax.plot(4,50.5,'*',ms=12,color=COL['blood'],zorder=58);ax.plot(*A['bone']['target_xy_m'],'*',ms=10,color=COL['bone'],zorder=58)
north(ax,-105,184);scalebar(ax,-103,-164,50)
note(ax,[4,50.5],[68,17],'Blood +108\nLocal force / crash',COL['blood'],8)
note(ax,[-34.3,9.2],[-78,-15],'Bone +96\nDirect: M05 + M07\nFamily hears through wall',COL['bone'],8)
note(ax,[23.5,83.7],[76,116],'Caretaker: possible distant view\nFunctional bell / no ringing','#8b792d',7.5)
note(ax,[2,146],[72,158],'Mayor / indoor staff\nNo specific new report','#62696b',7.5)
plain(ax,28,-114,'Farms retain earlier warnings;\nno new detailed attack account',7.3)

z=fig.add_axes([.497,.624,.478,.284]);base(z,[-23,29,47,67],'t3_reception_detail',True);dots(z,'reception_detail',True,1.2);attack(z,'reception_detail');actors(z,'reception_detail',False)
note(z,[4,50.5],[-6,63],'Direct local witness group\nExposure counted separately','#9d7422',8)
note(z,[4,37],[17,31],'Tavern interiors hear another impact\nNo wall-penetrating knowledge','#467f9e',8)
note(z,[37.7,51.9],[36,62],'M09: possible view + sound\nNot an exact casualty count','#718738',7.8)
scalebar(z,-20,31,10)
textfig(fig,.497,.606,'BLOOD EVENT  /  SURVIVING RECIPIENTS',11,bold=True)
totals=Counter({k:0 for k in CH})
for r in R.values():totals[r['blood_channel']]+=r['surviving_count']
for i,k in enumerate(CH):
 y=.58-i*.032;textfig(fig,.50,y,f'{totals[k]:>3}  {NAMES[k]}',10,CH[k],True)
textfig(fig,.497,.366,'RECEPTION DOES NOT EQUAL A NEW PLAN',11,bold=True)
textfig(fig,.497,.343,'Direct witnesses receive a local event, not the monsters’ full abilities.\nIndoor listeners hear force/cries without exact casualty counts.\nPossible distant views depend on light, attention and terrain.\nThe two circles are listening review bands, not exact acoustic limits.',9.7,'#60716b')
textfig(fig,.497,.254,'BONE: ONLY THE NEARBY POCKET',11,bold=True)
textfig(fig,.497,.231,'M05 (2): direct target-side witnesses, still alive.\nM07 (2): close open workfront can see/hear the precision threat.\nR15 (3): a wooden crack through the house wall; exact cause unclear.\nOther groups retain their prior Bone knowledge. No new global relay.',9.7,'#60716b')
textfig(fig,.025,.192,'BARRIER KNOWLEDGE AMONG 159 SURVIVORS',11,bold=True)
textfig(fig,.025,.17,'B0 72  /  B1 78  /  B2 9  /  B3 0  /  B4 0\nThe count change is four deaths, not knowledge spreading.\nNo contact event, no local lethal-contact witnesses.',9.5,'#60716b')
textfig(fig,.025,.093,'CHURCH BELL: EXISTS, BUT NO EXECUTED RING',11,bold=True)
textfig(fig,.025,.071,'The approach reaches the church entrance. Rope/control access is not mapped. A ground-floor pull could permit ringing around +100, conditionally;\nthat is not an event or an audible alarm zone on this sheet. No magical information, monster location or safe destination is communicated.',9,'#60716b')
textfig(fig,.025,.034,'Stop at the immediate +109 reception state. Step 5 will choose what survivors do with these unequal fragments of information.',9.5,'#60716b')
save(fig,'11_T3_event_reception')

def table(h,rows):return '| '+' | '.join(h)+' |\n|'+'|'.join(['---']*len(h))+'|\n'+'\n'.join('| '+' | '.join(str(v).replace('|','/').replace('\n',' ') for v in row)+' |' for row in rows)+'\n'
def pt(p):return '('+', '.join(f'{v:.2f}' for v in p)+')'
rank=sorted(A['blood']['selection_inventory'],key=lambda c:(c['priority_tier'],c['distance_range_m'][0]))
# Close passage/walking comparisons use concurrent positions, not the frozen review marker.
witpoints=A['witch']['timed_points']
def wp(t):
 for a,b in zip(witpoints,witpoints[1:]):
  if a['t_s']<=t<=b['t_s']:
   u=(t-a['t_s'])/(b['t_s']-a['t_s']);return [(1-u)*a['xyz_m'][i]+u*b['xyz_m'][i] for i in range(2)]
 return witpoints[-1]['xyz_m'][:2]
near={gid:min((Point(pos(gid,float(t))).distance(Point(wp(float(t)))),float(t)) for t in np.linspace(90,109,381)) for gid in ['R31','R33']}

notes=f'''# MASSACRE PLANNING — STEP 4 / SECOND SUPERNATURAL ACTION

Authored **{X['authored_utc']}**. This additive 2D pass uses the approved design bible and T0 → T1 → Step2B → Step3 causal chain. **No UE scene changes.**

- [10 — second action](10_T3_second_action.png), [SVG](10_T3_second_action.svg)
- [11 — local event reception](11_T3_event_reception.png), [SVG](11_T3_event_reception.svg)
- [Editable action layer](t3_second_action.json), [recipient CSV](t3_reception.csv), [validation manifest](t3_manifest.json)
- [Approved civilian reaction](T2_CIVILIAN_REACTIONS.md), [unchanged base](01_village_base_map.png), [clean canvas](02_massacre_planning_blank.png)

**Result: 159 living ordinary villagers, including four injured.** Blood's one second strike causes four new fatalities and two new injuries. Two of the prior injured die; the other two survive, so the number of injured survivors remains four. Bone hits coop timber deliberately and leaves M05 alive. No one contacts the barrier. The functional church bell is approved, but no ringing is invented through unresolved control access.

## 1. Canonical timing: remove the planning freeze

**Canonical window: +90–109.** Actors resume at their exact +90 positions while the approved civilian +90–105 knots occur concurrently. Step3's static actor markers were review references, not fifteen seconds of literal inactivity. No civilian knot shifts earlier, no one receives extra distance, and all civilian choices remain intact. Fourteen explicit continuations extend already-chosen motion by at most four seconds; they contain no new destination choice.

Blood assesses the developing pocket before all helpers arrive. Bone responds to the parent's existing protective reaction. The Witch walks continuously from +90. This uses Step3 as causal input without treating its future endpoint as instant knowledge for the actors.

| Canonical time | Event / activity |
|---|---|
| +90 onward | Witch resumes the same main-road walk at 1.1 m/s; M04 calls as she goes. Blood reorients toward local movement/cries. Bone remains actively engaged with M05. |
| +92–98 | Blood compares local concentrations as the existing civilian choices begin; no new attack yet. |
| +96 | Bone aims one exact strike into the coop beside M05. Nobody is hit. He observes the still-living pair afterward; no next civilian choice is simulated. |
| +98 | Blood selects eastern injury/help activity: six already close, two more approaching. |
| +98–101 | Blood advances {shape(A['blood']['geometry']).length:.2f} m deliberately to {pt(A['blood']['end_xy_m'])}. |
| +101–108 | One heavy, deliberate attack preparation and release. This is working staging, not a locked combat cooldown. |
| +105 | All eight are momentarily near the eastern aid area, but the supported injured person and escort keep moving. |
| +108 | The single broad surge reaches six still in its footprint. Four central-force fatalities; two outer-sweep injuries. The moving pair is beyond the forward edge. |
| +109 | Immediate local impact/sound can register. Blood is recovering from the second strike, Bone has no new selected action, Witch has kept walking. Stop before new civilian decisions. |

The nominal +125/+135 horizon is not forced: this +108 impact creates the clean earlier reaction boundary. One second accommodates immediate sensory receipt; it is not a new warning journey or group decision. The next pass starts from a common **+109** time, not a split civilian/actor clock.

## 2. Blood: compare physical concentrations

**Selected: C01, the eastern injury/help pocket.** The serious alternative is **C06: six people by the western frontage**—the two-person escort plus four nearby warning/hesitating neighbours. Different intentions do not prevent physical concentration, so those six are considered together for target comparison while retaining their separate civilian records.

The eastern six are tighter around assistance activity, with two more people visibly approaching from the tavern. It is a growing, locally perceptible mass near Blood's existing position. The western six are spread across the frontage. Selection does not depend on pretending the western pocket has only two people or giving Blood exact indoor headcounts. Close movement and cries can reveal a concentration even where final practical lighting remains unresolved.

The tavern contains seven known-to-the-planner people indoors, but Step3 allocates them as a three-person queue and a four-person shelter group. Their indoor connection/visibility is not established. Blood can perceive evidence of occupancy through sound, not seven targets through the roof. The receiving group is separately on the service side. The old-quarter five are behind buildings; the three authority seekers are moving farther uphill. Farmland, upper homes and the estate remain real populations but are not locally sensed targets.

The full inventory below evaluates every two-or-more existing reaction subgroup, the existing emerging groups split where physically necessary, and the close western aggregate. Singles do not become imaginary crowds merely because they share a cohort label. **Priority tiers are qualitative judgements, not an AI kill-efficiency score.**

'''+table(['Tier / candidate','Planner population','Range from Blood at +98','Reason'],[(str(c['priority_tier'])+' / '+c['id']+' '+c['label'],c['planner_count'],f"{c['distance_range_m'][0]:.1f}–{c['distance_range_m'][1]:.1f} m",c['reason']) for c in rank])+f'''
## 3. Blood action, motion and immediate consequences

The attack is one broad forward surge across approximately **{wave.area:.1f} m²**, with a denser central-force region and a lower-force fringe. It moves across the remaining eastern assistance activity rather than surgically acquiring isolated people. The direction stays north/northeast of Blood's short advance. Its provisional envelope intersects existing market timber/goods and **no building footprint**.

The chosen concentration is not frozen for convenience: R23 and R27 continue the supported +100–105 movement at the same final segment velocities. At impact they are {pt(pos('R23',108))} and {pt(pos('R27',108))}, outside the wave. R22 cannot stand; R26 is beginning assistance; R34 has arrived from the porch and is starting to help. Those six remain exposed because of their existing activities. No rescuer's later flight or new choice is pre-authored.

'''+table(['Origin / subgroup','People','Impact position','What they were doing / exposure','Immediate result'],[(c['origin_cohort']+' / '+c['group_id'],c['count'],pt(c['xy_m']),c['exposure'],c['result']) for c in X['casualties']])+'''
Fatality/injury severity is a provisional physical judgement about central force versus fringe exposure, not a calibrated health model. R34's two people have impaired movement/balance; Step5 must assess what they try and what assistance is possible. No final corpse poses, debris landings or eventual outcomes are assigned.

## 4. Bone: attention candidates and one chosen incident

'''+table(['Stimulus','Source','Distance at +94','Occlusion / reason'],[(s['id']+(' SELECTED' if s['selected'] else ''),', '.join(s['groups']),', '.join(k+': '+str(v)+' m' for k,v in s['distances_m'].items()),s['reason']+' Blockers: '+str(s['occluding_buildings'])) for s in A['bone']['attention_candidates']])+f'''
**Bone keeps M05 as his focus.** The parent remains a few metres away, shielding the child. The family calls inside Cottage_04 are a possible close sound through a wall; M07 is also nearby at the open workfront. Neither forces a target switch. Distant running and children on the other side of houses are not magically available stimuli.

At **+96** he hits existing coop timber at **{pt(A['bone']['target_xy_m'])}** from **{pt(A['bone']['start_xy_m'])}**. The precise line passes beside the group's planning anchor, not through either person's assigned position. It is a deliberate threatening object strike; **he does not accidentally miss**. One local puncture and wooden crack are the only physical effects. No civilian is injured and no new movement burst occurs.

He remains at the same ground position because the living pair's constrained protective reaction continues to interest him. This is active torment/observation, not a fifteen-second canonical freeze. No exposition or new family-memory claim is added. At +109 his current encounter is still M05; the centre crash has become a possible fresh cue, but his next attention decision is unchosen.

M05 directly experiences it. The smith/apprentice M07 has a close open plan-view line and can newly witness the precision threat; this is a **local information change**. The three household occupants R15 hear a short impact through the wall, without learning Bone's exact position or their relatives' fate. No broader relay occurs.

## 5. Witch: continuous destination movement

The Witch covers **{A['witch']['distance_ground_m']:.1f} m along the saved road height profile**, without running, stopping, helping or diverting. Her inherited starting z and point are exact. Her +109 position is **{pt(A['witch']['end_xyz_m'])} m** (x, y, z), still at the centre approach and far short of the Mayor's formal stairs.

'''+table(['Time','Map x / y / z'],[(p['t_s'],pt(p['xyz_m'])) for p in A['witch']['timed_points'] if p['t_s'] in [90,96,100,105,108,109]])+f'''
M04 keeps the approved appeal intent and tiny step; the Witch ignores them while walking away. The initial distance is about 2.8 m, but Step3's statement that they end 1.6 m from her described a **frozen reference**. Under concurrent movement that final closeness no longer occurs. At +109 they remain at their short-step endpoint and do not chase her. No explanatory dialogue, healing, blame or knowledge of her immunity is added.

R31's homeward pair passes in the same district: their closest synchronous distance is approximately **{near['R31'][0]:.2f} m around +{near['R31'][1]:.1f}**. They do not physically cross her body path or force avoidance. No crowd is relocated for an encounter.

At Blood's impact the Witch is approximately **{A['witch']['distance_from_wave_at_impact_m']:.2f} m behind the mapped wave edge**, with no plan-envelope intersection. Consequently **no split/meld effect is staged**. Her immunity and the rule that her own supernatural blood would flow around her remain locked for an actual future intersection. She passes near the existing first-strike area; she does not dodge toward a safer route.

## 6. Barrier eligibility: no contact in this window

'''+table(['Group','People','Clearance at +105','Same pace','Optimistic earliest contact bound','Contact by +109'],[(c['group_id'],c['count'],str(c['remaining_clearance_at_105_m'])+' m',str(c['speed_cap_m_s'])+' m/s',str(c['optimistic_contact_lower_bound_s'])+' s','No') for c in X['barrier']['contact_candidates']])+'''
The fastest eligible bound is **R58 after about +122.5**, even using straight-line distance to the closest rim. Real woodland navigation can make it later. R70 is nearer to the rim, but its cautious 0.4 m/s pace puts its optimistic bound around +129.8. Nobody is accelerated to demonstrate the weapon. These are reachability bounds, **not scheduled future contact events** or completed escape routes.

No person touches/crosses; no localized attack triggers; there are no direct lethal-contact witnesses. **B3 = 0 and B4 = 0.** People merely near the barrier are not struck. The capability remains contact-reactive and opaque/sealed, unchanged from the locked rules.

## 7. Church bell: approved feature, unresolved control access

The user has now approved an ordinary functional village bell. This is recorded in the separate Step4 layer as an addition to the healthy narrative reference; the old source maps and UE geometry remain unchanged.

The known public approach runs from the caretaker at **(23.5, 83.7)** through the gate to the entry at **(23.5, 86.4)**. The model has bell-opening proxies near y=89.2, but no mapped rope, pull control, interior stair or usable route to the operation point. Existence of the bell does not prove its operating access.

**No ring is executed in this pass; actual ringing time is null.** If an accessible ground-floor pull sits just inside that existing entrance, a decision around +92, approximately 2.7 m of walking at 1 m/s and roughly five seconds to grasp/pull could yield a first ring around **+100**. That is an explicit conditional earliest staging estimate, not an event. An upper-only control would take longer and needs its route resolved. The caretaker keeps the existing public-threshold help intention, with no invented teleport or climb.

No bell audibility zone or bell-based knowledge upgrade is drawn. When access is resolved, its meaning remains only extraordinary public alarm—not who caused the disaster, where either creation is, barrier lethality or which refuge is safe.

## 8. Local event reception at the stop

No full verbal propagation follows either event. Direct receipt, a possible view, hearing a crash and detailed understanding are distinct. The reception CSV records every surviving/deceased source subgroup separately; old knowledge persists where no new channel is established.

'''+table(['Blood event channel','Living recipients','Reaction records'],[(NAMES[k],totals[k],', '.join(r['group_id'] for r in R.values() if r['blood_channel']==k and r['surviving_count'])) for k in CH])+'''
Direct witnesses are working close plan-view staging, not verified 3D/lighting rays. Possible views are deliberately weaker claims. The 45 m local / 85 m possible-distant circles are **review bands, not exact acoustic cutoffs**; an interior hears muffled force and cries, not automatically an attacker identity or body count. Groups outside the band may hear an indistinct noise, but receive no specific event report in this authored pass. Ordinary exterior light is still blocked; no new magical global sensing is assumed.

Tavern interiors hear a renewed nearby impact, without seeing through walls. The receiving group remains service-side. M09 and the caretaker may have open distant sight plus sound but do not learn precise casualties by fiat. The Mayor/indoor estate staff and most lower farm workers retain their earlier emergency awareness without a new detailed attack report. M04 retains its earlier direct Bone-interception knowledge; neither that fact nor this new crash gives them his current position.

Bone reception is restricted to M05 (two direct witnesses), M07 (two close workfront witnesses) and R15 (three possible wall-muffled listeners). The +108 centre crash can become a possible sound for Bone by the stop, but it does not choose his next action.

'''+table(['Original cohort','Living at +109','New Blood reception within that cohort'],[(pid,sum(r['surviving_count'] for r in R.values() if r['origin_cohort']==pid),'; '.join(f"{NAMES[k]}: {sum(r['surviving_count'] for r in R.values() if r['origin_cohort']==pid and r['blood_channel']==k)}" for k in CH if any(r['origin_cohort']==pid and r['blood_channel']==k and r['surviving_count'] for r in R.values()))) for pid in T2['population']['origin_cohort_counts']])+'''
## 9. Causal damage only

'''+table(['Marker','Existing feature','Cause','Provisional change'],[(d['id'],d['feature_id'],d['event_id'],d['description']) for d in X['provisional_damage']])+'''
The first Blood strike already damaged one unspecified light market frame. Intersected timber here may include surviving parts of that earlier damage; no new intact market reconstruction is assumed. No house wall is intersected by the second envelope. No decorative rubble, supernatural structure, final mesh or corpse pose is added to UE or the clean planning map.

## 10. Concentrations and next-stimulus handoff

The action **breaks** the eastern assistance concentration. It does not automatically summon more helpers.

'''+table(['Pocket','People','State'],[(h['id']+' / '+', '.join(h['groups']),h['count'],h['description']) for h in X['post_action_concentrations']])+'''
Other houses, road streams and distant farm groups retain their prior membership and intent, with only the explicit short continued movements in the JSON. They are not silently merged into new crowds. No person decides to turn, flee a new direction, shout a new report, reach a new door or help R34 after this second strike; those are Step5 decisions.

Potential inputs for the **next** Bone decision are the renewed public crash, the living M05 pair after the deliberate object strike and M07's newly local awareness. A future shout/run/closure is not invented. Blood has no next selected concentration. The Witch's route remains Mayor-bound. Barrier contact candidates are still untested.

## 11. Assumptions for review

'''+ '\n'.join(f'{i+1}. {s}' for i,s in enumerate(X['assumptions']))+'''

The main staging choices to review are the eastern-versus-western concentration comparison, the wave's provisional force/exposure outcome, Bone choosing further torment rather than a kill, and the bell operating-access gap. These are documented review assumptions, not permission to advance Step5 automatically.

## 12. Editability, verification and stop

`t3_second_action.json` holds the independent event timeline, full target inventory, attention candidates, timed Witch route, wave/precision-hit geometry, civilian continuations, exposure outcomes, damage links, contact bounds, bell approval/access condition and per-subgroup reception. Apply it after the unchanged T2 source. Counts and reception are overrides/references, not additional civilians.

Run `python render_t3.py .` in this folder to regenerate only 10/11 PNG/SVG, these notes, the reception CSV and the T3 manifest. All **41 prior map/source files are hash-protected and byte-identical**. No historical layer is overwritten; the clean annotation template remains empty. The geometry is still the same healthy-village survey, up = UE +X, right = UE +Y, metres in plan. Witch travel also uses the saved height samples. New movement traces clear projected building footprints; lighting, small obstacles, acoustics and actual character clearance remain later scene checks.

**Stop at +109, before STEP 5 — SECOND CIVILIAN REACTION.** Use 159 survivors, four injured, the exact updated actor positions, local reception and existing intentions. Do not grant village-wide barrier knowledge, advance a second Blood target, choose Bone's next stimulus, reach the Mayor or continue the full massacre.
'''
(OUT/'T3_SECOND_ACTION.md').write_text(notes,encoding='utf-8',newline='\n')
cols=['group_id','origin_cohort','original_count','surviving_count','injured_survivors','xy_m','blood_channel','blood_information','distance_to_blood_event_m','blood_roof_obstructions','bone_channel','bone_information','distance_to_bone_event_m','bone_roof_obstructions','barrier_before','barrier_after','barrier_contact_information','bell_information','movement_source','next_decision']
with (OUT/'t3_reception.csv').open('w',newline='',encoding='utf-8') as fp:
 w=csv.DictWriter(fp,fieldnames=cols,lineterminator='\n');w.writeheader()
 for r in R.values():w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],(list,dict)) else r[k] for k in cols})
files=['10_T3_second_action.png','10_T3_second_action.svg','11_T3_event_reception.png','11_T3_event_reception.svg','t3_second_action.json','render_t3.py','T3_SECOND_ACTION.md','t3_reception.csv']
for n,h in X['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
manifest=dict(schema='t3-review/v1',files={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in files},image_dimensions={n:list(Image.open(OUT/n).size) for n in files if n.endswith('.png')},source_files_unchanged={n:True for n in X['source_sha256']},geometry_sha256=D['geometry_sha256'],canonical_window_s=[90,109],impact_s=108,population=X['population'],blood_candidates=len(rank),bone_candidates=len(A['bone']['attention_candidates']),barrier_contacts=0,bell_rung=False,church_bell_approved=True,building_footprints_hit_by_wave=[],movement_checks=checks,ue_edits=False,step5_executed=False)
(OUT/'t3_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'rendered':manifest['image_dimensions'],'protected':41,'living':159,'injured':4,'new_fatalities':4,'new_injuries':2,'reception_totals':dict(totals),'witch_ground_distance':actual,'witch_nearby_civilians':near},indent=2))
