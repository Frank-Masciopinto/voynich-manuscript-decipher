"""Run h53 measurements and write results/measurements.json + summary.json."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h53_lib as H  # noqa: E402

OUT = HERE / "results" / "measurements.json"
SUM = HERE / "results" / "summary.json"
STATUS = HERE / "results" / "STATUS.json"


def main() -> None:
    result = H.measure_all(n_perm=H.N_PERM, seed=H.SEED)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    pred = result["predictions"]
    t1 = result["t1_picture_order"]
    t2 = result["t2_process_text"]
    t3 = result["t3_split"]
    t4 = result["t4_thin_residual"]
    summary = {
        "hypothesis": "h53_hybrid_picture_program_process_text",
        "verdict": pred["verdict"],
        "n_pass": pred["n_pass"],
        "predictions": {k: pred[k] for k in ["P1", "P2", "P3", "P4"]},
        "highlights": {
            "t1_rho": t1["primary"]["spearman_rho"],
            "t1_tau": t1["primary"]["kendall_tau"],
            "t1_p": t1["primary"]["p"],
            "t1_means": t1["means_ord"],
            "t1_h52_rho": t1["h52_contrast"]["spearman_rho"],
            "t1_h52_p": t1["h52_contrast"]["p"],
            "t2_raw_D1": t2["raw_D1"],
            "t2_local_W25_D1": t2["local_W25_D1"],
            "t2_plc_n_passed": t2["page_line_copier_n_passed"],
            "t3_illust_match": t3["section_illustration_match_rate"],
            "t3_unique_section_R2": t3["unique_section_R2"],
            "t4_labels_null": t4["labels_remain_null"],
            "t4_h51_L1": t4["h51_L1"],
            "t4_h51_L2": t4["h51_L2"],
        },
        "runtime_sec": result["runtime_sec"],
        "seed": result["seed"],
        "n_perm": result["n_perm"],
        "disclaimer": result["disclaimer"],
    }
    SUM.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    STATUS.write_text(
        json.dumps(
            {"status": "complete", "verdict": pred["verdict"], "n_pass": pred["n_pass"]},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {OUT} verdict={pred['verdict']} n_pass={pred['n_pass']} "
        f"P=({pred['P1']}, {pred['P2']}, {pred['P3']}, {pred['P4']}) "
        f"rho={t1['primary']['spearman_rho']:.3f} p={t1['primary']['p']:.4f} "
        f"sec={result['runtime_sec']:.2f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
