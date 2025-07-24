# Partitioning on a UUID in Postgres 12 or 13
[Link to question](https://stackoverflow.com/questions/66847389/partitioning-on-a-uuid-in-postgres-12-or-13)
**Creation Date:** 1616977319
**Score:** 3
**Tags:** sql, postgresql, database-design, uuid, partitioning
## Question Body
<h2>Problem</h2>
<p>I've been asked to copy a fair bit of data to Postgres in a new table. The data contains assembly component lists, simplified in the table definition below:</p>
<pre><code>CREATE TABLE IF NOT EXISTS assembly_item (
    id               uuid       NOT NULL DEFAULT  NULL,
    assembly_id.     uuid.      NOT NULL DEFAULT  NULL,
    done_dts         timestamp  NOT NULL DEFAULT 'epoch', 

CONSTRAINT assembly_item_pk
    PRIMARY KEY (id) 
);
</code></pre>
<p>There are dozens of attributes in the original, and a few hundred million rows at the moment. These records are spread across several installations, and are not stored in Postgres locally. Insertions on this table add up quickly, and it's going to grow to 1B rows within the year, is the guess. Date is rarely updated, and never deleted. (It could happen in time, but not often.) The same <code>id</code> is <em>never</em> duplicated with different <code>assembly_id</code> values. So, unique at the partition level on <code>id</code> is safe. The goal here is to offload this data onto Postgres, and leave only very recent data in a cache on the local servers.</p>
<p>This looks like a natural candidate for partitioning, and I'm looking for some guidance on a sensible strategy. You can see from the simplified structure that we've got a unique row <code>id</code>, a parent <code>assembly_id</code>, and a timestamp. I've looked at the existing queries in the original database, and the main search field is <code>assembly_id</code>, the parent record identifier. The cardinality between <code>assembly</code> and <code>assembly_item</code> is around 1:200.</p>
<p>In order to make partitioning most useful, it seems like the data needs to be split based on a value that enables the query planner to prune out partitions intelligently. I've thought of a few ideas, but don't have the 200M rows to test agains yet. In the meantime, what I'm considering is:</p>
<ul>
<li><p>Partition by month using either <code>RANGE</code>, or by <code>LIST</code> on <code>YYYY-MM</code> of the <code>done_dts</code>. Rewrite all of the queries to scope by date range.</p>
</li>
<li><p>Partition by <code>HASH</code> against the first two characters of <code>assembly_id::text</code>, giving me 256 partitions with fairly equal sizes. I think that this lets us search on <code>assembly_id</code> and prune out many partitions that won't have matches, but it looks pretty weird when I set it up.</p>
</li>
</ul>
<p>I appreciate that I'm asking a somewhat speculative question, all I'm hoping for here are some pointers that might make my first attempt more successful. Once I've got a bit data set, I can experiment more directly.</p>
<p>I've included experimental setup code, with only a sampling of the partitions listed for brevity.</p>
<h2>Sample setup using a <code>LIST</code> partition</h2>
<pre><code>------------------------------------
-- Define table partitioned by list
------------------------------------
-- Could alternatively use RANGE here to partition by month.

BEGIN;

-- Drop parent table, if they exists.
-- This destroys ALL partitions automatically, even without a CASCADE clause.
DROP TABLE IF EXISTS assembly_item_list CASCADE;

CREATE TABLE IF NOT EXISTS assembly_item_list (
    id                              uuid          NOT NULL DEFAULT NULL,
    assembly_id                     uuid          NOT NULL DEFAULT NULL,
    assembly_done_dts               timestamp     NOT NULL DEFAULT 'epoch', -- Copied in from assembly.done_dts when rows are pushed to Postgres.
    year_and_month                  citext        NOT NULL DEFAULT NULL,    -- YYYY-MM from assembly_done_dts, calculated in insert function. Can't use a generated column as a partition key.

-- Reminder: id values come from the various source tables in IB. The upsert writes over matches ON CONFLICT with this ID.
-- Note: You *must* include the partition key in the primary key. It's a rule.
CONSTRAINT assembly_item_list_pk
    PRIMARY KEY (year_and_month, id) 
) PARTITION BY LIST (year_and_month);

-- Previous year partitions built here...

-- Build out 2021 completely.
CREATE TABLE assembly_item_list_2021_01 partition of assembly_item_list HASH (assembly_id) ('2021-01');
CREATE TABLE assembly_item_list_2021_02 partition of assembly_item_list HASH (assembly_id) ('2021-02');
-- etc.

-- In case I screw up at the end of the year....
CREATE TABLE assembly_item_list_default partition of assembly_item_list default; 

COMMIT; 
</code></pre>
<h2>Sample setup using a <code>HASH</code> partition.</h2>
<pre><code>------------------------------------
-- Define table partitioned by hash
------------------------------------

BEGIN;

-- Drop parent table, if they exists.
-- This destroys ALL partitions automatically, even without a CASCADE clause.
DROP TABLE IF EXISTS assembly_item_hash CASCADE;

CREATE TABLE IF NOT EXISTS assembly_item_hash (
    id                              uuid          NOT NULL DEFAULT NULL,
    assembly_id                     uuid          NOT NULL DEFAULT NULL,
    assembly_done_dts               timestamp     NOT NULL DEFAULT 'epoch', -- Copied in from assembly.done_dts when rows are pushed to Postgres.
    partition_key                   text          NOT NULL DEFAULT NULL,    -- '00', '0A', etc. Populated in a BEFORE INSERT trigger on the partition. Can't use a generated column as a partition key, can't use a column reference in DEFAULT. 

-- Reminder: id values come from the various source tables in IB. The upsert writes over matches ON CONFLICT with this ID.
-- Note: You *must* include the partition key in the primary key. It's a rule.
CONSTRAINT assembly_item_hash_pk
    PRIMARY KEY (partition_key, id) 
) PARTITION BY HASH (partition_key);

-----------------------------------------------------
-- Create trigger function to populate partition_key
-----------------------------------------------------
-- The partition key is a two-character hex string, like '00', '3E', and so on.
CREATE OR REPLACE FUNCTION set_partition_key()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.partition_key = UPPER(LEFT(NEW.assembly_id, 2));
        RETURN NEW;
END;
$$ language plpgsql IMMUTABLE; -- I don't think that I need to worry about IMMUTABLE here. 01234567890ABCDEF shouldn't break. 

-----------------------------------------------------
-- Build partitions
-----------------------------------------------------
-- Note: Have to assign triggers to partitions individually.
-- Seems that it would be easier to add the logic to my central insert function.

CREATE TABLE assembly_item_hash_00 partition of assembly_item_hash FOR VALUES WITH (modulus 256, remainder 0);
CREATE TRIGGER set_partition_key_trigger_00
    BEFORE INSERT OR UPDATE ON assembly_item_hash_00
    FOR EACH ROW
    EXECUTE PROCEDURE set_partition_key();

CREATE TABLE assembly_item_hash_01 partition of assembly_item_hash FOR VALUES WITH (modulus 256, remainder 1);
CREATE TRIGGER set_partition_key_trigger_01
    BEFORE INSERT OR UPDATE ON assembly_item_hash_01
    FOR EACH ROW
    EXECUTE PROCEDURE set_partition_key();
    
-- And so on for all 256 partitions.

COMMIT; 
</code></pre>
<p>Any advice? Really, anything that comes to mind?</p>

## Answers
### Answer ID: 66848699
<p>Whether date or a UUID-hash will be the better partition key, I cannot say.
But I can say this: either of your solutions can be more efficient.</p>
<h2>Hash partitioning based on <code>uuid</code></h2>
<p>Your plan to add a partition key column and populate it with a trigger function is very inefficient. And unnecessary. (Issues with the trigger function itself aside.)</p>
<p>There seems to be a misunderstanding. You have a comment:</p>
<blockquote>
<p>-- Note: You <em>must</em> include the partition key in the primary key. It's a rule.</p>
</blockquote>
<p>Not exactly. <a href="https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-LIMITATIONS" rel="noreferrer">The manual:</a></p>
<blockquote>
<p>Unique constraints (and hence primary keys) on partitioned tables must
include all the partition key columns. This limitation exists because
the individual indexes making up the constraint can only directly
enforce uniqueness within their own partitions; therefore, the
partition structure itself must guarantee that there are not
duplicates in different partitions.</p>
</blockquote>
<p>Partition key <em><strong>columns</strong></em>. Not partition keys.<br />
A setup with hash partitioning on <code>(assembly_id)</code> works with a PK on the same column. Like this:</p>
<pre class="lang-sql prettyprint-override"><code>CREATE TABLE IF NOT EXISTS assembly_item_hash (
  assembly_id       uuid      NOT NULL
, id                uuid      NOT NULL
, assembly_done_dts timestamp NOT NULL DEFAULT 'epoch'
, PRIMARY KEY (assembly_id, id)
) PARTITION BY HASH (assembly_id);

CREATE TABLE assembly_item_hash_000 PARTITION OF assembly_item_hash FOR VALUES WITH (MODULUS 256, REMAINDER 0);
CREATE TABLE assembly_item_hash_001 PARTITION OF assembly_item_hash FOR VALUES WITH (MODULUS 256, REMAINDER 1);
-- etc.
</code></pre>
<p><em><strong>Much</strong></em> simpler.</p>
<p>The only downside: the PK index is a larger, <code>uuid</code> occupies 16 bytes.</p>
<p>If that's an issue, you might fall back to that generated <code>partition_key</code> you had in mind. With a trigger per partition. (Ugh, the overhead!) But make the column <code>integer</code> instead of <code>text</code>, and use the <em>much</em> more efficient built-in hash function <code>uuid_hash()</code>. That's the function used for hash partitioning internally. But now we use it explicitly and go for <code>LIST</code> partitioning:</p>
<pre class="lang-sql prettyprint-override"><code>CREATE TABLE IF NOT EXISTS assembly_item_hash (
  id                uuid      NOT NULL
, assembly_id       uuid      NOT NULL
, partition_key     int4      NOT NULL
, assembly_done_dts timestamp NOT NULL DEFAULT 'epoch'
, PRIMARY KEY (partition_key, id)
) PARTITION BY LIST (partition_key);
</code></pre>
<p>Adds 4 bytes to each table row, saves 12 bytes from each index item - <em>in theory</em>. Due to alignment padding you lose another 4 bytes in table and index, ending up with the same total space on disk as before (roughly - table and index bloat can differ).
<em>Unless</em>  &quot;column tetris&quot; allows you to fit in that column more efficiently, to win up to 8 bytes per row total ... See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/2966524/calculating-and-saving-space-in-postgresql/7431468#7431468">Calculating and saving space in PostgreSQL</a></li>
</ul>
<h2>List partitioning based on <code>timestamp</code></h2>
<p>Don't use <code>citext</code>. Needless complication.</p>
<p>Use an integer number for YYYY-MM instead. Smaller, faster. I suggest this base function:</p>
<pre class="lang-sql prettyprint-override"><code>CREATE FUNCTION f_yyyymm(timestamp)
   RETURNS int
   LANGUAGE sql PARALLEL SAFE IMMUTABLE AS
'SELECT (EXTRACT(year FROM $1) * 100 + EXTRACT(month FROM $1))::int';
</code></pre>
<p>See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/15169410/how-do-you-do-date-math-that-ignores-the-year/15179731#15179731">How do you do date math that ignores the year?</a></li>
</ul>

