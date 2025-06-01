import sys
import os
import json
from tools import DBMS

def get_data_statistics():
    print("Starting database statistics collection...")
    db = DBMS()
    print(f"This is the database {db.db_name}")
    db.connect()  
    result = []
    
    try:
        print("Getting list of tables in public schema...")
        table_names_sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';" 
        db.cursor.execute(table_names_sql)
        tables = db.cursor.fetchall()
        
        print(f"Found {len(tables)} tables. Starting table scan...")
        for i, table_row in enumerate(tables):
            table_name = table_row['table_name'] if isinstance(table_row, dict) else table_row[0]
            print(f"[{i+1}/{len(tables)}] Scanning table '{table_name}'...")
            
            count_sql = f"SELECT COUNT(*) FROM {table_name}"
            db.cursor.execute(count_sql)
            count_result = db.cursor.fetchone()
            row_count = count_result['count'] if isinstance(count_result, dict) else count_result[0]
            result.append([table_name, str(row_count)])

            print(f"   ✓ Table '{table_name}' has {row_count} rows")
        
        print("All tables scanned successfully.")
        json_string = json.dumps(result)
        print(f"Data statistics collected for {len(result)} tables.")
        return json_string
        
    except Exception as e:
        print(f"Error executing statement: {e}")
        return "[]"  
    finally:
        db.close() 

if __name__ == "__main__":
    data_statistics = get_data_statistics()
    print(data_statistics)