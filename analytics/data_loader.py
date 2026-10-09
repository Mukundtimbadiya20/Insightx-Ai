import pandas as pd


REQUIRED_COLUMNS = [
    "month",
    "district",
    "anc_coverage",
    "institutional_delivery",
    "immunization",
    "high_risk_cases",
]

INDICATORS = [
    "anc_coverage",
    "institutional_delivery",
    "immunization",
    "high_risk_cases",
]


def load_data(file):
    """Load and validate healthcare data."""

    df = pd.read_csv(file)

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df["month"] = pd.to_datetime(
        df["month"],
        errors="coerce"
    )

    df["district"] = (
        df["district"]
        .astype("string")
        .str.strip()
    )

    for column in INDICATORS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Detect duplicate district-month combinations.
    duplicate_mask = df.duplicated(
        subset=["district", "month"],
        keep=False
    )

    # Identify impossible coverage percentages.
    coverage_columns = [
        "anc_coverage",
        "institutional_delivery",
        "immunization",
    ]

    invalid_coverage = (
        (df[coverage_columns] < 0)
        | (df[coverage_columns] > 100)
    ).any(axis=1)

    # High-risk counts cannot be negative.
    invalid_high_risk = df["high_risk_cases"] < 0

    quality_report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_records": int(duplicate_mask.sum()),
        "invalid_months": int(df["month"].isna().sum()),
        "invalid_coverage_records": int(invalid_coverage.sum()),
        "invalid_high_risk_records": int(invalid_high_risk.sum()),
        "invalid_districts": int(
            (
                df["district"].isna()
                | df["district"].eq("")
            ).sum()
        ),
    }

    return df, quality_report