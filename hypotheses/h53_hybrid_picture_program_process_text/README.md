# h53 — hybrid working theory: picture program (A) + process text (D)

**Verdict: hybrid supported** (4 of 4 pre-registered predictions).  
This is **not** a translation. The test asks whether MS 408 can be described as an astrological herbal / spa *picture program* whose *body text* behaves like the no-plaintext page-and-line copy process (h47), rather than as plaintext sentences carrying that program.

Pre-registration (committed before any statistic): [PREREG.md](PREREG.md) (commit `8c88225`).  
Results: [results/summary.json](results/summary.json), [results/measurements.json](results/measurements.json).

## The hybrid, in plain words

- **Pictures (Theory A):** one handbook layout — plants early, zodiac/calendar mid-book, baths, then pharmacy jars, then stars/cosmos late.
- **Writing (Theory D):** the words mostly follow a page-and-line copy-and-edit process; they do not show positive word-order syntax, and section identity does not carry meaning in the vocabulary beyond hand and quire effects.

## What we measured

| Pred | Test | Result | Key numbers |
|---|---|---|---|
| P1 | Section mean page-order matches medical-calendar order better than 1000 random rank permutations | **Pass** | Spearman ρ = 1.00, Kendall τ = 1.00, p = 0.005. Means: herbal 72.7 → zodiac 137.5 → biological 153.9 → pharmaceutical 188.3 → stars 205.0. h52 menstrual order contrast: ρ = 0.20, p = 0.453 (still fails). |
| P2 | Body text is process-like (D1 ≤ 0 raw and de-padded; within-folio drift like copier not Italian; h47 PLC ≥ 5/6 on ≥ 2 hands) | **Pass** | Raw D1 −0.18/−0.14/−0.17; local_W25 D1 −0.22/−0.23/−0.24 (all ≤ 0). h48 D1 passes 1A/2B/3B; Boccaccio S_edit = −0.0006 (fails). `page_line_copier` 6/6 on all three hands (h47). |
| P3 | Section predicts illustration/quire coding, not word bags beyond hand×quire | **Pass** | Section↔illustration match = 1.00. h10 unique section R² = 0.025 ≤ 0.05 (quire unique 0.068, hand 0.015). |
| P4 | Thin A residual: picture order + Roman months / image typology only; label↔text stays null | **Pass** | h51 L1 and L2 both false (edit1 Holm p ≈ 0.46; same-plant p ≥ 0.089). No EVA glosses invented. |

## Plain verdict

The **hybrid is supported as a working theory**: the drawings line up with a medical-calendar / spa handbook program, while the writing matches the process-text side already established in h47–h51. The failed h52 “blood → plants → yoga” order is a useful contrast — that narrative order does not fit; this handbook order does, *on the pictures*, without needing the words to mean remedies.

## Limits

- T2/T3/T4 **reuse** stored h10/h47/h48/h49/h51 summaries; only T1 and the section↔illustration check are newly computed here.
- Astronomical (mean ord ≈ 122) and cosmological (≈ 137) sit mid-book near the zodiac; primary P1 uses the five-role order without them. Sensitivity A2 (stars∪cosmological as sky_late) is reported in `measurements.json`.
- Section and quire nearly coincide (biological = Q13 only), so “picture program” and binding structure are entangled.
- One transcription (ZL3b). **Nothing here decodes MS 408.**

## Reproduce

```bash
PYTHONPATH=src python hypotheses/h53_hybrid_picture_program_process_text/run_h53.py
PYTHONPATH=src python -c "import sys; sys.path.insert(0,'hypotheses/h53_hybrid_picture_program_process_text'); import test_h53 as t; t.test_spearman_and_kendall_helpers(); t.test_score_predictions_verdicts(); t.test_prereg_and_saved_outputs(); print('ok')"
```
