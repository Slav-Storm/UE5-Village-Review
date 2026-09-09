"""Render only T1 planning outputs from the separate editable simulation layer.
Run python render_t1.py MAP_DIRECTORY [OUTPUT_DIRECTORY]. No Unreal calls.
"""
import ast,sys,json,hashlib,math,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
S=json.loads((OUT/'t1_simulation.json').read_text(encoding='utf-8'))
T0=json.loads((BASE/'t0_activity.json').read_text());C={c['id']:c for c in T0['population_clusters']};A={a['id']:a for a in S['actors']};M={m['id']:m for m in T0['narrative_micro_groups']}
start=A['bone']['timed_points'][0]['xy_m']
for name,h in S['protected_file_sha256'].items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h,name
source=BASE/'render_map.py';tree=ast.parse(source.read_text(encoding='utf-8'));cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in n.targets));oldargs=sys.argv;sys.argv=['render_map.py',str(BASE)];core={'__file__':str(source)};exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(source),'exec'),core);sys.argv=oldargs
plt=core['plt'];np=core['np'];Image=core['Image'];base=core['base'];draw=core['draw_geom'];plain=core['plain'];scalebar=core['scalebar'];D=core['D'];BG=core['BG'];INK=core['INK']
from matplotlib.patches import FancyArrowPatch,Wedge,Circle
from shapely.geometry import shape,Point,LineString,box
from shapely.ops import substring
COL={'blood':'#a52838','bone':'#654382','witch':'#087c7c'}
STATE={'U':'#d7dcd9','Q':'#d9b860','A':'#568fae','P':'#cf7839','T':'#8e73a7','V':'#b93243','D':'#45494a'}
SN={'U':'Unaware','Q':'Uncertain','A':'Aware','P':'Local panic','T':'Trapped-aware*','V':'Village-wide alarm','D':'Early fatalities'}
B=S['barrier'];rim=LineString(shape(B['geometry']).exterior.coords)

def arrow_line(ax,g,color,lw=1.5,gid='route',dashes=False):
    draw(ax,g,'none',color,lw,24,gid,ls=(0,(4,3)) if dashes else 'solid')
    if g.geom_type=='LineString' and g.length>3:
        for fraction in ([.45,.92] if g.length>70 else [.82]):
            e=g.interpolate(g.length*fraction);q=g.interpolate(max(0,g.length*fraction-2.4))
            p=FancyArrowPatch((q.x,q.y),(e.x,e.y),arrowstyle='-|>',mutation_scale=8,color=color,lw=lw*.7,zorder=26);p.set_gid(gid+'_arrow'+str(fraction));ax.add_patch(p)

def note(ax,point,textpoint,text,color=INK,size=8,gid='note',ha='center'):
    obj=ax.annotate(text,xy=point,xytext=textpoint,ha=ha,va='center',fontsize=size,color=color,zorder=55,
        bbox=dict(fc=BG,ec=color,lw=.4,alpha=.97,boxstyle='round,pad=.25'),
        arrowprops=dict(arrowstyle='-',color=color,lw=.6,shrinkA=2,shrinkB=2));obj.set_gid(gid);return obj

def barrier(ax,t,prefix,reference=True):
    g=shape(B['geometry']);region=box(ax.get_xlim()[0],ax.get_ylim()[0],ax.get_xlim()[1],ax.get_ylim()[1])
    if reference:draw(ax,g.intersection(region),'none','#aa969a',.6,15,prefix+'_barrier_reference',.7,ls=(0,(3,4)))
    if t>=60:draw(ax,g.intersection(region),'#9e2b3a','none',0,16,prefix+'_barrier_tint',.025 if t==60 else .075)
    if t>0:
        for i,pts in enumerate(B['snapshot_arcs'][str(t)]):draw(ax,LineString(pts).intersection(region),'none','#ab3e4d',2.0,21,prefix+'_barrier_front_'+str(i))
    p=B['seed_xy_m'];ax.plot(*p,'o',mfc=BG,mec='#9e2b3a',ms=4,zorder=30)

def awareness(ax,t,prefix,radius=3.0,labels=True):
    for cohort in S['cohort_awareness']:
        p=cohort['anchor_xy_m'];values=cohort['states'][str(t)];angle=90;total=cohort['initial_count']
        for state,count in values.items():
            end=angle+360*count/total
            patch=Wedge(p,radius,angle,end,facecolor=STATE[state],edgecolor=BG,lw=.2,zorder=35);patch.set_gid(prefix+'_awareness_'+cohort['cluster_id']+'_'+state);ax.add_patch(patch);angle=end
        ring=Circle(p,radius,fc='none',ec='#52615c',lw=.45,zorder=36);ax.add_patch(ring)
        if labels:ax.text(p[0]+radius+1.2,p[1],cohort['cluster_id'],fontsize=6.5,color=INK,va='center',zorder=40,bbox=dict(fc=BG,ec='none',alpha=.85,pad=.6))

def actor_paths(ax,prefix,until=90):
    for aid in ['blood','witch','bone']:
        a=A[aid];g=shape(a['geometry'])
        if aid=='blood':g=substring(g,0,g.length*max(0,min(1,(until-2)/52)))
        if aid=='witch':g=substring(g,0,g.length*max(0,min(1,(until-24)/66)))
        if aid=='bone':
            q=[p['xy_m'] for p in a['timed_points'] if p['t_s']<=until]
            if len(q)<2:continue
            g=LineString(q)
        if g.geom_type=='LineString':arrow_line(ax,g,COL[aid],2.0 if aid=='blood' else 1.35,prefix+'_actor_'+aid,aid=='witch')
    if until>=12:
        g=shape(A['bone']['local_position_envelope']);draw(ax,g,'none',COL['bone'],.85,28,prefix+'_bone_local_envelope',.8,ls=(0,(2,3)))

def events(ax,until,prefix):
    if until>=56:draw(ax,shape(S['events'][2]['impact_zone']),'#b83345','#912638',.65,29,prefix+'_impact_zone',.20)
    for event in S['events']:
        if event['t_s']>until:continue
        p=ax.plot(*event['xy_m'],marker='*',color=COL[event['actor']],mec=BG,mew=.4,ms=9,zorder=44)[0];p.set_gid(prefix+'_event_'+event['id'])

def direction(ax,x=-103,y=184):
    ax.annotate('',xy=(x,y),xytext=(x,y-13),arrowprops=dict(arrowstyle='-|>',color=INK,lw=.8),zorder=60)
    plain(ax,x,y+5,'N / +UE X',7.5)

def state_legend(fig,x,y,step=.13,fontsize=8.5):
    for i,k in enumerate(['U','Q','A','P','T','V','D']):
        fig.text(x+(i%4)*step,y-(i//4)*.021,'●',color=STATE[k],fontsize=12)
        fig.text(x+.012+(i%4)*step,y+.001-(i//4)*.021,SN[k],fontsize=fontsize,color=INK)

fig=plt.figure(figsize=(24,20),facecolor=BG)
fig.text(.032,.963,'T1  /  THE FIRST 90 SECONDS',fontsize=28,weight='bold',color=INK)
fig.text(.032,.939,'MASSACRE PLANNING — STEP 2  |  Existing T0 population and geometry preserved  |  Working simulation',fontsize=11,color='#60716b')
fig.text(.975,.963,'RELEASE → LOCAL VIOLENCE → SEALED → OPAQUE',ha='right',fontsize=10,color='#60716b')
fig.text(.975,.939,'No UE edits  ·  No final bodies / destruction  ·  Stop at +90',ha='right',fontsize=9,color='#60716b')
overview=fig.add_axes([.026,.172,.462,.731]);base(overview,D['main_extent'],'t1_overview');barrier(overview,60,'overview');actor_paths(overview,'overview');events(overview,90,'overview');awareness(overview,60,'overview',2.8);direction(overview);scalebar(overview,-105,-167,50)
plain(overview,37,-111,'Farmland / approach',8)
plain(overview,12,157,"Mayor's grounds",8)
plain(overview,36,89,'Church / cemetery',8)
note(overview,B['seed_xy_m'],[-94,-30],'Spell seed / +0',COL['blood'],8,'overview_barrier_seed')
note(overview,B['seam_xy_m'],[91,43],'Last seam\n+60',COL['blood'],8,'overview_barrier_seam')
for i,pts in enumerate(B['snapshot_arcs']['30']):
    p=pts[-1];note(overview,p,[-93,155] if i==0 else [60,-133],'+30 front',COL['blood'],8,'overview_barrier30_'+str(i))
plain(overview,-12,189,'Full outline = proposed spell rim',7.5)
fig.text(.034,.147,'COHORT AWARENESS AT +60',fontsize=11,weight='bold',color=INK)
state_legend(fig,.034,.126,.116,8)
fig.text(.034,.079,'Pins remain at T0 cohort references. Travelling subsets are tracked separately.\n*Trapped-aware is visual inference; no escape/collision test is authored.',fontsize=8.7,color='#60716b',linespacing=1.5)
fig.text(.034,.048,'Routes:  Blood — solid red     Bone — violet     Witch — dashed teal',fontsize=9,color=INK)

fig.text(.522,.91,'OPENING ACTIONS / LOWER VILLAGE AND CENTRE',fontsize=12,weight='bold',color=INK)
detail=fig.add_axes([.516,.439,.464,.455]);base(detail,[-48,-27,46,68],'t1_opening',True);actor_paths(detail,'detail');events(detail,90,'detail')
for mid in ['N02','R01','R02','R03']:
    motion=next(m for m in S['normal_and_immediate_motions'] if m['id']==mid)
    arrow_line(detail,shape(motion['geometry']),'#468977' if mid=='N02' else '#b18c43',.85,'detail_movement_'+mid,True)
note(detail,start,[-31,-21],'Cellar exit\nSpell initiated here',INK,8,'detail_start')
note(detail,S['events'][0]['xy_m'],[15,-16],'E01 +4 / E02 +6\nM01: 2 early fatalities',COL['bone'],8.5,'detail_E01_E02')
note(detail,[-4.6,-5.5],[24,-4],'Bone: last seen +12\nLocal pocket only afterward',COL['bone'],8,'detail_bone_cut')
note(detail,S['events'][2]['xy_m'],[15,61],'E03 +56 · well / stalls\n4 fatal + 4 injured (working)',COL['blood'],8.5,'detail_E03')
for t,labelxy in [(30,[-30,-8]),(60,[-16,2]),(90,[-34,33])]:
    p=A['witch']['snapshots'][str(t)][:2];detail.plot(*p,'D',ms=5,color=COL['witch'],mec=BG,mew=.5,zorder=48);note(detail,p,labelxy,'Witch +'+str(t),COL['witch'],8,'detail_witch'+str(t))
b30=A['blood']['snapshots']['30'][:2];detail.plot(*b30,'s',ms=4,color=COL['blood'],zorder=48);note(detail,b30,[2,21],'Blood +30',COL['blood'],8,'detail_blood30')
m4=next(m for m in S['micro_groups'] if m['micro_id']=='M04')['positions']['60'];note(detail,m4,[-34,49],'M04 already clear\nNormal water trip', '#397d6d',8,'detail_M04')
plain(detail,6,34,'TAVERN\n7 in / 7 out',8.7,weight='bold')
note(detail,M['M06']['xy_m'],[33,25],'M06: 3 outside\nRoof masks strike view',INK,7.6,'detail_M06')
note(detail,M['M09']['xy_m'],[36,60],'M09: unhurt\nSees / hears alarm',INK,7.6,'detail_M09')
plain(detail,-35,19,'Forge',8);plain(detail,15,5,'Village Gate',8);plain(detail,32,-23,'Orchard warning\ntoward farmyard',7.5)
scalebar(detail,-43,-23,20)

fig.text(.525,.407,'WORKING SEQUENCE',fontsize=12,weight='bold',color=INK)
for y,s in [(.385,'+0 / +2 release   ·   +4 / +6 first Bone kills   ·   +24 Witch walks'),(.365,'+54 Blood arrives   ·   +56 first major strike and local panic'),(.345,'+60 sealed, translucent   ·   ~+66 tavern interior understands'),(.325,'+90 opaque: 164 living people enter village-wide alarm')]:fig.text(.525,y,s,fontsize=9.5,color=INK)
fig.text(.525,.299,'Six early fatalities total; four injured are included among the living.\nEvent stars are incident locations, not final corpse positions.',fontsize=9,color='#60716b',linespacing=1.5)
fig.text(.525,.255,'EXTERNAL DAYLIGHT / WORKING CURVE',fontsize=11,weight='bold',color=INK)
light=fig.add_axes([.548,.079,.41,.153]);ts=[p['t_s'] for p in B['light_curve']];vs=[p['external_daylight_fraction']*100 for p in B['light_curve']]
light.set_facecolor(BG);light.plot(ts,vs,color=COL['blood'],lw=2);light.fill_between(ts,vs,alpha=.09,color=COL['blood']);light.axvline(60,color='#988b8b',ls='--',lw=.8);light.set_xlim(0,90);light.set_ylim(0,105);light.set_xticks([0,24,30,56,60,75,90]);light.set_yticks([0,25,50,75,100]);light.tick_params(labelsize=8);light.spines[['top','right']].set_visible(False);light.set_xlabel('Seconds since release',fontsize=8);light.set_ylabel('% of outside daylight',fontsize=8);light.text(60,95,'sealed',fontsize=8,ha='right');light.text(88,7,'opaque',fontsize=8,ha='right');light.grid(alpha=.15)
fig.text(.032,.023,'Plan projection, not a visibility / acoustics engine. Base geometry '+D['geometry_sha256'][:12]+' preserved. No event beyond +90 is authored.',fontsize=9,color='#60716b')

def save(fig,name,svg=False):
    fig.savefig(OUT/(name+'.png'),dpi=250,facecolor=BG)
    im=Image.open(OUT/(name+'.png')).convert('RGB');im.quantize(colors=256,dither=Image.Dither.NONE).save(OUT/(name+'.png'),optimize=True)
    if svg:
        path=OUT/(name+'.svg');fig.savefig(path,facecolor=BG,metadata={'Title':S['title'],'Description':'Separate editable T1 opening simulation, ending at90 seconds. No final body/debris positions.'})
        ns='http://www.w3.org/2000/svg';ink='http://www.inkscape.org/namespaces/inkscape';root=ET.parse(path).getroot()
        for axes in root.findall('.//{'+ns+'}g'):
            if not axes.get('id','').startswith('axes_'):continue
            groups=[('barrier','T1 barrier'),('actor','T1 actor routes'),('bone_local','T1 bounded Bone pocket'),('impact','T1 event footprint'),('event','T1 opening events'),('movement','T1 civilian movement'),('awareness','T1 awareness')]
            for token,label in groups:
                matches=[g for g in list(axes) if '_'+token+'_' in g.get('id','')]
                if matches:
                    group=ET.SubElement(axes,'{'+ns+'}g',{'id':axes.get('id')+'_'+token,'{'+ink+'}groupmode':'layer','{'+ink+'}label':label})
                    for g in matches:axes.remove(g);group.append(g)
        ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
    im.thumbnail((1800,1500));im.save(OUT.parent/(name+'_preview.png'));plt.close(fig)
save(fig,'04_T1_first_90_seconds',True)

fig=plt.figure(figsize=(28,20),facecolor=BG)
fig.text(.024,.966,'T1  /  HOW THE TRAP CLOSES',fontsize=29,weight='bold',color=INK)
fig.text(.024,.944,'Four synchronized snapshots  ·  Same geometry and T0-origin cohorts  ·  Pie colours show awareness counts within each cohort',fontsize=11,color='#60716b')
panels=[(0,'Release / spell begins','Normal daylight. Dashed rim is future reference only.'),(30,'Partial enclosure','Half the rim is formed; most people lack attack knowledge.'),(60,'Sealed / translucent','Physical enclosure complete; outside daylight still visible.'),(90,'Opaque / alarm begins','External daylight is gone. Stop before onward reactions.')]
view_records={}
for i,(t,title,caption) in enumerate(panels):
    x=.022+i*.245
    fig.text(x,.914,'T + '+str(t).zfill(2)+' s',fontsize=20,weight='bold',color=INK)
    fig.text(x,.892,title,fontsize=11,weight='bold',color=INK)
    ax=fig.add_axes([x,.331,.229,.545]);base(ax,D['main_extent'],'timeline'+str(t),True);ax.set_anchor('N');barrier(ax,t,'timeline'+str(t));actor_paths(ax,'timeline'+str(t),t);events(ax,t,'timeline'+str(t));awareness(ax,t,'timeline'+str(t),3.2);direction(ax);scalebar(ax,-104,-165,50)
    p=A['witch']['snapshots'][str(t)][:2];ax.plot(*p,'D',ms=5,color=COL['witch'],mec=BG,mew=.4,zorder=50)
    if t:plain(ax,-38,-37,'Witch +'+str(t),7,color=COL['witch'])
    if t>=12:plain(ax,25,-23,'Bone: local\npocket only',6.5,color=COL['bone'])
    count={k:sum(a['states'][str(t)].get(k,0) for a in S['cohort_awareness']) for k in STATE}
    fig.text(x,.293,caption,fontsize=9,color=INK,wrap=True)
    summary='\n'.join(f"{count[k]:>3}  {SN[k]}" for k in ['U','Q','A','P','T','V','D'] if count[k])
    fig.text(x,.267,summary,fontsize=10,color=INK,linespacing=1.6,va='top')
    if t==0:note(ax,start,[30,-30],'Release / cast',INK,7,'timeline0_start')
    if t==30:note(ax,A['blood']['snapshots']['30'][:2],[-50,25],'Blood en route',COL['blood'],7,'timeline30_blood')
    if t==60:note(ax,S['events'][2]['xy_m'],[45,25],'First strike\n+56',COL['blood'],7,'timeline60_strike')
    if t==90:plain(ax,0,168,'Mayor not reached',7)
    fig.canvas.draw();frame=ax.get_position();view_records[str(t)]=dict(world_extent_m=D['main_extent'],png_frame_px=[frame.x0*7000,(1-frame.y1)*5000,frame.width*7000,frame.height*5000])
state_legend(fig,.024,.082,.148,9)
fig.text(.024,.031,'Pins identify original T0 cohorts, not corpse locations or one crowd per pin. Fatalities stay in the origin ledger; moving subsets are separate in JSON. *Entrapment is inferred visually.',fontsize=9,color='#60716b')
fig.text(.024,.012,'T+90 means village-wide alarm, not universal knowledge of every killing. Map remains pale so the plan can be read; it is not a rendered lighting preview.',fontsize=9,color='#60716b')
save(fig,'05_T1_timeline',False)

files=['04_T1_first_90_seconds.png','04_T1_first_90_seconds.svg','05_T1_timeline.png','t1_simulation.json','render_t1.py']
manifest=dict(schema='t1-review/v1',source_geometry_sha256=D['geometry_sha256'],source_t0_sha256=S['source']['t0_sha256'],image_sizes={'04_T1_first_90_seconds.png':[6000,5000],'05_T1_timeline.png':[7000,5000]},timeline_frames=view_records,files={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in files},protected_unchanged={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h for n,h in S['protected_file_sha256'].items()})
assert all(manifest['protected_unchanged'].values())
(OUT/'t1_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Rendered two T1 sheets; all protected base/T0 files unchanged.',flush=True)
