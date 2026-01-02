import sys
import os
import json
import re
from pathlib import Path

# Setup project paths
from src.utils.path_config import setup_python_path
setup_python_path()

from src.Rewrite_Middleware.middleware import DBMS
from src.utils.data_distribution import DATABASE_STATISTICS

def collect_database_statistics(dbms_instance=None):
    """
    Collect statistics from the database
    
    Args:
        dbms_instance: DBMS instance, if None, a new instance will be created

    Returns:
        tuple: (db_name, statistics_list)
    """
    if dbms_instance is None:
        dbms_instance = DBMS()
    
    print("="*60)
    print("🗄️  Starting Database Statistics Collection")
    print("="*60)
    print(f"🔗 Database: {dbms_instance.db_name}")
    
    dbms_instance.connect()
    result = []
    
    try:
        print("📊 Getting list of tables in public schema...")
        table_names_sql = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """
        dbms_instance.cursor.execute(table_names_sql)
        tables = dbms_instance.cursor.fetchall()
        
        print(f"✅ Found {len(tables)} tables. Starting table scan...")
        print("-" * 60)
        
        for i, table_row in enumerate(tables):
            table_name = table_row['table_name'] if isinstance(table_row, dict) else table_row[0]
            print(f"[{i+1:2d}/{len(tables)}] Scanning '{table_name}'...", end=" ")
            
            try:
                count_sql = f"SELECT COUNT(*) FROM {table_name}"
                dbms_instance.cursor.execute(count_sql)
                count_result = dbms_instance.cursor.fetchone()
                row_count = count_result['count'] if isinstance(count_result, dict) else count_result[0]
                
                result.append([table_name, str(row_count)])
                print(f"✅ {row_count:,} rows")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                result.append([table_name, "0"])
        
        print("-" * 60)
        print(f"✅ Statistics collection completed for {len(result)} tables")

        # Show summary information
        total_rows = sum(int(count) for _, count in result)
        print(f"📊 Total rows across all tables: {total_rows:,}")
        
        return dbms_instance.db_name, result
        
    except Exception as e:
        print(f"❌ Error during collection: {e}")
        return dbms_instance.db_name, []
    finally:
        dbms_instance.close()


def update_data_distribution_file(db_name, statistics):
    """
    Update data_distribution.py file

    Args:
        db_name: Database name
        statistics: List of statistics data
    """
    try:        
        print(f"📁 Updating DATABASE_STATISTICS for: {db_name}")

        # Step 1: Update the dictionary
        DATABASE_STATISTICS[db_name] = statistics
        print(f"✅ Updated in-memory DATABASE_STATISTICS for '{db_name}'")

        # Step 2: Get the path to the data_distribution.py file
        distribution_file = Path(__file__).parent / "data_distribution.py"

        # Step 3: Read the existing file content
        with open(distribution_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Step 4: Generate new dictionary content
        dict_content = "{\n"
        for key, value in DATABASE_STATISTICS.items():
            # Format statistics data
            formatted_stats = json.dumps(value, ensure_ascii=False)
            dict_content += f'    "{key}": {formatted_stats},\n    \n'
        dict_content = dict_content.rstrip(',\n    \n') + '\n}'

        # Step 5: Replace DATABASE_STATISTICS dictionary content
        pattern = r'DATABASE_STATISTICS = \{[^}]*\}'
        replacement = f'DATABASE_STATISTICS = {dict_content}'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # Step 6: Write back to the file
        with open(distribution_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Successfully updated {distribution_file}")
        print(f"📋 Database '{db_name}' now has {len(statistics)} tables")
        return True
        
    except Exception as e:
        print(f"❌ Error updating distribution file: {e}")
        return False


def get_data_statistics():
    """
    Main function: Collect database statistics and update distribution file

    Returns:
        str: JSON formatted statistics
    """
    # Collect statistics from the database
    db_name, statistics = collect_database_statistics()
    
    if not statistics:
        print("⚠️  No statistics collected")
        return "[]"
    
    # Update the data_distribution.py file with collected statistics
    success = update_data_distribution_file(db_name, statistics)
    
    if success:
        print("="*60)
        print("🎉 Statistics Collection and Update Complete!")
        print("="*60)
        print(f"Database: {db_name}")
        print(f"📊 Tables: {len(statistics)}")
        print(f"📄 Updated format:")
        print(f"    \"{db_name}\": {json.dumps(statistics)}")
        print("="*60)

    # Return JSON formatted statistics
    return json.dumps(statistics)


if __name__ == "__main__":
    data_statistics = get_data_statistics()
    print(f"\n🎯 Final JSON Output:")
    print(data_statistics)


