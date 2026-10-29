# OpenPowerlifting to ClickHouse

A Python pipeline that loads the [OpenPowerlifting](https://www.openpowerlifting.org/data.html) dataset, validates it, and stores it in ClickHouse for fast analytics.

## Features

- Reads `.csv` or `.zip` files with pandas
- Previews data: shape, types, missing values, summaries
- Custom `validate()` step: removes duplicates, nulls, out-of-range values, DQ entries and inconsistent totals
- Saves to a ClickHouse `MergeTree` table (partitioned by year)

## Requirements

- Python 3.10+
- ClickHouse server
- `pandas`, `clickhouse-connect`

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install pandas clickhouse-connect
```

## Usage

```bash
python data.py openpowerlifting.zip --rows 10
python data.py openpowerlifting.zip --sample 100000   # quick test
```

## Table Schema

```sql
CREATE TABLE powerlifting (
  Name String, Sex LowCardinality(String), Event LowCardinality(String),
  Equipment LowCardinality(String), Federation LowCardinality(String),
  Country LowCardinality(String), Age Float32, BodyweightKg Float32,
  Best3SquatKg Float32, Best3BenchKg Float32, Best3DeadliftKg Float32,
  TotalKg Float32, Dots Float32, Date Date
) ENGINE = MergeTree
PARTITION BY toYear(Date)
ORDER BY (Federation, Sex, Event, Date, Name);
```

## Query Example

```sql
SELECT Name, TotalKg FROM powerlifting ORDER BY TotalKg DESC LIMIT 10;
```

## Project Structure

```
.
├── data.py      # load, show, validate, save
└── README.md
```

## Data Source

OpenPowerlifting data is public domain. See their website for terms.
