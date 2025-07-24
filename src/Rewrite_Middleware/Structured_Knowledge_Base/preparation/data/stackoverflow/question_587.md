# Hibernate generating bad syntax sql
[Link to question](https://stackoverflow.com/questions/32751191/hibernate-generating-bad-syntax-sql)
**Creation Date:** 1443051728
**Score:** 4
**Tags:** hibernate, postgresql
## Question Body
<p>There are two tables: bb_players and bb_player_skills.
player skills table has one to one relation with bb_players, and also foreign key to bb_players.</p>

<p>Error happens at executing this code:</p>

<pre><code>Query q = em.createNamedQuery(PlayerSkill.DELETE_SKILL_BY_PLAYER_ID);
q.setParameter("playerID", playerID);
q.executeUpdate();
</code></pre>

<p>The named query is:</p>

<pre><code> @NamedQuery(name = PlayerSkill.DELETE_SKILL_BY_PLAYER_ID, query = "DELETE FROM   PlayerSkill s " +
 " WHERE s.player.id = :playerID")
</code></pre>

<p>The error from postgresql logs is:</p>

<pre><code>ERROR,42601,"syntax error at or near ""cross""",,,,,, 
 "delete from bb_player_skills cross join bb_players player1_ where id=$1",30,,""
</code></pre>

<p>Is my named query wrong and how should I rewrite it?</p>

## Answers
### Answer ID: 55076316
<p>In case anyone else faces the same problem,Here is one solution.<br>The named query can be rewritten to avoid join cross. </p>

<pre><code>@NamedQuery(name = "PlayerSkill.DELETE_SKILL_BY_PLAYER_ID", query = "DELETE FROM   PlayerSkill s " +
 " WHERE s.player IN (SELECT player FROM Player player where player.id=:playerID)")
</code></pre>

### Answer ID: 32761005
<p>It appears that this may be an open Hibernate issue depending on your Hibernate version.</p>

<p>From: <a href="https://hibernate.atlassian.net/browse/HHH-7314" rel="noreferrer">https://hibernate.atlassian.net/browse/HHH-7314</a></p>

<blockquote>
  <p>Using a JPA Delete query with conditions requiring a join through Hibernate entity-manager generates invalid SQL for PostgreSQL.
  PostgreSQL cannot use CROSS JOIN in the FROM clause of a DELETE query.</p>
</blockquote>

### Answer ID: 32759203
<p>Looks like it is not a one to one relation. From bb_players it shoutd be a one to many relation, from bb_player_skills it should be a many to one relation.</p>

