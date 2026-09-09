"""Render the review maps from editable metric map_data.json. No Unreal dependency."""
import json, sys, math, hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch, Rectangle, Circle
from matplotlib.lines import Line2D
from shapely.geometry import shape, box
from shapely.ops import unary_union
from shapely import make_valid
from PIL import Image
HERE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'package'
D=json.loads((OUT/'map_data.json').read_text());F=D['features'];LM={l['id']:l for l in D['landmarks']}
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':10,'axes.titleweight':'bold','path.simplify':False})
BG='#f8f8f4';INK='#28343a';ROAD='#faf9ef';WOOD='#71866a';BUILD='#647380';LAND='#a0643c'
styles={
 'estate_area':('#eee8db','none',0,2),'agriculture':('#e5ddb9','#ada681',.45,3),
 'civic_area':('#ede6d5','none',0,3),'cemetery_area':('#ded3e2','none',0,3),
 'burial_reserve':('#f1eaf3','#a995b1',.55,3),
 'forest':('#cfdbc8','#99ac8e',.22,4),'orchard_trees':('#9eb38e','#708562',.3,6),
 'road':(ROAD,'#b8af97',.45,6),'footpath':('#e9d4ab','#c4aa7b',.22,7),
 'field':('none','none',0,3),'retaining':('#c5beb1','#938977',.2,8),
 'boundary':('#8b8572','#7d7463',.2,9),'stairs':('#e0ddd5','#6b6c69',.4,10),
 'stair_line':('none','#6b6c69',.3,11),'gate':('#6f7b83','#35434b',.4,11),
 'proxy':('#b7b3a7','#89887c',.2,10),'civic_proxy':('#aba18c','#726a58',.25,10),
 'sign':('#b59155','#735925',.25,11),'cellar_access':('#cfb991','#88714a',.35,13),
 'underground':('none','#8b758e',.45,14),'outbuilding':('#a0a6a6','#647078',.35,12),
 'building':(BUILD,'#374750',.4,12),'grave':('#8e8396','#605369',.25,13),
 'grave_open':('#baab94','#746047',.4,14),'grave_open_outline':('#f8f8f4','#4b3c2a',.8,15),
 'spoil':('#c1aa81','#9d8154',.2,14)
}
ext=box(*D['main_extent']);geoms={f['id']:make_valid(shape(f['geometry'])) for f in F}
def draw_geom(ax,g,fill,edge,lw,zorder,gid,alpha=1,ls='solid'):
    if g.is_empty:return
    if g.geom_type in ['MultiPolygon','GeometryCollection','MultiLineString','MultiPoint']:
        for i,q in enumerate(g.geoms):draw_geom(ax,q,fill,edge,lw,zorder,gid+'_'+str(i),alpha,ls)
    elif g.geom_type=='Polygon':
        vertices=[];codes=[]
        for ring in [g.exterior,*g.interiors]:
            pts=np.asarray(ring.coords);vertices.extend(pts);codes.extend([MPath.MOVETO]+[MPath.LINETO]*(len(pts)-2)+[MPath.CLOSEPOLY])
        p=PathPatch(MPath(vertices,codes),facecolor=fill,edgecolor=edge,lw=lw,zorder=zorder,alpha=alpha,linestyle=ls)
        p.set_gid(gid);ax.add_patch(p)
    elif g.geom_type=='LineString':
        p=np.array(g.coords);line,=ax.plot(p[:,0],p[:,1],color=edge,lw=lw,zorder=zorder,alpha=alpha,ls=ls);line.set_gid(gid)
    elif g.geom_type=='Point':ax.plot(g.x,g.y,'.',color=edge,ms=1,zorder=zorder)
def base(ax,extent,prefix,detail=False):
    ax.set_xlim(extent[0],extent[2]);ax.set_ylim(extent[1],extent[3]);ax.set_aspect('equal');ax.set_facecolor(BG)
    region=box(*extent)
    for spine in ax.spines.values():spine.set_color('#aeb6b3');spine.set_linewidth(.5)
    for f in F:
        c=f['category'];g=geoms[f['id']]
        if not g.intersects(region):continue
        if c=='contour':
            draw_geom(ax,g.intersection(region),'none','#b6b4a5',.25,1,prefix+'_'+f['id'],.7)
        elif c in styles:
            fill,edge,lw,z=styles[c]
            if c=='agriculture':
                fill={'pasture':'#dbe4c7','orchard':'#d0ddbb','garden':'#d4d59e','yard':'#e8dfc9'}.get(f['kind'],fill)
            if c=='building' and f.get('kind') in ['mayor','church','tavern','blacksmith'] or f['id']=='WitchHome':fill='#9b7659';edge='#61442f'
            if c=='underground' and (not detail or f['id']!='CellarFloor'):continue
            draw_geom(ax,g.intersection(region),fill,edge,lw,z,prefix+'_'+f['id'],ls='dashed' if c=='underground' else 'solid')
        elif c=='route_reference' and f['kind'] not in ['stair','alley','farm_path']:
            # Thin neutral centre guide identifies connected existing roads; never an event arrow.
            draw_geom(ax,g.intersection(region),'none','#afa285',.27,7,prefix+'_'+f['id'],.8)
    ax.tick_params(length=0,labelsize=6.8,pad=4,colors='#66736e')
    if detail:ax.set_xticks([]);ax.set_yticks([])
    else:
        ax.set_xticks(np.arange(-100,101,50));ax.set_yticks(np.arange(-150,201,50));ax.grid(color='#aebbb7',alpha=.18,lw=.4,zorder=0)
        ax.set_xlabel('UE +Y / metres',fontsize=8,color='#61706d');ax.set_ylabel('UE +X / metres',fontsize=8,color='#61706d')
def label(ax,key,textxy,text=None,size=9,ha=None):
    p=LM[key]['xy'];txt=text or LM[key]['label'];ha=ha or ('left' if textxy[0]>p[0] else 'right')
    a=ax.annotate(txt,xy=p,xytext=textxy,ha=ha,va='center',fontsize=size,color=INK,zorder=40,
        bbox=dict(boxstyle='round,pad=.22',fc=BG,ec='none',alpha=.95),
        arrowprops=dict(arrowstyle='-',color='#737c77',lw=.55,shrinkA=1,shrinkB=1,connectionstyle='angle3,angleA=0,angleB=90'))
    a.set_gid('label_'+key+'_'+str(len(ax.texts)))
    ax.plot(*p,'o',ms=2.6,mfc=BG,mec='#574f3f',mew=.6,zorder=41)
def plain(ax,x,y,s,size=8,ha='center',color='#697161',weight='normal',rotation=0):
    ax.text(x,y,s,fontsize=size,ha=ha,va='center',color=color,weight=weight,rotation=rotation,zorder=32,
        bbox=dict(fc=BG,ec='none',alpha=.78,pad=1.5))
def scalebar(ax,x,y,metres,labeltext=None):
    ax.plot([x,x+metres],[y,y],color=INK,lw=1.4,zorder=50)
    ax.plot([x,x],[y-0.8,y+.8],color=INK,lw=.8,zorder=50);ax.plot([x+metres,x+metres],[y-.8,y+.8],color=INK,lw=.8,zorder=50)
    ax.text(x+metres/2,y+1.4,labeltext or f'{metres:g} m',ha='center',va='bottom',fontsize=8,color=INK,zorder=51)

fig=plt.figure(figsize=(24,20),facecolor=BG)
title=fig.text(.036,.964,'VILLAGE BASE MAP',fontsize=28,weight='bold',color=INK)
subtitle=fig.text(.037,.939,'Current healthy / pre-massacre scene  |  Orthographic XY projection  |  09 September 2026',fontsize=11,color='#66746d')
fig.text(.966,.958,'SPATIAL REVIEW  /  01',ha='right',fontsize=10,color='#66746d')
fig.text(.966,.939,'Survey: '+D['survey_time_utc'].split('T')[1][:8]+' UTC  ·  No scene layout edits',ha='right',fontsize=9,color='#66746d')

ax=fig.add_axes([.035,.076,.484,.826]);base(ax,D['main_extent'],'overview')
label(ax,'mayor_mansion',(57,173),"Mayor's Mansion  +44.2 m",size=10)
label(ax,'mayor_stairs',(-67,113),"Mayor's Stairs",size=9.5)
label(ax,'mayor_cart',(-84,165),"Mayor's Cart Route",size=9.2)
label(ax,'future_burial',(75,134),'Future Burial Area',size=9.2)
label(ax,'church',(66,102),'Church  +19.7 m',size=9.5)
label(ax,'cemetery',(70,88),'Cemetery  [A]',size=9.2)
label(ax,'village_centre',(-75,58),'Village Centre  +7.9 m',size=9.2)
label(ax,'tavern',(59,33),'Tavern',size=9.5)
label(ax,'blacksmith',(-75,23),'Blacksmith',size=9.5)
label(ax,'witch_house',(-67,-5),"Witch's House  [C]",size=9.2)
label(ax,'cellar_entrance',(-66,-21),'Cellar Entrance',size=8.5)
label(ax,'village_gate',(55,1),'Village Gate  +0 m',size=9.5)
label(ax,'menu_sign',(61,12),'Menu sign (at gate)',size=8)
label(ax,'north_barn',(72,-51),'Farmyard / barn',size=8.3)
label(ax,'south_barn',(-73,-54),'Farmyard / barn',size=8.3)
label(ax,'direction_sign',(50,-25),'Direction sign',size=8)
plain(ax,29,-77,'Crop field',8);plain(ax,34,-39,'Crop field',8);plain(ax,29,-11,'Orchard',8)
plain(ax,-29,-85,'Pasture',8);plain(ax,-43,-45,'Crop field',8);plain(ax,-28,-10,'Paddock',7.5)
ax.annotate('Older residential\npocket',xy=(26,35),xytext=(67,55),fontsize=8,color=INK,ha='left',zorder=40,bbox=dict(fc=BG,ec='none',alpha=.92,pad=2),arrowprops=dict(arrowstyle='-',color='#737c77',lw=.5))
plain(ax,-59,70,'Forest working\nedge',8)
plain(ax,21,-117,'Main approach road',9,ha='left')
plain(ax,0,-161,'FOREST APPROACH',8.5,weight='bold')
plain(ax,-94,191,'FOREST',9,weight='bold');plain(ax,96,-119,'FOREST',9,weight='bold',rotation=90)
ax.annotate('',xy=(-98,179),xytext=(-98,165),arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.2),zorder=60)
plain(ax,-98,184,'N*',10,weight='bold');plain(ax,-98,160,'+UE X',7)
scalebar(ax,-104,-168,50)
plain(ax,25,197,'Map north = uphill / +UE X',8)
for text,extent in [('A',[20,82,70,124]),('B',[-57,93,32,171]),('C',[-25,-23,3,11])]:
    patch=Rectangle((extent[0],extent[1]),extent[2]-extent[0],extent[3]-extent[1],fill=False,lw=.55,ec='#788488',ls=(0,(4,3)),zorder=25);ax.add_patch(patch)
    ax.text(extent[0],extent[3]+1.2,text,fontsize=8,color='#627076',weight='bold',zorder=35)

fig.text(.562,.908,'A  /  CHURCHYARD AND BURIAL RESERVE',fontsize=13,weight='bold',color=INK)
a=fig.add_axes([.56,.617,.41,.274]);base(a,[16,80,77,126],'cemetery',True)
label(a,'church',(16.8,92),'Church',10,ha='left')
label(a,'cemetery',(48,91),'Older graves',9)
label(a,'lover_grave',(31,115),"Lover's Grave",9.5)
label(a,'son_grave',(47,119),"Son's Grave",9.5)
label(a,'future_burial',(65,117),'Future Burial Area\n699 m² · currently empty',9.5,ha='center')
plain(a,35,85,'Public church approach',8)
plain(a,44,109.7,'Space for possible\nthird grave',7.5,ha='left')
a.plot(35.2,110.3,'+',color='#806787',ms=6,zorder=35)
scalebar(a,19,82.5,10)
fig.text(.562,.598,'Two existing graves were opened manually from above. No massacre victims are buried here.',fontsize=8.8,color='#66746d')

fig.text(.562,.568,'B  /  MAYOR’S PEDESTRIAN AND SERVICE ACCESS',fontsize=13,weight='bold',color=INK)
b=fig.add_axes([.56,.306,.41,.247]);base(b,[-60,91,38,176],'mayor',True)
label(b,'mayor_mansion',(32,165),"Mayor's Mansion\nGrounds +44.2 m",9.5,ha='right')
label(b,'mayor_stairs',(30,113),'Formal staircase\n5 flights · 4 landings',9.5,ha='right')
label(b,'mayor_cart',(-58,154),'Cart / horse route',9,ha='left')
plain(b,-15,136,'Courtyard',9);plain(b,-36,111,'Village road\nconnection',8)
plain(b,-4,95,'Stair base +31.5 m',8,ha='left')
plain(b,-38,135,'Service access',8,ha='right')
scalebar(b,-54,95,20)
fig.text(.562,.29,'12.7 m stair rise. Property walls and service opening are projected from the existing meshes.',fontsize=8.8,color='#66746d')

fig.text(.562,.26,'C  /  FAMILY HOME AND CELLAR',fontsize=12,weight='bold',color=INK)
c=fig.add_axes([.56,.071,.215,.175]);base(c,[-28,-24,4,12],'witch',True)
label(c,'witch_house',(2,6),"Witch's House",8.5,ha='right')
label(c,'cellar_entrance',(-26,-20),'Cellar Entrance',8,ha='left')
plain(c,-6,9,'Family home +0 m',7)
scalebar(c,-5,-22,5)
fig.text(.561,.05,'Dashed outline = cellar below the house (floor −4.4 m).',fontsize=8.2,color='#66746d')

legend=fig.add_axes([.795,.057,.19,.191]);legend.axis('off')
legend.text(0,1,'LEGEND',fontsize=12,weight='bold',color=INK,va='top')
rows=[('Buildings / landmark buildings',BUILD,'#9b7659'),('Outbuildings / work proxies','#a0a6a6','#b7b3a7'),('Roads / narrow worn paths',ROAD,'#e9d4ab'),('Fields / pasture / orchard','#e5ddb9','#d0ddbb'),('Forest canopy proxies','#cfdbc8','#99ac8e'),('Existing cemetery / burial reserve','#ded3e2','#f1eaf3'),('Walls, fences and retaining edges','#8b8572','#c5beb1')]
for i,(name,c1,c2) in enumerate(rows):
    y=.86-i*.101
    legend.add_patch(Rectangle((0,y-.018),.05,.045,facecolor=c1,edgecolor='#73796d',lw=.35,transform=legend.transAxes))
    legend.add_patch(Rectangle((.06,y-.018),.05,.045,facecolor=c2,edgecolor='#73796d',lw=.35,transform=legend.transAxes))
    legend.text(.14,y+.002,name,fontsize=8.2,va='center',color=INK)
legend.text(0,.06,'Contours: 5 m intervals in UE Z.\n*N is a map convention, not geographic north.\nScale bars show horizontal distance.',fontsize=8.3,color='#66746d',va='top',linespacing=1.5)
fig.text(.036,.025,'READING LIMITS  ·  Roof / canopy footprints overlap ground below. Fences and narrow props are slightly emphasized. Terrain height is flattened into contours.',fontsize=9,color='#66746d')
fig.text(.966,.025,'GEOMETRY '+D['geometry_sha256'][:12]+'  ·  EMPTY EVENT LAYERS',ha='right',fontsize=9,color='#66746d')

INKNS='http://www.inkscape.org/namespaces/inkscape'
SVGNS='http://www.w3.org/2000/svg'
def svg_layers(path):
    root=ET.parse(path).getroot();ns='http://www.inkscape.org/namespaces/inkscape';sod='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'
    for g in root.findall('{'+SVGNS+'}g'):
        if g.get('id')=='figure_1':g.set('{'+ns+'}groupmode','layer');g.set('{'+ns+'}label','Existing village base geometry');g.set('id','existing_village_base')
    for name in ['Blood route','Bone route','Witch route','Civilian movement','Escape attempts','Blood barrier','Event nodes','Attack directions','Structural damage','Chronology']:
        g=ET.SubElement(root,'{'+SVGNS+'}g',{'id':'event_'+name.lower().replace(' ','_'),'{'+ns+'}groupmode':'layer','{'+ns+'}label':name+' (empty)'})
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
shared_palette=None
for name,text in [('01_village_base_map','VILLAGE BASE MAP'),('02_massacre_planning_blank','VILLAGE MASSACRE PLANNING MAP')]:
    title.set_text(text)
    fig.savefig(OUT/(name+'.png'),dpi=250,facecolor=BG)
    rgb=Image.open(OUT/(name+'.png')).convert('RGB')
    if shared_palette is None:shared_palette=rgb.quantize(colors=256,dither=Image.Dither.NONE)
    indexed=rgb.quantize(palette=shared_palette,dither=Image.Dither.NONE)
    indexed.save(OUT/(name+'.png'),optimize=True)
    fig.savefig(OUT/(name+'.svg'),facecolor=BG,metadata={'Title':text,'Description':'Derived from existing UE geometry; all event layers are empty.'})
    svg_layers(OUT/(name+'.svg'))
    print('Rendered',name,flush=True)
plt.close(fig)
# Coordinate transforms make later annotations convertible back to UE locations.
views={}
for name,axis in [('overview',ax),('cemetery',a),('mayor',b),('witch',c)]:
    p=axis.get_position();xmin,xmax=axis.get_xlim();ymin,ymax=axis.get_ylim()
    views[name]=dict(world_extent_m=[xmin,ymin,xmax,ymax],png_frame_px=[p.x0*6000,(1-p.y1)*5000,p.width*6000,p.height*5000],svg_frame_units=[p.x0*1728,(1-p.y1)*1440,p.width*1728,p.height*1440])
(OUT/'map_views.json').write_text(json.dumps(dict(png_size=[6000,5000],svg_viewbox=[0,0,1728,1440],coordinate_system=D['coordinate_system'],views=views),indent=2))
# The title is the only raster difference. The entire geometry/legend area must match.
im1=Image.open(OUT/'01_village_base_map.png').convert('RGB');im2=Image.open(OUT/'02_massacre_planning_blank.png').convert('RGB')
assert im1.size==im2.size
assert np.array_equal(np.asarray(im1)[400:],np.asarray(im2)[400:]),'Base/planning geometry diverged'
im1.thumbnail((1800,1500));im1.save(HERE/'preview.png')
print('Base/planning geometry raster identity verified; image size',im2.size)
