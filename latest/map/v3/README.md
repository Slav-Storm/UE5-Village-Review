# V3 review package

**Failed near-total test: 57 dead / 113 alive.** [Consolidated report](MASSACRE_V3_FULL_SIMULATION.md).

- [Full chronology](01_v3_full_chronology.png) / [SVG](01_v3_full_chronology.svg)
- [Blood incidents and actual path](02_v3_blood_incidents.png) / [SVG](02_v3_blood_incidents.svg)
- [Blood resource and power](03_v3_blood_power.png) / [SVG](03_v3_blood_power.svg)
- [Physical search network progression](04_v3_search_network.png) / [SVG](04_v3_search_network.svg)
- [Bone attention and incidents](05_v3_bone_incidents.png) / [SVG](05_v3_bone_incidents.svg)
- [Son-killer guard sequence](06_v3_guard_sequence.png) / [SVG](06_v3_guard_sequence.svg)
- [Shelters, splits and forced movement](07_v3_shelter_movement.png) / [SVG](07_v3_shelter_movement.svg)
- [Boundary contacts and local knowledge](08_v3_barrier_knowledge.png) / [SVG](08_v3_barrier_knowledge.svg)
- [Witch route and height profile](09_v3_witch_route.png) / [SVG](09_v3_witch_route.svg)
- [Mayor final minute](10_v3_mayor_minute.png) / [SVG](10_v3_mayor_minute.svg)
- [Casualty progression](11_v3_casualty_progression.png) / [SVG](11_v3_casualty_progression.svg)
- [Final aftermath / survivors](12_v3_final_aftermath.png) / [SVG](12_v3_final_aftermath.svg)
- [Environmental-story seeds](13_v3_story_seeds.png) / [SVG](13_v3_story_seeds.svg)

## Orientation and editing

North/uphill is map +Y = UE +X. East/right is map +X = UE +Y. Metres; elevation is gate-relative. Survey geometry comes from parent map_data.json. Door/floor approximations are separate. This is not validated UE collision.

[Clean base](../01_village_base_map.png), [blank planning map](../02_massacre_planning_blank.png), [T0](../03_T0_normal_activity.png), [approved T90](../T1_BONE_COMPLETION.md), [V1 history](../MASSACRE_FULL_SIMULATION.md) and [V2 history](../v2/MASSACRE_V2_FULL_SIMULATION.md) remain separate.

PNG is for review; SVG/JSON/JSONL/CSV are editable. Preserve the closed hash-identified branch. Future changes belong in another experiment.

Run python render_v3.py to regenerate sheets. Run python reproduce_v3.py --work NEW_EMPTY_DIRECTORY to reproduce in scratch from the six parent inputs. Requires Python, NumPy, Shapely, Matplotlib and Pillow. These scripts never open or change UE.
