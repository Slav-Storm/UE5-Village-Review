"""Regenerate only the separate T2 civilian reaction review and derived notes.
Usage: python render_t2.py MAP_DIRECTORY [T2_OUTPUT_DIRECTORY]
Requires matplotlib, numpy, Pillow, shapely. No UE calls, no new simulation.
Edit t2_civilian_reactions.json; this renderer validates and visualizes it.
"""
import ast, sys, json, hashlib, csv, textwrap
from pathlib import Path
from collections import Counter
from shapely.geometry import shape, Point, LineString, box
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse
from PIL import Image

HERE=Path(__file__).resolve().parent
BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
X=json.loads((OUT/'t2_civilian_reactions.json').read_text(encoding='utf-8'))
S=json.loads((BASE/'t1_simulation.json').read_text(encoding='utf-8'))
BX=json.loads((BASE/'bone_completion.json').read_text(encoding='utf-8'))
T0=json.loads((BASE/'t0_activity.json').read_text(encoding='utf-8'))
G=X['groups'];GI={g['id']:g for g in G};CG=X['concentrations'];CI={c['id']:c for c in CG};FIX=X['frozen_supernatural_state']
for n,h in X['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
source=BASE/'render_map.py';tree=ast.parse(source.read_text(encoding='utf-8'))
cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in n.targets))
oldargs=sys.argv;sys.argv=['render_map.py',str(BASE)];core={'__file__':str(source)}
exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(source),'exec'),core);sys.argv=oldargs
plt=core['plt'];base=core['base'];plain=core['plain'];draw=core['draw_geom'];scalebar=core['scalebar'];D=core['D'];BG=core['BG'];INK=core['INK']
COL={'ESCAPE':'#bb6238','SEEK AUTHORITY':'#7762a3','SEEK FAMILY':'#2f7f7c','SEEK SHELTER':'#4d7198','HELP':'#9a761b','FREEZE / DELAY':'#58605c','FOLLOW OTHERS':'#8d7664'}
ACT={'Blood':(FIX['blood_xy_m'],'#a42e40','D'),'Witch':(FIX['witch_xyz_m'][:2],'#087d79','D'),'Bone':(FIX['bone']['xy_m'],'#674087','h')}
SYMBOL={'B0':'o','B1':'s','B2':'^'}

# Validate actual handoff, census, injuries, timing, immutable inputs and movement.
assert FIX['blood_xy_m']==BX['preserved_handoff']['blood']
assert FIX['witch_xyz_m']==BX['preserved_handoff']['witch']
assert FIX['bone']==BX['bone']['handoff']
assert FIX['barrier_geometry']==S['barrier']['geometry']
assert all(v is None for v in FIX['next_major_actions'].values())
assert X['scope']['new_attacks']==X['scope']['barrier_contacts']==X['scope']['final_fates']==[]
assert X['scope']['start_s']==90 and X['scope']['stop_s']==105
assert sum(g['count'] for g in G)==163 and sum(g['injured_count'] for g in G)==4
assert len(GI)==len(G)
assert Counter({p:sum(g['count'] for g in G if g['origin_cohort']==p) for p in X['population']['origin_cohort_counts']})==Counter(X['population']['origin_cohort_counts'])
assert all(g['barrier_knowledge_at_90'] in SYMBOL and g['barrier_knowledge_at_105'] in SYMBOL for g in G)
assert X['barrier_knowledge_counts_at_90']['B3']==X['barrier_knowledge_counts_at_90']['B4']==0
micro_positions={m['micro_id']:m['positions']['90'] for m in BX['resolved_micro_groups'] if m['micro_id']!='M01'}
micros=Counter()
for g in G:
 for mid,n in g['micro_membership'].items():
  micros[mid]+=n;assert Point(g['start_xy_m']).distance(Point(micro_positions[mid]))<.01,(g['id'],mid)
assert dict(micros)==X['population']['micro_counts']
co=Counter();bc=Counter({f'B{i}':0 for i in range(5)})
for g in G:co[g['intent']]+=g['count'];bc[g['barrier_knowledge_at_90']]+=g['count']
assert dict(co)==X['intent_breakdown'] and dict(bc)==X['barrier_knowledge_counts_at_90']
bar=shape(FIX['barrier_geometry']);obstacles=[(f['id'],shape(f['geometry'])) for f in D['features'] if f['category'] in ['building','outbuilding']]
checks=[]
for g in G:
 geom=shape(g['geometry']);assert bar.contains(geom),(g['id'],'outside rim')
 assert Point(g['timed_points'][0]['xy_m']).distance(Point(g['start_xy_m']))<.001
 assert Point(g['timed_points'][-1]['xy_m']).distance(Point(g['end_xy_m']))<.001
 assert g['timed_points'][-1]['t_s']==105
 assert all(90<=p['t_s']<=105 for p in g['timed_points'])
 hits=[]
 if geom.geom_type=='LineString':
  hits=[(n,round(geom.intersection(o).length,4)) for n,o in obstacles if geom.intersection(o).length>.05]
  assert not hits,(g['id'],hits)
  assert 90<=g['movement_start_s']<g['movement_stop_s']<=105
  assert g['mean_plan_speed_m_s']<=2
  for a,b in zip(g['timed_points'],g['timed_points'][1:]):
   assert b['t_s']>a['t_s'];assert Point(a['xy_m']).distance(Point(b['xy_m']))/(b['t_s']-a['t_s'])<2.1
 checks.append(dict(group=g['id'],distance_m=round(geom.length,3),building_crossings=hits,barrier_clearance_m=round(geom.distance(bar.boundary),3),start_refinement=g['start_refined_within_existing_area']))
for c in CG:
 assert c['count']==sum(GI[i]['count'] for i in c['members'])
 assert c['blood_target_selected'] is False
assert len([i for c in CG for i in c['members']])==len(set(i for c in CG for i in c['members']))
assert GI['R14']['start_xy_m']==GI['R14']['end_xy_m']
assert min(c['barrier_clearance_m'] for c in checks)>0

def note(ax,anchor,pos,s,color=INK,size=8,gid='note',align='center'):
 a=ax.annotate(s,xy=anchor,xytext=pos,fontsize=size,color=color,ha=align,va='center',zorder=70,
   bbox=dict(boxstyle='round,pad=.28',fc=BG,ec=color,lw=.5,alpha=.98),arrowprops=dict(arrowstyle='-',color=color,lw=.65,shrinkA=3,shrinkB=3))
 a.set_gid(gid);return a
def linearrow(ax,coords,color,gid,lw=1.4):
 g=LineString(coords);draw(ax,g,'none',color,lw,40,gid)
 a=g.interpolate(max(0,g.length-1.4));b=g.interpolate(g.length)
 arrow=FancyArrowPatch(a.coords[0],b.coords[0],arrowstyle='-|>',mutation_scale=10,lw=.8,color=color,zorder=43);arrow.set_gid(gid+'_arrow');ax.add_patch(arrow)
def fixed(ax,prefix,labels=False):
 draw(ax,bar.boundary,'none','#a42e40',1.5,32,prefix+'_frozen_barrier',ls=(0,(5,2)))
 for name,(pos,color,m) in ACT.items():
  artist=ax.plot(*pos,marker=m,mfc=color,mec=BG,mew=.7,ms=8,zorder=61)[0];artist.set_gid(prefix+'_fixed_'+name)
  if labels:plain(ax,pos[0]+2,pos[1]-3,name+' · fixed',7,ha='left',color=color,weight='bold')
def population(ax,prefix,arrows=True,size=1):
 for g in G:
  p=g['end_xy_m'];col=COL[g['intent']]
  if arrows and g['distance_m']:
   start=g['start_xy_m'];ax.plot(*start,'o',mfc=BG,mec=col,ms=2.3*size,mew=.65,zorder=38)
   linearrow(ax,g['geometry']['coordinates'],col,prefix+'_reaction_'+g['id'],1.15*size)
  m=SYMBOL[g['barrier_knowledge_at_105']]
  mark=ax.plot(*p,marker=m,mfc=col,mec=BG,mew=.4,ms=(3.2+g['count']*.22)*size,zorder=49)[0];mark.set_gid(prefix+'_population_'+g['id'])
def north(ax,x,y):
 ax.annotate('N / +X',xy=(x,y),xytext=(x,y-19),ha='center',fontsize=7.5,weight='bold',arrowprops=dict(arrowstyle='-|>',color=INK,lw=.9),color=INK,zorder=72)
def save(fig,name):
 png=OUT/(name+'.png');fig.savefig(png,dpi=250,facecolor=BG)
 Image.open(png).convert('RGB').quantize(colors=256,dither=Image.Dither.NONE).save(png,optimize=True)
 fig.savefig(OUT/(name+'.svg'),facecolor=BG,metadata={'Title':X['title'],'Description':'Editable civilian intentions and frozen T+90 supernatural references; no new attacks.'})
 plt.close(fig)
def textfig(fig,x,y,s,size=9,color=INK,bold=False):
 return fig.text(x,y,s,fontsize=size,color=color,weight='bold' if bold else 'normal',va='top',linespacing=1.55)

# Sheet 08: whole clearing plus detailed civilian reactions in the lived-in settlement.
fig=plt.figure(figsize=(24,20),facecolor=BG)
textfig(fig,.025,.974,'STEP 3  /  WHAT DO THE VILLAGERS TRY TO DO?',25,bold=True)
textfig(fig,.025,.944,'Civilian reaction window +90–105 s  ·  163 survivors, including 4 injured  ·  All supernatural actors frozen at approved +90 state',10.5,'#60716b')
over=fig.add_axes([.025,.275,.315,.635]);base(over,D['main_extent'],'t2_over');population(over,'over',True,.82);fixed(over,'over');north(over,-105,184);scalebar(over,-105,-164,50)
for anchor,pos,label,col in [([-4,-36],[-52,-106],'4 witnesses head downhill\nKnown approach / no exit reached',COL['ESCAPE']),([6.5,-61.6],[50,-83],'5 at east barn gate\nStop / exchange warning',COL['HELP']),([-62,65],[-85,91],'Western trail intentions\n3 ahead / 3 still trailing',COL['ESCAPE']),([62.5,62],[87,63],'2 try east edge\nNo contact',COL['ESCAPE']),([-36.6,163],[63,166],'2 delivery workers\nSeek service-side guard',COL['SEEK AUTHORITY']),([-2.7,104],[-71,121],'3 begin formal approach\nGuard destination only',COL['SEEK AUTHORITY'])]:note(over,anchor,pos,label,col,7)
plain(over,36,-127,'LOWER FARMLAND',7.2,weight='bold');plain(over,40,111,'Church / cemetery',6.8);plain(over,4,153,'Mayor',7,weight='bold')
note(over,[-42,-139],[44,-154],'Opaque / sealed rim\nNo contact test; properties unknown to civilians','#a42e40',7)
detail=fig.add_axes([.365,.30,.61,.61]);base(detail,[-59,-3,57,85],'t2_detail',True);population(detail,'detail',True,1.15);fixed(detail,'detail')
plain(detail,5.5,32,'TAVERN',8.5,weight='bold');plain(detail,-34,22,'BLACKSMITH',8,weight='bold');plain(detail,34,71,'Older homes',8);plain(detail,-12,71,'Upper / middle homes',7.5)
for anchor,pos,label,col in [([-34.3,9.2],[-48,2],'R14 / M05 · 2 · B0\nStay low; parent protects child',COL['FREEZE / DELAY']),([-37.5,8.8],[-50,13],'BONE FIXED\nStill watching M05','#674087'),([-27,5],[-18,3],'R15 · 3 inside · B0\nCall for family; do not exit',COL['SEEK FAMILY']),([-17,35.6],[-45,34],'R33 / M04 · 2 · B1\nAppeal to nearby Witch',COL['HELP']),([-15.56,36.37],[-31,44],'WITCH FIXED\nNo reply or movement','#087d79'),([4,51.5],[3,65],'G01 · 8 helping / injured\n3 injured + 5 helpers',COL['HELP']),([-8,51.7],[-31,55],'G02 · 2\nLimping casualty + escort',COL['HELP']),([20.72,51.68],[29,62],'G06 · 3 · B1\nBegin uphill toward guards',COL['SEEK AUTHORITY']),([26,36],[49,32],'G05 · 5 · B1\nPassers + alley followers',COL['SEEK FAMILY']),([37.7,51.9],[49,57],'M09 · 5 · B1\nCaregiver keeps children close',COL['SEEK FAMILY']),([14.1,30],[43,17],'M06 · 3 outside · B1\nService-side warning / help',COL['HELP']),([4,37],[11,20],'7 remain indoors · B0\n3 intend family / 4 shelter',COL['SEEK SHELTER']),([-2.2088,44.5243],[-3,57],'BLOOD FIXED\nNo next target or attack','#a42e40')]:note(detail,anchor,pos,label,col,7.5)
scalebar(detail,-55,0,10)
textfig(fig,.365,.28,'Read movement as beginnings, not completed journeys.',11,bold=True)
textfig(fig,.365,.262,'Hollow dot: +90 start. Short solid arrow: executed civilian movement only. Filled marker: +105 position.\nStationary markers retain their +90 positions. Small markers represent groups; interior points are room proxies.',9,'#60716b')
textfig(fig,.025,.239,'LOCAL KNOWLEDGE',11,bold=True)
textfig(fig,.025,.218,'○ B0 · enclosure not identified: 74\n□ B1 · seen, properties unknown: 80\n△ B2 · confinement suspected: 9\nB3 crossing failure: 0   /   B4 attack witnessed: 0',9,'#60716b')
textfig(fig,.365,.218,'IMMEDIATE INTENT  /  PEOPLE',11,bold=True)
for i,(name,n) in enumerate(X['intent_breakdown'].items()):
 x=.365+(i%4)*.155;y=.197-(i//4)*.036;textfig(fig,x,y,f'{n}  {name}',8.8,COL[name],True)
textfig(fig,.025,.116,'REACTION ONLY',12,bold=True)
textfig(fig,.025,.094,'No new casualties. No perimeter contact. No new actor route. The Witch, Blood, Bone and the barrier make no new response in this pass.',10,'#60716b')
textfig(fig,.025,.071,'M05 remains under the existing threat; M04 does not know the Witch is responsible. Help attracts a local concentration without selecting Blood’s next target.',9,'#60716b')
textfig(fig,.025,.045,'Map north = UE +X / uphill; right = UE +Y. Metres are horizontal. Same 12:16 UTC healthy survey; no UE edits. Pale map is not a lighting render.',8.5,'#60716b')
save(fig,'08_T2_civilian_reaction_intentions')

# Sheet 09: actual concentrations versus merely converging intentions.
fig=plt.figure(figsize=(24,20),facecolor=BG)
textfig(fig,.025,.973,'STEP 3  /  EMERGING GROUPS AT THE REACTION HANDOFF',24,bold=True)
textfig(fig,.025,.943,'Candidate concentrations for the next requested action pass  ·  No target is selected  ·  Existing households remain visible',10.5,'#60716b')
textfig(fig,.025,.925,'Fixed references: Blood = red diamond   /   Witch = teal diamond   /   Bone = violet hexagon',9,'#60716b')
ax=fig.add_axes([.025,.19,.45,.72]);base(ax,D['main_extent'],'t2_groups');population(ax,'groups',False,1.05);fixed(ax,'groups');north(ax,-105,184);scalebar(ax,-105,-164,50)
for g in G:
 if g['indoor_at_90']:
  p=g['end_xy_m'];t=ax.text(*p,str(g['count']),ha='center',va='center',fontsize=8,color=BG,weight='bold',zorder=63);t.set_gid('indoor_count_'+g['id'])
offsets={'G01':(64,30),'G02':(-89,33),'G03':(58,-75),'G04':(-76,-59),'G05':(82,51),'G06':(83,81),'G07':(69,8),'G08':(70,-13),'G09':(-84,11),'G10':(-88,84),'G11':(-78,115)}
for c in CG:
 real=c['is_single_physical_crowd'];col='#956c20' if real else '#697780'
 if real:
  ring=Circle(c['xy_m'],3.5,fc='none',ec=col,lw=1.2,zorder=52);ring.set_gid('group_actual_'+c['id']);ax.add_patch(ring)
 else:
  ring=Circle(c['xy_m'],4.5,fc='none',ec=col,lw=.8,ls=':',zorder=52);ring.set_gid('group_intended_'+c['id']);ax.add_patch(ring)
 label=c['id']+' · '+str(c['count'])+(' people' if real else ' separate people*')
 note(ax,c['xy_m'],offsets[c['id']],label,col,7.5,'label_'+c['id'])
plain(ax,4,152,'ESTATE · 8 dispersed',7.5,weight='bold');plain(ax,45,112,'Cemetery reserve\nNo gathering',7.5);plain(ax,23.5,83,'Caretaker · 1',7)
plain(ax,36,-119,'FARMLAND APPROACH',8,weight='bold')

zoom=fig.add_axes([.50,.626,.474,.285]);base(zoom,[-16,39,16,58],'t2_injury',True);population(zoom,'injury',True,1.2);fixed(zoom,'injury')
note(zoom,[2,50],[2,56],'G01 / 8: 3 injured + 5 helpers','#956c20',8)
note(zoom,[-7.8,51.5],[-10,56],'G02 / 2\n1 injured + 1 escort','#956c20',8)
note(zoom,[-2.2088,44.5243],[-7,41.4],'Blood stays fixed; no response','#a42e40',8)
note(zoom,[8,51.5],[12,46.5],'2 porch helpers\narrive from east','#956c20',7.5)
scalebar(zoom,8,40,5)
textfig(fig,.502,.609,'ACTUAL LOCAL GROUPS  /  COUNTS ARE SUBSETS OF 163',10.7,bold=True)
ys=.584
for cid in ['G01','G02','G03','G04','G05','G06','G07','G11']:
 c=CI[cid];textfig(fig,.502,ys,f"{cid}  {c['count']:>2}  {c['name']}",9.5,bold=True)
 textfig(fig,.502,ys-.016,textwrap.fill(c['reason'],83),9.2,'#60716b');ys-=.047
textfig(fig,.502,.19,'NOT YET ONE CROWD',10.7,bold=True)
textfig(fig,.502,.169,'G08 · 6: three inside the tavern / three at its service side.\nG09 · 4: two homeward residents / two calling to the Witch.\nG10 · 6: three already on the trail / three still returning to its junction.\nThese people must not be treated as single attack footprints.',9,'#60716b')
textfig(fig,.025,.166,'○ Solid rings: co-located or coordinated group.\nDotted rings*: intentions sharing an area, not one physical crowd.\nUnringed dots: other survivors. White roof numbers: indoor people.',9,'#60716b')
textfig(fig,.025,.09,'163 LIVING  /  4 INJURED INCLUDED  /  NO NEW ATTACKS',12,bold=True)
textfig(fig,.025,.064,'The two injury pockets together contain 4 injured people and 6 helpers. Other nearby witnesses remain separate; no strategic crowd is manufactured.',9,'#60716b')
textfig(fig,.025,.04,'Civilian clock ends +105; actor references remain +90 as instructed. This deliberate planning freeze is not an approved extra fifteen-second attacker delay.',9,'#60716b')
save(fig,'09_T2_reaction_groups')

# Spreadsheet-friendly complete subgroup record.
columns=['id','origin_cohort','count','label','micro_membership','injured_count','start_xy_m','start_source','end_xy_m','knowledge_at_90','barrier_knowledge_at_90','barrier_knowledge_at_105','barrier_evidence','emotion','intent','destination_intent','movement_start_s','movement_stop_s','distance_m','mean_plan_speed_m_s','companions','people_left_behind','help_target','concentration_id','potential_bone_stimulus','heads_toward_boundary','approaches_witch','seeks_mayor','final_outcome']
with (OUT/'t2_reactions.csv').open('w',newline='',encoding='utf-8') as fp:
 writer=csv.DictWriter(fp,fieldnames=columns);writer.writeheader()
 for g in G:writer.writerow({k:json.dumps(g[k],ensure_ascii=False) if isinstance(g[k],(list,dict)) else g[k] for k in columns})

def table(header,rows):return '| '+' | '.join(header)+' |\n|'+'|'.join(['---']*len(header))+'|\n'+'\n'.join('| '+' | '.join(str(c).replace('|','/').replace('\n',' ') for c in row)+' |' for row in rows)+'\n'
def coord(p):return '('+', '.join(f'{x:.2f}' for x in p)+')'
notes=f'''# MASSACRE PLANNING — STEP 3 / FIRST CIVILIAN REACTION

Authored **{X['authored_utc']}**. This separate 2D layer starts with **163 living ordinary villagers, including four injured**, and ends with the same 163. Seven prior fatalities remain excluded. It uses the approved design bible, T0, T1, Step 2B and locked rules. **No UE edits, new attacks, new injuries, barrier contact or final fates.**

- [08 — civilian intentions](08_T2_civilian_reaction_intentions.png), [editable SVG](08_T2_civilian_reaction_intentions.svg)
- [09 — emerging groups](09_T2_reaction_groups.png), [editable SVG](09_T2_reaction_groups.svg)
- [Editable reaction source](t2_civilian_reactions.json), [complete subgroup CSV](t2_reactions.csv), [verification manifest](t2_manifest.json)
- [Unchanged base](01_village_base_map.png), [clean planning copy](02_massacre_planning_blank.png), [T0](03_T0_normal_activity.png), [approved +90 timeline](07_T1_bone_timeline.png)

## Window and frozen state

**+90 to +105 seconds: fifteen seconds to form and begin intentions.** Delays represent shock, decisions and coordination. Only 29 subgroup records begin a short physical movement; other markers stay at their approved location or symbolic interior/yard allocation. No complete long journey is run. Movement lengths are horizontal plan distances, not navmesh or animation results.

{X['scope']['clock_note']}

| Reference | Frozen state throughout this reaction pass |
|---|---|
| Blood | {coord(FIX['blood_xy_m'])} m, first-strike area. No next target or attack. |
| Bone | {coord(FIX['bone']['xy_m'])} m, watching M05 at (−34.30, +9.20). No motion, sound, torment or attack added. |
| Witch | {coord(FIX['witch_xyz_m'])} m including z, same approved main-road position. Destination intent remains Mayor; no movement or reply. |
| Barrier | Same opaque, physically sealed rim. Reactive capability is locked, but no contact or response happens. |

## Intent and barrier knowledge

Each person has one primary immediate intent. These categories partition the survivors; companions, micro-groups and concentration circles are references to those same people, never extra population.

'''+table(['Intent','People'],[(k,v) for k,v in X['intent_breakdown'].items()])+'''
HELP includes four people requesting/accepting assistance and 23 people providing help, warnings or investigation. It does not mean 27 able-bodied rescuers. SEEK SHELTER commonly means staying in the home already occupied; no mass teleport into buildings occurs.

'''+table(['Barrier knowledge','At +90','At +105'],[(k+' — '+X['barrier_knowledge_key'][k],X['barrier_knowledge_counts_at_90'][k],X['barrier_knowledge_counts_at_105'][k]) for k in X['barrier_knowledge_counts_at_90']])+'''
The knowledge partition stays unchanged during this short slice. B1/B2 evidence comes from pre-opacity observations or the already-established local relay, not from suddenly seeing through darkness. Indoor groups and pain-/threat-focused people often remain B0. B2 is a hypothesis, not proven solidity. **Nobody knows from experience that touching the barrier is lethal; B3 = B4 = 0.** All 163 know a catastrophe is happening, with different knowledge of its causes.

## Injured people and the new help concentration

Proposed functional mobility: **two cannot stand, one needs one supporting person, and one can bear weight but only limp**. These are planning assumptions about the four previously approved stall casualties, not extra injuries, diagnoses or final outcomes.

- **R22: two non-ambulant people**, still near (2, 50). R26's two nearby neighbours approach them. R34's two porch patrons arrive around the tavern's eastern frontage. Four helpers are beginning to organize support; nobody is carried away yet.
- **R23: one supported walker**, beginning a 2.5 m move from (4.5, 50.5) to (6, 52.5), +100–105. R27 first reaches them by +99 and accompanies that movement. No normal running is assigned.
- **R24: one limping person**, beginning a 3.6 m move to (−7.8, 51.5), +99–105. R28 reaches them first and escorts them just to the west edge.

**G01 has eight people: three injured and five helpers. G02 has two: one injured and one helper. Together there are four injured and six helpers across two adjacent pockets.** The other witnesses remain separately counted. The helpers come from four existing talking neighbours and two existing porch patrons. Rescue is an immediate human response to nearby pain, despite Blood remaining dangerously close. Blood does not react to the concentration in this pass.

## M05, M04 and the Witch

**M05 / R14:** the parent stays low and shields the child at the same compromised coop corner. Bone is only about 3.2 m away. They have no tested safe route, and the earlier hiding gap was tight; making them suddenly sprint through it would assume confidence they do not have. R15's three already-warned household occupants call from inside, without knowing the pair's current west-side position. Neither household members nor Bone are given a new visual certainty through walls. Bone's next decision and the family's fate remain open.

**M04 / R33:** the water carriers know Bone killed the assistant but have lost track of him. The Witch is initially approximately 2.8 m from their stopped road-edge position. They make a cautious 1.2 m step, ending about 1.6 m from her, and call for help. A familiar neighbour who appears calm is a plausible person to appeal to. They do not know she caused the disaster, is immune to her creations or is going to the Mayor. She neither replies nor moves. R31's two homeward passers use the same western district farther north; their path comes within about 5 m, but no interaction with her is asserted. No other group is routed toward her deliberately.

## Tavern, church and estate

The **tavern remains seven indoors and seven outdoors at the start**. Two of four porch patrons help the injured; the other two begin around the eastern frontage to find family. Three indoor customers intend to leave but remain on the interior side while organizing; three other customers and the indoor staff member stay. M06's two receiving staff and one delivery hand remain at the service side calling inside and offering assistance. Indoor people have warnings and dark windows, not exact Blood position/ability knowledge. The seven indoor people have not all left by +105, and the six departure/service intentions are **not** one crowd in the street.

The **caretaker stays alone at the church public threshold**, calling locally and intending to admit people. Church shelter is familiar masonry and community habit, not supernatural protection. Nobody reaches it, gathers at the disturbed graves or occupies the reserve. The geometry includes **Church_BellOpening-1 and Church_BellOpening1**, but no confirmed usable bell/rope or alarm routine. **No bell rings.** Whether a functional bell is intended remains a review question before it changes information spread.

The **estate keeps eight people, with five inside and three outside**. The Mayor demands a report from the nearby house-duty guard; neither knows an attacker location or the Witch's objective. Three indoor staff keep together. The entrance guard already suspects confinement and holds the controlled entrance, beginning a warning uphill. The service guard starts only seven metres toward the house; no report has reached the Mayor yet. The outside stable worker seeks immediate cover. The separately counted two-person provisions crew resumes only nine metres of its approved cart road toward service access. No guard travels down to confront an attacker, no new retinue is invented, and the Witch remains far below the property.

## New groups, including intentions that have not converged

'''+table(['ID','People','Physical status','Why they form / remain separate'],[(c['id']+' '+c['name'],c['count'],c['status'],c['reason']) for c in CG])+'''
These are **candidate inputs**, not a ranking or selection of Blood's next victim group. Existing occupied homes and the tavern still matter as concentrations. Separate rooms/households cannot be combined into one outdoor target footprint merely because their origin-cohort count is high. G08/G09/G10 deliberately show this distinction.

## Boundary and authority intentions

'''+table(['Group','People','First movement / intended destination','Remaining rim distance along this short motion'],[(g['id']+' '+g['label'],g['count'],g['destination_intent'],str(next(c['barrier_clearance_m'] for c in checks if c['group']==g['id']))+' m') for g in G if g['heads_toward_boundary']])+'''
**Twenty people begin escape intentions.** Seeing a sheet or suspecting confinement does not tell them whether a familiar way can be crossed. The eastern pair stops approximately 9.9 m from the rim; no other escaping group comes closer during this slice. Gate-directed lower residents only edge along their own house side. No new group reaches the village gate, leaves the clearing or touches the barrier.

**Eight seek authority:** R30's three centre passers start uphill along the main street; R65's three upper-yard residents begin the formal approach; R79/M12's two delivery workers resume the cart route. These are separate streams at different elevations, not one eight-person crowd. Nobody reaches the Mayor. The three-person church offer is not invented: there is still only one caretaker and no congregation.

## Potential Bone stimuli, held for the next action

'''+table(['ID','Civilian source','Stimulus','Perception limit'],[(s['id'],', '.join(s['groups']),s['description'],s['availability']) for s in X['pending_stimuli']])+'''
Bone does not acquire or respond to any new cue here. His current target is still M05. A candidate stimulus on the far side of the village is not automatically something he can hear or see; the next action must check actual perception. No deliberate miss, sound or discovery by him is added.

## Local knowledge and geometry review

The choices pass the local-knowledge check as working human responses: witnesses back away from known violence; family groups seek familiar people; some help injured neighbours; some appeal to authority; many frightened interiors stay put. No household avoids an exit because of a barrier killing that has not happened. No villager knows the Witch's responsibility or immunity. Guards have no automatic intelligence network.

All 29 new movement traces were checked against the unchanged projected building/outbuilding footprints and remain inside the approved rim. No new trace crosses a roof footprint. Stationary interior markers intentionally lie inside assigned buildings; they do not assert new room/door geometry. Small props, fences, thresholds, 3D slope, hearing and visibility are not fully collision-simulated. Indoor exit/closure intentions are left unexecuted where doors are not resolved. Prior source IDs such as CrushedHome remain healthy-survey identifiers, not newly authored destruction.

The initial unlabelled centre people, household interiors and yard members previously had **role/area allocations**, not exact individual poses. This layer refines those positions within the same assigned spaces. Named micro-groups and all resolved T1/Step2B movements remain exact at +90. Read the CSV's `start_source` and JSON's `start_refined_within_existing_area` flags; these are provisional spatial refinements, not silently claimed surveyed civilian coordinates.

The external light is gone, but maps stay pale for design readability. Existing indoor lamps are not extinguished by fiat. Exact sight distance, lamp coverage, stumbling/hesitation and window views need later scene-level evaluation; intent arrows are not proof that every metre is visibly lit.

## Review decisions / ambiguities

'''+ '\n'.join(f'{i+1}. {s}' for i,s in enumerate(X['review_assumptions']))+'''

These are review choices for this authored pass, not permission to execute the next phase. In particular, confirm the injury mobility split, family/aid reactions, subgroup position refinements and functional-bell question before using them as constraints on the next action.

## Complete population audit

Original cohort membership persists after movement. Named M groups are subsets of the R reaction records. M01's two people and the five other approved fatalities have no reaction record. All twelve surviving named micro-groups reconcile to their existing counts and exact +90 anchors.

'''+table(['Origin cohort','T0','Prior deaths','Survivors','Reaction records'],[(p['id']+' '+p['name'],p['count'],p['count']-X['population']['origin_cohort_counts'][p['id']],X['population']['origin_cohort_counts'][p['id']],', '.join(g['id'] for g in G if g['origin_cohort']==p['id'])) for p in T0['population_clusters']])+'''
### Immediate subgroup ledger

Coordinates are map x/y metres. An unchanged pair of coordinates indicates intent without executed relocation. See JSON/CSV for knowledge provenance, companions, people left behind, timing, helper links, candidate stimuli and boundary/Witch/Mayor flags for every record.

'''+table(['Record / origin / people','+90 → +105 position','Barrier','Immediate intent / direction'],[(f"{g['id']} / {g['origin_cohort']} / {g['count']} — {g['label']}",coord(g['start_xy_m'])+' → '+coord(g['end_xy_m']),g['barrier_knowledge_at_90'],g['intent']+': '+g['destination_intent']) for g in G])+'''
## Editable handoff and stop

Apply `t2_civilian_reactions.json` after the unchanged T0 → T1 → Step2B sources. Its 79 records are a disjoint partition of 163 people, not 79 new households or civilians. Timed knots describe only the short begun motions; destination prose is intention, not an executed future path. Derive group counts from member references, never add G counts to the population.

Run `python render_t2.py .` from this map folder. The renderer regenerates only 08/09 PNG/SVG, these derived notes, the CSV and `t2_manifest.json`. Edit the independent JSON rather than any clean/source map. All 32 preceding map/source artifacts are hash-protected and unchanged; the original empty massacre annotation template remains empty. No previous map is replaced.

**Stop at the civilian +105 reaction snapshot with the supernatural +90 state deliberately frozen.** No next target, attack, Witch segment, barrier response or final fate has been selected. The next requested ACTION phase receives these exact survivor locations, intentions, injuries, knowledge states, forming groups and possible stimuli. It must reconcile timing without treating the planning freeze as automatic extra escape time.
'''
notes=notes.replace('The three-person church offer is not invented: there is still only one caretaker and no congregation.','The church still has only one caretaker and no congregation.')
(OUT/'T2_CIVILIAN_REACTIONS.md').write_text(notes,encoding='utf-8',newline='\n')
for n,h in X['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h
files=['08_T2_civilian_reaction_intentions.png','08_T2_civilian_reaction_intentions.svg','09_T2_reaction_groups.png','09_T2_reaction_groups.svg','t2_civilian_reactions.json','render_t2.py','T2_CIVILIAN_REACTIONS.md','t2_reactions.csv']
manifest=dict(schema='t2-review/v1',title=X['title'],image_dimensions={n:list(Image.open(OUT/n).size) for n in files if n.endswith('.png')},files={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in files},source_files_unchanged={n:True for n in X['source_sha256']},geometry_sha256=D['geometry_sha256'],civilian_window_s=[90,105],frozen_actor_time_s=90,living=163,injured_in_living=4,prior_fatalities=7,new_fatalities=0,barrier_contacts=0,new_actor_actions=0,ue_edits=False,counts_validated=True,micro_anchors_validated=True,movement_checks=checks)
(OUT/'t2_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'rendered':manifest['image_dimensions'],'protected_files':len(X['source_sha256']),'living':163,'moving_subgroups':sum(bool(g['distance_m']) for g in G),'max_movement_m':max(g['distance_m'] for g in G),'min_barrier_clearance_m':min(c['barrier_clearance_m'] for c in checks)},indent=2))
