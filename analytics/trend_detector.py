import pandas as pd


def detect_trends(df, indicators, threshold=10):
    """Detect significant changes between consecutive observations."""

    results = []

    for district, group in df.groupby("district"):
        group = group.sort_values("month")

        for indicator in indicators:
            previous = group[indicator].shift(1)
            current = group[indicator]

            valid = (
                previous.notna()
                & (previous != 0)
                & current.notna()
                & group["month"].notna()
            )

            change_pct = (
                (current - previous) / previous
            ) * 100

            flagged = (
                valid
                & (change_pct.abs() >= threshold)
            )

            for idx in group.index[flagged]:
                results.append({
                    "type": "trend",
                    "district": district,
                    "indicator": indicator,
                    "month": group.loc[idx, "month"],
                    "value": current.loc[idx],
                    "prev_value": previous.loc[idx],
                    "change_pct": change_pct.loc[idx],
                })

    return pd.DataFrame(results)