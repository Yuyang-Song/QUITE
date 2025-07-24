# SQL scalar subquery checking a row was found
[Link to question](https://stackoverflow.com/questions/28883365/sql-scalar-subquery-checking-a-row-was-found)
**Creation Date:** 1425574507
**Score:** 0
**Tags:** sql-server-2008, t-sql, join, cardinality, scalar-subquery
## Question Body
<p><strong>Introduction</strong></p>

<p>Sometimes instead of a join you can deliberately use a scalar subquery to check that not more than one row was found.  For example you might have this query to look up nationality for some <code>person</code> rows.</p>

<p><code>select p.name,
       c.iso
from person p
join person_country_map pcm
  on p.id = pcm.person
join country c
  on pcm.country = c.id
where p.id in (1, 2, 3)
</code></p>

<p>Now, suppose that the <code>person_country_map</code> is not a functional mapping.  A given person may map to more than one country - so the join may find more than one row.  Or indeed, a person might not be in the mapping table at all, at least as far as any database constraints are concerned.</p>

<p>But for <em>this particular query</em> I happen to know that the persons I am querying will have exactly one country.  That is the assumption I am basing my code on.  But I would like to check that assumption where possible - so that if something went wrong and I end up trying to do this query for a person with more than one country, or with no country mapping row, it will die.</p>

<p><strong>Adding a safety check for at most one row</strong></p>

<p>To check for more than one row, you can rewrite the join as a scalar subquery:</p>

<p><code>select p.name,
       (
         select c.iso
         from person_country_map pcm
         join country c
           on pc.country = c.id
         where pcm.person = p.id
       ) as iso
from person p
where p.id in (1, 2, 3)
</code></p>

<p>Now the DBMS will give an error if a person queried maps to two or more countries.  It won't return multiple entries for the same person, as the straightforward join would.  So I can sleep a bit easier knowing that this error case is being checked for even before any rows are returned to the application.  As a careful programmer I might check in the application as well, of course.</p>

<p><strong>Is it possible to have a safety check for</strong> <em>no</em> <strong>row found?</strong></p>

<p>But what about if there is no row in person_country_map for a person?  The scalar subquery will return null in that case, making it roughly equivalent to a left join.</p>

<p>(For the sake of argument assume a foreign key from person_country_map.country to country.id and a unique index on country.id so that particular join will always succeed and find exactly one country row.)</p>

<p><strong>My question</strong></p>

<p>Is there some way I can express in SQL that I want one and exactly one result?  A plain scalar subquery is 'zero or one'.  I would like to be able to say</p>

<p><code>select 42, (select exactly one x from t where id = 55)</code></p>

<p>and have the query fail at runtime if the subquery wouldn't return a row.  Of course, the above syntax is fictional and I am sure it wouldn't be that easy.</p>

<p>I am using MSSQL 2008 R2, and in fact this code is in a stored procedure, so I can use TSQL if necessary.  (Obviously ordinary declarative SQL is preferable since that can be used in view definitions too.)  Of course, I can do an <code>exists</code> check, or I can select a value into a TSQL variable and then explicitly check it for nullness, and so on.  I could even select results into a temporary table and then build unique indexes on that table as a check.  But is there no more readable and elegant way to mark my assumption that a subquery returns exactly one row, and have that assumption checked by the DBMS?</p>

## Answers
### Answer ID: 28905240
<p>In MSSQL it appears that <code>isnull</code> only evaluates its second argument if the first is null.  So in general you can say</p>

<p><code>select isnull(x, 0/0)</code></p>

<p>to give a query which returns <code>x</code> if non-null and dies if that would give null.  Applying this to a scalar subquery,</p>

<p><code>select 42, isnull((select x from t where id = 55), 0/0)</code></p>

<p>will guarantee that exactly one row is found by the <code>select x</code> subquery.  If more than one, the DBMS itself will produce an error; if no row, the division by zero is triggered.</p>

<p>Applying this to the original example leads to the code</p>

<p><code>select p.name,
       -- Get the unique country code of this person.
       -- Although the database constraints do not guarantee it in general,
       -- for this particular query we expect exactly one row.  Check that.
       --
       isnull((
         select c.iso
         from person_country_map pcm
         join country c
           on pc.country = c.id
         where pcm.person = p.id
       ), 0/0) as iso
from person p
where p.id in (1, 2, 3)
</code></p>

<p>For a better error message you can use a conversion failure instead of division by zero:</p>

<p><code>select 42, isnull((select x from t where id = 55), convert(int, 'No row found'))</code></p>

<p>although that will need further <code>convert</code> shenanigans if the value you are fetching from the subquery is not itself an <code>int</code>.</p>

### Answer ID: 28885012
<p>You are making this harder than it needs to be  </p>

<p>For sure you need a FK relationship on  person.id to person_country_map.person </p>

<p>You either have unique constraint on person_country_map.person or you don't?<br>
If you don't have a unique constraint then yes you can have multiple records for the same person_country_map.person.   </p>

<p>If you want to know if you have any duplicate then  </p>

<pre><code>select pcm.person 
from person_country_map pcm
group by  pcm.person  
having count(*) &gt; 1
</code></pre>

<p>If there is more than one then you just need to determine which one  </p>

<pre><code>select p.name,
       min(c.iso)
from person p
join person_country_map pcm
  on p.id = pcm.person
join country c
  on pcm.country = c.id 
where p.id in (1, 2, 3)
group by p.name
</code></pre>

