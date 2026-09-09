# Review-only repository workflow

This repository is the shared visual reference for the UE5 village. Its only purpose is design review. The user has requested that visual reviews be committed and pushed here when asked; routine publication of those requested review images and notes is already authorized.

## Scope

Keep the actual Unreal project in its existing location. Never copy, move, restructure, initialize Git in, or push the UE project as part of this repository's update workflow. Do not add source geometry, assets, plugins, builds, UE packages, Blender files, caches, logs, credentials or unrelated material. Repository operations must explicitly target this checkout. Keep existing visibility unless the user asks to change it.

## On each requested village visual review

1. Read `REVIEW.md`, inspect the current UE scene through the established engine connection, and capture the requested views. Do not claim old files are fresh captures.
2. Prepare a complete review package outside `latest/` first. Maintain camera composition and descriptive filenames when useful. Default PNGs to a maximum width of 1600 px while preserving aspect ratio and full framing. Keep source-resolution captures outside this repository.
3. For a major milestone, preserve the previous `REVIEW.md`, manifest and `latest/` under `archive/YYYY-MM-DD_HHMMZ_short-milestone/` before replacement. Do not duplicate every small update.
4. Replace the images in `latest/` with the new requested set; remove superseded images so old views cannot masquerade as current ones. Keep stable identifiers below; add new views starting at 12. Do not renumber existing views to fill gaps. If a requested set omits a usual view, explicitly list that omission in `REVIEW.md`.
5. Update `REVIEW.md` with capture date/time and timezone, changes since the preceding review, a caption and embedded link for every screenshot, relevant implementation/composition decisions and known issues/unfinished areas. Distinguish observed work from plans. Record temporary exposure or other inspection settings. Update a small `latest/manifest.json` with camera/capture provenance and hashes when available; never include credentials or personal local paths.
6. Inspect the actual images and rendered/embedded links. Verify tracked files are only Markdown, review PNG/JPEG/WebP and small manifests; aim for at most 15 MB per latest package and no single file over 5 MB. The `.gitignore` is an allowlist, not a substitute for inspecting the staged file list.
7. Commit and push this review repository. Prefer one coherent commit per review. Never force-push routine reviews. If another contributor changed the remote, reconcile without losing their review material. Connector Git blob/tree/commit operations are acceptable when local Git authentication is unavailable.
8. Read back the remote branch commit and directory/manifest to verify the images and notes reached GitHub. Report owner/name, commit hash, and any real access limitation. Never report local staging or a queued upload as a successful push.

## Stable view filenames

- `01_aerial.png`
- `02_title_approach.png`
- `03_village_centre.png`
- `04_cemetery.png`
- `05_witch_house.png`
- `06_mayor_approach.png`
- `07_disturbed_graves.png`
- `08_cemetery_reserve.png`
- `09_family_yard.png`
- `10_cart_service.png`
- `11_cellar_threshold.png`
- Optional `00_contact_sheet.png` for a combined overview; its labels should match these identifiers on future captures.

Read the active request for scope. Do not make scene changes, create a massacre pass, or implement progression merely to prepare a review.

## Top-down planning map reviews

The user requested a high-resolution orthographic planning reference derived from the current scene, with an identical clean event-planning copy. `latest/map/` is a review-only exception permitting editable SVGs, metric 2D JSON and the small map renderer alongside PNGs/Markdown. Never include raw live actor dumps, UE packages or 3D meshes. Preserve the shared coordinate convention, scale, feature IDs and geometry hash. A map-only addition can retain earlier perspective images with their original dates. Archive an earlier map set before replacing it at a meaningful milestone. Keep event layers empty until the user collaboratively authors/authorizes the massacre plan. Do not apply map annotations to the UE scene automatically.

T0 ordinary population/activity belongs in `t0_activity.json` and its dedicated SVG/PNG, notes and renderer. Population clusters, micro-groups and ordinary movement must reconcile without double counting. Keep clean base sheets and future event layers unchanged. Do not proceed to the next massacre planning step until the user requests it.


T1 first-90-second planning belongs in `t1_simulation.json` and its dedicated PNG/SVG, timeline, CSV, notes and renderer. The user authorized this chronological 2D layer and its review publication only. Keep the original 15 base/T0 files byte-identical; never backfill T1 into the clean event template or approved T0. No UE edits are implied. Stop at +90 until the user requests Step 3. Resolve documented handoff assumptions before further simulation. T1 is an additive review, so earlier maps remain directly available without a duplicate archive. Small T1 JSON/CSV and renderer files are part of the review-only exception above.
