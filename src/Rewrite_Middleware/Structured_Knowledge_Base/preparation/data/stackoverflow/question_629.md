# LINQ vs. SQL Joins And Groupings (w/ Specific Case)
[Link to question](https://stackoverflow.com/questions/34142660/linq-vs-sql-joins-and-groupings-w-specific-case)
**Creation Date:** 1449520387
**Score:** 0
**Tags:** sql, linq, join, grouping
## Question Body
<p>In SQL, when you do a bunch of joins, it treats all of the joined objects as one "super-object" to be selected from. This remains the case when you group by a particular column, as long as you include anything you select in the grouping (unless it is produced by the grouping, such as summing a bunch of int columns).</p>

<p>In LINQ, you can similarly do a bunch of joins in a row, and select from them. However, when you perform a grouping, it behaves differently. The syntax in query-style LINQ only allows for grouping a single table (i.e., one of your joins), discarding the others.</p>

<p>For an example case suppose we have a few tables:</p>

<pre><code>Request
-------
int ID (PK)
datetime Created
int StatusID (FK)

Item
----
int ID (PK)
string Name

RequestItem
-----------
int ID (PK)
int ItemID (FK)
int RequestID (FK)
int Quantity

Inventory
---------
int ID (PK)
int ItemID (FK)
int Quantity    

LU_Status
---------
int ID (PK)
string Description
</code></pre>

<p>In our example, LU_Status has three values in the database:</p>

<pre><code>1 - New
2 - Approved
3 - Completed
</code></pre>

<p>This is a simplified version of the actual situation that lead me to this question. Given this schema, the need is to produce a report that shows the number of requested items (status not "Completed"), approved items (status "Approved"), distributed items (status "Completed"), and the number of items in stock (from Inventory), all grouped by the item. If this is a bit vague take a look at the SQL or let me know and I'll try to make it clearer.</p>

<p>In SQL I might do this:</p>

<pre><code>select i.Name,
Requested = sum(ri.Quantity), 
Approved = sum(case when r.StatusID = 2 then ri.Quantity else 0 end)
Distributed = sum(case when r.StatusID = 3 then ri.Quantity else 0 end)
Storage = sum(Storage)
from RequestItem as ri
inner join Request as r on r.ID = ri.RequestID
inner join Item as i on i.ID = ri.ItemID
inner join (select ItemID, Storage = sum(Quantity)
            from Inventory
            group by ItemID)
            as inv on inv.ItemID = ri.ItemID
group by i.Name
</code></pre>

<p>This produces the desired result.</p>

<p>I began to rewrite this in LINQ, and got so far as:</p>

<pre><code>var result = from ri in RequestItem
             join r in Request on ri.RequestID equals r.ID
             join i in Item on ri.ItemID equals i.ID
             join x in (from inv in Inventory
                        group inv by inv.ItemID into g
                        select new { ItemID = g.Key, Storage = g.Sum(x =&gt; x.Quantity) })
                        on ri.ItemID equals x.ItemID
             group...????
</code></pre>

<p>At this point everything had been going smoothly, but I realized that I couldn't simply group by i.Name like I did in SQL. In fact, there seemed to be no way to group all of the joined things together so that I could select the necessary things from them, so I was forced to stop there.. I understand how to use the group syntax in simpler situations (see the subquery), but if there's a way to do this sort of grouping in LINQ I'm not seeing it, and searching around here and elsewhere has not illuminated me.</p>

<p>Is this a shortcoming of LINQ, or am I missing something?</p>

## Answers
### Answer ID: 34144570
<p>The easiest way is to use <code>group new { ... } by ...</code> construct and include all the items from the joins that you need later inside the <code>{ ... }</code>, like this</p>

<pre><code>var query =
    from ri in db.RequestItem
    join r in db.Request on ri.RequestID equals r.ID
    join i in db.Item on ri.ItemID equals i.ID
    join x in (from inv in db.Inventory
               group inv by inv.ItemID into g
               select new { ItemID = g.Key, Storage = g.Sum(x =&gt; x.Quantity) }
              ) on ri.ItemID equals x.ItemID
    group new { ri, r, i, x } by i.Name into g
    select new
    {
        Name = g.Key,
        Requested = g.Sum(e =&gt; e.ri.Quantity),
        Approved = g.Sum(e =&gt; e.r.StatusID == 2 ? e.ri.Quantity : 0),
        Distributed = g.Sum(e =&gt; e.r.StatusID == 3 ? e.ri.Quantity : 0),
        Storage = g.Sum(e =&gt; e.x.Storage)
    };
</code></pre>

### Answer ID: 34144026
<p>You can create an anonymous type in a grouping that contains all data you need:</p>

<pre><code>var result = from ri in RequestItem
             join r in Request on ri.RequestID equals r.ID
             join i in Item on ri.ItemID equals i.ID
             join x in (from inv in Inventory
                        group inv by inv.ItemID into g
                        select new { ItemID = g.Key, Storage = g.Sum(x =&gt; x.Quantity) })
                        on ri.ItemID equals x.ItemID
             group new
             {
                 i.Name,
                 r.StatusId,
                 ri.Quantity,
                 x.Storage,
             }
             by i.Name into grp
             select new
             {
                 grp.Key,
                 Requested = grp.Where(x =&gt; x.StatusID == 2).Sum(x =&gt; x.Quantity),
                 Distributed = grp.Where(x =&gt; x.StatusID == 3).Sum(x =&gt; x.Quantity),
                 Storage = grp.Sum(x =&gt; x.Storage)
             }
</code></pre>

<p>(not tested, obviously, but it should be close).</p>

