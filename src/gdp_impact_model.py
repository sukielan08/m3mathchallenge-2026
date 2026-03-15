from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


def compute_va_sports(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["VA_sports_model"] = d["VA_gambling"] * (d["GGR_sports"] / d["GGR_gambling_total"])
    d["GDPShare_pct_model"] = 100.0 * d["VA_sports_model"] / d["GDP"]
    d["PerCapitaVA_model"] = d["VA_sports_model"] / d["Population"]
    return d


def simulate_fiscal_effect(df: pd.DataFrame, tau: float, mg: float, lam: float, alpha: float | None = None) -> pd.DataFrame:
    d = df.copy()

    if alpha is not None:
        d["DirectVA"] = alpha * d["GGR_sports"]
    else:
        d["DirectVA"] = d["VA_sports_model"]

    d["TaxRevenue"] = tau * d["GGR_sports"]
    d["FiscalDeltaGDP"] = (mg - 1.0) * d["TaxRevenue"]
    d["NetDeltaGDP"] = (1.0 - lam) * (d["DirectVA"] + d["FiscalDeltaGDP"])
    d["NetDeltaGDP_per_capita"] = d["NetDeltaGDP"] / d["Population"]
    return d


def plot_net_gdp(df: pd.DataFrame, title: str = "Net GDP Impact of Sports Betting") -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(df["Country"], df["NetDeltaGDP"] / 1e9)
    plt.ylabel("Net ΔGDP (billions)")
    plt.title(title)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Replace this with your real CSV later
    sample = pd.DataFrame({
        "Country": ["US", "UK"],
        "VA_gambling": [1.15e11, 1.85e10],
        "GGR_gambling_total": [1.72e11, 1.55e10],
        "GGR_sports": [1.35e10, 3.20e9],
        "GDP": [2.79e13, 3.34e12],
        "Population": [3.35e8, 6.77e7],
    })

    sample = compute_va_sports(sample)

    us = simulate_fiscal_effect(sample[sample["Country"] == "US"], tau=0.20, mg=1.2, lam=0.6)
    uk = simulate_fiscal_effect(sample[sample["Country"] == "UK"], tau=0.15, mg=1.2, lam=0.6)

    result = pd.concat([us, uk], ignore_index=True)
    print(result[["Country", "VA_sports_model", "TaxRevenue", "NetDeltaGDP", "NetDeltaGDP_per_capita"]])

    plot_net_gdp(result)
