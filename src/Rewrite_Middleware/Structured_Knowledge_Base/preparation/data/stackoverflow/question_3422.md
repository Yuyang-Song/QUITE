# Spark JDBC read results in row loss
[Link to question](https://stackoverflow.com/questions/79165375/spark-jdbc-read-results-in-row-loss)
**Creation Date:** 1730963770
**Score:** 1
**Tags:** oracle-database, apache-spark, amazon-s3, jdbc, aws-glue
## Question Body
<p>We're currently running into an issue with a spark job architecture which is used as an interface to import data sources from a corporate oracle data warehouse into Amazon s3.</p>
<p>The job contains no further processing logic except for a JDBC read which is followed immediately by a parquet write to s3.</p>
<p>Recently, and only by chance, we realized that somewhere in the processing pipeline of an ml workflow the row count wouldn't add up to an expected number and we were able to quickly track the issue down to this very import job.</p>
<p>After intensive investigation and testing we were able to prove that the row loss occurs during the partitioned JDBC read operation and alas, goes completely unnoticed if not secured by custom validation.</p>
<p>The spark job in this case is supposed to read about 70 million rows with 9 columns. It uses 32 partitions to query the data with a JDBC fetch size of 50k which should result in 32 concurrent JDBC connections that are used to query chunks of 50k rows per round trip for each partition.</p>
<p>This is the side effect we run into:</p>
<ul>
<li>the job succeeds and writes it's results to s3</li>
<li>memory and cpu consumption are completely fine according to the AWS provided metrics, in fact, the job was actually rather over then under provisioned</li>
<li>however, the row count written to s3 lacks a couple of thousand rows that somehow just get lost during the read operation</li>
<li>running the job multiple times always results in a row loss, but the total row loss varies in it's number from run to run but generally occurs randomly distributed across a variety of different partitions</li>
</ul>
<p>We've set up a glue crawler to query the partition results via athena to prove this issue.</p>
<p>The spark job runs on AWS Glue 4.0 with spark 3.3.0 and uses the amazon provided oracle JDBC driver, which according to <a href="https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-jdbc-home.html" rel="nofollow noreferrer">AWS</a> is provided in version 21.7 (the patch/micro version isn't documented by AWS).</p>
<p>If we remove all abstraction layers that simplify testing or are used to query username and password secrets from our secrets manager and stuff like that, the job logic itself could be reduced to a single entrypoint module as simple as this:</p>
<pre class="lang-py prettyprint-override"><code>from pyspark import StorageLevel
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

sql = &quot;&quot;&quot;
select 
    ora_hash(&lt;some integer id&gt;, 31) as bucket
    , col2
    , col3
    ...
from
    schema.table
    left join ...
where
    ...
&quot;&quot;&quot;


def read() -&gt; DataFrame:
    spark = SparkSession.builder.getOrCreate()

    return (
        spark.read.format(&quot;jdbc&quot;)
        .option(&quot;mode&quot;, &quot;FAILFAST&quot;)  # this has apparently no impact
        .option(&quot;driver&quot;, &quot;oracle.jdbc.OracleDriver&quot;)
        .option(&quot;url&quot;, &quot;&lt;url&gt;&quot;)
        .option(&quot;user&quot;, &quot;&lt;user&gt;&quot;)
        .option(&quot;password&quot;, &quot;&lt;password&gt;&quot;)
        .option(&quot;fetchsize&quot;, 50_000)
        .option(&quot;dbtable&quot;, f&quot;({sql}) tmp&quot;)
        .option(&quot;partitionColumn&quot;, &quot;bucket&quot;)
        .option(&quot;lowerBound&quot;, 0)
        .option(&quot;upperBound&quot;, 31)
        .option(&quot;numPartitions&quot;, 32)
        .load()
        .persist(StorageLevel.MEMORY_AND_DISK)
    )


def write(df: DataFrame) -&gt; None:
    df.write.mode(&quot;overwrite&quot;).parquet(&quot;s3://&lt;bucket-id&gt;/&lt;path&gt;&quot;)


def main() -&gt; None:
    write(read())

</code></pre>
<p>This type of job architecture is already used on production for about 3 years now. The issue however only surfaced recently and so far, alas, without us being able to pin the root cause of this issue.</p>
<p>From an observability perspective, the oracle database is a complete black box to us as we don't have access to any database logs, metrics or system tables/views. The JDBC driver is provided by AWS and the only thing we can really modify is the couple of lines spark code above. Not much of a surface for a bug fix alas.</p>
<p>The following three action items describe what we've tried and/or achieved so far.</p>
<h1>Action Item 1: Check for malformed data</h1>
<p>Our first guess was about malformed data which somehow either causes issues in spark or the JDBC driver.</p>
<p>So we essentially did sort of a binary search, dividing the total data set into 8 chunks and processing each chunk in separate sequentially executed spark jobs.</p>
<p>Alas, in this case, the row counts as well as other business checks on the exported datasets would align 1:1 with the data inside the oracle database.</p>
<p>Hmrpf.. Doesn't appear to be a data quality issue.</p>
<h1>Action Item 2: Fail on row loss</h1>
<p>Albeit that doesn't fix the issue yet, we definitely wanted to rewrite the job such that the row loss doesn't go unnoticed. The logic can be simplified to something like this:</p>
<pre class="lang-py prettyprint-override"><code>from pyspark import StorageLevel
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

sql = sql = &quot;&quot;&quot;
select 
    ora_hash(&lt;some integer id&gt;, 31) as bucket
    , col2
    , col3
    ...
from
    schema.table
    left join ...
where
    ...
&quot;&quot;&quot;


def compute_expected_row_count() -&gt; int:
    spark = SparkSession.builder.getOrCreate()
    query = f'select count(*) as &quot;row_count&quot; from ({sql}) data'
    df = (
        spark.read.format(&quot;jdbc&quot;)
        .option(&quot;mode&quot;, &quot;FAILFAST&quot;)
        .option(&quot;driver&quot;, &quot;oracle.jdbc.OracleDriver&quot;)
        .option(&quot;url&quot;, &quot;&lt;url&gt;&quot;)
        .option(&quot;user&quot;, &quot;&lt;user&gt;&quot;)
        .option(&quot;password&quot;, &quot;&lt;password&gt;&quot;)
        .option(&quot;dbtable&quot;, f&quot;({query}) tmp&quot;)
        .load()
    )
    return int(df.collect()[0].asDict()[&quot;row_count&quot;])


def read() -&gt; DataFrame:
    spark = SparkSession.builder.getOrCreate()

    df = (
        spark.read.format(&quot;jdbc&quot;)
        .option(&quot;mode&quot;, &quot;FAILFAST&quot;)
        .option(&quot;driver&quot;, &quot;oracle.jdbc.OracleDriver&quot;)
        .option(&quot;url&quot;, &quot;&lt;url&gt;&quot;)
        .option(&quot;user&quot;, &quot;&lt;user&gt;&quot;)
        .option(&quot;password&quot;, &quot;&lt;password&gt;&quot;)
        .option(&quot;fetchsize&quot;, 50_000)
        .option(&quot;dbtable&quot;, f&quot;({sql}) tmp&quot;)
        .option(&quot;partitionColumn&quot;, &quot;bucket&quot;)
        .option(&quot;lowerBound&quot;, 0)
        .option(&quot;upperBound&quot;, 31)
        .option(&quot;numPartitions&quot;, 32)
        .load()
        .persist(StorageLevel.MEMORY_AND_DISK)
    )

    expected_row_count = compute_expected_row_count()
    actual_row_count = df.count()

    if actual_row_count != expected_row_count:
        raise RuntimeError(
            f&quot;DataFrame was expected to contain '{expected_row_count}' rows &quot;
            f&quot;but only contains '{actual_row_count}' rows&quot;
        )
    return df


def write(df: DataFrame) -&gt; None:
    df.write.mode(&quot;overwrite&quot;).parquet(&quot;s3://&lt;bucket-id&gt;/&lt;path&gt;&quot;)


def main() -&gt; None:
    write(read())

</code></pre>
<p>This way, the job at least fails early if we run into a row loss and doesn't go by unnoticed. But obviously, the job would now continuously fail on each attempt.</p>
<p>Hmrpf.. At least no unnoticed data loss, but obviously still unacceptable</p>
<h1>Action Item 3: reduce read concurrency</h1>
<p>This is somewhat funny, but it's so far also the only thing we tried which resulted in a successful data extraction.</p>
<p>By reducing the read concurrency from 32 to 8 partitions, the job mostly executes it's control flow just fine without any row loss. However, sometimes, the row loss still occurs.</p>
<p>Apparently, the row loss risk increases as the amount of JDBC connections increase, but we still don't really understand why.</p>
<p>Hmrpf.. At least we where finally able to make the job somewhat consistently succeed without a row loss, but we still haven't been able to figure out the root cause.</p>
<p>If anyone ran into a similar issue in the past and could provide us with some hints as to what's going on here, that would be of great help.</p>
<p>Thanks a lot and happy hacking!</p>
<p>In case that's of any help, here are some of the spark configuration options mostly managed by AWS though:</p>
<pre class="lang-json prettyprint-override"><code>{
    &quot;spark.driver.cores&quot;: &quot;8&quot;,
    &quot;spark.driver.extraClassPath&quot;: &quot;/tmp:/opt/amazon/conf:/opt/amazon/glue-manifest.jar&quot;,
    &quot;spark.driver.extraJavaOptions&quot;: &quot;-XX:+IgnoreUnrecognizedVMOptions --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED&quot;,
    &quot;spark.driver.memory&quot;: &quot;20g&quot;,
    &quot;spark.executor.cores&quot;: &quot;8&quot;,
    &quot;spark.executor.extraClassPath&quot;: &quot;/tmp:/opt/amazon/conf:/opt/amazon/glue-manifest.jar&quot;,
    &quot;spark.executor.extraJavaOptions&quot;: &quot;-XX:+IgnoreUnrecognizedVMOptions --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED&quot;,
    &quot;spark.executor.id&quot;: &quot;driver&quot;,
    &quot;spark.executor.memory&quot;: &quot;20g&quot;,
    &quot;spark.sql.legacy.parquet.int96RebaseModeInWrite&quot;: &quot;LEGACY&quot;,
    &quot;spark.sql.parquet.fs.optimized.committer.optimization-enabled&quot;: &quot;true&quot;,
    &quot;spark.sql.parquet.output.committer.class&quot;: &quot;com.amazon.emr.committer.EmrOptimizedSparkSqlParquetOutputCommitter&quot;,
    &quot;spark.sql.shuffle.partitions&quot;: &quot;32&quot;
}
</code></pre>
<h1>Additional Notes</h1>
<p>I'm not sure if this contributes to the issue, but it might be worth noting that the job architecture exposes an interface to run a sequence of sql quality checks on the oracle database. So it is quiet common, that the data structures in oracle are queried with a sequence of quality checks before the actual read operation is executed. The quality checks are also issue via spark read JDBC.</p>
<p>Perhaps this results in some sort of awkward caching issues inside the oracle database? But alas, as mentioned above, we cannot really analyze what's going on inside the database.</p>

## Answers
### Answer ID: 79208226
<p>see that your jdbc driver has the correct version. you can query your own version if connected:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT Client_version
FROM V$SESSION
JOIN v$session_connect_info USING (SID, SERIAL#)
WHERE AUDSID = Sys_Context('USERENV', 'SESSIONID')
</code></pre>
<p>and the server version</p>
<pre class="lang-sql prettyprint-override"><code>SELECT VERSION_FULL FROM dba_registry
 WHERE comp_id = 'CATALOG'
</code></pre>
<p>if this does not match, download an appropriate jdbc driver version <a href="https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html" rel="nofollow noreferrer">from oracle</a>
and use it <a href="https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-jdbc-home.html#aws-glue-programming-etl-jdbc-custom-driver" rel="nofollow noreferrer">as documented by aws</a></p>

