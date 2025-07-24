# How to write select and group statement in LINQ?
[Link to question](https://stackoverflow.com/questions/78318065/how-to-write-select-and-group-statement-in-linq)
**Creation Date:** 1712945731
**Score:** 0
**Tags:** c#, asp.net-core
## Question Body
<p>I want to know how to rewrite my query in LINQ to fetch data from the database with the use of select and group statement.</p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th>ID</th>
<th>Item</th>
<th>Qty</th>
<th>Amount</th>
<th>Date</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Padlock</td>
<td>2</td>
<td>2.00</td>
<td>09/04/2024</td>
</tr>
<tr>
<td>2</td>
<td>Bolt</td>
<td>1</td>
<td>5.00</td>
<td>09/04/2024</td>
</tr>
<tr>
<td>3</td>
<td>Bolt</td>
<td>3</td>
<td>15.00</td>
<td>10/04/2024</td>
</tr>
<tr>
<td>4</td>
<td>Bolt</td>
<td>1</td>
<td>5.00</td>
<td>11/04/2024</td>
</tr>
</tbody>
</table></div>
<p>This is what l had tried. The code below actually fetch all records from the database, but l don't how to add the select and group statement into it.</p>
<pre><code>[HttpGet]
    public object Get()
    {
        return new { Items = _context.OrderDetail.ToList(), Count = _context.OrderDetail.Count() };
    }
}
</code></pre>
<p>This is what l am expecting.</p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th>Item</th>
<th>Qty</th>
<th>Amount</th>
</tr>
</thead>
<tbody>
<tr>
<td>Padlock</td>
<td>2</td>
<td>2.00</td>
</tr>
<tr>
<td>Bolt</td>
<td>5</td>
<td>25.00</td>
</tr>
<tr>
<td>Spanner</td>
<td>3</td>
<td>5.00</td>
</tr>
</tbody>
</table></div>

## Answers
### Answer ID: 78318130
<p>Need to get distinct names along with total quantity and total amount. Please try something like below. Replace the name of properties as you need.</p>
<pre><code>var result = items
        .GroupBy(item =&gt; item.Name)
        .Select(group =&gt; new
        {
            Name = group.Key,
            TotalQty = group.Sum(item =&gt; item.Qty),
            TotalAmount = group.Sum(item =&gt; item.Amount)
        });
</code></pre>

