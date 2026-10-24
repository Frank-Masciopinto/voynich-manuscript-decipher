# h54 — picture order with astronomical and cosmological sky sections

**Verdict: order_ok_fragile** (2 of 3 pre-registered predictions: P1 and P3 pass; P2 fails).  
This is **not** a translation. The test folds astronomical and cosmological pages into the h53 hybrid *picture program* as a mid-book calendar/sky block and asks whether that order is quire-robust.

Pre-registration (committed before any statistic): [PREREG.md](PREREG.md) (commit `251b17d`).  
Results: [results/summary.json](results/summary.json), [results/measurements.json](results/measurements.json).

## Predicted primary order (fixed in PREREG)

`herbal` < `sky_mid` < `biological` < `pharmaceutical` < `stars`

where `sky_mid` = pages with `section ∈ {astronomical, cosmological, zodiac}`.

## What we measured

| Pred | Test | Result | Key numbers |
|---|---|---|---|
| P1 | Primary sky_mid order vs 1000 rank permutations; contrasts S1–S4 | **Pass** | Spearman ρ = 1.00, Kendall τ = 1.00, p = 0.008. Means: herbal 72.7 → sky_mid 133.5 → biological 153.9 → pharmaceutical 188.3 → stars 205.0. S1 (7-role) ρ = 1.00 p = 0.000; S2 (sky_mid_early, drop Q14 cosmo) ρ = 1.00 p = 0.009; h53 five-step ρ = 1.00 p = 0.010; h52 menstrual ρ = 0.20 p = 0.460. |
| P2 | Quire bootstrap 5th-percentile ρ > 0.6 and every evaluable LOQO ρ > 0.6 | **Fail** | Bootstrap median ρ = 1.00 but p5 = 0.40 (72 % of draws ρ > 0.6). LOQO: drop Q20 → stars mean falls to 112.5 (only the two early Q8 star pages), ρ = 0.40; drop Q13 removes biological (not evaluable). All other LOQO ρ = 1.00. |
| P3 | If P1 and means strictly increasing, revise hybrid picture story to calendar-block form | **Pass** | Means strictly increasing. Revised story: plants → calendar/sky block (astr ∪ cosmo ∪ zodiac) → baths → pharmacy → stars. Caveat from P2: `stars` is bimodal (2 pages in Q8 at ord ≈ 112–113 + 23 in Q20); without Q20 the late-stars slot fails. Cosmological also straddles (Q8–10 mid-book + 3 pages in Q14 after baths). |

## Plain verdict

Folding astronomical and cosmological pages into a **mid-book sky_mid block** matches the book’s mean page order as well as h53’s five-step map did, and still beats the h52 menstrual order. The hybrid *picture* story should be revised to that interleaved calendar-block form — but only as a description of full-book means. The order is **not quire-robust**: it leans on Q20 dominating the stars mean, and biological lives in a single quire (Q13). Early Q8 “stars” pages and Q14 cosmological diagrams sit outside a clean linear handbook sequence.

No hand covers the full program (sky/zodiac ≈ hand 4; baths ≈ hand 2; Q20 stars ≈ hand 3). Within hand 4, astronomical (122.5) < cosmological (127.2) < zodiac (137.5).

## Limits

- Picture-order only; h53 process-text side not re-tested.
- Section and quire nearly coincide for biological and for Q20 stars.
- One binding/`quires.csv` map. **Nothing here decodes MS 408.**

## Reproduce

```bash
PYTHONPATH=src python hypotheses/h54_picture_order_with_sky_sections/run_h54.py
PYTHONPATH=src python -c "import sys; sys.path.insert(0,'hypotheses/h54_picture_order_with_sky_sections'); import test_h54 as t; t.test_spearman_and_kendall_helpers(); t.test_role_mask_sky_mid(); t.test_score_predictions_verdicts(); t.test_prereg_and_saved_outputs(); print('ok')"
```
