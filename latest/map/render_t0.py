"""Render only the separate T0 activity sheet; never writes either clean map.

Run python render_t0.py MAP_DIRECTORY [T0_DIRECTORY]. Both default to this
directory in the published package. Reads the existing renderer's definitions
with AST, stopping before its figure/export code, so base styling stays shared.
"""
import ast, hashlib, json, sys, textwrap
from pathlib import Path
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
T=json.loads((OUT/'t0_activity.json').read_text(encoding='utf-8'))
total=sum(c['count'] for c in T['population_clusters'])
assert total==T['represented_population'],'Update represented_population after editing cluster counts.'
for c in T['population_clusters']:
    assert c['count']>=0 and sum(d['count'] for d in c['distribution'])==c['count'],c['id']
    assert sum(m['count'] for m in T['narrative_micro_groups'] if m['cluster_id']==c['id'])<=c['count'],c['id']
counts={c['id']:c['count'] for c in T['population_clusters']}
zone_total=lambda ids:sum(counts[f'P{i:02}'] for i in ids)
source=BASE/'render_map.py'
assert hashlib.sha256(source.read_bytes()).hexdigest()==T['protected_base_file_sha256']['render_map.py'],'Base renderer changed; review integration before rendering.'
tree=ast.parse(source.read_text(encoding='utf-8'))
cut=next(i for i,node in enumerate(tree.body) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in node.targets))
core={ '__file__':str(source)}; saved=list(sys.argv)
sys.argv=['render_map.py',str(BASE)]
exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(source),'exec'),core)
sys.argv=saved
plt=core['plt']; np=core['np']; Image=core['Image']; D=core['D']; base=core['base']; plain=core['plain']; scalebar=core['scalebar']; BG=core['BG']; INK=core['INK']
from matplotlib.patches import FancyArrowPatch, Rectangle
from shapely.geometry import shape, Point, box
assert D['geometry_sha256']==T['source']['map_geometry_sha256']
POP='#146a70'; MOVE='#a67421'; MICRO='#6d4777'; LIGHT='#e9f3f0'
fig=plt.figure(figsize=(24,20),facecolor=BG)
fig.text(.033,.962,'T0  /  NORMAL VILLAGE ACTIVITY',fontsize=27,weight='bold',color=INK)
fig.text(.033,.938,'MASSACRE PLANNING — STEP 1  |  Late afternoon approaching early evening  |  Working time choice',fontsize=11,color='#60706a')
fig.text(.971,.962,f'{total} PEOPLE  ·  {len(counts)} CLUSTERS',fontsize=12,weight='bold',color=POP,ha='right')
fig.text(.971,.938,f"Existing survey geometry  ·  {len(T['narrative_micro_groups'])} ordinary micro-groups  ·  No UE edits",fontsize=9,color='#60706a',ha='right')

overview=fig.add_axes([.025,.174,.466,.735]);base(overview,D['main_extent'],'t0_overview')
detail=fig.add_axes([.51,.456,.463,.443]);base(detail,[-70,0,66,111],'t0_detail',True)
fig.text(.517,.908,'DAILY LIFE AROUND THE CENTRE AND HOUSEHOLDS',fontsize=12,weight='bold',color=INK)

def movement(axis,prefix):
    xmin,xmax=axis.get_xlim();ymin,ymax=axis.get_ylim();region=box(xmin,ymin,xmax,ymax)
    for f in T['ordinary_movement_flows']:
        g=shape(f['geometry']);clip=g.intersection(region)
        if clip.is_empty:continue
        core['draw_geom'](axis,clip,'none',MOVE,1.35,21,prefix+'_t0_flow_'+f['id'],.90)
        # Arrow heads follow existing route tangents; no straight cross-country arrows.
        for frac in ([.5,.92] if g.length>60 else [.8]):
            d=g.length*frac; a=g.interpolate(max(0,d-2.3));b=g.interpolate(d)
            if region.contains(a) and region.contains(b):
                arrow=FancyArrowPatch((a.x,a.y),(b.x,b.y),arrowstyle='-|>',mutation_scale=9,lw=1.1,color=MOVE,zorder=23)
                arrow.set_gid(prefix+'_t0_flow_'+f['id']+'_arrow_'+str(frac));axis.add_patch(arrow)

movement(overview,'overview');movement(detail,'detail')
for f in T['ordinary_movement_flows']:
    axis=overview if f['label_panel']=='overview' else detail
    artist=axis.text(*f['label_xy_m'],f['id'],fontsize=6.8,ha='center',va='center',color=MOVE,weight='bold',zorder=40,bbox=dict(fc=BG,ec='none',alpha=.95,pad=1.6))
    artist.set_gid(f['label_panel']+'_t0_flow_'+f['id']+'_label')
def callout(axis,xy,tag,text,color,gid,fontsize=8.5,ha='center',bold=False):
    artist=axis.annotate(text,xy=xy,xytext=tag,ha=ha,va='center',fontsize=fontsize,color=color,weight='bold' if bold else 'normal',zorder=43,
        bbox=dict(boxstyle='round,pad=.27',fc=BG,ec=color,lw=.55,alpha=.98),
        arrowprops=dict(arrowstyle='-',color=color,lw=.65,shrinkA=2,shrinkB=2,connectionstyle='arc3,rad=0'))
    artist.set_gid(gid)
    marker,=axis.plot(*xy,'o',mfc=BG,mec=color,ms=3,mew=.8,zorder=42);marker.set_gid(gid+'_anchor')
    return artist
for c in T['population_clusters']:
    name=textwrap.fill(c['name'],24)
    callout(overview,c['anchor_xy_m'],c['label_xy_m'],f"{c['id']} · ~{c['count']}\n{name}",POP,'overview_t0_population_'+c['id'],8.1,bold=True)

for m in T['narrative_micro_groups']:
    axis=overview if m['id'] in ['M01','M02','M03','M12'] else detail
    callout(axis,m['xy_m'],m['label_xy_m'],m['id'],MICRO,('overview' if axis is overview else 'detail')+'_t0_micro_'+m['id'],8.5,bold=True)

# Existing landmarks remain contextual labels, separate from all activity data.
plain(overview,0,-153,'FOREST APPROACH',8,weight='bold')
plain(overview,30,-107,'Working farmland',8.5)
plain(overview,20,4,'Village Gate',8)
plain(overview,-53,161,'Cart / horse access',8)
plain(overview,35,123,'Formal stairs',8)
callout(overview,[-11,-3],[-90,-16],"Witch's house\nNo public activity assigned",'#646d69','context_witch',7.6)
callout(overview,[36,106],[78,115],'Two open graves\nNo gathering','#646d69','context_graves',7.6)
plain(overview,76,133,'Future burial land\nUnoccupied',7.5)
overview.annotate('',xy=(-101,184),xytext=(-101,168),arrowprops=dict(arrowstyle='-|>',color=INK,lw=1),zorder=50)
plain(overview,-101,191,'N* / +UE X',8,weight='bold')
scalebar(overview,-105,-165,50)
rect=Rectangle((-70,0),136,111,fill=False,ec='#6e8179',ls=(0,(5,4)),lw=.65,zorder=25);overview.add_patch(rect)

plain(detail,-2,45,'CENTRE / WELL',7.5,weight='bold')
plain(detail,6,34,'TAVERN',8,color='#f8f8f4',weight='bold')
plain(detail,-35,19,'BLACKSMITH',7,weight='bold')
plain(detail,23,100,'CHURCH',7.5,weight='bold')
plain(detail,41,102,'Open graves\nNo activity',7.2,ha='left')
plain(detail,48,107,'Burial reserve',7,ha='left')
plain(detail,-4,106,'Stairs continue uphill',7.3)
plain(detail,7,1.8,'Gate',7)
plain(detail,-23,76,'Western homes',7.5)
plain(detail,26,47,'Older homes',7.5)
scalebar(detail,-63,4.2,20)

# Legend and census explain the meaning of group markers and avoid double counts.
fig.text(.035,.145,str(total),fontsize=35,weight='bold',color=POP)
fig.text(.102,.151,'APPROXIMATE ORDINARY POPULATION',fontsize=11,weight='bold',color=INK)
fig.text(.102,.133,f"{zone_total([1,2,3,4,5])} fields / farms / approach   ·   {zone_total([6,10,11,12,14])} households\n{zone_total([7,8,9])} centre / tavern / forge   ·   {zone_total([13,15,16,17])} forest / church / estate",fontsize=9.5,color=INK,linespacing=1.6)
fig.text(.036,.107,'P01 · ~6',fontsize=10,weight='bold',color=POP,bbox=dict(fc=LIGHT,ec=POP,lw=.6,pad=3))
fig.text(.104,.108,'Population reference for an area; not a single crowd.',fontsize=9,color=INK)
fig.text(.036,.083,'——›',fontsize=17,weight='bold',color=MOVE)
fig.text(.104,.087,'F01–F11: normal journeys; people already counted in P clusters.',fontsize=9,color=INK)
fig.text(.036,.061,'M01',fontsize=10,weight='bold',color=MICRO,bbox=dict(fc=BG,ec=MICRO,lw=.6,pad=3))
fig.text(.104,.062,'Micro-group within its parent cluster; never extra people.',fontsize=9,color=INK)

fig.text(.518,.428,f"{len(T['narrative_micro_groups'])} SMALL STORIES ALREADY IN PROGRESS",fontsize=12,weight='bold',color=INK)
short={
'M01':'P05 · 2 people · produce/tools toward home',
'M02':'P02 · 1 person · check and close livestock gate',
'M03':'P04 · 2 people · fodder and tools into storage',
'M04':'P08 · 2 people · fill water containers',
'M05':'P06 · 2 people · parent and child going home',
'M06':'P09 · 3 people · receive barrels and food',
'M07':'P07 · 2 people · finish a cart wheel',
'M08':'P10 · 2 people · talk beside shared storage',
'M09':'P10 · 5 people · four children and a caregiver',
'M10':'P11 · 1 person · carry firewood for cooking',
'M11':'P15 · 3 people · return with wood and tools',
'M12':'P17 · 2 people · provisions up the service road',
'M13':'P13 · 1 person · put away the church bucket'}
for i,m in enumerate(T['narrative_micro_groups']):
    col=0 if i<7 else 1;row=i if i<7 else i-7;x=.518+col*.238;y=.402-row*.047
    fig.text(x,y,m['id'],fontsize=10,weight='bold',color=MICRO)
    fig.text(x+.029,y,m['name'],fontsize=10,weight='bold',color=INK)
    summary=f"{m['cluster_id']} · {m['count']} {'person' if m['count']==1 else 'people'} · "+short[m['id']].split(' · ',2)[2]
    fig.text(x,y-.016,summary,fontsize=8.2,color='#5d6c65')
fig.text(.756,.094,'NO SUPERNATURAL PLAN',fontsize=10,weight='bold',color=INK)
fig.text(.756,.074,'Clean base and blank planning maps remain separate.\nNo attack, escape, barrier or aftermath is authored.',fontsize=8.8,color='#5d6c65',linespacing=1.5)
fig.text(.034,.026,'T0 snapshot counts are distinct from near-term movement. Indoor life is included. *Map north = UE +X; distance bars are horizontal metres.',fontsize=9,color='#60706a')
fig.text(.971,.026,'BASE '+D['geometry_sha256'][:12]+'  ·  T0 LAYER ONLY',fontsize=9,color='#60706a',ha='right')

fig.canvas.draw()
# Retain frame coordinates to turn future edit positions back into metric data.
views={}
for n,a in [('overview',overview),('activity_detail',detail)]:
    p=a.get_position();x0,x1=a.get_xlim();y0,y1=a.get_ylim()
    views[n]=dict(world_extent_m=[x0,y0,x1,y1],png_frame_px=[p.x0*6000,(1-p.y1)*5000,p.width*6000,p.height*5000])
png=OUT/'03_T0_normal_activity.png';svg=OUT/'03_T0_normal_activity.svg'
fig.savefig(png,dpi=250,facecolor=BG)
im=Image.open(png).convert('RGB');im.quantize(colors=256,dither=Image.Dither.NONE).save(png,optimize=True)
fig.savefig(svg,facecolor=BG,metadata={'Title':T['title'],'Description':'Ordinary T0 population and movement only. All future massacre layers remain empty.'})
ns='http://www.w3.org/2000/svg';ink='http://www.inkscape.org/namespaces/inkscape'
root=ET.parse(svg).getroot()
for axis in root.findall('.//{'+ns+'}g'):
    if not axis.get('id','').startswith('axes_'):continue
    for token,title in [('population','T0 population clusters'),('flow','T0 ordinary movement'),('micro','T0 narrative micro-groups')]:
        elements=[child for child in list(axis) if '_t0_'+token+'_' in child.get('id','')]
        if not elements:continue
        group=ET.SubElement(axis,'{'+ns+'}g',{'id':axis.get('id')+'_t0_'+token,'{'+ink+'}groupmode':'layer','{'+ink+'}label':title})
        for child in elements:axis.remove(child);group.append(child)
for name in ['Blood route','Bone route','Witch route','Civilian reaction','Escape attempts','Blood barrier','Event nodes','Attack directions','Structural damage','Chronology']:
    ET.SubElement(root,'{'+ns+'}g',{'id':'future_'+name.lower().replace(' ','_'),'{'+ink+'}groupmode':'layer','{'+ink+'}label':name+' (empty)'})
ET.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
plt.close(fig)
im.thumbnail((1800,1500));im.save(OUT.parent/'t0-preview.png')
manifest=dict(schema='t0-review/v1',population=total,clusters=len(T['population_clusters']),micro_groups=len(T['narrative_micro_groups']),ordinary_flows=len(T['ordinary_movement_flows']),base_geometry_sha256=D['geometry_sha256'],png_dimensions=[6000,5000],views=views,files={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['03_T0_normal_activity.png','03_T0_normal_activity.svg','t0_activity.json','render_t0.py']},protected_base_files_verified={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h for n,h in T['protected_base_file_sha256'].items()})
assert all(manifest['protected_base_files_verified'].values())
(OUT/'t0_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Rendered T0 only; all nine protected base files unchanged.',flush=True)
