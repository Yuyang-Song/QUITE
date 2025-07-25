import json

# Database statistics storage
# Format: {database_name: [["table_name", "row_count"], ...]}
DATABASE_STATISTICS = {
    "tpch_s1": [["region", "4"], ["nation", "24"], ["customer", "149999"], ["lineitem", "6001214"], ["orders", "1499999"], ["part", "199999"], ["partsupp", "799999"], ["supplier", "9999"]],
    
    "tpch_s10": [["customer", "1499999"], ["lineitem", "59986051"], ["nation", "24"], ["orders", "14999999"], ["part", "1999999"], ["partsupp", "7999999"], ["region", "4"], ["supplier", "99999"]],
    
    "dsb_1": [["call_center", "6"], ["catalog_page", "11718"], ["catalog_returns", "215301"], ["catalog_sales", "1438815"], ["customer", "100000"], ["customer_address", "50000"], ["customer_demographics", "1920800"], ["date_dim", "73049"], ["dbgen_version", "0"], ["household_demographics", "7200"], ["income_band", "20"], ["inventory", "11745000"], ["item", "18000"], ["promotion", "300"], ["reason", "35"], ["ship_mode", "20"], ["store", "12"], ["store_returns", "720039"], ["store_sales", "2880404"], ["time_dim", "86400"], ["warehouse", "5"], ["web_page", "60"], ["web_returns", "144042"], ["web_sales", "719384"], ["web_site", "30"]],
    
    "calcite_new_10": [["bonus", "29999999"], ["dept", "299999"], ["emp", "29999999"], ["emp_b", "29999999"], ["empnullables", "29999999"], ["empnullables_20", "55"]],
    
    "dsb_10": [["call_center", "24"], ["catalog_page", "12000"], ["catalog_returns", "2158260"], ["catalog_sales", "14397492"], ["customer", "500000"], ["customer_address", "250000"], ["customer_demographics", "1920800"], ["date_dim", "73049"], ["dbgen_version", "0"], ["household_demographics", "7200"], ["income_band", "20"], ["inventory", "133110000"], ["item", "102000"], ["promotion", "500"], ["reason", "45"], ["ship_mode", "20"], ["store", "102"], ["store_returns", "7198194"], ["store_sales", "28800991"], ["time_dim", "86400"], ["warehouse", "10"], ["web_page", "200"], ["web_returns", "1440354"], ["web_sales", "7197566"], ["web_site", "42"]]
}

def get_data_statistics(db_name: str) -> str:
    statistics = DATABASE_STATISTICS.get(db_name, [])
    return json.dumps(statistics)

def get_statistics_list(db_name: str) -> list:
    return DATABASE_STATISTICS.get(db_name, [])

def update_statistics(db_name: str, statistics: list):
    """
    Update statistics for a database.
    
    Args:
        db_name: Database name
        statistics: List of [table_name, row_count] pairs
    """
    DATABASE_STATISTICS[db_name] = statistics
    print(f"Updated statistics for database '{db_name}' with {len(statistics)} tables")

def get_available_databases() -> list:
    """Get list of available database names."""
    return list(DATABASE_STATISTICS.keys())


if __name__ == "__main__":
    # Demo usage
    print("Available databases:", get_available_databases())
    print("TPC-H S10 statistics:", get_data_statistics("tpch_s10"))