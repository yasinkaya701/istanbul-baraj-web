#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/yasinkaya/Hackhaton")
PANEL = ROOT / "output/newdata_feature_store/tables/istanbul_dam_driver_panel_2000_2026_extended.csv"
CLIMATE_PATH = ROOT / "assets/data/climate_baseline.js"

USAGE_PROFILE_OUT = [
    ROOT / "assets/data/usage_monthly_profile.js",
    ROOT / "baraj_web/assets/data/usage_monthly_profile.js",
]
USAGE_TREND_OUT = [
    ROOT / "assets/data/usage_trend_stats.js",
    ROOT / "baraj_web/assets/data/usage_trend_stats.js",
]
SIM_COEFFS_OUT = [
    ROOT / "assets/data/sim_coeffs.js",
    ROOT / "baraj_web/assets/data/sim_coeffs.js",
]
BASELINE_OUT = [
    ROOT / "assets/data/evap_usage_baseline.js",
    ROOT / "baraj_web/assets/data/evap_usage_baseline.js",
]


def load_js_payload(path: Path, prefix: str) -> dict:
    raw = path.read_text().strip()
    if not raw.startswith(prefix):
        raise ValueError(f"Unexpected JS format in {path}")
    payload = raw[len(prefix):].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    return json.loads(payload)


def write_js_payload(path: Path, var_name: str, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"window.{var_name} = " + json.dumps(payload, ensure_ascii=False) + ";"
    path.write_text(text, encoding="utf-8")


def build_usage_stats(panel: pd.DataFrame) -> tuple[dict, dict]:
    df = panel[["date", "consumption_mean_monthly"]].dropna().copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["days"] = df["date"].dt.days_in_month
    df["month_total"] = df["consumption_mean_monthly"] * df["days"]

    counts = df.groupby("year")["month"].nunique()
    full_years = counts[counts == 12].index
    df_full = df[df["year"].isin(full_years)].copy()
    annual = df_full.groupby("year")["month_total"].sum().sort_index()
    yoy = annual.pct_change().dropna()

    year_min = int(annual.index.min())
    year_max = int(annual.index.max())
    n_years = int(len(annual))
    span_years = max(1, year_max - year_min)
    cagr_all = float((annual.iloc[-1] / annual.iloc[0]) ** (1 / span_years) - 1) if n_years > 1 else 0.0

    cagr_2019_2023 = None
    if 2019 in annual.index and 2023 in annual.index:
        cagr_2019_2023 = float((annual.loc[2023] / annual.loc[2019]) ** (1 / 4) - 1)

    trend_payload = {
        "year_min": year_min,
        "year_max": year_max,
        "n_years": n_years,
        "cagr_all": cagr_all,
        "cagr_2019_2023": cagr_2019_2023 if cagr_2019_2023 is not None else cagr_all,
        "yoy_mean": float(yoy.mean()) if len(yoy) else 0.0,
        "yoy_median": float(yoy.median()) if len(yoy) else 0.0,
        "yoy_p10": float(np.percentile(yoy, 10)) if len(yoy) else 0.0,
        "yoy_p90": float(np.percentile(yoy, 90)) if len(yoy) else 0.0,
    }

    monthly_share = (
        df_full.groupby(["year", "month"])["month_total"]
        .sum()
        .div(annual, level=0)
        .groupby("month")
        .mean()
    )
    profile = [float(monthly_share.loc[m]) for m in range(1, 13)]
    profile_payload = {
        "year_min": year_min,
        "year_max": year_max,
        "months": list(range(1, 13)),
        "profile": profile,
        "note": f"Aylik tuketim dagilimi ({year_min}-{year_max} tam yil).",
    }

    return trend_payload, profile_payload


def build_sim_coeffs(panel: pd.DataFrame, climate: dict, existing: dict) -> dict:
    df = panel.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"weighted_total_fill": "fill_pct"})
    df = df[["date", "fill_pct", "rain_mm", "et0_mm_month", "consumption_mean_monthly"]].dropna().copy()
    df = df.sort_values("date")
    df["delta_fill"] = df["fill_pct"].diff(1)
    df = df.dropna()

    X = df[["rain_mm", "et0_mm_month", "consumption_mean_monthly"]].values
    X = np.column_stack([X, np.ones(len(X))])
    Y = df["delta_fill"].values
    coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
    a, b, c, intercept = [float(v) for v in coef.tolist()]

    rows = []
    for date_str, vals in climate.items():
        year = int(date_str.split("-")[0])
        if 2010 <= year <= 2024:
            rows.append(vals)
    mean_rain = float(np.mean([r["precip_mm_month"] for r in rows])) if rows else float(df["rain_mm"].mean())
    mean_et0 = float(np.mean([r["et0_mm_month"] for r in rows])) if rows else float(df["et0_mm_month"].mean())
    mean_use = float(df["consumption_mean_monthly"].mean())

    updated = dict(existing)
    updated.update(
        {
            "a_rain": a,
            "b_et0": b,
            "c_use": c,
            "intercept": intercept,
            "mean_rain": mean_rain,
            "mean_et0": mean_et0,
            "mean_use_monthly": mean_use,
        }
    )
    return updated


def build_baseline(climate: dict, baseline: dict) -> dict:
    year = int(baseline.get("year", 2023))
    area_km2_total = float(baseline.get("area_km2_total", 99.69))
    kc = float(baseline.get("kc_open_water", 1.05))
    usage_m3 = float(baseline.get("usage_baraj_m3", 275_104_161))

    rows = []
    for date_str, vals in climate.items():
        if date_str.startswith(f"{year}-"):
            rows.append(vals)
    if not rows:
        rows = list(climate.values())

    area_m2 = area_km2_total * 1_000_000.0
    evap_total_m3 = float(
        sum((r["et0_mm_month"] / 1000.0) * kc * area_m2 for r in rows)
    )
    total_loss = evap_total_m3 + usage_m3
    evap_share = evap_total_m3 / total_loss if total_loss else 0.0
    usage_share = usage_m3 / total_loss if total_loss else 0.0

    updated = dict(baseline)
    updated.update(
        {
            "evap_total_m3": evap_total_m3,
            "usage_baraj_m3": usage_m3,
            "evap_share": evap_share,
            "usage_share": usage_share,
        }
    )
    return updated


def main() -> None:
    panel = pd.read_csv(PANEL)
    climate = load_js_payload(CLIMATE_PATH, "window.CLIMATE_BASELINE = ")

    trend_payload, profile_payload = build_usage_stats(panel)
    for out in USAGE_TREND_OUT:
        write_js_payload(out, "USAGE_TREND", trend_payload)
    for out in USAGE_PROFILE_OUT:
        write_js_payload(out, "USAGE_PROFILE", profile_payload)

    existing_coeffs = load_js_payload(SIM_COEFFS_OUT[0], "window.SIM_COEFFS = ")
    updated_coeffs = build_sim_coeffs(panel, climate, existing_coeffs)
    for out in SIM_COEFFS_OUT:
        write_js_payload(out, "SIM_COEFFS", updated_coeffs)

    baseline_existing = load_js_payload(BASELINE_OUT[0], "window.BASELINE = ")
    updated_baseline = build_baseline(climate, baseline_existing)
    for out in BASELINE_OUT:
        write_js_payload(out, "BASELINE", updated_baseline)

    print("Updated usage trend/profile, sim coeffs, and baseline.")


if __name__ == "__main__":
    main()
