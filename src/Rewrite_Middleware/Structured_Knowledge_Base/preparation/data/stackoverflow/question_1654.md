# Oracle syntax - should we have to choose between the old and the new?
[Link to question](https://stackoverflow.com/questions/2821854/oracle-syntax-should-we-have-to-choose-between-the-old-and-the-new)
**Creation Date:** 1273690384
**Score:** 11
**Tags:** oracle-database, syntax
## Question Body
<p>I work on a code base in the region of about 1'000'000 lines of source, in a team of around eight developers. Our code is basically an application using an Oracle database, but the code has evolved over time (we have plenty of source code from the mid nineties in there!).</p>

<p>A dispute has arisen amongst the team over the syntax that we are using for querying the Oracle database. At the moment, the overwhelming majority of our queries use the "old" Oracle Syntax for joins, meaning we have code that looks like this...</p>

<p><em>Example of Inner Join</em></p>

<pre><code>select customers.*
       , orders.date
       , orders.value 
from customers, orders
where customers.custid = orders.custid
</code></pre>

<p><em>Example of Outer Join</em></p>

<pre><code>select customers.custid
       , contacts.ContactName
       , contacts.ContactTelNo 
from customers, contacts 
where customers.custid = contacts.custid(+)
</code></pre>

<p>As new developers have joined the team, we have noticed that some of them seem to prefer using SQL-92 queries, like this:</p>

<p><em>Example of Inner Join</em></p>

<pre><code>select customers.*
       , orders.date
       , orders.value 
from customers inner join orders 
     on (customers.custid = orders.custid)
</code></pre>

<p><em>Example of Outer Join</em></p>

<pre><code>select customers.custid
      , contacts.ContactName
      , contacts.ContactTelNo
from customers left join contacts 
      on (customers.custid = contacts.custid)
</code></pre>

<p>Group A say that everyone should be using the the "old" syntax - we have lots of code in this format, and we ought to value consistency. We don't have time to go all the way through the code now rewriting database queries, and it wouldn't pay us if we had. They also point out that "this is the way we've always done it, and we're comfortable with it..."</p>

<p>Group B however say that they agree that we don't have the time to go back and change existing queries, we really ought to be adopting the "new" syntax on code that we write from here on in. They say that developers only really look at a single query at a time, and that so long as developers know both syntax there is nothing to be gained from rigidly sticking to the old syntax, which might be deprecated at some point in the future.</p>

<p>Without declaring with which group my loyalties lie, I am interested in hearing the opinions of impartial observers - so let the games commence!</p>

<p>Martin.</p>

<p>Ps. I've made this a community wiki so as not to be seen as just blatantly chasing after question points...</p>

## Answers
### Answer ID: 2824961
<p>Use the new syntax. It's more powerful and concise. It's the industry standard. It's understood by many more people than the old syntax is. It is what Oracle recommend.</p>

### Answer ID: 2824926
<p>There is no performance difference between the old Oracle syntax and the new ANSI syntax, for one very good reason.  Oracle takes queries written in the new syntax and rewrites them into the old syntax before submitting it to the optimizer.  It is obvious really, Oracle is not going to support two versions of the optimizer, and it is simply cheaper to retain its investment in the existing syntax.  </p>

<p>In the earlier versions of Oracle (that is, 9i) there were some bugs in this process, which meant that some logically equivalent queries ran slower if we wrote them in the new syntax compared to the old.  These bugs have reduced in number over subsequent releases.</p>

<p>One subtle side-effect of this re-writing process is that it can be harder to employ hints in the new syntax.  This is because the translated query may lack the necessary anchor point, so the hint gets "lost".</p>

<p>So, while the clarity of new syntax makes it easier to understand complicated queries it may be easier to tune queries written in the old syntax.</p>

### Answer ID: 2823039
<p>I have used the old syntax for 18+ years, but now (~2 years) I almost allways uses the new syntax, because</p>

<ul>
<li>easy read - I for one dont miss "(+)"</li>
<li>when 'debugging' its easier to comment out at join in the new syntax, e.g. the join line (if written on 1 line, of course) and the fields selected from the table. No checking the where clause for join conditions</li>
<li>full outer join only available in new syntax (e.g. more features in general)</li>
<li>fits nicely with never features, e.g. MERGE INTO ... USING ... ON ...</li>
</ul>

### Answer ID: 2821892
<p>Similar thing here, but not as many devs, and not as old of code. I'm using the newer stuff, the older guys are using the older style, but we both know what the other is trying to do.</p>

<p>Personally, I'd say go with whichever style is easier for the individual developer to use. Unless you run benchmarks and find out that one is faster than the other (as in, enough of a difference to be significant), and both new and old can read &amp; understand the queries they see, there's no reason to change them.</p>

<p>However, my personal vote would be to leave the old stuff as-is, and write new queries using the newer syntax, as using <code>JOIN</code>s and <code>USING</code> and <code>ON</code> etc. are a lot easier to read, and know what's going on, then having a bunch of <code>AND x.col = y.col AND z.col = a.col</code> in the <code>WHERE</code> section.</p>

<p>That, and the new guys are probably going to be around longer, so they're gonna get their way eventually...</p>

<h3>An added example</h3>

<p>Don't know about the rest of you, but I'd hate having to try figuring something like this out (or write this) using the old-style of joining:</p>

<pre><code>SELECT DISTINCT product_zone_map_id, zh.name_english, zh.name_french, zone_id, ad.attribute_value_english AS bullprep_region_type,
        product_zone_type_id, ad.attribute_value_english, language_english, product_code, office_code,
        (
            SELECT attribute_value_english
            FROM presentation p JOIN presentation_details ad USING(presentation_id)
            WHERE dimension_id = 4
              AND object_id = product_zone_map_id
              AND attribute_type = 'BULLPREP PARENT ID'
              AND p.usage_start_date &lt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss')
              AND (p.usage_end_date &gt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss') OR p.usage_end_date IS NULL)
        ) AS bullprep_parent_id,
        (
            SELECT attribute_value_english
            FROM presentation p JOIN presentation_details ad USING(presentation_id)
            WHERE dimension_id = 4
              AND object_id = product_zone_map_id
              AND attribute_type = 'BULLPREP GROUP ID'
              AND p.usage_start_date &lt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss')
              AND (p.usage_end_date &gt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss') OR p.usage_end_date IS NULL)
        ) AS bullprep_group_id, product_zone_seq
FROM zone z JOIN zone_history zh ON(z.zone_id = zh.zone_id)
     JOIN product_zone_map pzm ON(z.zone_id = pzm.zone_id)
     JOIN product USING(product_id)
     JOIN product_history ph USING(product_id)
     JOIN language_reference USING(language_id)
     LEFT OUTER JOIN product_zone_attribute_details pzad USING(product_zone_map_id)
     LEFT OUTER JOIN attribute_details ad USING(attribute_id)
     JOIN zone_geocode_map USING(zone_id)
     JOIN geocode USING(geocode_id)
WHERE zh.usage_start_date &lt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss')
  AND (zh.usage_end_date &gt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss') OR zh.usage_end_date IS NULL)
  AND pzm.usage_start_date &lt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss')
  AND (pzm.usage_end_date &gt;= TO_TIMESTAMP('2010-05-12', 'yyyy-mm-dd hh24:mi:ss') OR pzm.usage_end_date IS NULL)
  AND (attribute_type = 'BULLPREP REGION TYPE' OR attribute_type IS NULL)
  AND product_id = 2075
ORDER BY product_zone_seq
</code></pre>

### Answer ID: 2822254
<p>If you don't have a coding standard that tells you how to do it, do it however you want.</p>

<p>Start using the JOIN style syntax. Then you can have 2 subgroups, one that prefers JOIN USING (a), and one that prefers JOIN ON (t1.a=t2.a).  </p>

<p>Seriously, if it's an available language feature and there's no standard saying whether or not it's OK to use, you decide, or push for an adopted coding standard.</p>

### Answer ID: 2822189
<p>I agree with what @Slokun has said, and I would add that over time, the developers are going to be more and more experienced with the JOIN syntax, and less with the WHERE clause joins. As people leave the project, and newcomers arrive, the bias will only get more skewed towards the modern syntax. It will make it a bit easier for non-Oracle DB programmers to look at the code in a pinch. Our project has both SQL Server and Oracle staffs, and the SQL Server folks are often befuddled by the (+) syntax. It goes both ways as well - if all your staff does is use the WHERE join syntax, they have a harder time with the JOIN syntax.</p>

<p>It's always a benefit to broaden one's horizons. Learn the new JOIN syntax and instantly nudge your career towards the 21st century! Personally, I made a conscious decision to learn the JOIN syntax here in the past year or two, and have started nudging others towards it as I go. What have you got to lose? I have found the new syntax much more readable and flexible.</p>

