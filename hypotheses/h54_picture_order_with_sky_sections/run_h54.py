"""Run h54 measurements and write results/measurements.json + summary.json."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h54_lib as H  # noqa: E402

OUT = HERE / "results" / "measurements.json"
SUM = HERE / "results" / "summary.json"
STATUS = HERE / "results" / "STATUS.json"


def main() -> None:
    result = H.measure_all(n_perm=H.N_PERM, n_boot=H.N_BOOT, seed=H.SEED)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    pred = result["predictions"]
    t1 = result["t1_extended_order"]
    t2 = result["t2_quire_hand_sensitivity"]
    t3 = result["t3_hybrid_story"]
    primary = t1["primary"]
    summary = {
        "hypothesis": "h54_picture_order_with_sky_sections",
        "verdict": pred["verdict"],
        "n_pass": pred["n_pass"],
        "predictions": {k: pred[k] for k in ["P1", "P2", "P3"]},
        "highlights": {
            "t1_rho": primary["spearman_rho"],
            "t1_tau": primary["kendall_tau"],
            "t1_p": primary["p"],
            "t1_means": primary["means_ord"],
            "t1_S1_rho": t1["sensitivity_S1_seven_role"]["spearman_rho"],
            "t1_S1_p": t1["sensitivity_S1_seven_role"]["p"],
            "t1_S2_rho": t1["sensitivity_S2_sky_mid_early"]["spearman_rho"],
            "t1_S2_p": t1["sensitivity_S2_sky_mid_early"]["p"],
            "t1_h53_rho": t1["contrast_S3_h53_five_step"]["spearman_rho"],
            "t1_h53_p": t1["contrast_S3_h53_five_step"]["p"],
            "t1_h52_rho": t1["contrast_S4_h52_menstrual"]["spearman_rho"],
            "t1_h52_p": t1["contrast_S4_h52_menstrual"]["p"],
            "t2_boot_rho_p5": t2["bootstrap"]["rho_p5"],
            "t2_boot_rho_median": t2["bootstrap"]["rho_median"],
            "t2_loqo_min_rho": t2["leave_one_quire_out"]["min_rho"],
            "t2_P2a": t2["bootstrap"]["P2a"],
            "t2_P2b": t2["leave_one_quire_out"]["P2b"],
            "t3_revise": t3["revise_hybrid_picture_story"],
            "t3_story": t3["revised_story_if_true"],
        },
        "runtime_sec": result["runtime_sec"],
        "seed": result["seed"],
        "n_perm": result["n_perm"],
        "n_boot": result["n_boot"],
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
        f"P=({pred['P1']}, {pred['P2']}, {pred['P3']}) "
        f"rho={primary['spearman_rho']:.3f} p={primary['p']:.4f} "
        f"boot_p5={t2['bootstrap']['rho_p5']:.3f} "
        f"loqo_min={t2['leave_one_quire_out']['min_rho']} "
        f"sec={result['runtime_sec']:.2f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
