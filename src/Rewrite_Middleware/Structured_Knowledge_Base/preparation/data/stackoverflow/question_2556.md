# Approach for joining a lot of dimensions in Spark
[Link to question](https://stackoverflow.com/questions/40057008/approach-for-joining-a-lot-of-dimensions-in-spark)
**Creation Date:** 1476521499
**Score:** 2
**Tags:** apache-spark, apache-spark-sql
## Question Body
<p>I need help on joining dimensions information with transactional data with Spark. </p>

<p>I have data stored in parquet files with about 200 columns. Around 100 of them are  dimensions' ids. In total dimensions values uses about 200GB in relational db and values changes over time quite rapidly. </p>

<p>How can I join these dimensions to the transactional data during aggregations. Aggregating scripts are dynamic and they can vary, for example there can be 20 dimensions used or just one. I can load all dimensions values to hdfs, and make joins. But making lot of joins is slow. </p>

<p>With Hive I used to use custom udfs which were retrieving from sql database dimension value for particular dimension id. There were local Guava caches used inside udfs, so every mapper/reducer offten used to make only one request if value count doesnt exceed cache limit. Using these udf without any modifications in Spark dramatically decreased performance of query. I can try to rewrite it with spark udfs, but I don't know is it worth even trying? May be this approach is not suitable for spark.  </p>

<p>What is the common approach for doing this with spark? </p>

