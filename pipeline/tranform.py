import os

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