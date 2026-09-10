# MASSACRE SIMULATION V4 — INDEPENDENT RE-SIMULATION FROM T+90

**CLOSED at T+366.0005. 100 fatalities, 70 survivors, including 10 injured survivors. FAILED against the near-total-massacre premise. Not approved for UE5 implementation.**

V4 is a separate experimental planning branch. The Mayor is its final death, personally killed by the Witch after exactly sixty seconds of confrontation. No post-terminal cleanup, hidden casualties or final corpse poses are added. These survivors are retained outcomes, not new canon.

**The source and model audit also fails in material areas.** Two unpinned western field workers (P02-03/P02-04) were initialized at (−31.6,−77), which falls in OuterPasture rather than their assigned SouthLongField. Their later events must remain provisional. The closed result has not been silently repaired after reading earlier branches. New structural openings affect cover and reactions but are not incorporated into a rebuilt navigation graph. First hits against intact covered groups are conservatively nonfatal. These limitations mean this is not a clean test proving that the requested V4 rules inherently fail.

## Review navigation

The sixteen PNG/SVG sheets are listed in [README](README.md). The original [clean base](../01_village_base_map.png), [blank planning map](../02_massacre_planning_blank.png), [T0](../03_T0_normal_activity.png) and [completed T1](../07_T1_bone_timeline.png) remain unchanged.

- [Frozen simulation JSON](v4_simulation.json)
- [Initial T90 register](initial_state.json)
- [Separate action/reaction phase records](action_reaction_phases.jsonl)
- [Cycle snapshots](v4_cycle_states.json)
- [Casualty ledger](casualties.csv) and [audited causal chains](v4_casualty_audit.json)
- [All survivors](survivors.csv) and [full survivor records](v4_survivors.json)
- [Executed actor paths](v4_executed_actor_paths.json)
- [Metrics](v4_metrics.json), [validation](v4_validation.json), [post-closure comparison](v4_comparison.json)
- [Closure digest](CLOSURE.json), [source manifest](source_manifest.json), [parameters](parameters.json)

## Source boundary and starting state

The supplied design bible was read first. Only map_data, map_views, T0 activity, T1 simulation, Bone completion and locked pre90 rules were used as historical inputs. V1/V2/V3 post90 files were first inspected after V4's closure digest was written. Geometry hash and source file hashes are in source_manifest.json.

The original population is170, with163 alive and four injured atT+90. Seven prior deaths are retained: three by Bone and four by Blood. Blood starts at(−2.2088,44.5243); Bone at(−37.5,8.8), focused on the living M05 parent/child at(−34.3,9.2); Witch at(−15.5566,36.3739,5.6398). The barrier is opaque and contact-reactive. B3/B4 begin at zero. Panic conveys catastrophe, not attacker identities or boundary mechanics.

Stable Pxx-nn IDs subdivide the existing T0 population and micro-groups without adding people. Exact T1 motion/micro endpoints remain; indoor membership and previously unpinned yard/field individuals use explicit refinements. The two-worker allocation error above is a failure in those refinements.

## Method and working parameters

This is a human-authored, event-driven causal ledger supported by deterministic geometry/accounting tools, not a probabilistic crowd or physics simulator. Eighteen major checkpoints contain shorter alternating ACTION/REACTION records. Existing orders advance on one clock, with event times ending increments. Maps show executed paths clipped at interruption or terminal time, not every intended destination.

Blood keeps his approved1.7019m/s movement; Bone bursts at9m/s; Witch remains1.1m/s on the saved3D route. Other routes avoid projected roofs and use a5% terrain allowance. Inferred threshold joins and rooms are provisional. No UE navmesh, lighting or raycast validation occurred. Macro geometry was not modified.

Accessible spilled blood begins at five relative units at the public attack site. A fatal spill adds one unit; injury adds.25; a later fatality adds the remaining.75 rather than double counting. Remote spills contribute only after a physical connection. Resource units are not litres.

Reach, branch slots, search speed and budget rise with the square root of accessible resource and use caps. FED, SATURATED and DELUGE are internal labels. Secondary nodes are search-only and require a connected substantial source. The body still has to reach every offensive corridor. The final minute multiplies bounded search/pressure parameters; body speed does not change.

Search records distinguish unsearched, weak, empty, active, strong and dispersed states. Low-value probes withdraw while retaining negative memory. At+280, prolonged modest returns also yield capacity to unresolved frontiers. A withdrawn branch cannot provide current hidden occupancy; it retains only its last observation. Range is approximated in plan space, not a solved hydraulic or geodesic attenuation model.

Structural state progresses intact → damaged → breached → heavily breached. Repeated impacts change casualty exposure and trigger new civilian choices. Opening points and intended passability are recorded for later work. **The static roof-avoidance route graph does not actually gain those new portals**, so access/visibility benefits are incompletely tested.

The coarse casualty resolver preserves covered occupants on a first intact-wall hit, then increases danger through repeated/breached exposure. Shared group anchors and this first-hit assumption materially affect results. They need replacement with spatial interior exposure if this becomes a production reconstruction.

## Chronological reading

- +90–110: blackout interrupts ordinary activity. Bone escalates the existing parent/child encounter, kills the shielding parent and then the apprentice who tries to help. Blood attacks visible rescuers around the four previously injured people. The bell is independently rung at+100 for public emergency only. The tavern splits after corner damage; Blood subsequently attacks the noisy refuge.
- +116–142: Bone follows the actual lower warning stream into the farms, kills an exposed warning carrier, punctures the barn, then attacks a helping farm worker. Barn households disagree and split. At+130 the forest crew and a western agricultural pair independently test the barrier; only local survivors gain B4.
- +142–184: Blood relocates toward a strong western household signal and reacquires its adjacent refuge after it disperses. Repeated strikes remove cover at+168/+176. Bone crosses back through lower households and the old quarter, injures/kills emerging people, forces a family from damaged cover, and kills the caregiver. Children continue toward public help.
- +188–254: Bone recognizes the entrance guard locally. A moving66-second torment sequence follows church approach → upper junction → formal stairs → gate. Bone injures then kills the helper the guard tries to rescue; later he kills the intervening service guard. The son-killer is deliberately spared until+254. Other guards acquire no historical guilt.
- +216–280: Blood physically reaches the lower refuge and attacks its already punctured face. A newly connected farm signal then causes another long relocation. He reaches farm attack range at+258. The western barn receives consecutive impacts at+266/+272, with different protection on the second. The provisions driver independently contacts the barrier at+280.
- +280–306: Bone follows upper movement, changes district and pressures the church doorway. Blood starts uphill, then a stronger newly reached eastern refuge redirects him. Witch continues the actual road and stair route and reaches the Mayor at+306.0005.
- +306–366: Witch secures Mayor and sustains a sixty-second confrontation. The house guard retreats to service workers. Rage intensifies existing connected searches. Bone pressures eastern shelters and follows human reactions toward the boundary and back to the church. New independent boundary contacts occur at+332. Blood reacquires eastern concentrations at+342/+360 from physical body range. Witch kills Mayor at+366.0005, ending the ledger.

## Locked behaviour and observed consequences

**WITCH = DESTINATION.** Remaining3D route is237.6006m, producing arrival+306.0005. She ignores the guard's plea and does not hunt or rescue. Blood naturally intersects her route at+110 and+134; it flows around her without a dodge. That sight is local evidence, not global knowledge of guilt. Exact restraint/execution and final dialogue remain reserved.

**BLOOD = CONCENTRATION.** Coarse connected returns and visible arrivals can outweigh nearer modest signals. His path links centre, lower village, farms and eastern district. Western houses are struck from the junction edge. Detection and offensive range remain separate. Search coverage improves more than body coverage.

**BONE = ATTENTION / ACTIVE PREDATION.** His five-district pattern contains meaningful injuries, direct kills, broken cover, route denial and forced movement. Repetitive walls and ordinary Blood crashes lose value. Visible reacting streams can redirect him without commands or telepathy.

**BARRIER = BOUNDARY / REACTIVE WEAPON.** Five actual contact events produce five direct deaths. No inward random attacks occur. Direct B4 and spoken reports remain distinct; independent eastern/upper mistakes remain possible despite earlier western discoveries.

**CIVILIANS = LOCAL KNOWLEDGE.** Families and refugees disagree. Some stay behind cover, some split, some abandon unsafe rescues, some seek church or guards, and some try an untested edge. Refusing entry/rescue is not automatically wrongdoing. Household-level decision timing and some outdoor holds are coarse and need more continuous validation.

## Guard, opportunists and final confrontation

The entrance guard isP16-02. Recognition at+188, final kill+254, duration66 seconds. A protected helper is injured+196 and killed+206; the intervening service guardP16-03 dies+238. Deliberate near-threats and denied routes connect these events. Emotional opportunities concern fractured recognition and inability to save others, without finished dialogue.

P08-24 steals stall takings for personal gain and carries the pouch through later refuge choices. P17-01 tries to monopolize provisions-cart space for valuables; his helper refuses. The driver later abandons the cart and independently attempts the boundary. Bone targets the helping workers rather than dispensing moral punishment. No people were added.

MayorP16-01 is secured at+306.0005. Subjects for later writing are lover, son, authority, responsibility, village suffering, helplessness and saving him until last. This is active rage, not later remorse. She does not possess a survivor counter. At+366.0005 she personally kills him. No reason for later creature/barrier deactivation is invented; this primary event ledger simply stops.

## Results and limits

| V4 measure | Result |
|---|---:|
| Fatalities / survivors / injured survivors |100 /70 /10|
| Blood / Bone / barrier / Witch direct deaths |76 /18 /5 /1|
| Blood executed plan travel |276.17m|
| Bone executed plan travel |539.66m|
| Completed footprint probes |41/41|
| Occupied shelters compromised |36|
| Secondary search nodes |8|
| Active trace at close / all historical laid trace |971.2m /2366.0m|
| Yard-area proximity proxy reached |83.6%|
| Breached/heavily breached structures |23|
| Forced movement orders / distinct affected people |188 /121|
| Other-killer fatalities with a Bone movement chain |11|
| Barrier fatalities with Bone movement context |3|

Coverage means building/outbuilding footprints buffered5m, measuring the area within8m of an actually laid search trace, including withdrawn branches. It is not proof of sensing every person in that area. All41 threshold probes include empty/outbuilding checks. Direct killer attribution is unchanged by indirect Bone context. Eleven non-Bone fatalities have a recorded prior Bone-caused movement chain; this is not a counterfactual proof that all eleven required Bone.

Nineteen fatalities occur during the final minute: twelve Blood, four Bone, two barrier and the Mayor. Amplification visibly increases range/budget in the recorded model, but no no-rage counterfactual isolates its unique causal contribution.

## Post-closure comparison

The following comparison was made only after the frozen closure hash was recorded.

| Branch | Dead | Alive | Blood | Bone | Barrier | Witch |
|---|---:|---:|---:|---:|---:|---:|
|V1|73|97|55|13|4|1|
|V2|112|58|101|5|5|1|
|V3|57|113|45|6|5|1|
|V4|100|70|76|18|5|1|

| Branch | Blood sampled trace, m | Bone sampled trace, m | Blood sampled zones | Bone sampled zones |
|---|---:|---:|---|---|
|V1|138.9|247.6|centre, old/eastern|centre, estate, lower, upper/church, western|
|V2|112.1|318.3|centre, old/eastern, upper/church, western|centre, lower, old/eastern, upper/church, western|
|V3|31.7|507.6|centre, old/eastern|centre, lower, old/eastern, upper/church, western|
|V4|273.3|521.1|centre, farms, lower, old/eastern|estate, farms, lower, old/eastern, upper/church|

Historical travel figures are snapshot lower bounds with unequal sampling, not standardized exact distances. V4's clipped executed-order figures above are its authoritative route measure.

V4 substantially widens searching and physical relocation. Bone is more directly consequential than any prior branch here, and eleven other-killer deaths have recorded Bone movement context. His guard sequence is mobile and affects two attempted protections. V3 and V4 happen to end that guard's life at+254; V4 begins recognition earlier and lasts66 seconds rather than51, with independently derived participants and movement.

Distributed nodes and search memory reduce permanent invisibility: every footprint is eventually checked and groups move repeatedly. However, late detection and dispersion can send Blood on long walks while survivors choose new rooms/buildings. Greater detection does not automatically make a slow body able to strike every refuge before the fixed ending. V4 has more casualties than V1/V3 but fewer than V2, and still leaves dozens.

Barrier deaths remain five, but three V4 contacts have recorded Bone-forced movement context. Local ignorance still matters; awareness is not transmitted globally. First-hit cover handling and static portal navigation suppress the intended structural escalation. Some old small refuges remain safe because no offensive corridor reaches them; others are found late. This is partly an implementation/parameter problem, not merely a narrative-rule result.

No mechanic here becomes globally omniscient or an autonomous remote killer. The weak point is instead uneven actionable coverage within the available time. The first-intact-hit casualty rule is particularly conservative. The final-minute amplifier expands a network but cannot erase earlier travel costs or silently kill dispersed people.

**Recommended next work only, not executed:** correct the two field pins from source; replace the first-hit/room proxy with explicit exposed/interior positions; make recorded breaches real route/stream/visibility portals; verify perception and hill travel in3D; process destination arrivals and new local danger more continuously; then run a fresh independent test. Do not add quotas, global exact sensing, arbitrary waiting for a population count, or post-Mayor cleanup.

## Every action/reaction checkpoint


### Cycle 01 — through +94.000: Blackout and first local intentions

ACTION: Blood attends to outdoor rescuers; Bone escalates M05 shielding encounter at94.

REACTION: Local households seek known cover; farm workers gather at familiar storage; caretaker heads to rope; entrance guard starts down stairs.

Census: 7 dead /163 alive /5 injured alive. Blood: FED, 5 accessible units. Witch: (-12.29, 39.23, 6.33).

### Cycle 02 — through +102.000: Aid interrupted and bell

ACTION: At98 Blood attacks actual rescuers. At102 Bone kills the shielding parent, after the earlier injury. Bell chosen at100.

REACTION: Child seeks relatives; smith approaches local cry; centre survivors move east; one existing opportunist steals.

Census: 17 dead /153 alive /0 injured alive. Blood: SATURATED, 13.0 accessible units. Witch: (-4.72, 43.56, 7.29).

### Cycle 03 — through +116.000: First refuge compromise

ACTION: Bone kills the distracting apprentice at108. Blood breaches the noisy tavern at110; network reaches several actual thresholds.

REACTION: Tavern splits into stay/service/east exit choices; smith abandons rescue; centre shelter splits; guard follows emergency bell independently.

Census: 21 dead /149 alive /1 injured alive. Blood: SATURATED, 16.25 accessible units. Witch: (9.84, 48.32, 8.88).

### Cycle 04 — through +130.000: Lower farms and independent boundary test

ACTION: Bone crosses into farms following the actual warning stream, kills one warning witness, then punctures the barn. Search extends toward remembered pre90 blood.

REACTION: Barn splits between staying behind storage and returning to family farmhouse; separate forest/field parties test only their own boundary sections.

Census: 22 dead /148 alive /1 injured alive. Blood: SATURATED, 16.25 accessible units. Witch: (24.37, 52.61, 11.54).

### Cycle 05 — through +142.000: First independent barrier attacks

ACTION: At130 the forest crew and western field pair independently test their own boundary sections. Blood strikes the moving porch escapees at134; Bone kills the exposed farm helper.

REACTION: Survivors recoil with direct B4 only locally; lower tavern refugees choose a nearby household; upper households choose the bell; Bone relocates out of farms.

Census: 32 dead /138 alive /1 injured alive. Blood: SATURATED, 23.25 accessible units. Witch: (35.35, 58.89, 13.61).

### Cycle 06 — through +156.000: Distributed pressure and western commitment

ACTION: Blood commits west to a strong connected concentration. Bone completes a farm-to-lower relocation and punctures the crowded lower refuge.

REACTION: Households make different compromise decisions; service cart driver exploits fear while helper refuses; forest witnesses seek a local warning audience.

Census: 32 dead /138 alive /1 injured alive. Blood: SATURATED, 23.25 accessible units. Witch: (35.71, 73.38, 16.02).

### Cycle 07 — through +174.000: Reacquisition and structural loss

ACTION: Blood follows a strengthened adjacent western threshold after the prior concentration disperses. His168 strike opens Cottage02. Bone injures an emerging guide, kills an isolated split member, then relocates uphill.

REACTION: Households reassess after new wall damage; injured people move more slowly; negative/empty probes are retired to free frontier budget.

Census: 35 dead /135 alive /6 injured alive. Blood: SATURATED, 26.25 accessible units. Witch: (18.01, 80.0, 20.75).

### Cycle 08 — through +184.000: Repeated damage and forced family movement

ACTION: Blood follows the western doorway concentration at176; previous breaches now remove cover. Bone forces the old-quarter family out and kills the shielding caregiver at180.

REACTION: Children follow their existing churchward intent and a guard goes to help; eastern passers choose another household; western households reassess cover.

Census: 45 dead /125 alive /2 injured alive. Blood: DELUGE, 36.25 accessible units. Witch: (7.19, 80.4, 22.57).

### Cycle 09 — through +202.000: Recognized guard and mobile torment

ACTION: Bone follows the already-fleeing children and recognizes the entrance guard at188. He deliberately threatens the guard, then injures the helper the guard tries to protect at196. Blood continues a long lower-village relocation.

REACTION: Guard escorts children and attempts rescue, caretaker admits them, and western B4 reports spread only inside the shared shelter.

Census: 45 dead /125 alive /3 injured alive. Blood: DELUGE, 36.25 accessible units. Witch: (-12.13, 82.44, 25.84).

### Cycle 10 — through +222.000: Guard retreat and lower refuge failure

ACTION: Bone kills the guard's rescued helper at206 and denies the upper turn at212, prolonging recognition while moving. At216 Blood reaches range of the lower refuge and attacks its already damaged face.

REACTION: Guard deliberately draws Bone away from the church; bell ceases for assistance. Lower refugees re-evaluate after cumulative damage.

Census: 57 dead /113 alive /5 injured alive. Blood: DELUGE, 48.0 accessible units. Witch: (-31.4, 91.62, 29.47).

### Cycle 11 — through +242.000: Farm discovery and moving guard torment

ACTION: Physical probes discover the farm; Blood commits down the approach. Bone overtakes the recognized guard and kills the service guard who intervenes at238.

REACTION: The son-killer continues up the formal stairs; local farm warning spreads by a returning witness; households react to newly reached thresholds.

Census: 58 dead /112 alive /5 injured alive. Blood: DELUGE, 48.0 accessible units. Witch: (-20.48, 104.78, 31.08).

### Cycle 12 — through +262.000: Farm strike and son-killer's death

ACTION: Blood reaches physical farm attack range at258. Bone kills the recognized entrance guard at254 after66 seconds of mobile torment.

REACTION: Farm refuges reassess the yard strike; driver tries the service-side forest without B4; helper chooses warning rather than flight; mansion guard closes the front.

Census: 70 dead /100 alive /10 injured alive. Blood: DELUGE, 60.25 accessible units. Witch: (-3.35, 102.5, 32.41).

### Cycle 13 — through +280.000: Cumulative barn failure and renewed Bone frontier

ACTION: Blood strikes the western barn at266 and272, with cumulative damage. Bone injures a helper, then leaves the estate toward a new upper-west stimulus.

REACTION: Barn B4 reports are local; service workers gather around injury; driver independently seeks the forest-side perimeter; compromised shelters choose again.

Census: 79 dead /91 alive /12 injured alive. Blood: DELUGE, 69.25 accessible units. Witch: (0.82, 119.26, 40.67).

### Cycle 14 — through +300.000: Upper frontier and church pressure

ACTION: Blood begins a second long relocation from farms toward upper concentration memory. Bone kills an exposed upper watcher, then reaches and punctures the church doorway.

REACTION: Upper travellers split between public refuge and a woodland attempt; church occupants make fresh shelter choices; modest long-held probes yield budget to unexplored frontiers.

Census: 80 dead /90 alive /12 injured alive. Blood: DELUGE, 69.25 accessible units. Witch: (2.0, 139.4, 44.23).

### Cycle 15 — through +312.000: Witch arrives; final minute starts

ACTION: Bone kills the exposed caretaker at300, then relocates toward a visibly reacting eastern node. Blood turns toward the strong distant refuge. Witch arrives at306.0005 and secures the Mayor.

REACTION: Church occupants reassess; house guard retreats to local service workers. Rage intensifies physically connected searches. No census controls the confrontation clock.

Census: 81 dead /89 alive /12 injured alive. Blood: DELUGE, 71.0 accessible units. Witch: (2, 146, 44.23).

### Cycle 16 — through +332.000: Final-minute shelter pressure

ACTION: Bone intercepts a limping refugee, punctures a crowded eastern refuge, then kills an exposed protector. Blood's remote signal weakens through dispersal but remains coarse short-term memory.

REACTION: Eastern household chooses unbriefed woodland escape; other occupants stay or split. Boundary contacts resolve only on physical arrival; no global B4 transfer.

Census: 85 dead /85 alive /11 injured alive. Blood: DELUGE, 72.25 accessible units. Witch: (2, 146, 44.23).

### Cycle 17 — through +354.000: Late reacquisition and local survivor decisions

ACTION: Bone kills an exposed eastern boundary helper, then relocates sharply to a new church doorway reaction. Blood reacquires the shifted eastern concentration and strikes at342.

REACTION: A direct B4 witness hides alone inside the forest; other refugees reconsider damaged cover; warnings remain local. The Mayor remains secured on the fixed confrontation clock.

Census: 87 dead /83 alive /16 injured alive. Blood: DELUGE, 73.5 accessible units. Witch: (2, 146, 44.23).

### Cycle 18 — through +366.001: Primary event closes

ACTION: Final eastern Blood strike at360. Witch kills the Mayor at366.0005 after exactly60 seconds of confrontation.

REACTION: Last surviving groups have only their local experiences and warnings. No further massacre deaths or attacker decisions are simulated.

Census: 100 dead /70 alive /10 injured alive. Blood: DELUGE, 85.75 accessible units. Witch: (2, 146, 44.23).

## All surviving pockets

Every survivor is listed individually in survivors.csv with knowledge and movement references. These pocket groupings do not merge their knowledge.

| Place / current group | People | IDs | Causal reason |
|---|---:|---|---|
|Church|2|P09-01, P10-10|At Church, structural state 2. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. Prior damage was not assumed to kill every occupant; unhit space and departures remained possible.|
|Cottage_03|7|P10-17, P10-18, P10-19, P10-20, P12-03, P12-07, P12-08|At Cottage_03, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|Cottage_04|2|P06-08, P06-14|At Cottage_04, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|Cottage_05|2|P11-19, P11-20|At Cottage_05, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|Cottage_09|4|P06-04, P06-05, P06-11, P06-12|At Cottage_09, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|Cottage_11|2|P12-01, P12-02|At Cottage_11, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|EndRowCottage|3|P11-21, P11-22, P15-03|At EndRowCottage, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|Outside: approach-witnesses|1|P05-06|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: delivery-helper|1|P17-02|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred. Estate workers/house guard moved on local crisis information; neither creation executed an attack on their final service-side position.|
|Outside: east-home|1|P03-03|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: east-passers-split5|1|P08-17|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: east-tools|1|P01-03|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: east-yard|1|P03-07|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: edge-animal|1|P14-07|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Direct boundary experience discouraged another crossing. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: edge-animal-split15|1|P14-05|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: estate-staff|3|P16-05, P16-06, P16-07|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred. Estate workers/house guard moved on local crisis information; neither creation executed an attack on their final service-side position.|
|Outside: foresters-split14|1|P15-02|Outside at the terminal clock, still following an interrupted journey. Direct boundary experience discouraged another crossing. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: house-guard|1|P16-04|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred. Estate workers/house guard moved on local crisis information; neither creation executed an attack on their final service-side position.|
|Outside: old-Cottage_01|1|P10-06|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: old-Cottage_06-split8|1|P10-08|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: old-CrookedCottage|1|P10-03|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Direct boundary experience discouraged another crossing. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: smith-customer|1|P07-04|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: smith-pair|1|P07-01|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: stable-staff|1|P16-08|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred. Estate workers/house guard moved on local crisis information; neither creation executed an attack on their final service-side position.|
|Outside: stall-thief|1|P08-24|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: strip-workers|2|P01-04, P01-05|Outside at the terminal clock, holding at the last chosen local cover/waypoint. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: tavern-service-runners-split8|1|P09-02|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: upper-Cottage_11|1|P12-10|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: upper-SealedCellarCottage-split12|1|P12-05|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: upper-UpperCottage|1|P12-04|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: water-pair|2|P08-01, P08-02|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: west-EndRowCottage|2|P11-05, P11-06|Outside at the terminal clock, still following an interrupted journey. Bone had changed this person's movement, but no later completed intended hit reached them. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|Outside: west-home|1|P04-03|Outside at the terminal clock, holding at the last chosen local cover/waypoint. The Mayor's fixed death ends this primary ledger; no cleanup event is inferred.|
|RearCottage|1|P11-04|At RearCottage, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|SealedCellarCottage|1|P12-06|At SealedCellarCottage, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|UpperCottage|4|P08-26, P12-11, P12-12, P12-13|At UpperCottage, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|
|WeaverCottage|11|P06-01, P06-02, P06-03, P06-09, P06-10, P11-03, P11-07, P11-08, P11-11, P11-12, P11-14|At WeaverCottage, structural state 0. A probe reached this shelter; detection did not itself authorize a remote attack. No lethal executed attack intersected this person's final shelter/movement after their last relocation. The remaining roof/cover and separation from Blood's body retained protection.|

## Environmental evidence seeds

| Time | Event | Position | Future evidence / interrupted activity |
|---|---|---|---|
|+94.0|E040|(-34.3, 9.2)|Bone injure: Parent shifts to block the coop gap and child; Bone's existing torment escalates with a precise nonfatal strike against the shielding adult.|
|+98.0|E044|(3.0, 50.8)|Blood corridor: The visibly clustering rescuers lifting the four wounded form the strongest nearby outdoor concentration. Blood strikes that aid activity.|
|+102.0|E051|(-32.6, 3.7)|Bone kill: Parent continues putting themself between Bone and the child at the attempted doorway. Bone ends the shielding act with a deliberate precise hit.|
|+106.0|E062|(-34.0, 13.0)|Bone deny: Smith tries to keep a route open for the child. Bone breaks the wheel and blocks the narrow working-yard approach rather than repeating an empty threat.|
|+108.0|E066|(-36.4, 10.8)|Bone kill: The apprentice steps into view to distract Bone from the rescue route. Bone's intended hit is exact; the smith is left alive to react.|
|+110.0|E069|(6.3, 34.5)|Blood corridor: Blood attacks the refuge into which he saw porch people disappear and can hear urgent overlapping voices. He does not know its exact headcount.|
|+122.0|E087|(15.7, -52.8)|Bone kill: One returning witness turns back to wave others into the farm lane. Bone catches that exposed gesture; it is the first farm incident, not systematic barn clearance.|
|+126.0|E092|(11.3, -55.2)|Bone puncture: A rushed barn latch catches Bone's attention. He punctures the side and denies the obvious yard exit, exposing the refuge to sound and later probes.|
|+130.0|E100|(-73.9, 82.4)|Barrier contact: Worker physically tests the opaque boundary on a familiar work route; no previous V4 lethal-contact knowledge|
|+130.0|E102|(-58.1, -76.0)|Barrier contact: Worker physically tests the opaque boundary on a familiar work route; no previous V4 lethal-contact knowledge|
|+134.0|E108|(25.6, 53.3)|Blood corridor: The exposed porch group is now moving across Blood's view; he follows the broad movement rather than treating its previous shelter signal as erased.|
|+134.0|E112|(17.1, -49.3)|Bone kill: A yard adult emerging from the damaged barn turns to guide another household member. Bone targets that visible protective turn rather than clearing the storage interior.|
|+151.0|E156|(24.5, 24.5)|Bone puncture: At the lower refuge Bone hears several arrivals argue over closing the door. He punctures the latch side; this creates a sightline and changes cover.|
|+160.0|E172|(12.7, 18.2)|Bone injure: A receiving worker returning from the breached tavern now tries to guide others through a lower doorway. Bone precisely injures the guide rather than repeating the latch strike.|
|+166.0|E175|(15.5, 13.2)|Bone kill: One split household member emerges alone after rejecting the crowded shelter; Bone shifts to the exposed solitary dash beside his current position.|
|+168.0|E177|(-14.3, 58.0)|Blood corridor: Blood reaches the reacquired western concentration. The continuously connected threshold now pulses strongly after several neighbours entered, without revealing names or exact headcounts.|
|+174.0|E199|(37.8, 46.7)|Bone deny: Bone reaches the already-breached family cottage and appears at its broken west side. The caregiver sees that remaining beside the table no longer provides cover.|
|+176.0|E203|(-16.0, 55.0)|Blood corridor: Several people emerge together from the damaged western refuge while a coarse presence remains behind its breached face. Blood strikes the exposed doorway concentration he can now perceive.|
|+180.0|E210|(38.7, 57.6)|Bone kill: The caregiver stops and turns toward the pursuing creature while the children continue. Bone deliberately strikes the shielding adult, changing the group's ability to navigate.|
|+188.0|E246|(29.0, 73.0)|Bone threat: Bone deliberately reveals himself to this guard and strikes the ground beside his boots. Recognition is an emotional/fragmented-speech opportunity, not finished dialogue.|
|+196.0|E252|(25.0, 84.0)|Bone injure: As the guard reaches toward a helper at the entrance, Bone precisely injures the helper, deliberately leaving the recognized guard untouched.|
|+206.0|E258|(18.9, 87.0)|Bone kill: Bone lets the guard almost complete the lift, then deliberately kills the wounded helper beside the church access. The recognized guard is spared to understand the intent.|
|+212.0|E264|(13.5, 85.1)|Bone deny: Bone strikes a handrail beside the guard's chosen turn and cuts the direct line for a moment. The guard is allowed to choose the longer side of the junction.|
|+216.0|E267|(24.5, 24.5)|Blood corridor: Lower-house search branches remain strongly reactive despite partial dispersal; Blood has physically reached attack range and presses through its Bone-damaged frontage.|
|+230.0|E291|(-3.0, 111.0)|Bone threat: Bone deliberately strikes beside the retreating guard's weapon hand at the stair base; broken recognition sounds can refer to the old confrontation without clean exposition.|
|+238.0|E295|(-5.0, 110.0)|Bone kill: The service guard places himself in the line to cover his colleague's retreat. Bone kills this intervening protector precisely and deliberately spares the son-killer again.|
|+248.0|E315|(2.0, 124.0)|Bone deny: Bone deliberately breaks the gate latch the guard reaches for. He has allowed the retreat to almost reach protection and then removes that option.|
|+254.0|E318|(2.0, 124.0)|Bone kill: After the mobile recognition sequence, failed rescues and denied gate, Bone deliberately ends the entrance guard's life with one precise intended strike.|
|+258.0|E325|(11.3, -55.2)|Blood corridor: Blood reacquires the refuge into which he just watched the farm household evacuate. He has walked into range; secondary nodes do not deliver this attack.|
|+262.0|E339|(-12.0, 134.0)|Bone injure: The helper tries to place the stable worker behind the trough when Bone appears. Bone targets this protective gesture; the exploitative driver is already farther away and is not selected as a moral punishment.|
|+266.0|E344|(-21.5, -53.9)|Blood corridor: The western barn is a strong nearby physical network return with urgent overlapping warnings. Blood turns toward that concentration from his real farm position.|
|+272.0|E358|(-21.5, -53.9)|Blood corridor: After the first breach Blood still perceives overlapping movement and recent concentrated presence at the barn. A second pressure strike exploits the existing opening; it does not treat the wall as intact.|
|+280.0|E360|(-44.2, 176.2)|Barrier contact: The driver independently tries crossing the service-side boundary without having received a lethal-contact warning|
|+280.0|E363|(14.4, 97.8)|Bone kill: A centre traveller who fled several refuges looks back from the upper threshold. Bone has followed that actual moving silhouette and kills the exposed watcher.|
|+290.0|E388|(23.5, 86.4)|Bone puncture: The church door is being worked as people debate whether to stay or leave. Bone punctures its frame, making the public refuge less trustworthy.|
|+300.0|E395|(6.8, 92.3)|Bone kill: The caretaker holds the compromised public entrance for departing people. Bone escalates from the punctured door to a precise attack on that exposed act of assistance.|
|+314.0|E451|(48.6, 67.8)|Bone kill: A limping delivery survivor crosses the open gap below Bone while trying to reach the eastern refuge. The visible uneven movement captures his immediate attention.|
|+318.0|E456|(50.5, 74.0)|Bone puncture: The animal workers try to bar the crowded cottage entrance as probing blood thickens underneath. Bone punctures the shutter beside them to expose a new angle.|
|+324.0|E470|(50.5, 74.0)|Bone kill: One animal worker leans out to hold the damaged exit for a neighbour. Bone escalates from the shutter strike and precisely kills that exposed protector.|
|+332.0|E474|(68.2, 78.1)|Barrier contact: A displaced household/runner attempts an untested boundary section. Only local witnesses acquire direct B4.|
|+332.0|E476|(-65.9, 104.3)|Barrier contact: A displaced household/runner attempts an untested boundary section. Only local witnesses acquire direct B4.|
|+336.0|E478|(64.0, 85.0)|Bone kill: One boundary witness turns back to steady the other while withdrawing from the lethal sheet. Bone strikes that exposed helping gesture precisely.|
|+342.0|E483|(55.1, 54.4)|Blood corridor: Blood reaches the eastern concentration's new refuge doorway. Visible arrivals and a renewed local probe response let him reacquire broad presence without exact person tracking.|
|+348.0|E510|(23.5, 97.7)|Bone kill: A recent eastern escapee steps into the damaged public doorway as the entry argument breaks. Bone selects that visible movement, not an unseen interior headcount.|
|+358.0|E521|(23.5, 97.7)|Bone deny: At the church-side argument one western refugee tries to feint around the broken entrance. Bone deliberately denies that side and forces another immediate choice; this is not a missed intended hit.|
|+360.0|E524|(50.5, 74.0)|Blood corridor: Blood's body has now reached the northern-eastern concentration. The rage-amplified strike follows a physically connected live threshold and exploits prior Bone damage, without attacking remotely from a search node.|

Additional evidence: abandoned provisions cart at the service side; stolen stall pouch carried by P08-24; physically connected and later withdrawn search traces; threshold branching; surviving group disagreements; two natural Blood/Witch intersections. These are requirements only, not produced assets.

## Full chronological event ledger

Person-level deaths/injuries and witnesses are in casualties.csv; local knowledge entries are separate in the frozen JSON. The event ledger contains decisions as well as consequences.

| Time | ID | Type | Position | Event |
|---|---|---|---|---|
|+90.000|E001|ACTION|(-2.21, 44.52)|At blackout Blood attends to exposed well-side aid activity; Bone maintains his existing M05 fixation. Neither receives later knowledge.|
|+90.000|E002|REACTION||Blackout prompts local first intentions; no barrier contact or attacker identity is shared village-wide.|
|+90.000|E003|move|(-6, 50.5)|Neighbours reach already-visible injured stall users to lift them|
|+90.000|E004|move|(-3, 57)|Through travellers seek nearest vacant cottage cover|
|+90.000|E005|move|(8, 54)|Goods buyers edge away along east market lane|
|+90.000|E006|move|(-11, 52)|Caller warns nearest western household|
|+90.000|E007|move|(1.4, 42)|Porch patrons enter and warn customers about the visible public attack|
|+90.000|E008|move|(14.1, 30)|Receiving staff bring delivery hand inside service entrance|
|+90.000|E009|move|(-18, 35)|Water carriers avoid the assistant's attack position and move toward lower western homes|
|+90.000|E010|move|(-19, 18)|Household workers seek familiar nearby home|
|+90.000|E011|move|(13, 21)|Garden workers seek neighbours behind a closed door|
|+90.000|E012|move|(-1.53, -19.26)|Witnesses retreat toward farms carrying only their direct lower-lane warning|
|+90.000|E013|move|(5.8, -61.8)|Tool workers seek familiar barn cover and farm household|
|+90.000|E014|move|(17.5, -55.5)|Yard household calls children/relatives toward barn cover|
|+90.000|E015|move|(9.2, -36.3)|Orchard worker checks the already-warned farmhouse|
|+90.000|E016|move|(31, -35)|Strip workers follow access to farmyard, unaware of precise attackers|
|+90.000|E017|move|(-25.4, -51.3)|Tool workers seek storage shelter|
|+90.000|E018|move|(-27, -49)|Yard worker helps close barn doors|
|+90.000|E019|move|(-24.7, -59.8)|Storage pair gathers inside familiar barn|
|+90.000|E020|move|(-19.2, -59.6)|Keeper calls partner away from livestock toward household|
|+90.000|E021|move|(-19.2, -59.6)|Partner follows ordinary farm access to keeper|
|+90.000|E022|move|(-31.6, -77)|Field pair returns toward voices and pasture gate|
|+90.000|E023|move|(37.7, 51.9)|Caregiver takes four children into the family home|
|+90.000|E024|move|(29.7, 32)|Neighbours enter shared storage rather than exposed road|
|+90.000|E025|move|(29, 48.5)|Yard worker calls to nearest household|
|+90.000|E026|move|(27.5, 34.5)|Alley pair seeks neighbours through known household access|
|+90.000|E027|move|(22.6, 40.8)|Passers complete normal homeward destination now seeking shelter|
|+90.000|E028|move|(-22, 58.4)|Resident takes fuel indoors and warns household|
|+90.000|E029|move|(-35, 70)|Neighbours gather at familiar central western house|
|+90.000|E030|move|(-30, 52.5)|Trades pair retreats into workshop household|
|+90.000|E031|move|(-45, 72)|Neighbours return through shared yard, suspecting enclosure|
|+90.000|E032|move|(-47.01, 70.32)|Forest crew compares familiar trail with opaque sheet before choosing|
|+90.000|E033|move|(-19, 82)|Garden residents seek household and family|
|+90.000|E034|move|(-19.0, 96.9)|Returning resident calls uphill for ordinary guard help|
|+90.000|E035|move|(23.5, 83.7)|Caretaker goes to accessible bell rope to signal public emergency|
|+90.000|E036|move|(58, 65)|Animal workers seek nearby family shelter|
|+90.000|E037|move|(2, 125)|Entrance guard walks down formal stairs to inspect emergency and meet callers|
|+90.000|E038|move|(-22, 132)|Service guard checks paused provisions crew and outer access|
|+90.000|E039|Mayor|(2, 146)|Mayor demands a local report; house guard stays nearby while three staff listen at service side.|
|+94.000|E040|Bone|(-34.3, 9.2)|Parent shifts to block the coop gap and child; Bone's existing torment escalates with a precise nonfatal strike against the shielding adult.|
|+94.000|E041|REACTION||The parent tries the household rear access after injury; the smith reacts to a nearby human cry, not remote omniscience.|
|+94.000|E042|move|(-34.3, 9.2)|Wounded parent pulls child toward the household door|
|+94.000|E043|move|(-39.5, 11.7)|Smith and apprentice turn toward the child/parent cry|
|+98.000|E044|Blood|(3.0, 50.8)|The visibly clustering rescuers lifting the four wounded form the strongest nearby outdoor concentration. Blood strikes that aid activity.|
|+98.000|E045|REACTION||Witnesses recoil from the aid strike; occupants argue over opening the tavern and the cellar-side service exit.|
|+98.000|E046|move|(17.0, 51.0)|Surviving east-side goods buyers leave the impact junction by market lane|
|+98.000|E047|split|(-4.82, 56.68)|P08-24 separates to steal stall takings while companions seek cover; this is opportunistic intent, unlike locked-door fear.|
|+98.000|E048|move|(-4.82, 56.68)|Take abandoned stall takings for personal gain|
|+100.000|E049|Bell|(23.5, 86.4)|At the rope, caretaker makes the independent choice to ring after the second unmistakable crash. Signal means public emergency only.|
|+100.000|E050|move|(-37.5, 8.8)|Follow the wounded parent's dragging footfall toward the door, maintaining M05 fixation|
|+102.000|E051|Bone|(-32.55, 3.67)|Parent continues putting themself between Bone and the child at the attempted doorway. Bone ends the shielding act with a deliberate precise hit.|
|+102.000|E052|REACTION||The child scrambles into the alerted household. The three indoor relatives can witness the doorway event and draw the child inside.|
|+102.000|E053|move|(-32.55, 3.67)|Child reaches family cover after parent falls|
|+102.000|E054|move|(-33.51, 4.7)|The smith's approach toward the child catches attention; Bone shifts off the cottage facade|
|+102.000|E055|REACTION||The aid wave clipped the tavern corner at98. That earlier damage, visible now at the windows, triggers a shelter disagreement before the next strike.|
|+102.000|E056|split|(6.28, 34.48)|Three occupants choose the service-side exit; four prefer to stay low behind furniture.|
|+102.000|E057|move|(6.28, 34.48)|Leave the damaged tavern through service side toward lower family houses|
|+102.000|E058|move|(6.28, 34.48)|Receiving staff lead delivery hand along the familiar household service path|
|+102.000|E059|move|(13.37, 29.95)|Porch witnesses reject the interior after its wall is struck and seek the east-side passage|
|+102.000|E060|hold|(6.28, 34.48)|Four occupants stay silent behind surviving interior partitions, believing outside is more dangerous|
|+102.000|E061|move|(-2.21, 44.52)|Porch retreat, close shouting and a crowded doorway make the tavern the strongest plausible nearby concentration after the outdoor aid strike|
|+106.000|E062|Bone|(-34.0, 13.0)|Smith tries to keep a route open for the child. Bone breaks the wheel and blocks the narrow working-yard approach rather than repeating an empty threat.|
|+106.000|E063|REACTION||Smith and apprentice disagree over pursuing the child through the blocked yard; the apprentice steps out to distract the creature.|
|+106.000|E064|move|(-34.0, 13.0)|Smith tries to pull apprentice away from blocked rescue route|
|+106.000|E065|move|(-4.0, 106.0)|Caller has only general emergency knowledge; guard heads toward bell and public church approach to meet people|
|+108.000|E066|Bone|(-36.41, 10.84)|The apprentice steps into view to distract Bone from the rescue route. Bone's intended hit is exact; the smith is left alive to react.|
|+108.000|E067|REACTION||The smith abandons the unsafe rescue and withdraws west. This is fear and grief, not villainy.|
|+108.000|E068|move|(-36.41, 10.84)|Surviving smith withdraws from exact local threat into lower western yards|
|+110.000|E069|Blood|(6.3, 34.5)|Blood attacks the refuge into which he saw porch people disappear and can hear urgent overlapping voices. He does not know its exact headcount.|
|+110.000|E070|Witch immunity|(3.56, 46.42)|Blood divides around Witch on the unchanged main route; she does not flinch.|
|+110.000|E071|REACTION||First tavern wall breach changes the refuge. Staff urge the service exit; some customers insist that the open lanes are worse.|
|+110.000|E072|move|(-4.82, 56.68)|Visible stream at the vacant cottage gap prompts remaining travellers to leave via rear toward upper homes|
|+110.000|E073|hold|(-14.26, 58.05)|Household keeps door locked despite visible probing blood; fear of road dominates|
|+110.000|E074|move|(-14.26, 58.05)|Caller disagrees with staying beside the visible probing stream and seeks western neighbours|
|+110.000|E075|move|(2.0, -38.0)|Lower witnesses seek barn workers to warn them about the precise attacker, avoiding their original northward road|
|+110.000|E076|move|(-25.0, -61.0)|Keeper seeks tools and family at barn after public bell|
|+110.000|E077|move|(-25.0, -61.0)|Partner chooses farmhouse relatives instead of barn group|
|+110.000|E078|move|(-27.0, -65.0)|One pair doubts village cover and considers their familiar western field edge|
|+110.000|E079|move|(-35.0, 13.0)|Lower-road warning voices and rapid movement draw Bone away from the now-repetitive forge scene; he crosses the lower district at burst speed|
|+116.000|E080|REACTION||Physical search at Cottage01 prompts disagreement: household holds familiar interior; three passers choose relatives farther east.|
|+116.000|E081|move|(20.28, 36.89)|Passers leave a probing threshold toward familiar family voices in the next yard|
|+116.000|E082|hold|(20.28, 36.89)|Household stays low in familiar rooms despite the blood at door, unwilling to cross exposed lanes|
|+116.000|E083|move|(-1.0, 43.0)|Connected dense Cottage01 signal outranks weak nearby probes; retain coarse memory when some occupants move east|
|+116.000|E084|move|(-6.12, -26.55)|Four people calling warnings and moving toward the eastern barn are a stronger novel stimulus than abandoned forge cover|
|+116.000|E085|move|(-53.0, 71.0)|Try familiar working edge because the woods might still offer a way out; barrier behaviour untested|
|+116.000|E086|move|(-38.23, -67.11)|Try familiar working edge because the woods might still offer a way out; barrier behaviour untested|
|+122.000|E087|Bone|(15.74, -52.8)|One returning witness turns back to wave others into the farm lane. Bone catches that exposed gesture; it is the first farm incident, not systematic barn clearance.|
|+122.000|E088|REACTION||Barn workers hear the near warning cut short; witnesses flee toward the barn while a field worker chooses the farmhouse.|
|+122.000|E089|move|(15.74, -52.8)|Three surviving witnesses run for the barn workers they were trying to warn|
|+122.000|E090|move|(18.0, -47.0)|Strip workers choose the farmhouse instead of the noisy barn threshold|
|+122.000|E091|move|(4.0, -49.0)|The barn door begins closing over returning witnesses; Bone circles to its side rather than following the same footsteps|
|+126.000|E092|Bone|(11.3, -55.2)|A rushed barn latch catches Bone's attention. He punctures the side and denies the obvious yard exit, exposing the refuge to sound and later probes.|
|+126.000|E093|REACTION||People inside the barn disagree over remaining together after the side is punctured. Original yard workers favour the farmhouse; tool workers fear crossing the lane.|
|+126.000|E094|move|(11.3, -55.2)|Yard household chooses nearby family home after the barn is punctured|
|+126.000|E095|hold|(11.3, -55.2)|Tool workers keep low behind barn storage, believing movement outside attracts the fast creature|
|+130.000|E096|REACTION||Tavern porch escapees see Blood arriving beside their east-side route and keep moving north-east. Lower service escapees enter the nearest occupied household.|
|+130.000|E097|move|(18.0, 47.0)|Porch escapees veer along market lane as Blood approaches their paused junction|
|+130.000|E098|move|(23.0, 18.0)|Seek the nearby occupied household after leaving the damaged tavern|
|+130.000|E099|move|(23.0, 18.0)|Seek the nearby occupied household after leaving the damaged tavern|
|+130.000|E100|Barrier|(-73.9, 82.42)|Worker physically tests the opaque boundary on a familiar work route; no previous V4 lethal-contact knowledge|
|+130.000|E101|move|(-73.9, 82.42)|Surviving witness recoils to warn nearby workers after a local lethal boundary response|
|+130.000|E102|Barrier|(-58.12, -75.97)|Worker physically tests the opaque boundary on a familiar work route; no previous V4 lethal-contact knowledge|
|+130.000|E103|move|(-58.12, -75.97)|Surviving witness recoils to warn nearby workers after a local lethal boundary response|
|+130.000|E104|move|(-4.0, 100.0)|Follow guard toward public help at the church|
|+130.000|E105|move|(-10.56, 91.48)|Household chooses familiar public church after bell and nearby calls; knows only emergency|
|+130.000|E106|move|(1.81, 88.77)|Household chooses familiar public church after bell and nearby calls; knows only emergency|
|+130.000|E107|move|(-31.0, 147.0)|Service guard closes last distance to question delivery crew directly|
|+134.000|E108|Blood|(25.65, 53.3)|The exposed porch group is now moving across Blood's view; he follows the broad movement rather than treating its previous shelter signal as erased.|
|+134.000|E109|Witch immunity|(28.54, 53.84)|Blood divides around Witch on the unchanged main route; she does not flinch.|
|+134.000|E110|REACTION||The new east-lane strike drives nearby goods buyers and households away from the junction; knowledge stays with local witnesses.|
|+134.000|E111|move|(6.0, 54.0)|Opportunist abandons taking more coins and flees carrying the stolen pouch|
|+134.000|E112|Bone|(17.12, -49.31)|A yard adult emerging from the damaged barn turns to guide another household member. Bone targets that visible protective turn rather than clearing the storage interior.|
|+134.000|E113|REACTION||Remaining yard workers accelerate toward the farmhouse. The barn stayers hear the attack and remain behind storage.|
|+134.000|E114|move|(17.12, -49.31)|Surviving yard household rushes to relatives after the exposed helper is struck|
|+134.000|E115|move|(18.0, -52.0)|Human shouts moving away from the tavern toward the lower houses are new; Bone abandons the repetitive barn door and makes a long return burst|
|+142.000|E116|ACTION||Blood compares coarse current network returns: western shared household is strong; nearby cottages now only several/empty. He commits to a deliberate cross-centre relocation.|
|+142.000|E117|move|(14.0, 49.0)|Strong connected western shared-household presence outweighs weak nearby thresholds; cross-centre relocation|
|+142.000|E118|REACTION||Pending probe and wall information prompts household-specific choices, with stays and disagreements preserved.|
|+142.000|E119|hold|(11.3, -55.2)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+142.000|E120|shelter decision|(11.3, -55.2)|Household elects silence rather than automatic flight|
|+142.000|E121|move|(2.8, 21.22)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E122|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E123|move|(-9.62, 26.77)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E124|move|(-9.62, 26.77)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E125|move|(2.8, 21.22)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E126|split|(37.8, 46.73)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+142.000|E127|hold|(37.8, 46.73)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+142.000|E128|move|(37.8, 46.73)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E129|move|(20.28, 36.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E130|move|(37.8, 46.73)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E131|move|(26.73, 42.37)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E132|move|(31.7, 29.3)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E133|hold|(37.8, 46.73)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+142.000|E134|shelter decision|(37.8, 46.73)|Household elects silence rather than automatic flight|
|+142.000|E135|move|(26.73, 42.37)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E136|move|(-27.88, 61.19)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E137|hold|(-14.26, 58.05)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+142.000|E138|shelter decision|(-14.26, 58.05)|Household elects silence rather than automatic flight|
|+142.000|E139|move|(-37.9, 50.76)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E140|move|(-28.7, 47.74)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E141|move|(-27.88, 61.19)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E142|move|(-27.88, 61.19)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E143|hold|(-37.9, 50.76)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+142.000|E144|shelter decision|(-37.9, 50.76)|Household elects silence rather than automatic flight|
|+142.000|E145|split|(7.29, 70.89)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+142.000|E146|hold|(7.29, 70.89)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+142.000|E147|move|(7.29, 70.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+142.000|E148|hold|(-10.56, 91.48)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+142.000|E149|shelter decision|(-10.56, 91.48)|Household elects silence rather than automatic flight|
|+146.000|E150|opportunist|(-41.34, 155.6)|P17-01 demands valuables for a place on the provisions cart, despite no known usable escape; helper objects. This exploits fear for gain.|
|+146.000|E151|split|(-41.34, 155.6)|Delivery helper refuses the driver's demand and goes to speak to the service guard.|
|+146.000|E152|move|(-41.34, 155.6)|Driver takes provisions cart toward service grounds while trying to monopolize its space|
|+146.000|E153|move|(-41.34, 155.6)|Helper walks down to service access after refusing to exploit frightened people|
|+146.000|E154|move|(-41.34, 155.6)|Service guard returns to access with only visual enclosure report; no B4 knowledge|
|+148.000|E155|move|(23.0, 17.0)|Overlapping voices and the lower cottage's hastily closing door attract Bone after his long farm-to-lower burst|
|+151.000|E156|Bone|(24.52, 24.47)|At the lower refuge Bone hears several arrivals argue over closing the door. He punctures the latch side; this creates a sightline and changes cover.|
|+151.000|E157|REACTION||The crowded lower house now has a precise puncture as well as search pressure. Occupants disagree about which side is safe.|
|+151.000|E158|hold|(6.28, 34.48)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+151.000|E159|shelter decision|(6.28, 34.48)|Household elects silence rather than automatic flight|
|+151.000|E160|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+151.000|E161|split|(24.52, 24.47)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+151.000|E162|hold|(24.52, 24.47)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+151.000|E163|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+151.000|E164|hold|(24.52, 24.47)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+151.000|E165|shelter decision|(24.52, 24.47)|Household elects silence rather than automatic flight|
|+151.000|E166|split|(24.52, 24.47)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+151.000|E167|hold|(24.52, 24.47)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+151.000|E168|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+151.000|E169|move|(-53.0, 71.0)|Forest survivors seek nearby neighbours to deliver the warning in person|
|+160.000|E170|ACTION||Connected Cottage02 probe has strengthened after arrivals while CrushedHome disperses. Blood retains the western concentration interest and follows the nearby stronger return.|
|+160.000|E171|move|(-15.06, 49.34)|Reacquire the western group through a strengthened adjacent threshold signal; no exact individual tracking|
|+160.000|E172|Bone|(12.67, 18.2)|A receiving worker returning from the breached tavern now tries to guide others through a lower doorway. Bone precisely injures the guide rather than repeating the latch strike.|
|+160.000|E173|REACTION||Lower-house escapees change pace and call for help; Bone can respond to those actual sounds.|
|+160.000|E174|move|(12.67, 18.2)|Remaining delivery pair tries to get the injured guide inside|
|+166.000|E175|Bone|(15.45, 13.18)|One split household member emerges alone after rejecting the crowded shelter; Bone shifts to the exposed solitary dash beside his current position.|
|+166.000|E176|move|(31.0, 22.0)|Visible pulsing search branches uphill and escaping household voices offer a new district stimulus; Bone leaves the repeat lower-door encounter|
|+168.000|E177|Blood|(-14.26, 58.05)|Blood reaches the reacquired western concentration. The continuously connected threshold now pulses strongly after several neighbours entered, without revealing names or exact headcounts.|
|+168.000|E178|REACTION||Pressure opens the previously intact cottage face. Original residents and refugees reassess different risks; nearby western homes hear the impact.|
|+168.000|E179|hold|(-9.62, 26.77)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+168.000|E180|shelter decision|(-9.62, 26.77)|Household elects silence rather than automatic flight|
|+168.000|E181|hold|(-9.62, 26.77)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+168.000|E182|shelter decision|(-9.62, 26.77)|Household elects silence rather than automatic flight|
|+168.000|E183|hold|(24.52, 24.47)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+168.000|E184|shelter decision|(24.52, 24.47)|Household elects silence rather than automatic flight|
|+168.000|E185|split|(-14.26, 58.05)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+168.000|E186|hold|(-14.26, 58.05)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+168.000|E187|move|(-14.26, 58.05)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E188|move|(-14.26, 58.05)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E189|split|(-27.88, 61.19)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+168.000|E190|hold|(-27.88, 61.19)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+168.000|E191|move|(-27.88, 61.19)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E192|move|(-14.26, 58.05)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E193|split|(-14.26, 58.05)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+168.000|E194|hold|(-14.26, 58.05)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+168.000|E195|move|(-14.26, 58.05)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E196|move|(-11.77, 71.76)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E197|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+168.000|E198|move|(6.28, 34.48)|Injured last tavern occupant tries service exit after hearing renewed attacks and losing usable cover|
|+174.000|E199|Bone|(37.8, 46.73)|Bone reaches the already-breached family cottage and appears at its broken west side. The caregiver sees that remaining beside the table no longer provides cover.|
|+174.000|E200|REACTION||Caregiver takes the children toward the public bell and visible church route; passers choose the eastern houses instead.|
|+174.000|E201|move|(37.8, 46.73)|Caregiver keeps the children together toward public help at church|
|+174.000|E202|move|(37.8, 46.73)|Two passers choose familiar eastern household instead of the northward caregiver route|
|+176.000|E203|Blood|(-16.0, 55.0)|Several people emerge together from the damaged western refuge while a coarse presence remains behind its breached face. Blood strikes the exposed doorway concentration he can now perceive.|
|+176.000|E204|REACTION||Surviving western neighbours reconsider both damaged houses; nearby intact western homes become more attractive than the central road.|
|+176.000|E205|split|(15.45, 13.18)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+176.000|E206|hold|(15.45, 13.18)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+176.000|E207|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+176.000|E208|move|(-27.88, 61.19)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+176.000|E209|move|(34.0, 48.0)|Bone follows the caregiver's protective turn after forcing the family out; the repeated empty cottage is already losing interest|
|+180.000|E210|Bone|(38.67, 57.63)|The caregiver stops and turns toward the pursuing creature while the children continue. Bone deliberately strikes the shielding adult, changing the group's ability to navigate.|
|+180.000|E211|REACTION||The children keep running along the already-selected churchward direction; they have no new global safety knowledge.|
|+180.000|E212|move|(38.67, 57.63)|Children continue toward bell and a visible uniformed adult at the public approach|
|+180.000|E213|move|(23.5, 82.0)|Guard sees/hears children approaching the open public route and goes to receive them|
|+184.000|E214|hold|(-20.0, 51.0)|Gather accessible recent western blood while assessing changed network returns; no exact survivor census|
|+184.000|E215|move|(-20.0, 51.0)|The connected lower-house threshold now reports a substantial concentration, stronger than the dispersed western pocket. Blood makes a deliberate long relocation across the village|
|+184.000|E216|REACTION||Blood's departure does not tell western survivors that routes are safe. Search pressure continues from secondary nodes while his body moves.|
|+184.000|E217|hold|(-9.62, 26.77)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E218|shelter decision|(-9.62, 26.77)|Household elects silence rather than automatic flight|
|+184.000|E219|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E220|hold|(-9.62, 26.77)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E221|shelter decision|(-9.62, 26.77)|Household elects silence rather than automatic flight|
|+184.000|E222|split|(15.45, 13.18)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+184.000|E223|hold|(15.45, 13.18)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+184.000|E224|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E225|hold|(24.52, 24.47)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E226|shelter decision|(24.52, 24.47)|Household elects silence rather than automatic flight|
|+184.000|E227|split|(24.52, 24.47)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+184.000|E228|hold|(24.52, 24.47)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+184.000|E229|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E230|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E231|hold|(24.52, 24.47)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E232|shelter decision|(24.52, 24.47)|Household elects silence rather than automatic flight|
|+184.000|E233|hold|(24.52, 24.47)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E234|shelter decision|(24.52, 24.47)|Household elects silence rather than automatic flight|
|+184.000|E235|hold|(-37.9, 50.76)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E236|shelter decision|(-37.9, 50.76)|Household elects silence rather than automatic flight|
|+184.000|E237|move|(7.29, 70.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E238|hold|(-10.56, 91.48)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+184.000|E239|shelter decision|(-10.56, 91.48)|Household elects silence rather than automatic flight|
|+184.000|E240|split|(24.52, 24.47)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+184.000|E241|hold|(24.52, 24.47)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+184.000|E242|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E243|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+184.000|E244|move|(38.0, 58.0)|The fleeing children reach a uniformed adult who turns toward them; this new protective gesture pulls Bone along the churchward route|
|+188.000|E245|Guard recognition|(29.0, 73.0)|At close range Bone recognizes the entrance guard as the son's killer. The deliberate attention changes; he does not immediately kill the guard.|
|+188.000|E246|Bone|(29.0, 73.0)|Bone deliberately reveals himself to this guard and strikes the ground beside his boots. Recognition is an emotional/fragmented-speech opportunity, not finished dialogue.|
|+188.000|E247|REACTION||Guard tries to put the children behind him and backs toward the church entrance. He sees deliberate personal interest but has no complete explanation.|
|+188.000|E248|move|(29.0, 73.0)|Guard escorts children toward the public entrance while keeping himself between them and Bone|
|+188.000|E249|move|(28.82, 73.04)|Children follow the guard's local protection to church|
|+188.000|E250|move|(23.5, 82.0)|Upper returner approaches to help hold the entrance for the children|
|+194.000|E251|move|(29.0, 72.0)|Bone changes angle along the church approach instead of striking the guard; he watches the guard attempt a rescue|
|+196.000|E252|Bone|(25.0, 84.0)|As the guard reaches toward a helper at the entrance, Bone precisely injures the helper, deliberately leaving the recognized guard untouched.|
|+196.000|E253|REACTION||Guard now has to choose between shielding the children and helping the wounded adult. Caretaker opens the ordinary public entrance and urges people inside.|
|+196.000|E254|move|(23.81, 84.15)|Children take the opened public doorway while guard turns toward wounded helper|
|+196.000|E255|move|(23.89, 83.22)|Guard refuses to leave the injured helper exposed; he tries to lift them toward the doorway|
|+196.000|E256|move|(25.0, 84.0)|Wounded helper tries to reach the church with guard assistance|
|+202.000|E257|REACTION||Church occupants debate admitting more people after hearing the precise strike. Caretaker continues admitting the nearby children; guard attempts to recover the helper rather than abandoning them.|
|+206.000|E258|Bone|(18.91, 86.98)|Bone lets the guard almost complete the lift, then deliberately kills the wounded helper beside the church access. The recognized guard is spared to understand the intent.|
|+206.000|E259|REACTION||Guard realizes this creature is singling him out. He calls the children farther inside and retreats toward the upper road to draw it away from the doorway.|
|+206.000|E260|move|(25.0, 84.0)|Guard tries to draw Bone away from the crowded church toward the formal estate route|
|+206.000|E261|hold|(23.5, 86.4)|Caretaker stops ringing to help people inside and keep the entrance open; bell conveyed emergency only|
|+206.000|E262|Bell|(23.5, 86.4)|Bell ringing ceases while the caretaker assists arrivals; silence is not an all-clear.|
|+206.000|E263|move|(29.0, 84.0)|Bone allows the recognized guard's retreat, then shifts ahead along the upper junction instead of immediately killing him|
|+212.000|E264|Bone|(13.54, 85.05)|Bone strikes a handrail beside the guard's chosen turn and cuts the direct line for a moment. The guard is allowed to choose the longer side of the junction.|
|+212.000|E265|REACTION||Guard changes the immediate angle while keeping his attempt to draw the creature away from the church.|
|+212.000|E266|move|(13.54, 85.05)|Guard takes the open side of the upper junction toward the formal staircase|
|+216.000|E267|Blood|(24.5, 24.5)|Lower-house search branches remain strongly reactive despite partial dispersal; Blood has physically reached attack range and presses through its Bone-damaged frontage.|
|+216.000|E268|hold|(5.49, 16.34)|Recover and draw on the new accessible blood at the lower refuge; body remains slow|
|+216.000|E269|REACTION||The previously punctured refuge loses protective value. Those still able to move reassess cover rather than being treated as removed from the simulation.|
|+216.000|E270|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E271|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E272|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E273|move|(24.52, 24.47)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E274|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E275|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E276|hold|(7.29, 70.89)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+216.000|E277|shelter decision|(7.29, 70.89)|Household elects silence rather than automatic flight|
|+216.000|E278|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E279|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E280|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+216.000|E281|move|(15.45, 13.18)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+222.000|E282|ACTION||Local lower refuges have dispersed; Blood lets connected probes explore unresolved farm and upper frontiers rather than repeatedly hitting empty walls.|
|+222.000|E283|REACTION||Centre travellers now choose a known upper home; the thief separates from public movement to conceal stolen goods. The surviving field witness leaves the boundary vicinity to warn the barn.|
|+222.000|E284|move|(-8.0, 66.0)|Seek a quieter known upper household after pausing to orient in the dark|
|+222.000|E285|move|(22.0, 61.0)|Opportunist seeks eastern shelter while concealing the stolen pouch|
|+222.000|E286|move|(-34.0, -67.0)|Shaken direct B4 witness goes to warn farm workers in person|
|+222.000|E287|move|(16.0, 87.0)|Bone overtakes the recognized guard along the upper route and takes a position at the first stair approach|
|+222.000|E288|move|(-22.0, 132.0)|Service guard sees the entrance guard retreating under pressure and comes down to assist, without inheriting his historical guilt|
|+222.000|E289|move|(-1.09, 98.56)|Entrance guard takes the formal steps toward assistance while Bone repeatedly changes angle|
|+226.000|E290|move|(5.49, 16.34)|Newly connected eastern farmhouse gives a substantial remote presence signal; it outweighs the dispersed lower thresholds. Blood walks down the approach|
|+230.000|E291|Bone|(-3.0, 111.0)|Bone deliberately strikes beside the retreating guard's weapon hand at the stair base; broken recognition sounds can refer to the old confrontation without clean exposition.|
|+230.000|E292|REACTION||The guard knows this is personal and calls to the approaching service guard for help. The service guard chooses to intervene rather than hold the estate.|
|+230.000|E293|move|(-3.0, 111.0)|Entrance guard continues up the landing while trying to keep the service guard in sight|
|+236.000|E294|move|(-3.0, 102.0)|Bone steps between the two guards' lines, keeping the recognized guard alive while the other attempts protection|
|+238.000|E295|Bone|(-5.0, 110.0)|The service guard places himself in the line to cover his colleague's retreat. Bone kills this intervening protector precisely and deliberately spares the son-killer again.|
|+238.000|E296|REACTION||Entrance guard retreats toward the controlled estate entrance, now deprived of the colleague who came to help. No other guard is assigned historical guilt.|
|+238.000|E297|move|(-3.0, 116.0)|Guard reaches for the formal gate after his assisting colleague is killed|
|+238.000|E298|hold|(10.71, -44.82)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+238.000|E299|shelter decision|(10.71, -44.82)|Household elects silence rather than automatic flight|
|+238.000|E300|move|(10.71, -44.82)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+238.000|E301|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+238.000|E302|move|(10.71, -44.82)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+238.000|E303|move|(10.71, -44.82)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+238.000|E304|split|(-20.0, -42.89)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+238.000|E305|hold|(-20.0, -42.89)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+238.000|E306|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+238.000|E307|move|(7.29, 70.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+238.000|E308|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+242.000|E309|REACTION||Eastern farmhouse evacuees see the slow figure on the approach and turn toward barn cover. Their earlier decision came from the visible probe, not knowledge of Blood's body.|
|+242.000|E310|move|(15.76, -41.46)|Turn toward familiar barn after seeing Blood approaching the farmyard|
|+242.000|E311|move|(15.76, -41.46)|Turn toward familiar barn after seeing Blood approaching the farmyard|
|+242.000|E312|move|(15.76, -41.46)|Turn toward familiar barn after seeing Blood approaching the farmyard|
|+242.000|E313|move|(-1.36, -8.58)|Continue down the approach toward the observed farm movement; major attack still requires body range|
|+242.000|E314|move|(-4.0, 113.0)|Bone follows the recognized guard to the controlled entrance, ending the long church-to-stairs pursuit|
|+248.000|E315|Bone|(2.0, 124.0)|Bone deliberately breaks the gate latch the guard reaches for. He has allowed the retreat to almost reach protection and then removes that option.|
|+248.000|E316|REACTION||Guard gives up forcing the latch and turns to face the creature. He calls toward the approaching bereaved woman, who continues uphill without helping or explaining.|
|+248.000|E317|Witch civilian interaction|(-13.94, 104.33)|Guard calls toward the Witch from the upper entrance. She continues on the saved route and does not respond meaningfully.|
|+254.000|E318|Bone|(2.0, 124.0)|After the mobile recognition sequence, failed rescues and denied gate, Bone deliberately ends the entrance guard's life with one precise intended strike.|
|+254.000|E319|Guard sequence ends|(2.0, 124.0)|Recognition at188 to final death254: 66 seconds, moving from church approach through upper junction and formal staircase. Fragmented memory opportunities reserved; no finished dialogue.|
|+254.000|E320|REACTION||Service-yard workers see the guard fall near the entrance. House guard closes the mansion front to protect the Mayor; this does not confer knowledge of all village events.|
|+254.000|E321|move|(-24.0, 132.0)|Driver abandons the provisions cart to try the service-side forest gap; knows confinement only, not lethal contact|
|+254.000|E322|move|(-22.0, 132.0)|Helper goes toward stable worker to warn them instead of following driver|
|+254.000|E323|move|(-11.5, 135.5)|Stable worker approaches the warning helper|
|+254.000|E324|move|(4.0, 125.0)|Abandoned cart and workers arguing at service side interrupt Bone's finished guard fixation; he crosses the grounds toward the new sound|
|+258.000|E325|Blood|(11.3, -55.2)|Blood reacquires the refuge into which he just watched the farm household evacuate. He has walked into range; secondary nodes do not deliver this attack.|
|+258.000|E326|hold|(-0.03, -34.48)|Gather spilled blood at the barn approach and assess remaining farm noise|
|+258.000|E327|REACTION||Nearby barn occupants hear the yard impact. Some fear the boundary, others only know the immediate farm danger.|
|+258.000|E328|move|(11.3, -55.2)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E329|move|(10.71, -44.82)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E330|move|(11.3, -55.2)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E331|move|(11.3, -55.2)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E332|move|(11.3, -55.2)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E333|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E334|split|(37.62, 33.04)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+258.000|E335|hold|(37.62, 33.04)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+258.000|E336|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E337|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+258.000|E338|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+262.000|E339|Bone|(-12.0, 134.0)|The helper tries to place the stable worker behind the trough when Bone appears. Bone targets this protective gesture; the exploitative driver is already farther away and is not selected as a moral punishment.|
|+262.000|E340|REACTION||Stable worker tries to support the injured helper. Mansion staff hear the nearby cry and approach the service side while the house guard remains with the Mayor.|
|+262.000|E341|move|(-12.0, 134.0)|Wounded helper tries to get behind stable-side cover with assistance|
|+262.000|E342|move|(-12.0, 134.0)|Stable worker supports injured helper|
|+262.000|E343|move|(-8, 144)|Domestic staff approach nearby injured workers to offer help; they have only local service-yard knowledge|
|+266.000|E344|Blood|(-21.5, -53.9)|The western barn is a strong nearby physical network return with urgent overlapping warnings. Blood turns toward that concentration from his real farm position.|
|+266.000|E345|REACTION||The western barn's first wall breach forces a decision. A direct B4 witness can warn these occupants, but villagers at other refuges do not inherit that warning.|
|+266.000|E346|move|(-21.5, -53.9)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E347|move|(-21.5, -53.9)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E348|move|(-21.5, -53.9)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E349|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E350|move|(-21.5, -53.9)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E351|move|(-21.5, -53.9)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E352|move|(-10.56, 91.48)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E353|split|(-42.56, 95.81)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+266.000|E354|hold|(-42.56, 95.81)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+266.000|E355|move|(-42.56, 95.81)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+266.000|E356|move|(-33.05, 156.68)|Driver tries the apparent forest-side opening after abandoning cart; he has seen the sheet but has no lethal-contact warning|
|+266.000|E357|move|(-17.0, 134.0)|New movement across the upper western approach is more novel than the service-yard cowering. Bone makes a long lateral relocation to investigate|
|+272.000|E358|Blood|(-21.5, -53.9)|After the first breach Blood still perceives overlapping movement and recent concentrated presence at the barn. A second pressure strike exploits the existing opening; it does not treat the wall as intact.|
|+272.000|E359|REACTION||Remaining farm witnesses move according to their own boundary knowledge. Barrier-aware occupants avoid it; unbriefed eastern residents may still consider an edge.|
|+280.000|E360|Barrier|(-44.2, 176.23)|The driver independently tries crossing the service-side boundary without having received a lethal-contact warning|
|+280.000|E361|ACTION||Many nearby probes now return only modest, faint or dispersed presence while unresolved frontiers remain. Blood reallocates capacity away from prolonged modest returns; their last observations remain coarse memory, not live sensors.|
|+280.000|E362|move|(-0.03, -34.48)|Recent strong upper refuge memory and unresolved upper streets outweigh weak farm remnants; Blood begins a long climb back through the western village|
|+280.000|E363|Bone|(14.45, 97.79)|A centre traveller who fled several refuges looks back from the upper threshold. Bone has followed that actual moving silhouette and kills the exposed watcher.|
|+280.000|E364|REACTION||The surviving travellers break from the upper doorway. One chooses a familiar western edge, another seeks public church cover.|
|+280.000|E365|split|(14.45, 97.79)|The travellers disagree over the bell refuge versus the apparently open western side.|
|+280.000|E366|move|(14.45, 97.79)|Try the western woodland edge without having received the foresters' lethal-contact report|
|+280.000|E367|move|(14.45, 97.79)|Remaining centre travellers choose public refuge after local attack|
|+286.000|E368|move|(-5.78, 91.66)|New human movement across the church approach and a physically gathering blood probe offer an active stimulus; Bone changes angle across the upper district|
|+290.000|E369|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E370|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E371|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E372|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E373|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E374|split|(55.2, 52.91)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+290.000|E375|hold|(55.2, 52.91)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+290.000|E376|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E377|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E378|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E379|hold|(23.5, 97.66)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+290.000|E380|shelter decision|(23.5, 97.66)|Household elects silence rather than automatic flight|
|+290.000|E381|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E382|move|(1.81, 88.77)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E383|move|(23.5, 86.4)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E384|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E385|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E386|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E387|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+290.000|E388|Bone|(23.5, 86.4)|The church door is being worked as people debate whether to stay or leave. Bone punctures its frame, making the public refuge less trustworthy.|
|+290.000|E389|REACTION||Religious refuge occupants reassess a visible search and damaged entrance. Fearful disagreement is not treated as moral guilt.|
|+290.000|E390|split|(23.5, 97.66)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+290.000|E391|hold|(23.5, 97.66)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+290.000|E392|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+300.000|E393|ACTION||A newly reached eastern refuge produces a very strong physical search response. Blood abandons the fading upper-memory destination and commits toward the stronger distant eastern concentration.|
|+300.000|E394|move|(-17.0, -7.71)|Strong live eastern refuge signal outweighs modest upper memory; Blood must cross the village physically before attacking|
|+300.000|E395|Bone|(6.81, 92.3)|The caretaker holds the compromised public entrance for departing people. Bone escalates from the punctured door to a precise attack on that exposed act of assistance.|
|+300.000|E396|REACTION||Church occupants no longer have their guide at the entrance. Some stay deeper; others continue the already chosen outward routes.|
|+300.000|E397|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+300.000|E398|split|(-41.23, 38.28)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+300.000|E399|hold|(-41.23, 38.28)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+300.000|E400|move|(-41.23, 38.28)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+300.000|E401|move|(-41.23, 38.28)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+300.000|E402|hold|(50.51, 74.04)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+300.000|E403|shelter decision|(50.51, 74.04)|Household elects silence rather than automatic flight|
|+300.000|E404|hold|(50.51, 74.04)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+300.000|E405|shelter decision|(50.51, 74.04)|Household elects silence rather than automatic flight|
|+300.000|E406|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+300.000|E407|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+300.000|E408|hold|(55.2, 52.91)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+300.000|E409|shelter decision|(55.2, 52.91)|Household elects silence rather than automatic flight|
|+306.001|E410|Witch arrival|(2, 146)|Witch completes the recalculated237.6006m remaining 3D route at1.1m/s and reaches the Mayor. She secures him here; exact restraint choreography remains reserved.|
|+306.001|E411|Mayor confrontation|(2, 146)|Approximately60-second private confrontation begins. Subjects: lover, son, misuse of authority, failure to stop the original violence, village suffering outside, his helplessness and her decision to save him until last. No finished dialogue; no survivor-count awareness.|
|+306.001|E412|REACTION||House guard sees the Mayor secured and withdraws through the service side, overwhelmed after losing the other guards. Staff remain with the injured workers outside; no one gains global knowledge.|
|+306.001|E413|move|(1, 139)|House guard withdraws to service workers after Mayor is secured; fear replaces ability to protect authority|
|+306.001|E414|move|(18.0, 84.0)|The eastern search branch is visibly gathering near a refuge, with new departing voices. Bone makes a sharp church-to-eastern relocation to investigate|
|+306.001|E415|Amplification|(-16.72, 2.01)|Witch's rage adds bounded local amplification to Blood's already accumulated resource. Body speed stays1.7019m/s; connected nodes and probes intensify.|
|+312.000|E416|REACTION||Existing connected shelters receive the visible intensification as new local information; isolated unconnected homes do not.|
|+312.000|E417|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E418|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E419|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E420|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E421|move|(-27.42, 5.27)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E422|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E423|move|(-27.42, 5.27)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E424|move|(-27.42, 5.27)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E425|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E426|split|(55.2, 52.91)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+312.000|E427|hold|(55.2, 52.91)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+312.000|E428|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E429|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E430|split|(-45.35, 62.59)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+312.000|E431|hold|(-45.35, 62.59)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+312.000|E432|move|(-45.35, 62.59)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E433|move|(-48.82, 77.14)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E434|move|(-28.7, 47.74)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E435|move|(-28.7, 47.74)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E436|hold|(-48.82, 77.14)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+312.000|E437|shelter decision|(-48.82, 77.14)|Household elects silence rather than automatic flight|
|+312.000|E438|hold|(50.51, 74.04)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+312.000|E439|shelter decision|(50.51, 74.04)|Household elects silence rather than automatic flight|
|+312.000|E440|hold|(50.51, 74.04)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+312.000|E441|shelter decision|(50.51, 74.04)|Household elects silence rather than automatic flight|
|+312.000|E442|split|(-48.82, 77.14)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+312.000|E443|hold|(-48.82, 77.14)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+312.000|E444|move|(-48.82, 77.14)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E445|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E446|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E447|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+312.000|E448|hold|(55.2, 52.91)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+312.000|E449|shelter decision|(55.2, 52.91)|Household elects silence rather than automatic flight|
|+312.000|E450|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+314.000|E451|Bone|(48.56, 67.78)|A limping delivery survivor crosses the open gap below Bone while trying to reach the eastern refuge. The visible uneven movement captures his immediate attention.|
|+314.000|E452|REACTION||The two nearby separate escapees see the precise interception and hurry toward the occupied doorway; this is local knowledge, not a village broadcast.|
|+314.000|E453|move|(48.56, 67.78)|Seek the occupied eastern house after seeing a nearby limping refugee struck|
|+314.000|E454|move|(48.56, 67.78)|Seek the occupied eastern house after seeing a nearby limping refugee struck|
|+314.000|E455|move|(49.0, 61.0)|Bone follows the door movement and visibly pulsing search at the crowded northern eastern cottage|
|+318.000|E456|Bone|(50.51, 74.04)|The animal workers try to bar the crowded cottage entrance as probing blood thickens underneath. Bone punctures the shutter beside them to expose a new angle.|
|+318.000|E457|REACTION||Occupants disagree over staying together under two-sided pressure. Some choose the nearby woodland edge because nobody here has reported a lethal barrier contact.|
|+318.000|E458|move|(41.12, 79.75)|Household chooses nearby forest edge rather than another visibly compromised house|
|+318.000|E459|hold|(41.12, 79.75)|Two family members stay low inside; opening another exit seems more dangerous|
|+318.000|E460|move|(-34.44, 18.56)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+318.000|E461|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+318.000|E462|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+318.000|E463|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+318.000|E464|split|(50.51, 74.04)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+318.000|E465|hold|(50.51, 74.04)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+318.000|E466|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+318.000|E467|split|(50.51, 74.04)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+318.000|E468|hold|(50.51, 74.04)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+318.000|E469|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+324.000|E470|Bone|(50.51, 74.04)|One animal worker leans out to hold the damaged exit for a neighbour. Bone escalates from the shutter strike and precisely kills that exposed protector.|
|+324.000|E471|REACTION||Remaining animal workers abandon the damaged exit and split from the attempted rescue; the refusal to continue is ordinary fear.|
|+324.000|E472|move|(50.51, 74.04)|Remaining workers abandon unsafe rescue and seek room beyond the house|
|+324.000|E473|Blood memory|(7.7, 16.17)|Eastern strong shelter return weakens as people split. Blood retains the recent substantial-presence area and probes neighbouring exits; body continues along its committed approach.|
|+332.000|E474|Barrier|(68.18, 78.06)|A displaced household/runner attempts an untested boundary section. Only local witnesses acquire direct B4.|
|+332.000|E475|move|(68.18, 78.06)|Recoil from lethal boundary response and seek nearby cover rather than try again|
|+332.000|E476|Barrier|(-65.85, 104.31)|A displaced household/runner attempts an untested boundary section. Only local witnesses acquire direct B4.|
|+332.000|E477|move|(52.0, 70.0)|Two eastern boundary witnesses recoil and one turns back for the other; this novel human response draws Bone away from the repeated cottage-door scene|
|+336.000|E478|Bone|(64.0, 85.0)|One boundary witness turns back to steady the other while withdrawing from the lethal sheet. Bone strikes that exposed helping gesture precisely.|
|+336.000|E479|REACTION||The remaining witness knows the barrier is lethal and chooses isolated tree-side cover inside it rather than another crossing.|
|+336.000|E480|move|(64.0, 85.0)|Surviving B4 witness separates from refuge traffic and hides inside the forest edge|
|+338.000|E481|REACTION|(23.5, 86.4)|New arrivals at the church argue over the damaged entrance and whether to admit more people. Refusing entry reflects fear; no additional bad actor is invented.|
|+338.000|E482|move|(64.0, 80.0)|Overlapping human voices at the church entrance are audible across this open upper-eastern gap. Local edge interest has decayed; Bone makes a sharp return relocation|
|+342.000|E483|Blood|(55.07, 54.36)|Blood reaches the eastern concentration's new refuge doorway. Visible arrivals and a renewed local probe response let him reacquire broad presence without exact person tracking.|
|+342.000|E484|hold|(30.75, 30.52)|Pressure recovery and resource gathering at the eastern doorway|
|+342.000|E485|REACTION||New impact changes the refuge again. Some remain behind the damaged face; others take side gaps despite uncertainty.|
|+342.000|E486|move|(-34.44, 18.56)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E487|hold|(-9.62, 26.77)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+342.000|E488|shelter decision|(-9.62, 26.77)|Household elects silence rather than automatic flight|
|+342.000|E489|move|(-9.62, 26.77)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E490|hold|(-9.62, 26.77)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+342.000|E491|shelter decision|(-9.62, 26.77)|Household elects silence rather than automatic flight|
|+342.000|E492|move|(-9.62, 26.77)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E493|move|(7.29, 70.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E494|move|(37.62, 33.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E495|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E496|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E497|hold|(-37.9, 50.76)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+342.000|E498|shelter decision|(-37.9, 50.76)|Household elects silence rather than automatic flight|
|+342.000|E499|hold|(7.29, 70.89)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+342.000|E500|shelter decision|(7.29, 70.89)|Household elects silence rather than automatic flight|
|+342.000|E501|hold|(-10.56, 91.48)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+342.000|E502|shelter decision|(-10.56, 91.48)|Household elects silence rather than automatic flight|
|+342.000|E503|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E504|move|(50.51, 74.04)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E505|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E506|move|(-37.9, 50.76)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+342.000|E507|hold|(50.51, 74.04)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+342.000|E508|shelter decision|(50.51, 74.04)|Household elects silence rather than automatic flight|
|+342.000|E509|move|(-37.9, 50.76)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+348.000|E510|Bone|(23.5, 97.66)|A recent eastern escapee steps into the damaged public doorway as the entry argument breaks. Bone selects that visible movement, not an unseen interior headcount.|
|+348.000|E511|REACTION||People at the public entrance recoil and abandon that immediate doorway attempt. Interior households choose silence or another route from their own observations.|
|+348.000|E512|move|(-20.0, -42.89)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+348.000|E513|split|(55.2, 52.91)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+348.000|E514|hold|(55.2, 52.91)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+348.000|E515|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+348.000|E516|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+348.000|E517|split|(55.2, 52.91)|Shelter disagreement: some distrust the probing blood; others insist that opening the door exposes everyone.|
|+348.000|E518|hold|(55.2, 52.91)|Remaining occupants barricade and keep quiet; refusal to leave is ordinary fear|
|+348.000|E519|move|(55.2, 52.91)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+348.000|E520|move|(30.75, 30.52)|The connected northern-eastern threshold still gives several overlapping presences while the nearer refuge disperses. Blood moves within real range of the next concentration|
|+358.000|E521|Bone|(23.5, 97.66)|At the church-side argument one western refugee tries to feint around the broken entrance. Bone deliberately denies that side and forces another immediate choice; this is not a missed intended hit.|
|+358.000|E522|REACTION||Western refugees abandon that entrance and recoil toward the open upper lane; they retain reports about the barrier, not knowledge of every attack.|
|+358.000|E523|move|(23.5, 97.66)|Take the remaining side of the public approach after Bone blocks the attempted entrance|
|+360.000|E524|Blood|(50.51, 74.04)|Blood's body has now reached the northern-eastern concentration. The rage-amplified strike follows a physically connected live threshold and exploits prior Bone damage, without attacking remotely from a search node.|
|+360.000|E525|hold|(42.66, 43.89)|Local pressure recovery at final eastern attack site; no post-terminal target selected|
|+360.000|E526|REACTION||Survivors respond to the latest eastern pressure and doorway denial. These are the final human reactions before the fixed confrontation ends.|
|+360.000|E527|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+360.000|E528|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+360.000|E529|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+360.000|E530|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+360.000|E531|hold|(23.5, 97.66)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+360.000|E532|shelter decision|(23.5, 97.66)|Household elects silence rather than automatic flight|
|+360.000|E533|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+360.000|E534|hold|(23.5, 97.66)|Stay silent and move behind intact inner cover after seeing the probe; outside danger is less understood|
|+360.000|E535|shelter decision|(23.5, 97.66)|Household elects silence rather than automatic flight|
|+360.000|E536|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+360.000|E537|move|(23.5, 97.66)|Leave newly compromised shelter for a nearby known refuge after local disagreement|
|+366.001|E538|Witch final death|(2, 146)|WITCH KILLS MAYOR. The approximately60-second confrontation ends by her choice, without survivor-count knowledge. Exact execution choreography remains reserved. PRIMARY MASSACRE COMPLETE.|

## Verification and stop boundary

Census, unique deaths, initial B3/B4, executed Blood range, actual barrier coordinates, final Mayor identity and no post-terminal casualties pass bookkeeping checks. Source placement and spatial/model validity do not fully pass; see v4_validation.json. Earlier branches and pre90 files remain unchanged. This result is preserved for review, not approved for implementation. No UE/Blender/VFX/corpse/destruction assets or later massacre events were authored.

## Timestamp precision

The canonical terminal clock is T+366.000540954. Event and casualty records round timestamps to milliseconds, so the Mayor event appears as T+366.001. Validation compares matching precision; this is the same final event, not an additional post-terminal death.
