# MASSACRE SIMULATION V3 — INDEPENDENT RE-SIMULATION FROM T+90

**CLOSED at T+373.923. Mayor personally killed by Witch, sixty seconds after her geometrically calculated arrival.**

**57 fatalities; 113 survivors; no injured survivors. FAILED against the near-total-massacre premise.** This is a failed working implementation/parameterisation, not evidence that the proposed V3 mechanics inherently cannot work. No quota deaths, unseen cleanup, UE changes or post-Mayor simulation were added.

V3 is a new causal branch. Its closed-state hash was written before opening V1/V2 simulation reports for comparison. Earlier branches and approved maps remain unchanged.

## Source boundary and T+90 handoff

Only unchanged map_data.json, map_views.json, t0_activity.json, t1_simulation.json, bone_completion.json and massacre_behaviour_rules.json feed this planner. The supplied design bible was read; its hash is in v3_provenance.json. No post90 V1/V2 movement, knowledge, target, survivor or casualty ledger was imported.

170 original residents; seven already dead; 163 alive including four injured. Blood (-2.209,44.524); Bone (-37.5,8.8), attending M05; Witch (-15.557,36.374,5.640). The barrier is opaque, sealed and contact-reactive. B3/B4 start at zero. Exhumed graves remain unchanged.

Pre90 files identify cohorts and micro-groups, not every person. Pxx-nn expands those existing counts into stable **V3-local** person IDs. They are not new villagers or identity matches to V1/V2 suffixes. Named micro-members and moved T1 endpoints are retained; unmarked static people are allocated within their T0 household/work areas. See v3_initial_state.json.

At T90, 4.88 relative units of accessible opening blood already make Blood **FED**. Raw carried-resource storage begins at zero; the first integration step collects those existing local sources before any V3 attack decision. The initial raw debug snapshot's AWAKENED label is an inventory/presentation artefact, not a second awakening. The closed state is preserved with that limitation disclosed.

## Method and limits

35 separately saved ACTION/REACTION pairs cover +90 to closure. Each phase is an editable object in v3_action_cycles.jsonl or v3_reaction_cycles.jsonl. Actions use current physical/perceptual state; reactions use local evidence. Movement and stream fronts advance continuously. Major incidents or a maximum fifteen-second window end a cycle. Most event times have one-second resolution; Witch arrival is analytic.

The existing map supplies footprints, roads, heights and barrier. Witch uses 3D distance. Other agents use plan-space paths: walking 1.25 m/s, flight 2.3 m/s, assisted injury 0.65 m/s, supervised child groups at most 1.5 m/s. Bone bursts at 8 m/s; Blood stays at 1.55 m/s. These are review parameters, not measured gameplay.

Most doorways, rear exits and deeper-room offsets are inferred. Interior markers represent occupied space, not literal collocated bodies. This is not UE collision, detailed interior sight, calibrated hearing or post-opacity lighting. Terrain/retaining-wall traversal outside the Witch route remains approximate.

Technical dry runs repaired narrow-gap routing, arrivals seeing existing streams, Bone's loss-of-sight repositioning and threshold sight gating; they were discarded and replayed from T90. Strengths were not adjusted toward a casualty count. At +286, two obstructed strikes give Blood local evidence to flank an intervening shed. The final engine reproduces the same events and casualty ledger from T90.

**Material weaknesses:** nearest-access search revisits local thresholds too readily; new branches all originate at the primary mass rather than independent connected blood sites; proxy wall footprints absorb pressure without cumulative breach; Bone can cycle between object threats and abandoned hidden targets; estate staff/guard reactions to Witch securing the Mayor are under-modelled. These limits prevent approval as a convincing full reconstruction.

## Locked behaviour

- WITCH = DESTINATION. Saved uphill route; ignores pleas; creator immunity; no incidental hunt or explanatory walk dialogue.
- BLOOD = CONCENTRATION + ACCESSIBLE BLOOD + PHYSICAL SEARCH. Coarse visible/activity/bleeding or stream-delivered cues; no exact indoor census in selection.
- BONE = ATTENTION / ACTIVELY PREDATORY. Precise intended hits and deliberate object strikes; local recognition; consequences and changing interests. Ordinary repeated Blood crashes are not attention inputs.
- BARRIER = BOUNDARY / REACTIVE WEAPON. Actual contact only; direct B4 differs from warning reports.
- CIVILIANS = LOCAL KNOWLEDGE. Groups can disagree/split; fear-based refusal or silence is not classified as exploitation.
- MAYOR = FINAL DEATH. Witch's sixty-second choice is independent of population. No casualty follows closure.

## Chronological reading

**+90–127:** Blood selects the visible junction goods concentration. His +96 corridor kills its six people and injures four porch customers. Those four seek cover but are struck again at +113. The original wounded stall users die at +125 while seeking frontage help. Bone's precise threats force M05 into movement; the parent tests the western boundary at +115. The child witnesses the lethal response and later reaches familiar cover. Eastern field contact +108 and a third contact +122 arise independently.

**Bell +100:** the caretaker reacts to blackout/lower disturbance, walks to the ground-floor rope, pulls the ordinary emergency bell, then takes cover. No magical attacker/boundary information or later ringing pattern is added.

**+120–184:** infiltration creates disagreements in an upper-middle household and the tavern. At +130 some tavern occupants leave by another exit; three remain and are struck at +163. The departing group lacks other areas' direct barrier knowledge: one tests the eastern edge and dies at +168. Bone follows novel human flight, kills an exposed tavern worker at +173, pressures another shelter and allows further movement. Blood strikes a physically detected central cottage concentration at +175.

**+203–254:** Bone locally recognises the entrance guard. The guard investigated the emergency and is trying to protect an upper-household refugee near the stair/estate threshold. Bone injures P12-09 at +223, then kills **the same person** at +243 while deliberately leaving the guard alive. Equipment threats and permitted retreat separate these acts. At +254 he kills the guard at (6,132), after 51 seconds of personal torment. Other guards receive no historical guilt.

**+239–310:** infiltration divides another central refuge. A departing person independently tests the eastern boundary at +262 without direct B4 or a received lethal-contact warning. Repeated pressure toward remaining people is obstructed by a shed footprint; Blood slowly flanks it at +286. The +308 strike reaches two remaining occupants.

**+313.923–373.923:** Witch reaches and secures the Mayor. The integration record is +314, a 0.077-second sampling difference; physical arrival is +313.923. Her rage increases local searching/pressure without faster body movement. Blood kills fifteen during the final minute, at +320, +344 and +361. Witch kills the Mayor at +373.923 regardless of the other 113 still alive.

## Blood resource and physical searching

Units are dimensionless accessible-volume bookkeeping, not litres. Death contributes one unit; injury contributes 0.22 and a later death only the remaining 0.78. Transfers require primary-mass proximity or a continuous reached trail. Final accounting: **57 generated = 21.66 collected + 35.34 remaining at sites**. The Mayor's final source is never used for another attack.

Power saturates as q = 1 - exp(-collected/15), with carried capacity 48. Before rage: control 24+50q m; stream-front speed 0.8+0.8q m/s; slots 2+floor(6q); total branch-length budget 55+300q m; pressure reach 11+19q m; half-width 3.5+5.5q m. Rage adds 8 m control, 0.2 m/s stream-front speed, one slot, 75 m budget, 4 m pressure reach and 1.5 m half-width. Body speed remains 1.55 m/s.

Blood starts FED, reaches SATURATED through actual accessible sources, and **never reaches DELUGE** here. Final local resource is 21.66; rage-enhanced control is about 70.2 m; stream front 1.61 m/s; seven slots. Growth is event/resource driven. Rage is additional, not its origin.

29 stream commitments test 13 footprints; 12 thresholds are reached. Branches physically grow over ground, cross estimated thresholds, then probe floors. Empty/weak/out-of-range branches withdraw. None/faint/presence/dense responses differ from the auditor's exact ledger. A quiet single person is harder to identify. Bone only exploits a stream where its threshold is locally visible.

Nine documented splits and fifteen movement commitments explicitly leave compromised shelters. Others stay deeper. This changes behaviour locally, but large untouched farm/refuge groups remain. The implementation does not achieve a village-wide search network.

## Opportunists versus ordinary fear

P08-20, an existing goods porter, takes unattended market valuables at +106. P04-06, an existing farmyard worker, takes the shared cart and monopolises stored supplies at +104. These are working personality refinements, not new people or supernatural collaboration. Both survive. Bone is not a moral judge.

Stolen goods remain associated with their carriers/shelters; no dramatic abandoned pose is fabricated. Remaining quiet or avoiding exposure is treated as fear, not malice. Shelter disagreements occur; no completed refusal-of-entry incident was forced into this run.

## Witch, estate and the final minute

Remaining route length: 237.601 m in 3D, including main street, the 0.9 m height seam, stair/landings, courtyard and minimal hall entry. Road/court speed 1.1 m/s; stairs 0.85 m/s. Arrival +313.923325 independently follows these shared source coordinates and paces. Matching V2 numerically does not imply an imported event.

At +91 the M04 water carriers call to her; she ignores them. Their observation records indifference, not proof of responsibility. No executed Blood corridor intersects her, so no immunity spectacle is forced.

Confrontation topics remain unvoiced: lover and son; the Mayor's responsibility, authority and failure; refusal of escape; pauses while suffering continues; realization that she saved him for last. Restraint and execution choreography remain undecided. This is active rage, not later spirit remorse.

The house guard and three staff survive within the hall footprint. Their exact room partition/sightline is unresolved. The terminal raw witness list is empty by reservation, not a claim nobody could witness the killing. Their confrontation reactions are insufficiently developed here and require review. The final-death rule alone does not explain how subsequent supernatural danger ceases.

Fifteen Blood fatalities occur during the extra minute, plus the Mayor. That interval matters. It does not establish that rage uniquely causes all fifteen: no complete no-rage counterfactual was run.

## Post-closure comparison

| Branch | Deaths | Survivors | Blood | Bone | Barrier | Witch |
|---|---:|---:|---:|---:|---:|---:|
| V1 | 73 | 97 | 55 | 13 | 4 | 1 |
| V2 | 112 | 58 | 101 | 5 | 5 | 1 |
| V3 | 57 | 113 | 45 | 6 | 5 | 1 |

V1/V2 reports were opened after the V3 closure hash. These are separate policies/parameterisations, not a controlled one-variable experiment. Unnamed static household refinements also differ. Numerical changes cannot be attributed solely to streams.

- **Shelters:** physical searching makes some refuges contestable, but reaches too few footprints. Twenty-nine final shelter pockets remain, including eight-person farm/residential groups. The shelter problem is not solved.
- **Blood:** physical search is legible but slower/more local than V2's sensing. Prior blood is collected and reused, but the body remains near the centre/old quarter. Only 21.66 units become controlled; Deluge never emerges.
- **Bone:** six total fatalities versus five in V2 is inadequate. Forced movement and personal cruelty improve, but repeated object pressure/abandonment remains too weak. His pattern stays distinct from Blood; ignoring repeated crashes alone is insufficient.
- **Guard:** independent recognition +203 and final kill +254 produce 51 seconds of torment, including harm to someone he tries to save. This is more personally consequential than equipment-only threats.
- **Boundary:** the +168 and +262 deaths follow compromised-shelter departures. All five contacts remain locally uninformed; matching V2's total is coincidence.
- **Final minute:** fifteen Blood fatalities occur, but the unique contribution of amplification is not isolated. It cannot compensate for poor earlier coverage.
- **Over/under effectiveness:** collocated proxy positions and simple fatal corridors can overstate certainty inside acquired groups. Immutable occluding footprints and over-repeated weak probes understate later breaches/search. No settlement-wide overpowering mechanic is demonstrated.
- **Narrative verdict:** near-total revenge is NOT supported. Keep this failed branch for diagnosis, not UE implementation.

V4 questions, not executed: add explored/empty/frontier memory to search; permit physically connected secondary-source branching within one budget; model cumulative structural openings; decay Bone's repeated shelter-level intimidation and seek a different acquired stimulus or consequential opening; resolve estate reactions to Witch arrival; validate light, thresholds, slopes and perception in 3D. Do not fix this with quotas, global omniscience, arbitrary time extension or post-Mayor cleanup.

## Verification / editability

Closed data: v3_simulation.json. Handoff, parameters, door assumptions, phase JSONL, actor trace, casualties, knowledge, movements and pockets are separate. Clean base/T0/blank maps are unchanged.

Deterministic replay matches casualties, decisions, people and sources exactly. Events differ only by an optional false reassessment field on three earlier moves. Census, unique deaths, guard killer, T90 B3/B4 and final Mayor-only death pass. This proves repeatability, not realistic psychology or narrative success.

No UE source, asset, texture, VFX, gore image, corpse pose or production damage is generated. No subsequent massacre/rebuilding step is simulated.

## Review sheets

| Sheet | Editable |
|---|---|
| [Full chronology](01_v3_full_chronology.png) | [SVG](01_v3_full_chronology.svg) |
| [Blood incidents and actual path](02_v3_blood_incidents.png) | [SVG](02_v3_blood_incidents.svg) |
| [Blood resource and power](03_v3_blood_power.png) | [SVG](03_v3_blood_power.svg) |
| [Physical search network progression](04_v3_search_network.png) | [SVG](04_v3_search_network.svg) |
| [Bone attention and incidents](05_v3_bone_incidents.png) | [SVG](05_v3_bone_incidents.svg) |
| [Son-killer guard sequence](06_v3_guard_sequence.png) | [SVG](06_v3_guard_sequence.svg) |
| [Shelters, splits and forced movement](07_v3_shelter_movement.png) | [SVG](07_v3_shelter_movement.svg) |
| [Boundary contacts and local knowledge](08_v3_barrier_knowledge.png) | [SVG](08_v3_barrier_knowledge.svg) |
| [Witch route and height profile](09_v3_witch_route.png) | [SVG](09_v3_witch_route.svg) |
| [Mayor final minute](10_v3_mayor_minute.png) | [SVG](10_v3_mayor_minute.svg) |
| [Casualty progression](11_v3_casualty_progression.png) | [SVG](11_v3_casualty_progression.svg) |
| [Final aftermath / survivors](12_v3_final_aftermath.png) | [SVG](12_v3_final_aftermath.svg) |
| [Environmental-story seeds](13_v3_story_seeds.png) | [SVG](13_v3_story_seeds.svg) |

## Bone incident and attention history

| Time | Event | Position | Trigger / consequence |
|---|---|---|---|
| +91 | E0011 | [-34.3, 9.2] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P06-13 |
| +97 | E0021 | [-34.04, 4.71] | Cuts off the nearer cover with another exact object strike, then allows flight. Target P06-13 |
| +100 | E0028 | [-37.5, 8.8] | Attention changes: human movement along try nearby forest/field edge; lethal response unknown Target P06-14 |
| +101 | E0030 | [-35.02, 2.05] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P06-14 |
| +107 | E0046 | [-43.78, 0.01] | Cuts off the nearer cover with another exact object strike, then allows flight. Target P06-14 |
| +110 | E0051 | [-37.5, 8.8] | Attention changes: human movement along try nearby forest/field edge; lethal response unknown Target P06-13 |
| +111 | E0052 | [-37.5, 8.8] | Short burst toward the current human stimulus. Target P06-13 |
| +112 | E0053 | [-51.09, -1.68] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P06-13 |
| +119 | E0058 | [-43.64, 3.67] | Attention changes: human movement along withdraw from witnessed lethal boundary Target P06-14 |
| +120 | E0061 | [-47.54, -1.37] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P06-14 |
| +126 | E0066 | [-38.61, -0.32] | Cuts off the nearer cover with another exact object strike, then allows flight. Target P06-14 |
| +129 | E0069 | [-43.64, 3.67] | Attention changes: human movement along surviving child retreats toward familiar cover Target P06-14 |
| +130 | E0070 | [-43.64, 3.67] | Short burst toward the current human stimulus. Target P06-14 |
| +131 | E0071 | [-31.16, 0.55] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P06-14 |
| +137 | E0076 | [-35.97, 1.37] | After changing the shelter's decision state, loses interest in the unexposed occupants. Target P06-14 |
| +140 | E0078 | [-35.97, 1.37] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +144 | E0079 | [-29.46, 30.13] | Attention changes: human movement along try nearby forest/field edge; lethal response unknown Target P09-02 |
| +145 | E0080 | [-30.0, 32.0] | Short burst toward the current human stimulus. Target P09-02 |
| +152 | E0084 | [21.86, 47.24] | Short burst toward the current human stimulus. Target P09-02 |
| +154 | E0085 | [39.04, 40.32] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P09-02 |
| +160 | E0088 | [34.58, 41.81] | Short burst toward the current human stimulus. Target P09-02 |
| +162 | E0089 | [53.56, 29.32] | Cuts off the nearer cover with another exact object strike, then allows flight. Target P09-02 |
| +165 | E0093 | [48.03, 33.57] | Attention changes: human movement along try nearby forest/field edge; lethal response unknown Target P09-12 |
| +166 | E0095 | [48.03, 33.57] | Short burst toward the current human stimulus. Target P09-12 |
| +167 | E0096 | [60.49, 24.79] | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. Target P09-12 |
| +173 | E0106 | [53.59, 24.83] | Precisely kills the acquired person following their movement / protective response. Target P09-12 |
| +176 | E0114 | [54.57, 28.96] | Attention changes: human movement along withdraw from witnessed lethal boundary Target P09-13 |
| +177 | E0115 | [54.57, 28.96] | Short burst toward the current human stimulus. Target P09-13 |
| +178 | E0116 | [44.81, 24.89] | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. Target P09-13 |
| +184 | E0118 | [42.25, 23.35] | Cuts off the nearer cover with another exact object strike, then allows flight. Target P09-13 |
| +187 | E0120 | [47.19, 25.88] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +197 | E0122 | [14.0, 53.0] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +200 | E0123 | [13.66, 76.94] | Attention changes: person watches from an exposed position Target P16-02 |
| +203 | E0125 | [5.01, 99.24] | Locally sees the entrance guard; fragmented recognition changes his attention. Target P16-02 |
| +203 | E0126 | [5.01, 99.24] | Repositions to regain the recognised guard's sightline. |
| +205 | E0127 | [2.0, 122.0] | Deliberately reveals himself to the guard. Target P16-02 |
| +213 | E0129 | [2.0, 122.0] | Precise near-hit damages the guard's equipment. Target P16-02 |
| +223 | E0132 | [2.0, 122.0] | Spares the guard while harming a person within his protective reach. Target P12-09 |
| +235 | E0137 | [2.0, 122.0] | Appears from another angle and lets the guard retreat. Target P16-02 |
| +243 | E0143 | [2.0, 122.0] | Spares the guard while harming a person within his protective reach. Target P12-09 |
| +253 | E0147 | [2.91, 115.1] | Repositions to regain the recognised guard's sightline. |
| +254 | E0148 | [6.0, 132.0] | Kills the recognised entrance guard personally after prolonged, consequential torment. Target P16-02 |
| +259 | E0152 | [4.35, 122.97] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +263 | E0155 | [13.21, 92.22] | Attention changes: visible search stream pulses at threshold; Bone recognises interest Target P10-14 |
| +264 | E0156 | [15.0, 86.0] | Short burst toward the current human stimulus. Target P10-14 |
| +269 | E0158 | [28.0, 47.66] | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. Target P10-14 |
| +275 | E0161 | [27.84, 48.12] | After changing the shelter's decision state, loses interest in the unexposed occupants. Target P10-14 |
| +278 | E0162 | [27.84, 48.12] | Attention changes: visible search stream pulses at threshold; Bone recognises interest Target P10-23 |
| +279 | E0165 | [28.0, 47.66] | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. Target P10-23 |
| +285 | E0166 | [27.84, 48.12] | After changing the shelter's decision state, loses interest in the unexposed occupants. Target P10-23 |
| +288 | E0169 | [27.84, 48.12] | Attention changes: visible search stream pulses at threshold; Bone recognises interest Target P10-14 |
| +289 | E0170 | [28.0, 47.66] | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. Target P10-14 |
| +295 | E0173 | [27.84, 48.12] | After changing the shelter's decision state, loses interest in the unexposed occupants. Target P10-14 |
| +298 | E0174 | [27.84, 48.12] | Attention changes: visible search stream pulses at threshold; Bone recognises interest Target P10-23 |
| +299 | E0176 | [28.0, 47.66] | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. Target P10-23 |
| +305 | E0182 | [27.84, 48.12] | After changing the shelter's decision state, loses interest in the unexposed occupants. Target P10-23 |
| +308 | E0184 | [27.84, 48.12] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +318 | E0194 | [38.0, 65.0] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +328 | E0200 | [-30.0, 32.0] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +338 | E0203 | [14.0, 53.0] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +339 | E0207 | [14.24, 61.0] | Attention changes: visible search stream pulses at threshold; Bone recognises interest Target P09-03 |
| +343 | E0209 | [15.0, 86.0] | Short burst toward the current human stimulus. Target P09-03 |
| +353 | E0213 | [37.13, 22.14] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |
| +356 | E0217 | [20.84, 30.28] | Attention changes: visible search stream pulses at threshold; Bone recognises interest Target P10-15 |
| +366 | E0222 | [-37.0, 70.0] | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. |

## Barrier contact ledger

| Time | Person | Position | Direct witnesses | Prior stage |
|---|---|---|---|---|
| +108 | P01-04 | [60.15, -62.29] | P01-05 | 1 |
| +115 | P06-13 | [-52.01, -1.9] | P06-14 | 1 |
| +122 | P06-09 | [56.19, 15.56] | P06-10, P08-12, P08-13, P08-14, P08-15, P08-16 | 1 |
| +168 | P09-02 | [60.49, 24.79] | P09-03, P09-04, P09-05, P09-07, P09-12, P09-13 | 1 |
| +262 | P10-24 | [60.83, 25.31] | none | 1 |

Fourteen distinct people directly witness a reactive contact; twenty-two receive a warning report. These are separate forms of knowledge. v3_knowledge.csv records the actual transmission.

## All survivor pockets

| Place | Alive | Existing V3 IDs | Reason |
|---|---:|---|---|
| NorthBarn | 4 | P01-01, P01-02, P01-03, P01-05 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Farmstead_West | 8 | P01-06, P03-01, P03-02, P03-03, P03-04, P03-05, P03-06, P03-07 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| SouthBarn | 6 | P02-01, P02-02, P02-03, P02-04, P02-05, P02-06 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Farmstead_South | 6 | P04-01, P04-02, P04-03, P04-04, P04-05, P04-06 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| WitchHome | 4 | P05-03, P05-04, P05-05, P05-06 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| NeedleHouse | 2 | P06-01, P06-02 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| CollapsedCellarCottage | 4 | P06-03, P06-04, P06-11, P06-12 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_04 | 4 | P06-05, P06-06, P06-07, P06-14 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. The surviving M05 child reached familiar cover after witnessing the parent's boundary death; Bone pressured the encounter but did not complete a human strike on the child. |
| Cottage_09 | 3 | P06-08, P08-01, P08-02 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| CrookedCottage_YardShed | 5 | P06-10, P10-01, P10-02, P10-03, P10-16 | A physical search was assigned but had not reached the threshold by withdrawal/closure. No completed detection or lethal corridor reached these occupants. |
| Blacksmith | 3 | P07-01, P07-02, P07-04 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| AbandonedCottage | 3 | P08-11, P12-01, P12-02 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_03_YardShed | 1 | P08-20 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_07 | 8 | P10-10, P10-11, P10-12, P10-17, P10-18, P10-19, P10-20, P10-21 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| CrushedHome | 3 | P11-01, P11-02, P11-15 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| RearCottage | 5 | P11-03, P11-04, P11-16, P11-21, P11-22 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| EndRowCottage | 6 | P11-05, P11-06, P11-17, P15-01, P15-02, P15-03 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| WeaverCottage | 3 | P11-07, P11-08, P11-18 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_02 | 2 | P11-09, P11-10 | A search branch reached the footprint, but did not lead to a lethal executed attack on these occupants. Coarse response, cover, competing cues and the terminal clock left them alive. |
| Cottage_05 | 3 | P11-11, P11-12, P11-19 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_10 | 3 | P11-13, P11-14, P11-20 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| UpperCottage | 5 | P12-03, P12-04, P12-11, P12-14, P16-08 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| SealedCellarCottage | 6 | P12-05, P12-06, P12-12, P16-03, P17-01, P17-02 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_03 | 3 | P12-07, P12-08, P12-13 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_11 | 1 | P12-10 | A search branch reached the footprint, but did not lead to a lethal executed attack on these occupants. Coarse response, cover, competing cues and the terminal clock left them alive. |
| Church | 1 | P13-01 | The caretaker used the rope at +100 and then sheltered. No physical search branch or acquired Bone attack reached the church before closure; the bell signalled emergency only. |
| SplitRoofCottage | 4 | P14-01, P14-02, P14-05, P14-06 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| Cottage_08 | 3 | P14-03, P14-04, P14-07 | No executed search branch reached this footprint. It lay outside the chosen local search network or was passed over by its limited branch budget. The retained occupants were not exposed by an executed Bone incident. |
| MayorHall | 4 | P16-04, P16-05, P16-06, P16-07 | House guard and three staff remained inside. The Witch's chosen target was the Mayor. No Blood/Bone attack reached their room before her timed final killing. Their subsequent reactions are unexecuted. |

These 113 are provisional outcomes, not approved new survivor lore. Blood ends (24.323,32.882), searching locally; Bone ends (-2,108), no acquired current person; Witch ends (2,146). All subsequent actor, barrier and civilian actions are unexecuted.

## Every ACTION / REACTION cycle

| Cycle | Window | Action records | Human decisions | New deaths | Living |
|---|---|---:|---:|---:|---:|
| C01 | +90 to +96 | 13 | 35 | 6 | 157 |
| C02 | +96 to +101 | 12 | 45 | 0 | 157 |
| C03 | +101 to +107 | 14 | 8 | 0 | 157 |
| C04 | +107 to +112 | 7 | 10 | 1 | 156 |
| C05 | +112 to +117 | 3 | 25 | 5 | 151 |
| C06 | +117 to +122 | 7 | 18 | 1 | 150 |
| C07 | +122 to +127 | 5 | 8 | 4 | 146 |
| C08 | +127 to +137 | 8 | 58 | 0 | 146 |
| C09 | +137 to +142 | 2 | 11 | 0 | 146 |
| C10 | +142 to +151 | 5 | 57 | 0 | 146 |
| C11 | +151 to +162 | 6 | 50 | 0 | 146 |
| C12 | +162 to +167 | 7 | 26 | 3 | 143 |
| C13 | +167 to +172 | 9 | 40 | 1 | 142 |
| C14 | +172 to +177 | 10 | 10 | 7 | 135 |
| C15 | +177 to +184 | 3 | 49 | 0 | 135 |
| C16 | +184 to +199 | 4 | 70 | 0 | 135 |
| C17 | +199 to +214 | 7 | 55 | 0 | 135 |
| C18 | +214 to +229 | 3 | 66 | 0 | 135 |
| C19 | +229 to +243 | 11 | 80 | 1 | 134 |
| C20 | +243 to +254 | 5 | 55 | 1 | 133 |
| C21 | +254 to +259 | 4 | 17 | 1 | 132 |
| C22 | +259 to +264 | 4 | 26 | 1 | 131 |
| C23 | +264 to +269 | 2 | 19 | 0 | 131 |
| C24 | +269 to +275 | 3 | 39 | 0 | 131 |
| C25 | +275 to +280 | 4 | 6 | 0 | 131 |
| C26 | +280 to +285 | 1 | 24 | 0 | 131 |
| C27 | +285 to +295 | 7 | 48 | 0 | 131 |
| C28 | +295 to +305 | 9 | 50 | 0 | 131 |
| C29 | +305 to +310 | 4 | 20 | 2 | 129 |
| C30 | +310 to +320 | 10 | 46 | 4 | 125 |
| C31 | +320 to +335 | 6 | 55 | 0 | 125 |
| C32 | +335 to +344 | 9 | 44 | 10 | 115 |
| C33 | +344 to +359 | 8 | 54 | 0 | 115 |
| C34 | +359 to +364 | 2 | 13 | 1 | 114 |
| C35 | +364 to +373.923 | 5 | 37 | 1 | 113 |

## Full chronological event ledger

The seven opening fatalities remain in the casualty/source ledger. All post90 events follow; exact exposures, intentions, witnesses and resources are in v3_casualties.csv.

| Time | ID | Phase / actor | Event | Living |
|---|---|---|---|---:|
| +91 | E0001 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0002 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0003 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0004 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0005 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0006 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0007 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0008 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 163 |
| +91 | E0009 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_13] | 163 |
| +91 | E0010 | ACTION / Blood | Commits to visible dense human activity; five-second build-up. | 163 |
| +91 | E0011 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 163 |
| +91 | E0012 | REACTION / Civilians | Calls to the familiar Witch while she continues uphill without answering. | 163 |
| +91 | E0013 | REACTION / Civilians | Calls to the familiar Witch while she continues uphill without answering. | 163 |
| +95 | E0014 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_09_YardShed] | 163 |
| +96 | E0015 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. | 157 |
| +97 | E0016 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +97 | E0017 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +97 | E0018 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +97 | E0019 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +97 | E0020 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_13] | 157 |
| +97 | E0021 | ACTION / Bone | Cuts off the nearer cover with another exact object strike, then allows flight. | 157 |
| +98 | E0022 | REACTION / Civilians | take household handcart and monopolise stored goods | 157 |
| +98 | E0023 | REACTION / Civilians | take portable unattended market valuables for private gain | 157 |
| +99 | E0024 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_13] | 157 |
| +99 | E0025 | ACTION / Blood | Search response: dense (coarse cue only). [Cottage_13] | 157 |
| +99 | E0026 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_11] | 157 |
| +100 | E0027 | REACTION / Caretaker | Ground-floor rope: public emergency only. | 157 |
| +100 | E0028 | ACTION / Bone | Attention changes: human movement along try nearby forest/field edge; lethal response unknown | 157 |
| +101 | E0029 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_13] | 157 |
| +101 | E0030 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 157 |
| +102 | E0031 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_13] | 157 |
| +103 | E0032 | ACTION / Blood | Slow approach toward visible dense human activity. | 157 |
| +104 | E0033 | REACTION / Civilians | take shared handcart and monopolise stored supplies; portable goods now carried. | 157 |
| +104 | E0034 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +104 | E0035 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +104 | E0036 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +104 | E0037 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +104 | E0038 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +104 | E0039 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 157 |
| +104 | E0040 | ACTION / Blood | New surface search branch toward an untested nearby access. [Tavern] | 157 |
| +106 | E0041 | REACTION / Civilians | take unattended market valuables for private gain; portable goods now carried. | 157 |
| +106 | E0042 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_09_YardShed] | 157 |
| +107 | E0043 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_11] | 157 |
| +107 | E0044 | ACTION / Blood | Search response: presence (coarse cue only). [Tavern] | 157 |
| +107 | E0045 | ACTION / Blood | Slow approach toward visible dense human activity. | 157 |
| +107 | E0046 | ACTION / Bone | Cuts off the nearer cover with another exact object strike, then allows flight. | 157 |
| +108 | E0047 | ACTION / Blood | Search response: none (coarse cue only). [Tavern] | 156 |
| +108 | E0048 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01_YardShed] | 156 |
| +108 | E0049 | ACTION / Blood | Commits to visible aid/bleeding; five-second build-up. | 156 |
| +108 | E0050 | ACTION / Barrier | A civilian physically tests the boundary; local reactive strike. | 156 |
| +110 | E0051 | ACTION / Bone | Attention changes: human movement along try nearby forest/field edge; lethal response unknown | 156 |
| +111 | E0052 | ACTION / Bone | Short burst toward the current human stimulus. | 156 |
| +112 | E0053 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 156 |
| +113 | E0054 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. | 152 |
| +114 | E0055 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_11] | 152 |
| +115 | E0056 | ACTION / Barrier | A civilian physically tests the boundary; local reactive strike. | 151 |
| +118 | E0057 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_11] | 151 |
| +119 | E0058 | ACTION / Bone | Attention changes: human movement along withdraw from witnessed lethal boundary | 151 |
| +120 | E0059 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_11] | 151 |
| +120 | E0060 | ACTION / Blood | Commits to visible aid/bleeding; five-second build-up. | 151 |
| +120 | E0061 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 151 |
| +121 | E0062 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_11] | 151 |
| +122 | E0063 | ACTION / Barrier | A civilian physically tests the boundary; local reactive strike. | 150 |
| +125 | E0064 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01_YardShed] | 146 |
| +125 | E0065 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. | 146 |
| +126 | E0066 | ACTION / Bone | Cuts off the nearer cover with another exact object strike, then allows flight. | 146 |
| +127 | E0067 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_11] | 146 |
| +127 | E0068 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Tavern] | 146 |
| +129 | E0069 | ACTION / Bone | Attention changes: human movement along surviving child retreats toward familiar cover | 146 |
| +130 | E0070 | ACTION / Bone | Short burst toward the current human stimulus. | 146 |
| +131 | E0071 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 146 |
| +132 | E0072 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_11] | 146 |
| +133 | E0073 | ACTION / Blood | Search response: presence (coarse cue only). [Tavern] | 146 |
| +133 | E0074 | ACTION / Blood | Slow approach toward physical stream presence. [Tavern] | 146 |
| +134 | E0075 | ACTION / Blood | Commits to visible dense human activity; five-second build-up. | 146 |
| +137 | E0076 | ACTION / Bone | After changing the shelter's decision state, loses interest in the unexposed occupants. | 146 |
| +139 | E0077 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. | 146 |
| +140 | E0078 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 146 |
| +144 | E0079 | ACTION / Bone | Attention changes: human movement along try nearby forest/field edge; lethal response unknown | 146 |
| +145 | E0080 | ACTION / Bone | Short burst toward the current human stimulus. | 146 |
| +146 | E0081 | ACTION / Blood | Commits to visible dense human activity; five-second build-up. | 146 |
| +151 | E0082 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01] | 146 |
| +151 | E0083 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. | 146 |
| +152 | E0084 | ACTION / Bone | Short burst toward the current human stimulus. | 146 |
| +154 | E0085 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 146 |
| +157 | E0086 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_13] | 146 |
| +158 | E0087 | ACTION / Blood | Commits to physical stream presence; five-second build-up. [Tavern] | 146 |
| +160 | E0088 | ACTION / Bone | Short burst toward the current human stimulus. | 146 |
| +162 | E0089 | ACTION / Bone | Cuts off the nearer cover with another exact object strike, then allows flight. | 146 |
| +163 | E0090 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Tavern] | 143 |
| +164 | E0091 | ACTION / Blood | Search response: none (coarse cue only). [Tavern] | 143 |
| +164 | E0092 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_09_YardShed] | 143 |
| +165 | E0093 | ACTION / Bone | Attention changes: human movement along try nearby forest/field edge; lethal response unknown | 143 |
| +166 | E0094 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_13] | 143 |
| +166 | E0095 | ACTION / Bone | Short burst toward the current human stimulus. | 143 |
| +167 | E0096 | ACTION / Bone | Deliberate near-hit at cover / carried object; the acquired person is intentionally spared for now. | 143 |
| +168 | E0097 | ACTION / Barrier | A civilian physically tests the boundary; local reactive strike. | 142 |
| +169 | E0098 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01] | 142 |
| +169 | E0099 | ACTION / Blood | Search response: dense (coarse cue only). [Cottage_01] | 142 |
| +170 | E0100 | ACTION / Blood | Commits to physical stream dense; five-second build-up. [Cottage_01] | 142 |
| +172 | E0101 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 142 |
| +172 | E0102 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 142 |
| +172 | E0103 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 142 |
| +172 | E0104 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 142 |
| +172 | E0105 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_01] | 142 |
| +173 | E0106 | ACTION / Bone | Precisely kills the acquired person following their movement / protective response. | 141 |
| +175 | E0107 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Cottage_01] | 135 |
| +176 | E0108 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 135 |
| +176 | E0109 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 135 |
| +176 | E0110 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 135 |
| +176 | E0111 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 135 |
| +176 | E0112 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_01] | 135 |
| +176 | E0113 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01_YardShed] | 135 |
| +176 | E0114 | ACTION / Bone | Attention changes: human movement along withdraw from witnessed lethal boundary | 135 |
| +177 | E0115 | ACTION / Bone | Short burst toward the current human stimulus. | 135 |
| +178 | E0116 | ACTION / Bone | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. [CrookedCottage_YardShed] | 135 |
| +179 | E0117 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_09_YardShed] | 135 |
| +184 | E0118 | ACTION / Bone | Cuts off the nearer cover with another exact object strike, then allows flight. | 135 |
| +187 | E0119 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_11] | 135 |
| +187 | E0120 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 135 |
| +190 | E0121 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01_YardShed] | 135 |
| +197 | E0122 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 135 |
| +200 | E0123 | ACTION / Bone | Attention changes: person watches from an exposed position | 135 |
| +202 | E0124 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_11] | 135 |
| +203 | E0125 | ACTION / Bone | Locally sees the entrance guard; fragmented recognition changes his attention. | 135 |
| +203 | E0126 | ACTION / Bone | Repositions to regain the recognised guard's sightline. | 135 |
| +205 | E0127 | ACTION / Bone | Deliberately reveals himself to the guard. | 135 |
| +213 | E0128 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_12] | 135 |
| +213 | E0129 | ACTION / Bone | Precise near-hit damages the guard's equipment. | 135 |
| +219 | E0130 | ACTION / Blood | New surface search branch toward an untested nearby access. [Tavern] | 135 |
| +223 | E0131 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_13] | 135 |
| +223 | E0132 | ACTION / Bone | Spares the guard while harming a person within his protective reach. | 135 |
| +231 | E0133 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_13] | 135 |
| +231 | E0134 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_09_YardShed] | 135 |
| +234 | E0135 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Tavern] | 135 |
| +235 | E0136 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01] | 135 |
| +235 | E0137 | ACTION / Bone | Appears from another angle and lets the guard retreat. | 135 |
| +236 | E0138 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_12] | 135 |
| +238 | E0139 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_12] | 135 |
| +238 | E0140 | ACTION / Blood | Commits to physical stream presence; five-second build-up. [Cottage_12] | 135 |
| +243 | E0141 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01_YardShed] | 134 |
| +243 | E0142 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Cottage_12] | 134 |
| +243 | E0143 | ACTION / Bone | Spares the guard while harming a person within his protective reach. | 134 |
| +245 | E0144 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_09_YardShed] | 134 |
| +250 | E0145 | ACTION / Blood | Commits to visible aid/bleeding; five-second build-up. | 134 |
| +251 | E0146 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01] | 134 |
| +253 | E0147 | ACTION / Bone | Repositions to regain the recognised guard's sightline. | 134 |
| +254 | E0148 | ACTION / Bone | Kills the recognised entrance guard personally after prolonged, consequential torment. | 133 |
| +255 | E0149 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. | 132 |
| +256 | E0150 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 132 |
| +257 | E0151 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01_YardShed] | 132 |
| +259 | E0152 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 132 |
| +262 | E0153 | ACTION / Blood | Commits to physical stream presence; five-second build-up. [Cottage_12] | 131 |
| +262 | E0154 | ACTION / Barrier | A civilian physically tests the boundary; local reactive strike. | 131 |
| +263 | E0155 | ACTION / Bone | Attention changes: visible search stream pulses at threshold; Bone recognises interest | 131 |
| +264 | E0156 | ACTION / Bone | Short burst toward the current human stimulus. | 131 |
| +267 | E0157 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Cottage_12] | 131 |
| +269 | E0158 | ACTION / Bone | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. [Cottage_12] | 131 |
| +274 | E0159 | ACTION / Blood | Commits to physical stream presence; five-second build-up. [Cottage_12] | 131 |
| +275 | E0160 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_11] | 131 |
| +275 | E0161 | ACTION / Bone | After changing the shelter's decision state, loses interest in the unexposed occupants. | 131 |
| +278 | E0162 | ACTION / Bone | Attention changes: visible search stream pulses at threshold; Bone recognises interest | 131 |
| +279 | E0163 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_02] | 131 |
| +279 | E0164 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Cottage_12] | 131 |
| +279 | E0165 | ACTION / Bone | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. [Cottage_12] | 131 |
| +285 | E0166 | ACTION / Bone | After changing the shelter's decision state, loses interest in the unexposed occupants. | 131 |
| +286 | E0167 | ACTION / Blood | Flanks the intervening structure after repeated obstructed pressure. [Cottage_12] | 131 |
| +287 | E0168 | ACTION / Blood | New surface search branch toward an untested nearby access. [Tavern] | 131 |
| +288 | E0169 | ACTION / Bone | Attention changes: visible search stream pulses at threshold; Bone recognises interest | 131 |
| +289 | E0170 | ACTION / Bone | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. [Cottage_12] | 131 |
| +290 | E0171 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_11] | 131 |
| +291 | E0172 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_13] | 131 |
| +295 | E0173 | ACTION / Bone | After changing the shelter's decision state, loses interest in the unexposed occupants. | 131 |
| +298 | E0174 | ACTION / Bone | Attention changes: visible search stream pulses at threshold; Bone recognises interest | 131 |
| +299 | E0175 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_06] | 131 |
| +299 | E0176 | ACTION / Bone | Precise shutter / wall strike near a stream-marked or noisy shelter; occupants cannot locate a safe side. [Cottage_12] | 131 |
| +301 | E0177 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Tavern] | 131 |
| +303 | E0178 | ACTION / Blood | Commits to physical stream presence; five-second build-up. [Cottage_12] | 131 |
| +304 | E0179 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_02] | 131 |
| +304 | E0180 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_13] | 131 |
| +305 | E0181 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_02] | 131 |
| +305 | E0182 | ACTION / Bone | After changing the shelter's decision state, loses interest in the unexposed occupants. | 131 |
| +308 | E0183 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Cottage_12] | 129 |
| +308 | E0184 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 129 |
| +309 | E0185 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_12] | 129 |
| +309 | E0186 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01] | 129 |
| +314 | E0187 | ACTION / Witch | Reaches and secures the Mayor; sixty-second confrontation begins. No survivor-count knowledge. | 129 |
| +314 | E0188 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_06] | 129 |
| +314 | E0189 | ACTION / Blood | New surface search branch toward an untested nearby access. [OldQuarterStore] | 129 |
| +315 | E0190 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_06] | 129 |
| +315 | E0191 | ACTION / Blood | Commits to physical stream presence; five-second build-up. [Cottage_06] | 129 |
| +316 | E0192 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_06] | 129 |
| +317 | E0193 | ACTION / Blood | Search response: presence (coarse cue only). [Cottage_06] | 129 |
| +318 | E0194 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 129 |
| +319 | E0195 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [OldQuarterStore] | 129 |
| +320 | E0196 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [Cottage_06] | 125 |
| +321 | E0197 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 125 |
| +321 | E0198 | ACTION / Blood | Physically accessible spilled blood joins controllable mass. | 125 |
| +321 | E0199 | ACTION / Blood | Search response: none (coarse cue only). [Cottage_06] | 125 |
| +328 | E0200 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 125 |
| +329 | E0201 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01] | 125 |
| +331 | E0202 | ACTION / Blood | New surface search branch toward an untested nearby access. [OldQuarterSharedShed] | 125 |
| +338 | E0203 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 125 |
| +339 | E0204 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [OldQuarterSharedShed] | 125 |
| +339 | E0205 | ACTION / Blood | Search response: dense (coarse cue only). [OldQuarterSharedShed] | 125 |
| +339 | E0206 | ACTION / Blood | Commits to physical stream dense; five-second build-up. [OldQuarterSharedShed] | 125 |
| +339 | E0207 | ACTION / Bone | Attention changes: visible search stream pulses at threshold; Bone recognises interest | 125 |
| +343 | E0208 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_01_YardShed] | 125 |
| +343 | E0209 | ACTION / Bone | Short burst toward the current human stimulus. | 125 |
| +344 | E0210 | ACTION / Blood | Search response: none (coarse cue only). [OldQuarterSharedShed] | 115 |
| +344 | E0211 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [OldQuarterSharedShed] | 115 |
| +347 | E0212 | ACTION / Blood | New surface search branch toward an untested nearby access. [CrookedCottage] | 115 |
| +353 | E0213 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 115 |
| +354 | E0214 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [CrookedCottage] | 115 |
| +356 | E0215 | ACTION / Blood | Search response: dense (coarse cue only). [CrookedCottage] | 115 |
| +356 | E0216 | ACTION / Blood | Commits to physical stream dense; five-second build-up. [CrookedCottage] | 115 |
| +356 | E0217 | ACTION / Bone | Attention changes: visible search stream pulses at threshold; Bone recognises interest | 115 |
| +357 | E0218 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_01_YardShed] | 115 |
| +359 | E0219 | ACTION / Blood | Search response: none (coarse cue only). [CrookedCottage] | 115 |
| +361 | E0220 | ACTION / Blood | Deliberate pressure strike toward the perceived concentration. [CrookedCottage] | 114 |
| +364 | E0221 | ACTION / Blood | New surface search branch toward an untested nearby access. [Cottage_12] | 114 |
| +366 | E0222 | ACTION / Bone | Loses the concealed subject; darts to a different architectural sightline to look for a new human reaction. | 114 |
| +367 | E0223 | ACTION / Blood | Thin blood reaches an estimated threshold; visible infiltration may compromise shelter. [Cottage_12] | 114 |
| +368 | E0224 | ACTION / Blood | New surface search branch toward an untested nearby access. [Tavern] | 114 |
| +372 | E0225 | ACTION / Blood | New surface search branch toward an untested nearby access. [CrookedCottage_YardShed] | 114 |
| +373.923 | E0226 | ACTION / Witch | Mayor personally killed by Witch. Primary simulation closes; no later casualties. | 113 |
