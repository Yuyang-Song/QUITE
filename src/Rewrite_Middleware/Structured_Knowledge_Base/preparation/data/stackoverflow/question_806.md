# Entity Framework 4: how to insert the next highest number without using an identity field?
[Link to question](https://stackoverflow.com/questions/4329898/entity-framework-4-how-to-insert-the-next-highest-number-without-using-an-ident)
**Creation Date:** 1291243340
**Score:** 2
**Tags:** sql, sql-server-2005, entity-framework-4, linq-to-entities, pivot-table
## Question Body
<p>I have a Product table that uses UPC as part of the primary key.  Everything is fine until the product doesn't have a UPC and the recommended way to solve this is to generate a number between 8004 + identity number and 8005 + identity number.</p>

<p>I need to generate a unique UPC if the UPC is zero while in a transaction, then be able to retrieve the new UPCs for only the products which had zero as a UPC value.</p>

<p>In SQL, I could do this:</p>

<pre><code> insert into Product (ID, Name)
 select min(pivotTable.value), 'New Product' as Name
 from pivotTable
 where not exists( 
     select null as nothing 
     from product
     where pivotTable.value = product.ID ) and
 pivotTable.value &gt; 8004000000 and pivotTable.value &lt; 8005000000

 select id
 from   product
 where  Name = 'New Product' -- assuming Name is unique
</code></pre>

<p><strong>How would I do this in Entity Framework 4</strong>?  A separate concern is that this is all under a single transaction, so assigning numbers of sets of missing UPCs could assign the same UPC to all new products.</p>

<p>EDIT:</p>

<p>I ended up creating a view that looks like this to get the next highest number, but EF won't generate the table in a diagram because it cannot determine a primary key.  If I hack the XML, it works until I update from database, which erases my changes.</p>

<pre><code>Select min(ID), 'New Product' as Name
from ( select distinct ID
       from   product p1
       where  p1.ID &gt; 8004000000 and p1.ID &lt; 8005000000
       union
       select distinct coalesce( ID, 8004000000) as ID) A

     left outer join

     ( select distinct ID
       from   product p2
       where  p2.ID &gt; 8004000000 and p2.ID &lt; 8005000000
       union
       select distinct coalesce( ID, 8004000000) as ID) B

     on A.ID + 1 = B.ID
where B.ID is null
</code></pre>

<p>So the question is the same: <strong>How could you generate the least highest available number in Entity Framework 4</strong>, i.e., how could you rewrite the SQL query above in Linq to Entities, or how could you get the view to show in the Entity Framework 4 diagram without editing the XML file which tosses your changes on refresh?</p>

<p>EDIT: This seems to generate the next available using Linq:</p>

<pre><code>// Setup our ID list
var prod = DC.Products.Where(p =&gt; p.ID &gt; 0 &amp;&amp; p.ID &lt; 1000)
    .Select(p =&gt; p.ID).Distinct();

// Compare the list against itself, offset by 1.  Look for "nulls"
// which represent "next highest number doesn't exist"
var q = (from p1 in prod
         from p2 in prod.Where(a =&gt; a == p1 + 1).DefaultIfEmpty() // Left join
         where p2 == 0                            // zero is null in this case
         select p1).Min();
var r = q + 1;   // one higher than current didn't exist, so that's the answer
</code></pre>

## Answers
### Answer ID: 7197284
<p>not quite sure why you need this complex calculations. However, if you need always unique database-wide number take a look at <code>RowVersion</code> type in MSSQL tables. It will give you always unique number which is changed every time row with the record is updated. And it is unique for a whole db.</p>

