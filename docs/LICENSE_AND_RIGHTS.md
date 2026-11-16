# Data, software, and model licensing review (16 November 2026)

**Status: unresolved author/legal decision. Do not publish as open-source licensed until resolved.**

### FPSD dataset

Original dataset: https://github.com/Yanhui-Struggle/FPSD

The accessible public FPSD GitHub root showed a dataset README, COCO/VOC folders and a paper citation, **without an explicit LICENSE file or a blanket permission statement**. Public download does not automatically authorize mirroring the imagery, TIFF arrays, COCO annotations, cropped chips or derived caches. We therefore **link to the upstream source and do not redistribute its files**. This determination only concerns the inspected upstream repository; ask the maintainers for clarification if redistribution or image examples are desired.

### YOLO / Ultralytics

Ultralytics' current license page, https://www.ultralytics.com/license, explains AGPL-3.0 versus Enterprise options for its code and trained/fine-tuned models. It states that certain derivative open-source workflows must comply with **AGPL-3.0** requirements, potentially including corresponding application source and model weights. This research repo deliberately excludes Ultralytics vendor code and original detector weights; its optional full-FPSD path imports \`ultralytics\` when the user installs it.

**Do not assume omission of binaries automatically resolves AGPL compliance.** The project owner and coauthor must choose a licensing/distribution strategy compatible with all incorporated dependencies and code provenance. Consult the upstream terms, including https://docs.ultralytics.com/help/contributing, before choosing a project license.

### Author code ownership

Authorship of the paper is not automatically proof that one researcher alone holds all software licensing rights. Confirm contribution provenance, university/workplace IP agreements where applicable, and any coauthor permissions **before** adding an author-approved LICENSE.

### Public code release versus full data replication

A code-only public repository can document what is and is not reproducible without embedding raw data/weights. It must not promise an out-of-box raw-FPSD reproduction when original dataset and stage-one detector assets are external.

No specific code license has been approved. **The repository intentionally has no \`LICENSE\` file at present.** Making a repo public without one is not an open-source license.
