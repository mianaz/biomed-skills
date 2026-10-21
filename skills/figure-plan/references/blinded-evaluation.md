# Test a figure-planning change

Read this before preparing a benchmark. Separate story planning, panel plotting,
geometry and final rendering. A gain in one does not establish a gain in all.

## Freeze and isolate

1. Select development and test papers before deriving rules. Split by study,
   including companion supplements and reused data. Preserve exclusions and
   unavailable files. A paper-disjoint set is not certified unseen to a model.
2. Freeze the skill, task packet, comparator and evaluation definitions. Keep
   original figures, captions, placements and paper identities outside the task
   packet. Use opaque IDs and a recorded shuffle seed. Retain scientifically
   necessary labels even if they can identify a study to a human.
3. Run in a fresh sandbox with only the assigned instructions and inputs. Disable
   network in the model's execution tools and verify protected-file and network
   access fail there. A text-only planner can instead use a closed execution host;
   record that no file/network tool executed, and test the file boundary separately.
   Keep a cloud model's inference connection distinct from tool network access;
   this is not offline inference. Do not change the user's global connectivity.
   Record runtime/provider context, including advertised but unavailable tools;
   an assistant that prepared the references cannot be called an independent
   blinded evaluator. A deterministic program has no LLM instruction condition.
4. Inspect outputs before unblinding. Compare with the original only after the
   candidate is saved. Test cases used to revise the rule become development
   cases for that revision; retain the result under its frozen version.

**Done:** the exposure record states exactly what the generator and reviewer saw,
which restrictions were tested, and whether the result was frozen before reveal.

## Choose the test that answers the question

| Test | Allowed input | What it can test |
|---|---|---|
| Geometry | Independent letter-free assets, dimensions, canvas | Packing, consistent scale, preservation and rendering |
| Group-aware layout | Geometry input plus neutral evidence groups/order | Whether relationships survive assembly |
| Story planning | Manuscript/results and available evidence; original figure assignments withheld | Claims, figure sequence, main/supporting choices |
| Source-data-only | Actual data, necessary units/design, permitted methods | Plot choice, statistical meaning and reproducible panels |

Do not reconstruct values from screenshots and call them source data. Keep a
source-data coverage ledger: a workbook can contain some numeric panels while
omitting images, schematics or a complete experiment. Missing inputs become
placeholders. Historical development datasets remain development replays.

A 2026-10-14 pilot used 34 randomized panels from four figures in two other papers.
Its frozen geometry rule reduced unused space against an equal-cell grid and
kept a common scaling factor, but broke scientific neighbours and did not solve
source-font readability. It is evidence about that packing implementation only;
it does not validate an LLM's use of this skill or replace a group-aware test.

## Evaluate separately

Report by figure and paper, not with each panel treated as an independent study:

- Evidence: missing/cropped content, distorted geometry, unsupported new content.
- Assembly: stable IDs resolve to source assets. A plan that substitutes display
  letters for IDs can still have readable prose but fail reproducible assembly.
- Argument: claim support, required comparisons, alternative explanations,
  main/supporting rationale, design–result and image–quantification adjacency.
- Readability: effective font by role, source resolution, legend/scale-bar survival.
- Layout: overlap, overflow, external whitespace, gutters, scale variation.
- Rendering: independent PPT panel/letter objects and the actual exported page.
- Preference: blinded human judgments with randomized left/right display if run.

Original-neighbour retention or resemblance is descriptive, not a beauty score.
Use fixed-size side-by-side previews and show failures. Report the comparator,
per-paper results and unmeasured endpoints; do not hide them in one total score.
If a common renderer fixes fonts, colors or plotting code, treat those as shared
controls rather than capabilities demonstrated by one instruction condition.
Keep invalid outputs visible; any repaired replay is a separate development run.

**Done:** the result supports a specific change, leaves a recorded failure, or
shows no gain. A general skill-performance claim needs an independent agent test
and a fresh test set after optimization.
