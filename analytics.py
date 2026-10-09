import pandas as pd
import numpy as np


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
    """Load and normalize healthcare data from a CSV file."""

    df = pd.read_csv(file)

    # Validate the required schema.
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Normalize dates.
    df["month"] = pd.to_datetime(
        df["month"],
        errors="coerce"
    )

    # Normalize numerical indicators.
    for column in INDICATORS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Normalize district names.
    df["district"] = df["district"].astype("string").str.strip()

    # Identify duplicate district-month records.
    duplicate_mask = df.duplicated(
        subset=["district", "month"],
        keep=False
    )

    duplicate_count = int(duplicate_mask.sum())

    # Collect data-quality information.
    quality_report = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_records": duplicate_count,
        "invalid_months": int(df["month"].isna().sum()),
        "invalid_districts": int(
            (df["district"].isna() | df["district"].eq("")).sum()
        ),
    }

    # Invalid values are reported, not silently deleted.
    return df, quality_report