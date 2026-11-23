# Finance Performance — Automated ETL & Financial Analytics

**End-to-End Data Engineering Project | Python • Pandas • PostgreSQL • Docker • pgAdmin 4 • Metabase**

## Project Overview

Finance Performance is an end-to-end Data Engineering and Business Intelligence project designed to transform raw retail transactions into actionable financial insights.

The project demonstrates how to build an ETL pipeline, clean and validate transactional data, store structured information in PostgreSQL, perform SQL analysis, and create an interactive financial dashboard using Metabase.

The project is designed to run locally using Docker Compose and Python.

## Business Problem

Retail companies generate large volumes of transactional data. Without a structured analytics pipeline, it can be difficult to monitor sales performance, identify top-selling products, understand customer behavior, and analyze geographic trends.

This project addresses these challenges by creating a reproducible data processing and analytics workflow.

## Project Objectives

- Extract transactional data from Excel files.
- Clean and transform raw data using Python and pandas.
- Identify sales, cancellations and missing values.
- Load processed data into PostgreSQL.
- Analyze business KPIs using SQL.
- Visualize financial performance using Metabase.
- Validate transformation logic using automated tests.
- Document the architecture and deployment process.

## Dataset

**Source:** UCI Machine Learning Repository — Online Retail II

**Dataset URL:** https://archive.ics.uci.edu/dataset/502/online+retail+ii

**Format:** Microsoft Excel (.xlsx)

**Records:** Approximately 1.07 million transactions.

**Period:** December 2009 – December 2011.

The dataset contains retail transactions from a UK-based online retailer.

Main fields include:

| Field | Description |
|---|---|
| Invoice | Invoice number |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of items |
| InvoiceDate | Transaction date |
| Price | Unit price in GBP |
| Customer ID | Customer identifier |
| Country | Customer country |

The dataset is publicly available under the CC BY 4.0 license.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | ETL pipeline development |
| pandas | Data cleaning and transformation |
| PostgreSQL | Relational data storage |
| Docker Compose | Container orchestration |
| pgAdmin 4 | Database administration |
| SQL | Financial analytics |
| Metabase Open Source | Business Intelligence dashboard |
| pytest | Automated testing |
| VS Code | Development environment |
| Git & GitHub | Version control and portfolio |

## Data Pipeline Architecture

```text
UCI Online Retail II Dataset
            |
            v
      Excel Extraction
            |
            v
   Python + pandas ETL
            |
            v
 Data Cleaning & Validation
            |
            v
     PostgreSQL Database
            |
       +----+----+
       |         |
       v         v
    pgAdmin   Metabase
       |         |
       v         v
 SQL Analysis  BI Dashboard
```

## ETL Process

### 1. Extract

The pipeline reads both worksheets from the Online Retail II Excel file.

### 2. Transform

The transformation stage includes:

- Standardizing column names.
- Converting dates and numerical fields.
- Handling missing values.
- Identifying cancelled transactions.
- Identifying valid positive sales.
- Calculating gross sales amounts.
- Preparing monthly reporting dimensions.

### 3. Load

The cleaned dataset is loaded into the `finance.transactions` table in PostgreSQL using a staging-table approach.

The pipeline is designed for full refreshes rather than incremental loading.

## Key Financial KPIs

The project analyzes:

1. Gross sales revenue.
2. Number of sales invoices.
3. Average order value.
4. Monthly sales trends.
5. Top countries by revenue.
6. Top products by revenue.
7. Number of cancelled invoices.
8. Number of identified customers.
9. Data quality indicators.

**Important:** Gross sales are calculated from positive sales transactions. Cancellations are monitored separately. The dataset does not include product costs, so actual profit margins cannot be calculated.

## Project Structure

```text
finance_performance/
├── data/
│   ├── raw/
│   └── processed/
├── etl/
│   ├── __init__.py
│   └── pipeline.py
├── sql/
│   └── analyses.sql
├── tests/
│   └── test_pipeline.py
├── dashboards/
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Docker Desktop
- Python 3
- Git
- VS Code
- pgAdmin 4 (optional local client)

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/finance_performance.git
cd finance_performance
```

Replace `YOUR_USERNAME` with your GitHub username.

### Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder password with a strong local password.

### Start Docker services

```bash
docker compose up -d
docker compose ps
```

### Install Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Download the dataset

Download Online Retail II from UCI and place the extracted Excel file at:

```text
data/raw/online_retail_II.xlsx
```

### Run the ETL pipeline

```bash
python -m etl.pipeline
```

### Run automated tests

```bash
python -m pytest -v
```

## PostgreSQL Connection

For pgAdmin 4 running locally:

| Parameter | Value |
|---|---|
| Host | 127.0.0.1 |
| Port | 55432 |
| Database | finance_db |
| Username | finance_admin |
| Password | Value configured in `.env` |

## Metabase Dashboard

Open:

http://localhost:3001

Metabase uses the Docker service name `postgres` as its database host, with port `5432`.

The financial dashboard is designed to include:

- KPI summary cards.
- Monthly sales trends.
- Revenue by country.
- Top-performing products.
- Cancellation monitoring.
- Interactive date, country and product filters.

## SQL Analysis Example

```sql
SELECT
    invoice_month,
    ROUND(SUM(revenue)::numeric, 2) AS gross_sales
FROM finance.transactions
WHERE is_sale = TRUE
GROUP BY invoice_month
ORDER BY invoice_month;
```

## Testing and Data Quality

Automated unit tests verify:

- Positive sales identification.
- Cancellation classification.
- Revenue calculations.
- Preservation of expected records.

Additional SQL queries help validate the loaded data.


## Future Improvements

- Incremental ETL processing.
- Automated scheduling.
- Improved data quality reporting.
- Database constraints and monitoring.
- Dedicated PostgreSQL database for Metabase metadata.
- CI/CD with GitHub Actions.
- Cloud deployment.

## Skills Demonstrated

**Data Engineering:** ETL, data transformation, data validation, relational databases, Docker.

**Data Analytics:** SQL aggregation, financial KPIs, sales analysis, data visualization.

**Software Engineering:** Python project organization, automated tests, Git and technical documentation.

## Data Attribution

Online Retail II — UCI Machine Learning Repository.

License: Creative Commons Attribution 4.0 International (CC BY 4.0).

Dataset: https://archive.ics.uci.edu/dataset/502/online+retail+ii

## Author

Data Analytics & Data Engineering Portfolio

*Python | SQL | PostgreSQL | Docker | Business Intelligence*# finance_performance-
