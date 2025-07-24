# How to Make Grouped Query with Specific Key Fields Translatable by EF Core?
[Link to question](https://stackoverflow.com/questions/78976816/how-to-make-grouped-query-with-specific-key-fields-translatable-by-ef-core)
**Creation Date:** 1726123902
**Score:** 0
**Tags:** c#, .net, entity-framework, entity-framework-core
## Question Body
<p>I'm working on an application where I need to insert data into a database while avoiding duplicates. To achieve this, I group the imported data by several fields, extract the key fields, and then query the database to check if records already exist. The problem I'm facing is that EF Core isn't able to translate my query to SQL, resulting in runtime exceptions.</p>
<p>Here’s the relevant code:</p>
<pre><code>// Group the imports to ensure uniqueness
var items = items
    .GroupBy(i =&gt; new { i.Field1, i.Field2, i.Field3, i.Field4, i.Field5 })
    .Select(g =&gt; g.First())
    .ToList();

// Extract keys to query the database only on indexed fields
var keys = items.Select(i =&gt; new
{
    i.Field1,
    i.Field2,
    i.Field3,
    i.Field4,
    i.Field5
}).ToList();

// Query the database for existing records using only the key fields
var existingRecords = await _dbContext.DataSet
    .Where(dbRecord =&gt; keys.Contains(new
    {
        dbRecord.Field1,
        dbRecord.Field2,
        dbRecord.Field3,
        dbRecord.Field4,
        dbRecord.Field5
    }))
    .ToListAsync();

// Filter out records that already exist
var recordsToInsert = items
    .Where(item =&gt; !existingRecords.Any(existing =&gt;
        existing.Field1 == item.Field1 &amp;&amp;
        existing.Field2 == item.Field2 &amp;&amp;
        existing.Field3 == item.Field3 &amp;&amp;
        existing.Field4 == item.Field4 &amp;&amp;
        existing.Field5 == item.Field5))
    .ToList();
</code></pre>
<p>EF Core throws an exception indicating that the .Contains() operation cannot be translated into SQL. I understand that EF Core has limitations when it comes to certain operations, but I need to optimize this query to avoid pulling all the records into memory.</p>
<p>Could anyone suggest how I can rewrite this query so that it remains translatable by EF Core and performs efficiently?</p>

