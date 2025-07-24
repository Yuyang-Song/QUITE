# How can I rewrite that query - Can&#39;t write CLR type System.DateTime with handler type IntervalHandler
[Link to question](https://stackoverflow.com/questions/64023074/how-can-i-rewrite-that-query-cant-write-clr-type-system-datetime-with-handler)
**Creation Date:** 1600846242
**Score:** 0
**Tags:** c#, entity-framework-core, npgsql
## Question Body
<p>After upgrading from EF 2.1.x  to 3.1.x this query started to throw</p>
<p><code>Can't write CLR type System.DateTime with handler type IntervalHandler</code></p>
<p>But I'm not really sure how can I &quot;nicely&quot; rewrite this query, so performing math on those dates isn't going to explode</p>
<p><code>input is IQueryable</code></p>
<pre><code>input.OrderBy
(
        x =&gt;
        (x.RegistrationDate == null ? new DateTime(1990,1, 1).Date : x.RegistrationDate.Value.Date)
        -
        (x.InvoiceDate == null ? new DateTime(1990, 1, 1).Date : x.InvoiceDate.Value.Date)
)
</code></pre>
<p>Both of those <code>Dates</code> have type: <code>timestamp without time zone</code> in database</p>
<p><code>PostgreSQL 8.4.20 64-bit</code></p>
<p><code>&lt;PackageReference Include=&quot;Npgsql.EntityFrameworkCore.PostgreSQL&quot; Version=&quot;3.1.4&quot; /&gt;</code></p>
<p>Thanks in advance!</p>

