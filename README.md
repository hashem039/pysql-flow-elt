# PySQL-Flow: Modular ELT Pipeline

PySQL-Flow is a native Python and SQL modular ELT (Extract, Load, Transform) framework designed to unify heterogeneous data sources into a centralized SQLite data warehouse. It prioritizes decoupled logic, idempotency, and resilient data processing.

## 🚀 Key Features

*   **Modular Architecture:** Decoupled extraction and transformation layers for independent scaling and maintenance.
*   **Multi-Source Ingestion:** Seamlessly unifies structured CSVs, semi-structured JSON logs, and REST API payloads.
*   **Standardized ELT Pattern:** Implements a strict Extract-Load-Transform workflow to maintain full data lineage.
*   **Native SQL Transformations:** Leverages robust SQL scripts for data cleansing, normalization, and staging.
*   **Resilient Design:** Built-in validation and error handling for file paths, API connectivity, and SQL execution.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **Data Manipulation:** Pandas
*   **Database:** SQLite
*   **API Ingestion:** Requests
*   **Orchestration:** Modular Python scripts

## 📁 Project Structure

```text
├── data_sources/           # Raw CSV and JSON data files
├── pipeline/
│   ├── extract.py          # Extraction logic for CSV, JSON, and APIs
│   └── transform.py        # SQL execution engine
├── scripts/
│   └── 01_stage_vault.sql  # Native SQL transformation routines
├── main.py                 # Pipeline entry point and orchestrator
└── requirements.txt        # Project dependencies
```

## ⚙️ Getting Started

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Pipeline:**
    ```bash
    python main.py
    ```

## 🔄 Workflow

1.  **Extraction:** Data is pulled from local files (CSV, JSON) and remote REST APIs.
2.  **Loading:** Raw data is loaded into `src_` prefix tables in the SQLite database, ensuring a "clean slate" on every run.
3.  **Transformation:** Native SQL scripts are executed to normalize data, handle nulls, and prepare the data for downstream analysis.

---
*Developed with a focus on clean code and data integrity.*
