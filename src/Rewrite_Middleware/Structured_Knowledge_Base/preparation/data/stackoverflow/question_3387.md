# Rebuilding fact tables with over 30 million rows takes over 1hr
[Link to question](https://stackoverflow.com/questions/78181120/rebuilding-fact-tables-with-over-30-million-rows-takes-over-1hr)
**Creation Date:** 1710774382
**Score:** 0
**Tags:** business-intelligence, sql-server-2019, large-data-volumes, fact-table
## Question Body
<p>I currently have one Microsoft SQL Server database (Enterprise) running on a VM with 32 GB RAM.</p>
<p>We take data from multiple sources, roughly 500k rows per day is imported into a table. These individual transactional rows are then used to rebuild several aggregated tables.</p>
<p>The transactional database table contains over 30 million rows. Every night after the latest rows are imported, we will drop and then rebuild one of the (history) tables which contains another 30 million rows, before making use of this table to then build several other tables. It will drop the table, rebuild using a <code>SELECT ... INTO</code> and then create non-clustered indexes.</p>
<p>This takes &gt; 1 hour and fries the VM and uses little CPU but all of the available memory.</p>
<p>I have tried rewriting the lengthy stored procedure to not rebuild the tables, and only use <code>MERGE</code> statements to insert or update only the records where a transaction has been received overnight. This is no quicker (and I have seen lots of documentation suggesting <code>MERGE</code> uses more resource, reads, writes, etc).</p>
<p>I am now at a loss on how to improve the performance of this after using Live Query Statistics to implement suggested indexes.</p>
<p>I have been looking at partitioning the large table &gt; 30 million rows and increasing the RAM to 64 GB.</p>
<p>When I run query statistics there are no other suggestions however it is extremely slow and sits on query progress of 100% for a long time despite the activity monitor suggesting that it has already moved onto the next query.</p>
<p>30% query cost relative to the batch was associated to inserting the index on the 30m row (history) table.</p>
<p>Are there any other suggestions?</p>
<p>Should I go back to using MERGE statements and only updating unique records that have been received overnight (rather than rebuilding the whole fact table)?</p>
<p>Any advice would be greatly received.</p>
<p>Improve performance of SQL fact table building following ETL process overnight involving &gt; 30 million rows.</p>

