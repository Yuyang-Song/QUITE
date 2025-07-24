# How to avoid distinct
[Link to question](https://stackoverflow.com/questions/10347552/how-to-avoid-distinct)
**Creation Date:** 1335516312
**Score:** 7
**Tags:** mysql, sql, distinct
## Question Body
<p>I have a query which works when I use DISTINCT. However I have a feeling I could rewrite the query in a way that would help me avoid use of DISTINCT, which would make easier(quicker) for the database to process the query. </p>

<p>If there is no point in rewriting the query, please explain, if there is, please look at simplified query and give me a hint how to reformulate it so I wouldn't get duplicates in the first place.</p>

<pre><code>SELECT Us.user_id, COUNT( DISTINCT Or.order_id ) AS orders
FROM users AS Us
LEFT JOIN events AS Ev ON Ev.user_id = Us.user_id
LEFT JOIN orders AS Or ON Or.event_id = Ev.event_id
OR Or.user_id = Us.user_id
GROUP BY Us.user_id
</code></pre>

<p>Short description of the query: I have a table of users, of their events and orders. Sometimes orders have column user_id, but mostly it is null and they have to be connected via event table.</p>

<p>Edit:</p>

<p>These are results of the simplified query I wrote, first without distinct and then including distinct.</p>

<pre><code>user_id orders
3952    263
3953    7
3954    2
3955    6
3956    1
3957    0
...

user_id orders
3952    79
3953    7
3954    2
3955    6
3956    1
3957    0
...
</code></pre>

<p>Problem fixed:</p>

<pre><code>SELECT COALESCE( Or.user_id, Ev.user_id ) AS user, COUNT( Or.order_id ) AS orders
FROM orders AS Or
LEFT JOIN events AS Ev ON Ev.event_id = Or.event_id
GROUP BY COALESCE( Or.user_id, Ev.user_id )
</code></pre>

## Answers
### Answer ID: 10349464
<p>You are not getting anything from the user table, nor the events table, so why join them.  Your last "OR" clause makes explicit reference that it has a user_ID column.  I would hope your order table has an index on the user ID placing the order, then you could just do</p>

<pre><code>select
      user_id,
      count(*) as Orders
   from
      orders
   group by
      user_id
</code></pre>

### Answer ID: 10348872
<p>If an order can be associated with multiple events, or a user with an event multiple times, then it is possible for the same order to be associated with the same user multiple times.  In this scenario, using <code>DISTINCT</code> will count that order only once per user whereas omitting it will count that order once for each association with the user.</p>

<p>If you're after the former, then your existing query is your best option.</p>

