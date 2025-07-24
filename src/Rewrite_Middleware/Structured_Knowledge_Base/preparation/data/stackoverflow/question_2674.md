# PostgreSQL hierarchy(?) structure
[Link to question](https://stackoverflow.com/questions/46223960/postgresql-hierarchy-structure)
**Creation Date:** 1505405706
**Score:** 0
**Tags:** postgresql, hierarchy
## Question Body
<p>Please excuse my ignorance.  I'm certain this is a FAQ, but I don't know the terminology well enough to know what to look for.</p>

<p>My company uses the following structure in terms of territory (example following):</p>

<pre><code>  Customer -&gt; Market -&gt; Area -&gt; District -&gt; Region
  XYZ Co. -&gt; Queens -&gt; NYC -&gt; Mid Atlantic -&gt; Northeast
</code></pre>

<p>Each customer has only one market.  Each market has only one district, and so forth.  (I'm not sure if you'd call that one-to-many or many-to-one.  I don't want to label it incorrectly).</p>

<p>This is how I have things set up right now:</p>

<pre><code>create table region(
id           int  not null primary key,
name         varchar(24)
);

create table district(
id           int  not null primary key,
name         varchar(24),
region_id    int  references region(id) on update cascade
);

create table area(
id           int  not null primary key,
name         varchar(24),
district_id  int  references district(id) on update cascade
);

create table market(
id           int  not null primary key,
name         varchar(24),
area_id      int  references area(id) on update cascade
);
create table customer(
id         int  not null primary key,
name       varchar(32),
sixweekavg numeric, 
market_id  int  references market(id) on update cascade
);
</code></pre>

<p>Right now I have an opportunity to improve that setup as I'm more or less rewriting the site.  I looked at this popular page:
<a href="https://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database">What are the options for storing hierarchical data in a relational database?</a>
And I'm sure that my best scenario lies there, but I don't know enough to figure out which one.</p>

<p>It's a reporting site, so there are way more reads than writes.  Some of my pages show aggregated data at each level, customer through region (and top, too).  So right now on a page that shows district-level data I would write something like:</p>

<pre><code>select d.name, sum(sixweekavg) as avg from customer c
  inner join market m on m.id = c.market_id
  inner join area a on a.id = m.area_id
  inner join district d on d.id = a.district_id
  group by d.name order by d.name;
</code></pre>

<p>Pretty standard stuff, right?  I'm sure a whole separate conversation could be had about materialized views, but for now I'd like to explore a better option for structuring the hierarchy (if that's even the correct term for this).</p>

<p>So given the following summary</p>

<ul>
<li>PostgreSQL (it can be assumed this will not change)</li>
<li>Fixed hierarchy (my employer may at some point add or remove a tier, but every row in the customer table will always have the same number of "parents")</li>
<li>Significantly more reads than writes</li>
</ul>

<p>Is there one method that may be better than the others for setting this up?</p>

<p><strong>ltree</strong></p>

<p>I did look at ltree, but I'm not quite sure how that would work.  On pages where a user can select a district, for example, I query the district table for the names of each district.  I had the idea to add an ltree column in my customers table which would hold the hierarchy, but still maintain the other tables.  Is that a feasible and reasonable approach? I've searched for real-world examples of ltree but came up short - most that I found were designed for a random number of parent/child nodes, like a threaded comment section.</p>

<p>I appreciate your help and your patience!</p>

