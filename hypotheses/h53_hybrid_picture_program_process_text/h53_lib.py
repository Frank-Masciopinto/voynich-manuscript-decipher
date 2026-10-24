"""h53: hybrid picture-program (A) + process text (D). Statistics only; no translation."""
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

SEED = 53
N_PERM = 1000

PRIMARY_ROLES = ["herbal", "zodiac", "biological", "pharmaceutical", "stars"]
PRIMARY_RANKS = {r: i + 1 for i, r in enumerate(PRIMARY_ROLES)}

SECTION_TO_ILLUST = {
    "herbal": "H",
    "zodiac": "Z",
    "biological": "B",
    "pharmaceutical": "P",
    "stars": "S",
    "cosmological": "C",
    "astronomical": "A",
    "text-only": "T",
}

H47 = ROOT / "hypotheses" / "h47_page_line_generator" / "results" / "summary.json"
H48 = ROOT / "hypotheses" / "h48_within_folio_drift" / "results" / "summary.json"
H49 = ROOT / "hypotheses" / "h49_seed_skeleton_extraction" / "results" / "summary.json"
H10_VAR = ROOT / "hypotheses" / "h10_section_vs_quire_hand" / "results" / "variance_decomposition.csv"
H10_SUM = ROOT / "hypotheses" / "h10_section_vs_quire_hand" / "results" / "summary.json"
H51 = ROOT / "hypotheses" / "h51_label_to_seed_link" / "results" / "summary.json"
H52 = ROOT / "hypotheses" / "h52_menstrual_plant_moon_yoga" / "results" / "summary.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_meta() -> pd.DataFrame:
    q = load_quires().copy().reset_index(drop=True)
    q["ord"] = np.arange(len(q))
    q["page"] = q["page"].astype(str)
    return q


def spearman_rho(xs: np.ndarray, ys: np.ndarray) -> float:
    """Spearman via average ranks (pandas), same as h05_lib.spearman."""
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


def role_means(meta: pd.DataFrame, roles: list[str], sky_late: bool = False) -> dict[str, float]:
    out = {}
    for r in roles:
        if r == "sky_late":
            mask = meta["section"].isin(["stars", "cosmological"])
        else:
            mask = meta["section"] == r
        out[r] = float(meta.loc[mask, "ord"].mean()) if mask.any() else float("nan")
    return out


def order_score(order: list[str], means: dict[str, float]) -> tuple[float, float]:
    hyp = np.array([i + 1 for i in range(len(order))], float)
    obs = np.array([means[r] for r in order], float)
    return spearman_rho(hyp, obs), kendall_tau(order, means)


def perm_p(order: list[str], means: dict[str, float], rng: np.random.Generator, n_perm: int) -> tuple[float, float, float, float]:
    rho, tau = order_score(order, means)
    null = []
    for _ in range(n_perm):
        perm = list(rng.permutation(order))
        null.append(order_score(perm, means)[0])
    null = np.asarray(null, float)
    p = float((null >= rho).mean())
    return rho, tau, p, float(np.percentile(null, 95))


# ---------------- T1 ----------------
def test_t1(meta: pd.DataFrame, rng: np.random.Generator, n_perm: int = N_PERM) -> dict:
    means = role_means(meta, PRIMARY_ROLES)
    rho, tau, p, p95 = perm_p(PRIMARY_ROLES, means, rng, n_perm)

    # Sensitivity A2: sky_late = stars ∪ cosmological
    a2_order = ["herbal", "zodiac", "biological", "pharmaceutical", "sky_late"]
    means_a2 = role_means(meta, a2_order, sky_late=True)
    rho_a2, tau_a2, p_a2, _ = perm_p(a2_order, means_a2, rng, n_perm)

    # h52 menstrual contrast on same book
    plants = float(meta.loc[meta["section"].isin(["herbal", "pharmaceutical"]), "ord"].mean())
    water = float(meta.loc[meta["section"] == "biological", "ord"].mean())
    moon = float(meta.loc[meta["section"] == "zodiac", "ord"].mean())
    end = float(meta.loc[(meta["quire"] == 20) & (meta["section"] == "stars"), "ord"].mean())
    h52_order = ["water_blood", "moon", "plants", "end_yoga"]
    h52_means = {
        "water_blood": water,
        "moon": moon,
        "plants": plants,
        "end_yoga": end,
    }
    rho52, tau52, p52, _ = perm_p(h52_order, h52_means, rng, n_perm)

    stored_h52 = None
    if H52.is_file():
        s = load_json(H52)
        stored_h52 = {
            "stored_verdict": s.get("verdict"),
            "stored_t1_rho": s.get("highlights", {}).get("t1_rho"),
            "stored_t1_p": s.get("highlights", {}).get("t1_p"),
        }

    P1 = bool(rho > 0.6 and p < 0.05)
    return {
        "means_ord": means,
        "primary": {
            "order": PRIMARY_ROLES,
            "spearman_rho": rho,
            "kendall_tau": tau,
            "p": p,
            "null_p95": p95,
        },
        "sensitivity_A2": {
            "order": a2_order,
            "means_ord": means_a2,
            "spearman_rho": rho_a2,
            "kendall_tau": tau_a2,
            "p": p_a2,
        },
        "h52_contrast": {
            "order": h52_order,
            "means_ord": h52_means,
            "spearman_rho": rho52,
            "kendall_tau": tau52,
            "p": p52,
            "stored": stored_h52,
        },
        "P1": P1,
    }


# ---------------- T2 ----------------
def test_t2() -> dict:
    h47 = load_json(H47)
    h48 = load_json(H48)
    h49 = load_json(H49)

    hands = ["1A", "2B", "3B"]
    raw_d1 = {}
    depadded_d1 = {}
    for h in hands:
        by = h49["predictions"]["S1"]["by_hand"][h]
        raw_d1[h] = float(by["raw_D1"])
        depadded_d1[h] = float(by["local_W25_D1"])

    p2a_hands = [h for h in hands if raw_d1[h] <= 0.0]
    p2a = len(p2a_hands) >= 2
    dep_hands = [h for h in hands if depadded_d1[h] <= 0.0]
    p2_depadded = len(dep_hands) >= 2

    h48_pred = h48["predictions"]
    ms_drift_hands = list(h48_pred.get("D1_pass_hands", []))
    # Italian control must fail D1
    bocc = next(r for r in h48["slopes_and_half_drift"] if r["stream"] == "it_boccaccio")
    italian_fails_d1 = (not bool(bocc.get("D1_pass"))) or float(bocc.get("S_edit", 0)) <= 0.0
    p2_drift = len(ms_drift_hands) >= 2 and italian_fails_d1

    n_passed = h47["predictions"]["U2"]["n_passed_by_hand"]
    plc_ok_hands = [h for h in hands if int(n_passed.get(h, 0)) >= 5]
    p2_plc = len(plc_ok_hands) >= 2

    P2 = bool(p2a and p2_depadded and p2_drift and p2_plc)
    return {
        "raw_D1": raw_d1,
        "local_W25_D1": depadded_d1,
        "P2a_hands_D1_le_0": p2a_hands,
        "P2a": p2a,
        "depadded_hands_D1_le_0": dep_hands,
        "P2_depadded": p2_depadded,
        "h48_D1_pass_hands": ms_drift_hands,
        "it_boccaccio_S_edit": float(bocc["S_edit"]),
        "it_boccaccio_D1_pass": bool(bocc["D1_pass"]),
        "P2_drift": p2_drift,
        "page_line_copier_n_passed": n_passed,
        "plc_ok_hands": plc_ok_hands,
        "P2_plc": p2_plc,
        "P2": P2,
        "sources": ["h47", "h48", "h49"],
    }


# ---------------- T3 ----------------
def test_t3(meta: pd.DataFrame) -> dict:
    expected = meta["section"].map(SECTION_TO_ILLUST)
    match_rate = float((expected == meta["illustration"]).mean())
    # NMI-like: since mapping is deterministic, report match + contingency size
    n_mismatch = int((expected != meta["illustration"]).sum())
    P3a = match_rate >= 0.95

    var = pd.read_csv(H10_VAR)
    sec_row = var.loc[var["factor"] == "section"].iloc[0]
    unique_section_r2 = float(sec_row["unique_R2"])
    alone_section_r2 = float(sec_row["alone_R2"])
    quire_unique = float(var.loc[var["factor"] == "quire", "unique_R2"].iloc[0])
    hand_unique = float(var.loc[var["factor"] == "hand", "unique_R2"].iloc[0])

    h10_sum = load_json(H10_SUM) if H10_SUM.is_file() else {}
    # P3b: unique section R² ≤ 0.05 (pre-registered), aligning with FINDINGS that
    # section on hand residuals vanishes once quire is removed.
    P3b = unique_section_r2 <= 0.05

    P3 = bool(P3a and P3b)
    return {
        "section_illustration_match_rate": match_rate,
        "n_mismatch": n_mismatch,
        "n_pages": int(len(meta)),
        "P3a": P3a,
        "unique_section_R2": unique_section_r2,
        "alone_section_R2": alone_section_r2,
        "unique_quire_R2": quire_unique,
        "unique_hand_R2": hand_unique,
        "h10_summary_keys": list(h10_sum.keys()),
        "note": (
            "Section↔illustration is the picture coding. Unique section R² from h10 "
            "is small; FINDINGS/h11: section on hand residuals dies when quire is removed."
        ),
        "P3b": P3b,
        "P3": P3,
        "sources": ["quires.csv", "h10"],
    }


# ---------------- T4 ----------------
def test_t4(t1: dict) -> dict:
    h51 = load_json(H51)
    L1 = bool(h51["predictions"]["L1"])
    L2 = bool(h51["predictions"]["L2"])
    labels_null = (not L1) and (not L2)
    picture_order_ok = bool(t1["P1"])
    anchors = {
        "roman_month_names_h05": (
            "Zodiac circle-centre words are later Roman-script month names "
            "(Mars, Abril, May, …), not Voynichese (h05)."
        ),
        "image_typology": (
            "Illustration codes track section (H herbal plants, Z zodiac, B baths/nymphs, "
            "P pharma jars/roots, S stars) — picture-side only; no EVA glosses."
        ),
    }
    P4 = bool(picture_order_ok and labels_null)
    return {
        "h51_L1": L1,
        "h51_L2": L2,
        "h51_L1_edit1_p_holm": h51["predictions"].get("L1_edit1_p_holm"),
        "h51_L2_primary_p": h51["predictions"].get("L2_primary_p"),
        "labels_remain_null": labels_null,
        "picture_order_P1": picture_order_ok,
        "anchors_used": anchors,
        "P4": P4,
        "sources": ["h51", "h05", "T1"],
    }


def score_predictions(t1: dict, t2: dict, t3: dict, t4: dict) -> dict:
    P1, P2, P3, P4 = t1["P1"], t2["P2"], t3["P3"], t4["P4"]
    n_pass = int(P1) + int(P2) + int(P3) + int(P4)
    if P1 and P2 and P3 and P4:
        verdict = "hybrid_supported"
    elif P1 and P4 and (not P2 or not P3):
        verdict = "picture_only"
    elif P2 and not P1:
        verdict = "process_only"
    else:
        verdict = "unsupported"
    return {
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "P4": P4,
        "n_pass": n_pass,
        "verdict": verdict,
    }


def measure_all(n_perm: int = N_PERM, seed: int = SEED) -> dict:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    meta = load_meta()
    t1 = test_t1(meta, rng, n_perm=n_perm)
    t2 = test_t2()
    t3 = test_t3(meta)
    t4 = test_t4(t1)
    pred = score_predictions(t1, t2, t3, t4)
    return {
        "hypothesis": "h53_hybrid_picture_program_process_text",
        "seed": seed,
        "n_perm": n_perm,
        "t1_picture_order": t1,
        "t2_process_text": t2,
        "t3_split": t3,
        "t4_thin_residual": t4,
        "predictions": pred,
        "runtime_sec": time.time() - t0,
        "disclaimer": (
            "Working theory about picture program + writing process. "
            "Not a translation. No EVA glosses invented."
        ),
    }
