import json, math, heapq, random
from pathlib import Path
import numpy as np
from shapely.geometry import shape,Point,LineString
from shapely.ops import nearest_points,unary_union
ROOT=Path(__file__).resolve().parent
MAP=json.loads((ROOT/"inputs/map_data.json").read_text())
T0=json.loads((ROOT/"inputs/t0_activity.json").read_text())
T1=json.loads((ROOT/"inputs/t1_simulation.json").read_text())
BONE=json.loads((ROOT/"inputs/bone_completion.json").read_text())
F={x["id"]:x for x in MAP["features"]}
BUILD={k:shape(v["geometry"]) for k,v in F.items() if v["category"] in ("building","outbuilding")}
BARRIER=shape(T1["barrier"]["geometry"])
ROADS=unary_union([shape(f["geometry"]) for f in F.values() if f["category"]=="route_reference"])
def xy(g):return list(g.coords)[0]
def dist(a,b):return math.dist(a[:2],b[:2])
def center(k):return xy(BUILD[k].centroid)
def outside(p):
 p=Point(p)
 for g in BUILD.values():
  if g.contains(p):p=nearest_points(g.boundary,p)[0];p=Point(p.x+(p.x-g.centroid.x)*.10,p.y+(p.y-g.centroid.y)*.10)
 return xy(p)
DOORS={}
for k,g in BUILD.items():
 a,b=nearest_points(g.boundary,ROADS)
 c=g.centroid;v=np.array(xy(a))-np.array(xy(c));v/=max(.001,np.linalg.norm(v))
 front=list(np.array(xy(a))+v*.7)
 opposite=LineString([xy(c),list(np.array(xy(c))-v*30)]).intersection(g.boundary)
 if opposite.geom_type=="MultiPoint":opposite=list(opposite.geoms)[-1]
 rear=outside(list(np.array(xy(opposite))-v*.7)) if opposite.geom_type=="Point" else outside([g.bounds[0]-.8,c.y])
 DOORS[k]={"front":front,"rear":rear,"centre":xy(c)}
DOORS["Church"]["front"]=[23.5,83.7]
DOORS["MayorHall"]["front"]=[2,136.8]
OBST=unary_union([g.buffer(.25) for g in BUILD.values()])
# 2m visibility-tested walking grid. Shortcuts use clearing surface, not walls.
STEP=2
NODES={}
for ix in range(-43,43):
 for iy in range(-84,93):
  p=(ix*STEP,iy*STEP)
  if BARRIER.buffer(2).covers(Point(p)) and not OBST.contains(Point(p)):NODES[(ix,iy)]=p
def node(p):
 q=(round(p[0]/STEP),round(p[1]/STEP))
 if q in NODES:return q
 return min(NODES,key=lambda n:dist(NODES[n],p))
CACHE={}
def path(a,b):
 a=outside(a);b=outside(b);aa=node(a);bb=node(b)
 key=(aa,bb)
 if key in CACHE:return [a]+CACHE[key]+[b]
 if not LineString([a,b]).intersects(OBST):return[a,b]
 todo=[(dist(a,b),0,aa)];cost={aa:0};prev={}
 while todo:
  _,c,u=heapq.heappop(todo)
  if u==bb:break
  if c>cost[u]+.0001:continue
  for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
   v=(u[0]+dx,u[1]+dy)
   if v not in NODES:continue
   seg=LineString([NODES[u],NODES[v]])
   if seg.intersects(OBST):continue
   # Streets preferable, but backyard/field ground remains traversable.
   w=dist(NODES[u],NODES[v])*(1 if ROADS.distance(Point(NODES[v]))<4 else 1.18)
   n=c+w
   if n<cost.get(v,1e9):
    cost[v]=n;prev[v]=u;heapq.heappush(todo,(n+dist(NODES[v],NODES[bb]),n,v))
 if bb not in cost:
  # Narrow passages can fall between 2m samples. Use a continuous visibility graph.
  polys=OBST.buffer(.18,join_style=2).simplify(.15,preserve_topology=True)
  verts=[a,b]+[list(p) for g in (list(polys.geoms) if hasattr(polys,"geoms") else [polys]) for p in list(g.exterior.coords)[:-1]]
  todo=[(0,0)];cost2={0:0};prev2={}
  while todo:
   c,u=heapq.heappop(todo)
   if u==1:break
   if c>cost2[u]+.0001:continue
   for v in range(len(verts)):
    if v==u:continue
    if LineString([verts[u],verts[v]]).intersects(OBST):continue
    nc=c+dist(verts[u],verts[v])
    if nc<cost2.get(v,1e9):cost2[v]=nc;prev2[v]=u;heapq.heappush(todo,(nc,v))
  if 1 not in cost2:raise ValueError(("Continuous route blocked",a,b))
  r=[1];u=1
  while u!=0:u=prev2[u];r.append(u)
  return [verts[i] for i in reversed(r)]
 route=[bb];u=bb
 while u!=aa:u=prev[u];route.append(u)
 route=[NODES[u] for u in reversed(route)]
 # simplify only with visible segments
 simp=[a];i=0
 while i<len(route):
  j=i
  while j+1<len(route) and not LineString([simp[-1],route[j+1]]).intersects(OBST):j+=1
  simp.append(route[j]);i=j+1
 CACHE[key]=simp[1:]
 return simp+[b]
def length(ps):return sum(dist(a,b) for a,b in zip(ps,ps[1:]))
def along(ps,d):
 for a,b in zip(ps,ps[1:]):
  n=dist(a,b)
  if d<=n:return [a[i]+(b[i]-a[i])*d/max(n,.00001) for i in range(2)]
  d-=n
 return list(ps[-1])
def visible(a,b,ignore=()):
 seg=LineString([a,b])
 return not any(seg.crosses(g.buffer(-.3)) for k,g in BUILD.items() if k not in ignore)
def witch_route():
 start=[-15.556599900140176,36.37393621055349,5.639787035645556]
 road=F["route_MainStreet"]; coords=road["geometry"]["coordinates"];h=road["heights_m"]
 idx=min(range(len(coords)),key=lambda i:dist(coords[i],start))
 while idx<len(coords)-1 and coords[idx][1]<start[1]:idx+=1
 pts=[start]+[list(p)+[z] for p,z in zip(coords[idx:],h[idx:])]
 kinds=["road"]*(len(pts)-1)
 for name,kind in [("route_MayorStairSubgrade","stair"),("route_MayorCourtWalk","court")]:
  f=F[name]
  for p,z in zip(f["geometry"]["coordinates"],f["heights_m"]):
   v=list(p)+[z]
   if math.dist(pts[-1],v)>.01:pts.append(v);kinds.append(kind)
 # Threshold to current Mayor position, ordinary interior approach assumed.
 pts.append([2,146,44.225]);kinds.append("interior")
 times=[90.]
 for a,b,k in zip(pts,pts[1:],kinds):
  speed=.85 if k=="stair" else 1.1
  times.append(times[-1]+math.dist(a,b)/speed)
 return pts,times,kinds

