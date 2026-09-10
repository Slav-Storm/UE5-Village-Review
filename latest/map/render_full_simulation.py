"""Render additive offline planning documents. python render_full_simulation.py BASE [OUT]"""
import ast,json,sys,hashlib,csv,textwrap
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image
from shapely.geometry import shape,Point,LineString
from shapely.ops import substring
HERE=Path(__file__).resolve().parent;BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE;OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
X=json.loads((OUT/'full_simulation.json').read_text(encoding='utf-8'))
for n,h in X['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
src=BASE/'render_map.py';tree=ast.parse(src.read_text(encoding='utf-8'));cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in n.targets));oldargs=sys.argv;sys.argv=['render_map.py',str(BASE)];core={'__file__':str(src)};exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(src),'exec'),core);sys.argv=oldargs
plt=core['plt'];base=core['base'];draw=core['draw_geom'];BG=core['BG'];INK=core['INK'];D=core['D'];F={f['id']:f for f in D['features']}
T1=json.loads((BASE/'t1_simulation.json').read_text(encoding='utf-8'));T3=json.loads((BASE/'t3_second_action.json').read_text(encoding='utf-8'));BONE=json.loads((BASE/'bone_completion.json').read_text(encoding='utf-8'))
COL={'Blood':'#a23144','Bone':'#694389','Witch':'#007c78','barrier':'#a86328','bell':'#ab9338'}
def stamp(ax,p,txt,c,off=(0,10),size=7):
 ax.annotate(txt,xy=p,xytext=off,textcoords='offset points',ha='center',va='bottom',fontsize=size,color=c,bbox={'facecolor':BG,'edgecolor':c,'alpha':.95,'boxstyle':'round,pad=.25','linewidth':.35},arrowprops={'arrowstyle':'-','color':c,'lw':.4},zorder=100)
def mark(ax,e,tag=None,size=32):
 c=COL.get(e['actor'],'#555');ax.scatter(*e['xy_m'],s=size,marker='*' if e['fatalities'] else 'o',c=c,zorder=80)
 if tag:stamp(ax,e['xy_m'],tag,c)
def rim(ax):draw(ax,shape(T1['barrier']['geometry']),'none',COL['barrier'],.6,40,'barrier_unchanged',.65,'dashed')
def route(ax,m,c,ls='solid',lw=1):draw(ax,shape(m['geometry']),'none',c,lw,55,m.get('id','route'),.8,ls)
def title(fig,heading,sub):
 fig.text(.045,.967,heading,fontsize=20,weight='bold',color=INK);fig.text(.045,.943,sub,fontsize=9,color='#52605f')
def footer(fig,extra=''):
 fig.text(.045,.026,'Same healthy-village geometry • Up = UE +X / uphill • Right = UE +Y • Metres in plan • No UE edits',fontsize=8,color='#596965')
 if extra:fig.text(.045,.045,extra,fontsize=8,color=INK)
def save(fig,name):
 fig.savefig(OUT/(name+'.png'),dpi=200,facecolor=BG);fig.savefig(OUT/(name+'.svg'),facecolor=BG);plt.close(fig)
 im=Image.open(OUT/(name+'.png')).convert('RGB');im.quantize(colors=192,method=Image.Quantize.MEDIANCUT).save(OUT/(name+'.png'),optimize=True)
def census(ax,s):
 for r,g in s['groups'].items():
  n=len(g['people']);ax.scatter(*g['xy'],s=10+n*3,c='#3e806f',edgecolor=BG,lw=.4,zorder=60)
def textblock(fig,x,y,txt,width=70,size=10):fig.text(x,y,textwrap.fill(txt,width),fontsize=size,va='top',color=INK,linespacing=1.5)

# Permanent early milestone; no duplicate full-resolution images per increment.
fig=plt.figure(figsize=(16,12),facecolor=BG);title(fig,'AUTONOMOUS SIMULATION / EARLY CONSEQUENCES','First barrier discoveries and the first shelter failure • Separate causal layers, continuing from +109')
views=[([-82,45,-35,80],'A02_BARRIER_WEST','+123 / WESTERN WORKING TRAIL'),([42,45,81,83],'A03_BARRIER_EAST','+130 / EASTERN ANIMAL YARD'),([-38,45,2,77],'A04_BLOOD_WEST_SHELTER','+133 / WESTERN REFUGE')]
for i,(extent,eid,heading) in enumerate(views):
 ax=fig.add_axes([.04+i*.325,.31,.30,.57]);base(ax,extent,eid,True);rim(ax);e=next(e for e in X['events'] if e['id']==eid)
 if e['geometry']:draw(ax,shape(e['geometry']),COL[e['actor']],COL[e['actor']],.8,45,eid,.17)
 mark(ax,e);ax.set_title(heading,fontsize=12,pad=16,loc='left')
 for gid in sorted({X['people'][pid]['group'] for pid in e['direct_witnesses']}):
  gg=X['groups'][gid];p=gg['initial_xy']
  for m in gg['moves']:
   if m['start_s']>e['time_s']:break
   geom=shape(m['geometry']);p=list((geom if geom.geom_type=='Point' else geom.interpolate(min(geom.length,(e['time_s']-m['start_s'])*m['speed_m_s']))).coords[0])
  ax.scatter(*p,s=23,c='#2b7d69',zorder=75)
 if i==0:stamp(ax,[-69,63],'Nearby witnesses only','#2b7d69',(35,35),7)
 if i==1:stamp(ax,[71,64],'Partner witnesses contact','#2b7d69',(-48,30),7)
 for m in X['civilian_movements']:
  if m['start_s']<=e['time_s'] and m['mode'] in ['escape','attempt crossing','assisted retreat','call for shelter','shelter noisily']:
   geom=shape(m['geometry']);stop=min(e['time_s'],m['end_s'],m.get('interrupted_at_s') or 1e9)
   if geom.geom_type=='LineString':draw(ax,substring(geom,0,max(0,(stop-m['start_s'])*m['speed_m_s'])),'none','#807344',.7,55,m['id'],.8)
 textblock(fig,.045+i*.325,.25,[
 'One leading walker makes actual contact. Two companions and three nearby woodcutters witness the lethal response. Distant groups do not inherit that knowledge.',
 'The eastern pair independently makes the same mistake. One dies; the partner witnesses it. No west-trail warning could have reached them in time.',
 'The heavy surge breaches the refuge wall and north-side entry attempt. Six fatalities; one newly injured escort. Existing injuries remain separately tracked.'
 ][i],45,10)
footer(fig,'Stars are event sites, not final corpse poses. Damage is restricted to the force footprint. No escape route is presumed safe.');save(fig,'12_early_barrier_shelter')

# Consolidated ledger is regenerated at every published milestone.
events=sorted(X.get('prior_events',[])+X['events'],key=lambda e:e['time_s']);last=X['snapshots'][-1];living=[p for p in X['people'].values() if p['alive']]
lines=['# MASSACRE FULL SIMULATION', '',f"Stage: **{X['stage']}**. Authored {X['authored_utc']}. Current canonical time **+{last['time_s']:.3f} s**.",'',f"**{len(living)} living; {sum(p['injured'] for p in living)} injured among them; {170-len(living)} fatalities from the original 170.** Eleven fatalities predate this continuation.",'','[Early milestones](12_early_barrier_shelter.png) · [Editable consolidated data](full_simulation.json) · [Event CSV](full_event_ledger.csv) · [Population CSV](full_population_ledger.csv)','','## Continuity and method','','The approved +109 handoff remains the starting state. Each reaction file commits locally justified intentions; its paired action file queries positions at the actual event/decision time. Existing motion and the Witch walk continue during planning decisions. No literal supernatural freeze grants extra escape time. Member IDs refer to the original R/P census, not extra NPCs. Split groups retain the same people.','',
 'The newly approved ground-floor bell rope permits a short first peal at +100. The caretaker returns to the recorded threshold by +104.7; the +109 position remains unchanged. Later peals occur while he admits people. Hearing the bell conveys a public emergency only. It does not supply attacker identities, barrier contact rules, guilt or safe destinations.','',
 'The Witch keeps the saved main-road centreline, formal staircase with landings, courtyard and surveyed front door. Working speeds are 1.1 m/s along road/court and 0.85 m/s along the steep stair profile; the endpoint connection uses the saved heights. She is expected to reach the Mayor around +312.625. No shortcut, waiting for a body-count target or route change is introduced.','',
 'Action/reaction boundaries are causal review boundaries. A decision may start a continuing journey or warning; its timed record does not mean the destination is already reached. Civilian positions, sight lines, warning proximity, source knowledge and event time determine subsequent exposure.','',
 '## Chronological event ledger','','| Time | Event | Immediate action | New fatalities | New injuries | Living |','|---|---|---|---:|---:|---:|']
for e in events:lines.append(f"| +{e['time_s']:.3f} | {e['id']} / {e['actor']} | {e['action']} | {len(e['fatalities'])} | {len(e['injuries'])} | {e['population_after']} |")
lines+=['','Opening events are inherited from the unchanged T1, Bone-completion and T3 layers. The +100 bell is an explicit new continuity overlay; its population at receipt is 163 (the historical +108 losses are already reflected in the continuation census). Event counts are references, not extra deaths. Consult the original opening layers for the full early witness detail; an empty inherited witness list here does not erase their evidence.','','## Action / reaction increments','','| Layer | Canonical bounds | Population after | Reason |','|---|---|---:|---|']
for c in X['cycles']:
 q=json.loads((OUT/c['file']).read_text(encoding='utf-8'));lines.append(f"| [{q['id']}]({c['file']}) | +{q['start_s']:.3f} to +{q['end_s']:.3f} | {q['snapshot']['living']} | {q['reason']} |")
lines+=['','## Causal consequences and local reception','']
for e in events:
 lines += [f"### {e['id']} / +{e['time_s']:.3f}", '',e['cause'],'',f"Event site: {e['xy_m']}. Direct witnesses: {', '.join(e['direct_witnesses']) or 'none established'}. Likely listeners: {', '.join(e['likely_listeners']) or 'none established'}.",'',f"Fatalities: {', '.join(e['fatalities']) or 'none'}. Newly injured: {', '.join(e['injuries']) or 'none'}. No final body pose.",'']
 if e.get('witch_intersection'):lines += ['**Natural Witch intersection:** blood separates/melds around her and continues. She neither stops nor dodges. This is a future visual clue, not an implemented effect.','']
lines+=['## Current surviving pockets','','| Original group / role | Living | Injured | Latest recorded position |','|---|---:|---:|---|']
for r,g in last['groups'].items():lines.append(f"| {r} / {X['groups'][r]['label']} | {len(g['people'])} | {sum(X['people'][p]['injured'] for p in g['people'])} | {g['xy']} {'inside '+g['inside'] if g['inside'] else 'outside'} |")
lines+=['','## Knowledge discipline','','Every information transfer is retained separately in the JSON. Direct barrier witnesses can reach B4; people receiving a warning are marked as reported knowledge, not falsely counted as direct witnesses. Ordinary alarm is not attacker tracking. Silence/hiding does not automatically disclose indoor headcounts to either creature. Sound bands and roof occlusion are planning tests, not a verified acoustic/lighting simulation.','','## Geometry and staging limits','','The macro layout, source geometry, cemetery, two exhumed graves and future burial reserve are unchanged. Individual door centres recovered from the original archived survey are kept as small 2D links. Imported cottage blocks without modelled doorways use explicitly approximate existing street-facing thresholds. These are abstraction links through occupied buildings, not new doors, tunnels or layout changes. Small fences, retaining edges, slopes, detailed interior rooms and character-width clearance still require later scene validation.','',
 'Force envelopes are provisional design regions. Direct central force can cause fatal exposure, while outer force causes injury. This is not a calibrated combat damage model. Structure damage requires actual envelope intersection; nobody inside an untouched house dies merely because another house is struck. Precise Bone hits identify a target or intentionally hit an object. No final mesh, gore, corpse pose or production asset is created.','',
 f"All **{len(X['source_sha256'])} prior map/source files are hash-protected and byte-identical**. The original clean map and empty annotation template remain clean. No Unreal connection or edit is used. Unresolved arrest motives, guard responsibility for the earlier tragedy, the child's remaining consciousness, boss implementation, post-boss memory and rebuilding are not resolved by this simulation.",'']
(OUT/'MASSACRE_FULL_SIMULATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
with (OUT/'full_event_ledger.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['time_s','event','actor','x_m','y_m','new_fatalities','new_injuries','living_after','cause','direct_witnesses','likely_listeners'])
 for e in events:w.writerow([e['time_s'],e['id'],e['actor'],*e['xy_m'],len(e['fatalities']),len(e['injuries']),e['population_after'],e['cause'],';'.join(e['direct_witnesses']),';'.join(e['likely_listeners'])])
with (OUT/'full_population_ledger.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['person','origin_cohort','current_group','role','alive','injured','death_event','death_time_s','attacker','attempted_activity','exposure','direct_barrier_level','received_barrier_warning'])
 for p in X['people'].values():w.writerow([p['id'],p['origin'],p['group'],p['role'],p['alive'],p['injured'],p['death'],p.get('death_s'),p.get('attacker'),p.get('attempted_activity'),p.get('exposure'),p['barrier_level'],p['barrier_reported']])
print('Rendered early milestone and consolidated ledger:',last['time_s'],len(living),'living')
