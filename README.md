# InsightX AI

### Automated Healthcare Analytics & Insight Generation Engine

InsightX AI is a Python-based analytical application that
identifies significant trends, statistical outliers, and
correlations in healthcare datasets.

## Features

- CSV data ingestion
- Schema validation and data-quality reporting
- Configurable trend detection
- IQR-based outlier detection
- Pearson correlation analysis
- Structured automated insight generation
- Severity classification
- Interactive Streamlit dashboard
- District and month filters
- Interactive Plotly charts
- CSV exports

## Technology Stack

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- SciPy

## Project Structure

- `app.py`: Dashboard
- `analytics/data_loader.py`: Data ingestion
- `analytics/trend_detector.py`: Trend analysis
- `analytics/outlier_detector.py`: Outlier detection
- `analytics/correlation_analyzer.py`: Correlation analysis
- `services/insight_engine.py`: Insight generation
- `data/healthcare_data.csv`: Sample dataset

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd InsightX-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Statistical Methods

### Trend Detection

Compares consecutive monthly observations and flags
percentage changes that exceed a configurable threshold.

### Outlier Detection

Uses the Interquartile Range method to flag unusually
low or high observations.

### Correlation Analysis

Calculates Pearson correlation coefficients and flags
indicator pairs meeting a configurable threshold.

### Automated Insights

Converts analytical results into structured records
containing a unique ID, metric, severity, and explanation.

## Limitations

The included sample dataset contains only two months
of observations for six districts.

Correlation estimates may be unstable with this limited
sample size and should not be interpreted as evidence
of causation.

The severity rules are illustrative and are not clinically
validated healthcare risk thresholds.

## Future Improvements

- Automated unit testing
- More extensive data-quality validation
- Configurable rules for each indicator
- Historical trend analysis
- Additional statistical anomaly detection methods
- API integration
- Automated deployment