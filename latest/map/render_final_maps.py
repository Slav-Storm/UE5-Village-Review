"""Offline final review renderer. python render_final_maps.py BASE [OUT]. No UE API."""
from pathlib import Path
import ast,json,sys,csv,hashlib,textwrap,math
from collections import Counter,defaultdict
import numpy as np
from shapely.geometry import shape,Point,LineString
from shapely.ops import substring
HERE=Path(__file__).resolve().parent;BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE;OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else HERE
# Reuse the established map palette and projection, stopping before its first
# figure. No pixels are traced, generated geography invented, or UE queried.
src=OUT/'render_full_simulation.py';tree=ast.parse(src.read_text(encoding='utf-8'));cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fig' for t in n.targets))
exec(compile(ast.Module(body=tree.body[:cut],type_ignores=[]),str(src),'exec'),globals())
FINAL=X['final_state'];TERM=FINAL['terminal_time_s'];PEOPLE=X['people'];T2=json.loads((BASE/'t2_civilian_reactions.json').read_text(encoding='utf-8'))
EVENTS=sorted(X['prior_events']+X['events'],key=lambda e:e['time_s']);DEATHS=[e for e in EVENTS if e['fatalities']]
COL.update(civilian='#9a782c',survivor='#226f60',warning='#3c788a')
OPENING={a['id']:a for a in T1['actors']}

def person_at(pid,t):
 r=pid.split(':')[0]
 if r not in X['groups']:return PEOPLE[pid].get('death_xy_m')
 p=X['groups'][r]['initial_xy']
 for m in X['civilian_movements']:
  if pid in m['members_at_choice'] and m['start_s']<=t:
   g=shape(m['geometry']);p=list((g if g.geom_type=='Point' else g.interpolate(min(g.length,(t-m['start_s'])*m['speed_m_s']))).coords[0])
 return p

def realised(m):
 stop=min(TERM,m['end_s'],m.get('interrupted_at_s') or 1e9)
 stop=min(stop,max(PEOPLE[p].get('death_s',TERM) if not PEOPLE[p]['alive'] else TERM for p in m['members_at_choice']))
 g=shape(m['geometry'])
 return g if g.geom_type=='Point' else substring(g,0,max(0,(stop-m['start_s'])*m['speed_m_s'])),stop

def arrow(ax,g,c,lw=1,alpha=.8,ls='solid'):
 draw(ax,g,'none',c,lw,48,'editable_trace',alpha,ls)
 if g.geom_type=='LineString' and g.length>3:
  a=g.interpolate(max(0,g.length-2));b=g.interpolate(g.length)
  ax.annotate('',xy=b.coords[0],xytext=a.coords[0],arrowprops={'arrowstyle':'-|>','color':c,'lw':lw,'mutation_scale':7,'alpha':alpha},zorder=52)

def actor_routes(ax,who):
 if who in ['Blood','Witch']:
  arrow(ax,shape(OPENING[who.lower()]['geometry']),COL[who],1.35)
  arrow(ax,shape(T3['actors'][who.lower()]['geometry']),COL[who],1.35)
 if who=='Witch':arrow(ax,LineString([q['xyz_m'][:2] for q in X['witch']['timed_points']]),COL[who],1.7)
 elif who=='Bone':
  arrow(ax,shape(OPENING['bone']['geometry']),COL[who],.75,.65,'dashed')
  for m in BONE['bone']['movement_bursts']:arrow(ax,shape(m['geometry']),COL[who],.75,.65,'dashed')
 for m in X['actor_movements']:
  if m['actor']==who:arrow(ax,shape(m['geometry']),COL[who],.8 if who=='Bone' else 1.3,.7,'dashed' if who=='Bone' else 'solid')

def force(ax):
 for e in EVENTS:
  if e['actor']=='Blood' and e.get('geometry'):draw(ax,shape(e['geometry']),COL['Blood'],COL['Blood'],.55,41,e['id'],.16)

def all_deaths(ax,actors=None):
 for e in DEATHS:
  if actors is None or e['actor'] in actors:ax.scatter(*e['xy_m'],marker='X',s=22+5*len(e['fatalities']),color=COL.get(e['actor'],'#444'),edgecolors=BG,lw=.4,zorder=75)

def civilian_routes(ax):
 for m in T1['normal_and_immediate_motions']:arrow(ax,shape(m['geometry']),'#708c87',.35,.5)
 for g in T2['groups']:arrow(ax,shape(g['geometry']),'#708c87',.35,.5)
 for m in T3['civilian_continuations']:arrow(ax,shape(m['geometry']),'#708c87',.35,.5)
 for m in X['civilian_movements']:
  g,stop=realised(m)
  if g.length>.5:arrow(ax,g,COL['civilian'],.6,.48)

def remaining(ax,numbers=True):
 groups=defaultdict(list)
 for p in PEOPLE.values():
  if p['alive']:
   v=person_at(p['id'],TERM);groups[tuple(round(a,1) for a in v)].append(p)
 for xy,ps in groups.items():
  if not (ax.get_xlim()[0]<=xy[0]<=ax.get_xlim()[1] and ax.get_ylim()[0]<=xy[1]<=ax.get_ylim()[1]):continue
  n=len(ps);inj=sum(p['injured'] for p in ps)
  ax.scatter(*xy,s=28+5*n,c=COL['survivor'],edgecolors='#b1612e' if inj else BG,linewidths=1.6 if inj else .6,zorder=80)
  if numbers:ax.text(*xy,str(n),color='white',fontsize=7,ha='center',va='center',weight='bold',zorder=81,clip_on=True)

def page(name,heading,sub):
 fig=plt.figure(figsize=(20,16),facecolor=BG);title(fig,heading,sub)
 main=fig.add_axes([.035,.105,.49,.79]);base(main,[-82,-22,82,175],name,True);rim(main)
 farm=fig.add_axes([.595,.075,.355,.29]);base(farm,[-82,-170,82,-20],name+'_farms',True);rim(farm)
 farm.set_title('LOWER FARMLAND / SAME COORDINATES',fontsize=10,loc='left',pad=12)
 for ax in [main,farm]:
  core['scalebar'](ax,ax.get_xlim()[0]+8,ax.get_ylim()[0]+7,20)
 main.annotate('+X / UPHILL',xy=(-72,166),xytext=(-72,151),ha='center',fontsize=7,color=INK,bbox={'facecolor':BG,'edgecolor':'none','alpha':.95},arrowprops={'arrowstyle':'-|>','color':INK,'lw':.8},zorder=96)
 for fid,label,xytext in [('MayorHall','Mayor',(-23,165)),('Church','Church',(57,111)),('WitchHome','Witch\'s home',(-53,-14))]:
  p=shape(F[fid]['geometry']).centroid.coords[0]
  main.annotate(label,xy=p,xytext=xytext,fontsize=8,color=INK,ha='center',bbox={'facecolor':BG,'edgecolor':'none','alpha':.9},arrowprops={'arrowstyle':'-','color':'#65736b','lw':.6},zorder=90)
 footer(fig,'A single provisional causal branch. 73 fatalities / 97 survivors. The intended near-total massacre is NOT achieved by this branch.')
 return fig,main,farm

def note(fig,y,heading,body):
 fig.text(.575,y,heading,fontsize=12,color=INK,weight='bold',va='top')
 fig.text(.575,y-.028,textwrap.fill(body,79),fontsize=10,color=INK,va='top',linespacing=1.45)

def finish(fig,n):save(fig,n)

fig,a,b=page('13_full_chronology','FULL MASSACRE / CHRONOLOGICAL PLANNING','T+0 to +312.625 seconds • Mayor is the final death • Clean village geometry preserved')
for ax in [a,b]:
 force(ax)
 for who in ['Blood','Bone','Witch']:actor_routes(ax,who)
 all_deaths(ax)
for p,label,off in [([-1,-11],'1 / opening',(30,-10)),([-35,30],'2 / western incidents',(-48,-12)),([-16,59],'3 / refuge',(0,18)),([30,47],'4 / east row',(60,-10)),([23.5,86.4],'5 / bell',(40,5)),([2,124],'6 / guards',(-45,-5)),([2,146],'7 / final',(48,4))]:stamp(a,p,label,INK,off,8)
note(fig,.88,'ONE CANONICAL CLOCK','The maps separate choices from responses. Journeys keep moving across review boundaries; no literal pauses or universal knowledge are introduced.')
rows=[('0–90','Approved opening; barrier seals/darkens; quiet Bone incidents and first Blood strike.'),('90–109','Approved first civilian reaction and second supernatural action.'),('117–140','Smith and water-carrier incidents; independent west/east/field boundary discoveries.'),('133–181','Western refuge, tavern and rescue failures; Bone follows and silences the ordinary bell.'),('197–252','Gate threat, eastern evacuation, returned household and lower refuge incidents.'),('256–292.6','Last investigating guard; stair witnesses pass the Witch; she enters the grounds.'),('312.625','Witch personally kills the Mayor. No post-climax deaths are appended.')]
for i,(t,s) in enumerate(rows):fig.text(.575,.775-i*.047,t,fontsize=10,color=INK,weight='bold');fig.text(.663,.775-i*.047,textwrap.fill(s,57),fontsize=9,color=INK,va='top')
fig.text(.575,.415,'Red: Blood force/route   Purple: Bone incidents/bursts\nTeal: Witch walk   Brown: contact-reactive boundary',fontsize=9,color=INK)
finish(fig,'13_full_chronology')

fig,a,b=page('14_blood_incidents','BLOOD / PERCEIVED CONCENTRATIONS','Solid traces are actual advances • Shaded regions are provisional force footprints, not final destruction')
for ax in [a,b]:force(ax);actor_routes(ax,'Blood');all_deaths(ax,['Blood'])
blood_events=[e for e in DEATHS if e['actor']=='Blood']
offsets=[(-38,-20),(-43,5),(-33,20),(-42,-25),(18,30),(48,18),(45,-5),(48,-22),(68,-40)]
for e,off in zip(blood_events,offsets):stamp(a,e['xy_m'],f"+{e['time_s']:g}",COL['Blood'],off,8)
note(fig,.88,'CONCENTRATION, NOT A HIDDEN CENSUS','Targets follow visible crowds, used doorways, injured cries and helpers. The larger quiet farm and western household populations are excluded from actor knowledge.')
for i,e in enumerate(blood_events):fig.text(.575,.76-i*.03,f"+{e['time_s']:7.3f}   {len(e['fatalities']):2} fatalities   {e['id']}",fontsize=9,color=COL['Blood'])
note(fig,.49,'55 FATALITIES ATTRIBUTED TO BLOOD','Some people behind intersected wall bays are collateral exposures. A wall being hit does not delete an entire house or reveal every occupant. No natural Blood/Witch intersection occurred; none was forced.')
finish(fig,'14_blood_incidents')

fig,a,b=page('15_bone_pattern','BONE / A PATTERN OF INCIDENTS','Separate dashed bursts, observation periods, exact hits and deliberate object strikes • No systematic clearance route')
for ax in [a,b]:
 actor_routes(ax,'Bone');all_deaths(ax,['Bone'])
 for e in BONE['bone']['incidents']:ax.scatter(*e['xy_m'],s=12,facecolors='none',edgecolors=COL['Bone'],lw=.6,zorder=60)
 for e in X['events']:
  if e['actor']=='Bone' and not e['fatalities']:ax.scatter(*e['xy_m'],s=28,facecolors='none',edgecolors=COL['Bone'],lw=1,zorder=70)
for p,label,off in [([-42.7,9.3],'+117 / interposition',(-25,-18)),([-40.3,43.8],'+125–147 / clatter + shutter',(-28,15)),([-22,56],'+154–171 / rescue + pursuit',(-30,20)),([23.5,86.4],'+181 / bell',(38,5)),([2,125],'+197–256 / guards',(48,0)),([2,138.5],'+270 / door',(50,5))]:stamp(a,p,label,COL['Bone'],off,7)
note(fig,.88,'ATTENTION IS THE CAUSAL LINK','Clatter, a slammed shutter, a protective lift, a repeated bell, a watching guard, cart wheels and a moving door each redirect attention. Bone often watches, threatens, allows movement or leaves survivors behind.')
note(fig,.745,'13 FATALITIES / INTENTIONAL HITS','Three belong to the approved opening. Ten occur in the continuation. Hollow marks are nonfatal incidents; crosses are fatal event sites. Neither marks a final corpse pose.')
note(fig,.635,'UNRESOLVED MEMORY','The calm uphill walker becomes an unusual visual stimulus near the end. No new family history, exposition or claim about how much of the child remains is authored.')
note(fig,.525,'FINAL POSITION','Bone remains at the formal grounds edge, approximately (-5, 126) metres, observing the approach. The six church witnesses and other people he abandoned remain alive.')
finish(fig,'15_bone_pattern')

fig,a,b=page('16_witch_route','WITCH / DESTINATION','Unchanged purposeful walk from the external cellar approach to the Mayor • No death-quota waiting')
for ax in [a,b]:actor_routes(ax,'Witch')
for t,label,off in [(109,'+109',(-34,12)),(181.5,'+181.5',(28,-10)),(228.49,'+228.5',(-35,10)),(X['witch']['main_road_end_s'],'+258.2 / stair base',(-40,-15)),(X['witch']['gate_s'],'+292.6 / gate',(48,-5)),(TERM,'+312.625 / Mayor',(55,12))]:
 pts=X['witch']['timed_points'];times=[p['time_s'] for p in pts];i=min(len(pts)-1,int(np.searchsorted(times,t)));p=pts[i]['xyz_m'][:2];a.scatter(*p,s=24,c=COL['Witch'],zorder=80);stamp(a,p,label,COL['Witch'],off,8)
note(fig,.88,'WITCH = DESTINATION','She ignores pleas and surrounding suffering, keeps the existing road and formal stairs, and reaches the Mayor. Their final execution choreography remains reserved; only the minimal personal killing closes the ledger.')
note(fig,.75,'THE STAIR PASS / +265.2','Three descending witnesses pass her on the actual shared staircase. She keeps climbing. This is a naturally occurring environmental-story seed; no road or civilian group was relocated to create it.')
zax=fig.add_axes([.61,.47,.33,.18]);zax.set_facecolor(BG);pts=X['witch']['timed_points'];zax.plot([p['time_s'] for p in pts],[p['xyz_m'][2] for p in pts],color=COL['Witch']);zax.set_xlabel('Canonical seconds (+109 onward)',fontsize=8);zax.set_ylabel('Saved height / m',fontsize=8);zax.tick_params(labelsize=8);zax.grid(alpha=.2)
finish(fig,'16_witch_route')

fig,a,b=page('17_civilian_movements','CIVILIANS / MOVEMENT AND INTERRUPTED INTENT','Executed travel only through T+312.625 • Planned endpoints after the terminal time are not drawn as completed escape')
for ax in [a,b]:civilian_routes(ax);remaining(ax)
note(fig,.88,'MOVEMENT BEFORE FATE','Thin grey traces preserve the approved opening and first reaction; amber traces are the continuation. Each trip retains its reason, speed, start, interruption and original members in editable data.')
note(fig,.745,'LOCAL RESPONSES','People seek household cover, help injured neighbours, carry warnings, follow the bell, ask guards, return from a dangerous boundary, or stay hidden. Different groups can repeat the same fatal mistake without having received a warning.')
note(fig,.62,'97 SURVIVORS, NOT AN INVISIBLE CLEANUP','Green numbers aggregate people at the same current location. Orange rims mark injured survivors. These are provisional planning survivors, not approved new lore or named survivor characters.')
note(fig,.49,'UNFINISHED SERVICE ESCAPE','Three estate refugees are still moving toward the wooded boundary. Their first possible contact would be about +328.48 if uninterrupted, after this simulation ends. No contact or death is assigned to them.')
finish(fig,'17_civilian_movements')

fig,a,b=page('18_barrier_knowledge','BARRIER / CONTACT AND LOCAL KNOWLEDGE','The same opaque boundary remains active • It responds to contact, never fires indiscriminately into the village')
for ax in [a,b]:
 all_deaths(ax,['barrier'])
 for e in X['events']:
  if e['actor']=='barrier':
   for pid in e['direct_witnesses']:ax.scatter(*person_at(pid,e['time_s']),s=16,c=COL['survivor'],zorder=70)
 for k in X['knowledge_events']:
  if k['topic']=='barrier' and k['channel']=='relay' and 'source_xy_m' in k and any(w in k['claim'].lower() for w in ['kill','touch']):
   for r in k['recipient_groups']:arrow(ax,LineString([k['source_xy_m'],r['xy_m']]),COL['warning'],.9,.9)
for e in X['events']:
 if e['actor']=='barrier':stamp(b if e['xy_m'][1]<-22 else a,e['xy_m'],f"+{e['time_s']:.1f} / 1 death",COL['barrier'],(42,12),8)
note(fig,.88,'FOUR INDEPENDENT DISCOVERIES','Western working trail +123.04; eastern animal yard +129.909; west field +135.615; southern approach +204.271. Each first contact kills one person. Nearby direct witnesses learn the lethal rule; other groups do not automatically know.')
note(fig,.74,'DIRECT EXPERIENCE VERSUS REPORT','Green dots show living witnesses at contact time. Blue short arrows show later, local warning exchanges at their actual meeting positions. Hearing an unexplained scream or the ordinary bell does not grant contact knowledge.')
note(fig,.595,'THE ESTATE GROUP HAS NOT TESTED IT','Those refugees know there is an enclosure but never received the four contact reports. Their approach remains an unexecuted intention at the terminal time. This distinction is kept in the JSON and ledgers.')
note(fig,.47,'FUTURE BOSS CONTEXT PRESERVED','The formation / seal / opacity / reactive-contact sequence remains the Witch boss mechanic intended to be understood before the later reconstruction. No boss or memory cutscene is implemented here.')
finish(fig,'18_barrier_knowledge')

fig,a,b=page('19_casualty_progression','CASUALTIES / ONE RECONCILED CENSUS','170 original people • Stable member IDs • Every fatality links to a time, place, activity, cause and witnesses')
for ax in [a,b]:force(ax);all_deaths(ax)
cax=fig.add_axes([.60,.605,.35,.255]);cax.set_facecolor(BG);tt=[0];yy=[0];n=0
for e in EVENTS:n+=len(e['fatalities']);tt.append(e['time_s']);yy.append(n)
cax.step(tt,yy,where='post',color=COL['Blood'],lw=1.8);cax.axhline(170,color='#87968c',ls=':',lw=.8);cax.set_ylim(0,180);cax.set_xlim(0,TERM+4);cax.set_xlabel('Canonical seconds',fontsize=9);cax.set_ylabel('Cumulative fatalities',fontsize=9);cax.tick_params(labelsize=8);cax.grid(alpha=.2)
note(fig,.58,'FINAL LEDGER','73 fatalities: Blood 55, Bone 13, barrier 4, Witch 1. The final one is the Mayor. 97 people remain alive, including two injured western rescue survivors. Nobody is silently removed or assigned a delayed death.')
note(fig,.475,'MATERIAL PREMISE GAP','This branch does not deliver the intended near-total massacre. The actor rules, the fixed Witch walk and these plausible civilian choices leave many hidden pockets. That is a result to review, not a universal prediction or permission to erase survivors.')
finish(fig,'19_casualty_progression')

fig,a,b=page('20_final_aftermath','FINAL AFTERMATH / PLANNING STATE','Primary climax complete at T+312.625 • Survivor mismatch explicitly retained • No final corpse poses or production destruction')
for ax in [a,b]:force(ax);all_deaths(ax);remaining(ax)
for who,p in FINAL['actors'].items():a.scatter(*p,s=65,marker='D',color=COL[who],edgecolors=BG,zorder=90);stamp(a,p,who,COL[who],(36,12),9)
note(fig,.88,'MAYOR IS THE FINAL DEATH','The Witch personally kills him at the end of her continuous route. Exact choreography, her subsequent fate and any later barrier change remain unassigned. No post-Mayor massacre is added.')
note(fig,.745,'97 LIVING / 2 INJURED','Large surviving pockets include 13 in the farm household, seven in each of two western refuges, six in the church, six in an upper home, and smaller scattered households and farm groups. Three workers remain in the Mayor\'s house.')
note(fig,.605,'READ THE MARKS AS REQUIREMENTS','Crosses identify fatal event sites. Red footprints identify force and damage requirements. Green numbers identify living people. These layers guide later design; the healthy UE scene and clean planning maps are unchanged.')
note(fig,.48,'STOP STATE','Blood scans near (23,55); Bone observes near (-5,126); the Witch is at (2,146). The barrier remains contact-reactive. Three service escapees are still en route to it, with no contact before the final frame.')
finish(fig,'20_final_aftermath')

# Add review-facing final material to the accumulating chronological document.
doc=OUT/'MASSACRE_FULL_SIMULATION.md';old=doc.read_text(encoding='utf-8')
if '<!-- FINAL REVIEW END -->' in old:old=old.split('<!-- FINAL REVIEW END -->',1)[1].lstrip()
top=['# MASSACRE FULL SIMULATION — FINAL REVIEW','',f'**Primary event concludes at T+{TERM:.3f}: the Witch personally kills the Mayor, who is the final death.**','',f'**73 fatalities; 97 survivors, including two injured survivors. This branch does not achieve the intended near-total massacre.** The surviving majority is a substantial narrative mismatch, not a cosmetic issue. Per the user\'s instruction, no hidden person is killed merely to satisfy the premise. These are outcomes of one authored causal branch and are not locked canonical survivor characters.','',
'The last pre-Mayor fatal event is at +270. Subsequent frames retain continuous movement, observation, hiding and information limits. Blood is not given the locations of distant shelters, and Bone does not systematically clear the people he has left. The Mayor event is the explicitly authorized minimal ledger closure; no cinematic execution, post-Mayor attack, Witch death/spirit transition or later barrier collapse is invented.','',
'## Review maps','',
'| Map | Purpose |','|---|---|',
'| [13 Full chronology](13_full_chronology.png) | Opening through final Mayor event; major causal regions. |',
'| [14 Blood incidents](14_blood_incidents.png) | Actual advances, perceived concentrations and force footprints. |',
'| [15 Bone pattern](15_bone_pattern.png) | Separate bursts, exact strikes, threats and observation. |',
'| [16 Witch route](16_witch_route.png) | Saved route, stair pass and height profile. |',
'| [17 Civilian movements](17_civilian_movements.png) | Executed normal/reaction travel and surviving pockets. |',
'| [18 Barrier / knowledge](18_barrier_knowledge.png) | Independent contacts and local warning exchanges. |',
'| [19 Casualty progression](19_casualty_progression.png) | Reconciled census and event geography. |',
'| [20 Final aftermath](20_final_aftermath.png) | Living pockets, actor positions and provisional force requirements. |','',
'SVG companions preserve editable vector groups. The unchanged clean base, blank canvas, T0 map and all earlier step layers remain separately available. The first progress milestone and its nine early cycle files remain recoverable unchanged.','',
'## Clear chronological summary','',
'- **0–109:** Preserve the approved quiet opening, first public Blood strike, barrier seal/opacity, initial civilian decisions and second Blood strike. A newly authorized ordinary bell peal at +100 is a documented overlay; it gives an emergency signal only.','- **117–140:** Bone kills the interposing smith, threatens the water carriers, and later kills one at their refuge doorway while allowing the other inside. Three independent side/field contacts teach only nearby witnesses that the barrier is lethal.','- **133–181:** Blood follows the western refuge, the active tavern doorway and a supported rescue group. Bone redirects through shutter noise and rescue gestures, then follows the renewed bell and kills its keeper. Six people in the church withdraw into the nave and remain alive when he leaves.','- **197–224:** A deliberate gate threat becomes a guard death. Blood strikes nine exposed eastern evacuees, then follows a reversing family back into its home. The broad force also reaches two occupants in an intersected neighbouring bay. A separate southern approach contact kills one escapee; returning witnesses later warn other farm-road users.','- **231–270:** Blood follows five people leaving the next refuge. That strike injures occupants behind an intersected wall, whose cries and helpers then become a newly perceptible concentration. Bone attacks people operating or guarding the estate doorway and kills the investigating guard protecting the stair witnesses. The three witnesses descend past the Witch and reach a nearby home.','- **270–312.625:** The immediate audible/visible concentrations have been lost or dispersed; quiet pockets remain. The Witch completes the stairs and grounds without waiting for a body-count target. Three estate refugees use the service road and begin a still-unfinished woodland escape. The Witch kills the Mayor personally at the terminal frame.','',
'## Locked rules','']+[f'- {r}' for r in FINAL['locked_rules']]+['',
'## Guard and estate outcomes','',
'| Person | Role / ordinary response | Outcome |','|---|---|---|',
'| R74:01 | Entrance guard interposes for courtyard refugees. | Bone, +202, formal gate. |',
'| R75:01 | Service guard obtains an actual centre report, escorts witnesses, then protects their stair retreat. | Bone, +256, upper stairs. |',
'| R76:01 | House-duty guard receives reports, admits people and holds the insecure doorway. | Bone, +241, mansion threshold. |',
'| R79:02 | Provisions worker moves a clattering cart into service cover. | Bone, +214. |',
'| R79:01 | Other provisions worker seeks help, is admitted, then tries to secure the door. | Bone, +270. |',
'| R78:01 | Stable worker witnesses the cart strike and hides. | Alive at terminal. |',
'| R65:01–03 | Courtyard refugees seek house protection, then try the service route. | All alive; no barrier contact before terminal. |',
'| R77:01–03 | Household workers withdraw within the mansion. | Alive; local witnesses of the final event. |',
'| R73:01 | Mayor remains in the house as protection is lost. | Witch, +312.625; final death. |','',
'No guard\'s historical responsibility for the lover/son tragedy is decided. Reports identify only what the sender could observe or hear.','',
'## Final state and required narrative review','',
'The survivor census includes the uninjured water carrier, the six church occupants, the parent/child group Bone abandoned near the forge, older western households, farm residents, the three stair witnesses, three mansion workers and other quiet pockets. The complete [survivor ledger](full_survivors.csv) lists every person, current position, injury and final intent. Quiet does not mean calm, informed or safe.','',
'The two injured survivors are R24:01 and R28:01, concealed beside the western damaged home. Their eventual medical outcomes are unassigned; no delayed death is invented.','',
'The three estate refugees have not touched the boundary. Their leading intention would reach it around **+328.48** if nothing intervened, beyond the **+312.625** terminal frame. Their future response and any contact are explicitly unexecuted.','',
'The intended successful extermination remains **unresolved**. This branch supports a severe massacre and the Mayor climax, but it cannot honestly stand as the final near-total-annihilation reconstruction. A later review can reconsider specific civilian choices, awareness/visibility assumptions or narrative timing. This output does not silently change those rules, move the village, invent an omniscient hunt or kill the remaining 97.','',
'## Geometry, perception and damage assumptions','',
'All 50 pre-continuation artifacts and the healthy scene geometry are unchanged. The terrain remains a 2D projection with saved heights; the Witch uses a 3D-distance clock. Civilian foot speeds are plan-speed approximations, especially on stairs and wooded slopes. Human-width clearance, retaining edges, detailed interior sight lines, hearing and usable light after opacity require later UE validation. No emissive barrier or final lighting lore is locked to justify long-distance sight.','',
'A 28m conservative candidate filter is a planning aid, not supernatural sensing. Three explicitly documented investigative decisions use already acquired voices/doorways just beyond or behind that filter. The subsequent strikes require reacquisition or continued audible occupancy. Indoor numerical counts in inventories are labelled planner counts; Blood does not know them.','',
'The force model uses a provisional central fatal region and outer injury region. It is not a calibrated gameplay damage model or unique physical prediction. Every structural requirement identifies only an intersected existing feature/bay, not a whole-building deletion. Bone\'s intended human hits are exact; object hits are deliberate. No final gore, corpse pose, rubble mesh or asset is produced.','',
'## Environmental-story seed register','',
'The [consolidated JSON](full_simulation.json) keeps each seed paired with the ordinary action it interrupts: handcart movement, water carrying, a protective smith, a failed refuge call, a tavern receiving doorway, a supported rescue, a shutter closing, the bell rope, family evacuation and return, provisions handling, guard interposition, door securing, independent boundary attempts, and the Witch passing people running down her staircase. These are causal placement opportunities, not finished aftermath props.','',
'## Editing and verification','',
'Each C##_reaction.json / C##_action.json pair is separately editable and recoverable. full_simulation.json is the consolidated rendering input and includes stable people, timed movement, decision evidence, knowledge events, perception inventories, attention changes, force regions, provisional damage and story seeds. Reconcile edits to the full input and relevant cycle file together; do not edit the clean map. Run `python render_full_simulation.py .` then `python render_final_maps.py .` in this folder to regenerate notes, ledgers and the final map set.','',
'The [validation record](full_validation.json) checks the 170-person census, unique deaths, event-clock reconciliation, all source hashes, nine published early cycles, movement lengths/bounds, decision evidence timing, fatal exposure regions, short Bone hit ranges and the final Mayor-only terminal event. This validates consistency of this branch; it does not validate its unmet near-total-death premise.','',
'<!-- FINAL REVIEW END -->','']
doc.write_text('\n'.join(top)+old,encoding='utf-8',newline='\n')
with (OUT/'full_survivors.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['person','origin','group','role','x_m','y_m','injured','inside','final_intent','direct_barrier_level','received_barrier_warning'])
 snap=X['snapshots'][-1]['groups']
 for p in PEOPLE.values():
  if p['alive']:
   g=snap[p['group']];w.writerow([p['id'],p['origin'],p['group'],p['role'],*person_at(p['id'],TERM),p['injured'],g['inside'],g['intent'],p['barrier_level'],p['barrier_reported']])
with (OUT/'full_knowledge_ledger.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['time_s','topic','channel','source','source_group','recipients','claim','phase'])
 for k in sorted(X['knowledge_events'],key=lambda k:k['time_s']):w.writerow([k['time_s'],k['topic'],k['channel'],k['source'],k.get('source_group'),';'.join(k['people']),k['claim'],k['phase']])
with (OUT/'full_movement_ledger.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['id','group','original_members','start_s','planned_end_s','executed_through_s','planned_distance_m','executed_distance_m','reason','phase'])
 for m in X['civilian_movements']:
  g,t=realised(m);w.writerow([m['id'],m['group'],';'.join(m['members_at_choice']),m['start_s'],m['end_s'],t,m['distance_m'],round(g.length,3),m['reason'],m['phase']])
print('Rendered eight final maps and full review notes:',FINAL['fatalities'],'fatalities;',FINAL['survivors'],'survivors.')
