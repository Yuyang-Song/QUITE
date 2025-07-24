# Transform Sql to EF Core Linq query
[Link to question](https://stackoverflow.com/questions/65189259/transform-sql-to-ef-core-linq-query)
**Creation Date:** 1607374601
**Score:** 0
**Tags:** linq, entity-framework-core
## Question Body
<p>I am trying to translate the following query from SQL to EF Core. I can easily just use a stored procedure (I already have the SQL), but am trying to learn how some of the linq queries work. Unfortunately this is not by any means an ideal database schema that I inherited and I don't have the time to convert it to something better.</p>
<pre><code>DECLARE @userId INT = 3

SELECT *
FROM dbo.CardGamePairs
WHERE EXISTS (SELECT 1
              FROM dbo.Users
              WHERE Users.Id = CardGamePairs.player1Id
                AND Users.userId = @userId)
UNION
SELECT *
FROM dbo.CardGamePairs
WHERE EXISTS (SELECT 1
              FROM dbo.Users
              WHERE Users.Id = TableB.player2Id
               AND Users.userId = @userId)
</code></pre>
<p>So basically I have an id that can exist in one of two separate columns in table b and I don't know in which column it may be in, but I need all rows that have that ID in either column. The following is what I tried to make this work:</p>
<pre><code>//Find data from table A where id matches (part of the subquery from above)
var userResults = _userRepository.GetAllAsQueryable(x =&gt; x.userId == userId).ToList();

//Get data from table b
var cardGamePairsResults = _cardGamePairsRepository.GetAllAsQueryable(x =&gt; userResults .Any(y =&gt; y.userId == x.player1Id || y.userId == x.player2Id));

</code></pre>
<p>When I run the code above I get this error message:</p>
<blockquote>
<p>predicate: (y) =&gt; y.userId == x.player1Id || y.userId == x.player2Id))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>
<p>Any ideas on how I can make this work? (I tried changing the column and table names to something that would actually make sense, hopefully I didn't miss any spots and make it more confusing.)</p>

## Answers
### Answer ID: 65189838
<p>Because you are already have user id use it to query both columns.</p>
<pre><code>var userResults = _userRepository
  .GetAllAsQueryable(x =&gt; x.userId == userId)
  .ToList();

var cardGamePairsResults = _cardGamePairsRepository
  .GetAllAsQueryable(x =&gt; x.player1Id == userId || x.player2Id == userId));
</code></pre>

