# In MySQL is there a way to chose one column over another when doing SELECT *?
[Link to question](https://stackoverflow.com/questions/46699455/in-mysql-is-there-a-way-to-chose-one-column-over-another-when-doing-select)
**Creation Date:** 1507767410
**Score:** 1
**Tags:** mysql, sql, select
## Question Body
<p>Ok, for a moment, throw out of your mind "good database design". Let's say I have two tables, and they have some of the same columns.</p>

<pre><code>item
-------
id
title
color
</code></pre>

<p>and</p>

<pre><code>item_detail
-------
id
weight
color
</code></pre>

<p>In a good normal query, you'd choose the columns you want within the query, like so:</p>

<pre><code>SELECT item.title, item_detail.color, item_detail.weight ...
</code></pre>

<p>But what if you are stuck with a query that was built with star/all: </p>

<pre><code>SELECT * ...
</code></pre>

<p>In this case you would get two <code>color</code> columns pulled back in your results, one for each table. Is there a way in MySQL to chose one <code>color</code> column over the other, so only one shows up in the results, without a full rewrite of the statement? So that I could say that the table <code>item_detail</code> takes priority?</p>

<p>Probably not but I thought I'd ask.</p>

## Answers
### Answer ID: 46699526
<p>Err. No there is not.<br>
But define "without a full rewrite of the statement". As far as I can see you'd just need to rewrite the <code>select *</code> portion of the query.<br>
If you cannot touch the statement at all, then you are free to ignore the column in your application (the order of the columns does not change between calls)... or you could create a view...<br>
It's hard to know which constraints you are dealing with when you say "But what if you are stuck with a query".</p>

