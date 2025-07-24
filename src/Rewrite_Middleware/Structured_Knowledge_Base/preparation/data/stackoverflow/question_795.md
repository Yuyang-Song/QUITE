# How to avoid joins between fact tables in a star schema?
[Link to question](https://stackoverflow.com/questions/42629656/how-to-avoid-joins-between-fact-tables-in-a-star-schema)
**Creation Date:** 1488814687
**Score:** 6
**Tags:** database-design, data-warehouse, star-schema
## Question Body
<p>I'm trying to model my data warehouse using a star schema but I have a problem to avoid joins between fact tables.<br>
To give a trivial idea of my problem, I want to collect all the events who occur on my operating system. So, I can create a fact table <code>event</code> with some dimensions like <code>datetime</code> or <code>user</code>. The problem is I want to collect different kinds of event: hardware event and software event.<br>
The problem is those events have not the same dimensions. By instance, for a hardware event, I can have <code>physical_component</code> or <code>related_driver</code> dimensions and, for a software event, <code>software_name</code> or <code>online_application</code> dimensions (that is just some examples, the idea to keep in mind is the fact <code>event</code> can be specialized into some specific events with specific dimensions).<br>
In a relational model, I would have 3 tables organized like that:
<a href="https://i.sstatic.net/Bgy2P.png" rel="noreferrer"><img src="https://i.sstatic.net/Bgy2P.png" alt="enter image description here"></a>
<br>The problem is : how to handle joins between fact tables in a star schema?<hr>
I imagined 4 ideas but I'm not sure one of them are adapted to the situation.<br>
<strong>The first one</strong> is to keep the model used in a relational database and add the dimension tables like that:<br>
<a href="https://i.sstatic.net/e2ZHy.png" rel="noreferrer"><img src="https://i.sstatic.net/e2ZHy.png" alt="enter image description here"></a>
<br>In this case, the problem is we still have join between fact tables and need to use <code>JOIN</code> SQL statement in all of our queries.
<hr><strong>The second one</strong> is to create only 2 fact tables who will duplicate the shared dimensions (datetime and user) and to create a materialized view event who summarized all the events:
<br>
<a href="https://i.sstatic.net/ebcXa.png" rel="noreferrer"><img src="https://i.sstatic.net/ebcXa.png" alt="enter image description here"></a>
<br>
The problem here is: what happen if I want to make a query on the materialized view? According to what I read in the Oracle documentation, we don't have to make query directly on materialized view but we have to let the query rewrite process make its work.
<hr><strong>The third one</strong> is to create only one fact table who will contain all the information possible for an event (hardware or software):<br>
<a href="https://i.sstatic.net/FVRYj.png" rel="noreferrer"><img src="https://i.sstatic.net/FVRYj.png" alt="enter image description here"></a>
<br>This time, the problem is my fact table will contain a lot of <code>NULL</code> value.
<hr>And <strong>the last one</strong> is to create 3 fact tables (without materialized view this time) like this:<br>
<a href="https://i.sstatic.net/RgX02.png" rel="noreferrer"><img src="https://i.sstatic.net/RgX02.png" alt="enter image description here"></a>
<br>This time, the problem is all events are present in the fact table <code>event</code> and in its own table. Because we will store a huge quantity of data, I'm not sure this duplication is a good idea.
<br>
So what is the best solution? Or does it exist a fifth solution?</p>

## Answers
### Answer ID: 42651147
<p>Events should be a single fact.  If you split them in two, you'll have a difficult time doing aggregations across both.  </p>

<p>If necessary, you can have separate hardware and software attribute dimensions, but you should have a generic event dimension, even if it is just a junk dimension with a few simple attributes, e.g. type (hardware/software), criticality (high, low), etc.</p>

<p>On a side note, I've generally seen the diagrams with the arrows coming from the fact going to the dimensions.  The fact table keys look at the dimensions rather then the other way around.</p>

### Answer ID: 42643671
<p>From your description and your subsequent comments to other answers, I'd say that option 2 or option 4 are the right way to model things from a dimensional modelling perspective. Each fact should be a measure of a business process, and the dimensionality of software and hardware events seems to be sufficiently different that they warrant being stored separately.</p>

<p>Then, there's a case for also storing the separate events table as a view, materialised view, or plain-ol' table storing the things that are common.</p>

<p>Once you've decided that's the right way to model things 'logically', you then need to balance performance, maintainability, usability and storage.
For dimensional modelling, usability and performance of queries take top priority (otherwise you may as well not use a dimensional model at all), and the extra work in ETL, and extra space needed, are prices worth paying.</p>

<p>A non-materialised view would save you the space at the price of performance, but it could be that you could give it a sufficiently awesome index or two that would mitigate that. A materialised view will give you performance at the price of storage.</p>

<p>I'd be tempted to create the two fact tables with indexes and a non-materialised view, and see what performance of that is like before taking further performance enhancing steps. 10 million fact rows isn't so bad, it might still perform.</p>

<p>A materialized view can be queried directly. But if you want to, you can use the query rewrite capabilities of Oracle so that the Materialized view is instead used as a performance-enhancer, like an index, when you're querying the original tables.
See here for details: <a href="http://www.sqlsnippets.com/en/topic-12918.html" rel="nofollow noreferrer">http://www.sqlsnippets.com/en/topic-12918.html</a>
Whether you choose to use it in query rewrite mode or just as a view in its own right depends on whether you want the users to know about this extra table, or for it to just sit in the background as a helpful friend.</p>

### Answer ID: 42633811
<p>You would never/rarely join fact tables together.  You may join aggregated facts which share (conformed) dimensions (i.e. Number of software events per hour compared with number of hardware events per hour).</p>

<p>To me, you always have to consider the kinds of questions that are going to be asked when looking at dimensional modeling.</p>

### Answer ID: 42633755
<p>There doesn't seem to be a reason in your scenario to combine or link the two types of events. Having said that, you may have some reason you did not describe (for example, collecting logs from many systems and wanting to see them together easily).</p>

<p>So my advice is to make a single fact table with both hardware and software dimension keys. One of them is always going to be 0 or -1 (= default 'n/a' record). </p>

<p>This allows you to aggregate them together without UNION statements or other complicated logic and can even support events that are linked to both hardware and software if they appear in the future.</p>

