# Database Performance Solution - &quot;View Caching&quot; - Is this a good idea?
[Link to question](https://stackoverflow.com/questions/3912909/database-performance-solution-view-caching-is-this-a-good-idea)
**Creation Date:** 1286873345
**Score:** 1
**Tags:** sql-server, database-design, relational-database
## Question Body
<p><strong>A little context first:</strong></p>

<p>I would say I have good SQL server experience, but am a developer, not a DBA. My current task is to improve on the performance of a database, which has been built with a very heavy reliance on views. The application is peppered with inline sql, and using Tuning Advisor only suggests a couple of missing indexes, which look reasonable.</p>

<p>I feel that reworking the database design so that the data created by these particular views (lots of CASE WHENS) is persisted as hard data is too much work given the budget and time scales here. A full rewrite of these enormous views and all of the code that relies on them also appears to be out of the question.</p>

<p><strong>My proposed solution:</strong></p>

<p>Testing has shown that if I do a SELECT INTO with the view data to persist it in permenant table, and then replace references to the view with this table, query times go down to 44% of what they were when using the view.</p>

<p>Since the data is refreshed by a spider process overnight, I think I can just drop and recreate this table on a daily basis, and then make minor modifications to the queries to use this view.</p>

<p>Can someone with good DBA experience give me an opinion on whether that is a good / *&amp;?!! awful idea. If the latter, is there a better way to approach this?</p>

<p>Thanks.</p>

## Answers
### Answer ID: 3913001
<p>You say: "...reworking the database design so that the data created by these particular views ... is persisted as hard data is too much work given the budget and time scales here." and yet this is exactly what you are proposing to do. It's just that you use the views themselves instead of making the code a function or a stored procedure.</p>

<p>Anyway, my opinion is that if you invest a bit of effort in making this robust (i.e. you ensure that if the spider runs, the persisted data always get refreshed, and you never run the select-into before the end of the spidering) your solution is ok.</p>

<p>What would concern me is that this is a hack - however brilliant - so whoever inherits your solution may find it difficult to understand the why and how. See if you can provide a good explanation either by comments or a seperate document.</p>

