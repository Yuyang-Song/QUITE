# Does normalization really hurt performance in high traffic sites?
[Link to question](https://stackoverflow.com/questions/2702665/does-normalization-really-hurt-performance-in-high-traffic-sites)
**Creation Date:** 1272067708
**Score:** 6
**Tags:** c#, performance, sql-server-2008, normalization, denormalization
## Question Body
<p>I am designing a database and I would like to normalize the database. In one query I will joining about 30-40 tables. Will this hurt the website performance if it ever becomes extremely popular? This will be the main query and it will be getting called 50% of the time. The other queries I will be joining about two tables. </p>

<p>I have a choice right now to normalize or not to normalize but if the normalization becomes a problem in the future I may have to rewrite 40% of the software and it may take me a long time. Does normalization really hurt in this case? Should I denormalize now while I have the time?</p>

## Answers
### Answer ID: 2702692
<p>Don't make early optimizations.  Denormalization isn't the only way to speed up a website.  Your caching strategy is also quite important and if that query of 30-40 tables is of fairly static data, caching the results may prove to be a better optimization.</p>

<p>Also, take into account the number of writes to the number of reads.  If you are doing approximately 10 reads for every insert or update, you could say that data is fairly static, hence you should cache it for some period of time.</p>

<p>If you end up denormalizing your schema, your writes will also become more expensive and potentially slow things down as well.  </p>

<p>Really analyze your problem before making too many optimizations and also wait to see where your bottlenecks in the system really as you might end up being surprised as to what it is you should optimize in the first place.</p>

### Answer ID: 2703028
<p>Maybe I missing something here. But if your architecture requires you to join 30 to 40 tables in a single query, ad that query is the main use of your site then you have larger problems.</p>

<p>I agree with others, don't prematurely optimize your site. However, you should optimize your architecture to account for you main use case. a 40 table join for a query run over 50% of the time is not optimized IMO.</p>

### Answer ID: 2702742
<p>Normalization can hurt performance. However this is no reason to denormalize prematurely.</p>

<p>Start with full normalization and then you'll see if you have any performance problems. At the rate you are describing (1000 updates/inserts per day) I don't think you'll run into problems unless the tables are huge.</p>

<p>And even if there are tons of database optimization options (Indexes, Prepared stored procedures, materialized views, ...) that you can use.</p>

### Answer ID: 2702717
<p>When performance is a concern, there are usually better alternatives than denormalization:</p>

<ul>
<li>Creating appropriate indexes and statistics on the involved tables</li>
<li>Caching</li>
<li>Materialized views (Indexed views in MS SQL Server)</li>
<li>Having a denormalized copy of your tables (used exclusively for the queries that need them), in addition to the normalized tables that are used in most cases (requires writing synchronization code, that could run either as a trigger or a scheduled job depending on the data accuracy you need)</li>
</ul>

### Answer ID: 2702681
<p>I quote: "normalize for correctness, denormalize for speed - and only when necessary"</p>

<p>I refer you to: <a href="https://stackoverflow.com/questions/293425/in-terms-of-databases-is-normalize-for-correctness-denormalize-for-performance">In terms of databases, is &quot;Normalize for correctness, denormalize for performance&quot; a right mantra?</a> </p>

<p>HTH.</p>

