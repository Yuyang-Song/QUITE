# Warehouse PostgreSQL database architecture recommendation
[Link to question](https://stackoverflow.com/questions/17685672/warehouse-postgresql-database-architecture-recommendation)
**Creation Date:** 1374004103
**Score:** 1
**Tags:** database, postgresql, architecture
## Question Body
<p><strong>Background:</strong></p>

<p>I am developing an application that allows users to generate lots of different reports. The data is stored in PostgreSQL and has natural unique group key, so that the data with one group key is totally independent from the data with others group key. Reports are built only using 1 group key at a time, so all of the queries uses "WHERE groupKey = X;" clause. The data in PostgreSQL updates intensively via parallel processes which adds data into different groups, but I don't need a realtime report. The one update per 30 minutes is fine.</p>

<p><strong>Problem:</strong></p>

<p>There are about 4 gigs of data already and I found that some reports takes significant time to generate (up to 15 seconds), because they need to query not a single table but 3-4 of them. </p>

<p>What I want to do is to reduce the time it takes to create a report without significantly changing the technologies or schemes of the solution. </p>

<p><strong>Possible solutions</strong></p>

<p>What I was thinking about this is:</p>

<ol>
<li><p>Splitting one database into several databases for 1 database per each group key. Then I will get rid of WHERE groupKey = X (though I have index on that column in each table) and the number of rows to process each time would be significantly less.</p></li>
<li><p>Creating the slave database for reads only. Then I will have to sync the data with replication mechanism of PostgreSQL for example once per 15 minutes (Can I actually do that? Or I have to write custom code)</p></li>
</ol>

<p>I don't want to change the database to NoSQL because I will have to rewrite all sql queries and I don't want to. I might switch to another SQL database with column store support if it is free and runs on Windows (sorry, don't have Linux server but might have one if I have to).</p>

<p><strong>Your ideas</strong></p>

<p>What would you recommend as the first simple steps?</p>

## Answers
### Answer ID: 17694380
<ol>
<li>Tune the report query. Use explain. Avoid procedure when you could do it in pure sql.</li>
<li>Tune the server; memory, disk, processor. Take a look at server config.</li>
<li>Upgrade postgres version. </li>
<li>Do vacuum.</li>
</ol>

<p>Out of 4, only 1 will require significant changes in the application.</p>

### Answer ID: 17687235
<p>Two thoughts immediately come to mind for reporting:</p>

<p>1). Set up some summary (aka "aggregate") tables that are precomputed results of the queries that your users are likely to run. Eg. A table containing the counts and sums grouped by the various dimensions. This can be an automated process -- a db function (or script) gets run via your job scheduler of choice -- that refreshes the data every N minutes.</p>

<p>2). Regarding replication, if you are using Streaming Replication (PostgreSQL 9+), the changes in the master db are replicated to the slave databases (hot standby = read only) for reporting.</p>

