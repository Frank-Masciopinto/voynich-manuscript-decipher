"""Small tests for h52 (no full permutation suite)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h52_lib as H  # noqa: E402


def test_stem_and_js_helpers():
    assert H.stem3("otedy") == ("t", "e", "d")
    assert H.stem_or_edit1_hit("otedy", ["tedol", "qokain"]) is True
    assert H.stem_or_edit1_hit("chedy", ["qokain"]) is False
    a = __import__("collections").Counter({"a": 10, "b": 5})
    b = __import__("collections").Counter({"a": 8, "c": 2})
    assert 0 <= H.js_div(a, b) <= 1.5
    assert 0 <= H.jaccard(a, b, k=2) <= 1


def test_role_and_score_predictions():
    assert H.role_of_page("biological", 13) == "water_blood"
    assert H.role_of_page("stars", 20) == "end_yoga"
    assert H.role_of_page("stars", 8) is None
    t = {"P1": False}
    fake = {k: {"P1": False, "P2": False, "P3": False, "P4": False, "P5": False, "P6": False}[k] if False else None for k in []}
    # direct
    preds = H.score_predictions(
        {"P1": False}, {"P2": False}, {"P3": False}, {"P4": False}, {"P5": True}, {"P6": False}
    )
    assert preds["n_pass"] == 1
    assert preds["verdict"] == "no_match"
    preds2 = H.score_predictions(
        {"P1": True}, {"P2": True}, {"P3": False}, {"P4": False}, {"P5": False}, {"P6": False}
    )
    assert preds2["verdict"] == "partial_nearby"


def test_prereg_exists_and_saved_outputs_when_present():
    assert (HERE / "PREREG.md").is_file()
    meas = HERE / "results" / "measurements.json"
    if not meas.is_file():
        return
    data = json.loads(meas.read_text(encoding="utf-8"))
    assert data["seed"] == 52
    assert set(data["predictions"]) >= {"P1", "P2", "P3", "P4", "P5", "P6", "verdict", "n_pass"}
    assert data["predictions"]["verdict"] in {"match", "partial_nearby", "no_match"}
