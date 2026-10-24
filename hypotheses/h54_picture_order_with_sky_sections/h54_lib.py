"""h54: picture order with astronomical/cosmological sky block. No translation."""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))
from msdecipher.quires import load_quires  # noqa: E402

SEED = 54
N_PERM = 1000
N_BOOT = 1000

PRIMARY_ROLES = ["herbal", "sky_mid", "biological", "pharmaceutical", "stars"]

S1_ORDER = [
    "herbal",
    "astronomical",
    "cosmological",
    "zodiac",
    "biological",
    "pharmaceutical",
    "stars",
]
S2_ORDER = ["herbal", "sky_mid_early", "biological", "pharmaceutical", "stars"]
S3_ORDER = ["herbal", "zodiac", "biological", "pharmaceutical", "stars"]  # h53
S4_ORDER = ["water_blood", "moon", "plants", "end_yoga"]  # h52


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_meta() -> pd.DataFrame:
    q = load_quires().copy().reset_index(drop=True)
    q["ord"] = np.arange(len(q), dtype=int)
    q["page"] = q["page"].astype(str)
    q["quire"] = q["quire"].astype(int)
    q["lfd_hand"] = q["lfd_hand"].astype(str)
    q["section"] = q["section"].astype(str)
    return q


def spearman_rho(xs: np.ndarray, ys: np.ndarray) -> float:
    rx = pd.Series(xs).rank().to_numpy(dtype=float)
    ry = pd.Series(ys).rank().to_numpy(dtype=float)
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def kendall_tau(order: list[str], means: dict[str, float]) -> float:
    conc = disc = 0
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            a, b = order[i], order[j]
            if means[a] < means[b]:
                conc += 1
            elif means[a] > means[b]:
                disc += 1
    return (conc - disc) / (conc + disc) if (conc + disc) else 0.0


def role_mask(meta: pd.DataFrame, role: str) -> pd.Series:
    sec = meta["section"]
    if role == "sky_mid":
        return sec.isin(["astronomical", "cosmological", "zodiac"])
    if role == "sky_mid_early":
        return sec.isin(["astronomical", "zodiac"]) | (
            (sec == "cosmological") & meta["quire"].isin([8, 9, 10])
        )
    if role == "water_blood":
        return sec == "biological"
    if role == "moon":
        return sec == "zodiac"
    if role == "plants":
        return sec.isin(["herbal", "pharmaceutical"])
    if role == "end_yoga":
        return (meta["quire"] == 20) & (sec == "stars")
    return sec == role


def role_means(meta: pd.DataFrame, roles: list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for r in roles:
        mask = role_mask(meta, r)
        out[r] = float(meta.loc[mask, "ord"].mean()) if mask.any() else float("nan")
    return out


def order_score(order: list[str], means: dict[str, float]) -> tuple[float, float]:
    hyp = np.array([i + 1 for i in range(len(order))], float)
    obs = np.array([means[r] for r in order], float)
    return spearman_rho(hyp, obs), kendall_tau(order, means)


def perm_p(
    order: list[str], means: dict[str, float], rng: np.random.Generator, n_perm: int
) -> tuple[float, float, float, float]:
    rho, tau = order_score(order, means)
    null = []
    for _ in range(n_perm):
        perm = list(rng.permutation(order))
        null.append(order_score(perm, means)[0])
    null = np.asarray(null, float)
    p = float(np.mean(null >= rho))
    return rho, tau, p, float(np.percentile(null, 95))


def score_block(
    order: list[str], meta: pd.DataFrame, rng: np.random.Generator, n_perm: int
) -> dict:
    means = role_means(meta, order)
    if any(np.isnan(list(means.values()))):
        return {
            "order": order,
            "means_ord": means,
            "spearman_rho": float("nan"),
            "kendall_tau": float("nan"),
            "p": float("nan"),
            "null_p95": float("nan"),
            "missing_role": True,
        }
    rho, tau, p, p95 = perm_p(order, means, rng, n_perm)
    return {
        "order": order,
        "means_ord": means,
        "spearman_rho": rho,
        "kendall_tau": tau,
        "p": p,
        "null_p95": p95,
        "missing_role": False,
    }


def sky_page_map(meta: pd.DataFrame) -> dict:
    sky_secs = ["astronomical", "cosmological", "zodiac", "stars"]
    rows = []
    for _, r in meta[meta["section"].isin(sky_secs)].iterrows():
        rows.append(
            {
                "page": r["page"],
                "quire": int(r["quire"]),
                "section": r["section"],
                "ord": int(r["ord"]),
                "lfd_hand": r["lfd_hand"],
                "illustration": r["illustration"],
            }
        )
    by_sec = {}
    for sec in sky_secs:
        m = meta[meta["section"] == sec]
        by_sec[sec] = {
            "n": int(len(m)),
            "mean_ord": float(m["ord"].mean()) if len(m) else float("nan"),
            "min_ord": int(m["ord"].min()) if len(m) else None,
            "max_ord": int(m["ord"].max()) if len(m) else None,
            "quires": sorted(int(x) for x in m["quire"].unique()),
        }
    return {"pages": rows, "by_section": by_sec}


def test_t1(meta: pd.DataFrame, rng: np.random.Generator, n_perm: int = N_PERM) -> dict:
    primary = score_block(PRIMARY_ROLES, meta, rng, n_perm)
    s1 = score_block(S1_ORDER, meta, rng, n_perm)
    s2 = score_block(S2_ORDER, meta, rng, n_perm)
    s3 = score_block(S3_ORDER, meta, rng, n_perm)
    s4 = score_block(S4_ORDER, meta, rng, n_perm)
    P1 = bool(
        (not primary["missing_role"])
        and primary["spearman_rho"] > 0.6
        and primary["p"] < 0.05
    )
    return {
        "primary": primary,
        "sensitivity_S1_seven_role": s1,
        "sensitivity_S2_sky_mid_early": s2,
        "contrast_S3_h53_five_step": s3,
        "contrast_S4_h52_menstrual": s4,
        "sky_map": sky_page_map(meta),
        "P1": P1,
    }


def _pages_from_quire_draw(meta: pd.DataFrame, drawn_quires: np.ndarray) -> pd.DataFrame:
    parts = []
    for qid in drawn_quires:
        chunk = meta[meta["quire"] == int(qid)]
        if len(chunk):
            parts.append(chunk)
    if not parts:
        return meta.iloc[0:0].copy()
    return pd.concat(parts, ignore_index=True)


def test_t2(
    meta: pd.DataFrame, rng: np.random.Generator, n_boot: int = N_BOOT
) -> dict:
    quires = np.array(sorted(meta["quire"].unique()), dtype=int)
    boot_rhos: list[float] = []
    attempts = 0
    max_attempts = n_boot * 50
    while len(boot_rhos) < n_boot and attempts < max_attempts:
        attempts += 1
        drawn = rng.choice(quires, size=len(quires), replace=True)
        sub = _pages_from_quire_draw(meta, drawn)
        means = role_means(sub, PRIMARY_ROLES)
        if any(np.isnan(list(means.values()))):
            continue
        rho, _ = order_score(PRIMARY_ROLES, means)
        if np.isnan(rho):
            continue
        boot_rhos.append(float(rho))
    boot_rhos_a = np.asarray(boot_rhos, float)
    p5 = float(np.percentile(boot_rhos_a, 5)) if len(boot_rhos_a) else float("nan")
    P2a = bool(len(boot_rhos_a) == n_boot and p5 > 0.6)

    loqo = []
    primary_quires = sorted(
        int(q)
        for q in meta.loc[
            role_mask(meta, "herbal")
            | role_mask(meta, "sky_mid")
            | role_mask(meta, "biological")
            | role_mask(meta, "pharmaceutical")
            | role_mask(meta, "stars"),
            "quire",
        ].unique()
    )
    for qid in primary_quires:
        sub = meta[meta["quire"] != qid]
        means = role_means(sub, PRIMARY_ROLES)
        if any(np.isnan(list(means.values()))):
            loqo.append(
                {
                    "dropped_quire": qid,
                    "spearman_rho": None,
                    "evaluable": False,
                    "reason": "missing_role",
                }
            )
            continue
        rho, _ = order_score(PRIMARY_ROLES, means)
        loqo.append(
            {
                "dropped_quire": qid,
                "spearman_rho": float(rho),
                "evaluable": True,
                "means_ord": means,
            }
        )
    eval_rhos = [r["spearman_rho"] for r in loqo if r["evaluable"]]
    P2b = bool(eval_rhos) and all(r > 0.6 for r in eval_rhos)

    # Hand coverage (report-only)
    roles_for_tab = [
        "herbal",
        "astronomical",
        "cosmological",
        "zodiac",
        "biological",
        "pharmaceutical",
        "stars",
    ]
    tab = (
        meta[meta["section"].isin(roles_for_tab)]
        .groupby(["lfd_hand", "section"])
        .size()
        .unstack(fill_value=0)
    )
    coverage = {str(h): {c: int(tab.loc[h, c]) if c in tab.columns else 0 for c in roles_for_tab} for h in tab.index}
    hand4 = meta[meta["lfd_hand"] == "4"]
    sky_internal = {
        "astronomical_mean_ord": float(hand4.loc[hand4["section"] == "astronomical", "ord"].mean())
        if (hand4["section"] == "astronomical").any()
        else None,
        "cosmological_mean_ord": float(hand4.loc[hand4["section"] == "cosmological", "ord"].mean())
        if (hand4["section"] == "cosmological").any()
        else None,
        "zodiac_mean_ord": float(hand4.loc[hand4["section"] == "zodiac", "ord"].mean())
        if (hand4["section"] == "zodiac").any()
        else None,
    }

    P2 = bool(P2a and P2b)
    return {
        "bootstrap": {
            "n_requested": n_boot,
            "n_valid": int(len(boot_rhos_a)),
            "attempts": attempts,
            "rho_mean": float(boot_rhos_a.mean()) if len(boot_rhos_a) else float("nan"),
            "rho_median": float(np.median(boot_rhos_a)) if len(boot_rhos_a) else float("nan"),
            "rho_p5": p5,
            "rho_p95": float(np.percentile(boot_rhos_a, 95)) if len(boot_rhos_a) else float("nan"),
            "frac_rho_gt_0_6": float(np.mean(boot_rhos_a > 0.6)) if len(boot_rhos_a) else float("nan"),
            "P2a": P2a,
        },
        "leave_one_quire_out": {
            "rows": loqo,
            "n_evaluable": len(eval_rhos),
            "min_rho": float(min(eval_rhos)) if eval_rhos else float("nan"),
            "P2b": P2b,
        },
        "hand_coverage": {
            "counts": coverage,
            "note": (
                "No single lfd_hand covers the full five-role primary program; "
                "sky/zodiac lean hand 4, baths hand 2, Q20 stars hand 3 (report-only)."
            ),
            "hand4_sky_internal_means": sky_internal,
            "P2c_votes": False,
        },
        "P2": P2,
    }


def test_t3(t1: dict, meta: pd.DataFrame) -> dict:
    means = t1["primary"]["means_ord"]
    order = PRIMARY_ROLES
    strictly_increasing = all(
        means[order[i]] < means[order[i + 1]] for i in range(len(order) - 1)
    )
    revise = bool(t1["P1"] and strictly_increasing)
    revised_story = (
        "plants → calendar/sky block (astronomical ∪ cosmological ∪ zodiac) "
        "→ baths → pharmacy → stars"
    )
    # Document interleaving facts (deterministic from meta, not a free claim)
    cosmo = meta[meta["section"] == "cosmological"]
    stars = meta[meta["section"] == "stars"]
    facts = {
        "astronomical_quires": sorted(int(x) for x in meta.loc[meta["section"] == "astronomical", "quire"].unique()),
        "cosmological_quires": sorted(int(x) for x in cosmo["quire"].unique()),
        "zodiac_quires": sorted(int(x) for x in meta.loc[meta["section"] == "zodiac", "quire"].unique()),
        "stars_quires": sorted(int(x) for x in stars["quire"].unique()),
        "early_Q8_stars_n": int(((stars["quire"] == 8)).sum()),
        "late_Q20_stars_n": int(((stars["quire"] == 20)).sum()),
        "cosmo_after_biological_n": int((cosmo["ord"] > meta.loc[meta["section"] == "biological", "ord"].max()).sum())
        if (meta["section"] == "biological").any()
        else 0,
        "cosmo_Q14_n": int((cosmo["quire"] == 14).sum()),
    }
    P3 = bool(t1["P1"] and revise)
    return {
        "strictly_increasing_primary_means": strictly_increasing,
        "revise_hybrid_picture_story": revise,
        "revised_story_if_true": revised_story,
        "interleave_facts": facts,
        "P3": P3,
        "disclaimer": (
            "Picture-program revision only. Not a translation. "
            "Process-text side of h53 not re-tested."
        ),
    }


def score_predictions(t1: dict, t2: dict, t3: dict) -> dict:
    P1, P2, P3 = t1["P1"], t2["P2"], t3["P3"]
    n_pass = int(P1) + int(P2) + int(P3)
    if P1 and P2 and P3:
        verdict = "extended_order_supported"
    elif P1 and P3 and not P2:
        verdict = "order_ok_fragile"
    else:
        verdict = "not_supported"
    return {"P1": P1, "P2": P2, "P3": P3, "n_pass": n_pass, "verdict": verdict}


def measure_all(n_perm: int = N_PERM, n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    meta = load_meta()
    t1 = test_t1(meta, rng, n_perm=n_perm)
    t2 = test_t2(meta, rng, n_boot=n_boot)
    t3 = test_t3(t1, meta)
    pred = score_predictions(t1, t2, t3)
    return {
        "hypothesis": "h54_picture_order_with_sky_sections",
        "seed": seed,
        "n_perm": n_perm,
        "n_boot": n_boot,
        "prereg_commit_hint": "committed before computing; see git log for PREREG.md",
        "t1_extended_order": t1,
        "t2_quire_hand_sensitivity": t2,
        "t3_hybrid_story": t3,
        "predictions": pred,
        "runtime_sec": time.time() - t0,
        "disclaimer": (
            "Working theory about picture program order with sky sections. "
            "Not a translation. No EVA glosses invented."
        ),
    }
