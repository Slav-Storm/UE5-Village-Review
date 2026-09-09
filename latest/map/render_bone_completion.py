"""Render the separate Step 2B overlay; approved T0/T1 files are read-only.
Usage: python render_bone_completion.py MAP_DIRECTORY [OUTPUT_DIRECTORY]
Requires matplotlib, numpy, Pillow and shapely. No Unreal calls.
"""
import ast,sys,json,copy,hashlib,csv,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import shape,Point,LineString,box
from shapely.ops import substring
from matplotlib.patches import FancyArrowPatch,Wedge,Circle
HERE=Path(__file__).resolve().parent;BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE;OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
X=json.loads((OUT/'bone_completion.json').read_text(encoding='utf-8'));RULES=json.loads((OUT/'massacre_behaviour_rules.json').read_text(encoding='utf-8'));S=json.loads((BASE/'t1_simulation.json').read_text(encoding='utf-8'));OLD=copy.deepcopy(S)
for n,h in X['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
S['cohort_awareness']=X['resolved_cohort_awareness'];A={a['id']:a for a in S['actors']};B=S['barrier'];BX=X['bone'];I={i['id']:i for i in BX['incidents']}
source=BASE/'render_map.py';tree=ast.parse(source.read_text(encoding='utf-8'));cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in n.targets));oldargs=sys.argv;sys.argv=['render_map.py',str(BASE)];core={'__file__':str(source)};exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(source),'exec'),core);sys.argv=oldargs
plt=core['plt'];np=core['np'];Image=core['Image'];base=core['base'];draw=core['draw_geom'];plain=core['plain'];scalebar=core['scalebar'];D=core['D'];BG=core['BG'];INK=core['INK']
COL={'blood':'#a52838','bone':'#684183','witch':'#087c7c'};STATE={'U':'#d7dcd9','Q':'#d9b860','A':'#568fae','P':'#cf7839','T':'#8e73a7','V':'#b93243','D':'#45494a'};SN={'U':'Unaware','Q':'Uncertain','A':'Aware','P':'Local panic','T':'Trapped-aware*','V':'Global alarm','D':'Early fatalities'}
# Reuse only pure drawing functions from approved T1, never its CSV/exports.
tree=ast.parse((BASE/'render_t1.py').read_text(encoding='utf-8'));wanted={'arrow_line','note','barrier','awareness','events','direction','state_legend'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted],type_ignores=[]),'inherited_T1_drawing_helpers','exec'),globals())

def point(t):
 if t<=12:
  points=A['bone']['timed_points']
  for a,b in zip(points,points[1:]):
   if a['t_s']<=t<=b['t_s']:
    u=(t-a['t_s'])/(b['t_s']-a['t_s']);return [a['xy_m'][i]+u*(b['xy_m'][i]-a['xy_m'][i]) for i in range(2)]
 p=A['bone']['last_confirmed_xy_m']
 for b in BX['movement_bursts']:
  if t<b['start_s']:return p
  g=shape(b['geometry'])
  if t<=b['end_s']:return list(g.interpolate(g.length*(t-b['start_s'])/(b['end_s']-b['start_s'])).coords)[0]
  p=list(g.coords)[-1]
 return p

def fixed_routes(ax,t,prefix):
 for aid,dep,arr in [('blood',2,54),('witch',24,90)]:
  g=shape(A[aid]['geometry']);g=substring(g,0,g.length*max(0,min(1,(t-dep)/(arr-dep))))
  if g.geom_type=='LineString':arrow_line(ax,g,COL[aid],1.9 if aid=='blood' else 1.5,prefix+'_actor_'+aid,aid=='witch')
 p=A['witch']['snapshots'][str(t)][:2];ax.plot(*p,'D',ms=5,color=COL['witch'],mec=BG,mew=.4,zorder=48)

def burst(ax,g,prefix,lw=1.25):
 draw(ax,g,'none',COL['bone'],lw,32,prefix,ls=(0,(1.5,2.5)))
 if g.length>1:
  a=g.interpolate(g.length*.7);b=g.interpolate(max(0,g.length*.7-1.3));p=FancyArrowPatch((b.x,b.y),(a.x,a.y),arrowstyle='-|>',mutation_scale=8,color=COL['bone'],lw=.8,zorder=34);p.set_gid(prefix+'_arrow');ax.add_patch(p)

def bone_pattern(ax,t,prefix,full=False):
 q=[p['xy_m'] for p in A['bone']['timed_points'] if p['t_s']<=min(12,t)]
 if len(q)>1:burst(ax,LineString(q),prefix+'_bone_opening',.8)
 for b in BX['movement_bursts']:
  if t<=b['start_s']:continue
  g=shape(b['geometry']);g=substring(g,0,g.length*min(1,(t-b['start_s'])/(b['end_s']-b['start_s'])))
  if g.geom_type=='LineString':burst(ax,g,prefix+'_bone_burst_'+b['id'],1.25 if b['id']!='J06' else .8)
 for bid in ['B04','B06','B08','B11','B13','B16']:
  i=I[bid]
  if i['t_s']>t:continue
  marker='*' if i['fatal'] else 'o';p=ax.plot(*i['xy_m'],marker=marker,mfc=COL['bone'] if i['fatal'] else BG,mec=COL['bone'],mew=.85,ms=9 if i['fatal'] else 6,zorder=42)[0];p.set_gid(prefix+'_bone_incident_'+bid)
  if full and not i['fatal']:
   ring=Circle(i['xy_m'],1.4,fc='none',ec=COL['bone'],lw=.55,ls=':',zorder=40);ring.set_gid(prefix+'_bone_observe_'+bid);ax.add_patch(ring)
 if t>=26:
  p=I['B07']['intentional_target_xy_m'];ax.plot(*p,'x',ms=5,color=COL['bone'],zorder=49)
 bp=point(t);ax.plot(*bp,'h',ms=9,mfc=COL['bone'],mec=BG,mew=.6,zorder=54)

def save(fig,name,svg=False):
 fig.savefig(OUT/(name+'.png'),dpi=250,facecolor=BG)
 im=Image.open(OUT/(name+'.png')).convert('RGB');im.quantize(colors=256,dither=Image.Dither.NONE).save(OUT/(name+'.png'),optimize=True)
 if svg:
  path=OUT/(name+'.svg');fig.savefig(path,facecolor=BG,metadata={'Title':X['title'],'Description':'Bone incident pattern plus unchanged Blood/Witch routes; a separate Step2B overlay.'})
  ns='http://www.w3.org/2000/svg';ink='http://www.inkscape.org/namespaces/inkscape';root=ET.parse(path).getroot()
  for group in root.findall('.//{'+ns+'}g'):
   if group.get('id','').startswith('axes_'):
    for token,label in [('bone_burst','Bone short movement bursts'),('bone_incident','Bone incidents'),('bone_observe','Bone observation periods'),('actor','Approved Blood and Witch routes'),('awareness','Resolved cohort awareness')]:
     matches=[g for g in list(group) if '_'+token+'_' in g.get('id','')]
     if matches:
      layer=ET.SubElement(group,'{'+ns+'}g',{'id':group.get('id')+'_'+token,'{'+ink+'}groupmode':'layer','{'+ink+'}label':label})
      for g in matches:group.remove(g);layer.append(g)
  ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
 plt.close(fig)

fig=plt.figure(figsize=(24,20),facecolor=BG)
fig.text(.028,.961,'STEP 2B  /  BONE: A PATTERN OF INCIDENTS',fontsize=25,weight='bold',color=INK)
fig.text(.028,.936,'Complete +0–90 account  ·  One additional fatality  ·  Approved Blood/Witch movement and barrier formation preserved',fontsize=10.8,color='#60716b')
fig.text(.97,.912,'Movement bursts + attention changes + periods of observation',ha='right',fontsize=10,color=COL['bone'])
over=fig.add_axes([.025,.285,.325,.61]);base(over,D['main_extent'],'bone_overview');barrier(over,90,'over');fixed_routes(over,90,'over');events(over,90,'over');bone_pattern(over,90,'over');awareness(over,90,'over',2.6);direction(over);scalebar(over,-104,-165,50)
plain(over,17,157,"Mayor's grounds",8);plain(over,31,91,'Church / cemetery',7.5);plain(over,30,-117,'Farmland approach',8)
note(over,point(90),[-76,1],'Bone +90\nM05 remains his focus',COL['bone'],8,'over_bone90')
fig.text(.026,.26,'T+90: 163 LIVING / 7 EARLY FATALITIES',fontsize=11,weight='bold',color=INK)
fig.text(.026,.239,'Four injured are included among the living.\nCohort pins stay at their original T0 reference anchors.',fontsize=9,color='#60716b',linespacing=1.5)

ax=fig.add_axes([.367,.285,.607,.61]);base(ax,[-49,-20,23,57],'bone_detail',True);fixed_routes(ax,90,'detail');events(ax,90,'detail');bone_pattern(ax,90,'detail',True)
for ov in X['local_civilian_overrides']:
 if ov['id']=='O_ASSISTANT':continue
 arrow_line(ax,shape(ov['geometry']),'#9b833c',.9,'detail_civilian_'+ov['id'],True)
for a,b in [(I['B11']['xy_m'],X['local_civilian_overrides'][2]['geometry']['coordinates'][0]),(point(90),BX['handoff']['attention_target_xy_m'])]:
 ax.plot([a[0],b[0]],[a[1],b[1]],color='#b29b61',ls=':',lw=.7,zorder=28)
ax.plot(*BX['handoff']['attention_target_xy_m'],'s',ms=4,color='#9b833c',zorder=50)
note(ax,I['B01']['xy_m'],[12,-14],'B01 / B02  +4 / +6\nApproved first two kills',COL['bone'],8,'detail_opening')
note(ax,point(12),[11,-4],'B03  +12\nHousehold voice',COL['bone'],8,'detail_12')
note(ax,point(16),[-33,-10],'B04  +16–21\nBrief domestic familiarity',COL['bone'],8,'detail_16')
note(ax,point(24),[4,4],'B06 / B07  +24–32\nLets M05 hide; deliberate near-miss',COL['bone'],8,'detail_24')
note(ax,point(35),[-17,18],'B08 / B09  +32–38\nChanges angle; attention shifts',COL['bone'],7.5,'detail_38')
note(ax,I['B11']['xy_m'],[-36,49],'B11  +45\nAssistant intercepted on N05\n1 additional fatality',COL['bone'],8,'detail_45')
note(ax,point(51),[-13,47],'B12 / B13  +46–56\nWatches halted water carriers',COL['bone'],7.5,'detail_50')
note(ax,point(60),[-11,33],'J06  +58–64\nReturns to unfinished encounter',COL['bone'],7.5,'detail_return')
note(ax,point(90),[-43,-2],'B16–B18  +64–90\nWatches M05 from west of coop\nNext action remains unchosen',COL['bone'],8,'detail_90')
note(ax,I['B07']['intentional_target_xy_m'],[-41,4],'× Intentional ground hit\nNo injury',COL['bone'],7,'detail_miss')
note(ax,[-18,35],[-40,32],'M04: both alive\nShort step off the walking line','#8e7733',7.5,'detail_water')
plain(ax,-35,21,'BLACKSMITH',7.5,weight='bold');plain(ax,7,34,'TAVERN\nUnchanged',7.5,weight='bold');plain(ax,-11,-3,'WITCH\nHOME',7.5,weight='bold');plain(ax,14,13,'Lower homes',7.5)
plain(ax,5,52,'Blood strike +56\nUnchanged',7.5,color=COL['blood']);scalebar(ax,-46,-17,10)

fig.text(.377,.255,'HOW TO READ BONE',fontsize=11,weight='bold',color=INK)
fig.text(.377,.239,'Violet dotted arrows: short bursts, each with a recorded attention trigger.\nOpen rings: observation / torment. Stars: attacks. Hexagon: current Bone position.\nOchre: immediate civilian movement or sight/attention line; never a future escape plan.',fontsize=9,color='#60716b',linespacing=1.6,va='top')
fig.text(.026,.165,'LOCKED MASSACRE BEHAVIOURAL RULES',fontsize=12,weight='bold',color=INK)
for x,title,texts in [(.026,'WITCH = DESTINATION','Walks toward the Mayor.\nDoes not divert or dodge her creations.'),(.268,'BLOOD = CONCENTRATION','Seeks substantial populations.\nApproved first strike only here.'),(.510,'BONE = ATTENTION','Malicious, precise, stimulus-led.\nIntended hits never miss.'),(.752,'BARRIER = BOUNDARY /\nREACTIVE WEAPON','Contact-reactive from +90.\nNo contact or response simulated.')]:
 fig.text(x,.148,title,fontsize=9.5,weight='bold',color=INK,va='top');fig.text(x,.111,texts,fontsize=9,color='#60716b',va='top',linespacing=1.5)
fig.text(.026,.061,'ACTION → REACTION → ACTION → REACTION',fontsize=13,weight='bold',color=INK)
fig.text(.026,.04,'Next: villagers choose their first responses. No next major actor/barrier action is selected here. No UE changes or final body/destruction placement.',fontsize=9.3,color='#60716b')
save(fig,'06_T1_bone_completed',True)

fig=plt.figure(figsize=(28,20),facecolor=BG);fig.text(.024,.966,'T1  /  FIRST 90 SECONDS — BONE COMPLETED',fontsize=26,weight='bold',color=INK)
fig.text(.024,.944,'Current Step 2B timeline  ·  Supersedes the earlier 05 timeline for review; the approved original remains unchanged',fontsize=11,color='#60716b')
panels=[(0,'Release / ordinary village','Bone leaves; the first two events remain at +4/+6.'),(30,'Local torment / uneven knowledge','Bone is watching M05 hide. Most still lack attack knowledge.'),(60,'Sealed / major strike has occurred','Bone is returning south. One additional victim; local changes only.'),(90,'Opaque / reactive boundary','Bone watches M05 by the coop. Stop at global alarm.')]
frames={}
for i,(t,title,caption) in enumerate(panels):
 x=.022+i*.245;fig.text(x,.915,'T + '+str(t).zfill(2)+' s',fontsize=20,weight='bold',color=INK);fig.text(x,.892,title,fontsize=10.5,weight='bold',color=INK)
 ax=fig.add_axes([x,.334,.229,.542]);base(ax,D['main_extent'],'bone_timeline'+str(t),True);ax.set_anchor('N');barrier(ax,t,'frame'+str(t));fixed_routes(ax,t,'frame'+str(t));events(ax,t,'frame'+str(t));bone_pattern(ax,t,'frame'+str(t));awareness(ax,t,'frame'+str(t),3.1);direction(ax);scalebar(ax,-104,-165,50)
 bp=point(t);note(ax,bp,[-66,-30] if t in [30,90] else [-61,17] if t==60 else [30,-30],'Bone +'+str(t),COL['bone'],7,'frame_bone'+str(t))
 if t==90:plain(ax,0,174,'Mayor not reached',7)
 totals={k:sum(a['states'][str(t)].get(k,0) for a in S['cohort_awareness']) for k in STATE};summary='\n'.join(f'{totals[k]:>3}  {SN[k]}' for k in ['U','Q','A','P','T','V','D'] if totals[k])
 fig.text(x,.30,caption,fontsize=8.8,color=INK);fig.text(x,.274,summary,fontsize=10,color=INK,va='top',linespacing=1.5)
 fig.canvas.draw();r=ax.get_position();frames[str(t)]={'world_extent_m':D['main_extent'],'png_frame_px':[r.x0*7000,(1-r.y1)*5000,r.width*7000,r.height*5000]}
state_legend(fig,.024,.084,.148,9)
fig.text(.024,.037,'At +90 the barrier can answer physical contact lethally; no contact has occurred in this simulation. Daylight loss starts global alarm, not identical knowledge or preselected flight.',fontsize=9,color='#60716b')
fig.text(.024,.017,'Bone: violet incident rings and short dotted bursts. Blood/Witch retain their routes. Pale plan backgrounds preserve readability; this is not a lighting render.',fontsize=9,color='#60716b')
save(fig,'07_T1_bone_timeline')

with (OUT/'t1b_awareness.csv').open('w',newline='',encoding='utf-8') as fp:
 w=csv.writer(fp);w.writerow(['cohort','T0_count','seconds','unaware','uncertain','aware','local_panic','trapped_aware','global_alarm','fatalities'])
 for c in S['cohort_awareness']:
  for t,s in c['states'].items():w.writerow([c['cluster_id'],c['initial_count'],t]+[s.get(k,0) for k in ['U','Q','A','P','T','V','D']])
assert all(hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h for n,h in X['source_sha256'].items())
files=['06_T1_bone_completed.png','06_T1_bone_completed.svg','07_T1_bone_timeline.png','bone_completion.json','massacre_behaviour_rules.json','render_bone_completion.py','t1b_awareness.csv']
if (OUT/'T1_BONE_COMPLETION.md').exists():files.append('T1_BONE_COMPLETION.md')
manifest=dict(schema='t1b-review/v1',image_dimensions={'06_T1_bone_completed.png':[6000,5000],'07_T1_bone_timeline.png':[7000,5000]},timeline_frames=frames,files={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in files},source_files_unchanged={n:True for n in X['source_sha256']},stop_time_s=90,initial_population=170,living=163,fatalities=7,injured_in_living=4,ue_edits=False)
(OUT/'t1b_manifest.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
print('Rendered Bone completion and revised timeline. All 23 approved source files remain unchanged.')
