import sqlite3
import sys
print(sys.path)
from pipeline.extract import extract_csv, extract_json, extract_api
#from pipeline.transform import run_transformations

import os

def create_or_replace_database(db_path):
    """
    Creates or replaces the SQLite database.

    Parameters:
    db_path (str): The path to the SQLite database file.

    Returns:
    sqlite3.Connection: A connection object to the newly created database.
    """
    # Check if the database file already exists
    if os.path.exists(db_path):
        print(f"⚠️ Database file '{db_path}' already exists. Deleting it...")
        os.remove(db_path)
        print(f"✅ Existing database file '{db_path}' has been deleted.")

    # Create a new database file
    conn = sqlite3.connect(db_path)
    print(f"✅ New database created at '{db_path}'.")
    return conn

def run_transformations(db_conn, script_path):
    """Reads a local SQL file and executes it sequentially against the database."""
    if not os.path.exists(script_path):
        print(f"❌ SQL file not found at: {script_path}")
        return
        
    with open(script_path, 'r') as f:
        sql_script = f.read()
        
    cursor = db_conn.cursor()
    try:
        # executescript allows running multiple SQL commands separated by semicolons
        cursor.executescript(sql_script)
        db_conn.commit()
        print("🚀 Successfully ran SQL staging transformations.")
    except Exception as e:
        db_conn.rollback()
        print(f"❌ SQL Execution Error: {e}")
def main():
    print("--- Starting Practice Master Data Pipeline ---")
    
    # Target central data database (Acts as your local data warehouse)
    # Define the database file path
    db_file = "database.db"

    # Create or replace the database
    conn = create_or_replace_database(db_file)
    
    try:
        # Phase 1: Extract and Load Raw Data
        print("\n[Phase 1: Extraction]")
        extract_csv("data_sources/partners.csv", conn)
        extract_json("data_sources/logs.json", conn)
        
        # Free public API example for practice
        sample_api = "https://jsonplaceholder.typicode.com/posts"
        extract_api(sample_api, conn)
        
        # Phase 2: Native SQL Transformation and Staging
        print("\n[Phase 2: Transformation]")
        run_transformations(conn, "scripts/01_stage_vault.sql")
        
        print("\n🎉 Pipeline Execution Completed Successfully!")
        
    except Exception as e:
        print(f"\n💥 Pipeline failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()