# Can I use hadoop instead of other database for fast SQL manipulations?
[Link to question](https://stackoverflow.com/questions/24271723/can-i-use-hadoop-instead-of-other-database-for-fast-sql-manipulations)
**Creation Date:** 1403032780
**Score:** 0
**Tags:** sql, hadoop, hbase
## Question Body
<p>I'm not very familiar with Hadoop nor an expert in database, I just want to know if by using Hadoop, HBase or Pig, Hive (together or separately), I can improve the execution speed for SQL queries of "select" or "insert".</p>

<p>The thing is, originally the data was stored on Microsoft SQL and other tools for intensive aggregation things, but the speed is very slow, for datasets, maybe GB size, it takes minutes to return the results (select for example).</p>

<p>I'm thinking if i can put the data on Hadoop HDFS and using some tools provided by Apache together with MR that I can rewrite the SQL (select, insert functions in No_SQL pattern but rather like functional, or more programming oriented pattern) that I can improve the processing speed?</p>

<p>And suggestions about how to do this or whether I'm in the right direction?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 24356643
<p>The entire Hadoop ecosystem (including HDFS, Hive and HBase) is not designed for fast interactive/real time queries with less than few minutes responses. Instead Hadoop is well suited for batch programming (more than few minutes responses) with very big datasets (think about terabytes or petabytes).</p>

<p>If you just have a few Giga bytes dataset (wich is considered a small dataset in the Hadoop world) you better improve the performance of your queries remaining in the SQL world. For example if you are joining two or more tables you can denormalize your data so that you can avoid the join.</p>

<p>That said, there is an initiative called <a href="http://hortonworks.com/labs/stinger/" rel="nofollow">Stinger</a> from Microsoft and Hortonworks which tries to improve the performance of Hive in order to make queries interactive. The introduced a tool called <a href="http://hortonworks.com/hadoop/tez/" rel="nofollow">Tez</a> which make Hive 10 to 100 times faster.</p>

<p>My suggestion would be to try the performance of hadoop by using a <a href="http://hortonworks.com/products/hortonworks-sandbox/" rel="nofollow">Hortonworks sandbox VM</a> and test the performance of hive on your laptop. If you use the version 2.1, it comes already with Tez and the latest version of Hive.</p>

<p>You have to remember that with the Hortonworks sandbox you are using a cluster made of just one node. If you want improve the performance of the Hive query you can distribute your dataset and then the processing to more than one node.</p>

<p>Only with a real test with a sql database and hadoop you can see which solution is performing better. My guess would be that with such a small dataset and comparing your SQL database with Hive on just one node, you can still performs better with a SQL database. But with a bigger dataset and by using more that one node, the performance of the SQL database starts to degrade in favor of the hadoop solution.</p>

<p>P.S: I am a Hortonworks certified developer and instructor.</p>

