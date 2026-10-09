import pandas as pd


def generate_insights(
    trends,
    outliers,
    correlations,
    trend_threshold=10,
):
    """Generate structured insights from analytical results."""

    insights = []
    insight_id = 1

    # Trend insights
    for _, row in trends.iterrows():
        change = row["change_pct"]

        if abs(change) >= 2 * trend_threshold:
            severity = "High"
        else:
            severity = "Medium"

        direction = (
            "increased"
            if change > 0
            else "decreased"
        )

        explanation = (
            f"{row['indicator']} in {row['district']} "
            f"{direction} by {abs(change):.2f}% "
            "compared with the previous observation."
        )

        insights.append({
            "insight_id": f"INS-{insight_id:04d}",
            "type": "trend",
            "district": row["district"],
            "indicator": row["indicator"],
            "period": row["month"],
            "metric": row["value"],
            "change_pct": change,
            "severity": severity,
            "explanation": explanation,
        })

        insight_id += 1

    # Outlier insights
    for _, row in outliers.iterrows():
        explanation = (
            f"{row['indicator']} in {row['district']} "
            f"has an unusual value of {row['value']}, "
            "outside the calculated IQR boundaries."
        )

        insights.append({
            "insight_id": f"INS-{insight_id:04d}",
            "type": "outlier",
            "district": row["district"],
            "indicator": row["indicator"],
            "period": row["month"],
            "metric": row["value"],
            "change_pct": None,
            "severity": "High",
            "explanation": explanation,
        })

        insight_id += 1

    # Correlation insights
    for _, row in correlations.iterrows():
        correlation = row["correlation"]

        explanation = (
            f"{row['indicator_1']} and {row['indicator_2']} "
            f"have a Pearson correlation of {correlation:.2f}. "
            "Interpret this relationship cautiously."
        )

        insights.append({
            "insight_id": f"INS-{insight_id:04d}",
            "type": "correlation",
            "district": "All districts",
            "indicator": (
                f"{row['indicator_1']} and "
                f"{row['indicator_2']}"
            ),
            "period": "All periods",
            "metric": correlation,
            "change_pct": None,
            "severity": (
                "High"
                if abs(correlation) >= 0.85
                else "Medium"
            ),
            "explanation": explanation,
        })

        insight_id += 1

    columns = [
        "insight_id",
        "type",
        "district",
        "indicator",
        "period",
        "metric",
        "change_pct",
        "severity",
        "explanation",
    ]

    return pd.DataFrame(insights, columns=columns)