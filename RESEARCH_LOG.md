# Research log — everything tried on MS 408, in order

This is the single running log of every stage in this repository: what was asked, what was done, what came out, and where it led. **Nothing here is a translation.** Detailed numbers are in [FINDINGS.md](FINDINGS.md) and in each linked report or hypothesis README. Dates and times are Europe/Warsaw, taken from `git log`.

Status key:
- **closed**: answered; nothing more is planned.
- **lead**: a result worth following up.
- **open**: unanswered or blocked.

## Dead ends (closed, negative)
- **The tone sheet:**
  - The "Codex Translation Sheet" is not a translation table (h01).
  - No tone or pitch map extends it to the whole script (h02, h03).
- **Zodiac cribs:** the circle-centre words are later Roman-script month names, and no label matches any sign or month name list (h05).
- **Drawing cribs:**
  - Word–drawing links are section and quire effects; none survives with quire held fixed (h09, h10, h13).
  - Pharmaceutical labels don't resemble their "same plant" herbal folio (h09, h17).
  - Same-genus or same-family folios don't share first words or vocabulary (h17).
  - Bax's `keerodal` / Apiaceae similarity fails out of sample (h18).
- **Section models:**
  - A topic-plaintext codebook doesn't predict an unseen section better than a setting switch or a global baseline (h07).
  - Section vocabulary is not above drift once quires are resampled (h08, h10).
- **Copy-modify:** the copy step is inert in per-hand copy-modify fits; the gain comes from the word grammar (h12).
- **Italian plaintext under the real Naibbe tables (h27):** shuffling Boccaccio, or replacing it with Zipf nonsense on the same letter frequencies, leaves the likelihood-fingerprint match. The tables and the copy layer carry it. The plaintext does not.
- **One cut of the Naibbe tables (h28):** shuffling which letter owns which string, which strings are prefixes versus suffixes, or the order of units inside each string each takes the fingerprint outside the match rule. The order cut is the large one. No one of the three is the sole carrier.
- **A decodable toy table hitting MS's D4 window (h29):** three length × suffix-pool settings are ≥0.8 decodable and clear the D4 floor of −0.07, but their D4 (+0.38 to +0.48) is above the MS band. No setting of the 25 reproduces the five-statistic fingerprint.
- **Transcription moving the fingerprint (h40):** across ZL3b, IT2a and RF1b, D1–D5 stay inside the h20 tolerances and the last-glyph link stays far above the generators. The space-predictability target does move: for hands 2B and 3B it sits above 0.80.
- **First-line copy seeding or open-spread copying across folios (h46):** folio-opening first lines have a *lower* one-edit pair rate with later lines on the same folio than interior lines do (`seed − interior` = −0.017 to −0.024 across all three hands), and cross-folio one-edit rates across a visible open spread (`v → r`) are no higher than across a page turn (`r → v`).
- **De-padded seed skeleton syntax (h49):** stripping same-folio exact repeats and one-edit echoes (`local_W25` or `folio_comp`) does not uncover positive word-order syntax ($D_1 = -0.22\text{ to }-0.24$ on `local_W25`), and MS 408's de-padded retention rate, $D_1$, and `morphs_per_type` all match the no-plaintext `page_line_copier` within $\pm 0.08$ across Hands 1A, 2B and 3B.
- **Vertical paragraph/line-initial header or glyph acrostic (h50):** vertical sequences of paragraph-initial words and raw or onset-stripped line-initial words have negative bigram gain ($D_1 < 0$) in all three hands, and vertical line-initial first-unit redundancy ($R_{\text{acro}}$) is only 14–24 % of horizontal within-word redundancy (matching prose controls at 24–40 %).
- **Diagram/plant label links to de-padded paragraph seeds (h51):** matching `L`-locus labels to their own folio's de-padded `seed_W25` tokens via exact, one-edit, or onset-stripped stem overlap shows no enrichment over within-quire folio permutations ($p_{\text{Holm}} = 0.46$), and de-padded herbal–pharmaceutical same-plant pairs do not beat random herbal partners ($p \ge 0.089$).

## Open leads
- **Line structure (h13–h16, h30, h47):**
  - Line-start words are a 2B/3B habit, adding a d-/s- or gallows onset to common words; `am`/`dam`/`dy` end lines in every hand.
  - Modelled in `h47` (`page_line_copier`), which reproduces line-edge concentration, paragraph-initial gallows, and the cross-line junction drop alongside the 5/5 fingerprint, space band, page burstiness, near-repeat decay, and folio-boundary break.
- **Hands (h11, h12, h14, h15):**
  - Hands look like one system with spelling habits (`-edy → -ol`) plus different vocabulary.
  - Word-level evidence for the mapping is weak (it is mostly shared stems).
- **Weak leads from h09:** root/jar words.
- **Section signal (h11):** survives on hand residuals but cannot be separated from quire with this data.
- **Burstiness (h41):** at 10,500 tokens, clustering of the 50 most frequent words separates plain Boccaccio from Naibbe ciphertext, but not a plaintext through the cipher: Naibbe on real, shuffled and nonsense Boccaccio all score 3.4–3.7. The three hands score 5.1–5.2, above plain Boccaccio and every Naibbe arm and C0. New-type rate, lag-100 mutual information and adjacent-block divergence separate nothing.
- **Near-repeat range (h42):** one-edit pairs are absent in Boccaccio and in the h39 graph respelling. Hand 1A drops at gap 21–100, hand 3B at 101–500. Hand 2B is not elevated for adjacent pairs, is elevated at gaps 2–20, and is elevated again at 101–500. C0 drops at gap 2–5. Fitted self-citation and the h39 tuned copier stay elevated through gap 21–100.
- **Page clustering as evidence of content (h44):** fitted self-citation, cut into arbitrary pages of 230 tokens, reaches a burst excess of 1.63, inside the manuscript range of 1.50–1.69. The h39 tuned copier exceeds it (4.76). The excess number does not require a plaintext or real page boundaries.
- **Vowel/consonant account of the glyph link (h45):** in prose controls the Sukhotin split carries a median share of 0.004 of the last-to-first link. The pre-registered sound pattern is not there, so the pen-versus-sound comparison is not scored.
- **Folio boundary (h43, h46, h47, h48):** at a matched distance of 80 tokens, same-folio windows are more alike than cross-folio windows in hands 1A (effect 0.082 vs null 0.059) and 2B (0.100 vs 0.074). Short-lag (`6–20`) one-edit pair rates also drop across folio boundaries in all three hands (`h46`). Inside each folio (`h48`), similarity is not a stationary page palette alone: both one-edit rate ($z = 5.2\text{–}11.5$) and unit-3gram cosine ($z = 10.5\text{–}19.1$) decay significantly with line distance $\Delta\ell$ against a within-folio line-order permutation null, decomposing short-lag same-folio one-edit excess into roughly half folio-level vocabulary palette (37–63 %) and half top-to-bottom sequential copy drift (37–63 %). Adding a partial folio-buffer reset (`rho_keep = 0.15`) and line-boundary slot framing to a no-plaintext copier (`h47`) passes all 6 benchmark families simultaneously across hands 1A, 2B and 3B.
- **Not yet attempted:**
  - A pharma label ↔ grid layout from the scans, so h17 test A can be redone on individual labels.
  - The image-stage glyph check on higher-resolution scans.

## How to add an entry
1. **Where:** append at the bottom (newest last) and use the next `L` number. If the entry changes the summaries above, update them in the same PR.
2. **Fields:** date (Europe/Warsaw), ID + title + folder link, question, what was done, result + verdict (one or two lines), key commits, status (closed / lead / open), what it led to.
3. **Sources:** only report what the linked code or README shows. Put numbers in FINDINGS.md and link them; don't invent or round in a way that changes a verdict.
4. **Requirement:** every PR that adds or changes analysis must add or update an entry (see [CONTRIBUTING.md](CONTRIBUTING.md)).

---

## Entries

### L01 · 2026-10-11 15:33 · Setup: repo, source PDF, workflow
- **Folder:** [source/](source/), [docs/WORKFLOW.md](docs/WORKFLOW.md), [docs/PRIOR_WORK.md](docs/PRIOR_WORK.md), [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md)
- **Question:** what is the source, and what should a decipherment workflow look like?
- **Done:**
  - Downloaded the Yale PDF (214 pp) and split it in two to stay under GitHub's 100 MB file limit (`scripts/join_pdf.sh` rejoins them).
  - Wrote a staged workflow (catalogue letters → word structure → word classes → …) and surveys of prior work and data sources.
- **Result:** infrastructure only.
- **Commits:** aeb98d1, 4196fbd
- **Status:** closed
- **Led to:** L02

### L02 · 2026-10-11 15:59 · Transcription data, IVTFF parser, glyph catalogue, descriptive statistics
- **Folder:** [src/msdecipher/](src/msdecipher/), [glyphs/REPORT.md](glyphs/REPORT.md), [reports/stats_report.md](reports/stats_report.md)
- **Question:** which letters are used, and what does the text look like statistically?
- **Done:**
  - Built a fetch script with a SHA256 manifest for voynich.nu transcriptions (ZL3b primary; IT2a, RF1b, GC2a). They are git-ignored because no licence is stated.
  - Wrote an IVTFF 2.0 parser, unit segmentation and the glyph catalogue.
  - Computed Zipf, Heaps, entropies, positional stats, Currier A/B and a Sukhotin test.
- **Result:** descriptive only.
  - 27 EVA symbols plus 85 rare codes.
  - Zipf s 0.985, h2 2.22, h3 1.95.
  - Currier A/B differ (this checks consistency with Currier's own classification).
- **Commits:** b40125e, 4582c0c, f31792d, 4eaffb9
- **Status:** closed
- **Led to:** L03, L04

### L03 · 2026-10-11 16:01–16:34 · Image stage (scans → folio index → glyph candidates)
- **Folder:** [docs/IMAGE_STAGE.md](docs/IMAGE_STAGE.md), [reports/image_stage/REPORT.md](reports/image_stage/REPORT.md), `data/page_index.csv`
- **Question:** do the scans support the transcriber's glyph classes?
- **Done:** built a PDF page → folio index, then binarisation, line/word/glyph segmentation, EVA alignment and clustering.
- **Result:** weak and inconclusive (28 pages, proxy metrics). kNN recovers the EVA unit 36% of the time vs 6% chance; no inventory size is supported.
- **Commits:** 0341dff, 07cb118, 57d20f5
- **Status:** open (needs higher-resolution scans)
- **Led to:** —

### L04 · 2026-10-11 16:13–16:49 · Controls: Latin/Italian/German, ciphers, generators, then Hebrew and Arabic
- **Folder:** [docs/CONTROLS.md](docs/CONTROLS.md), [reports/controls/](reports/controls/)
- **Question:** is MS 408 like natural language, simple ciphers or generated text?
- **Done:**
  - Collected public-domain control texts.
  - Applied 12 transformations (abjad, substitution, Vigenère, nomenclator, verbose, anagram…) and 5 generators, then ran a metric suite with verdict screening.
  - Added Hebrew (Sefaria) and Arabic (Tanzil, Muqaddimah) with abjad normalisation.
- **Result:** lexicon metrics don't discriminate. Letter-level entropy is far below every family except anagram and the slot-grammar generator.
- **Commits:** bae9274, d9beb7a, 128306e, 237959d, 037e8f8, d90fa4c
- **Status:** closed
- **Led to:** L05

### L05 · 2026-10-11 17:23 · Hardening: topical Latin controls, jackknife/bootstrap CIs, prediction-interval verdicts
- **Folder:** [docs/CONTROLS.md](docs/CONTROLS.md), [docs/STATS_NOTE.md](docs/STATS_NOTE.md)
- **Question:** do the verdicts survive uncertainty and topic-matched controls?
- **Done:**
  - Added herbal/medical Latin (Pliny, Celsus, Macer, Isidore), Sidrach, Ariosto and Faust.
  - Added size-matched windows, block-jackknife CIs, z and prediction-interval verdicts, and alphabet-size normalisation.
- **Result:** the letter-level outlier result holds (h2 z −6.8 vs natural plaintext).
- **Commits:** 3e47bac, 73de1ed
- **Status:** closed
- **Led to:** L06

### L06 · 2026-10-11 17:45 · Word structure and word classes (stages 6–7)
- **Folder:** [docs/WORD_STRUCTURE.md](docs/WORD_STRUCTURE.md), [reports/word_structure/REPORT.md](reports/word_structure/REPORT.md)
- **Question:** do words have internal slot structure, and are there behavioural word classes?
- **Done:** fitted a learned skip-HMM slot grammar, a prefix-core-suffix model, MDL and a within-word shuffle null; clustered frequent words with stability tests.
- **Result:** position matters unusually much (2.93 bits/type shuffle gap vs natural maximum 1.47), but independent slots aren't enough. Words are suffix-light (21% vs 67–73%).
- **Commits:** 69ec3f5, bec5bb7, 2e33eea
- **Status:** closed
- **Led to:** L07

### L07 · 2026-10-11 18:08–19:02 · Mechanisms: Naibbe, Timm–Schinner, Zattera, Stolfi
- **Folder:** [docs/MECHANISMS.md](docs/MECHANISMS.md), [reports/mechanisms/REPORT.md](reports/mechanisms/REPORT.md)
- **Question:** does any published generating mechanism reproduce the text?
- **Done:**
  - Naibbe cipher with the author's tables.
  - Timm & Schinner self-citation via the authors' Java.
  - Zattera slot alphabet, Stolfi PCFG and a slot-conditioned bigram, all run through the full metric suite.
- **Result:** no mechanism matches everything. Out of 35 metrics: fitted self-citation 23, Naibbe 11–14, Zattera 9, Stolfi 8.
- **Commits:** 44609e1, 24a180e, 992ef96, 990a683, 6d45e3a, 4320b19
- **Status:** closed
- **Led to:** L11

### L08 · 2026-10-11 18:28 · h01 "Codex Translation Sheet" (user-supplied tone/glyph image)
- **Folder:** [hypotheses/h01_tone_sheet/](hypotheses/h01_tone_sheet/)
- **Question:** is the sheet a valid glyph → tone/meaning table?
- **Done:** coverage, unit existence, tone-scale fit vs random, section permutation and predictive tests.
- **Result:** not a translation table. It covers 1% of word types, and its tones fit no better than random (p = 0.39).
- **Commits:** ddab805
- **Status:** closed
- **Led to:** L09

### L09 · 2026-10-11 19:09 · h02 full tone map for every unit
- **Folder:** [hypotheses/h02_full_tone_map/](hypotheses/h02_full_tone_map/)
- **Question:** can the sheet be extended to all letters, by frequency or other orderings?
- **Done:** 39 candidate Hz maps, tested against random-map and shuffle nulls and 13 controls.
- **Result:** hypothesis generation only; nothing is both beyond the nulls and non-circular.
- **Commits:** 247f42a
- **Status:** closed
- **Led to:** L10

### L10 · 2026-10-11 20:25 · h03 slot-grammar tone map
- **Folder:** [hypotheses/h03_slotgrammar_map/](hypotheses/h03_slotgrammar_map/)
- **Question:** does pitch tied to slot position (or slot = syllable) carry information?
- **Done:** slot-tied pitch maps, slot-pattern "chords", held-out gain vs letters and mechanisms.
- **Result:** rising melodies are tautological, slot patterns add nothing beyond letters, and the syllable reading is non-diagnostic.
- **Commits:** d60079d
- **Status:** closed
- **Led to:** —

### L11 · 2026-10-11 20:40–21:26 · Hybrid copy-and-modify model and plaintext-signal test
- **Folder:** [docs/HYBRID.md](docs/HYBRID.md), [reports/mechanisms/hybrid/](reports/mechanisms/hybrid/)
- **Question:** does a cipher-plus-copy hybrid fit, and does a plaintext topic help?
- **Done:** a copy-modify engine with Naibbe / codebook / plaintext-edit encoders, folio-fold fits, held-out suite, and a section-vocabulary test with a drift-aware null.
- **Result:** a 6-parameter hybrid fits 21.7/35 held-out metrics, but the plaintext is not what helps. The no-plaintext C0 reaches 25.3/35.
- **Commits:** 1e904b5, f53d473, b1a28cb
- **Status:** closed
- **Led to:** L13

### L12 · 2026-10-11 20:47 · h05 zodiac pages as cribs
- **Folder:** [hypotheses/h05_zodiac_cribs/](hypotheses/h05_zodiac_cribs/)
- **Question:** are the circle-centre and nymph labels the names of zodiac signs?
- **Done:** 12 pages / 10 signs; affix, length, isomorph and crib-drag tests against 19 name lists.
- **Result:** no cribs. The centre words are later Roman-script month names, and no label matches a name list beyond chance.
- **Commits:** af3cc08
- **Status:** closed
- **Led to:** L13

### L13 · 2026-10-11 22:47–22:56 · h06 section-varying no-plaintext generator; hybrid on the zodiac pages
- **Folder:** [hypotheses/h06_section_null_and_zodiac/](hypotheses/h06_section_null_and_zodiac/)
- **Question:** can a generator without plaintext produce the section signal, and do generators match the zodiac pages?
- **Done:** section-varying pools, units and parameters, plus a random-block null; generators fitted elsewhere were scored on the zodiac pages.
- **Result:**
  - Section-aligned parameters reproduce the section classification accuracy without plaintext (0.68–0.72), but not its JS magnitude.
  - No generator reproduces the zodiac pages.
- **Commits:** 37905ef, 03ade37
- **Status:** closed
- **Led to:** L14

### L14 · 2026-10-11 23:26 · FINDINGS.md master summary
- **Folder:** [FINDINGS.md](FINDINGS.md)
- **Question:** what is established so far?
- **Done:** wrote the summary, hypotheses table, caveats and next steps.
- **Result:** documentation.
- **Commits:** 5a9e9e7
- **Status:** closed
- **Led to:** L15, L16

### L15 · 2026-10-12 17:12 · h08 quire map and quire-level CIs
- **Folder:** [hypotheses/h08_quires/](hypotheses/h08_quires/)
- **Question:** do the results survive resampling by quire instead of 8-page blocks?
- **Done:** built `data/quires.csv`, quire/bifolium resampling and leak-free group folds.
- **Result:** the letter-level findings hold. The section signal weakens: NB 0.723 with quire CI 0.523–0.924 is no longer above drift.
- **Commits:** 79e12aa
- **Status:** closed
- **Led to:** L17, L18

### L16 · 2026-10-12 17:47 · h07 leave-one-section-out
- **Folder:** [hypotheses/h07_leave_one_section_out/](hypotheses/h07_leave_one_section_out/)
- **Question:** does a setting-switch generator or a topic-plaintext hybrid better predict an unseen section?
- **Done:** pre-registered falsification test; fitted on four sections and predicted the fifth.
- **Result:** weak and negative-leaning. Setting-switch beats the topic codebook, but neither beats a global baseline.
- **Commits:** 397a5cb
- **Status:** closed
- **Led to:** —

### L17 · 2026-10-12 17:48–17:55 · h09 image-context cribs from the drawings
- **Folder:** [hypotheses/h09_image_context_cribs/](hypotheses/h09_image_context_cribs/)
- **Question:** can drawings (plants, stars, jars, water, nymphs) tie words to meanings?
- **Done:**
  - Pre-registered visual tags for 224 folios.
  - Tested label–object sharing, same-plant pairs, label-in-text, enrichment with quire nulls, and transfer.
- **Result:** no robust word–meaning pair; enrichment is a section/quire effect. Root/jar words are a weak lead.
- **Commits:** 7edbf90, c807ba0, 11bda08
- **Status:** closed (root/jar words remain a weak lead)
- **Led to:** L18

### L18 · 2026-10-12 18:28–18:33 · h10 section vs quire and hand
- **Folder:** [hypotheses/h10_section_vs_quire_hand/](hypotheses/h10_section_vs_quire_hand/)
- **Question:** is the "section" effect really a quire or scribe effect?
- **Done:** within-stratum and reverse contrasts, variance decomposition and h09 rechecks (pre-registered).
- **Result:** no section effect passes both nulls after Holm; hand/language effects dominate.
- **Commits:** a4bc34e, 828ccf5, 40bbaa0
- **Status:** closed
- **Led to:** L19

### L19 · 2026-10-12 18:44–19:04 · h11 hand × language models
- **Folder:** [hypotheses/h11_hand_language_model/](hypotheses/h11_hand_language_model/)
- **Question:** how much do scribe and language explain, and what remains?
- **Done:** hierarchical models, residual section/image tests, hand features and a rewrite-rule orthography test.
- **Result:**
  - Hand × language is the largest factor.
  - A section signal survives on hand residuals but not once quire is also removed.
  - Rules close 22.7% of the 1A–2B gap (first rule `-edy → -ol`).
- **Commits:** 5bce8d2, 528412f, b7a6026
- **Status:** lead (spelling mapping)
- **Led to:** L20

### L20 · 2026-10-12 19:40–20:06 · h12 per-hand copy-modify generators
- **Folder:** [hypotheses/h12_per_hand_copy_modify/](hypotheses/h12_per_hand_copy_modify/)
- **Question:** is each hand one system plus a spelling mapping, and does copying matter?
- **Done:** C0 engine fitted per hand × language, with pooled, shuffled, cross-hand and rule-mapped baselines.
- **Result:**
  - Per-hand beats pooled in 14/15 folds.
  - The copy step is inert (p_copy ≈ 0.02–0.04).
  - The mapping closes 45–69% of the top-word gap.
- **Commits:** a1366f0, e7a5a05, 60de6ad
- **Status:** closed
- **Led to:** L21

### L21 · 2026-10-12 20:10–20:13 · h13 top-100 words in context and images
- **Folder:** [hypotheses/h13_top_word_context/](hypotheses/h13_top_word_context/)
- **Question:** what do position, neighbours and images say about the 100 most common words?
- **Done:** per-word cards (position, PPMI classes, spelling variants, image links) with quire×HL nulls.
- **Result:**
  - Real line-position preferences: 7 line-start words, 3 line-end words.
  - Neighbour classes track hand.
  - 0/868 image tests survive.
- **Commits:** c80e2f7, f2e3d97, 7b437bb
- **Status:** lead (line position)
- **Led to:** L22

### L22 · 2026-10-12 20:15–20:17 · h14 line-position controls
- **Folder:** [hypotheses/h14_line_position_controls/](hypotheses/h14_line_position_controls/)
- **Question:** are the line-start/end effects artefacts of line length or layout?
- **Done:** stratified, within-line and length-matched nulls; 2B → 1A Procrustes alignment.
- **Result:**
  - The effects are real.
  - Line-start words are mostly a 2B/3B habit; `am`/`dam`/`dy` end lines in every hand.
  - Rule partners are aligned closer than random (p = 0.0005).
- **Commits:** be999f9, 3c697fe, 596bf2f
- **Status:** lead
- **Led to:** L23

### L23 · 2026-10-12 20:30–20:32 · h15 line-start robustness and stem control
- **Folder:** [hypotheses/h15_line_initial_robustness_and_stem_control/](hypotheses/h15_line_initial_robustness_and_stem_control/)
- **Question:** is the 2B/3B line-start habit consistent across quires, and is the `-edy`/`-ol` pairing just shared stems?
- **Done:** per-quire/bifolium meta-analysis, leave-one-out, 1A power check, stem-controlled Procrustes.
- **Result:**
  - Line starts: ratio 3.28 [2.48, 4.35]; 7/8 quires; absent in 1A at full power.
  - The rule-pair advantage is mostly shared stems (p = 0.097).
- **Commits:** 0466079, 5616426, 6068136
- **Status:** lead (line structure); closed (word-level mapping)
- **Led to:** L24

### L24 · 2026-10-12 20:36–20:39 · h16 line-start onsets and an open line-edge search
- **Folder:** [hypotheses/h16_line_initial_prefix/](hypotheses/h16_line_initial_prefix/)
- **Question:** are 2B/3B line-start words ordinary words with a d-/s- added at the front, and does 1A have its own line-edge words?
- **Done:** onset and stripped-form tests; open search per hand × language.
- **Result:**
  - Yes: onset ratio 1.71 (z = 17.5); the stripped form is a common word in 69% vs 28% of cases.
  - 1A has its own small set (dchor, sor, sho).
- **Commits:** 310f5af, 243fb2e, 0dd63bf
- **Status:** lead (not yet modelled)
- **Led to:** L26

### L25 · 2026-10-12 20:39–20:43 · Public release: SEO README, licence, contributing guides, CI
- **Folder:** [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md), [.github/](.github/), [CITATION.cff](CITATION.cff)
- **Question:** make the repository public and usable by contributors.
- **Done:**
  - SEO README, MIT licence, contributing guide, code of conduct, issue/PR templates, citation file, social preview.
  - CI test workflow (with the images extra and poppler); Naibbe round-trip test skipped when the control corpus isn't fetched.
- **Result:** CI green.
- **Commits:** 7f0eff0, ed3669f, 9c23d8d
- **Status:** closed
- **Led to:** L28

### L26 · 2026-10-12 20:41–20:55 · h17 published plant IDs and pharmaceutical labels as cribs
- **Folder:** [hypotheses/h17_herbal_label_cribs/](hypotheses/h17_herbal_label_cribs/)
- **Question:** do labels and texts of plants that the literature identifies, or matches between herbal and pharma pages, share words?
- **Done:**
  - Built a table of 239 ID proposals for 107 folios from 8 source groups.
  - Tests: pharma ↔ herbal labels, same genus/family folios, Bax crib consistency; nulls held quire × hand × language fixed.
- **Result:**
  - Labels and same-plant folios: no link (p ≥ 0.16).
  - Bax cribs at family level: Holm 0.004, but the pass rests on one crib (`keerodal` ~ `ksheodal`).
- **Commits:** e499f8c, ae54722, 4830bba
- **Status:** closed (the lead was tested in L27)
- **Led to:** L27

### L27 · 2026-10-12 21:00–21:03 · h18 out-of-sample Apiaceae crib test
- **Folder:** [hypotheses/h18_apiaceae_crib/](hypotheses/h18_apiaceae_crib/)
- **Question:** does the `keerodal` shape recur on Apiaceae folios that weren't used to find it?
- **Done:** pre-registered non-Bax Apiaceae set (with a no-Vatne sensitivity set), a k…dal/k…dy shape, a quire×HL null and random-shape calibration.
- **Result:** fails. The target pages open with 0 such words (null 0.08–0.17); token share p = 0.23–0.26; all Holm p = 1. The pharma grid → label map isn't available.
- **Commits:** 0220892, ff46f11, 48ad021
- **Status:** closed
- **Led to:** —

### L28 · 2026-10-12 · This research log
- **Folder:** [RESEARCH_LOG.md](RESEARCH_LOG.md)
- **Question:** keep everyone on the same page.
- **Done:** chronological log of L01–L27; linked from README and CONTRIBUTING; added a PR checkbox.
- **Result:** documentation.
- **Commits:** (this commit)
- **Status:** closed
- **Led to:** future entries

### L29 · 2026-10-12 21:09–21:40 · h19 held-out likelihood comparison of mechanisms (issue #3, option 3)
- **Folder:** [hypotheses/h19_heldout_likelihood/](hypotheses/h19_heldout_likelihood/)
- **Question:** scored on held-out pages, does MS 408 behave like language, generated (copy-and-modify) text, or a Naibbe cipher?
- **Done:**
  - Per hand × language (1A, 2B, 3B) with bifolium and quire folds; hyperparameters fitted on inner splits.
  - Models: char LM, slot grammar, Kneser–Ney 1–3, copy-and-modify as a probabilistic model (EM copy rate and edit channel), Naibbe likelihood with Latin/Italian plaintext LMs, and a line-start onset feature.
  - Calibration: 4 plain controls, 2 Naibbe ciphertexts and a synthetic copy text.
- **Result:**
  - Context gain is 0.25 bits/word in MS vs 0.94 in the controls, and n-grams hurt. The best MS model is context-free.
  - Not Naibbe-like: escape weight 0.94–0.99 on MS vs ≤ 0.009 on real ciphertext.
  - ML copy rate 0.10–0.13 (CIs ±0.02), inside the controls' range of 0.07–0.17. The synthetic rate of 0.2 is recovered.
  - The onset feature saves 0.25–0.59 bits on line-initial tokens.
  - P1 passes; P2–P5 fail.
- **Commits:** 2726c9e, a71ad8b, 44b3838, (FINDINGS/README/log commit)
- **Status:** closed
- **Led to:** —

### L30 · 2026-10-13 08:32–09:20 · h20 generators and Italian encodings vs the MS likelihood fingerprint
- **Folder:** [hypotheses/h20_generators_vs_italian/](hypotheses/h20_generators_vs_italian/)
- **Question:** which condition reproduces MS 408's held-out fingerprint from h19 (no n-gram gain, cache gain of real-text size, a 5-word copy rate, char-level dominance)? Italian is the primary real-language reference.
- **Done:**
  - 9 Italian texts, with a new download script and manifest (texts git-ignored).
  - h12 C0 engine per hand; Timm–Schinner self-citation (authors' Java).
  - Italian through Naibbe, a syllabic cipher, vowel removal and suspension.
  - Added a position-conditioned char LM (PCLM); `rapidfuzz` became a project dependency.
- **Result:**
  - Only C0 (2B, 3B) reproduces all five statistics; self-citation reaches up to 4/5.
  - No Italian text or Italian encoding reproduces. Italian keeps an n-gram gain of +0.24 to +1.42 bits/word; Naibbe-Italian lacks local repetition.
  - P1–P4 and P6 pass; P5 fails on its threshold.
- **Commits:** 38ae92c, ba444aa, (FINDINGS/README/log commit)
- **Status:** closed
- **Led to:** —

### L31 · 2026-10-13 09:30–10:10 · h21 order-breaking Italian encodings and cross-hand C0
- **Folder:** [hypotheses/h21_italian_order_breaking_and_cross_hand/](hypotheses/h21_italian_order_breaking_and_cross_hand/)
- **Question:** can Italian that is encoded to break word order but keep local repetition reproduce the h20 fingerprint, and how contrived must it be? Does C0's match survive fitting on other hands?
- **Done:**
  - Within-line shuffle, nulls drawn from MS 2B tokens, recency homophones and Naibbe, applied to Boccaccio, Cucina, Sidrach and Cennini: 24 base cells.
  - An 18-setting grid on Boccaccio, with the top 2 settings transferred to the other sources.
  - C0 fitted per hand (seeds 20 and 21) and on pooled other hands, point-matched across hands.
- **Result:**
  - Shuffling removes the n-gram gain, but char dominance and bits/glyph stay non-MS. The best encoding, Naibbe plus 33 % nulls, reaches 3/5; the best grid setting reaches 1–2/5 on bifolium folds.
  - Cross-hand C0 stays inside the MS range but point-matches unseen hands unevenly.
  - PA1, PA2 and PB3 pass; PA3, PB1 and PB2 fail.
- **Commits:** 2408d3e, 5d2852a, (FINDINGS/README/log commit)
- **Status:** closed
- **Led to:** —

### L32 · 2026-10-13 10:12–10:35 · h22 Italian cipher plus a generic copy-and-modify layer
- **Folder:** [hypotheses/h22_italian_cipher_plus_copy/](hypotheses/h22_italian_cipher_plus_copy/)
- **Question:** is local copying the one ingredient missing from Italian encodings? How much plaintext signal survives it? Is hand 2B genuinely distinct?
- **Done:**
  - Copy layer (c × W grid, edits not fitted to MS) on Naibbe, Naibbe+nulls, syllabic+nulls and Naibbe+shuffle, with clean vs leaky nulls.
  - Top-2 transfer to Cucina, Sidrach and Cennini; plaintext recovery (signal share, oracle decoding, MI).
  - Cross-hand C0 with 5 seeds.
- **Result:**
  - Naibbe + 5 % copying (W = 20) reaches 4/5 on all four sources, at distance 5.4–7.9; it fails only D4, and nothing reaches 5/5 on bifolium folds.
  - The h21 null benefit was mostly the MS leak.
  - The plaintext signal largely survives.
  - Blind C0 fits never match 2B (but match 1A every time).
  - QA1–QA3, QA6 and QB1 pass; QA4 and QA5 fail.
- **Commits:** b37c88b, da1c19d, (FINDINGS/README/log commit)
- **Status:** closed
- **Led to:** —

### L33 · 2026-10-13 13:45–14:07 · h23 copy-rule variants and hand 2B diagnostics
- **Folder:** [hypotheses/h23_copy_rule_variants/](hypotheses/h23_copy_rule_variants/)
- **Question:** can a copy rule raise the 5-word copy rate without lowering word-vs-char dominance (D4)? What makes 2B distinct?
- **Done:**
  - 7 copy rules × 3 copy rates on Naibbe-Boccaccio; syllabic secondary.
  - Top-2 transfer to Cucina, Sidrach and Cennini.
  - 2B diagnostics: descriptives, size-matched section subsets, -edy removed.
- **Result:**
  - Suffix-swap copying at 5 % gives 5/5 on Boccaccio (distance 3.0) and 4/5 on all transfers (D4 just out); within-line copying gives 5/5 on Cennini. Distances are in the C0 range.
  - So the fingerprint does not separate cipher + copying from a generator.
  - 2B's low bits/glyph sits in biological pages and in -edy.
  - RA1, RA2, RA4, RA5 and RB2 pass; RA3 and RB1 fail.
- **Commits:** 1d5d29c, 346606e, (FINDINGS/README/log commit; also repo rename URLs and README title)
- **Status:** closed
- **Led to:** —

### L34 · 2026-10-13 14:16–14:42 · h24 neutral-cipher robustness, and hand vs section
- **Folder:** [hypotheses/h24_neutral_cipher_robustness/](hypotheses/h24_neutral_cipher_robustness/)
- **Question:** is the h23 Naibbe+copy 5/5 robust to seeds? Does it survive ciphers not designed from MS? Is 2B a hand effect or a section effect?
- **Done:**
  - 60 Naibbe cells: 3 copy rules × 4 sources × 5 seeds.
  - 54 neutral-cipher cells (6 families × 3 copy conditions × 3 seeds) plus 9 transfer cells.
  - 8 section-matched MS subsets.
  - Repo-rename follow-up: user-agent URLs in fetch.py and controls_fetch.py; LICENSE contributors name.
- **Result:**
  - Naibbe+copy is at least 4/5 in 60/60 cells (5/5 in 15–35 %), distance 2.2–4.4.
  - Neutral ciphers reach at most 3/5, distance at least 89, so the match depends on Naibbe's MS-like tables.
  - 2B's low bits/glyph is a biological-section effect.
  - S2 passes; S1, S3 and S4 fail; S5 shows a section effect.
- **Commits:** f327363, 381f275, (README fix), (FINDINGS/README/log/rename commit)
- **Status:** closed
- **Led to:** —

### L35 · 2026-10-13 14:55–16:22 · h25 neutral hybrid cipher (Naibbe structure, random tables)
- **Folder:** [hypotheses/h25_neutral_hybrid_cipher/](hypotheses/h25_neutral_hybrid_cipher/)
- **Question:** is Naibbe's design alone, with random non-MS tables, enough to reach the MS fingerprint? Which structural parameter matters most?
- **Done:**
  - 138 cells: baseline × 4 copy conditions, × 4 sources, × char/EVA-like rendering; 9 one-at-a-time variants.
  - Base seeds reduced from 10 to 6 for runtime after an interruption.
- **Result:**
  - No 5/5 anywhere; the best is long codes without copying (distance 8.9, 3/5).
  - Copying worsens NH, and EVA rendering wrecks D4.
  - The number of tables has the largest effect.
  - So the Naibbe match is carried by its MS-like tables.
  - T2, T3 and T5 pass; T1 and T4 fail.
- **Commits:** be8e60e, c30b486, (FINDINGS/README/log commit)
- **Status:** closed
- **Led to:** —

### L36 · 2026-10-13 16:56–17:20 · h26 Naibbe-structure cipher with glyph-grammar tables
- **Folder:** [hypotheses/h26_neutral_glyph_grammar_tables/](hypotheses/h26_neutral_glyph_grammar_tables/)
- **Question:** is any orderly word-internal glyph grammar in the tables enough to reach MS's fingerprint, or only an MS-like one? Which property matters?
- **Done:**
  - 71 Boccaccio cells (RS slot grammars and variants, Latin chain, MS chain; ± swap; EVA-like rendering).
  - Real-Naibbe-tables anchor (10 cells, diagnostic).
  - Transfer (18 cells).
- **Result:**
  - No grammar-generated tables match; even the MS-trained chain fails (94–103).
  - The real Naibbe tables in the same engine give 3.43. So the match depends on the hand-designed tables.
  - Word length is the top property (ρ +0.85).
  - G1–G5 all fail.
- **Commits:** b66763a, ed4398d, 7cd2011, b11119f, 47d2f5e
- **Status:** closed
- **Led to:** —

### L37 · 2026-10-13 18:36 · h27 real Naibbe tables with the plaintext removed
- **Folder:** [hypotheses/h27_plaintext_ablation/](hypotheses/h27_plaintext_ablation/)
- **Question:** with the author's tables and a 5% suffix-swap copy held fixed, does the fingerprint still appear if the plaintext is not Italian?
- **Done:**
  - Pre-registered, then 15 Boccaccio cells: real tokens, the same tokens shuffled, and Zipf nonsense (4000 types, Italian letter unigrams, Zipf ranks).
  - Same engine and seeds as the h26 real-table anchor. Bifolium primary; quire also scored.
- **Result:**
  - Bifolium distance 3.432 (real), 3.294 (shuffle), 2.808 (zipf). Each is ≥4/5 in 5/5 seeds.
  - The real arm matches the h26 anchor seeds exactly, so the engine path is the same one.
  - P1 and P3 pass; P2 fails. Plaintext structure is not what carries the match. The predicted split between word order and spelling does not appear.
- **Commits:** 814b9e6, (results and log commit)
- **Status:** closed
- **Led to:** L38

### L38 · 2026-10-13 18:39 · h28 permutations of the real Naibbe tables
- **Folder:** [hypotheses/h28_table_permutation/](hypotheses/h28_table_permutation/)
- **Question:** which level of the author's tables carries the h26 match: the letter-to-string mapping, the prefix/suffix split, or the order inside each string?
- **Done:**
  - Pre-registered, then 15 Boccaccio cells. Real tables permuted three ways (letter, state, unit), then the h27 engine and 5% suffix-swap copy.
  - The original table file was not modified. The h26 anchor was not recomputed.
- **Result:**
  - Bifolium distance 21.96 (letter), 27.50 (state), 143.08 (unit). None matches (rule: distance ≤ 5.43 and ≥4/5 in ≥60% of seeds).
  - Letter and state still reach ≥4/5 in 4/5 seeds. The miss is D4 in every seed (−0.39 and −0.45). The unit shuffle also misses D4 (−1.12) and D5 in 3/5 seeds. Unit order changed in 75.5% of strings.
  - A1 fails; A2 and A3 pass. The pre-registered reading is that no single one of these three cuts is the carrier.
- **Commits:** 814b9e6, (results and log commit)
- **Status:** closed
- **Led to:** L39

### L39 · 2026-10-13 19:16 · h29 D4 toys and stored-cell correlations
- **Folder:** [hypotheses/h29_d4_toy_tables/](hypotheses/h29_d4_toy_tables/)
- **Question:** which stored property tracks the fingerprint distance, and can a two-knob toy table be both decodable and above the D4 floor of −0.07?
- **Done:**
  - Spearman on the committed h26, h25, and h24 bifolium tables. No new ciphertext for that part.
  - 25 toy cells: code length L from 1 to 5, suffix-pool size V in {8, 16, 32, 64, 128}, one seed, character segmentation, no copy layer. Bifolium only.
- **Result:**
  - On 66 h26 cells, mean word length has the largest correlation with distance (ρ +0.85) and moves against D4 (ρ −0.81). R1 passes.
  - Three cells are ≥0.8 decodable and have D4 ≥ −0.07 (L=3 with V=64 and V=128, L=4 with V=128). Their D4 is +0.38 to +0.48, above the MS window, so T1 fails and none of them is a two-sided D4 match.
  - ρ(D4, V) is +0.11, so T2 fails. No cell is 5/5. The closest are L=2, V=16 and V=32 (4/5, distance 12.7 and 16.8), both under 0.51 decodable.
- **Commits:** 814b9e6, (results and log commit)
- **Status:** closed
- **Led to:** —

### L40 · 2026-10-13 · h30 line structure per hand
- **Folder:** [hypotheses/h30_line_structure/](hypotheses/h30_line_structure/)
- **Question:** is the MS line verse, a list/table entry, or margin-broken prose?
- **Done:** M1–M6 for 1A, 2B, 3B, 3A plus Dante, Ariosto, Macer, Augustine, Manzoni, Sidrach and Cucina. The nulls permute within the hand|quire stratum (positional MI and paragraph onsets) or shuffle lines within a page (across-line MI). Held-out bag, positional, bigram and HMM models.
- **Result:** L1, L3 and L4 pass for 1A, 2B and 3B: no rhyme, CV .26–.44, END→ONSET dependency within lines but not across breaks, gallows paragraph onsets (JS .41–.57). L2 passes for 1A and 3B, and 2B misses it at the threshold. L5 fails for all hands (position gain .03–.04 bits/token). 3A has only 80 lines and is underpowered.
- **Commits:** f137ec3 (prereg), (code + results + docs commit)
- **Status:** closed
- **Led to:** entry-level model (paragraph → body → line-final marker)

### L41 · 2026-10-13 · h31 MS 408's word-construction system
- **Folder:** [hypotheses/h31_word_construction/](hypotheses/h31_word_construction/)
- **Question:** are MS words built from a small inventory of morpheme-like pieces (language-like), or freely combined pieces (generator-like decoration)?
- **Done:**
  - Pre-registered, then segmented with Morfessor (MDL), a Bayesian stem + suffix model and the project's affix model.
  - Corpora: hands 1A, 2B and 3B; 6 natural texts (Latin, Italian, Hebrew, Arabic); Naibbe on Pliny and Ariosto; C0 fitted on 2B.
  - Measured inventory, productivity, stem–suffix constraint, paradigm reuse, cross-word agreement, and held-out bits/word against the h19 CharLM.
- **Result:**
  - Neither H-morph nor H-decor passes.
  - Inventory is generator-sized: 0.07–0.085 morphs/type (NAT 0.21–0.54, GEN 0.06–0.07). Productivity 0.67–0.73 sits between the groups. Morph − CharLM gap is 1.3–1.4 bits/word (NAT 2.7–3.7).
  - Words depend on their neighbours: ending → next word's first letter 0.07–0.17 bits, last letter 0.11–0.23. No generator shows this (≤ 0.03).
- **Commits:** e97c4d1 (prereg), 9432f07 (code + results), (docs commit)
- **Status:** lead (junction dependence)
- **Led to:** a junction-rule generator, and line-position controls for A1

### L42 · 2026-10-13 22:20 · h32 shared spelling system between hands
- **Folder:** [hypotheses/h32_hand_spelling_system/](hypotheses/h32_hand_spelling_system/)
- **Question:** how much of the hand 1A vs 2B difference is a mappable spelling system once section is held fixed, and do the hands write the same content in different spelling?
- **Done:**
  - Pre-registered, then learned up to 30 context-dependent unit rewrite rules (word edge or neighbouring unit as context) on herbal 1A vs herbal 2B (and 3B), scored on held-out page halves over 5 splits, against h11's rules on the same splits, same-hand cross-section gaps, split halves and 20 permuted-hand controls.
  - Mapped 2B herbal into 1A spelling and ran Smith-Waterman on every 2B×1A page pair (200 shuffles each), shared bigram/trigram counts, and a same-plant-family profile test (h17 families).
- **Result:**
  - The transducer closes 29.3 % ± 1.3 % of the section-matched gap (h11 22.7 %; permuted hands ≤ 7.1 %; same hand cross-section 3.3–15.2 %). With 10 rules it is no better than h11 (23.2 %). 70.7 % remains, so most of the difference is vocabulary.
  - No same-content signal: 0 of 1900 page pairs align beyond shuffles after BH; mapped n-gram sharing is at the shuffle level (bigram ratio 0.98, against 1.22 within 1A); same-family pages are not more alike (p = 0.90).
  - Only four rules recur across splits (`#ai→dai`, `-edy→-ol`, `#a→cho`, `chd→ch`). They are word-edge habits; the rest is a split-specific tail. P1–P3 pass, S1 fails, Q1 partial.
- **Commits:** 299b769 (prereg), ac8a559 (code), a9ed537 (results + README), (log commit)
- **Status:** closed (same content); lead (word-edge habits)
- **Led to:** an EM-trained weighted FST on word-pair alignments, and checking whether the four edge habits coincide with h30's line-edge rules

### L43 · 2026-10-14 · h33 are MS spaces true word boundaries?
- **Folder:** [hypotheses/h33_word_boundary_resegmentation/](hypotheses/h33_word_boundary_resegmentation/)
- **Question:** do the real units straddle the spaces, given h31's strong last-glyph → next-first-glyph link?
- **Done:**
  - Pre-registered, then re-cut hands 1A, 2B and 3B, 5 natural texts and 3 generators identically. Transforms: join pairs, shift ±1/±2 glyphs, Morfessor on stripped lines.
  - Each run in full and line-interior variants. Scored TTR, Zipf, morphs/type, held-out KN gain, junction MI and space predictability.
- **Result:**
  - No re-cut makes MS more word-like. TTR rises 35–60 % and Zipf flattens, as in real text and generators.
  - The n-gram gain rise after shifting is a split-word artifact, also seen in generators. This is a pre-registration flaw and is recorded.
  - Spaces are predictable from ±2 glyphs: .75–.82 of entropy removed, against natural ≤ .757 and generators .82–.88. H-straddle 0/3; S1 passes 2/3; P1 fails as written.
- **Commits:** 533f9e8 (prereg), (code + results + docs)
- **Status:** closed (straddling words); lead (rule-placed spaces)
- **Led to:** a junction-rule generator; a proper DP word segmenter

### L44 · 2026-10-14 · h34 per-hand word-gap rule generator
- **Folder:** [hypotheses/h34_boundary_rule_generator/](hypotheses/h34_boundary_rule_generator/)
- **Question:** can a per-hand gap rule (next word chosen by its first glyph given the previous last glyph) added to generators reproduce h31's end→start link and h33's space predictability, while keeping inventory and the D1–D5 fingerprint?
- **Done:**
  - Pre-registered, then fitted rule tables on train bifolia per hand and applied them to C0, Naibbe-Italian+swap copy and nonsense-plaintext Naibbe (local reordering, K=10, s grid 0–3).
  - Controls: s=0, shuffled table, all-gaps, edge-excluded. Evaluated on test bifolia; ran the h20 fingerprint for s=0 and s* cells.
- **Result:**
  - At s*=1 the link is reproduced in 8/9 cells (MS .14/.27/.22; generators .08–.20; s=0 ≤ .004), with the MS table pattern (r .90–.97; shuffled ≤ .31) and last glyph beating ending 9/9.
  - Fingerprint 5/5 in 8/9 cells; Naibbe-Italian goes 4/5 → 5/5 for all hands. Same with nonsense plaintext.
  - MS link survives dropping line-edge words (95–98 %).
  - Space predictability barely moves (−.015 to −.03): P4 fails 2/9. H-gap supported (P1, P2, P3, P6).
- **Commits:** 46d318e (prereg), (code + results + docs)
- **Status:** lead (gap rule explains the junction link); open (space placement)
- **Led to:** a word-internal start/end glyph model for space placement; finer s fit

### L45 · 2026-10-14 · h35 per-hand word-shape model
- **Question:** does per-hand word-internal glyph structure explain the h34 space-predictability gap?
- **Did:** glyph 3-gram shape model per hand on even bifolia; type-level re-spelling of C0 / Naibbe-Italian / Naibbe-nonsense words; h34 gap rule kept; held-out odd bifolia. Controls: shape off, shuffled shape, nonsense.
- **Found:**
  - Space predictability .72–.80 (8/9), within ±.04 of hand 9/9; was .84 for Naibbe.
  - Link, gap table (r .92–.97), inventory kept; shuffled model .23–.34; Italian = nonsense.
  - Fingerprint falls to 2–3/5 (cache gain, copy rate, word/glyph dominance): re-spelling breaks near-copies.
  - Gap drivers: glyphs both final and internal (`l`, `y`, `r`; also `o`, `s`, `d`).
- **Commits:** 1410b0a (prereg), (code + results + docs)
- **Status:** lead (space placement); open (one generator matching space placement and fingerprint)
- **Led to:** similarity-preserving re-spelling

### L46 · 2026-10-14 · h36 similarity-preserving re-spelling
- **Question:** can a re-spelling that keeps one-glyph near-copies near fix space placement (h35) and keep the 5/5 fingerprint?
- **Did:** glyph-by-glyph rank map per position class (`pos`) and per previous glyph (`ctx`), fitted on even bifolia; h34 gap rule kept; scored on odd bifolia for C0 / Naibbe-Italian / Naibbe-nonsense. Controls: shape off, shuffled map, nonsense, h35 reference.
- **Found:**
  - Edit-neighbour preservation .83–.96 (`pos`) vs .01 for h35; fingerprint back to 5/5 in 6/9, 4/5 in the rest.
  - Space predictability rises to .78–.95 (1/9 in .72–.80): worse than no re-spelling. `ctx` S .74–.92, E .39–.82.
  - Link, gap table (r .95–.98), inventory kept; Italian = nonsense.
- **Commits:** eea4e97 (prereg), (code + results + docs)
- **Status:** negative (trade-off between copy structure and space placement)
- **Led to:** copy-aware re-spelling (shape the source word, replay copy edits on top)

### L47 · 2026-10-14 · h37 copy-aware re-spelling
- **Question:** if only "source" words get the h35 word-shape re-spelling and near-copies are rebuilt by replaying their one-glyph edit, do space placement, copy structure and the 5/5 fingerprint hold together?
- **Did:** edit-neighbour graph (root = no more frequent type at edit distance 1), roots re-spelled with the per-hand 3-gram shape model, derived types rebuilt from their re-spelled parent (position-relative edit, glyph drawn from the shape model); h34 gap rule kept; fit even bifolia, score odd; C0 / Naibbe-Italian / Naibbe-nonsense × 1A/2B/3B. Controls: h34 off, h35, h36 pos, shuffled shape model, nonsense.
- **Found:**
  - Parent→child edits survive for 96–98 % of derived types, but edit-neighbour preservation over all pairs is only .45–.51 (P6 0/9): siblings and cross-family neighbours are rebuilt independently.
  - Space predictability .69–.74 (P1 3/9; slightly *too* unpredictable, opposite side to h36); fingerprint 2–4/5 (P5 0/9).
  - Link (9/9), gap table r .84–.93 (8/9), inventory (9/9) kept; shuffled shape model far off (9/9); Italian = nonsense (3/3).
- **Commits:** 83fe362 (prereg), (code + results + docs)
- **Status:** negative (copy tree kept, near-copy network lost)
- **Led to:** network-aware re-spelling (shared glyph substitutions across all edit neighbours, e.g. respell a word's variable slot once per family) or a generator that copies in MS shape directly

### L48 · 2026-10-14 · h38 family re-spelling and native-shape copier
- **Question:** can re-spelling whole near-copy families (A) or copying directly in MS word shapes (B) match space placement, the near-copy network and the 5/5 fingerprint at once?
- **Did:** A: edit-1 connected components share a re-spelled root and a family-wide glyph map (word-final slots from the hand's final-glyph distribution). B: self-citation generator (15 % fresh, else copy from last 50 with 0/1/2 edits) with seeds and edits from the per-hand shape model; fresh words from shape model, Naibbe-Italian or Naibbe-nonsense. h34 gap rule; train even / test odd bifolia; hands 1A/2B/3B. Controls: shuffled-shape model, h37 reference, nonsense feed.
- **Found:**
  - A: S in .72–.80 in 8/9; all-pairs near-copy .46–.56 (0/9 ≥ .9); fingerprint 1–4/5 (0/9 at 5/5); final-glyph JS lower than h37 in 6/9; shuffled control further off 7/9.
  - B: S .32–.45 (0/9 in range); fingerprint 1/5 (9/9); link + gap table kept 9/9; final-glyph JS ≤ .05 in 5/9; inventory 1.7–2.4× MS.
  - Italian = nonsense (no plaintext signal either way).
- **Commits:** a5c19e1 (prereg), (code + results + docs)
- **Status:** negative (A: spaces fixed, network not; B: wrong on spaces and fingerprint)
- **Led to:** keep a full edit graph (not a BFS tree) with a per-family glyph map solved jointly, or tune B's fresh/copy rates to MS λ5 before re-testing

### L49 · 2026-10-14 · h39 graph-preserving re-spelling and tuned native copier
- **Question:** final round of the h35–h39 loop: can a re-spelling that keeps the whole one-edit graph (A), or a native copier with tuned rates (B), match space placement, the near-copy network and the 5/5 fingerprint at once?
- **Did:** A: one glyph substitution per word slot (0,1,2,mid,−3,−2,−1), simulated annealing (1 500 proposals) jointly over the top-800-type edit graph against hand-train slot and final-glyph distributions and space predictability. B: h38 copier with 80-point grid over fresh rate, window and unchanged-copy share, tuned on even bifolia (types/5k, near-repeat proxy, S). h34 gap rule; scored on odd bifolia; hands 1A/2B/3B; generators C0, Naibbe-Italian + 5 % swap, Naibbe-nonsense. Controls: shuffled-target annealing, h38 reference, nonsense feed.
- **Found:**
  - A: near-copy E .74–.83 (0/9 ≥ .9, best of loop); spaces .74–.84 (3/9 in range); fingerprint 5/5 in 4/9; final-glyph JS ≤ .04 9/9; 340–1 330 types merged; gap-table r .16–.60; shuffled control far off 9/9.
  - B: tuned to grid edge (25 % fresh, window 50, 55 % unchanged); near-repeat matched; link + table kept 9/9; spaces .48–.59 (0/9); fingerprint 1/5 (λ5 .21–.23 vs MS .03–.04); inventory 1.13–1.63× MS.
  - Italian = nonsense.
- **Commits:** 351b9d5 (prereg), (code + results + docs)
- **Status:** negative (loop ends; per-slot recoding is the closest compromise)
- **Led to:** synthesis section in FINDINGS (h33–h39); next direction: model word similarity as a shared slot grammar (type-level) rather than token copying, or a context-dependent slot map that also preserves the gap table

### L50 · 2026-10-14 10:52 · h40 transcription targets
- **Folder:** [hypotheses/h40_transcription_targets/](hypotheses/h40_transcription_targets/)
- **Question:** do space predictability, the last-glyph link and D1–D5 survive ZL3b with uncertain spaces joined, IT2a, and RF1b?
- **Done:**
  - Pre-registered, then five readings of hands 1A, 2B and 3B. Space and junction on the h33 token cap. Bifolium D1–D5 on up to 10,500 tokens. No generator was rerun.
  - The nine stored h39 graph cells were re-scored against each hand's widened space band.
- **Result:**
  - R1–R3 pass. The largest D1–D5 range is 2B's D4, 0.065, inside the tolerance of 0.10. Junction stays 0.083–0.242, against generator originals ≤ 0.0034.
  - Interior space bands: 1A 0.750–0.770, 2B 0.811–0.827, 3B 0.815–0.847. The 2B and 3B bands sit above the old 0.72–0.80 target. Four of nine h39 cells fall in the widened band, three in the old one.
- **Commits:** 7af068c (prereg), 96d9abb (results and log)
- **Status:** closed (fingerprint and link); lead (the space target was too low for 2B and 3B)
- **Led to:** —

### L51 · 2026-10-14 10:52 · h41 long-range plaintext visibility
- **Folder:** [hypotheses/h41_plaintext_visibility/](hypotheses/h41_plaintext_visibility/)
- **Question:** at 10,500 tokens, can any long-range statistic tell Boccaccio from shuffled and Zipf Naibbe ciphertext, and where does MS 408 sit on a statistic that can?
- **Done:**
  - Pre-registered. Five Boccaccio windows, five seeds each of Naibbe plus suffix-swap on real, shuffled and Zipf plaintext, and five C0 streams fit on hand 2B (`n_random` 60).
  - Statistics: half-sample new-type rate, burstiness of the 50 most frequent words, MI at lag 100 over lag 1, and Jensen–Shannon divergence of adjacent 200-token blocks.
- **Result:**
  - V1 passes on burstiness only (plain 4.16–4.78; shuffle and zipf both ≤ 3.74). The other three statistics overlap.
  - V2 fails. Hands 1A, 2B and 3B score 5.22, 5.11 and 5.10, closer to plain Boccaccio (mean 4.40) than to C0 (3.59) or the cipher arms (3.54).
  - Correction (same day): the separation test compared plain text with ciphertext. Through the cipher, Naibbe on real Boccaccio (burst 3.41–3.65) overlaps shuffled (3.40–3.70) and nonsense (3.38–3.74) on all four statistics, so no statistic here sees a plaintext through Naibbe. The pre-registration lacked that arm in the separation rule.
- **Commits:** 7af068c (prereg), 96d9abb (results and log), (correction commit)
- **Status:** lead (MS word clustering is far above any Naibbe arm and C0, and above plain Boccaccio); closed (plaintext visibility through Naibbe: none of the four statistics)
- **Led to:** —

### L52 · 2026-10-14 10:52 · h42 near-repeat decay
- **Folder:** [hypotheses/h42_near_repeat_decay/](hypotheses/h42_near_repeat_decay/)
- **Question:** do one-edit word pairs in MS 408 die out within a few tokens, within a page, or not at all?
- **Done:**
  - Pre-registered. Edit distance 1 on EVA units, gaps 1 through 1,000, against a shuffle inside hand × quire (ten shuffles).
  - Streams: hands 1A, 2B, 3B, Boccaccio, one C0 stream, fitted self-citation, and the h39 tuned copier and graph respell for hand 2B.
- **Result:**
  - N1–N3 pass on the first-drop rule. Hand 1A drops at 21–100, hand 2B at 21–100, hand 3B at 101–500. Hand 2B's adjacent excess is 0.007 (not elevated), and its 101–500 bin is elevated again (0.010).
  - C0 drops at gap 2–5 (adjacent excess 0.024) and is elevated again at 6–20. Fitted self-citation and the h39 tuned copier stay elevated through 21–100 and drop at 101–500, which is later than hand 2B's first drop. Boccaccio and the h39 graph respell have no elevated bin (Boccaccio adjacent excess −0.027).
- **Commits:** 7af068c (prereg), 96d9abb (results and log)
- **Status:** closed (not Boccaccio's pattern); lead (hand 2B's excess returns at 101–500 tokens)
- **Led to:** L53

### L53 · 2026-10-14 12:08 · h43 vocabulary at the folio boundary
- **Folder:** [hypotheses/h43_page_edge/](hypotheses/h43_page_edge/)
- **Question:** at a matched distance, are windows on one folio more alike than windows split by a folio boundary, and do known section edges behave the same way?
- **Done:**
  - Pre-registered. Windows of 80 tokens, pairs 80 and 160 tokens apart, cosine of word counts. Null: 100 rotations of the text against fixed folio lengths inside each quire.
  - Hands 1A, 2B, 3B. Controls: Boccaccio novellas (20 boundaries), cucina recipes (180), Pliny chapters (155).
- **Result:**
  - E1 passes. At distance 80, 1A effect 0.082 against a null 95th percentile of 0.059 (184 same, 45 cross) and 2B 0.100 against 0.074 (4440 / 41). 3B has 23 cross pairs, so it is unscored.
  - E2 fails. Only Pliny passes at distance 80 (0.047 vs 0.014). Boccaccio and cucina have 20 and 12 cross pairs there. At distance 160, Boccaccio and Pliny pass and cucina's effect is −0.26.
- **Commits:** adf281d (prereg), (results and log commit)
- **Status:** lead (folio boundary in 1A and 2B); closed (not the same break as a novella or a recipe)
- **Led to:** —

### L54 · 2026-10-14 12:08 · h44 generator page clustering
- **Folder:** [hypotheses/h44_generator_page_burst/](hypotheses/h44_generator_page_burst/)
- **Question:** can a generator with no plaintext match the manuscript's page-level burst excess?
- **Done:**
  - Pre-registered. h41 burst statistic, shuffles inside the page, inside the quire, and overall. Generated pages are 230 tokens, the median hand-2B folio. Quires are 8 pages.
  - Streams: MS hands, fitted self-citation s1 and s2, C0, an h06 pool and a no-pool stream with default parameters, two h39 streams, and a per-page vocabulary control.
- **Result:**
  - B1 fails. MS excess is 1.51, 1.69 and 1.50. fitted_s1 is 1.63 and the h39 tuned copier is 4.76. C0 is 0.15, the h06 pool 0.27, h06 with no pool 0.05, and the h39 graph respelling 0.19.
  - B2 and B3 pass. The per-page vocabulary stream reaches 33.2. In every hand, more of the excess sits inside the folio than inside the quire.
- **Commits:** adf281d (prereg), (results and log commit)
- **Status:** closed (the excess is not evidence of content)
- **Led to:** —

### L55 · 2026-10-14 12:08 · h45 vowel/consonant share of the glyph link
- **Folder:** [hypotheses/h45_edge_link_classes/](hypotheses/h45_edge_link_classes/)
- **Question:** how much of the last-glyph to next-first-glyph link is a two-way vowel/consonant split?
- **Done:**
  - Pre-registered. Sukhotin classes fit on each stream. Share is the mutual information of the classes divided by the mutual information of the glyphs.
  - Four controls, three hands, fitted self-citation, and an h34 gap rule applied to that self-citation stream.
- **Result:**
  - C1 fails. The median control share is 0.004, against a bar of 0.25. Boccaccio 0.002, cucina 0.005, Pliny 0.0004, Macer 0.21. Sukhotin recovers e a o i u on Boccaccio.
  - C2 and C3 are not scored. MS shares are 0.058, 0.066 and 0.057. Self-citation is 0.002 and the gap rule is 0.001. The gap-rule stream is the whole fitted text, 48,671 tokens.
- **Commits:** adf281d (prereg), a97b8a7 (results and log)
- **Status:** closed (the vowel/consonant split is not the control pattern)
- **Led to:** —

### L56 · 2026-10-14 14:48 · h46 folio reset mechanism
- **Folder:** [hypotheses/h46_folio_reset_mechanism/](hypotheses/h46_folio_reset_mechanism/)
- **Question:** do one-edit word pairs drop across folio boundaries at matched token lag, do folio-opening first lines seed their page's one-edit cluster, and does Hand 2B's `101–500` excess come from visible open spreads (`v → r`)?
- **Done:**
  - Pre-registered. Hands 1A, 2B, 3B (`h14_lib.table()`, ZL3b, comma as space, collapsed EVA units).
  - Test 1: same-folio vs cross-folio one-edit rate in lags `6-20`, `21-100`, `101-500` against 100 within-quire circular rotations (seed 46). Test 2: line-1 seed rate vs interior baseline rate on folios with $\ge 6$ lines against 200 within-folio line-order permutations. Test 3: `v_to_r` (open spread) vs `r_to_v` (page turn) across consecutive folios in `21-100` and `101-500` against 200 transition-label permutations.
- **Result:**
  - F1–F3 fail. In Test 1, all three hands pass at `6-20` (`same − cross` +0.020, +0.024, +0.015), and 1A (+0.006 vs null 95th +0.002) and 3B (+0.008 vs +0.007; also `101-500` +0.008 vs +0.006) pass at `21-100`, whereas 2B (+0.006 vs +0.011) does not exceed the rotation null at `21-100` or `101-500`.
  - In Test 2, line 1 has a *lower* one-edit rate with its folio than interior lines do in every hand (−0.017, −0.024, −0.019). In Test 3, `v_to_r − r_to_v` is within noise (+0.004 and −0.001 in 2B).
- **Commits:** 7992e99 (prereg), (results and log commit)
- **Status:** closed (first-line seeding and open-spread copying); lead (short-lag `6–20` one-edit chains break at folio edges in all three hands)
- **Led to:** L57, L58

### L57 · 2026-10-14 14:48 · h47 unified page- and line-bounded generator
- **Folder:** [hypotheses/h47_page_line_generator/](hypotheses/h47_page_line_generator/)
- **Question:** can a single no-plaintext generator with partial folio-buffer reset and line-boundary slot framing simultaneously pass all six manuscript benchmark families (`B1`–`B6`) across hands 1A, 2B and 3B?
- **Done:**
  - Pre-registered. Fit `page_line_copier` on even bifolia of hands 1A, 2B and 3B (partial lookback reset `rho_keep = 0.15` at folio edges; line-initial/paragraph-initial onset weights, line-final ending weights, and cross-line junction reset at line breaks) and generated on each hand's real folio/line template up to 10,500 tokens (seed 47).
  - Scored `page_line_copier` (1A, 2B, 3B) and the two stored Hand 2B `h39` baselines (`native_tuned` and `C0_graph`) on `B1` (`h20` 5/5 fingerprint), `B2` (`h40` interior space band + junction $J \ge 0.06$), `B3` (`h30` line-edge concentration, cross/within MI $< 0.5$, para-initial $z > 3$), `B4` (`h43` folio-boundary drop), `B5` (`h44` folio-concentrated burstiness), and `B6` (`h42` page-scale near-repeat decay).
- **Result:**
  - U1–U3 pass. `page_line_copier` passes 6/6 benchmarks on Hand 1A, 6/6 on Hand 2B, and 6/6 on Hand 3B (5/6 if `d=80` unscored is excluded; `d=160` passes with +0.129 vs +0.061).
  - On Hand 2B, the stored `h39` baselines pass only 1/6 (`h39_native_tuned_2B`) and 2/6 (`h39_C0_graph_2B`).
- **Commits:** 7992e99 (prereg), (results and log commit)
- **Status:** lead (a single page-and-line-bounded no-plaintext generator reproduces all six benchmark families simultaneously)
- **Led to:** —

### L58 · 2026-10-14 14:48 · h48 within-folio copy drift vs fixed page palette
- **Folder:** [hypotheses/h48_within_folio_drift/](hypotheses/h48_within_folio_drift/)
- **Question:** within a single folio, is similarity stationary from top to bottom (a fixed page vocabulary palette) or does it decay with line lag $\Delta\ell$ (sequential top-to-bottom copy drift)?
- **Done:**
  - Pre-registered. Same-folio line pairs on folios with $\ge 8$ paragraph lines across MS hands 1A, 2B, 3B, prose controls (`it_boccaccio`, `la_pliny_herbal`), drift generators (`self_citation`, `h39_native_tuned`), and a within-folio line-permuted control (`palette_ctrl`), scored against 200 within-folio line-order permutations (seed 48) and 200 within-quire shuffles.
- **Result:**
  - D1–D3 pass in 3/3 MS hands. One-edit drift slope $S_{\text{edit}}$ (`Delta_l in {1,2}` minus `Delta_l >= 5`) is +0.0086 ($z = 5.2$), +0.0093 ($z = 11.5$) and +0.0060 ($z = 7.8$) in 1A, 2B and 3B, while Boccaccio (−0.0006) and Pliny (−0.0001) show zero one-edit slope. Unit-3gram cosine slope $S_{\text{cos3}}$ is +0.042, +0.042 and +0.030 ($z = 10.5\text{–}19.1$).
  - Decomposing short-lag ($\Delta\ell \in \{1,2\}$) same-folio one-edit excess over a within-quire shuffle (`D3`) shows that both a folio-wide vocabulary palette (62.8 %, 36.8 %, 59.8 %; $z = 5.5\text{–}11.7$) and within-folio sequential drift (37.2 %, 63.2 %, 40.2 %; $z = 5.2\text{–}10.9$) contribute in every hand.
- **Commits:** 7992e99 (prereg), dbfbe24 (results and log)
- **Status:** lead (each folio combines a page-level vocabulary shift with top-to-bottom line-by-line copy drift)
- **Led to:** L59, L60, L61

### L59 · 2026-10-14 15:25 · h49 de-padded seed skeleton extraction
- **Folder:** [hypotheses/h49_seed_skeleton_extraction/](hypotheses/h49_seed_skeleton_extraction/)
- **Question:** does stripping same-folio exact repeats and one-edit echoes (`local_W25` within 25 tokens, or `folio_comp` across the whole folio) uncover a language-like seed skeleton with positive word-order syntax ($D_1 > 0$) or a distinct morpheme inventory compared with the no-plaintext `page_line_copier`?
- **Done:**
  - Pre-registered. Extracted `raw`, `local_W25`, and `folio_comp` seed streams on MS hands 1A, 2B, 3B (`h30_lib.load_ms`, up to 10,500 tokens), `page_line_copier` (1A, 2B, 3B from `h47`), `naibbe_boccaccio_swap`, and `it_boccaccio`.
  - Measured `keep_rate`, 5-fold Kneser–Ney word-order gain `D1_seed` and adjacent top-50 stem bigram MI $z$-score against 100 within-folio seed permutations (`mi_adj_z`), `morphs_per_type`, and cross-folio seed continuity (`adj_folio_cos`) against 200 within-quire folio-order permutations (seed 49).
- **Result:**
  - S1 fails (0/3 hands): `D1_seed` stays negative after de-padding in every MS hand (`local_W25`: −0.225, −0.233, −0.240; `folio_comp`: −0.213, −0.153, −0.124), whereas plain `it_boccaccio` retains positive `D1_seed = +0.032` on `local_W25`.
  - S2 passes (2/3 hands: 1A `mi_adj_z = 2.29`, 2B `2.00`, 3B `1.26`), matched by `page_line_copier_2B` (`2.15`). S3 passes in 3/3 hands: on `local_W25`, MS and `page_line_copier` agree within $\pm 0.08$ on `keep_rate` (max diff 0.073), `D1_seed` (max diff 0.020), and `morphs_per_type` (max diff 0.011).
- **Commits:** ecacc79 (prereg), (results and log commit)
- **Status:** closed (de-padding one-edit echoes leaves a seed skeleton indistinguishable from the no-plaintext `h47` generator)
- **Led to:** —

### L60 · 2026-10-14 15:25 · h50 vertical header and acrostic stream
- **Folder:** [hypotheses/h50_header_acrostic_stream/](hypotheses/h50_header_acrostic_stream/)
- **Question:** do vertical sequences of paragraph-initial words (`para_words`), line-initial words (`line_words_raw`, `line_words_stripped`), or line-initial first units (`line_first_unit`) carry sequential syntax or spell vertical words down the margin?
- **Done:**
  - Pre-registered. Extracted the four vertical streams across MS hands 1A, 2B, 3B, `page_line_copier` (1A, 2B, 3B), and prose/recipe controls (`it_boccaccio`, `la_pliny_herbal`, `cucina`).
  - Scored 5-fold KN bigram gain `D1_vert` and lag-1 class MI (`M1`), vertical first-unit redundancy $R_{\text{acro}} = H_1 - h_2$ vs horizontal within-word redundancy $R_{\text{horiz}}$ and Sukhotin alternation (`M2`), and onset-stripped Line-1 to folio-body similarity vs 200 within-quire Line-1 swaps (`M3`, seed 50).
- **Result:**
  - A1 and A2 fail (0/3 hands); A3 passes (3/3 hands, and also passes in 3/3 `page_line_copier` hands). All MS vertical word streams have negative `D1_vert` (`para_words` −0.083, −0.076, −0.103; `line_words_stripped` −0.220, −0.198, −0.183; vs `cucina` `para_words` +0.427).
  - Vertical first-unit redundancy $R_{\text{acro}}$ (0.394, 0.261, 0.270 bits, driven by gallows on paragraph-first lines) is only 13.7–24.3 % of horizontal within-word redundancy (below the 50 % bar and matching prose controls at 24.4–39.7 %).
- **Commits:** ecacc79 (prereg), (results and log commit)
- **Status:** closed (no vertical word syntax or margin glyph acrostic)
- **Led to:** —

### L61 · 2026-10-14 15:25 · h51 diagram/plant label link to de-padded folio seeds
- **Folder:** [hypotheses/h51_label_to_seed_link/](hypotheses/h51_label_to_seed_link/)
- **Question:** when label-to-text matching is relaxed from exact word identity to unit edit distance $\le 1$ (`edit1_hit`) or onset-stripped 3-unit stem (`stem_hit`) and compared against de-padded folio seeds (`seed_W25`) and paragraph headers, do labels anchor their folio's seeds or paired herbal folios?
- **Done:**
  - Pre-registered. Parsed 428 label words ($\ge 2$ EVA units) across 30 folios with $\ge 20$ paragraph tokens, plus 16 herbal–pharma same-plant pairs (`ZL3b-n.txt`).
  - Tested own-folio label $\leftrightarrow$ `seed_W25` / `full_para` / `header_tokens` hit rates against 2,000 within-quire folio permutations (`Test 1`), de-padded same-plant pair rank percentiles against 2,000 random partner permutations (`Test 2`), and same-folio one-edit progeny size of label-linked vs length-matched unlinked seeds (`Test 3`, seed 51).
- **Result:**
  - L1 and L2 fail; L3 passes. On own-folio `seed_W25` (`Test 1`), `exact_hit` is 7.7 % ($p_{\text{Holm}} = 0.46$), `edit1_hit` is 33.6 % vs 32.2 % within-quire null ($z = 1.03, p_{\text{Holm}} = 0.46$), and `stem_hit` is 32.9 % vs 32.7 % ($p_{\text{Holm}} = 0.46$). On the 16 same-plant pairs (`Test 2`), de-padded `seed_W25` mean rank percentiles are 0.48–0.59 ($p \ge 0.089$).
  - In `Test 3`, label-linked seeds have larger same-folio one-edit progeny than length-matched unlinked seeds (7.00 vs 5.34, $z = 3.96, p = 0.0005$), but swapping label sets across folios within the same quire produces nearly the same gap (+0.95 vs +1.65, $p = 0.068$), showing that both draw from dense quire-level EVA word shapes rather than folio-specific label seeding.
- **Commits:** ecacc79 (prereg), (results and log commit)
- **Status:** closed (labels do not anchor folio-specific paragraph seeds or de-padded herbal–pharma pairs)
- **Led to:** —

### L62 · 2026-10-24 15:04 · h52 menstrual-plant-moon-yoga thematic reading
- **Folder:** [hypotheses/h52_menstrual_plant_moon_yoga/](hypotheses/h52_menstrual_plant_moon_yoga/)
- **Question:** does MS 408’s structure and vocabulary fit a story of woman-only creation of plants from menstrual blood in water, one plant per moon period, with yoga-like science at the end — without inventing a translation?
- **Done:**
  - Pre-registered six tests (structure order, bath–plant link, moon–plant mapping, published water/seed cribs, end register, directional bifolio) before any computing (commit 80c564c).
  - Ran on ZL3b + `quires.csv` + h09 visual tags / candidate lists + h01 `qo`/`dy`; 2,000 permutations, seed 52.
- **Result:**
  - **No match (0/6).** P1 ρ=0.20 (p=0.45): plants (mean ord 85) precede moon (138) and baths (154); end stars at 213.
  - P2 bath→herbal stem-hit 0.89 < null 0.93 (p=0.98); h09 water within-quire Holm=1.0.
  - P3 zodiac more like stars running text than herbal (0.592 vs 0.579); herbal-vs-random p=0.97.
  - P4a water/nymph vs root Δlrr=3.11 (p≈0) and P4b `qo` not herbal-enriched, but within-quire Holm=1.0 → P4 fails.
  - P5 Q20 vs Q8: 0/4 Holm; D1 matches early herbal (gap −0.009).
  - P6 only 1 mixed bifolium; forward−reverse p=0.51.
- **Commits:** 80c564c (prereg), 074f01b (results and log)
- **Status:** closed (thematic reading unsupported; nearby section/calendar/copy readings fit better)
- **Led to:** —

### L63 · 2026-10-24 15:14 · h53 hybrid picture-program + process-text working theory
- **Folder:** [hypotheses/h53_hybrid_picture_program_process_text/](hypotheses/h53_hybrid_picture_program_process_text/)
- **Question:** can MS 408 be described as an astrological herbal / spa *picture program* (Theory A) whose body text is mostly a page-and-line *copy process* (Theory D / h47), without claiming a translation?
- **Done:**
  - Pre-registered four tests (picture order, process text, split prediction, thin A residual) before any computing (commit 8c88225).
  - Newly computed medical-calendar section-order Spearman vs 1000 rank permutations (seed 53) and section↔illustration match; reused stored h47/h48/h49/h10/h51/h52 summaries for D-side and label nulls.
- **Result:**
  - **Hybrid supported (4/4).** P1 ρ=1.00 (p=0.005): herbal 72.7 → zodiac 137.5 → biological 153.9 → pharmaceutical 188.3 → stars 205.0. h52 menstrual contrast ρ=0.20 (p=0.453).
  - P2: raw D1 −0.18/−0.14/−0.17; local_W25 D1 −0.22/−0.23/−0.24; h48 D1 passes 3/3 MS hands, Boccaccio fails; `page_line_copier` 6/6 on 1A/2B/3B.
  - P3: section↔illustration match 1.00; h10 unique section R² 0.025 (≤ 0.05 bar).
  - P4: h51 L1/L2 remain false; picture anchors only (Roman months, jar/root image typology); no EVA glosses.
- **Commits:** 8c88225 (prereg), 54c590e (results and log)
- **Status:** closed (hybrid supported as working theory; not a reading)
- **Led to:** —

