import pandas as pd


def generate_insights(
    df,
    trends,
    outliers,
    correlations,
    trend_threshold=10,
):
    """
    Generate structured, data-driven insights from analytics results.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset used to calculate reference statistics.
    trends : pandas.DataFrame
        Results from trend detection.
    outliers : pandas.DataFrame
        Results from IQR-based outlier detection.
    correlations : pandas.DataFrame
        Strong correlation pairs.
    trend_threshold : float
        Configurable percentage-change threshold.

    Returns
    -------
    pandas.DataFrame
        Structured insights with severity and explanations.
    """

    insights = []
    insight_id = 1

    # --------------------------------------------------
    # 1. TREND INSIGHTS
    # --------------------------------------------------

    for _, row in trends.iterrows():

        change = float(row["change_pct"])
        threshold = float(trend_threshold)

        # Severity is derived from the configured threshold.
        if abs(change) >= 2 * threshold:
            severity = "High"
        elif abs(change) >= threshold:
            severity = "Medium"
        else:
            severity = "Low"

        direction = (
            "increased"
            if change > 0
            else "dropped"
        )

        indicator_name = (
            str(row["indicator"])
            .replace("_", " ")
            .title()
        )

        period = pd.to_datetime(row["month"]).strftime("%Y-%m")

        current_value = float(row["value"])
        previous_value = float(row["prev_value"])

        explanation = (
            f"{indicator_name} in {row['district']} "
            f"{direction} by {abs(change):.1f}% compared "
            f"to the previous month. The value changed "
            f"from {previous_value:g} to {current_value:g}, "
            f"exceeding the {threshold:g}% "
            f"significant-change threshold."
        )

        insights.append({
            "insight_id": f"INS-{insight_id:04d}",
            "type": "trend",
            "district": row["district"],
            "indicator": row["indicator"],
            "period": period,
            "metric": current_value,
            "previous_value": previous_value,
            "change_pct": round(change, 2),
            "severity": severity,
            "explanation": explanation,
        })

        insight_id += 1

    # --------------------------------------------------
    # 2. OUTLIER INSIGHTS
    # --------------------------------------------------

    for _, row in outliers.iterrows():

        indicator = row["indicator"]
        value = float(row["value"])

        # Calculate the mean dynamically from the supplied dataset.
        reference_values = df[indicator].dropna()

        if reference_values.empty:
            continue

        reference_mean = float(reference_values.mean())

        deviation = value - reference_mean

        # Calculate how far the value lies outside its IQR boundary.
        lower_bound = float(row["lower_bound"])
        upper_bound = float(row["upper_bound"])

        if value < lower_bound:
            boundary_distance = lower_bound - value
            boundary = lower_bound
        else:
            boundary_distance = value - upper_bound
            boundary = upper_bound

        # Relative deviation avoids relying on a fixed numeric cutoff.
        iqr = upper_bound - lower_bound
        relative_distance = (
            boundary_distance / iqr
            if iqr > 0
            else 0
        )

        if relative_distance >= 0.25:
            severity = "High"
        else:
            severity = "Medium"

        indicator_name = (
            str(indicator)
            .replace("_", " ")
            .title()
        )

        period = (
            pd.to_datetime(row["month"]).strftime("%Y-%m")
            if pd.notna(row["month"])
            else "Unknown"
        )

        comparison = (
            "below"
            if deviation < 0
            else "above"
        )

        explanation = (
            f"{row['district']}'s {indicator_name} of "
            f"{value:g} is {abs(deviation):.2f} "
            f"{comparison} the dataset mean "
            f"({reference_mean:.2f}). The value is outside "
            f"the IQR boundaries "
            f"({lower_bound:.2f} to {upper_bound:.2f}), "
            f"flagging it for review."
        )

        insights.append({
            "insight_id": f"INS-{insight_id:04d}",
            "type": "outlier",
            "district": row["district"],
            "indicator": indicator,
            "period": period,
            "metric": value,
            "reference_mean": round(reference_mean, 2),
            "deviation_from_mean": round(deviation, 2),
            "boundary": round(boundary, 2),
            "boundary_distance": round(boundary_distance, 2),
            "change_pct": None,
            "severity": severity,
            "explanation": explanation,
        })

        insight_id += 1

    # --------------------------------------------------
    # 3. CORRELATION INSIGHTS
    # --------------------------------------------------

    for _, row in correlations.iterrows():

        correlation = float(row["correlation"])

        # Severity represents association strength, not healthcare risk.
        if abs(correlation) >= 0.85:
            severity = "High"
        else:
            severity = "Medium"

        indicator_a = (
            str(row["indicator_1"])
            .replace("_", " ")
            .title()
        )

        indicator_b = (
            str(row["indicator_2"])
            .replace("_", " ")
            .title()
        )

        if correlation > 0:
            relationship = "positive"
        else:
            relationship = "negative"

        explanation = (
            f"{indicator_a} and {indicator_b} show a "
            f"{relationship} Pearson correlation of "
            f"{correlation:.2f}. This describes an observed "
            f"linear association, not causation. Interpret "
            f"cautiously because the dataset is small."
        )

        insights.append({
            "insight_id": f"INS-{insight_id:04d}",
            "type": "correlation",
            "district": "All districts",
            "indicator": f"{row['indicator_1']} and {row['indicator_2']}",
            "period": "All periods",
            "metric": round(correlation, 4),
            "previous_value": None,
            "change_pct": None,
            "severity": severity,
            "explanation": explanation,
        })

        insight_id += 1

    # --------------------------------------------------
    # 4. RETURN CONSISTENT STRUCTURED OUTPUT
    # --------------------------------------------------

    columns = [
        "insight_id",
        "type",
        "district",
        "indicator",
        "period",
        "metric",
        "previous_value",
        "change_pct",
        "reference_mean",
        "deviation_from_mean",
        "boundary",
        "boundary_distance",
        "severity",
        "explanation",
    ]

    return pd.DataFrame(insights).reindex(columns=columns)