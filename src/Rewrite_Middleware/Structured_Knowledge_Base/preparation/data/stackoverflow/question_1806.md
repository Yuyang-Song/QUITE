# SubSonic, ORM, edmx, Linq: serializable Db communication?
[Link to question](https://stackoverflow.com/questions/8601200/subsonic-orm-edmx-linq-serializable-db-communication)
**Creation Date:** 1324542750
**Score:** 0
**Tags:** linq, subsonic, edmx
## Question Body
<p>the following scenario waits for nice alternatives:</p>

<ul>
<li>a central Windows service written in .NET accepts clients to query a database in the background (and also lets them write to the Db).</li>
<li>clients should be able to use old-style .NET Remoting for compatibility (or a very simple transition to WCF could be made)</li>
<li>currently queries are sent via homemade objects which either carry standard instructions (Insert, Update, SelectCommand) or a string-based direct SQL query, but to use Linq all records need to be pulled to the local client</li>
<li>should work with oracle and MSSQL</li>
<li>Events are sent to the clients from the server when data changes in a table - this is a must-have!</li>
</ul>

<p>These are the main requirements. Now we have started to evaluate a transition to Linq with edmx, but we fear to loose flexibility and we would have to rewrite quite all of the Db handling code. The essential improvement we would like to see is a Linqed binding over the network so we can use Linq queries without directly attaching to the EMF layer of .NET 4. And I started investigation on ORM alternatives and came across subsonic right now.</p>

<p>So to start asking the question :) - will it be possible to use SubSonic in such a way that the client has all knowledge on the entities but the query transofrmation and the Db connection is hosted only on a central server? We want to decouple the direct access to the Db because of Db events, replication and other specific features necessary for our applications.</p>

<p>Regards Florian</p>

## Answers
### Answer ID: 8721661
<p>Your question is very broad -- I can only answer one tiny part.</p>

<p>SubSonic ORM 3.0 contains a Linq to SQL translater. Your Linq queries are converted into SQL, and only the rows you actually consume are returned to the client. The effect is much the  same as if you had written custom SQL, and indeed you can retrieve the generated SQL.</p>

<p>Most of your question seems to be way out of scope, because it's more about distributed query processing rather than simple ORM stuff.</p>

### Answer ID: 8602556
<p>There was a project, <a href="http://interlinq.codeplex.com/" rel="nofollow">InterLINQ</a>, that was aiming to solve a need similar to what your describing in a somewhat generic way (generic, as in able to work with multiple query providers on the server side).  I have never used this project, and it seems that it hasn't been worked on in over a year and it lacks documentation.</p>

<p>I don't think SubSonic would be any easier to achieve this with than any other linq provider.  You would probably be just as well off trying to serialize the expression representing the query in a provider-agnostic way.</p>

