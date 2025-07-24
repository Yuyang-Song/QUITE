# Dynamic query using LinqKit is so slow! Can a stored procedure be better in that case?
[Link to question](https://stackoverflow.com/questions/17746301/dynamic-query-using-linqkit-is-so-slow-can-a-stored-procedure-be-better-in-that)
**Creation Date:** 1374237614
**Score:** 1
**Tags:** c#, entity-framework, stored-procedures, linqkit
## Question Body
<p>I am using LinqKit to build a query using dynamically generated filters. </p>

<p>That query fetches a quite large object graph from the database to perform calculations and does some other modifications to that data. As long as I don't use <code>Includes</code> in my query, it doesn't take long to get the main entity I need from the database. But, unfortunately, <strong>I need many of it's related entities</strong> to perform the needed calculations.</p>

<p>Each time I am adding an <code>Include</code>, this translates into a new <strong>nested subquery</strong> in SQL. I have about 8 or 9 <code>Inlcudes</code> so this translates to <strong>a lot</strong> of nested subqueries. That queries takes forever to return the data.</p>

<p>I would like all these nested subqueries to disappear from the SQL, but it's kinda tough to shape the SQL just the way I want using LinqKit from the application side.</p>

<p>I thought that, for that specific case, it would be a good idea to write a <strong>stored procedure</strong> just the way I want the SQL to be, and call it from Entity Framework.</p>

<p>My problem is I don't know how to get the <strong>object graph</strong> on the application side using a stored procedure. I can make EF generate a <code>ComplexType</code> which will include all the data in a single "entity", but the code doing calculation awaits a <strong>specific entity object graph</strong> (the main entity and it's related entities) so that code has no idea what that <code>ComplexType</code> is. I really don't want to have to rewrite the calculation engine to use that <code>ComplexType</code>. I can map the result to a single Entity, but only <strong>that</strong> Entity will be returned. I want the related entities to be returned too.</p>

<p>Looks like I'm caught between a rock and a crazy place.</p>

<p>Can anybody suggest anything ?</p>

## Answers
### Answer ID: 17746962
<p>We had the similar problems too. We end up building SQL views, and query against the views instead. I also think it's idea from CQRS pattern, basically, you separate your read model from write model.</p>

