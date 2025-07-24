# AWS Glue Spark Job Fails to Support Upper case Column Name with Double Quotes
[Link to question](https://stackoverflow.com/questions/58093109/aws-glue-spark-job-fails-to-support-upper-case-column-name-with-double-quotes)
**Creation Date:** 1569396002
**Score:** 3
**Tags:** pyspark, aws-glue, aws-glue-data-catalog, data-lake
## Question Body
<p>Problem Statement/Root Cause: We are using AWS Glue to load data from a production PostGress DB into AWS DataLake. Glue internally uses Spark job to move the data. Our ETL process is, however, failing as Spark only supports lowercase table column names and unfortunately, all our source PostGress table column names are in CamelCase and enclosed in double-quotes.</p>

<p>E.g. : Our Source table column name in the PostGress DB is "CreatedDate". The Spark job query is looking for createddate and is failing because it can't find the column name. So, the spark job query needs to look for exactly "CreatedDate" to be able to move data from the PostGress DB. This seems to be an inherent limitation of both Spark (as it only supports lowercase table column names) and PostGress (Column names that were created with double-quotes have to be double-quoted for the rest of their life).</p>

<p>Reference Links: 
<a href="https://docs.aws.amazon.com/athena/latest/ug/tables-databases-columns-names.html" rel="nofollow noreferrer">https://docs.aws.amazon.com/athena/latest/ug/tables-databases-columns-names.html</a>
<a href="https://stackoverflow.com/questions/20878932/are-postgresql-column-names-case-sensitive">Are PostgreSQL column names case-sensitive?</a></p>

<p>Solutions evaluated:
1. We will not be able to rename the column names from CamelCase to lowercase as that will necessitate a bigger change in all downstream systems.
2. We are trying to rewrite/tweak Glue's auto-generated Spark code to see if we can get it to work with double-quoted, non-lowercase source table column names.</p>

<p>Has anyone run into this issue before and have you tried to tweak the auto-generated Spark code to get it working?</p>

## Answers
### Answer ID: 58112408
<p><strong>Sandeep Fatangare</strong> thanks for you suggesting.</p>
<p>I am very new to AWS Glue I don't know whether I'm doing correctly. Please guide me if I'm wrong.</p>
<p>I try editing the script by navigating to</p>
<p>AWS Glue -&gt; Jobs and choose the failed Job script</p>
<p>In the details tab, it shows the location &quot;location mention in the job details is s3://aws-glue-assets-us-east-1/scripts/glueetl/jdbc_incremental.py&quot;.</p>
<p>And in <strong>Script Tab</strong> I start editing the script</p>
<p>previous :</p>
<pre><code>applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=self.get_mappings(),                                                                                      transformation_ctx=&quot;applymapping1_&quot; + self.source.table_name)
</code></pre>
<p>Edited :</p>
<pre><code>applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=self.get_mappings(),
                                           caseSensitive : Boolean = false, 
                                           transformation_ctx=&quot;applymapping1_&quot; + self.source.table_name)
</code></pre>
<p>And I faced 2 problems</p>
<ol>
<li>I cant able to save the edited script</li>
<li>And while running the script it told me workflow name is missing</li>
</ol>

### Answer ID: 58101183
<p>Solution 1: If you are using scala and glue dynamic frame, you can use <code>applyMapping()</code>. Default value for <code>caseSensitive</code> is true. Check <a href="https://docs.aws.amazon.com/glue/latest/dg/glue-etl-scala-apis-glue-dynamicframe-class.html#glue-etl-scala-apis-glue-dynamicframe-class-defs-applyMapping" rel="nofollow noreferrer">https://docs.aws.amazon.com/glue/latest/dg/glue-etl-scala-apis-glue-dynamicframe-class.html#glue-etl-scala-apis-glue-dynamicframe-class-defs-applyMapping</a> </p>

<p>Solution 2: if you are using pyspark dataframe in python, you can set conf:</p>

<pre><code>spark_session.sql('set spark.sql.caseSensitive=true')
</code></pre>

