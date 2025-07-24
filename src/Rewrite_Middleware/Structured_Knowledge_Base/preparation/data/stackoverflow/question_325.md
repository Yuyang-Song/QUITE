# Multiple tables or a single big one (MySQL)
[Link to question](https://stackoverflow.com/questions/20675803/multiple-tables-or-a-single-big-one-mysql)
**Creation Date:** 1387438264
**Score:** 0
**Tags:** mysql
## Question Body
<p>We are a gaming website and we are storing scores obtained in a MySQL database. The whole system was pretty outdated and we are currently working on rewriting everything.</p>

<p>We currently have one table per level, with about 2000 levels, a couple more added each week. Each table has from ten thousand to about a million lines.</p>

<p>Now that we are restructuring everything, we were wondering if we should merge everything into a single table or keep the current system.</p>

<p>Most of the queries we are running are on a single table. Finding a user current score. Add a high score. But when a user decides to look at the page where it lists all his scores, it gets ugly. We have to loop through the tables and execute 2000+ queries to fill the page. This page is rarely run though compared to the single-table queries.</p>

<p>Any pointers on how to handle the situation would be greatly appreciated!</p>

## Answers
### Answer ID: 20675886
<p>If I were you I would look at adding everything to one table as they are all related to the same entity.</p>

<p>If you do decide to do this you will have to make sure you apply the perfect indexing on that one table to ensure that it performs optimally. With great indexing you can make that table very fast even though it has millions of rows in it. I did it just this week for a project of my own.</p>

