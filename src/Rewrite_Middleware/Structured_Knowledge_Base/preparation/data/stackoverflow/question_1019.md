# EF Core - many queries sent to database for subquery
[Link to question](https://stackoverflow.com/questions/55027679/ef-core-many-queries-sent-to-database-for-subquery)
**Creation Date:** 1551889145
**Score:** 2
**Tags:** linq, linq-to-entities, entity-framework-core, ef-core-2.2
## Question Body
<p>Using EF Core 2.2.2, I have a table in my database which is used to store notes for many other tables. In other words, it's sortof like a detail table in a master-detail relationship, but with multiple master tables. Consider this simplified EF Model:</p>

<pre><code>public class Person
{
  public Guid PersonID { get; set; }
  public string Name { set; set; }
}

public class InvoiceItem
{
  public Guid InvoiceItemID { get; set; }
  public Guid InvoiceID { get; set; }
  public string Description { get; set; }
}

public class Invoice
{
  public Guid InvoiceID { get; set; }
  public int InvoiceNumber { get; set; }

  public List&lt;Item&gt; Items { get; set; }
}

public class Notes
{
  public Guid NoteID { get; set; }
  public Guid NoteParentID { get; set; }
  public DateTime NoteDate { get; set; }
  public string Note { get; set; }
}
</code></pre>

<p>In this case, Notes can store Person notes or Invoice notes (or InvoiceItem notes, though let's just say that the UI doesn't support that).</p>

<p>I have query methods set up like this:</p>

<pre><code>public IQueryable&lt;PersonDTO&gt; GetPersonQuery()
{
  return from p in Context.People
             select new PersonDTO
             {
               PersonID = p.PersonID,
               Name = p.Name
             };
}

public List&lt;PersonDTO&gt; GetPeople()
{
  return (from p in GetPersonQuery()
              return p).ToList();
}

public IQueryable&lt;InvoiceDTO&gt; GetInvoiceQuery()
{
  return from p in Context.Invoices
             select new InvoiceDTO
             {
               InvoiceID = p.InvoiceID,
               InvoiceNumber = p.InvoiceNumber
             };
}

public List&lt;InvoiceDTO&gt; GetInvoices()
{
  return (from i in GetInvoiceQuery()
              return i).ToList();
}
</code></pre>

<p>These all work as expected. Now, let's say I add InvoiceItems to the Invoice query, like this:</p>

<pre><code>public IQueryable&lt;InvoiceDTO&gt; GetInvoiceQuery()
{
  return from p in Context.Invoices
             select new InvoiceDTO
             {
               InvoiceID = p.InvoiceID,
               InvoiceNumber = p.InvoiceNumber,
               Items = (from ii in p.Items
                             select new ItemDTO
                             {
                               ItemID = ii.ItemID,
                               Description = ii.Description
                             }).ToList()
             };
}
</code></pre>

<p>That also works great, and issues just a couple queries. However, the following:</p>

<pre><code>public IQueryable&lt;InvoiceDTO&gt; GetInvoiceQuery()
{
  return from p in Context.Invoices
             select new InvoiceDTO
             {
               InvoiceID = p.InvoiceID,
               InvoiceNumber = p.InvoiceNumber,
               Items = (from ii in p.Items
                             select new ItemDTO
                             {
                               ItemID = ii.ItemID,
                               Description = ii.Description
                             }).ToList(),
              Notes = (from n in Context.Notes
                             where i.InvoiceID = n.NoteParentID
                             select new NoteDTO
                             {
                               NoteID = n.NoteID,
                               Note = n.Note
                             }).ToList(),
             };
}
</code></pre>

<p>sends a separate query to the Note table for each Invoice row in the Invoice table. So, if there are 1,000 invoices in the Invoice table, this is sending something like 1,001 queries to the database. </p>

<p>It appears that the Items subquery does not have the same issue because there is an explicit relationship between Invoices and Items, whereas there isn't a specific relationship between Invoices and Notes (because not all notes are related to invoices).</p>

<p>Is there a way to rewrite that final query, such that it will not send a separate note query for every invoice in the table?</p>

## Answers
### Answer ID: 55039434
<p>The problem is indeed the correlated subquery versus collection navigation property. EF Core query translator still has issues processing such subqueries, which are in fact logical collection navigation properties and should have been processed in a similar fashion.</p>

<p>Interestingly, simulating collection navigation property with intermediate projection (<code>let</code> operator in LINQ query syntax) seems to fix the issue:</p>

<pre><code>var query =
    from i in Context.Invoices
    let i_Notes = Context.Notes.Where(n =&gt; i.InvoiceID == n.NoteParentID) // &lt;--
    select new InvoiceDTO
    {
        InvoiceID = i.InvoiceID,
        InvoiceNumber = i.InvoiceNumber,
        Items = (from ii in i.Items
                 select new ItemDTO
                 {
                     ItemID = ii.ItemID,
                     Description = ii.Description
                 }).ToList(),
        Notes = (from n in i_Notes // &lt;--
                 select new NoteDTO
                 {
                     NoteID = n.NoteID,
                     Note = n.Note
                 }).ToList(),
    };
</code></pre>

