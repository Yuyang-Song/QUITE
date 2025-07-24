# Exception has occurred: DatatypeMismatch column &quot;occurence_timestamp&quot; is of type timestamp without time zone but expression is of type bigint
[Link to question](https://stackoverflow.com/questions/79276868/exception-has-occurred-datatypemismatch-column-occurence-timestamp-is-of-type)
**Creation Date:** 1734046077
**Score:** -1
**Tags:** python, sql, python-3.x, pandas, postgresql
## Question Body
<p>Here are the core steps and logics of my script below:</p>
<ol>
<li>Create and instantiate a <code>PostgreSQLDB</code> class object that does database operation</li>
<li>Use view <code>vw_valid_case_from_db1</code> to get a list of <code>case_id</code> which will be included</li>
<li><code>df_db1_case_table</code> is a pandas df that extracts information from the table named db1</li>
<li>Filter and include only cases from 2 for the rows in <code>df_db1_case_table</code></li>
<li>I have set up a table named <code>db2_case_table</code> that I want to batch insert the information from the filtered <code>df_db1_case_table</code> (or named <code>df_db1_case_table_filtered</code>). The name of columns from <code>df_db1_case_table_filtered</code> match with the columns from <code>db2_case_table</code></li>
<li>The problem is I am getting this error <code>Exception has occurred: DatatypeMismatch column &quot;occurence_timestamp&quot; is of type timestamp without time zone but expression is of type bigint LINE 1: ...7.0, 2259027.0, NULL, 'CA23307772', NULL, '1441', 1689711600... HINT:  You will need to rewrite or cast the expression. File &quot;some_path_to.py&quot;, line 170, in &lt;module&gt; cursor.executemany(insert_query, data_to_insert) psycopg2.errors.DatatypeMismatch: column &quot;occurence_timestamp&quot; is of type timestamp without time zone but expression is of type bigint LINE 1: ...7.0, 2259027.0, NULL, 'CA23307772', NULL, '1441', 1689711600... HINT:  You will need to rewrite or cast the expression.</code></li>
<li>The section <code>for col in timestamp_columns:</code> of the code below is how I tried to solve this. Namely, if the data type of the (whatever)_timestamp is in 'int64' or 'float64' format, it will be enforced to be in datetime format. However, it doesn't work and the same error appears.</li>
<li>Additional information: if I remove all of the (whatever)_timestamp fields <code>['occurence_timestamp', 'reported_timestamp', 'created_timestamp', 'modified_timestamp', 'agency_extract_timestamp', 'city_extract_timestamp', 'pdf_extract_timestamp' ]</code>, the script works fine.</li>
</ol>
<p>Script below:</p>
<pre><code>import pandas as pd
import os
import logging
from datetime import datetime
from helper_db_operation import PostgreSQLDB

# Set up logging configuration
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Some database credential code
postgres_db = PostgreSQLDB(postgres_user, postgres_password, postgres_host, postgres_db_name)

# Query to fetch valid case IDs from db1 view
sql_query_get_valid_case_case_from_db1 = &quot;&quot;&quot;
    SELECT case_id
    FROM vw_valid_case_from_db1
&quot;&quot;&quot;

# Execute query and load results into a Pandas DataFrame
try:
    df_db1_valid_cases = pd.read_sql(sql_query_get_valid_case_case_from_db1, postgres_db.conn)
except Exception as e:
    logging.error(f&quot;Error while fetching data from db1 view: {e}&quot;)
    raise

# 1.2) connect db1_case, then apply the filter from 1.1) to exclude invalid case
# Query to fetch all case from db1 table
sql_query_get_case_table_from_db1 = &quot;&quot;&quot;
    SELECT *
    FROM public.db1_case
&quot;&quot;&quot;

# Execute query and load results into a Pandas DataFrame
df_db1_case_table = pd.read_sql(sql_query_get_case_table_from_db1, postgres_db.conn)

# Apply the filter to include only those case that are in the valid list from df_db1_valid_cases
valid_case_ids = df_db1_valid_cases['case_id'].tolist()

# Filter df_db1_case_table to include only rows where the ID is in the valid case IDs
df_db1_case_table_filtered = df_db1_case_table[df_db1_case_table['id'].isin(valid_case_ids)]

# Check the result of the filtering
logging.debug(f&quot;Filtered {len(df_db1_case_table_filtered)} valid case.&quot;)

target_table = 'db2_case_table'

# Fetch the target table schema to determine the column names dynamically
try:
    query_table_schema = f&quot;&quot;&quot;
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{target_table}';
    &quot;&quot;&quot;
    df_table_schema = pd.read_sql(query_table_schema, postgres_db.conn)
    target_columns = df_table_schema['column_name'].tolist()
except Exception as e:
    logging.error(f&quot;Error fetching schema for table {target_table}: {e}&quot;)
    raise

# Convert epoch timestamps to datetime for `occurence_timestamp` and other timestamp columns
timestamp_columns = [
    'occurence_timestamp', 'reported_timestamp', 'created_timestamp', 'modified_timestamp', 
    'agency_extract_timestamp', 'city_extract_timestamp', 'pdf_extract_timestamp'
]

for col in timestamp_columns:
    if col in df_db1_case_table_filtered.columns:
        if df_db1_case_table_filtered[col].dtype in ['int64', 'float64']:
            df_db1_case_table_filtered[col] = pd.to_datetime(
                df_db1_case_table_filtered[col], unit='s', errors='coerce'
            )
        elif pd.api.types.is_datetime64_any_dtype(df_db1_case_table_filtered[col]):
            df_db1_case_table_filtered[col] = df_db1_case_table_filtered[col].dt.tz_localize(None)

# Ensure the correct columns are included in `df_for_insertion`
df_for_insertion = df_db1_case_table_filtered[
    [col for col in df_db1_case_table_filtered.columns if col in target_columns]
]

logging.info(df_for_insertion.dtypes)
logging.info(df_for_insertion[['occurence_timestamp']].head())

# Insert the filtered and dynamically mapped data into PostgreSQL
try:
    # Convert the DataFrame into a list of tuples
    data_to_insert = df_for_insertion.to_records(index=False).tolist()
    logging.info(data_to_insert[:5])

    # Generate the INSERT query dynamically based on the DataFrame columns
    columns = ', '.join(df_for_insertion.columns)
    placeholders = ', '.join(['%s'] * len(df_for_insertion.columns))
    insert_query = f&quot;INSERT INTO {target_table} ({columns}) VALUES ({placeholders})&quot;

    # Execute the batch insert
    with postgres_db.conn.cursor() as cursor:
        cursor.executemany(insert_query, data_to_insert)
        postgres_db.conn.commit()
    
except Exception as e:
    logging.error(f&quot;Error while inserting data into table {target_table}: {e}&quot;)
    raise
</code></pre>
<p>Additional information:
This is the print out of the check of column type from the dataframe</p>
<pre><code>occurence_timestamp             datetime64[ns]
reported_timestamp              datetime64[ns]
</code></pre>
<p>This is the sample example of occurence_timestamp values</p>
<pre><code>occurence_timestamp
0 2023-07-18 20:20:00
1 2023-09-21 17:00:00
2 2023-09-21 15:48:00
3 2023-09-21 21:30:00
4 2023-09-11 08:45:00
</code></pre>

## Answers
### Answer ID: 79277938
<p>Try converting the datetime to string format</p>
<pre><code>df['occurence_timestamp'] = df['occurence_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
</code></pre>
<p>Unfortunately I am unable to test as I dont have postgres in my local.</p>

