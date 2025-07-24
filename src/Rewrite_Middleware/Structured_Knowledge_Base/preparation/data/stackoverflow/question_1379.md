# Convert LOTS of identical MySQL tables into ONE and lots of VIEWs that point to it?
[Link to question](https://stackoverflow.com/questions/7350566/convert-lots-of-identical-mysql-tables-into-one-and-lots-of-views-that-point-to)
**Creation Date:** 1315495643
**Score:** 4
**Tags:** mysql, view, innodb, myisam
## Question Body
<p>I'm running a pretty big deployment of WPMU (Wordpress Multi-User, Wordpress Multisite) that uses 4096 databases and 100k+ tables (with a lot of overlap in what schema is concerned, obviously).</p>

<p>Basically it's the same 20-some tables replicated over and over again for each and every blog, some of them empty, others containing a few to a few hundred rows.</p>

<p>My plan (that saves lots of headaches but may prove inefficient) is to merge all same-schema tables into a few big-ish InnoDB tables and replace the old ones with MySQL VIEWs that point to them, rewriting the queries so that the relevant rows are returned (store the old table name in a new column and then using the view to add the column to the query WHERE clause).</p>

<p>The question is: would this provide ANY kind of improvement in what performance is concerned? (key buffer efficiency, table cache efficiency, indexing) or is this just snake oil and I should resort to a more drastic approach of rewriting the app in such a way that i don't need VIEWs but the queries go straight to the big InnoDB tables?</p>

## Answers
### Answer ID: 7352552
<p>I would recommend against doing the table merge you're thinking of.  </p>

<p>Consider some of the downsides to merging the tables:</p>

<ul>
<li>Index data structures for the merged tables will be larger and deeper, and therefore less efficient.</li>
<li>Blogs that accumulate a lot of data but then go idle still contribute to the overall size of the tables and indexes, and therefore make queries take longer.</li>
<li>Harder to back up and restore an individual blog.</li>
<li>Harder to move an individual blog to another database server if you want to scale out.</li>
<li>Harder to use SQL privileges to restrict access for a given blog (though you could apply SQL privileges to the views).</li>
<li>Harder to add custom features that include schema changes for a given blog.</li>
</ul>

<p>Using views or not using views doesn't affect the above issues positively or negatively.  In MySQL at least, a view is basically just a query rewrite at runtime, it's not going to use indexes any better or worse than querying the base tables directly.</p>

<p>I once spoke with the database architect for Wordpress.com.  They host millions of Wordpress blogs on <strike>dozens</strike> hundreds of physical servers.  In their early days, they started out with the data for all blogs merged into the same tables, but they found the operational difficulties became too great as they grew.  Now they host each blog in a separate database.</p>

