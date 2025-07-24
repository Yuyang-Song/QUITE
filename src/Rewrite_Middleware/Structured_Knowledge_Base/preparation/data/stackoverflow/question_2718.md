# Postgresql slow data readout into Python&#39;s Pandas dataframe
[Link to question](https://stackoverflow.com/questions/48927026/postgresql-slow-data-readout-into-pythons-pandas-dataframe)
**Creation Date:** 1519301294
**Score:** 3
**Tags:** database, python-3.x, postgresql, pandas, database-performance
## Question Body
<p>I am trying to read data from a table, which is a PostgreSQL database, to a Pandas dataframe. Before the DB creation, I used to store data as msgpack files (created using Pandas to_msgpack ~25 GB of data on a SSD).
The table has around ~4.5 GB, around 10^8 rows, due to the conversion of types and duplicates removal. The database is stored in the tablespace on a SSD drive. </p>

<p>Now I am rewriting my code so it works with the DB instead of Msgpack files. The only main difference in the data is that time in the msgpack files is being stored as a UNIX timestamp, since in the DB it is Postgresql's timestamp. </p>

<p>The key part is importing the data.
My current Python code:</p>

<pre><code>db_connection = psycopg2.connect("dbname={} user={} host={} password={} port={}".format(database_name, user, host, password, port))
df = pd.read_sql(('SELECT * '
                  'FROM "raw_data" '
                  # 'WHERE "time" &gt; %(dstart)s AND "time" &lt; %(dfinish)s '
                  # 'ORDER BY "time" ASC'
                  ),
                  db_connection,
                  params={"dstart": start_date, "dfinish": end_date,}, 
                  index_col=['time'])
</code></pre>

<p>It takes around 5-6 minutes to execute this code, since reading the data from Msgpack takes around 3 min. I thought it may be caused by DB -> Pandas DataFrame conversion, but when I type the same query in the SQL console it takes around the same time to display the results. Strange thing is that "explain" says that execution time is only 10 s. Is there any way to improve performance of such the process?</p>

<p>My CPU: 8-core Xenon, SSD and 64GB RAM.</p>

<p>DB structure:</p>

<pre><code>CREATE DOMAIN T AS double precision;
CREATE TABLE IF NOT EXISTS raw_data(
    time timestamp PRIMARY KEY  NOT NULL UNIQUE,
    ib1 T,
    ib2 T,
    pb1 boolean,
    pb2 boolean,
    fn int,
    bm smallint
);
</code></pre>

<p>Explain: </p>

<pre><code>test=# explain analyse select * from raw_data;
                                                             QUERY PLAN                                                             
------------------------------------------------------------------------------------------------------------------------------------
 Seq Scan on raw_data  (cost=0.00..1596470.56 rows=98799456 width=32) (actual time=0.014..6935.492 rows=98801394 loops=1)
 Planning time: 0.048 ms
 Execution time: 10199.595 ms
(3 rows)
</code></pre>

<p>Postgresql config:</p>

<pre><code>superuser_reserved_connections = 3  # (change requires restart)
dynamic_shared_memory_type = posix  # the default is the first option
log_destination = 'stderr'      # Valid values are combinations of
logging_collector = on          # Enable capturing of stderr and csvlog
log_directory = 'log'           # directory where log files are written,
log_filename = 'postgresql-%a.log'  # log file name pattern,
log_truncate_on_rotation = on       # If on, an existing log file with the
log_rotation_age = 1d           # Automatic rotation of logfiles will
log_rotation_size = 0           # Automatic rotation of logfiles will
log_line_prefix = '%m [%p] '        # special values:
log_timezone = 'Europe/Vaduz'
datestyle = 'iso, mdy'
timezone = 'UTC'
default_text_search_config = 'pg_catalog.english'
default_statistics_target = 100
maintenance_work_mem = 2GB
checkpoint_completion_target = 0.9
effective_cache_size = 44GB
work_mem = 320MB
wal_buffers = 16MB
shared_buffers = 15GB
max_connections = 20
</code></pre>

