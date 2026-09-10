# V4 review maps

**MASSACRE SIMULATION V4 — INDEPENDENT RE-SIMULATION FROM T+90**

**100 dead; 70 survivors; 10 injured survivors. Failed experimental pass. Do not implement in UE5.** Read the [full simulation and limitations](MASSACRE_V4_FULL_SIMULATION.md) and [validation](v4_validation.json), including the two-worker source-allocation error.

Up is UE+X/uphill; right is UE+Y. Distances are plan metres; Witch route timing includes surveyed heights. Geometry is the existing 9 September survey, not a new scene capture. Small interior/threshold positions are provisional. The 8 m network proximity coverage is not actual omniscient detection.

[Combined overview of all sixteen sheets](00_v4_contact_sheet.png).

The clean [base](../01_village_base_map.png), [blank planning copy](../02_massacre_planning_blank.png), T0/T1 and V1/V2/V3 remain separately available.

| Map | Editable vector |
|---|---|
|[Full chronology](01_v4_full_chronology.png)|[SVG](01_v4_full_chronology.svg)|
|[Blood body path](02_v4_blood_body_path.png)|[SVG](02_v4_blood_body_path.svg)|
|[Blood power and accessible resource](03_v4_blood_power.png)|[SVG](03_v4_blood_power.svg)|
|[Distributed search network](04_v4_distributed_network.png)|[SVG](04_v4_distributed_network.svg)|
|[Search memory and frontier](05_v4_search_memory_frontier.png)|[SVG](05_v4_search_memory_frontier.svg)|
|[Bone attention and relocation](06_v4_bone_attention_route.png)|[SVG](06_v4_bone_attention_route.svg)|
|[Bone direct and indirect consequences](07_v4_bone_consequences.png)|[SVG](07_v4_bone_consequences.svg)|
|[Son-killer guard sequence](08_v4_guard_sequence.png)|[SVG](08_v4_guard_sequence.svg)|
|[Shelters and civilian movement](09_v4_shelter_civilian_movement.png)|[SVG](09_v4_shelter_civilian_movement.svg)|
|[Cumulative structural cover](10_v4_structural_damage.png)|[SVG](10_v4_structural_damage.svg)|
|[Barrier contact and local knowledge](11_v4_barrier_knowledge.png)|[SVG](11_v4_barrier_knowledge.svg)|
|[Witch: one destination](12_v4_witch_route.png)|[SVG](12_v4_witch_route.svg)|
|[Mayor: the final minute](13_v4_mayor_final_minute.png)|[SVG](13_v4_mayor_final_minute.svg)|
|[Casualty progression](14_v4_casualty_progression.png)|[SVG](14_v4_casualty_progression.svg)|
|[Final aftermath and survivors](15_v4_final_aftermath.png)|[SVG](15_v4_final_aftermath.svg)|
|[Environmental storytelling seeds](16_v4_environmental_seeds.png)|[SVG](16_v4_environmental_seeds.svg)|

Run `python render_v4.py` beside these files to regenerate presentation sheets from the frozen JSON and the unchanged parent map_data.json/t1_simulation.json. Requires matplotlib and shapely. Edit the annotation data/SVG for review; rerendering does not invent new events or repair census consistency automatically. The frozen canonical dataset, phase ledger, cycle states and person ledgers preserve editability without claiming a probabilistic or exact physics replay.

V4 closed before any V1/V2/V3 post90 files were read. CLOSURE.json records its digest. Earlier files are preserved in place and in Git history. Stop at the Mayor's final death; no post-terminal cleanup is authorized.
