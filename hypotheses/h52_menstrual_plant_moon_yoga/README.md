# h52 — menstrual blood → plants / moon periods / end-yoga reading

**Verdict: no match** (0 of 6 pre-registered predictions).  
This is **not** a translation. The test asks whether the manuscript’s section order, vocabulary links, zodiac cycling, published cribs, and end-section register fit that thematic story better than chance. They do not.

Pre-registration (committed before any statistic): [PREREG.md](PREREG.md).  
Results: [results/summary.json](results/summary.json), [results/measurements.json](results/measurements.json).

## The claim, in plain words

Women create plants without male sperm: menstrual blood put in water flowers into plants; each moon period a different plant; the end of the book is a yoga-like science.

## What we measured

| Pred | Test | Result | Key numbers |
|---|---|---|---|
| P1 | Book order = water → moon → plants → end yoga | **Fail** | Spearman ρ = 0.20 vs null p = 0.45. Observed mean page ranks: plants 85, moon 138, water/baths 154, end stars 213 — plants come **first**, baths **after** the zodiac. |
| P2 | Bath pages share vocabulary with plant pages beyond hand nulls | **Fail** | Nymph/tube label stem-hit into same-hand herbal = 0.89 vs null mean 0.93 (p = 0.98). h09 water within-quire Holm min = 1.0. |
| P3 | Zodiac pages cycle with plant vocabulary | **Fail** | Zodiac labels are **less** like herbal text than like stars (sim 0.579 vs 0.592); herbal similarity vs random pools p = 0.97. Adjacent-zodiac similarity p_cycle = 0.0125 alone is not enough (needs plant link too). |
| P4 | Published female/water cribs beat seed cribs and survive within-quire | **Fail** | h09 water/nymph words *are* more enriched on biological pages than root words on herbal (Δ log₂ rate 3.11, p ≈ 0), and h01 `qo` (“seed”) is not herbal-enriched — but **neither water nor nymph list survives within-quire Holm** (both 1.0). Quire artefact, not a meaning. |
| P5 | End (Q20 stars) looks like a distinct instructional / yoga register | **Fail** | 0/4 metrics differ from Q8 stars after Holm. Word bigram gain D1 on Q20 (−3.42) matches length-matched early herbal (−3.41); gap −0.009 ≪ +0.05 bar. |
| P6 | Water vocabulary predicts later plant text on the same bifolio | **Fail** | Only **1** bifolium mixes water-tagged and plant pages. Forward−reverse = +0.20, p = 0.51. |

## Nearby readings that fit better

- **Baths as their own section (spa / balneology drawings):** biological = quire 13 only; no extra text link to herbal beyond hand/quire effects (h09, h10, T2).
- **Zodiac as a calendar with Roman month names:** circle centres are later Roman-script months (h05), not Voynichese plant names; no plant cycling (h06, T3).
- **Pharma as jars / roots:** image-object structure without a menstrual story (h09).
- **End stars as more copy-structured text:** Q20 matches the same line/copy regime as the rest of the book (h30, h47, T5), not a separate “yoga science” register.

## Limits

- No EVA→English glosses were invented. “Blood”, “sperm”, and “yoga” have no published crib list to test, so those words were never assigned.
- T6 is almost empty: plant quires and the bath quire barely share bifolia.
- High zodiac↔plant *label-set* overlap in T3 is partly a set-size effect (large plant label pool vs tiny star-label subtype pool); the pre-registered similarity-to-running-text test is the one that fails.
- One transcription (ZL3b). Nothing here decodes MS 408.

## Reproduce

```bash
python hypotheses/h52_menstrual_plant_moon_yoga/run_h52.py
python -m pytest hypotheses/h52_menstrual_plant_moon_yoga/test_h52.py -q
```
