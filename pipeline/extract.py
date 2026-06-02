import pandas as pd
import os
import sqlite3
import requests

def extract_csv(file_path, conn, table_name='src_csv_partners'):
    """
    Extracts data from a CSV file and loads it into a SQLite database.

    Parameters:
    file_path (str): The path to the CSV file.
    conn (sqlite3.Connection): The SQLite database connection.
    table_name (str): The name of the table to insert data into. Default is 'src_csv_partners'.

    Returns:
    None
    """
    try:
        # Validate file path
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Load the DataFrame into the SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully loaded into table '{table_name}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def extract_json(file_path, conn, table_name='src_json_logs'):
    """
    Extracts data from a JSON file and loads it into a SQLite database.

    Parameters:
    file_path (str): The path to the JSON file.
    conn (sqlite3.Connection): The SQLite database connection.
    table_name (str): The name of the table to insert data into. Default is 'src_json_logs'.

    Returns:
    None
    """
    try:
        # Validate file path
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        # Read the JSON file into a DataFrame
        df = pd.read_json(file_path)

        # Load the DataFrame into the SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully loaded into table '{table_name}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: Invalid JSON format. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def extract_external_sqlite(source_db_path, conn, table_prefix='src_sqlite_'):
    """
    Extracts data from an external SQLite database and loads it into another SQLite database.

    Parameters:
    source_db_path (str): The path to the source SQLite database.
    conn (sqlite3.Connection): The SQLite database connection to load data into.
    table_prefix (str): The prefix for the table names in the target database. Default is 'src_sqlite_'.

    Returns:
    None
    """
    try:
        # Validate source database path
        if not os.path.isfile(source_db_path):
            raise FileNotFoundError(f"The source database '{source_db_path}' does not exist.")

        # Connect to the source SQLite database
        source_conn = sqlite3.connect(source_db_path)
        cursor = source_conn.cursor()

        # Get the list of tables in the source database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Extract data from each table and load it into the target database
        for table in tables:
            table_name = table[0]
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", source_conn)
            df.to_sql(f"{table_prefix}{table_name}", conn, if_exists='replace', index=False)
            print(f"Data from table '{table_name}' successfully loaded into '{table_prefix}{table_name}'.")

        # Close the source connection
        source_conn.close()

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


import requests
import pandas as pd

def extract_api(api_url, conn, table_name='src_api_data'):
    """
    Extracts data from an API endpoint and loads it into a SQLite database.

    Parameters:
    api_url (str): The URL of the API endpoint.
    conn (sqlite3.Connection): The SQLite database connection.
    table_name (str): The name of the table to insert data into. Default is 'src_api_data'.

    Returns:
    None
    """
    try:
        # Validate API URL
        if not api_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid API URL. Ensure it starts with 'http://' or 'https://'.")

        # Make the API request
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the JSON response
        try:
            data = response.json()
        except ValueError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

        # Normalize nested JSON objects if necessary
        df = pd.json_normalize(data)

        # Validate if the DataFrame is empty
        if df.empty:
            raise ValueError("The API response contains no data to load.")

        # Load the DataFrame into the SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ Data successfully extracted from API and loaded into table '{table_name}'.")

    except requests.exceptions.Timeout:
        print("❌ API request timed out. Please check the API endpoint or your network connection.")
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
    except ValueError as e:
        print(f"❌ Data processing error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")