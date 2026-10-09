import pandas as pd


def detect_correlations(df, indicators, threshold=0.70):
    """Calculate Pearson correlations and flag strong relationships."""

    correlation_matrix = df[indicators].corr(
        method="pearson"
    )

    flagged_pairs = []

    for i in range(len(indicators)):
        for j in range(i + 1, len(indicators)):
            indicator_a = indicators[i]
            indicator_b = indicators[j]

            correlation = correlation_matrix.loc[
                indicator_a,
                indicator_b
            ]

            if (
                pd.notna(correlation)
                and abs(correlation) >= threshold
            ):
                flagged_pairs.append({
                    "indicator_1": indicator_a,
                    "indicator_2": indicator_b,
                    "correlation": correlation,
                })

    return correlation_matrix, pd.DataFrame(flagged_pairs)