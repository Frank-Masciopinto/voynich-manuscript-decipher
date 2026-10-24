"""Small tests for h53 (not the full permutation suite)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h53_lib as H  # noqa: E402


def test_spearman_and_kendall_helpers():
    # Perfect increasing order
    order = ["a", "b", "c"]
    means = {"a": 1.0, "b": 2.0, "c": 3.0}
    rho, tau = H.order_score(order, means)
    assert abs(rho - 1.0) < 1e-9
    assert abs(tau - 1.0) < 1e-9
    # Reversed
    means_rev = {"a": 3.0, "b": 2.0, "c": 1.0}
    rho_r, tau_r = H.order_score(order, means_rev)
    assert abs(rho_r + 1.0) < 1e-9
    assert abs(tau_r + 1.0) < 1e-9


def test_score_predictions_verdicts():
    def pack(p1, p2, p3, p4):
        return H.score_predictions({"P1": p1}, {"P2": p2}, {"P3": p3}, {"P4": p4})

    assert pack(True, True, True, True)["verdict"] == "hybrid_supported"
    assert pack(True, False, True, True)["verdict"] == "picture_only"
    assert pack(False, True, True, False)["verdict"] == "process_only"
    assert pack(False, False, False, False)["verdict"] == "unsupported"


def test_prereg_and_saved_outputs():
    assert (HERE / "PREREG.md").is_file()
    text = (HERE / "PREREG.md").read_text(encoding="utf-8")
    assert "before any h53 statistic was computed" in text
    meas = HERE / "results" / "measurements.json"
    if not meas.is_file():
        return
    data = json.loads(meas.read_text(encoding="utf-8"))
    assert data["seed"] == 53
    assert set(data["predictions"]) >= {"P1", "P2", "P3", "P4", "verdict", "n_pass"}
    assert data["predictions"]["verdict"] in {
        "hybrid_supported",
        "picture_only",
        "process_only",
        "unsupported",
    }
