"""Read-only navigation/projection helpers using the isolated approved survey."""
import json, math, heapq
from pathlib import Path
import numpy as np
from shapely.geometry import shape, Point, LineString, Polygon
from shapely.ops import unary_union, nearest_points, substring
from shapely import make_valid
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/'inputs/map_data.json').read_text())
F={f['id']:f for f in D['features']}; GEOM={k:make_valid(shape(f['geometry'])) for k,f in F.items()}
H=json.loads((HERE/'package/v2_handoff_90.json').read_text())
ROOFS={k:GEOM[k] for k,f in F.items() if f['category'] in ['building','outbuilding']}
OB=unary_union(list(ROOFS.values())).buffer(.22,join_style=2)
RIM=shape(H['barrier']); DOORS=H['doors']
def xy(p):return [float(p[0]),float(p[1])]
def dist(a,b):return math.dist(a[:2],b[:2])
def centre(k):return list(GEOM[k].centroid.coords[0])
def clear(a,b):
    l=LineString([a,b]);return not l.intersects(OB) and RIM.buffer(.02).covers(l)
def sight(a,b,ignore=()):
    l=LineString([a,b]);return not any(l.intersection(g).length>.3 for k,g in ROOFS.items() if k not in ignore)
def exit_point(p,building=None):
    if building:return DOORS[building]
    q=Point(p)
    if not OB.covers(q):return xy(p)
    # Roof overlap at an approved outdoor work/yard anchor is a documented
    # under-eave transition, not an instantaneous moved starting position.
    b=nearest_points(q,OB.boundary)[1];v=np.array([b.x-q.x,b.y-q.y]);v/=max(np.linalg.norm(v),1e-6)
    return [b.x+v[0]*.08,b.y+v[1]*.08]

cache=HERE/'navigation_v2.json'
if cache.exists():
    nav=json.loads(cache.read_text());N=np.array(nav['nodes']);ADJ={int(k):v for k,v in nav['adj'].items()}
else:
    nodes=[]
    for g in (OB.buffer(.08,join_style=2).geoms if hasattr(OB,'geoms') else [OB.buffer(.08,join_style=2)]):
        if g.geom_type=='Polygon':nodes.extend([list(q) for q in g.exterior.coords[:-1]])
    for k,f in F.items():
        if f['category'] in ['route_reference','footpath_reference']:
            g=GEOM[k]
            for ds in np.arange(0,g.length+1,5):nodes.append(list(g.interpolate(ds).coords[0]))
    # Sparse existing clearing navigation samples support cross-yard paths.
    for x in np.arange(-90,91,8):
        for y in np.arange(-166,179,8):
            p=Point(x,y)
            if RIM.contains(p) and not OB.covers(p):nodes.append([float(x),float(y)])
    nodes+=list(DOORS.values());nodes=[p for p in nodes if not OB.covers(Point(p)) and RIM.covers(Point(p))]
    N=np.array(list(dict.fromkeys((round(p[0],4),round(p[1],4)) for p in nodes)))
    ADJ={i:[] for i in range(len(N))}
    for i,a in enumerate(N):
        near=np.where(np.linalg.norm(N-a,axis=1)<15)[0]
        for j in near:
            if j<=i or not clear(a,N[j]):continue
            w=dist(a,N[j]);ADJ[i].append([int(j),w]);ADJ[int(j)].append([i,w])
    cache.write_text(json.dumps({'nodes':N.tolist(),'adj':ADJ},separators=(',',':')))

def outdoor_path(a,b):
    a=exit_point(a);b=exit_point(b)
    if dist(a,b)<.01:return [a,b]
    if clear(a,b):return [a,b]
    def links(p):
        idx=np.argsort(np.linalg.norm(N-np.array(p),axis=1))[:40]
        return [(int(i),dist(p,N[i])) for i in idx if clear(p,N[i])]
    starts=links(a);ends=dict(links(b));q=[];best={};prev={}
    for i,w in starts:heapq.heappush(q,(w,i));best[i]=w;prev[i]=None
    winner=None;total=1e20
    while q:
        cost,i=heapq.heappop(q)
        if cost>best.get(i,1e20):continue
        if cost>total:break
        if i in ends and cost+ends[i]<total:total=cost+ends[i];winner=i
        for j,w in ADJ[i]:
            nc=cost+w
            if nc<best.get(j,1e20):best[j]=nc;prev[j]=i;heapq.heappush(q,(nc,j))
    if winner is None:raise RuntimeError(f'No existing-clearance path {a} -> {b}')
    seq=[];i=winner
    while i is not None:seq.append(N[i].tolist());i=prev[i]
    return [a]+seq[::-1]+[b]

def path(a,b,inside_a=None,inside_b=None):
    sa=exit_point(a,inside_a);sb=exit_point(b,inside_b)
    pts=[xy(a)]
    if dist(a,sa)>.01:pts.append(xy(sa))
    pts+=outdoor_path(sa,sb)[1:]
    if dist(b,sb)>.01:pts.append(xy(b))
    out=[pts[0]]
    for p in pts[1:]:
        if dist(out[-1],p)>.001:out.append(p)
    return out if len(out)>1 else [out[0],out[0]]

def length(pts):return sum(dist(a,b) for a,b in zip(pts,pts[1:]))
def along(pts,ds):return list(LineString(pts).interpolate(max(0,min(ds,length(pts)))).coords[0])
def nearest_rim(p,direction=None):
    if direction is None:return list(nearest_points(Point(p),RIM.exterior)[1].coords[0])
    v=np.array(direction,dtype=float);v/=np.linalg.norm(v);g=LineString([p,(np.array(p)+v*600).tolist()]).intersection(RIM.boundary)
    pp=list(g.geoms) if hasattr(g,'geoms') else [g]
    points=[q for q in pp if q.geom_type=='Point'];return list(min(points,key=lambda q:q.distance(Point(p))).coords[0])

def witch_route():
    start=H['actors']['Witch'];r=F['route_MainStreet'];g=GEOM[r['id']];project=g.project(Point(start[:2]));coords=r['geometry']['coordinates'];heights=r['heights_m'];walk=[start];cum=0
    for i in range(1,len(coords)):
        cum+=dist(coords[i-1],coords[i])
        if cum>project+.001:walk.append(coords[i]+[heights[i]])
    segments=[];t=90.;previous=start
    def append(points,speed,kind):
        nonlocal t,previous
        for p in points:
            dd=math.dist(previous,p)
            if dd<.0001:continue
            dur=dd/speed;segments.append({'start':t,'end':t+dur,'a':previous,'b':p,'kind':kind,'distance_3d_m':dd,'speed_m_s':speed});t+=dur;previous=p
    append(walk[1:],1.1,'main street')
    stair=F['route_MayorStairSubgrade'];append([p+[z] for p,z in zip(stair['geometry']['coordinates'],stair['heights_m'])],.85,'formal stairs / landings')
    court=F['route_MayorCourtWalk'];append([p+[z] for p,z in zip(court['geometry']['coordinates'],court['heights_m'])],1.1,'court / gate')
    append([[2,137.5,44.225],[2,146,44.225]],1.1,'mansion interior to Mayor')
    return {'segments':segments,'arrival':t,'terminal':t+60,'confrontation':60,'distance_3d_m':sum(s['distance_3d_m'] for s in segments)}

def witch_at(t,wr):
    for s in wr['segments']:
        if t<=s['end']:
            f=max(0,min(1,(t-s['start'])/(s['end']-s['start'])));return [a+(b-a)*f for a,b in zip(s['a'],s['b'])]
    return wr['segments'][-1]['b']

if __name__=='__main__':
    w=witch_route();print(json.dumps({'nodes':len(N),'witch':{k:v for k,v in w.items() if k!='segments'},'stairs_start':next(s['start'] for s in w['segments'] if s['kind'].startswith('formal'))},indent=2))
