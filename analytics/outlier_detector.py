import pandas as pd


def detect_outliers(df, indicators):
    """Detect outliers using the IQR method."""

    results = []

    for indicator in indicators:
        values = df[indicator].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            (df[indicator] < lower_bound)
            | (df[indicator] > upper_bound)
        )

        for _, row in df.loc[mask].iterrows():
            results.append({
                "type": "outlier",
                "district": row["district"],
                "indicator": indicator,
                "month": row["month"],
                "value": row[indicator],
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
            })

    return pd.DataFrame(results)