"""Offline renderer of the CLOSED V2 review. No simulation or Unreal calls.
Run beside v2_simulation.json; map_data.json is in the parent directory.
python render_v2.py [output-directory] [map-data-path]
"""
import json, sys, math, textwrap, re
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch, Circle, Rectangle
from matplotlib.collections import PatchCollection, LineCollection
from shapely.geometry import shape, Point, LineString, box
from shapely.ops import substring, unary_union
from PIL import Image
HERE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else HERE
MAP=Path(sys.argv[2]) if len(sys.argv)>2 else OUT.parent/'map_data.json'
S=json.loads((OUT/'v2_simulation.json').read_text());D=json.loads(MAP.read_text());H=json.loads((OUT/'v2_handoff_90.json').read_text())
E=S['events'];PEOPLE=S['people'];FINAL=S['final_state'];ARR=S['witch_route']['arrival'];END=S['terminal']
GEOM={f['id']:shape(f['geometry']) for f in D['features']}; LM={x['id']:x for x in D['landmarks']}
BG='#f6f5ef';INK='#25343b';BLOOD='#b04446';BONE='#5764b0';WITCH='#91499c';CIV='#20818a';BARRIER='#96584e';GREEN='#357459'
COL={'Blood':BLOOD,'Bone':BONE,'Witch':WITCH,'Barrier':BARRIER,'Civilian':CIV}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':INK,'text.color':INK,'axes.titleweight':'bold'})
STY={'forest':('#dce4d6','#cbd5c4',.25),'agriculture':('#e9dfbc','#cec49d',.5),'estate_area':('#eae4d9','none',0),'civic_area':('#eae2cf','none',0),'cemetery_area':('#dfd5e5','none',0),'burial_reserve':('#eee5ef','#c1a9c2',.5),'road':('#fffdf0','#c0b69e',.55),'footpath':('#e5cfa9','#c5b38e',.3),'boundary':('#998f7d','#998f7d',.3),'retaining':('#c7bdae','#a59e8f',.3),'stairs':('#dfdbd3','#969189',.4),'gate':('#6c7981','#58636d',.5),'outbuilding':('#b3b8b5','#818984',.4),'building':('#7d8b90','#455760',.65),'grave':('#9d8aa3','#7d6a83',.4),'grave_open':('#c6b18f','#8c7759',.5),'cellar_access':('#c5ae82','#877553',.4),'orchard_trees':('#aebe9f','none',0)}

def polygon_parts(g):
    if g.geom_type=='Polygon':yield g
    elif hasattr(g,'geoms'):
        for q in g.geoms:yield from polygon_parts(q)

def base(ax,extent,minor=True):
    reg=box(*extent);by=defaultdict(list)
    for f in D['features']:
        c=f['category'];g=GEOM[f['id']]
        if c not in STY or not g.intersects(reg):continue
        for q in polygon_parts(g.intersection(reg)):
            by[c].append(Patch(np.asarray(q.exterior.coords),closed=True))
    for z,(c,st) in enumerate(STY.items()):
        if by[c]:ax.add_collection(PatchCollection(by[c],facecolor=st[0],edgecolor=st[1],linewidth=st[2],zorder=z+1))
    ax.set(xlim=(extent[0],extent[2]),ylim=(extent[1],extent[3]),aspect='equal',facecolor=BG)
    ax.tick_params(labelsize=8,length=0);ax.grid(alpha=.1,color='#6e8176');ax.set_xlabel('Map east / UE +Y (m)',fontsize=9);ax.set_ylabel('Map north / UE +X (m)',fontsize=9)
    x=extent[0]+(extent[2]-extent[0])*.075;y=extent[3]-(extent[3]-extent[1])*.15
    ax.annotate('N*',xy=(x,y+12),xytext=(x,y),ha='center',fontsize=10,weight='bold',arrowprops={'arrowstyle':'-|>','color':INK},zorder=80)
    n=25 if extent[2]-extent[0]>100 else 10; yy=extent[1]+(extent[3]-extent[1])*.05
    ax.plot([x,x+n],[yy,yy],color=INK,lw=2,zorder=90);ax.text(x+n/2,yy+2,f'{n} m',ha='center',fontsize=8,zorder=90,bbox={'fc':BG,'ec':'none','pad':1})

def rim(ax):
    g=shape(H['barrier']);a=np.array(g.exterior.coords);ax.plot(a[:,0],a[:,1],color=BARRIER,lw=1.8,ls=(0,(5,3)),zorder=35)

def label(ax,p,text,offset=(8,6),color=INK,size=9):
    return ax.annotate(text,xy=p[:2],xytext=offset,textcoords='offset points',fontsize=size,color=color,zorder=90,bbox={'fc':BG,'ec':'none','pad':1.5,'alpha':.95},arrowprops={'arrowstyle':'-','color':color,'lw':.6})

def landmark(ax,key,offset=(8,6),short=None):
    if key in LM:label(ax,LM[key]['xy'],short or LM[key]['label'],offset,size=9)

def line(ax,path,color,lw=1.8,alpha=.8,ls='-',arrow=False):
    a=np.array(path)
    if len(a)<2:return
    ax.plot(a[:,0],a[:,1],color=color,lw=lw,alpha=alpha,ls=ls,zorder=42)
    if arrow and np.linalg.norm(a[-1,:2]-a[-2,:2])>.15:ax.annotate('',xy=a[-1,:2],xytext=a[max(0,len(a)-3),:2],arrowprops={'arrowstyle':'->','color':color,'lw':lw},zorder=43)

def eventpoint(ev):
    if ev['actor']=='Blood' and ev.get('fatalities'):
        return np.mean([PEOPLE[p]['fatality']['xy'] for p in ev['fatalities']],axis=0)
    return ev['xy']

def mark(ax,p,txt,color,sz=110):
    cache=getattr(ax,'_v2_marks',[])
    for q,t in cache:
        if txt and math.dist(p[:2],q[:2])<2.0:
            t.set_text(t.get_text()+'/'+txt)
            if len(t.get_text())>4:
                t.set_position((q[0]+3,q[1]+3));t.set_color(color);t.set_bbox({'fc':BG,'ec':'none','pad':1});t.set_ha('left')
            return
    ax.scatter(*p[:2],s=sz,c=color,edgecolors=BG,linewidths=.8,zorder=70)
    if txt:
        t=ax.text(*p[:2],txt,ha='center',va='center',fontsize=8,color='white',weight='bold',zorder=71);cache.append((list(p),t));ax._v2_marks=cache

def footprint(ax,ev,alpha=.13):
    for q in polygon_parts(shape(ev['footprint'])):ax.add_patch(Patch(np.array(q.exterior.coords),fc=BLOOD,ec=BLOOD,lw=.5,alpha=alpha,zorder=37))

def witchpos(t):
    for seg in S['witch_route']['segments']:
        if t<=seg['end']:
            f=max(0,min(1,(t-seg['start'])/(seg['end']-seg['start'])));return (np.array(seg['a'])+(np.array(seg['b'])-seg['a'])*f).tolist()
    return S['witch_route']['segments'][-1]['b']

def witchline(ax):
    a=[r['a'] for r in S['witch_route']['segments']]+[S['witch_route']['segments'][-1]['b']];line(ax,a,WITCH,2.8)

def actorpaths(ax,actor):
    for m in S['actor_movements']:
        if m['actor']==actor:line(ax,m['path'],COL[actor],1.6 if actor=='Blood' else 1.15,.8 if actor=='Blood' else .55,ls='-' if actor=='Blood' else (0,(2,3)),arrow=True)

def executed(m):
    l=LineString(m['path']);g=substring(l,0,min(l.length,m['executed_length_m']));return list(g.coords) if hasattr(g,'coords') else []

def sheet(title,subtitle,extent=(-87,-25,86,170),full=False):
    fig=plt.figure(figsize=(20,14),facecolor=BG)
    fig.text(.04,.948,title,fontsize=25,weight='bold');fig.text(.04,.915,subtitle,fontsize=11,color='#62736e')
    ax=fig.add_axes([.045,.11,.53,.765]);base(ax,extent);rim(ax)
    fig.text(.04,.05,'V2 / independent branch from approved +90  •  112 fatalities / 58 survivors  •  near-total premise FAILED',fontsize=11,weight='bold')
    fig.text(.04,.026,'N* = uphill / UE +X, not a surveyed compass bearing. Existing metric 2D geometry. Planning only; no UE edits or final assets.',fontsize=9,color='#62736e')
    return fig,ax

def notes(fig,heading,items,top=.855,x=.615,width=61,step=.038,fontsize=11):
    fig.text(x,top,heading,fontsize=15,weight='bold');y=top-.04
    for item in items:
        parts=textwrap.wrap(item,width,break_long_words=False,break_on_hyphens=False)
        fig.text(x,y,'\n'.join(parts),fontsize=fontsize,va='top',linespacing=1.45)
        y-=step*len(parts)+.017
    return y

def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=180,facecolor=BG)
    fig.savefig(OUT/(name+'.svg'),facecolor=BG)
    im=Image.open(OUT/(name+'.png')).convert('RGB');im.quantize(colors=256,dither=Image.Dither.NONE).save(OUT/(name+'.png'),optimize=True)
    svg=OUT/(name+'.svg');svg.write_text(re.sub(r'(-?\d+\.\d{3})\d+',r'\1',svg.read_text(encoding='utf-8')),encoding='utf-8')
    plt.close(fig);print(name,flush=True)

def context(fig,at=(.67,.46,.25,.28)):
    a=fig.add_axes(at);base(a,(-108,-166,108,184));rim(a);a.set_title('Unchanged clearing / approach',fontsize=10);return a

# 01 Chronology: whole clearing, readable selected incident index.
fig,ax=sheet('01 / FULL CHRONOLOGICAL MAP','T+90 → T+373.923  |  New V2 events only; seven opening deaths preserved',(-110,-168,110,187))
actorpaths(ax,'Blood');actorpaths(ax,'Bone');witchline(ax)
chosen=['V2E005','V2E007','V2E011','V2E012','V2E013','V2E016','V2E018','V2E029','V2E031','V2E045','V2E051','V2E058','V2E060','V2E062','V2E063']
indexed=[e for e in E if e['id'] in chosen];texts=[]
for i,e in enumerate(indexed,1):
    p=eventpoint(e);mark(ax,p,str(i),COL[e['actor']],100)
    texts.append(f'{i:02}  +{e["time"]:.1f}  {e["kind"]}'+(f' · {len(e["fatalities"])} dead' if e['fatalities'] else ''))
notes(fig,'SELECTED MILESTONES',texts,step=.023,fontsize=10)
fig.text(.615,.185,'Red: Blood path  /  blue dashes: Bone bursts\nPurple: Witch destination walk  /  brown: barrier\nFull 63-event ledger and 157 cycles in the notes.',fontsize=10,linespacing=1.6)
landmark(ax,'village_gate',(-66,-8));landmark(ax,'church',(10,0));landmark(ax,'mayor_mansion',(10,16))
save(fig,'01_v2_full_chronology')

# 02 Blood: wave envelopes and numbered targets, no invented travel.
strikes=[e for e in E if e['kind']=='blood strike']
fig,ax=sheet('02 / BLOOD INCIDENTS & MOVEMENT','Slow concentration choices; local living-blood signals, not hidden headcount knowledge')
actorpaths(ax,'Blood')
for i,e in enumerate(strikes,1):footprint(ax,e,.095);mark(ax,eventpoint(e),str(i),BLOOD,92)
notes(fig,'EXECUTED PRESSURE SURGES',[f'{i:02}  +{e["time"]:.1f}  {len(e["fatalities"])} fatalities · {e["power"]["range_m"]:.1f} m reach' for i,e in enumerate(strikes,1)],step=.0165,fontsize=10)
fig.text(.615,.13,'Envelopes = provisional force exposure, not final debris.\nNormal movement remains 1.5 m/s throughout.',fontsize=10)
landmark(ax,'tavern',(16,-16));landmark(ax,'church',(15,10));landmark(ax,'blacksmith',(-76,-15));save(fig,'02_v2_blood_incidents')

# 03 Resource growth with map and source reuse, labels are developer-only.
fig,ax=sheet('03 / BLOOD RESOURCE & POWER GROWTH','Accessible blood drives gradual growth; emotional amplification begins only at Mayor arrival')
actorpaths(ax,'Blood')
for i,e in enumerate(strikes):
    ax.scatter(*e['xy'],s=20+e['power']['accessible_units']*1.4,c=BLOOD,alpha=.18,zorder=45)
for r in S['resource_draws'][::9]:line(ax,[r['from'],r['to']],BLOOD,.55,.25)
for tm in [90,125,167,258.538,343.04]:
    p=min(S['power_history'],key=lambda q:abs(q['time']-tm));label(ax,p['xy'],f'+{tm:g}  {p["state"]}',(-110,18) if tm==90 else (14,18 if tm in [167,343.04] else -20),BLOOD)
t=np.array([p['time'] for p in S['power_history']]);pw=S['power_history']
for rect,keys,ylabel in [([.615,.58,.34,.26],['accessible_units','carried_units'],'Blood proxy units (not litres)'),([.615,.22,.34,.25],['sense_m','range_m','width_m'],'Local range / metres')]:
    a=fig.add_axes(rect,facecolor=BG)
    for k in keys:a.plot(t,[p[k] for p in pw],lw=2,label=k.replace('_units','').replace('_m','').replace('_',' '))
    a.axvspan(ARR,END,color=WITCH,alpha=.08);a.axvline(ARR,color=WITCH,lw=1,ls='--');a.set_xlabel('Seconds since release');a.set_ylabel(ylabel);a.grid(alpha=.18);a.legend(fontsize=9,loc='upper left')
fig.text(.615,.105,'Shaded final minute: ×1 → ×1.22, capped locally.\nFinite source/carry ledger conserves 112 generated units.\nInitial +90: 6.416 accessible units, already FED.',fontsize=10,linespacing=1.5)
save(fig,'03_v2_blood_power_growth')

# 04 Bone incident pattern; no continuous coverage line.
fig,ax=sheet('04 / BONE ATTENTION PATTERN','Short bursts, returns, observation and deliberate restraint; no systematic clearing route')
actorpaths(ax,'Bone');be=[e for e in E if e['actor']=='Bone']
for i,e in enumerate(be,1):mark(ax,e['xy'],str(i),BONE,105)
notes(fig,'INCIDENTS / NOT A CLEARANCE ITINERARY',[f'{i:02} +{e["time"]:.1f} — {e["kind"]}' for i,e in enumerate(be,1)],step=.021,fontsize=10)
fig.text(.615,.19,'Post-guard intervals include listening, impact-noise\ninvestigation and idle vantage time. No inferred kills.\n3 preserved opening deaths + 2 V2 deaths = 5.',fontsize=10,linespacing=1.6)
mark(ax,FINAL['actors']['Bone']['xy'],'',BONE,140);label(ax,FINAL['actors']['Bone']['xy'],'Terminal listening position',(20,-24),BONE)
save(fig,'04_v2_bone_pattern')

# 05 Dedicated guard sequence.
fig,ax=sheet('05 / BONE & THE SON-KILLER GUARD','Recognition +165.947 → precise final strike +213.947  |  48 seconds',(-19,66,43,147))
guard=next(p for p in PEOPLE.values() if p['role']=='entrance guard');gid=guard['group']
for m in S['civilian_movements']:
    if m['group']==gid:line(ax,executed(m),CIV,2.1,.9,arrow=True)
for m in S['actor_movements']:
    if m['actor']=='Bone' and 158<m['start']<214:line(ax,m['path'],BONE,1.7,.8,ls='--',arrow=True)
ge=[e for e in be if 'guard' in e['kind'] or 'recognition' in e['kind']]
for i,e in enumerate(ge,1):mark(ax,e['xy'],str(i),BONE,135)
notes(fig,'A PERSONAL INTERRUPTION',[
 '1  +165.947: locally visible entrance guard is recognized. No remote identity knowledge.',
 '2–5: chosen object hits and permitted retreats. Fear and protective retreat keep Bone interested.',
 '6  +213.947: one deliberate, precise final hit. The guard is not killed by an accidental near-miss.',
 'Turquoise: guard movement from ordinary duty into the local emergency, then retreat. Blue: Bone’s separate bursts.',
 'Dialogue opportunities only: fractured recognition, confused child/Witch identity, scraps of the arrest memory. No finished lines or further family history.',
 'Other guards receive no inherited guilt. Both survive this branch.'
],step=.027,fontsize=11)
landmark(ax,'mayor_stairs',(15,5));landmark(ax,'church',(15,5));save(fig,'05_v2_bone_guard_sequence')

# 06 Witch exact preserved route and altitude.
fig,ax=sheet('06 / WITCH DESTINATION ROUTE','Continuous uphill walk; she does not hunt, help, dodge or count survivors')
witchline(ax)
for tm,off in [(90,(-95,-10)),(150,(12,-12)),(210,(-85,12)),(258.2449,(-115,-8)),(ARR,(15,8))]:
    p=witchpos(tm);mark(ax,p,'',WITCH,100);label(ax,p,f'+{tm:.1f}',off,WITCH)
for e in E:
    if e['kind']=='Witch ignored appeal':ax.scatter(*e['xy'],marker='*',s=160,c=CIV,zorder=70)
segments=S['witch_route']['segments'];tt=[90]+[r['end'] for r in segments];zz=[segments[0]['a'][2]]+[r['b'][2] for r in segments]
a=fig.add_axes([.615,.57,.34,.25],facecolor=BG);a.plot(tt,zz,c=WITCH,lw=2);a.set(xlabel='Seconds since release',ylabel='Survey elevation / m');a.grid(alpha=.15)
notes(fig,'PHYSICAL TIMING',[
 f'{sum(r["distance_3d_m"] for r in segments):.2f} m remaining 3D route after +90; main street, formal stairs, courtyard, minimal interior approach.',
 f'1.1 m/s ordinary walk; 0.85 m/s on stairs. Arrival +{ARR:.3f}, recalculated independently.',
 f'{sum(e["kind"]=="Witch ignored appeal" for e in E)} nearby appeals receive no help or explanation. Stars mark these encounters.',
 'No executed Blood envelope crosses her position. The immunity rule is retained without forcing a spectacle.'
],top=.48,step=.026,fontsize=10)
save(fig,'06_v2_witch_route')

# 07 Confrontation exact minute; topics remain unauthored.
fig,ax=sheet('07 / ARRIVAL & THE FINAL MINUTE','The Mayor is restrained on arrival; death follows a fixed 60 seconds, never a survivor census',(-54,77,51,166))
witchline(ax);mark(ax,[2,146],'M',WITCH,220);landmark(ax,'mayor_cart',(-85,0));landmark(ax,'mayor_stairs',(-100,-8))
a=fig.add_axes([.615,.65,.34,.16],facecolor=BG);a.set(xlim=(ARR-4,END+4),ylim=(0,1),yticks=[]);a.axvspan(ARR,END,color=WITCH,alpha=.12);a.plot([ARR,END],[.5,.5],c=WITCH,lw=3)
for t0,txt,yy in [(ARR,'Secure Mayor',.82),(343.039881,'Church wave',.16),(368.076261,'Eastern wave',.8),(END,'Final death',.16)]:
    a.plot([t0,t0],[.35,.65],c=WITCH);a.annotate(txt,xy=(t0,.5),xytext=(t0,yy),fontsize=9,ha='center')
a.set_xlabel('Canonical seconds / release = 0')
notes(fig,'TOPICS & EMOTIONAL BEATS — NO SCRIPT',[
 'Opening: establish responsibility and deny escape. Method of restraint remains reserved.',
 'Middle: blame, the loss of lover/son, deliberate helplessness. Pauses allow the Mayor to hear the village. No new arrest details are defined.',
 'End: rage remains dominant; this is not the later remorseful spirit. She kills him at +373.923.',
 '77 alive at arrival → 58 at terminal. The interval contains 18 Blood deaths and the Mayor; those counts never inform the Witch.',
 'Rage amplification raises local pressure/range. A frozen-state diagnostic finds both final strikes already fatal at these same positions without it; do not claim it alone caused 18 deaths.'
],top=.555,step=.025,fontsize=10)
save(fig,'07_v2_mayor_final_minute')

# 08 Actual civilian movement, intended unexecuted tails excluded.
fig,ax=sheet('08 / CIVILIAN MOVEMENT','Executed paths only; group intentions are recorded separately from outcomes',(-108,-166,108,184))
for m in S['civilian_movements']:line(ax,executed(m),CIV,.8,.36,arrow=False)
for i,(place,n) in enumerate(FINAL['survivor_locations'].items(),1):
    q=list(GEOM[place].centroid.coords[0]);mark(ax,q,str(i),GREEN,95+n*5)
notes(fig,'MOVEMENT THAT THE MASSACRE INTERRUPTS',[
 'Agricultural households return from fields or retreat after their own barrier discovery. They do not inherit perimeter knowledge from the opposite edge.',
 'Village people seek familiar homes, larger refuges, family and authority. Helpers and callers are exposed according to their current positions.',
 'Foresters move in from the western edge. Some later join the failed western refuge.',
 'The entrance guard descends to investigate/help, then retreats under Bone’s personal attention. Estate service people remain above.',
 '78 movement records; planned tails stop at a new decision, the last traveller’s death, arrival or the terminal frame.',
 'Green numbered circles identify final survivor pockets, not magically safe destinations.'
],step=.03,fontsize=11)
save(fig,'08_v2_civilian_movement')

# 09 Boundary local discoveries and warning links.
fig,ax=sheet('09 / BARRIER CONTACT & LOCAL KNOWLEDGE','B3/B4 start at zero; discovery belongs to witnesses and later warning recipients',(-110,-166,110,187))
bar=[e for e in E if e['actor']=='Barrier']
for i,e in enumerate(bar,1):
    mark(ax,e['xy'],str(i),BARRIER,150)
    for m in S['civilian_movements']:
        if any(p in m['members'] for p in e['fatalities']):line(ax,executed(m),CIV,1.5,.8)
    for gid in e.get('witnesses',[]):
        snaps=[p for p in S['snapshots'] if p['time']<=e['time']+.01]
        if snaps and gid in snaps[-1]['groups']:line(ax,[e['xy'],snaps[-1]['groups'][gid]['xy']],BARRIER,1,.5,ls=':')
notes(fig,'FIVE INDEPENDENT CONTACTS',[
 *[f'{i}  +{e["time"]:.3f} · one fatality at ({e["xy"][0]:.1f}, {e["xy"][1]:.1f}) m.' for i,e in enumerate(bar,1)],
 'B0 unidentified; B1 observed; B2 suspected confinement; B3 failed crossing witnessed; B4 reactive strike witnessed.',
 'Dotted links: direct local event recipients, not village-wide broadcasts. Warning recipients retain “reported danger” provenance rather than falsely becoming direct B4 witnesses.',
 'The bell only signals public emergency. It provides no barrier instruction or safe route.'
],step=.026,fontsize=11)
save(fig,'09_v2_barrier_knowledge')

# 10 Population curve and casualty locations.
fig,ax=sheet('10 / CASUALTY PROGRESSION','Individual causal ledger; no target death rate, no deaths after the Mayor',(-105,-163,105,180))
for p in PEOPLE.values():
    if p['fatality']:
        f=p['fatality'];ax.scatter(*f['xy'],s=22,c=COL.get(f['actor'],BARRIER),alpha=.6,zorder=45)
ts=[0];alive=[170];dead=[0]
counts=Counter(round(p['fatality']['time'],6) for p in PEOPLE.values() if p['fatality'])
for t0,n in sorted(counts.items()):ts.append(t0);dead.append(dead[-1]+n);alive.append(170-dead[-1])
a=fig.add_axes([.615,.54,.34,.3],facecolor=BG);a.step(ts,dead,where='post',color=BLOOD,label='fatalities',lw=2);a.step(ts,alive,where='post',color=GREEN,label='alive',lw=2);a.axvline(90,color=INK,ls=':');a.axvspan(ARR,END,color=WITCH,alpha=.1);a.set(xlim=(0,385),ylim=(0,175),xlabel='Seconds since release',ylabel='People');a.legend();a.grid(alpha=.15)
notes(fig,'RECONCILED CENSUS',[
 'T+90: 7 dead / 163 alive / 4 injured. All preserved opening IDs remain unchanged.',
 f'Arrival +{ARR:.3f}: 93 dead / 77 alive.',
 f'Terminal +{END:.3f}: 112 dead / 58 alive / 0 injured survivors.',
 'Causes, including preserved opening: Blood 101; Bone 5; barrier 5; Witch 1.',
 '65.9% fatalities is a severe massacre, but not the requested near-total annihilation. The branch fails that narrative premise.'
],top=.445,step=.026,fontsize=11)
save(fig,'10_v2_casualty_progression')

# 11 Final pockets and terminal actors.
fig,ax=sheet('11 / FINAL AFTERMATH PLANNING STATE','T+373.923  |  Mayor is last death; all 58 surviving people remain explicitly counted',(-105,-112,105,181))
for e in strikes:footprint(ax,e,.055)
pocketitems=[]
for i,(place,n) in enumerate(FINAL['survivor_locations'].items(),1):
    q=list(GEOM[place].centroid.coords[0]);mark(ax,q,str(i),GREEN,200);pocketitems.append(f'{i}  {place.replace("_"," ")} — {n} alive')
notes(fig,'EIGHT SURVIVING POCKETS',pocketitems,step=.027,fontsize=11)
notes(fig,'WHY THIS IS ANOTHER RULE / PREMISE FAILURE',[
 'Lower farms remain outside the chosen incidents. Several homes are bypassed; Blood’s local sensing is not a village-wide sweep.',
 'Bone remains attention-driven and spends time tormenting the guard or investigating noise. Witch never hunts the estate staff.',
 'These are provisional failed-branch survivors, not locked new lore. No post-Mayor cleanup is allowed.'
],top=.415,step=.026,fontsize=10)
for actor,off in [('Blood',(12,16)),('Bone',(12,-15)),('Witch',(12,14))]:
    q=FINAL['actors'][actor]['xy'];ax.scatter(*q,s=160,marker='*',c=COL[actor],zorder=75);label(ax,q,actor+' / stop',off,COL[actor])
label(ax,[2,146],'8 / estate survivors',(-120,-22),GREEN)
save(fig,'11_v2_final_aftermath')

# 12 Environmental causality seeds, not detailed destruction.
fig,ax=sheet('12 / ENVIRONMENTAL STORY SEEDS','Each seed links an ordinary intention to an executed incident; no final corpse or asset placement',(-105,-162,105,182))
seeds=[('V2E003','Deliberately struck coop board: M05 was seeking protection.'),('V2E010','Aid interrupted: injured opening victims and helpers.'),('V2E018','Tavern refuge / activity interrupted by a sensed concentration.'),('V2E013','Farm escape test: local boundary contact, then warning/retreat.'),('V2E045','Guard retreat and chosen object strikes preserve personal recognition.'),('V2E051','Western shelter: people arriving from separate intentions gather.'),('V2E058','Mayor secured; village sound continues during helpless waiting.'),('V2E060','Church refuge: bell and grouped shelter become vulnerable.'),('V2E062','Eastern household: late pressure corridor through the occupied bay.')]
txt=[]
for i,(eid,caption) in enumerate(seeds,1):
    ev=next(x for x in E if x['id']==eid);mark(ax,eventpoint(ev),str(i),COL[ev['actor']],125);txt.append(f'{i}  +{ev["time"]:.1f}  {caption}')
notes(fig,'PRODUCTION OPPORTUNITIES / CAUSE FIRST',txt,step=.0225,fontsize=10)
fig.text(.615,.13,'Preserve object IDs and before-activity in the JSON.\nOld asset names such as CrushedHome are identifiers,\nnot proof of pre-existing massacre destruction.',fontsize=10,linespacing=1.4)
save(fig,'12_v2_story_seeds')
