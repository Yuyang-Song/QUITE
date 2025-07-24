# Not equal vs IN in AWS Redshift
[Link to question](https://stackoverflow.com/questions/78228296/not-equal-vs-in-in-aws-redshift)
**Creation Date:** 1711489040
**Score:** -1
**Tags:** performance, amazon-redshift, query-optimization
## Question Body
<p>usually iit is better to use IN as not equal in Oracle or another SQL databases. The optimiser could rewrite the query to use the index for scanning the values.</p>
<p>I am curious how can it affect the performance cause there is no classic index on a column like in Oracle.</p>
<p>Does it affect the performance in Redshift if using &lt;&gt; 1 instead of IN ( 2,3,4 ) ?</p>

## Answers
### Answer ID: 78228648
<p>This is very much an &quot;it depends&quot; situation.  Redshift uses metadata on all columns to know which blocks contain which value ranges.  Being able to exclude data from a query based on metadata is one of Redshift's most powerful features when dealing with large tables.  So if you are writing a clause against a column that has (valid) metadata that help with this data reduction then one set of factors are in play.  If not then another set.</p>
<p>In general positive assertions like A IN (2,3,4) is better than a negative assertion like A &lt;&gt; 1.  Redshift can use the former to compare metadata against these values and exclude blocks that cannot include any of them.  It can also use A &lt;&gt; 1 as it is a simple case and remove any blocks that only has the value 1.  The killer is NOT IN as this usually requires a full scan of the table.</p>
<p>Now Redshift can convert long IN lists (10 or more last I tested) to virtual tables and INNER JOINs this to achieve the same result.  This can also thwart the metadata check so long IN lists are also a potential problem.  In this case the &lt;&gt; 1 could be better.</p>
<p>If your metadata isn't helpful in reducing table scan then the difference will likely be much smaller.  Redshift has to read all the rows and apply the clause.  Not much difference between these at that level.  However long IN lists still can create JOINs which could be somewhat slower.</p>
<p>Like I said &quot;it depends&quot;.</p>

