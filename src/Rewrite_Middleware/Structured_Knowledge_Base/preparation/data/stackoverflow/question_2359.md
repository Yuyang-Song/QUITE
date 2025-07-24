# SQLite: Inconsistency of SELECT Query Results
[Link to question](https://stackoverflow.com/questions/31019448/sqlite-inconsistency-of-select-query-results)
**Creation Date:** 1435128226
**Score:** 1
**Tags:** sql, sqlite, select, corruption
## Question Body
<p>I'm facing something really weird, unexpected behavior, about some inconsistencies among different SELECT Queries and I have no idea whether this can come from the SQLite library, corrupted data, etc.</p>

<p>I have a database file with the following table, named ResultTable10 and with the structure as follows:</p>

<ul>
<li>INTEGER: Idx (PrimaryKey)</li>
<li>INTEGER: TimeStamp</li>
<li>INTEGER: Desynchronisation</li>
<li>INTEGER: Loop</li>
<li>INTEGER: Step</li>
<li>REAL   : ConditionValue</li>
<li>INTEGER: LimitId</li>
<li>TEXT   : 2KLINE1</li>
</ul>

<p>If I am using the most violent and brutal SELECT query: </p>

<pre><code>SELECT * FROM ResultTable10 
</code></pre>

<p>Then I am scrolling through the data using SQLite Browser (<a href="http://sqlitebrowser.org/" rel="nofollow noreferrer">http://sqlitebrowser.org/</a>)</p>

<p>And let's go to, for instance Loop = 124</p>

<p><img src="https://i.sstatic.net/l7iVL.png" alt="Data at Loop = 124"></p>

<p>And let's scroll a bit more to Loop = 125
<img src="https://i.sstatic.net/wOmmf.png" alt="Data at Loop = 125"></p>

<p>According to the data provider the number of rows for a given Loop value is always the same (and the values of the column Step for a giver Loop number are always same either, and by the way, same order too).</p>

<p>However, I found out that apparently if I'm only sticking to the SQL SELECT Query Results, this actually not ~that~ true:
<img src="https://i.sstatic.net/4HjtK.png" alt="Row Count Different"></p>

<p>It seems that the minimum value of the field Step for the two different loops (respectively Loop 124 and 125) is not the same (respectively Step ) </p>

<p>Furthermore the following queries targeting the Step = 508 are returning inconsistent results as well:</p>

<pre><code>SELECT * FROM ResultTable10 WHERE Step = 508 AND Loop = 125;
</code></pre>

<p>Here I can clearly see what I got before when I was scrolling the whole set of data.
<img src="https://i.sstatic.net/whNOw.png" alt="SELECT * FROM ResultTable10 WHERE Step = 508 AND Loop = 125;"></p>

<pre><code>SELECT * FROM ResultTable10 WHERE Step = 508 AND Loop = 124;
</code></pre>

<p>But now the query on the Loop = 124 does not show any result about what I've seen previously.
<img src="https://i.sstatic.net/kHzQh.png" alt="SELECT * FROM ResultTable10 WHERE Step = 508 AND Loop = 124;"></p>

<pre><code>SELECT * FROM ResultTable10 WHERE Step = 508 AND Loop BETWEEN 124 AND 125;
</code></pre>

<p>It seems fine if both Loops are passed in the WHERE clause
<img src="https://i.sstatic.net/MTUt6.png" alt="SELECT * FROM ResultTable10 WHERE Step = 508 AND Loop BETWEEN 124 AND 125;"></p>

<p>Does anybody else have already experienced this inconsistency, any potential fix, workaround (except rewriting all the data or performing massive query)?</p>

<p>Possibly where does this behavior come from? (Data Corruption, typos in my SQL statements, etc.)</p>

<p>EDIT:
It seems that I'm having some corruption issues, I tried to dig a bit more with the System.Data.SQLite .NET library and I ended up with some queries on 
that
:
<img src="https://i.sstatic.net/Ila5V.png" alt="System.Data.SQLite .NET Library"></p>

<p>Any general guidelines to prevent from those annoying corruptions?
(I've already checked that one here: <a href="http://www.sqlite.org/howtocorrupt.html" rel="nofollow noreferrer">http://www.sqlite.org/howtocorrupt.html</a>)</p>

