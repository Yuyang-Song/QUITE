# SQL Server - Non-Unique Clustered Index Optimization
[Link to question](https://stackoverflow.com/questions/50065980/sql-server-non-unique-clustered-index-optimization)
**Creation Date:** 1524843905
**Score:** 1
**Tags:** sql-server, indexing
## Question Body
<p>We are moving an existing company desktop application to the cloud. I've been doing a lot of the database work and I have been optimizing them for appropriate indexes to maintain responsiveness as needed.</p>

<p>I was trying to optimize a couple tables and couldn't get the indexes to behave on all the calls i wanted them too so tried a non-unique cluster key on a temp table to see if it would give me better numbers since 'they would have disk locality, so it should be able to find them with sequential read rather than repeated random reads'. </p>

<p>I have 2 tables of concern that will definitely account for the majority of traffic, but the problem is the same. We expect millions to tens of millions of records in our user settings table. Our legacy software I have confirmed will be syncing ~1300-1500 configuration options per user into the database. Expect a table size of at least ~40-50 million rows.</p>

<p>My initial design of the table was this </p>

<pre><code>    CREATE TABLE dbo.Settings
    (
       SettingID BIGINT PRIMARY KEY NOT NULL IDENTITY(1,1),
       CustomerID INT NOT NULL,
       SettingTypeID INT NOT NULL
       .... other rows
    )

CREATE NONCLUSTERED INDEX [INDEX_NAME] ON dbo.Settings(CustomerID);
</code></pre>

<p>I think a better optimization is</p>

<pre><code>CREATE TABLE dbo.Settings
(
   CustomerID INT NOT NULL,
   SettingTypeID INT NOT NULL,
   .... other rows
)

CREATE CLUSTERED INDEX [INDEX_NAME] ON dbo.TRSettings(CustomerID);
</code></pre>

<p>All queries for product will be of the form, with maybe some sort of additional where condition like the specific settings I want for a given page. </p>

<pre><code>SELECT * FROM dbo.Settings WHERE CustomerID=@CustomerID ...
</code></pre>

<p>From profiling the selects seems to be 5-50x faster, averaging about 25-30x faster. Since it can do a range scan rather than repeated lookups from the nonclustered index.</p>

<p>For some reason inserts are reading the same to 50% faster in some of my tests (my guess is it has to rebuild the nonclustered index and the write to the actual table).</p>

<p>Brought it up to our product lead and the current consensus seems to be 'we will throw more hardware at it if needed' since we'd have to spend about half a day rewriting some code to work (pretty positive new table wouldn't work with entity framework or can you access the uniquifier hidden column?), but for my knowledge are there any gotcha's I'm unaware of? It seems like for customer records where you'll often be indexing multiple numbers of the items (ie a users settings) its best to have an index like this which approximates NoSQL clustering so you can guarantee disk locality. I'm just not familiar enough with insert performance to see if there would be unexpected issues with tree rebuilding.</p>

