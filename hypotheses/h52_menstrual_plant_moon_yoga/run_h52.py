"""Run h52 measurements and write results/measurements.json + summary.json."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h52_lib as H  # noqa: E402

OUT = HERE / "results" / "measurements.json"
SUM = HERE / "results" / "summary.json"
STATUS = HERE / "results" / "STATUS.json"


def main() -> None:
    result = H.measure_all(n_perm=H.N_PERM, seed=H.SEED)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    pred = result["predictions"]
    summary = {
        "verdict": pred["verdict"],
        "n_pass": pred["n_pass"],
        "predictions": {k: pred[k] for k in ["P1", "P2", "P3", "P4", "P5", "P6"]},
        "highlights": {
            "t1_rho": result["t1_structure"]["primary"]["spearman_rho"],
            "t1_p": result["t1_structure"]["primary"]["p"],
            "t1_means": result["t1_structure"]["means_ord"],
            "t2_hit_rate": result["t2_bath_plant"]["nymph_tube_label_stem_hit_rate"],
            "t2_p_hit": result["t2_bath_plant"]["p_hit"],
            "t3_p_cycle": result["t3_moon_plant"]["p_cycle"],
            "t4_P4": result["t4_cribs"]["P4"],
            "t5_n_sig": result["t5_end_yoga"]["n_metrics_holm_lt_05"],
            "t5_d1_gap": result["t5_end_yoga"]["d1_end_minus_early_herbal"],
            "t6_fwd_minus_rev": result["t6_directional"]["forward_minus_reverse"],
            "t6_p": result["t6_directional"]["p_directional"],
            "nearby": result["nearby_better_fits"],
        },
        "runtime_sec": result["runtime_sec"],
        "seed": result["seed"],
        "n_perm": result["n_perm"],
    }
    SUM.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    STATUS.write_text(json.dumps({"status": "complete", "verdict": pred["verdict"], "n_pass": pred["n_pass"]}, indent=2) + "\n")
    print(
        f"wrote {OUT} verdict={pred['verdict']} n_pass={pred['n_pass']} "
        f"P={pred['P1'], pred['P2'], pred['P3'], pred['P4'], pred['P5'], pred['P6']} "
        f"sec={result['runtime_sec']:.1f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
