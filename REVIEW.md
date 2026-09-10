# MASSACRE SIMULATION V2 — RE-SIMULATED FROM T+90

**112 fatalities, 58 survivors, no injured survivors. This remains a NARRATIVE / RULE FAILURE for the intended near-total massacre.**

The Witch reaches and secures the Mayor at **T+313.923**, keeps him helpless for a fixed sixty seconds, then personally kills him at **T+373.923**. He is the final death. All remaining survivors are reported; no post-Mayor cleanup is authored.

Prepared 2026-09-10T08:50:24.981064+00:00. This is a new 2D planning branch. **UE5 is unchanged; no new editor screenshots were captured.**

![V2 final aftermath planning map](latest/map/v2/11_v2_final_aftermath.png)

## Current review

- [V2 index: all twelve PNG/SVG sheets](latest/map/v2/README.md)
- [Full chronology, every event and action/reaction cycle, survivor reasons and V1 comparison](latest/map/v2/MASSACRE_V2_FULL_SIMULATION.md)
- [Full chronological map](latest/map/v2/01_v2_full_chronology.png)
- [Blood incidents](latest/map/v2/02_v2_blood_incidents.png) and [power growth](latest/map/v2/03_v2_blood_power_growth.png)
- [Bone pattern](latest/map/v2/04_v2_bone_pattern.png) and [son-killer guard sequence](latest/map/v2/05_v2_bone_guard_sequence.png)
- [Witch route](latest/map/v2/06_v2_witch_route.png) and [final-minute timeline](latest/map/v2/07_v2_mayor_final_minute.png)
- [Civilian movement](latest/map/v2/08_v2_civilian_movement.png), [barrier knowledge](latest/map/v2/09_v2_barrier_knowledge.png), [casualty progression](latest/map/v2/10_v2_casualty_progression.png)
- [Environmental story seeds](latest/map/v2/12_v2_story_seeds.png)

## What changed

Only the approved T+0–90 history is input. V1's post90 events, knowledge, movement and outcomes are excluded. V2 uses accessible spilled blood, limited growing living-blood sensing, prolonged recognition of the entrance guard, independent local barrier discoveries, and a fixed final minute. There are 157 separately retained ACTION/REACTION pairs.

Blood causes more deaths, but local coverage leaves eight survivor pockets. Bone spends forty-eight seconds tormenting the recognized guard, then kills him precisely. The Witch ignores three appeals and continues uphill. The bell begins independently at +93.92 and communicates only emergency.

Compared **after V2 closure**, V1's 73 dead / 97 alive becomes 112 dead / 58 alive. This still fails the intended near-total premise. The final minute includes eighteen Blood deaths plus the Mayor. A frozen-state diagnostic does not establish rage amplification alone as necessary for those eighteen exposures.

## Editable data and limits

[Consolidated JSON](latest/map/v2/v2_simulation.json), separate [actions](latest/map/v2/v2_actions.jsonl) / [reactions](latest/map/v2/v2_reactions.jsonl), individual [casualties](latest/map/v2/v2_casualties.csv) / [survivors](latest/map/v2/v2_survivors.csv), local knowledge, movements, resources, parameter files and small offline scripts are included.

[Validation](latest/map/v2/v2_validation.json) checks census, unique deaths, resource conservation, local range/exposure, the exact final minute and source preservation. [Manifest](latest/map/v2/v2_manifest.json) records artifact hashes. 2D roofs, doors/interiors, hearing, sensing and force remain planning approximations, not tested UE physics. The failed survivor outcome is provisional, not newly approved lore. Later barrier/Witch fate and cessation of danger remain unresolved.

## Preserved references

[Clean base](latest/map/01_village_base_map.png), [blank canvas](latest/map/02_massacre_planning_blank.png), [T0](latest/map/03_T0_normal_activity.png), [T1](latest/map/t1_simulation.json) and [Bone completion](latest/map/bone_completion.json) remain byte-identical. All V1 files remain in [the parent map folder](latest/map), as historical comparison only. [Previous V1 review at its immutable commit](https://github.com/Slav-Storm/UE5-Village-Review/blob/431c59298f5f1cfb372b3e03e788dd4c1efebf24/REVIEW.md) preserves the former review page.

Existing perspective screenshots keep their original capture dates. This additive V2 folder does not replace any old image set; no duplicate archive of large images is needed.

**STOPPED for V2 review. No UE implementation, assets, destruction, corpses, VFX, bosses, cutscenes or rebuilding.**
