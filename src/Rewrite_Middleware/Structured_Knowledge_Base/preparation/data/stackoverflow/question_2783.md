# SQL - ACID relationships between two varying entities
[Link to question](https://stackoverflow.com/questions/52163183/sql-acid-relationships-between-two-varying-entities)
**Creation Date:** 1536053567
**Score:** 0
**Tags:** sql, sql-server, database, acid
## Question Body
<p><em>Let's say there is a a system and you have three entities:</em></p>

<ul>
<li>User</li>
<li>Team (group of users)</li>
<li>Role</li>
</ul>

<p><em>And you want to setup up some permission relationships, with the flexibility in the database anyway, to say:</em></p>

<ul>
<li>User X can change permissions of User Y</li>
<li>User X can change permissions of Team Y</li>
<li>User X can change permissions of Role Y</li>
<li>Team X can change permissions of Role Y</li>
<li>Team X can change permissions of Team Y</li>
<li>Role X can change permissions of Team Y</li>
<li>Role X can change permissions of Role Y</li>
</ul>

<p><em>With a similar scenario, I currently have a table with the following schema:</em></p>

<ul>
<li>SubjectType (User | Team | Role)</li>
<li>SubjectId <em>(integer - not foreign key)</em></li>
<li>TargetType (User | Team | Role)</li>
<li>TargetId <em>(integer - not foreign key)</em></li>
</ul>

<p><em>This is allows all the relationships to be specified in one place, however, as there are no specified relationships, it has the problem:</em></p>

<ul>
<li>Role A is configured with access to teams with team IDs X,Y,Z</li>
<li>Teams Y and Z are removed with no errors elsewhere</li>
<li>When querying targets for Role A, the team IDs Y and Z are still returned.</li>
</ul>

<p><em>As it stands, I can see two options, each with compromise involved (pros = +, cons = -):</em></p>

<p><strong>1. Leave as is with data in one place but remove orphaned permission relationships when the entity is removed.</strong></p>

<ul>
<li>(+) Keeps one table and single query simplicity
and manually remove team permission entries when a team is removed</li>
<li>(-) Will require 3 manual deletion operations (User | Team | Role). Whilst there would be a single deletion function where this could take place in a repeatable manner, there is no hard and fast guarantree</li>
</ul>

<p><strong>2. Specify each relationship in its own table.</strong></p>

<ul>
<li>(+) ACID guarantee will prevent entries becoming orphaned</li>
<li>(-) Much greater table verbosity, 7-9 tables for basically the same thing</li>
<li>(-) More queries, more joins (specially if using class table inheritance)</li>
</ul>

<p>I'm kind of leaning towards the second option with the thought of adding the extra complexity below and abstracting it into single access functions and am thinking that is worth the extra work (involves a bit of a rewrite).</p>

<p>However, I am wondering if there is a different option I have missed, or if there are some strong experienced based recommendations on this problem?</p>

<p>Using SQL Server 2012 with this setup but I imagine this to be a generic SQL / database issue.</p>

