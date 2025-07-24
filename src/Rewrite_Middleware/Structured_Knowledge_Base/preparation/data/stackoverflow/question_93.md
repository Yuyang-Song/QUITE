# PostgreSQL: How to structure and index time-related data for optimal query performance?
[Link to question](https://stackoverflow.com/questions/12544247/postgresql-how-to-structure-and-index-time-related-data-for-optimal-query-perfo)
**Creation Date:** 1348321017
**Score:** 16
**Tags:** sql, performance, postgresql, database-design, indexing
## Question Body
<p><strong>The Problem:</strong></p>

<p>I have time-related data in my database and I am struggling to organize, structure and index that data in a way so that users can retrieve it efficiently; even simple database queries take longer than acceptable.</p>

<p><strong>Project Context:</strong></p>

<p>While this is a pure database question, some context might help to understand the data model:</p>

<p>The project centers around doing research on a big, complex machine. I don't know a lot about the machine itself, but rumour in the lab has it there's a <a href="http://en.wikipedia.org/wiki/DeLorean_time_machine#Flux_capacitor" rel="nofollow noreferrer">flux capacitor</a> in there somewhere - and I think yesterday, I spotted the tail of <a href="http://en.wikipedia.org/wiki/Schr%C3%B6dinger%27s_cat" rel="nofollow noreferrer">Schrödinger's cat</a> hanging out of it at the side ;-)</p>

<p>We measure many different <em>parameters</em> while the machine is running using sensors positioned all over the machine at different measurement points (so-called <em>spots</em>) at certain intervals over a period of time. We use not only one <em>device</em> to measure these parameters, but a whole range of them; they differ in the quality of their measurement data (I think this involves sample rates, sensor quality, price and many other aspects that I'm not concerned with); one aim of the project actually is to establish a comparison between these devices. You can visualize these measurement devices as a bunch of lab trolleys, each with a lot of cables connected to the machine, each delivering measurement data. </p>

<p><strong>The Data Model:</strong></p>

<p>There is measurement data from every spot and every device for every parameter, for example once a minute over a period of 6 days. My job is to store that data in a database and to provide efficient access to it.</p>

<p>In a nutshell:</p>

<ul>
<li>a device has a unique name</li>
<li>a parameter also has a name; they're not unique though, so it also has an ID</li>
<li>a spot has an ID</li>
</ul>

<p>The project database is more complex of course, but these details don't seem relevant to the issue.</p>

<ul>
<li>a measurement data <em>index</em> has an ID, a time stamp for when the measurement was done and references to the device and the spot on which the measurement was carried out</li>
<li>a measurement data <em>value</em> has a reference to the parameter and to the value that was actually measured</li>
</ul>

<p>Initially, I had modeled the measurement data value to have its own ID as primary key; the <code>n:m</code> relationship between measurement data index and value was a separate table that only stored <code>index:value</code> ID pairs, but as that table itself consumed quite a lot of harddrive space, we eliminated it and changed the value ID to be a simple integer that stores the ID of the measurement data index it belongs to; the primary key of the measurement data value is now composed of that ID and the parameter ID.</p>

<p><em>On a side note</em>: When I created the data model, I carefully followed common design guidelines like <a href="http://en.wikipedia.org/wiki/Third_normal_form" rel="nofollow noreferrer">3NF</a> and appropriate table constraints (such as unique keys); another rule of thumb was to create an index for every foreign key. I have a suspicion that the deviation in the measurement data index / value tables from 'strict' 3NF might be one of the reasons for the performance issues I am looking at now, but changing the data model back has not solved the problem.</p>

<p><strong>The Data Model in DDL:</strong></p>

<p><strong>NOTE:</strong> There is an update to this code further below.</p>

<p>The script below creates the database and all tables involved. Please note that there are no explicit indexes yet. Before you run this, please make sure you don't happen to already have a database called <code>so_test</code> with any valuable data...</p>

<pre><code>\c postgres
DROP DATABASE IF EXISTS so_test;
CREATE DATABASE so_test;
\c so_test

CREATE TABLE device
(
  name VARCHAR(16) NOT NULL,
  CONSTRAINT device_pk PRIMARY KEY (name)
);

CREATE TABLE parameter
(
  -- must have ID as names are not unique
  id SERIAL,
  name VARCHAR(64) NOT NULL,
  CONSTRAINT parameter_pk PRIMARY KEY (id)
);

CREATE TABLE spot
(
  id SERIAL,
  CONSTRAINT spot_pk PRIMARY KEY (id)
);

CREATE TABLE measurement_data_index
(
  id SERIAL,
  fk_device_name VARCHAR(16) NOT NULL,
  fk_spot_id INTEGER NOT NULL,
  t_stamp TIMESTAMP NOT NULL,
  CONSTRAINT measurement_pk PRIMARY KEY (id),
  CONSTRAINT measurement_data_index_fk_2_device FOREIGN KEY (fk_device_name)
    REFERENCES device (name) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_index_fk_2_spot FOREIGN KEY (fk_spot_id)
    REFERENCES spot (id) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_index_uk_all_cols UNIQUE (fk_device_name, fk_spot_id, t_stamp)
);

CREATE TABLE measurement_data_value
(
  id INTEGER NOT NULL,
  fk_parameter_id INTEGER NOT NULL,
  value VARCHAR(16) NOT NULL,
  CONSTRAINT measurement_data_value_pk PRIMARY KEY (id, fk_parameter_id),
  CONSTRAINT measurement_data_value_fk_2_parameter FOREIGN KEY (fk_parameter_id)
    REFERENCES parameter (id) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION
);
</code></pre>

<p>I have also created a script to fill the table with some test data:</p>

<pre><code>CREATE OR REPLACE FUNCTION insert_data()
RETURNS VOID
LANGUAGE plpgsql
AS
$BODY$
  DECLARE
    t_stamp  TIMESTAMP := '2012-01-01 00:00:00';
    index_id INTEGER;
    param_id INTEGER;
    dev_name VARCHAR(16);
    value    VARCHAR(16);
  BEGIN
    FOR dev IN 1..5
    LOOP
      INSERT INTO device (name) VALUES ('dev_' || to_char(dev, 'FM00'));
    END LOOP;
    FOR param IN 1..20
    LOOP
      INSERT INTO parameter (name) VALUES ('param_' || to_char(param, 'FM00'));
    END LOOP;
    FOR spot IN 1..10
    LOOP
      INSERT INTO spot (id) VALUES (spot);
    END LOOP;

    WHILE t_stamp &lt; '2012-01-07 00:00:00'
    LOOP
      FOR dev IN 1..5
      LOOP
        dev_name := 'dev_' || to_char(dev, 'FM00');
        FOR spot IN 1..10
        LOOP
          INSERT INTO measurement_data_index
            (fk_device_name, fk_spot_id, t_stamp)
            VALUES (dev_name, spot, t_stamp) RETURNING id INTO index_id;
          FOR param IN 1..20
          LOOP
            SELECT id INTO param_id FROM parameter
              WHERE name = 'param_' || to_char(param, 'FM00');
            value := 'd'  || to_char(dev,   'FM00')
                  || '_s' || to_char(spot,  'FM00')
                  || '_p' || to_char(param, 'FM00');
            INSERT INTO measurement_data_value (id, fk_parameter_id, value)
              VALUES (index_id, param_id, value);
          END LOOP;
        END LOOP;
      END LOOP;
      t_stamp := t_stamp + '1 minute'::INTERVAL;
    END LOOP;

  END;
$BODY$;

SELECT insert_data();
</code></pre>

<p>The PostgreSQL query planner requires up to date statistics, so analyze all tables. Vacuuming might not be required, but do it anyway:</p>

<pre><code>VACUUM ANALYZE device;
VACUUM ANALYZE measurement_data_index;
VACUUM ANALYZE measurement_data_value;
VACUUM ANALYZE parameter;
VACUUM ANALYZE spot;
</code></pre>

<p><strong>A Sample Query:</strong></p>

<p>If I now run a really simple query to e.g. obtain all value for a certain parameter, it already takes a couple of seconds, although the database is not very large yet:</p>

<pre><code>EXPLAIN (ANALYZE ON, BUFFERS ON)
SELECT measurement_data_value.value
  FROM measurement_data_value, parameter
 WHERE measurement_data_value.fk_parameter_id = parameter.id
   AND parameter.name = 'param_01';
</code></pre>

<p>Exemplary result on my development machine (please see below for some details on my environment):</p>

<pre><code>                                                                QUERY PLAN                                                                
------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join  (cost=1.26..178153.26 rows=432000 width=12) (actual time=0.046..2281.281 rows=432000 loops=1)
   Hash Cond: (measurement_data_value.fk_parameter_id = parameter.id)
   Buffers: shared hit=55035
   -&gt;  Seq Scan on measurement_data_value  (cost=0.00..141432.00 rows=8640000 width=16) (actual time=0.004..963.999 rows=8640000 loops=1)
         Buffers: shared hit=55032
   -&gt;  Hash  (cost=1.25..1.25 rows=1 width=4) (actual time=0.010..0.010 rows=1 loops=1)
         Buckets: 1024  Batches: 1  Memory Usage: 1kB
         Buffers: shared hit=1
         -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual time=0.004..0.008 rows=1 loops=1)
               Filter: ((name)::text = 'param_01'::text)
               Buffers: shared hit=1
 Total runtime: 2313.615 ms
(12 rows)
</code></pre>

<p>There are no indexes in the database apart from the implicit ones, so it's not surprising the planner does sequential scans only. If I follow what seems to be a rule of thumb and add btree indexes for every foreign key like</p>

<pre><code>CREATE INDEX measurement_data_index_idx_fk_device_name
    ON measurement_data_index (fk_device_name);
CREATE INDEX measurement_data_index_idx_fk_spot_id
    ON measurement_data_index (fk_spot_id);
CREATE INDEX measurement_data_value_idx_fk_parameter_id
    ON measurement_data_value (fk_parameter_id);
</code></pre>

<p>then do another vacuum analyze (just to be safe) and re-run the query, the planner uses bitmap heap and bitmap index scans and the total query time somewhat improves:</p>

<pre><code>                                                                                   QUERY PLAN                                                                                   
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Nested Loop  (cost=8089.19..72842.42 rows=431999 width=12) (actual time=66.773..1336.517 rows=432000 loops=1)
   Buffers: shared hit=55033 read=1184
   -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual time=0.005..0.012 rows=1 loops=1)
         Filter: ((name)::text = 'param_01'::text)
         Buffers: shared hit=1
   -&gt;  Bitmap Heap Scan on measurement_data_value  (cost=8089.19..67441.18 rows=431999 width=16) (actual time=66.762..1237.488 rows=432000 loops=1)
         Recheck Cond: (fk_parameter_id = parameter.id)
         Buffers: shared hit=55032 read=1184
         -&gt;  Bitmap Index Scan on measurement_data_value_idx_fk_parameter_id  (cost=0.00..7981.19 rows=431999 width=0) (actual time=65.222..65.222 rows=432000 loops=1)
               Index Cond: (fk_parameter_id = parameter.id)
               Buffers: shared read=1184
 Total runtime: 1371.716 ms
(12 rows)
</code></pre>

<p>However, this is still more than a second of execution time for a really simple query.</p>

<p><strong>What I have done so far:</strong></p>

<ul>
<li>got myself a copy of <a href="http://www.packtpub.com/postgresql-90-high-performance/book" rel="nofollow noreferrer">PostgreSQL 9.0 High Performance</a> - great book!</li>
<li>did some basic PostgreSQL server configuration, see environment below</li>
<li>created a framework to run a series of performance tests using real queries from the project and to display the results graphically; these queries use devices, spots, parameters and a time interval as input parameters and the test series run over e.g. 5, 10 devices, 5, 10 spots, 5, 10, 15, 20 parameters and 1..7 days. The basic result is that they're all too slow, but their query plan was way too complex for me to understand, so I went back to the really simple query used above.</li>
</ul>

<p>I have looked into <a href="http://www.postgresql.org/docs/current/interactive/ddl-partitioning.html" rel="nofollow noreferrer">partitioning</a> the value table. The data is time-related and partitioning seems an appropriate means to organize that kind of data; even the <a href="http://www.postgresql.org/docs/current/interactive/ddl-partitioning.html#DDL-PARTITIONING-IMPLEMENTATION" rel="nofollow noreferrer">examples</a> in the PostgreSQL documentation use something similar. However, I read in the <a href="http://www.postgresql.org/docs/current/interactive/ddl-partitioning.html#DDL-PARTITIONING-OVERVIEW" rel="nofollow noreferrer">same article</a>:</p>

<blockquote>
  <p>The benefits will normally be worthwhile only when a table would otherwise be very large. The exact point at which a table will benefit from partitioning depends on the application, although a rule of thumb is that the size of the table should exceed the physical memory of the database server.</p>
</blockquote>

<p>The entire test database is less than 1GB in size and I am running my tests on a development machine with 8GB of RAM and on a virtual machine with 1GB (see also environment below), so the table is far from being very large or even exceeding the physical memory. I might implement partitioning anyway at some stage, but I have a feeling that approach does not target the performance problem itself.</p>

<p>Furthermore, I am considering to <a href="http://www.postgresql.org/docs/current/interactive/sql-cluster.html" rel="nofollow noreferrer">cluster</a> the value table. I dislike the fact that clustering must be re-done whenever new data is inserted and that it furthermore requires an exclusive read/write lock, but looking at <a href="https://stackoverflow.com/a/9436055/217844">this</a> SO question, it seems that it anyway has its benefits and might be an option. However, clustering is done on an index and as there are up to 4 selection criteria going into a query (devices, spots, parameters and time), I would have to create clusters for all of them - which in turn gives me the impression that I'm simply not creating the right indexes...</p>

<p><strong>My Environment:</strong></p>

<ul>
<li>development is taking place on a MacBook Pro (mid-2009) with a dual-core CPU and 8GB of RAM</li>
<li>I am running database performance tests on a virtual Debian 6.0 machine with 1GB of RAM, hosted on the MBP</li>
<li>PostgreSQL version is 9.1 as that was the latest version when I installed it, upgrading to 9.2 would be possible</li>
<li>I have changed <code>shared_buffers</code> from the default 1600kB to 25% of RAM on both machines as recommended in the <a href="http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server#shared_buffers" rel="nofollow noreferrer">PostgreSQL docs</a> (which involved enlarging <a href="http://www.postgresql.org/docs/current/interactive/kernel-resources.html" rel="nofollow noreferrer">kernel settings</a> like SHMALL, SHMMAX, etc.)</li>
<li>similarly, I have changed <a href="http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server#effective_cache_size" rel="nofollow noreferrer">effective_cache_size</a> from the default 128MB to 50% of the RAM available</li>
<li>I ran performance test with different <a href="http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server#work_mem" rel="nofollow noreferrer">work_mem</a> settings, but did not see any major difference in performance</li>
</ul>

<p><strong>NOTE:</strong> One aspect that I believe is important is that the performance test series with real queries from the project do not differ performance-wise between the MacBook with 8GB and the virtual machine with 1GB; i.e. if a query takes 10s on the MacBook, it also takes 10s on the VM. Also, I ran the same performance tests before and after changing <code>shared_buffers</code>, <code>effective_cache_size</code> and <code>work_mem</code> and the configuration changes did not improve performance by more than 10%; some results in fact even got worse, so it seems any difference is caused rather by test variation than by configuration change. These observations lead me to believe that RAM and <code>postgres.conf</code> settings are not the limiting factors here yet. </p>

<p><strong>My Questions:</strong></p>

<p>I don't know if different or additional indexes would speed up the query and if they did, which ones to create. Looking at the size of the database and how simple my query is, I have the impression there is something fundamentally wrong about my data model or how I have chosen my indexes so far.</p>

<p>Does anyone have some advice for me how to structure and index time-related my to improve query performance ?</p>

<p>Asked more broadly, is tuning query performance</p>

<ul>
<li>usually done 'on an incident base', i.e. once a query does not perform satisfactorily ? It seems <em>all</em> my queries are too slow...</li>
<li>mainly a question of looking at (and understanding) query plans, then adding indexes and measuring if things improved, possibly accelerating the process by applying one's experience ?</li>
</ul>

<p>How do I get this database to fly ?</p>

<hr>

<p><strong>Update 01:</strong></p>

<p>Looking at the responses so far, I think I have not explained the need for measurement data index / values tables properly, so let me try again. <strong>Storage space</strong> is the issue here.</p>

<p><strong>NOTE:</strong></p>

<ul>
<li>the figures used here are more of illustrative purpose and meant for comparison only, i.e. the numbers themselves are not relevant, what matters is the percental difference in storage requirements between using a single table vs. using an index and a value table</li>
<li>PostgreSQL data type storage sizes are documented in <a href="http://www.postgresql.org/docs/current/interactive/datatype.html" rel="nofollow noreferrer">this</a> chapter</li>
<li>this makes no claim to be scientifically correct, e.g. the units are probably mathematical bogus; the numbers should add up though</li>
</ul>

<p>Assuming</p>

<ul>
<li>1 day of measurements</li>
<li>1 set of measurements per minute</li>
<li>10 devices</li>
<li>10 parameters</li>
<li>10 spots</li>
</ul>

<p>This adds up to</p>

<pre>
1 meas/min x 60 min/hour x 24 hour/day = 1440 meas/day
</pre>

<p>Each measurement has data from every spot and every device for every parameter, so</p>

<pre>
10 spots x 10 devices x 10 parameters = 1000 data sets/meas
</pre>

<p>So in total</p>

<pre>
1440 meas/day x 1000 data sets/meas = 1 440 000 data sets/day
</pre>

<p>If we store all measurements in a single table as <a href="https://stackoverflow.com/a/12545542/217844">Catcall suggested</a>, e.g.</p>

<pre><code>CREATE TABLE measurement_data
(
  device_name character varying(16) NOT NULL,
  spot_id integer NOT NULL,
  parameter_id integer NOT NULL,
  t_stamp timestamp without time zone NOT NULL,
  value character varying(16) NOT NULL,
  -- constraints...
);
</code></pre>

<p>a single row would add up to</p>

<pre>
17 + 4 + 4 + 8 + 17 = 50 bytes/row
</pre>

<p>in the worst case where all varchar fields are fully filled. This amounts to</p>

<pre>
50 bytes/row x 1 440 000 rows/day = 72 000 000 bytes/day
</pre>

<p>or ~69 MB per day.</p>

<p>While this does not sound a lot, the storage space requirement in the real database would be prohibitive (again, the numbers used here are only for illustration). We have therefore split measurement data into an index and a value table as explained earlier in the question:</p>

<pre><code>CREATE TABLE measurement_data_index
(
  id SERIAL,
  fk_device_name VARCHAR(16) NOT NULL,
  fk_spot_id INTEGER NOT NULL,
  t_stamp TIMESTAMP NOT NULL,
  -- constraints...
);

CREATE TABLE measurement_data_value
(
  id INTEGER NOT NULL,
  fk_parameter_id INTEGER NOT NULL,
  value VARCHAR(16) NOT NULL,
  -- constraints...
);
</code></pre>

<p>where <strong>the ID of a value row is equal to the ID of the index it belongs to</strong>.</p>

<p>The sizes of a row in the index and value tables are</p>

<pre>
index: 4 + 17 + 4 + 8 = 33 bytes
value: 4 + 4 + 17     = 25 bytes
</pre>

<p>(again, worst case scenario). The total amount of rows is</p>

<pre>
index: 10 devices x 10 spots x 1440 meas/day =   144 000 rows/day
value: 10 parameters x 144 000 rows/day      = 1 440 000 rows/day
</pre>

<p>so the total is</p>

<pre>
index: 33 bytes/row x   144 000 rows/day =  4 752 000 bytes/day
value: 25 bytes/row x 1 440 000 rows/day = 36 000 000 bytes/day
total:                                   = 40 752 000 bytes/day
</pre>

<p>or ~39 MB per day - as opposed to ~69 MB for a single table solution.</p>

<hr>

<p><strong>Update 02 (re: <a href="https://stackoverflow.com/a/12553459/217844">wildplassers response</a>):</strong></p>

<p>This question is getting pretty long as it is, so I was considering updating the code in place in the original question above, but I think it might help to have both the first and the improved solutions in here to better see the differences.</p>

<p>Changes compared to the original approach (somewhat in order of importance):</p>

<ul>
<li>swap timestamp and parameter, i.e. move <code>t_stamp</code> field from <code>measurement_data_index</code> table to <code>measurement_data_value</code> and move <code>fk_parameter_id</code> field from value to index table: With this change, all fields in the index table are constant and new measurement data is written to the value table only. I did not expect any major query performance improvement from this (I was wrong), but I feel it makes the measurement data index concept clearer. While it requires fractionally more storage space (according to some rather crude estimate), having a 'static' index table might also help in deployment when <a href="http://www.postgresql.org/docs/current/interactive/manage-ag-tablespaces.html" rel="nofollow noreferrer">tablespaces</a> are moved to different harddrives according to their read/write requirements.</li>
<li>use a surrogate key in device table: From what I understand, a surrogate key is a primary key that is not strictly required from a database design point of view (e.g. device name is already unique, so it could also serve as PK), but might help to improve query performance. I added it because again, I feel it makes the concept clearer if the index table references IDs only (instead of some names and some IDs).</li>
<li>rewrite <code>insert_data()</code>: Use <code>generate_series()</code> instead of nested <code>FOR</code> loops; makes the code much 'snappier'.</li>
<li>As a side effect of these changes, inserting test data takes only about 50% of the time required by the first solution.</li>
<li>I did not add the view as wildplasser suggested; there's no backward compatibility required.</li>
<li>Additional indexes for the FKs in the index table seem to be ignored by the query planner and have no impact on query plan or performance.</li>
</ul>

<p>(it seems without this line, the code below is not properly displayed as code on the SO page...)</p>

<pre><code>\c postgres
DROP DATABASE IF EXISTS so_test_03;
CREATE DATABASE so_test_03;
\c so_test_03

CREATE TABLE device
(
  id SERIAL,
  name VARCHAR(16) NOT NULL,
  CONSTRAINT device_pk PRIMARY KEY (id),
  CONSTRAINT device_uk_name UNIQUE (name)
);

CREATE TABLE parameter
(
  id SERIAL,
  name VARCHAR(64) NOT NULL,
  CONSTRAINT parameter_pk PRIMARY KEY (id)
);

CREATE TABLE spot
(
  id SERIAL,
  name VARCHAR(16) NOT NULL,
  CONSTRAINT spot_pk PRIMARY KEY (id)
);

CREATE TABLE measurement_data_index
(
  id SERIAL,
  fk_device_id    INTEGER NOT NULL,
  fk_parameter_id INTEGER NOT NULL,
  fk_spot_id      INTEGER NOT NULL,
  CONSTRAINT measurement_pk PRIMARY KEY (id),
  CONSTRAINT measurement_data_index_fk_2_device FOREIGN KEY (fk_device_id)
    REFERENCES device (id) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_index_fk_2_parameter FOREIGN KEY (fk_parameter_id)
    REFERENCES parameter (id) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_index_fk_2_spot FOREIGN KEY (fk_spot_id)
    REFERENCES spot (id) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_index_uk_all_cols UNIQUE (fk_device_id, fk_parameter_id, fk_spot_id)
);

CREATE TABLE measurement_data_value
(
  id INTEGER NOT NULL,
  t_stamp TIMESTAMP NOT NULL,
  value VARCHAR(16) NOT NULL,
  -- NOTE: inverse field order compared to wildplassers version
  CONSTRAINT measurement_data_value_pk PRIMARY KEY (id, t_stamp),
  CONSTRAINT measurement_data_value_fk_2_index FOREIGN KEY (id)
    REFERENCES measurement_data_index (id) MATCH FULL
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE OR REPLACE FUNCTION insert_data()
RETURNS VOID
LANGUAGE plpgsql
AS
$BODY$
  BEGIN
    INSERT INTO device (name)
    SELECT 'dev_' || to_char(item, 'FM00')
    FROM generate_series(1, 5) item;

    INSERT INTO parameter (name)
    SELECT 'param_' || to_char(item, 'FM00')
    FROM generate_series(1, 20) item;

    INSERT INTO spot (name)
    SELECT 'spot_' || to_char(item, 'FM00')
    FROM generate_series(1, 10) item;

    INSERT INTO measurement_data_index (fk_device_id, fk_parameter_id, fk_spot_id)
    SELECT device.id, parameter.id, spot.id
    FROM device, parameter, spot;

    INSERT INTO measurement_data_value(id, t_stamp, value)
    SELECT index.id,
           item,
           'd'  || to_char(index.fk_device_id,    'FM00') ||
           '_s' || to_char(index.fk_spot_id,      'FM00') ||
           '_p' || to_char(index.fk_parameter_id, 'FM00')
    FROM measurement_data_index index,
         generate_series('2012-01-01 00:00:00', '2012-01-06 23:59:59', interval '1 min') item;
  END;
$BODY$;

SELECT insert_data();
</code></pre>

<p>At some stage, I will change my own conventions to using inline <code>PRIMARY KEY</code> and <code>REFERENCES</code> statements instead of explicit <code>CONSTRAINT</code>s; for the moment, I think keeping this the way it was makes it easier to compare the two solutions.</p>

<p>Don't forget to update statistics for the query planner:</p>

<pre><code>VACUUM ANALYZE device;
VACUUM ANALYZE measurement_data_index;
VACUUM ANALYZE measurement_data_value;
VACUUM ANALYZE parameter;
VACUUM ANALYZE spot;
</code></pre>

<p>Run a query that should produce the same result as the one in the first approach:</p>

<pre><code>EXPLAIN (ANALYZE ON, BUFFERS ON)
SELECT measurement_data_value.value
  FROM measurement_data_index,
       measurement_data_value,
       parameter
 WHERE measurement_data_index.fk_parameter_id = parameter.id
   AND measurement_data_index.id = measurement_data_value.id
   AND parameter.name = 'param_01';
</code></pre>

<p>Result:</p>

<pre><code>Nested Loop  (cost=0.00..34218.28 rows=431998 width=12) (actual time=0.026..696.349 rows=432000 loops=1)
  Buffers: shared hit=435332
  -&gt;  Nested Loop  (cost=0.00..29.75 rows=50 width=4) (actual time=0.012..0.453 rows=50 loops=1)
        Join Filter: (measurement_data_index.fk_parameter_id = parameter.id)
        Buffers: shared hit=7
        -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual time=0.005..0.010 rows=1 loops=1)
              Filter: ((name)::text = 'param_01'::text)
              Buffers: shared hit=1
        -&gt;  Seq Scan on measurement_data_index  (cost=0.00..16.00 rows=1000 width=8) (actual time=0.003..0.187 rows=1000 loops=1)
              Buffers: shared hit=6
  -&gt;  Index Scan using measurement_data_value_pk on measurement_data_value  (cost=0.00..575.77 rows=8640 width=16) (actual time=0.013..12.157 rows=8640 loops=50)
        Index Cond: (id = measurement_data_index.id)
        Buffers: shared hit=435325
Total runtime: 726.125 ms
</code></pre>

<p>This is almost half of the ~1.3s the first approach required; considering I'm loading 432K rows, it is a result I can live with for the moment.</p>

<p><strong>NOTE:</strong> The field order in the value table PK is <code>id, t_stamp</code>; the order in wildplassers response is <code>t_stamp, whw_id</code>. I did this that way because I feel a 'regular' field order is the one in which fields are listed in the table declaration (and 'reverse' is then the other way around), but that's just my own convention that keeps me from getting confused. Either way, as <a href="https://stackoverflow.com/a/12545427/217844">Erwin Brandstetter</a> pointed out, this order is absolutely <strong>critical</strong> for the performance improvement; if it is the wrong way around (and a reverse index as in wildplassers solution is missing), the query plan looks like below and performance is more than 3 times worse:</p>

<pre><code>Hash Join  (cost=22.14..186671.54 rows=431998 width=12) (actual time=0.460..2570.941 rows=432000 loops=1)
  Hash Cond: (measurement_data_value.id = measurement_data_index.id)
  Buffers: shared hit=63537
  -&gt;  Seq Scan on measurement_data_value  (cost=0.00..149929.58 rows=8639958 width=16) (actual time=0.004..1095.606 rows=8640000 loops=1)
        Buffers: shared hit=63530
  -&gt;  Hash  (cost=21.51..21.51 rows=50 width=4) (actual time=0.446..0.446 rows=50 loops=1)
        Buckets: 1024  Batches: 1  Memory Usage: 2kB
        Buffers: shared hit=7
        -&gt;  Hash Join  (cost=1.26..21.51 rows=50 width=4) (actual time=0.015..0.359 rows=50 loops=1)
              Hash Cond: (measurement_data_index.fk_parameter_id = parameter.id)
              Buffers: shared hit=7
              -&gt;  Seq Scan on measurement_data_index  (cost=0.00..16.00 rows=1000 width=8) (actual time=0.002..0.135 rows=1000 loops=1)
                    Buffers: shared hit=6
              -&gt;  Hash  (cost=1.25..1.25 rows=1 width=4) (actual time=0.008..0.008 rows=1 loops=1)
                    Buckets: 1024  Batches: 1  Memory Usage: 1kB
                    Buffers: shared hit=1
                    -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual time=0.004..0.007 rows=1 loops=1)
                          Filter: ((name)::text = 'param_01'::text)
                          Buffers: shared hit=1
Total runtime: 2605.277 ms
</code></pre>

## Answers
### Answer ID: 12553459
<p>The idea behind this "solution" is: avoid the separate key-domains for {device,spot,paramater}. There are only 1000 possible combinations of these three. (could be seen as a bad case of BCNF-violation). So I combine them into one what_how_where table, which refers to the tree separate domains. The number of key-elements in the measurement(data) table is reduced from 4 to 2, and the surrogate key is omitted (since it is not used) The what_how_where table <em>does</em> have a surrogate key. I's meaning can be expressed as: if a tuple is present in this table: the parameter 'what' can be measured by device 'how' on location 'where".</p>

<pre><code>-- temp schema for scratch
DROP SCHEMA tmp CASCADE;
CREATE SCHEMA tmp;
SET search_path=tmp;

        -- tables for the three "key domain"s
CREATE TABLE device
        ( id SERIAL NOT NULL PRIMARY KEY
        , dname VARCHAR NOT NULL -- 'name' might be a reserve word
        , CONSTRAINT device_name UNIQUE (dname)
        );

CREATE TABLE parameter
        ( id SERIAL PRIMARY KEY -- must have ID as names are not unique
        , pname VARCHAR NOT NULL
        );

CREATE TABLE spot
        ( id SERIAL PRIMARY KEY
        , sname VARCHAR NOT NULL
        );
        -- One table to combine the three "key domain"s
CREATE TABLE what_how_where
        ( id SERIAL NOT NULL PRIMARY KEY
        , device_id INTEGER NOT NULL REFERENCES device(id)
        , spot_id INTEGER NOT NULL REFERENCES spot(id)
        , parameter_id INTEGER NOT NULL REFERENCES parameter(id)
        , CONSTRAINT what_natural UNIQUE (device_id,spot_id,parameter_id)
        );

CREATE TABLE measurement
        ( whw_id INTEGER NOT NULL REFERENCES what_how_where(id)
        , t_stamp TIMESTAMP NOT NULL
        , value VARCHAR(32) NOT NULL
        , CONSTRAINT measurement_natural PRIMARY KEY (t_stamp,whw_id)
        );

INSERT INTO device (dname)
SELECT 'dev_' || d::text
FROM generate_series(1,10) d;

INSERT INTO parameter (pname)
SELECT 'param_' || p::text
FROM generate_series(1,10) p;

INSERT INTO spot (sname)
SELECT 'spot_' || s::text
FROM generate_series(1,10) s;

INSERT INTO what_how_where (device_id,spot_id,parameter_id)
SELECT d.id,s.id,p.id
FROM device d
JOIN spot s ON(1=1)
JOIN parameter p ON(1=1)
        ;
ANALYSE what_how_where;

INSERT INTO measurement(whw_id, t_stamp, value)
SELECT w.id
        , g
        , random()::text
FROM what_how_where w
JOIN generate_series('2012-01-01'::date, '2012-09-23'::date, '1 day'::interval) g
        ON (1=1)
        ;

CREATE UNIQUE INDEX measurement_natural_reversed ON measurement(whw_id,t_stamp);
ANALYSE measurement;

        -- A view to *more or less* emulate the original behaviour
DROP VIEW measurement_data ;
CREATE VIEW measurement_data AS (
        SELECT d.dname AS dname
        , p.pname AS pname
        , w.spot_id AS spot_id
        , w.parameter_id AS parameter_id
        , m.t_stamp AS t_stamp
        , m.value AS value
        FROM measurement m
        JOIN what_how_where w ON m.whw_id = w.id
        JOIN device d ON w.device_id = d.id
        JOIN parameter p ON w.parameter_id = p.id
        );


EXPLAIN (ANALYZE ON, BUFFERS ON)
SELECT md.value
  FROM measurement_data md
 WHERE md.pname = 'param_8'
   AND md.t_stamp &gt;= '2012-07-01'
   AND md.t_stamp &lt; '2012-08-01'
        ;
</code></pre>

<p>UPDATE: there is one practical problem, which can only be solved by some kind of clustering:</p>

<ul>
<li>given an estimated row size of 50 bytes</li>
<li>and a <em>specificity</em> of the query of 5% only (1/20) of the parameters is wanted</li>
<li>which means that about 4 "wanted" tuples live on a OS disk page (+76 unwanted tuples)</li>
</ul>

<p>Without clustering, this means that <em>all</em> the pages have to been pulled in + inspected. Indexes do not help here (they only help if they can <em>avoid</em> pages being pulled in, this <em>could</em> be the case for a (range)search on the first key column(s)) The indexes may help a bit for scanning the in-memory pages <em>after</em> these have been fetched.</p>

<p>As a consequence, this means that (once the footprint of your query is larger that available bufferspace) your query actually measures the I/O speed of your machine.</p>

### Answer ID: 12545427
<p>I basically revised your whole setup. Tested under PostgreSQL 9.1.5.</p>

<h3>DB schema</h3>

<ul>
<li><p>I think that your table layout has a major logical flaw (as also pointed out by @Catcall). I changed it the way I suspect it should be:<br>
Your last table <code>measurement_data_value</code> (which I renamed to <code>measure_val</code>) is supposed to save a value per <code>parameter</code> (now: <code>param</code>) for every row in <code>measurement_data_index</code> (now: <code>measure</code>). See below.</p></li>
<li><p>Even though "a device has a unique name" use an integer surrogate primary key anyway. Text strings are inherently bulkier and slower to be used as foreign keys in big tables. They are also subject to <strong>collation</strong>, which can slow down queries significantly.</p>

<p><a href="https://stackoverflow.com/q/9888096/939860">Under this related question</a> we found that joining and sorting on a medium sized <code>text</code> column was the major slow-down.
If you insist on using a text string as primary key, read up on <a href="http://www.postgresql.org/docs/current/interactive/collation.html" rel="nofollow noreferrer">collation support</a> in PostgreSQL 9.1 or later.</p></li>
<li><p>Don't fall for the anti-pattern of using <code>id</code> as name for a primary key. When you join a couple of tables (like you will have to do a lot!) you end up with several columns name <code>id</code> - what a mess! (Sadly, some ORMs use it.)</p>

<p>Instead, name a surrogate primary key column after the table somehow to make it meaningful on its own. Then you can have foreign keys referencing it have the same name (that's a good, as they contain the same data).</p>

<pre><code>CREATE TABLE spot
( <b>spot_id</b> SERIAL PRIMARY KEY);</code></pre></li>
<li><p>Don't use super-long identifiers. They are hard to type and hard to read. Rule of thumb: as long a necessary to be clear, as short as possible.</p></li>
<li><p>Don't use <code>varchar(n)</code> if you don't have a compelling reason. Just use <a href="http://www.postgresql.org/docs/current/interactive/datatype-character.html" rel="nofollow noreferrer"><code>varchar</code>, or simpler: just <code>text</code></a>.</p></li>
</ul>

<p>All this and more went into my proposal for a better db schema:</p>

<pre><code>CREATE TABLE device
( device_id serial PRIMARY KEY 
 ,device text NOT NULL
);

CREATE TABLE param
( param_id serial PRIMARY KEY
 ,param text NOT NULL
);
CREATE INDEX param_param_idx ON param (param); -- you are looking up by name!

CREATE TABLE spot
( spot_id  serial PRIMARY KEY);

CREATE TABLE measure
( measure_id serial PRIMARY KEY
 ,device_id int NOT NULL REFERENCES device (device_id) ON UPDATE CASCADE
 ,spot_id int NOT NULL REFERENCES spot (spot_id) ON UPDATE CASCADE
 ,t_stamp timestamp NOT NULL
 ,CONSTRAINT measure_uni UNIQUE (device_id, spot_id, t_stamp)
);

CREATE TABLE measure_val   -- better name? 
( measure_id int NOT NULL REFERENCES measure (measure_id)
                 ON UPDATE CASCADE ON DELETE CASCADE  -- guessing it fits
 ,param_id int NOT NULL REFERENCES param (param_id)
                 ON UPDATE CASCADE ON DELETE CASCADE  -- guessing it fits
 ,value text NOT NULL
 ,CONSTRAINT measure_val_pk PRIMARY KEY (measure_id, param_id)
);
CREATE INDEX measure_val_param_id_idx ON measure_val (param_id);  -- !crucial!
</code></pre>

<p>I renamed the bulky <code>measurement_data_value</code> to <code>measure_val</code>, because that's what's in the table: parameter-values for measurements. Now, the <strong>multi-column pk</strong> makes sense, too.</p>

<p>But I added a <strong>separate index on <code>param_id</code></strong>. The way you had it, column <code>param_id</code> was the second column in a multi-column index, which leads to poor results for <code>param_id</code>. Read all the <a href="https://dba.stackexchange.com/q/6115/3684">gory details about that under this related question on dba.SE</a>.</p>

<p>After implementing this alone, your query should be faster. But there is more you can do.</p>

<h3>Test data</h3>

<p>This fills in the data <strong>much faster</strong>. The point is that I use set-based DML commands, executing mass-inserts instead of loops that execute individual inserts, which takes forever. Makes quite a difference for the considerable amount of test data you want to insert. It's also much shorter and simpler.</p>

<p>To make it even more efficient, I use a <a href="http://www.postgresql.org/docs/current/interactive/queries-with.html#QUERIES-WITH-MODIFYING" rel="nofollow noreferrer">data-modifying CTE</a> (new in Postgres 9.1) that instantly reuses the massive amount of rows in the last step.</p>

<pre><code>CREATE OR REPLACE FUNCTION insert_data()
RETURNS void LANGUAGE plpgsql AS
$BODY$
BEGIN
   INSERT INTO device (device)
   SELECT 'dev_' || to_char(g, 'FM00')
   FROM generate_series(1,5) g;

   INSERT INTO param (param)
   SELECT 'param_' || to_char(g, 'FM00')
   FROM generate_series(1,20) g;

   INSERT INTO spot (spot_id)
   SELECT nextval('spot_spot_id_seq'::regclass)
   FROM generate_series(1,10) g; -- to set sequence, too

   WITH x AS (
      INSERT INTO measure (device_id, spot_id, t_stamp)
      SELECT d.device_id, s.spot_id, g
      FROM   device    d
      CROSS  JOIN spot s
      CROSS  JOIN generate_series('2012-01-06 23:00:00' -- smaller set
                                 ,'2012-01-07 00:00:00' -- for quick tests
                                 ,interval '1 min') g
      RETURNING *
      )
   INSERT INTO measure_val (measure_id, param_id, value)
   SELECT x.measure_id
         ,p.param_id
         ,x.device_id || '_' || x.spot_id || '_' || p.param
   FROM  x
   CROSS JOIN param p;
END
$BODY$;
</code></pre>

<p>Call:</p>

<pre><code>SELECT insert_data();
</code></pre>

<h3>Query</h3>

<ul>
<li>Use explicit <code>JOIN</code> syntax and table aliased to make your queries easier to read and debug:</li>
</ul>

<pre><code>SELECT v.value
FROM   param <b>p</b>
JOIN   measure_val <b>v USING (param_id)</b>
WHERE  p.param = 'param_01';
</code></pre>

<p>The <code>USING</code> clause is just for simplifying the syntax, but not superior to <code>ON</code> otherwise.</p>

<p>This should be <strong>much faster</strong> now for two reasons:</p>

<ul>
<li>Index <code>param_param_idx</code> on <code>param.param</code>.</li>
<li>Index <code>measure_val_param_id_idx</code> on <code>measure_val.param_id</code>, like explained in detail <a href="https://dba.stackexchange.com/q/6115/3684">here</a>.</li>
</ul>

<h3>Edit after feedback</h3>

<p>My major oversight was that you already had added the crucial index in form of <code>measurement_data_value_idx_fk_parameter_id</code> further down in your question. (I blame your cryptic names! :p ) On closer inspection, you have more than 10M (7 * 24 * 60 * 5 * 10 * 20) rows in your test setup and your query retrieves > 500K. I only tested with a much smaller subset.</p>

<p>Also, as you retrieve 5% of the whole table, indexes will only go so far. I was to optimistic, such an amount of data is bound to take some time. Is it a realistic requirement that you query 500k rows? I would assume you aggregate in your real life application?</p>

<h3>Further options</h3>

<ul>
<li><a href="http://www.postgresql.org/docs/current/interactive/ddl-partitioning.html" rel="nofollow noreferrer">Partitioning</a>.</li>
<li><p>More RAM and settings that make use of it.</p>

<blockquote>
  <p>A virtual Debian 6.0 machine with 1GB of RAM</p>
</blockquote>

<p>is way below what you need.</p></li>
<li><p><a href="http://www.postgresql.org/docs/current/interactive/indexes-partial.html" rel="nofollow noreferrer">Partial indexes</a>, especially in connection with <strong>index-only scans</strong> of PostgreSQL 9.2.</p></li>
<li><a href="http://en.wikipedia.org/wiki/Materialized_view" rel="nofollow noreferrer"><strong>Materialized views</strong></a> of aggregated data. Obviously, you are not going to display 500K rows, but some kind of aggregation. You can compute that once and save results in a materialized view, from where you can retrieve data much faster.</li>
<li><p>If your queries are predominantly by parameter (like the example), you could use <a href="http://www.postgresql.org/docs/current/interactive/sql-cluster.html" rel="nofollow noreferrer"><strong><code>CLUSTER</code></strong></a> to physically rewrite the table according to an index:</p>

<pre><code>CLUSTER measure_val USING measure_val_param_id_idx
</code></pre>

<p>This way all rows for one parameter are stored in succession. Means fewer block to read and easier to cache. Should make the query at hand much faster. Or <code>INSERT</code> the rows in favorable order to begin with, to the same effect.<br>
Partitioning would mix well with <code>CLUSTER</code>, since you would not have to rewrite the whole (huge) table every time. As your data is obviously just inserted and not updated, a partition would stay "in order" after <code>CLUSTER</code>.</p></li>
<li><p>Generally, <strong>PostgreSQL 9.2</strong> should be great for you as its <a href="http://www.postgresql.org/docs/current/interactive/release-9-2.html#AEN110346" rel="nofollow noreferrer">improvements focus on performance with big data</a>.</p></li>
</ul>

### Answer ID: 12553004
<p>It seems from the numbers that you are being hit by timing overhead. You can verify this by using <a href="http://www.postgresql.org/docs/9.2/static/pgtesttiming.html" rel="nofollow">pg_test_timing</a> or adding <code>timing off</code> to your explain parameters (both are introduced in PostgreSQL version 9.2). I can approximately replicate your results by turning setting my clocksource to HPET instead of TSC.</p>

<p>With HPET:</p>

<pre><code> Nested Loop  (cost=8097.73..72850.98 rows=432000 width=12) (actual time=29.188..905.765 rows=432000 loops=1)
   Buffers: shared hit=56216
   -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual time=0.004..0.008 rows=1 loops=1)
         Filter: ((name)::text = 'param_01'::text)
         Rows Removed by Filter: 19
         Buffers: shared hit=1
   -&gt;  Bitmap Heap Scan on measurement_data_value  (cost=8097.73..68529.73 rows=432000 width=16) (actual time=29.180..357.848 rows=432000 loops=1)
         Recheck Cond: (fk_parameter_id = parameter.id)
         Buffers: shared hit=56215
         -&gt;  Bitmap Index Scan on measurement_data_value_idx_fk_parameter_id  (cost=0.00..7989.73 rows=432000 width=0) (actual time=21.710..21.710 rows=432000 loops=1)
               Index Cond: (fk_parameter_id = parameter.id)
               Buffers: shared hit=1183
 Total runtime: 1170.409 ms
</code></pre>

<p>With HPET and timing off:</p>

<pre><code> Nested Loop  (cost=8097.73..72850.98 rows=432000 width=12) (actual rows=432000 loops=1)
   Buffers: shared hit=56216
   -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual rows=1 loops=1)
         Filter: ((name)::text = 'param_01'::text)
         Rows Removed by Filter: 19
         Buffers: shared hit=1
   -&gt;  Bitmap Heap Scan on measurement_data_value  (cost=8097.73..68529.73 rows=432000 width=16) (actual rows=432000 loops=1)
         Recheck Cond: (fk_parameter_id = parameter.id)
         Buffers: shared hit=56215
         -&gt;  Bitmap Index Scan on measurement_data_value_idx_fk_parameter_id  (cost=0.00..7989.73 rows=432000 width=0) (actual rows=432000 loops=1)
               Index Cond: (fk_parameter_id = parameter.id)
               Buffers: shared hit=1183
 Total runtime: 156.537 ms
</code></pre>

<p>With TSC:</p>

<pre><code> Nested Loop  (cost=8097.73..72850.98 rows=432000 width=12) (actual time=29.090..156.233 rows=432000 loops=1)
   Buffers: shared hit=56216
   -&gt;  Seq Scan on parameter  (cost=0.00..1.25 rows=1 width=4) (actual time=0.004..0.008 rows=1 loops=1)
         Filter: ((name)::text = 'param_01'::text)
         Rows Removed by Filter: 19
         Buffers: shared hit=1
   -&gt;  Bitmap Heap Scan on measurement_data_value  (cost=8097.73..68529.73 rows=432000 width=16) (actual time=29.083..114.908 rows=432000 loops=1)
         Recheck Cond: (fk_parameter_id = parameter.id)
         Buffers: shared hit=56215
         -&gt;  Bitmap Index Scan on measurement_data_value_idx_fk_parameter_id  (cost=0.00..7989.73 rows=432000 width=0) (actual time=21.667..21.667 rows=432000 loops=1)
               Index Cond: (fk_parameter_id = parameter.id)
               Buffers: shared hit=1183
 Total runtime: 168.869 ms
</code></pre>

<p>So your slowness seems to be mostly caused by instrumentation overhead. However, selecting huge amounts of rows won't be extremely fast in PostgreSQL. If you need to do number crunching on large swathes of data it might be a good idea to structure your data so you can fetch it in larger chunks. (e.g. if you need to always process at least a days worth of data, aggregate all measurements for one day into an array)</p>

<p>In general, you have to have a idea of what your workload is going to be to do tuning. What is a win in one case might be a big loss in some other case. I recommend checking out <a href="http://www.postgresql.org/docs/9.2/static/pgstatstatements.html" rel="nofollow">pg_stat_statements</a> to figure out where your bottlenecks are.</p>

### Answer ID: 12545542
<p>I don't see how you relate a particular measured value with a particular combination of device, spot, and time. Am I missing something obvious?</p>

<p>Let's look at it a different way.</p>

<pre><code>CREATE TABLE measurement_data
(
  device_name character varying(16) NOT NULL,
  spot_id integer NOT NULL,
  parameter_id integer NOT NULL,
  t_stamp timestamp without time zone NOT NULL,
  value character varying(16) NOT NULL,
  CONSTRAINT measurement_data_pk PRIMARY KEY (device_name , spot_id , t_stamp , parameter_id ),
  CONSTRAINT measurement_data_fk_device FOREIGN KEY (device_name)
      REFERENCES device (name) MATCH FULL
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_fk_parameter FOREIGN KEY (parameter_id)
      REFERENCES parameter (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT measurement_data_fk_spot FOREIGN KEY (spot_id)
      REFERENCES spot (id) MATCH FULL
      ON UPDATE NO ACTION ON DELETE NO ACTION
);
</code></pre>

<p>(An even better name for this table is "measurements". Every table contains data.)</p>

<p>I'd expect much better performance on this kind of table. But I'd also expect any query that returns many, many rows to struggle with performance. (Unless the hardware and the network matches the task.)</p>

