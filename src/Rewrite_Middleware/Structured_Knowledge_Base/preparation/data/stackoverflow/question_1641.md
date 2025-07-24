# Peoplesoft queries - performance
[Link to question](https://stackoverflow.com/questions/2463881/peoplesoft-queries-performance)
**Creation Date:** 1268842311
**Score:** 2
**Tags:** oracle-database, peoplesoft
## Question Body
<p>I'm facing a problem with PeopleSoft queries (using Oracle backend database): when a rather complex query involving multiple records is set off by a user, PS does an enforced join of security records, thus producing SQL like this:  </p>

<blockquote>
  <p>select .... from<br>
  ps_job a, PS_EMPL_SRCQRY a1, ps_table2 b, ps_sec_rcd2 b1, ps_table3 c, ps_sec_rcd3 c1<br>
  where (...security joins a->a1, b->b1, c->c1...) and (...joins of a, b and c...) and<br>
  a.setid_dept = 'XYZ';  </p>
</blockquote>

<p>(let's assume the last condition has a high selectivity and there is an index on the column)
Obviously, due to the arrangement of the conditions, first a huge join is created, written to the temp segment, and when the last condition is finally applied, only a small subset is selected. A query formulated in this way is very likely to hit the preset timeout of the APPSRV, and even of the QRYSRV. When writing the query manually, I would rather move the most selective condition to the start, thus limiting the amount of the data being handled, to a considerable level.<br>
Any ideas on how to make PS behave like this? Actually, already rewriting "Oracle-styled" SQL to ANSI SQL seems to accelerate the queries - however, PS writes Oracle-style queries...</p>

<p>Thanks in advance<br>
DBa</p>

## Answers
### Answer ID: 10562638
<p>Apart from what Grant had suggested, another way would be to create views on the tables that the user would query and perform normal joins.</p>

<p>For the above you will have to - 
1. Create views for each of the records that would be used in the query.
2. Add the views to the query security tree.
3. Use the views in the PS query. This would perform the normal joins on the views and there would be no security records in the joins.</p>

<p>To enforce user level security on the data, you could have another security view and join it to the final query, and have a condition in the where clause checking the currently logged in user.</p>

<p>This way you would have a fixed number of views to create and not a view for each user query.</p>

### Answer ID: 2480920
<p>The only fix I know of to force it to do the joins the way it should, instead of the way it does (and avoid the dreaded Merge Join Cartesian) is to create a view that does the join correctly.</p>

<ul>
<li>Create a record with the correct fields.   </li>
<li>Make it type SQL view.  </li>
<li>Paste in your SQL that now works.   </li>
<li>Add it to the query security tree.   </li>
<li>Refresh the security cache.</li>
</ul>

