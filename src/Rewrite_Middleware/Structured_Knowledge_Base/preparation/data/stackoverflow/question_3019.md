# Group by column and get first record of group using Linq
[Link to question](https://stackoverflow.com/questions/62459027/group-by-column-and-get-first-record-of-group-using-linq)
**Creation Date:** 1592512765
**Score:** 2
**Tags:** c#, entity-framework, linq, asp.net-core
## Question Body
<p>I'm trying to query a database using Linq to get only the last message a patient has sent from every patient from the SmsMessages table. I am trying to group the messages by patient Id, sort the groupings by the date, and then return the first record of that group, like follows:</p>

<pre><code>   var sms = await _dataContext.SmsMessages
                .GroupBy(message =&gt; message.PatientId)
                .Select(group =&gt; group.OrderByDescending(message =&gt; message.CreatedOn).FirstOrDefault())
                .ToListAsync();
</code></pre>

<p>Several answers to similar questions, <a href="https://stackoverflow.com/questions/19012986/how-to-get-first-record-in-each-group-using-linq">for example</a>, suggest doing a variation of the above, but I receive the following error when the query executes:
The error: </p>

<blockquote>
  <p>fail: Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware<a href="https://stackoverflow.com/questions/19012986/how-to-get-first-record-in-each-group-using-linq">1</a>
        An unhandled exception has occurred while executing the request.
  System.InvalidOperationException: The LINQ expression '(GroupByShaperExpression:
  KeySelector: (s.PatientId), 
  ElementSelector:(EntityShaperExpression: 
      EntityType: SmsMessage
      ValueBufferExpression: 
          (ProjectionBindingExpression: EmptyProjectionMember)
      IsNullable: False
  )
  )
      .OrderByDescending(message => message.CreatedOn)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation.</p>
</blockquote>

## Answers
### Answer ID: 67214039
<p>In my case I couldn't afford grouping on client side since the data was too heavy to download all the rows into client side when only the last row was needed. After spending some time trying different ef core and LINQ expressions, the only way I found was using Raw SQL query which uses a temp table. The SQL query looks like:</p>
<pre><code>SELECT message.* FROM message JOIN 
(SELECT PatientId, MAX(message.CreatedOn) AS CreatedOn 
FROM message GROUP BY message.PatientId) temp 
ON (message.PatientId = temp.PatientId and message.CreatedOn = temp.CreatedOn);
</code></pre>
<p>Then the method <code>FromSqlRaw</code> should be used to call this query using entity framework.</p>
<pre><code>var sms = _dataContext.SmsMessages.FromSqlRaw(
    &quot;SELECT message.* FROM message JOIN (SELECT PatientId, MAX(message.CreatedOn) AS CreatedOn FROM message GROUP BY message.PatientId) temp ON (message.PatientId = temp.PatientId and message.CreatedOn = temp.CreatedOn);&quot;).
    ToList();
</code></pre>

### Answer ID: 62467437
<blockquote>
  <p>This issue is related to <a href="https://learn.microsoft.com/en-us/ef/core/querying/client-eval" rel="nofollow noreferrer"><strong>Client vs. Server Evaluation</strong></a>.</p>
</blockquote>

<p>Before performing GroupBy, you need to add <code>ToList()</code> operation to <code>_dataContext.SmsMessages</code> to convert the server-side operation to the client side. </p>

<p>Otherwise, on the server side, <strong>sql server cannot recognize client-side methods</strong>.</p>

<p>Just change your code as follow:</p>

<pre><code> var sms = await _dataContext.SmsMessages.ToList()
                .GroupBy(message =&gt; message.PatientId)
                .Select(group =&gt; group.OrderByDescending(message =&gt; message.CreatedOn).FirstOrDefault())
                .ToListAsync();
</code></pre>

