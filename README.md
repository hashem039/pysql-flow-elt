# Practice Master Data Pipeline

A modular data pipeline designed to extract data from various sources, load it into a central SQLite database, and perform transformations using native SQL scripts.

## Project Structure

```text
/practise_master_pipeline/
├── main.py                 # Entry point of the pipeline
├── pipeline/
│   ├── extract.py          # Extraction logic (CSV, JSON, API)
│   └── tranform.py         # Transformation execution logic
├── scripts/
│   └── 01_stage_vault.sql  # SQL transformation script
├── data_sources/
│   ├── partners.csv        # Sample partner data
│   └── logs.json           # Sample log data
├── requirements.txt        # Python dependencies
└── database.db             # SQLite database (generated at runtime)
```

## Features

- **Multi-source Extraction**: Seamlessly handles data from CSV files, JSON files, and REST APIs.
- **SQLite Integration**: Uses SQLite as a local data warehouse for staging and processing.
- **SQL-based Transformations**: Executes native SQL scripts for cleaning and hashing, keeping data logic separate from application code.
- **Automated Workflow**: Orchestrates the entire ETL process from raw data to staged tables.

## Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Installation

1. Clone the repository or download the project files.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Pipeline

Execute the main script to start the pipeline:

```bash
python main.py
```

## Workflow Overview

1. **Phase 1: Extraction**
   - Extracts partner data from `data_sources/partners.csv`.
   - Extracts log data from `data_sources/logs.json`.
   - Fetches sample post data from an external API (JSONPlaceholder).
   - Loads all raw data into `src_` prefixed tables.

2. **Phase 2: Transformation**
   - Runs `scripts/01_stage_vault.sql`.
   - Cleans the raw data (trimming, case normalization).
   - Generates unique hashes for records.
   - Loads the processed data into staging tables like `STG_PARTNERS`.

## Dependencies

- `pandas`: For data manipulation and loading to SQLite.
- `requests`: For API data extraction.
- `sqlite3`: Standard library for database interaction.
