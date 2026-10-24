"""Small tests for h54 (not the full permutation suite)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h54_lib as H  # noqa: E402


def test_spearman_and_kendall_helpers():
    order = ["a", "b", "c"]
    means = {"a": 1.0, "b": 2.0, "c": 3.0}
    rho, tau = H.order_score(order, means)
    assert abs(rho - 1.0) < 1e-9
    assert abs(tau - 1.0) < 1e-9
    means_rev = {"a": 3.0, "b": 2.0, "c": 1.0}
    rho_r, tau_r = H.order_score(order, means_rev)
    assert abs(rho_r + 1.0) < 1e-9
    assert abs(tau_r + 1.0) < 1e-9


def test_role_mask_sky_mid():
    meta = H.load_meta()
    mid = meta[H.role_mask(meta, "sky_mid")]
    assert set(mid["section"].unique()) <= {"astronomical", "cosmological", "zodiac"}
    assert len(mid) == 30  # 8 + 10 + 12 from quires map
    early = meta[H.role_mask(meta, "sky_mid_early")]
    assert not ((early["section"] == "cosmological") & (early["quire"] == 14)).any()


def test_score_predictions_verdicts():
    def pack(p1, p2, p3):
        return H.score_predictions({"P1": p1}, {"P2": p2}, {"P3": p3})

    assert pack(True, True, True)["verdict"] == "extended_order_supported"
    assert pack(True, False, True)["verdict"] == "order_ok_fragile"
    assert pack(False, True, False)["verdict"] == "not_supported"


def test_prereg_and_saved_outputs():
    assert (HERE / "PREREG.md").is_file()
    text = (HERE / "PREREG.md").read_text(encoding="utf-8")
    assert "before any h54 statistic was computed" in text
    assert "herbal` < `sky_mid` < `biological` < `pharmaceutical` < `stars`" in text
    meas = HERE / "results" / "measurements.json"
    if not meas.is_file():
        return
    data = json.loads(meas.read_text(encoding="utf-8"))
    assert data["seed"] == 54
    assert set(data["predictions"]) >= {"P1", "P2", "P3", "verdict", "n_pass"}
    assert data["predictions"]["verdict"] in {
        "extended_order_supported",
        "order_ok_fragile",
        "not_supported",
    }
