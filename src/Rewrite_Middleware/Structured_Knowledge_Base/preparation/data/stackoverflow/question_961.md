# Check which messages already exist without loading entire table to memory
[Link to question](https://stackoverflow.com/questions/51999936/check-which-messages-already-exist-without-loading-entire-table-to-memory)
**Creation Date:** 1535097512
**Score:** 2
**Tags:** c#, entity-framework, entity-framework-core
## Question Body
<p>I want to check if any message already exists before adding it to database, but my current query loads the entire table into memory. Query generated from my code is basically just <code>select * from tableName</code>.</p>

<p>How can I rewrite this query to be evaluated in database?</p>

<pre><code>public void AddMessages(IEnumerable&lt;Message&gt; messages)
{
    if (messages == null)
        throw new ArgumentNullException(nameof(messages));

    var duplicates = (from currMsg in context.Messages
                      where messages.Any(msg =&gt;
                                                msg.Prop1 == currMsg.Prop1 &amp;&amp;
                                                msg.Prop2 == currMsg.Prop2 &amp;&amp;
                                                msg.Prop3 == currMsg.Prop3)
                      select currMsg);

    var messagesWithoutDuplicates = messages.Except(duplicates);

    context.Messages.AddRange(messagesWithoutDuplicates);
    context.SaveChanges();
}
</code></pre>

<p>I could also run it in a loop, but then I would create many db calls instead of 1 and I would prefer to do this in a single call.</p>

## Answers
### Answer ID: 52001773
<p>Since there is no easy way of doing this in a single call I decided to sacrifice performance and retain readability and testability. This is my solution:</p>

<pre><code>using (var transaction = context.Database.BeginTransaction())
{
    try
    {
        foreach (var message in messages)
        {
            var exists = context.Messages.Any(msg =&gt; msg.Prop1 == message.Prop1 &amp;&amp;
                                                     msg.Prop2 == message.Prop2 &amp;&amp;
                                                     msg.Prop3 == message.Prop3 &amp;&amp;);

            if (!exists)
            {
                context.Messages.Add(message);
            }
        }

        context.SaveChanges();
        transaction.Commit();
    }
    catch (Exception ex)
    {
        _logger.Error(ex);
        transaction.Rollback();
        throw;
    }
}
</code></pre>

### Answer ID: 52000691
<p>Depending on your use-case, you may need to insert them one-by-one and trust on the database unique-index (you have one, right?) to throw it back in your face if it's a duplicate.</p>

<p>There is two weaknesses in your code <em>besides</em> memory consumption: concurrency (what if somebody else inserts while you check for duplicates) and the fact that your records to insert might themselves be duplicates that you did not check for. </p>

### Answer ID: 52000147
<p>you can use SELECT COUNT(*) FROM TABLE if you wish to check how many rows in table.
execute this query before you do your task.</p>

<p>or if you wish to update if row cannot be inserted ( duplicated )
you need to use merge-insert for that.</p>

<p>Merge Insert (MySql) => <a href="https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html" rel="nofollow noreferrer">https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html</a></p>

<p>Merge Insert (Oracle) => <a href="https://docs.oracle.com/cd/B28359_01/server.111/b28286/statements_9016.htm#SQLRF01606" rel="nofollow noreferrer">https://docs.oracle.com/cd/B28359_01/server.111/b28286/statements_9016.htm#SQLRF01606</a></p>

