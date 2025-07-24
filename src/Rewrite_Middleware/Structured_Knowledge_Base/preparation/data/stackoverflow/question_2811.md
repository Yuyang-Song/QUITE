# How is more correct to get this data with spring-data-jpa?
[Link to question](https://stackoverflow.com/questions/53633419/how-is-more-correct-to-get-this-data-with-spring-data-jpa)
**Creation Date:** 1544016361
**Score:** -2
**Tags:** java, postgresql, spring-boot, spring-data-jpa, nativequery
## Question Body
<p>For example I need show statistic table on web page. This table consists of 5 rows:</p>

<pre><code>AVG-rating | 5
TotalSum   | 12.1
SumToday   | 2.1
SummMonth  | 8.6
SomeElse   | 666 
</code></pre>

<p>Each value in this table - calculated using an aggregate function in a database.</p>

<p><strong>Question</strong>: How is more correct to get this data with <code>spring-data-jpa</code>?</p>

<p>Now I have One service - <code>StatisticService</code> with public methos <code>getStatistic(user);</code></p>

<p>In this method I call <code>5 methods</code> from <code>repository</code> for each statistic value and form response. Each repository method - <code>native query</code>.</p>

<p>I do not like this aproach. And I think best way is create <code>View</code> in <code>database</code> and select all statistic <strong>in one query to view</strong>. </p>

<p>But this aproach I do not like too. Because I'm tied to the base. and the base contains logic. Although in the first case I use native queries, but I can rewrite them to <code>JPQL</code> (but maybe not all).</p>

<p>How to more correctly extract aggregated information from the database with <code>spring-data-jpa</code>? </p>

## Answers
### Answer ID: 53633554
<p>Since you have all the values calculated inside DB I do not see any opportunities rather than you call every 5 queries. Otherwise you need to implement this calculation logic inside your code</p>

