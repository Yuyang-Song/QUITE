# Finding count of occurrences from a table of unique values
[Link to question](https://stackoverflow.com/questions/58468176/finding-count-of-occurrences-from-a-table-of-unique-values)
**Creation Date:** 1571520640
**Score:** -1
**Tags:** mysql, join, count
## Question Body
<p>I have a movie database with three tables. Filmparticipation, Person and Filmcharacter </p>

<p>My problem is that I have to find every actor that has acted as a unique character in over 200 movies. </p>

<p>An unique character, is an character that only shows up once in the filmcharacter table. </p>

<p>I think that I have found the table of unique characters with the following query</p>

<pre><code>SELECT filmcharacter.partid FROM filmcharacter GROUP BY 
filmcharacter.partid HAVING count(*) = 1;
</code></pre>

<p>I rewrite this as a WITH statement in the form of</p>

<pre><code>WITH unique_table(partid) AS (SELECT partid FROM filmcharacter GROUP 
BY partid HAVING count(*) = 1)
</code></pre>

<p>However I am unsure how to further solve this problem. I was planning on using WITH to create a table with the data that I need, then selecting the rows that I want, joining them with relevant things.</p>

<pre><code>   WITH unique_table(partid) AS (SELECT partid FROM filmcharacter 
   INNER 
   JOIN filmparticipation ON(filmcharacter.partid = 
   filmparticipation.partid) INNER JOIN person(person.personid = 
   filmparticipation.personid) GROUP 
   BY partid)
</code></pre>

<p>I'm not sure how to move onwards next I have tried</p>

<pre><code>   WITH unique_table(partid) AS (SELECT partid FROM filmcharacter 
   INNER 
   JOIN filmparticipation ON(filmcharacter.partid = 
   filmparticipation.partid) INNER JOIN person(person.personid = 
   filmparticipation.personid) GROUP 
   BY partid) SELECT * FROM unique_table GROUP BY partid HAVING 
   count(partid) &gt; 200;
</code></pre>

<p>But If send that, I get query zero tables.</p>

<p>The tables have the following keys:</p>

<pre><code>Filmparticipation(personid, partid)

Filmcharacter(partid)

Person(personid)
</code></pre>

<p>What I expect to get is something along the lines of a table. That has an Id that identifies the actor (personid) and the count of times they have appeared acting as a unique character</p>

<pre><code>  Actor       Count
----------|----------
     1        201
     2        309
</code></pre>

## Answers
### Answer ID: 58468246
<p>You could join the table <code>person</code> with <code>filmparticipation</code> and use <code>not exists</code> to ensure that the same <code>partid</code> does not occur another time in the <code>filmparticipation</code>:</p>

<pre><code>select p.personid, count(*) as `count`
from person p
inner join filmparticipation fp on fp.personid = p.personid
where not exists (
    select 1
    from filmparticipation fp1
    where fp1.partid = fp.partid and fp.personid != p.personid
)
group by p.personid
having count(*) &gt; 200
</code></pre>

<p>If you are running MySQL 8.0, this can also be achieved with a window count:</p>

<pre><code>select personid, count(*)
from (
    select p.personid, count(*) over(partition by fp.partid) cnt
    from person p
    inner join filmparticipation fp on fp.personid = p.personid
) x
where cnt = 1
group by person_id
having count(*) &gt; 200
</code></pre>

