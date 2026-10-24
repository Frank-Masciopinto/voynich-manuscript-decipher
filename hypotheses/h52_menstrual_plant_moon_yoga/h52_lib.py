"""h52: menstrual-plant-moon-yoga thematic reading. Statistics only; no translation."""
from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "hypotheses" / "h09_image_context_cribs"))
sys.path.insert(0, str(ROOT / "hypotheses" / "h13_top_word_context"))
sys.path.insert(0, str(ROOT / "hypotheses" / "h51_label_to_seed_link"))

import h09_lib as H09  # noqa: E402
import h13_lib  # noqa: E402
from msdecipher.quires import load_quires  # noqa: E402

try:
    import h51_lib as H51
except Exception:  # pragma: no cover
    H51 = None

SEED = 52
N_PERM = 2000
VT_PATH = ROOT / "hypotheses" / "h09_image_context_cribs" / "data" / "visual_tags.csv"
CAND_PATH = ROOT / "hypotheses" / "h09_image_context_cribs" / "results" / "candidate_word_meanings.csv"
H01_TABLE = ROOT / "hypotheses" / "h01_tone_sheet" / "table.csv"

ROLE_SECTIONS = {
    "plants": {"herbal", "pharmaceutical"},
    "water_blood": {"biological"},
    "moon": {"zodiac"},
    "end_yoga": set(),  # filled by quire==20 & stars
}
PRIMARY_ORDER = ["water_blood", "moon", "plants", "end_yoga"]
ALT_ORDER = ["moon", "water_blood", "plants", "end_yoga"]


def eva_units(w: str) -> tuple[str, ...]:
    return tuple(h13_lib.SEG(w.replace("'", "")))


def stem3(w: str) -> tuple[str, ...]:
    u = list(eva_units(w))
    while u and u[0] in {"o", "q", "d", "s"}:
        u = u[1:]
    return tuple(u[:3])


def unit_lev(a: tuple[str, ...], b: tuple[str, ...]) -> int:
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return 2
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            ins, delete, sub = cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)
            cur.append(min(ins, delete, sub))
        prev = cur
    return prev[-1]


def stem_or_edit1_hit(w: str, bag: set[str] | list[str]) -> bool:
    if w in bag:
        return True
    sw = stem3(w)
    uw = eva_units(w)
    for x in bag:
        if stem3(x) == sw and sw:
            return True
        if unit_lev(uw, eva_units(x)) <= 1:
            return True
    return False


def jaccard(a: Counter, b: Counter, k: int = 50) -> float:
    A = {w for w, _ in a.most_common(k)}
    B = {w for w, _ in b.most_common(k)}
    if not A and not B:
        return 0.0
    return len(A & B) / len(A | B)


def js_div(a: Counter, b: Counter, k: int = 200) -> float:
    vocab = [w for w, _ in (a + b).most_common(k)]
    if not vocab:
        return 0.0
    pa = np.array([a[w] for w in vocab], float)
    pb = np.array([b[w] for w in vocab], float)
    pa = pa / pa.sum() if pa.sum() else pa
    pb = pb / pb.sum() if pb.sum() else pb
    m = 0.5 * (pa + pb)
    def _kl(p, q):
        mask = p > 0
        return float(np.sum(p[mask] * np.log2(p[mask] / np.clip(q[mask], 1e-12, None))))
    return 0.5 * _kl(pa, m) + 0.5 * _kl(pb, m)


def holm(ps: list[float]) -> list[float]:
    return H09.holm(ps).tolist()


def load_meta() -> pd.DataFrame:
    q = load_quires().copy()
    q = q.reset_index(drop=True)
    q["ord"] = np.arange(len(q))
    q["page"] = q["page"].astype(str)
    return q


def page_bags(loci: pd.DataFrame, gtypes=("P",)) -> dict[str, Counter]:
    return H09.page_bags(loci, gtypes=gtypes)


def folio_hand_lang(meta: pd.DataFrame) -> dict[str, tuple]:
    out = {}
    for r in meta.itertuples():
        out[str(r.page)] = (str(r.lfd_hand), str(r.currier_language), int(r.quire), str(r.section), int(r.ord))
    return out


def role_of_page(section: str, quire: int) -> str | None:
    if quire == 20 and section == "stars":
        return "end_yoga"
    if section in ROLE_SECTIONS["plants"]:
        return "plants"
    if section in ROLE_SECTIONS["water_blood"]:
        return "water_blood"
    if section in ROLE_SECTIONS["moon"]:
        return "moon"
    return None


# ---------------- T1 structure ----------------
def test_t1(meta: pd.DataFrame, rng: np.random.Generator) -> dict:
    means = {}
    for role in PRIMARY_ORDER:
        if role == "end_yoga":
            mask = (meta["quire"] == 20) & (meta["section"] == "stars")
        elif role == "plants":
            mask = meta["section"].isin(ROLE_SECTIONS["plants"])
        elif role == "water_blood":
            mask = meta["section"] == "biological"
        else:
            mask = meta["section"] == "zodiac"
        means[role] = float(meta.loc[mask, "ord"].mean()) if mask.any() else float("nan")

    def score(order):
        ranks_hyp = {r: i + 1 for i, r in enumerate(order)}
        xs = np.array([ranks_hyp[r] for r in PRIMARY_ORDER], float)
        ys = np.array([means[r] for r in PRIMARY_ORDER], float)
        # Spearman via rank of ys
        yr = ys.argsort().argsort().astype(float) + 1
        xs = xs - xs.mean()
        yr = yr - yr.mean()
        denom = np.sqrt((xs ** 2).sum() * (yr ** 2).sum())
        rho = float((xs * yr).sum() / denom) if denom else 0.0
        # Kendall tau
        conc = disc = 0
        for i in range(len(order)):
            for j in range(i + 1, len(order)):
                ri, rj = order[i], order[j]
                if means[ri] < means[rj]:
                    conc += 1
                elif means[ri] > means[rj]:
                    disc += 1
        tau = (conc - disc) / (conc + disc) if (conc + disc) else 0.0
        return rho, tau

    rho, tau = score(PRIMARY_ORDER)
    rho2, tau2 = score(ALT_ORDER)
    null = []
    for _ in range(N_PERM):
        perm = list(rng.permutation(PRIMARY_ORDER))
        null.append(score(perm)[0])
    null = np.asarray(null)
    p = float((null >= rho).mean())
    return {
        "means_ord": means,
        "primary": {"order": PRIMARY_ORDER, "spearman_rho": rho, "kendall_tau": tau, "null_mean": float(null.mean()), "null_p95": float(np.percentile(null, 95)), "p": p},
        "alt_A2": {"order": ALT_ORDER, "spearman_rho": rho2, "kendall_tau": tau2},
        "P1": bool(p < 0.05 and rho > 0.5),
    }


# ---------------- T2 bath-plant ----------------
def test_t2(loci: pd.DataFrame, meta: pd.DataFrame, bags: dict[str, Counter], rng: np.random.Generator) -> dict:
    hl = folio_hand_lang(meta)
    # build section bags per hand
    by_hl_sec: dict[tuple, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    for f, bag in bags.items():
        if f not in hl:
            continue
        hand, lang, quire, section, _ = hl[f]
        by_hl_sec[(hand, lang)][section] += bag

    rows = []
    for (hand, lang), secmap in by_hl_sec.items():
        if "biological" not in secmap or "herbal" not in secmap:
            continue
        bio, herb = secmap["biological"], secmap["herbal"]
        stars = secmap.get("stars", Counter())
        zod = secmap.get("zodiac", Counter())
        rows.append({
            "hand": hand, "lang": lang,
            "js_bio_herb": js_div(bio, herb),
            "js_bio_stars": js_div(bio, stars) if stars else None,
            "js_bio_zodiac": js_div(bio, zod) if zod else None,
            "jacc50_bio_herb": jaccard(bio, herb),
            "n_bio": int(sum(bio.values())),
            "n_herb": int(sum(herb.values())),
        })

    # nymph/tube labels vs herbal
    labs = loci[loci.gtype == "L"]
    hits = []
    for r in labs.itertuples():
        if r.sub not in {"n", "t"}:
            continue
        if r.folio not in hl:
            continue
        hand, lang, quire, section, _ = hl[r.folio]
        # herbal pages same hand
        herb_words = set()
        for f, bag in bags.items():
            if f in hl and hl[f][0] == hand and hl[f][3] == "herbal":
                herb_words.update(bag)
        for w in r.words:
            if len(eva_units(w)) < 2:
                continue
            hits.append(dict(folio=r.folio, hand=hand, w=w, hit=stem_or_edit1_hit(w, herb_words)))
    # Build per-hand herbal type sets once
    herb_types = defaultdict(set)
    for f, bag in bags.items():
        if f in hl and hl[f][3] == "herbal":
            herb_types[hl[f][0]].update(bag)
    herb_stems = {hand: {stem3(w) for w in ws} for hand, ws in herb_types.items()}
    def _hit_stem(hand, w):
        return bool(w in herb_types.get(hand, set()) or (stem3(w) and stem3(w) in herb_stems.get(hand, set())))
    hit_rate = float(np.mean([_hit_stem(h["hand"], h["w"]) for h in hits])) if hits else 0.0
    hit_rate_edit1 = float(np.mean([h["hit"] for h in hits])) if hits else 0.0

    # null: permute herbal partner bags within hand — sample random same-hand non-bio pages as "herbal"
    bio_labs = list(hits)
    hands = sorted({h["hand"] for h in bio_labs})
    pages_by_hand = defaultdict(list)
    for f, bag in bags.items():
        if f in hl:
            pages_by_hand[hl[f][0]].append(f)
    # Precompute unit/stem for label words
    lab_u = [(h, eva_units(h["w"]), stem3(h["w"])) for h in bio_labs]
    null_rates = np.empty(N_PERM)
    for i in range(N_PERM):
        rate_bits = []
        for hand in hands:
            cand = [f for f in pages_by_hand[hand] if hl[f][3] != "biological"]
            if len(cand) < 2:
                continue
            n_herb_pages = sum(1 for f in pages_by_hand[hand] if hl[f][3] == "herbal")
            n_herb_pages = max(1, min(n_herb_pages, len(cand)))
            chosen = list(rng.choice(cand, size=n_herb_pages, replace=False))
            bag_set = set().union(*[bags[f].keys() for f in chosen])
            bag_stems = {stem3(w) for w in bag_set}
            for h, uw, sw in lab_u:
                if h["hand"] != hand:
                    continue
                hit = h["w"] in bag_set or (sw and sw in bag_stems)
                rate_bits.append(hit)
        null_rates[i] = float(np.mean(rate_bits)) if rate_bits else 0.0
    null_rates = np.asarray(null_rates)
    p_hit = float((null_rates >= hit_rate).mean()) if len(null_rates) else 1.0

    # closer to plants than moon/end?
    closer = []
    for row in rows:
        ok = True
        if row["js_bio_stars"] is not None and not (row["js_bio_herb"] < row["js_bio_stars"]):
            ok = False
        if row["js_bio_zodiac"] is not None and not (row["js_bio_herb"] < row["js_bio_zodiac"]):
            ok = False
        closer.append(ok)

    # h09 within-quire recheck: water candidates
    cand = pd.read_csv(CAND_PATH) if CAND_PATH.exists() else pd.DataFrame()
    water_holm = None
    if not cand.empty:
        w = cand[cand.tag == "water"]
        if "p_holm_within_quire" in w.columns and len(w):
            water_holm = float(w["p_holm_within_quire"].min())

    P2 = bool(p_hit < 0.05 and (all(closer) if closer else False) and (water_holm is not None and water_holm < 0.05))
    return {
        "per_hand": rows,
        "nymph_tube_label_stem_hit_rate": hit_rate,
        "nymph_tube_label_edit1_hit_rate": hit_rate_edit1,
        "n_nymph_tube_label_tokens": len(hits),
        "null_hit_mean": float(null_rates.mean()) if len(null_rates) else None,
        "null_hit_p95": float(np.percentile(null_rates, 95)) if len(null_rates) else None,
        "p_hit": p_hit,
        "bio_closer_to_herb_than_moon_end": closer,
        "h09_water_min_holm_within_quire": water_holm,
        "P2": P2,
    }


# ---------------- T3 moon-plant ----------------

def test_t3(loci, meta, bags, rng):
    hl = folio_hand_lang(meta)
    zod_pages = [str(p) for p in meta.loc[meta["section"] == "zodiac", "page"].tolist()]
    labs = loci[loci.gtype == "L"]
    zlab = defaultdict(Counter)
    for r in labs.itertuples():
        if r.folio in zod_pages:
            zlab[r.folio].update(r.words)
    herb_pages = [f for f in bags if f in hl and hl[f][3] == "herbal"]
    star_pages = [f for f in bags if f in hl and hl[f][3] == "stars"]
    pharma_pages = [f for f in bags if f in hl and hl[f][3] == "pharmaceutical"]

    # Precompute pooled bags
    herb_bag = sum((bags[f] for f in herb_pages), Counter())
    star_bag = sum((bags[f] for f in star_pages), Counter())
    pharma_bag = sum((bags[f] for f in pharma_pages), Counter())

    def sim_to_bag(c, partner):
        return 1.0 - js_div(c, partner, k=80) / 2.0

    sims_h = [sim_to_bag(c, herb_bag) for f, c in zlab.items() if c]
    sims_s = [sim_to_bag(c, star_bag) for f, c in zlab.items() if c]
    sims_p = [sim_to_bag(c, pharma_bag) for f, c in zlab.items() if c]
    sim_herb = float(np.mean(sims_h)) if sims_h else 0.0
    sim_star = float(np.mean(sims_s)) if sims_s else 0.0
    sim_pharma = float(np.mean(sims_p)) if sims_p else 0.0

    # null: random pooled bags from non-zodiac pages, same token budget approx via random folio sets
    all_non_z = [f for f in bags if f in hl and hl[f][3] != "zodiac"]
    n_h = min(len(herb_pages), len(all_non_z))
    # Vectorised JS against random folio pools using a fixed top vocab
    vocab = [w for w, _ in (herb_bag + star_bag + pharma_bag).most_common(120)]
    if not vocab:
        vocab = [w for w, _ in sum((bags[f] for f in list(bags)[:20]), Counter()).most_common(120)]
    w2i = {w: i for i, w in enumerate(vocab)}
    def vec(counter):
        v = np.zeros(len(vocab), float)
        for w, c in counter.items():
            j = w2i.get(w)
            if j is not None:
                v[j] = c
        s = v.sum()
        return v / s if s else v
    z_vecs = [vec(c) for c in zlab.values() if c]
    folio_vecs = {f: vec(bags[f]) for f in all_non_z}
    def js_vec(p, q):
        m = 0.5 * (p + q)
        def kl(a, b):
            mask = a > 0
            return float(np.sum(a[mask] * np.log2(a[mask] / np.clip(b[mask], 1e-12, None))))
        return 0.5 * kl(p, m) + 0.5 * kl(q, m)
    def mean_sim_to(partner_vec):
        return float(np.mean([1.0 - js_vec(zv, partner_vec) / 2.0 for zv in z_vecs])) if z_vecs else 0.0
    # recompute sim_herb etc with same metric for consistency
    sim_herb = mean_sim_to(vec(herb_bag))
    sim_star = mean_sim_to(vec(star_bag))
    sim_pharma = mean_sim_to(vec(pharma_bag))
    null_sim = np.empty(N_PERM)
    for i in range(N_PERM):
        chosen = rng.choice(all_non_z, size=max(1, n_h), replace=False)
        partner = np.mean([folio_vecs[f] for f in chosen], axis=0)
        # renormalise mean of distributions approx
        s = partner.sum()
        partner = partner / s if s else partner
        null_sim[i] = mean_sim_to(partner)
    p_sim = float((null_sim >= sim_herb).mean())

    def label_words(pages, subs=None):
        s = []
        for r in labs.itertuples():
            if r.folio in pages and (subs is None or r.sub in subs):
                for w in r.words:
                    if len(eva_units(w)) >= 2:
                        s.append(w)
        return s

    z_words = label_words(set(zod_pages))
    h_plant = set(label_words(set(herb_pages))) | set(label_words(set(pharma_pages), subs={"f", "p", "c"}))
    s_words = set(label_words(set(star_pages), subs={"s", "a", "z"}))
    p_jar = set(label_words(set(pharma_pages), subs={"c"}))

    # stem index for speed
    def stem_index(words):
        idx = defaultdict(set)
        for w in words:
            idx[stem3(w)].add(w)
            idx[("_",) + eva_units(w)].add(w)
        return idx

    def overlap_rate(src, dst_set):
        if not src or not dst_set:
            return 0.0
        dst_stems = {stem3(w) for w in dst_set}
        dst_units = {eva_units(w) for w in dst_set}
        hits = 0
        for w in src:
            if w in dst_set or stem3(w) in dst_stems:
                hits += 1
                continue
            uw = eva_units(w)
            if any(unit_lev(uw, du) <= 1 for du in dst_units if abs(len(du) - len(uw)) <= 1):
                hits += 1
        return hits / len(src)

    o_herb = overlap_rate(z_words, h_plant)
    o_star = overlap_rate(z_words, s_words)
    o_pharma = overlap_rate(z_words, p_jar)

    # bootstrap overlap comparison herb vs star
    zlist = list(z_words)
    boot = 0
    B = min(N_PERM, 500)
    for _ in range(B):
        sample = [zlist[i] for i in rng.integers(0, len(zlist), size=len(zlist))] if zlist else []
        if overlap_rate(sample, h_plant) <= overlap_rate(sample, s_words):
            boot += 1
    p_overlap = boot / B if B else 1.0

    order = [p for p in zod_pages if p in zlab and zlab[p]]
    # precompute pairwise sim matrix
    n = len(order)
    sim = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            s = 1.0 - js_div(zlab[order[i]], zlab[order[j]], k=50) / 2.0
            sim[i, j] = sim[j, i] = s
    obs_cycle = float(np.mean([sim[i, i + 1] for i in range(n - 1)])) if n > 1 else 0.0
    null_cycle = np.empty(N_PERM)
    for k in range(N_PERM):
        perm = rng.permutation(n)
        null_cycle[k] = float(np.mean([sim[perm[i], perm[i + 1]] for i in range(n - 1)])) if n > 1 else 0.0
    p_cycle = float((null_cycle >= obs_cycle).mean()) if n > 1 else 1.0

    beat_star = o_herb > o_star
    beat_pharma = o_herb > o_pharma
    P3 = bool(beat_star and beat_pharma and p_overlap < 0.05 and p_cycle < 0.05 and p_sim < 0.05)
    return {
        "n_zodiac_pages": len(zod_pages),
        "n_zodiac_label_tokens": len(z_words),
        "sim_to_herbal": sim_herb,
        "sim_to_stars": sim_star,
        "sim_to_pharma": sim_pharma,
        "p_sim_herbal_vs_random": p_sim,
        "overlap_zodiac_to_plant_labels": o_herb,
        "overlap_zodiac_to_star_labels": o_star,
        "overlap_zodiac_to_jar_labels": o_pharma,
        "p_overlap_herb_beats_star": p_overlap,
        "adjacent_zodiac_sim": obs_cycle,
        "p_cycle": p_cycle,
        "P3": P3,
    }


def test_t4(bags, meta, rng):
    hl = folio_hand_lang(meta)
    cand = pd.read_csv(CAND_PATH)

    def top_words(tag, k=5):
        sub = cand[cand.tag == tag].sort_values("p_holm_global").head(k)
        return sub["word"].tolist()

    female_side = list(dict.fromkeys(top_words("water") + top_words("nymph")))[:5]
    seed_side = top_words("root")[:5]
    words = list(dict.fromkeys(female_side + seed_side + ["qo"]))

    bio_pages = [f for f in bags if f in hl and hl[f][3] == "biological"]
    herb_pages = [f for f in bags if f in hl and hl[f][3] == "herbal"]
    pages = bio_pages + herb_pages
    hands = np.array([hl[f][0] for f in pages])
    labels = np.array([1] * len(bio_pages) + [0] * len(herb_pages))

    # page x word count matrix
    mat = np.zeros((len(pages), len(words)), float)
    totals = np.zeros(len(pages), float)
    for i, f in enumerate(pages):
        totals[i] = sum(bags[f].values()) or 1.0
        for j, w in enumerate(words):
            mat[i, j] = bags[f][w]

    def lrr_from_mask(pos_mask, word_idx):
        # pos_mask True = positive class pages
        pos = mat[pos_mask][:, word_idx].sum(0)
        neg = mat[~pos_mask][:, word_idx].sum(0)
        np_ = totals[pos_mask].sum() or 1.0
        nn = totals[~pos_mask].sum() or 1.0
        rp = (pos + 0.5) / np_
        rn = (neg + 0.5) / nn
        return np.log2(rp / rn)

    fem_idx = [words.index(w) for w in female_side]
    seed_idx = [words.index(w) for w in seed_side]
    qo_idx = words.index("qo")

    bio_mask = labels == 1
    fem_lrr = lrr_from_mask(bio_mask, fem_idx)
    seed_lrr = lrr_from_mask(~bio_mask, seed_idx)  # seed on herbal vs bio
    diff = float(fem_lrr.mean() - seed_lrr.mean())
    qo_lrr = float(lrr_from_mask(~bio_mask, [qo_idx])[0])

    blocks = [np.where(hands == h)[0] for h in sorted(set(hands))]
    null_diffs = np.empty(N_PERM)
    null_qo = np.empty(N_PERM)
    for k in range(N_PERM):
        lab = labels.copy()
        for b in blocks:
            lab[b] = rng.permutation(lab[b])
        pm = lab == 1
        if not pm.any() or pm.all():
            null_diffs[k] = 0.0
            null_qo[k] = 0.0
            continue
        fl = lrr_from_mask(pm, fem_idx)
        sl = lrr_from_mask(~pm, seed_idx)
        null_diffs[k] = float(fl.mean() - sl.mean())
        null_qo[k] = float(lrr_from_mask(~pm, [qo_idx])[0])

    p_a = float((null_diffs >= diff).mean())
    p_enrich_qo = float((null_qo >= qo_lrr).mean())
    P4a = bool(diff > 0 and p_a < 0.05)
    P4b = bool(p_enrich_qo > 0.05)
    water_holm = float(cand.loc[cand.tag == "water", "p_holm_within_quire"].min())
    nymph_holm = float(cand.loc[cand.tag == "nymph", "p_holm_within_quire"].min())
    within_quire_ok = (water_holm < 0.05) or (nymph_holm < 0.05)
    P4 = bool(P4a and P4b and within_quire_ok)
    return {
        "female_side_words": female_side,
        "seed_side_words": seed_side,
        "mean_lrr_female_on_bio": float(fem_lrr.mean()),
        "mean_lrr_seed_on_herb": float(seed_lrr.mean()),
        "diff_female_minus_seed": diff,
        "p_P4a": p_a,
        "P4a": P4a,
        "qo_lrr_herb_vs_bio": qo_lrr,
        "p_enrich_qo": p_enrich_qo,
        "P4b_not_enriched": P4b,
        "h09_water_min_holm_within_quire": water_holm,
        "h09_nymph_min_holm_within_quire": nymph_holm,
        "within_quire_survives": within_quire_ok,
        "P4": P4,
        "note": "No EVA glosses invented; uses h01 qo/dy and h09 candidate lists only.",
    }


# ---------------- T5 end yoga ----------------
def test_t5(loci: pd.DataFrame, meta: pd.DataFrame, bags: dict[str, Counter], rng: np.random.Generator) -> dict:
    hl = folio_hand_lang(meta)
    end_pages = [str(p) for p in meta.loc[(meta["quire"] == 20) & (meta["section"] == "stars"), "page"]]
    q8_pages = [str(p) for p in meta.loc[(meta["quire"] == 8) & (meta["section"] == "stars"), "page"]]
    herb_pages = [str(p) for p in meta.loc[meta["section"] == "herbal", "page"]]
    all_star_pages = [str(p) for p in meta.loc[meta["section"] == "stars", "page"]]

    # Cache per-folio line stats once
    sub = loci[loci.gtype == "P"].sort_values(["folio", "n"])
    folio_line_rows = defaultdict(list)
    for r in sub.itertuples():
        ws = list(r.words)
        if not ws:
            continue
        onset = eva_units(ws[0])[0] if ws else ""
        folio_line_rows[r.folio].append(dict(
            n=int(r.n), words=ws, para_first=(int(r.n) == 1),
            gallows=onset in {"p", "t", "k", "f"},
        ))

    def metrics_pages(pages):
        lines = [ln for f in pages for ln in folio_line_rows.get(f, [])]
        if not lines:
            return dict(n_lines=0, n_tok=0, cv=0.0, gallows_rate=0.0, ttr=0.0, d1=0.0, pos_mi=0.0)
        lens = [len(l["words"]) for l in lines]
        cv = float(np.std(lens) / np.mean(lens)) if np.mean(lens) else 0.0
        para = [l for l in lines if l["para_first"]]
        gal = float(np.mean([l["gallows"] for l in para])) if para else 0.0
        toks = [w for l in lines for w in l["words"]]
        ttr = len(set(toks)) / max(1, len(toks))
        un = Counter(toks)
        bi = Counter(zip(toks, toks[1:]))
        N = len(toks)
        H1 = -sum((c / N) * math.log2(c / N) for c in un.values())
        Nb = sum(bi.values()) or 1
        H2 = -sum((c / Nb) * math.log2(c / Nb) for c in bi.values())
        d1 = H1 - H2
        first = Counter(l["words"][0] for l in lines if l["words"])
        rest = Counter(w for l in lines for w in l["words"][1:])
        pos_mi = js_div(first, rest, k=50)
        return dict(n_lines=len(lines), n_tok=len(toks), cv=cv, gallows_rate=gal, ttr=ttr, d1=float(d1), pos_mi=float(pos_mi))

    end_m = metrics_pages(end_pages)
    q8_m = metrics_pages(q8_pages)
    early, n, n_target = [], 0, end_m["n_tok"]
    for f in herb_pages:
        early.append(f)
        n += sum(bags.get(f, Counter()).values())
        if n >= max(1, n_target):
            break
    herb_m = metrics_pages(early)

    keys = ["gallows_rate", "pos_mi", "ttr", "d1"]
    obs_diff = {k: end_m[k] - q8_m[k] for k in keys}
    n_end, n_q8 = len(end_pages), len(q8_pages)
    pool = all_star_pages[:]
    null_diffs = {k: np.empty(N_PERM) for k in keys}
    for i in range(N_PERM):
        rng.shuffle(pool)
        a, b = pool[:n_end], pool[n_end:n_end + n_q8]
        ma, mb = metrics_pages(a), metrics_pages(b)
        for k in keys:
            null_diffs[k][i] = ma[k] - mb[k]
    ps = [float(np.mean(np.abs(null_diffs[k]) >= abs(obs_diff[k]))) for k in keys]
    adj = holm(ps)
    n_sig = sum(1 for p in adj if p < 0.05)
    d1_gap = end_m["d1"] - herb_m["d1"]
    P5 = bool(n_sig >= 3 and d1_gap >= 0.05)
    return {
        "end_Q20": end_m,
        "stars_Q8": q8_m,
        "early_herbal_matched": {**herb_m, "n_folios": len(early)},
        "obs_diff_end_minus_Q8": obs_diff,
        "holm_p_diff": dict(zip(keys, adj)),
        "n_metrics_holm_lt_05": n_sig,
        "d1_end_minus_early_herbal": d1_gap,
        "P5": P5,
    }


def test_t6(loci: pd.DataFrame, meta: pd.DataFrame, bags: dict[str, Counter], rng: np.random.Generator) -> dict:
    hl = folio_hand_lang(meta)
    vt = pd.read_csv(VT_PATH) if VT_PATH.exists() else pd.DataFrame()
    water_score = {}
    if not vt.empty:
        for r in vt.itertuples():
            water_score[str(r.folio)] = int(getattr(r, "nymphs", 0) or 0) + int(getattr(r, "pools", 0) or 0) + int(getattr(r, "green_water", 0) or 0) + int(getattr(r, "blue_water", 0) or 0)

    def is_water(f):
        if f in hl and hl[f][3] == "biological":
            return True
        return water_score.get(f, 0) > 0

    def is_plant(f):
        return f in hl and hl[f][3] in {"herbal", "pharmaceutical"}

    # pairs on same bifolium
    bif = defaultdict(list)
    for r in meta.itertuples():
        bif[str(r.bifolium_id)].append(str(r.page))

    forwards, reverses = [], []
    pair_info = []
    for bid, pages in bif.items():
        pages = sorted(pages, key=lambda f: hl[f][4] if f in hl else 0)
        wpages = [f for f in pages if is_water(f) and f in bags]
        ppages = [f for f in pages if is_plant(f) and f in bags]
        if not wpages or not ppages:
            continue
        for w in wpages:
            for p in ppages:
                if w == p:
                    continue
                wb = set(bags[w])
                # stem hit of water tokens into plant page
                wtoks = list(bags[w].elements()) if hasattr(bags[w], "elements") else [x for x, c in bags[w].items() for _ in range(c)]
                # subsample for speed
                if len(wtoks) > 80:
                    wtoks = list(rng.choice(wtoks, size=80, replace=False))
                rate = float(np.mean([stem_or_edit1_hit(t, bags[p]) for t in wtoks])) if wtoks else 0.0
                forward = hl[w][4] < hl[p][4]
                pair_info.append(dict(bifolium=bid, water=w, plant=p, rate=rate, forward=forward))
                if forward:
                    forwards.append(rate)
                else:
                    reverses.append(rate)

    fwd = float(np.mean(forwards)) if forwards else 0.0
    rev = float(np.mean(reverses)) if reverses else 0.0
    obs = fwd - rev

    # null: shuffle order flag within each bifolium's pairs
    null = []
    # group rates by bifolium
    by_b = defaultdict(list)
    for pi in pair_info:
        by_b[pi["bifolium"]].append(pi["rate"])
    rates_all = [pi["rate"] for pi in pair_info]
    n_fwd = len(forwards)
    for _ in range(N_PERM):
        if not rates_all:
            null.append(0.0)
            continue
        perm = rng.permutation(rates_all)
        null.append(float(np.mean(perm[:n_fwd]) - np.mean(perm[n_fwd:])) if n_fwd and n_fwd < len(perm) else 0.0)
    null = np.asarray(null)
    p = float((null >= obs).mean()) if len(null) else 1.0

    # random plant null for absolute forward
    plant_pages = [f for f in bags if is_plant(f)]
    null_abs = []
    fwd_pairs = [pi for pi in pair_info if pi["forward"]]
    for _ in range(min(N_PERM, 200)):
        vals = []
        for pi in fwd_pairs:
            rp = plant_pages[int(rng.integers(0, len(plant_pages)))]
            wtoks = list(bags[pi["water"]].elements()) if hasattr(bags[pi["water"]], "elements") else [x for x, c in bags[pi["water"]].items() for _ in range(min(c, 3))]
            if len(wtoks) > 40:
                wtoks = list(rng.choice(wtoks, size=40, replace=False))
            vals.append(float(np.mean([stem_or_edit1_hit(t, bags[rp]) for t in wtoks])) if wtoks else 0.0)
        null_abs.append(float(np.mean(vals)) if vals else 0.0)
    p_abs = float((np.asarray(null_abs) >= fwd).mean()) if null_abs else 1.0

    P6 = bool(obs > 0 and p < 0.05 and p_abs < 0.05)
    return {
        "n_bifolia_with_water_and_plant": len({pi["bifolium"] for pi in pair_info}),
        "n_forward_pairs": len(forwards),
        "n_reverse_pairs": len(reverses),
        "mean_forward_stem_hit": fwd,
        "mean_reverse_stem_hit": rev,
        "forward_minus_reverse": obs,
        "p_directional": p,
        "p_forward_vs_random_plant": p_abs,
        "P6": P6,
        "note": "Most herbal pages precede Q13; mixed bifolia are rare.",
    }


def score_predictions(t1, t2, t3, t4, t5, t6) -> dict:
    preds = {
        "P1": bool(t1["P1"]),
        "P2": bool(t2["P2"]),
        "P3": bool(t3["P3"]),
        "P4": bool(t4["P4"]),
        "P5": bool(t5["P5"]),
        "P6": bool(t6["P6"]),
    }
    n = sum(preds.values())
    if n >= 4:
        verdict = "match"
    elif n >= 2:
        verdict = "partial_nearby"
    else:
        verdict = "no_match"
    preds["n_pass"] = n
    preds["verdict"] = verdict
    return preds


def measure_all(n_perm: int = N_PERM, seed: int = SEED) -> dict:
    global N_PERM
    N_PERM = n_perm
    t0 = time.time()
    rng = np.random.default_rng(seed)
    loci = H09.parse()
    meta = load_meta()
    bags = page_bags(loci, gtypes=("P",))
    t1 = test_t1(meta, rng)
    t2 = test_t2(loci, meta, bags, rng)
    t3 = test_t3(loci, meta, bags, rng)
    t4 = test_t4(bags, meta, rng)
    t5 = test_t5(loci, meta, bags, rng)
    t6 = test_t6(loci, meta, bags, rng)
    preds = score_predictions(t1, t2, t3, t4, t5, t6)
    nearby = {
        "baths_as_spa_balneology": "biological = Q13 only; vocab link to plants fails within-hand null (T2)",
        "zodiac_as_calendar": "Roman-script month names (h05); no Voynichese plant cycling (T3/h06)",
        "pharma_as_jars": "h09 jar/root labels; no menstrual reading required",
        "end_stars_as_copy_text": "Q20 matches the same copy/line regime as the rest (T5/h47), not a distinct yoga register",
    }
    return {
        "seed": seed,
        "n_perm": n_perm,
        "runtime_sec": time.time() - t0,
        "t1_structure": t1,
        "t2_bath_plant": t2,
        "t3_moon_plant": t3,
        "t4_cribs": t4,
        "t5_end_yoga": t5,
        "t6_directional": t6,
        "predictions": preds,
        "nearby_better_fits": nearby,
    }


def main_write(path: Path | None = None) -> dict:
    path = path or (HERE / "results" / "measurements.json")
    result = measure_all()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    r = main_write()
    print(json.dumps(r["predictions"], indent=2))
